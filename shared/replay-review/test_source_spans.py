"""Independent original-byte checks for the cross-line citation handoff."""
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import replay_review as r


class SourceSpanTests(unittest.TestCase):
    def review(self, data, omit=False):
        pack = r.replay.make_pack([('missing/original.jsonl', data)], omit)
        return r.review_bytes(r.replay.canonical(pack))

    def decoded(self, result):
        return [v for v in result['reviews'] if v['domain'] == 'decoded-json-line']

    def assert_spans(self, data, result):
        for entry in self.decoded(result):
            self.assertEqual(entry['source_sha256'], hashlib.sha256(data).hexdigest())
            line_span = entry['source_span']
            begin, end = line_span['byte_start'], line_span['byte_end']
            raw_line = data[begin:end]
            self.assertEqual(hashlib.sha256(raw_line).hexdigest(), line_span['sha256'])
            self.assertEqual(entry['report']['sha256'], line_span['sha256'])
            for finding in entry['report'].get('findings', []):
                for key, absolute in finding['embedded_source_spans'].items():
                    local = finding[key]
                    a, b = absolute['byte_start'], absolute['byte_end']
                    self.assertEqual((a, b), (begin + local['byte_start'], begin + local['byte_end']))
                    piece = data[a:b]
                    self.assertEqual(piece, raw_line[local['byte_start']:local['byte_end']])
                    self.assertEqual(hashlib.sha256(piece).hexdigest(), absolute['sha256'])
                    self.assertEqual(absolute['sha256'], local['sha256'])
                    self.assertEqual(absolute['bytes'], len(piece))

    def test_bom_crlf_multibyte_prior_lines_absolute_offsets(self):
        data = b'\xef\xbb\xbf2026-10-18T10:00:00Z ' + 'é🐸'.encode() + b'\r\n\r\n' + br'{"ts":1792317602000,"message":"\ud83d\udc38\u202e"}' + b'\r\n'
        result = self.review(data)
        self.assert_spans(data, result)
        entry = self.decoded(result)[0]
        self.assertEqual(entry['physical_line'], 3)
        f = entry['report']['findings'][0]
        self.assertEqual(f['embedded_source_spans']['source_focus']['byte_start'], data.index(br'\u202e'))
        self.assertEqual(entry['source_span']['byte_end'], len(data)-2)

    def test_bom_on_first_json_line_excluded_from_local_domain(self):
        data = b'\xef\xbb\xbf  ' + br'{"ts":1792317602000,"message":"\u202e"}'
        result = self.review(data)
        self.assert_spans(data, result)
        self.assertEqual(self.decoded(result)[0]['source_span']['byte_start'], 3)

    def test_duplicate_omitted_line_both_spellings_remain(self):
        data = br'{"ts":1792317602000,"owner":0,"\u006fwner":1,"message":"\u202e"}' + b'\r\n'
        result = self.review(data, True)
        self.assertEqual(result['replay']['omitted'], 1)
        self.assert_spans(data, result)
        findings = self.decoded(result)[0]['report']['findings']
        duplicate = next(f for f in findings if f.get('rule') == 'duplicate-key')
        spans = duplicate['embedded_source_spans']
        a=spans['source_token']; b=spans['first_source_token']
        self.assertEqual(data[a['byte_start']:a['byte_end']], br'"\u006fwner"')
        self.assertEqual(data[b['byte_start']:b['byte_end']], b'"owner"')

    def test_raw_literal_and_decoded_citations_agree(self):
        data = ('{"ts":1792317602000,"message":"é' + chr(0x202E) + '"}\n').encode()
        result = self.review(data)
        self.assert_spans(data, result)
        focus = [f['embedded_source_spans']['source_focus'] for f in self.decoded(result)[0]['report']['findings']]
        self.assertEqual(focus[0], focus[1])

    def test_invalid_omitted_json_keeps_original_span(self):
        data=b'2026-10-18T10:00:00Z ok\n  {broken\r\n'
        result=self.review(data, True)
        self.assertEqual(result['review_errors'],1)
        self.assertEqual(result['assessment'],'review-required')
        self.assert_spans(data,result)
        self.assertEqual(self.decoded(result)[0]['physical_line'],2)

    def test_non_json_unicode_whitespace_prefix_is_review_error(self):
        data=('\u00a0'+ '{"ts":1792317602000,"message":"ok"}').encode()
        result=self.review(data,True)
        self.assertEqual(result['review_errors'],1)
        self.assertEqual(result['assessment'],'review-required')
        self.assert_spans(data,result)

    def test_tampered_pack_rejected_before_citation_review(self):
        pack=r.replay.make_pack([('x',br'{"ts":1792317602000,"message":"\u202e"}')])
        pack['timeline']['events'][0]['message']='changed'
        with patch.object(r.json_citations,'review',side_effect=AssertionError('must not review')):
            with self.assertRaises(ValueError):
                r.review_bytes(r.replay.canonical(pack))

    def test_retained_listing_cap_keeps_full_counts_and_valid_spans(self):
        data=(br'{"ts":1792317602000,"message":"\u202e"}' + b'\r\n')*3
        with patch.object(r,'MAX_RETAINED_REVIEWS',1):
            result=self.review(data)
        self.assertTrue(result['listings_truncated'])
        self.assertEqual(result['finding_count'],3)
        self.assertEqual(len(self.decoded(result)),1)
        self.assert_spans(data,result)

    def test_generated_unicode_and_line_endings(self):
        # Independent slice/hash oracle across byte shifts and escaped spellings.
        for prefix in ('','é','🐸','é🐸'):
            for newline in (b'\n',b'\r\n'):
                data=('2026-10-18T10:00:00Z '+prefix).encode()+newline
                data+=json.dumps({'ts':1792317602000,'message':prefix+chr(0x202E)},ensure_ascii=False).encode()+newline
                self.assert_spans(data,self.review(data))

    def test_copied_folder_has_no_line_runtime_dependency(self):
        scratch=Path('test/scratch');scratch.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            target=Path(directory)/'portable'
            shutil.copytree(Path(r.__file__).parent,target)
            run=subprocess.run([sys.executable,'-B','replay_review.py','demo'],cwd=target,capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr)
            result=json.loads(run.stdout)
            self.assertEqual(result['tool_version'],'1.1.0')
            self.assertTrue(result['replay']['verified'])
            self.assertTrue(all('embedded_source_spans' in f for entry in self.decoded(result) for f in entry['report']['findings']))


if __name__=='__main__':
    unittest.main()
