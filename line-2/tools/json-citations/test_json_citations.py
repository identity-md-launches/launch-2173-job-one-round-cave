import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

import json_citations as tool


class CitationTests(unittest.TestCase):
    def check_citations(self, raw):
        report = tool.review(raw)
        for finding in report['findings']:
            for field in ('source_token', 'first_source_token', 'source_focus', 'first_source_focus'):
                if field not in finding:
                    continue
                citation = finding[field]
                start, end = citation['byte_start'], citation['byte_end']
                self.assertTrue(0 <= start < end <= len(raw))
                span = raw[start:end]
                self.assertEqual(citation['bytes'], len(span))
                self.assertEqual(citation['sha256'], hashlib.sha256(span).hexdigest())
                self.assertTrue(citation['excerpt_escaped_bytes'].isascii())
                self.assertEqual(citation['excerpt_truncated'], len(span) > 96)
                if field.endswith('token'):
                    self.assertIsInstance(json.loads(span), str)
                elif finding['domain'] == 'decoded-string':
                    evidence = finding['evidence'] if field == 'source_focus' else finding['evidence']['first']
                    # An independently decoded JSON fragment must reproduce the
                    # exact scanner evidence, not merely contain a suspicious char.
                    decoded = json.loads(b'"' + span + b'"')
                    self.assertEqual(tool.lantern.lantern.escaped(decoded), evidence['escaped'])
                else:
                    evidence = finding['evidence'] if field == 'source_focus' else finding['evidence']['first']
                    self.assertEqual(tool.lantern.lantern.escaped(span.decode()), evidence['escaped'])
        return report

    def test_demo_all_findings_have_citations(self):
        report = self.check_citations(tool.DEMO)
        self.assertEqual(report['finding_count'], 5)
        self.assertEqual(report['sha256'], hashlib.sha256(tool.DEMO).hexdigest())
        self.assertTrue(all('source_token' in f for f in report['findings']))

    def test_duplicate_spelling_quotes_and_original_escape_are_retained(self):
        raw = br'{"owner":0,"\u006fwner":1}'
        finding = self.check_citations(raw)['findings'][0]
        self.assertEqual(raw[finding['source_token']['byte_start']:finding['source_token']['byte_end']], br'"\u006fwner"')
        self.assertEqual(raw[finding['first_source_token']['byte_start']:finding['first_source_token']['byte_end']], b'"owner"')
        self.assertNotEqual(finding['source_token']['sha256'], finding['first_source_token']['sha256'])

    def test_nested_duplicate_keys_remain_unambiguous(self):
        raw = br'{"a/b~":[{"x":"\u202e","x":"\u200b"}],"a/b~":"\u2066"}'
        report = self.check_citations(raw)
        decoded = [f for f in report['findings'] if f['domain'] == 'decoded-string']
        self.assertEqual([raw[f['source_focus']['byte_start']:f['source_focus']['byte_end']] for f in decoded],
                         [br'\u202e', br'\u200b', br'\u2066'])
        self.assertEqual(decoded[1]['location'], [{'pair': 0, 'role': 'value'}, {'index': 0}, {'pair': 1, 'role': 'value'}])

    def test_multibyte_prefix_crlf_and_surrogate_pairs(self):
        raw = (' {"é": ["🐸", "').encode() + br'\ud83d\udc38\r\n\u00e9\u202e' + b'"]}\r\n'
        finding = self.check_citations(raw)['findings'][0]
        focus = finding['source_focus']
        self.assertEqual(focus['byte_start'], raw.index(br'\u202e'))
        self.assertEqual(focus['byte_end'] - focus['byte_start'], 6)

    def test_supplementary_variation_selector(self):
        for raw, width in [(br'"\udb40\udd00"', 12), (('"' + chr(0xE0100) + '"').encode(), 4)]:
            finding = self.check_citations(raw)['findings'][0]
            self.assertEqual(finding['source_focus']['bytes'], width)
            self.assertEqual(finding['evidence']['codepoint'], 'U+E0100')

    def test_identifier_collision_first_focus(self):
        raw = br'"owner \u043ewner"'
        report = self.check_citations(raw)
        finding = next(f for f in report['findings'] if f['evidence']['rule'] == 'lookalike-collision')
        self.assertEqual(raw[finding['first_source_focus']['byte_start']:finding['first_source_focus']['byte_end']], b'owner')
        self.assertEqual(raw[finding['source_focus']['byte_start']:finding['source_focus']['byte_end']], br'\u043ewner')

    def test_raw_and_decoded_domains_remain_distinct(self):
        raw = ('"é' + chr(0x202E) + '"').encode()
        report = self.check_citations(raw)
        self.assertEqual([f['domain'] for f in report['findings']], ['decoded-string', 'raw-json'])
        self.assertEqual(report['findings'][0]['source_focus'], report['findings'][1]['source_focus'])

    def test_json_escapes_and_control_characters(self):
        raw = br'{"quote\"slash\\solidus\/":"\b\f\t\n\r \u202e"}'
        report = self.check_citations(raw)
        self.assertEqual([f['evidence']['rule'] for f in report['findings']], ['control-character', 'control-character', 'bidi-control'])

    def test_long_excerpts_bounded_hash_full_token(self):
        raw = b'"' + b'a' * 2000 + br'\u202e"'
        finding = self.check_citations(raw)['findings'][0]
        self.assertTrue(finding['source_token']['excerpt_truncated'])
        self.assertEqual(len(finding['source_token']['excerpt_escaped_bytes']), 96)
        self.assertEqual(finding['source_focus']['excerpt_escaped_bytes'], r'\\u202e')

    def test_generated_valid_documents_have_roundtrippable_evidence(self):
        rng = random.Random(737)
        alphabet = ['a', 'é', '🐸', '"', '\\', '\n', '\t', chr(0x202E), chr(0xE0100), chr(0x200B)]
        for index in range(60):
            text = ''.join(rng.choice(alphabet) for _ in range(40))
            raw = json.dumps({'é': [index, {text: text}, text]}, ensure_ascii=index % 2 == 0).encode()
            self.check_citations(raw)

    def test_global_truncation_preserves_counts(self):
        full = tool.review(tool.DEMO)
        for limit in (1, 2, 3):
            result = tool.review(tool.DEMO, max_findings=limit)
            self.assertEqual(result['finding_count'], full['finding_count'])
            self.assertEqual(result['findings'], full['findings'][:limit])
            self.assertTrue(result['truncated'])

    def test_upstream_evidence_is_preserved(self):
        original = tool.lantern.review(tool.DEMO)
        cited = tool.review(tool.DEMO)
        for before, after in zip(original['findings'], cited['findings']):
            retained = {key: value for key, value in after.items()
                        if key not in {'source_token', 'first_source_token',
                                       'source_focus', 'first_source_focus'}}
            self.assertEqual(before, retained)
        self.assertEqual(original['finding_count'], cited['finding_count'])

    def test_cli_findings_exit_one_and_ascii_error(self):
        scratch = Path.cwd() / 'test' / 'scratch'
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            path = Path(directory) / 'input.json'
            path.write_bytes(tool.DEMO)
            result = subprocess.run([sys.executable, '-B', str(Path(tool.__file__)),
                                     '--file', str(path)], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)['finding_count'], 5)
            self.assertFalse(result.stderr)

    def test_strict_validation_and_budgets_still_apply(self):
        for raw in (b'{', b'NaN', b'"\xff"', br'"\ud800"', b'{} {}', b'\xef\xbb\xbf{}', b'[' * 65 + b'0' + b']' * 65):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                tool.review(raw)
        with self.assertRaises(ValueError):
            tool.review(b' ' * (tool.MAX_BYTES + 1))
        with self.assertRaises(ValueError):
            tool.review(b'{}', max_findings=True)

    def test_empty_scalar_numeric_and_max_depth(self):
        for raw in (b'{}', b'[]', b'""', b'null', b'true', b'false', b'9' * 5000,
                    b'1e999999', b'[' * 64 + b'"x"' + b']' * 64):
            self.assertEqual(tool.review(raw)['finding_count'], 0)

    def test_cli_demo_real_file_and_error(self):
        script = str(Path(tool.__file__))
        for arguments, expected in [(['--demo'], 0), (['--file', 'dist/line-2/22.json'], 0),
                                    (['--file', 'test/scratch/missing-citation-input.json'], 2),
                                    (['--file', '../outside.json'], 2)]:
            completed = subprocess.run([sys.executable, '-B', script] + arguments, capture_output=True)
            self.assertEqual(completed.returncode, expected)
            json.loads(completed.stdout)
            self.assertFalse(completed.stderr)


if __name__ == '__main__':
    unittest.main()
