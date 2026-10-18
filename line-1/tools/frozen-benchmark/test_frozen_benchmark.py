"""Protocol admission, independent byte checks, and real downstream compatibility."""
import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
import frozen_benchmark as fb


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.plan = {'schema': fb.SCHEMA, 'baseline': 'base-v1', 'candidates': ['a-v1', 'b-v1'],
                     'pass_rule': 'Exact expected output, one execution per case.',
                     'alpha': '0.05', 'cases': ['one', 'two', 'three']}
        self.manifest = fb.freeze(fb.canonical(self.plan))
        self.pin = self.manifest['plan_sha256']
        self.raw = b'case,baseline,a-v1,b-v1\nthree,0,1,0\none,1,1,1\ntwo,0,1,1\n'

    def check(self, raw=None, manifest=None, pin=None):
        return fb.check(fb.canonical(manifest or self.manifest),
                        self.raw if raw is None else raw, pin or self.pin)

    def test_complete_and_normalized_order(self):
        report, normalized = self.check()
        self.assertEqual(report['case_count'], 3)
        self.assertEqual(report['observation_bytes_sha256'], hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(report['normalized_csv_sha256'], hashlib.sha256(normalized).hexdigest())
        self.assertEqual(list(csv.reader(io.StringIO(normalized.decode())))[1][0], 'one')
        self.assertEqual(self.check(normalized)[1], normalized)

    def test_pin_uses_independent_canonical_definition(self):
        raw = (json.dumps(self.plan, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode()
        self.assertEqual(self.pin, hashlib.sha256(raw).hexdigest())
        plan = copy.deepcopy(self.plan)
        plan['alpha'] = '0.0500'
        self.assertEqual(fb.freeze(json.dumps(plan).encode()), self.manifest)
        pretty = json.dumps(self.manifest, indent=4).encode()
        self.assertEqual(fb.verify_manifest(pretty, self.pin), self.plan)

    def test_tampered_self_consistent_manifest_needs_old_pin(self):
        for field, value in [('baseline', 'base-v2'), ('pass_rule', 'Always pass'),
                             ('alpha', '0.1'), ('cases', ['one', 'two']),
                             ('candidates', ['a-v1', 'b-v2'])]:
            plan = dict(self.plan, **{field: value})
            new = fb.freeze(fb.canonical(plan))
            with self.subTest(field=field), self.assertRaises(fb.InputError):
                self.check(manifest=new)
        modified = copy.deepcopy(self.manifest)
        modified['plan']['alpha'] = '0.1'
        with self.assertRaises(fb.InputError):
            self.check(manifest=modified)

    def test_complete_case_set_required(self):
        for raw in [self.raw.rsplit(b'two', 1)[0], self.raw + b'extra,0,1,1\n',
                    self.raw + b'one,1,1,1\n', self.raw.replace(b'two,', b'four,')]:
            with self.subTest(raw=raw), self.assertRaises(fb.InputError):
                self.check(raw)

    def test_entire_family_and_order_required(self):
        for header in [b'case,baseline,a-v1', b'case,baseline,b-v1,a-v1',
                       b'case,baseline,a-v1,b-v2', b'case,baseline,a-v1,b-v1,c-v1']:
            with self.subTest(header=header), self.assertRaises(fb.InputError):
                self.check(header + b'\none,1,1,1\n')

    def test_csv_errors_fail_without_omission(self):
        variants = [self.raw + b'\n', self.raw.replace(b'0,1,0', b'0,,0'),
                    self.raw.replace(b'0,1,0', b'0,True,0'), self.raw + b'"unfinished',
                    self.raw.replace(b'two,', b' two,'), b'\xff',
                    self.raw.replace(b'0,1,0', b'0,1,0,1')]
        for raw in variants:
            with self.subTest(raw=raw), self.assertRaises(fb.InputError):
                self.check(raw)

    def test_bom_crlf_and_quoted_ids(self):
        plan = dict(self.plan, cases=['one,quoted', 'two', 'three'])
        manifest = fb.freeze(fb.canonical(plan))
        raw = b'\xef\xbb\xbf' + self.raw.replace(b'one,1', b'"one,quoted",1').replace(b'\n', b'\r\n')
        report, normalized = self.check(raw, manifest, manifest['plan_sha256'])
        self.assertEqual(report['case_count'], 3)
        self.assertIn(b'"one,quoted",1,1,1\n', normalized)

    def test_duplicate_json_members_unknown_fields_and_nonfinite(self):
        for raw in [b'{"x":1,"x":2}', b'{"a":{"x":1,"x":2}}', b'{"a":NaN}',
                    b'{"a":Infinity}', b'\xff', b'[' * 1100]:
            with self.subTest(raw=raw[:30]), self.assertRaises(fb.InputError):
                fb.parse_json(raw)
        for value in [dict(self.plan, extra=True), {'schema': fb.SCHEMA}, []]:
            with self.assertRaises(fb.InputError):
                fb.freeze(fb.canonical(value))

    def test_invalid_labels_and_types(self):
        for field, value in [('cases', ['x', 'x']), ('cases', []), ('cases', [1]),
                             ('cases', ['a\n']), ('cases', ['x' * 257]),
                             ('candidates', ['a-v1']), ('candidates', ['a-v1'] * 2),
                             ('candidates', ['baseline', 'a-v1']),
                             ('candidates', ['base-v1', 'a-v1']), ('pass_rule', ''),
                             ('baseline', ' base-v1'), ('pass_rule', '\ud800'),
                             ('alpha', 0.05), ('alpha', 'NaN'), ('alpha', '1e-2'),
                             ('alpha', '0'), ('alpha', '0.21')]:
            with self.subTest(field=field, value=value), self.assertRaises(fb.InputError):
                fb.freeze(fb.canonical(dict(self.plan, **{field: value})))
        for alpha in ['0.000001', '0.2']:
            fb.freeze(fb.canonical(dict(self.plan, alpha=alpha)))

    def test_resource_bounds(self):
        with self.assertRaises(fb.InputError):
            fb.parse_json(b' ' * (fb.MAX_BYTES + 1))
        with self.assertRaises(fb.InputError):
            self.check(b' ' * (fb.MAX_BYTES + 1))
        with self.assertRaises(fb.InputError):
            fb.freeze(fb.canonical(dict(self.plan, cases=[str(i) for i in range(10001)])))
        # Valid short UTF-8 spec that would expand beyond the readable output limit.
        plan = dict(self.plan, cases=[str(i) + '\u2603' * 100 for i in range(3500)])
        raw = json.dumps(plan, ensure_ascii=False).encode()
        self.assertLess(len(raw), fb.MAX_BYTES)
        with self.assertRaises(fb.InputError):
            fb.freeze(raw)

    def test_manifest_shape_and_pin_format(self):
        for value in [{}, dict(self.manifest, extra=1), dict(self.manifest, schema='v2')]:
            with self.assertRaises(fb.InputError):
                fb.verify_manifest(fb.canonical(value), self.pin)
        for pin in ['x', self.pin.upper(), '0' * 64]:
            with self.assertRaises(fb.InputError):
                self.check(pin=pin)

    def test_workspace_guard_before_read(self):
        with self.assertRaises(fb.InputError):
            fb.read_workspace('/')
        with self.assertRaises(fb.InputError):
            fb.read_workspace('.')

    def test_demo_exercises_rejections(self):
        demo = fb.demo()
        self.assertEqual(demo['data_kind'], 'synthetic_demonstration')
        self.assertEqual(set(demo['rejected']), {'missing_case', 'unplanned_case', 'family_drift'})

    def test_actual_candidate_ladder_accepts_emitted_csv(self):
        source = Path(__file__).resolve().parents[1] / 'candidate-ladder' / 'candidate_ladder.py'
        if not source.is_file():
            self.skipTest('optional predecessor integration not copied')
        spec = importlib.util.spec_from_file_location('ladder_integration', source)
        ladder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ladder)
        report, raw = self.check()
        names, rows = ladder.read_csv_bytes(raw)
        verdict = ladder.analyze(raw, names, rows, ladder.parse_alpha(report['alpha']))
        self.assertEqual(verdict['paired_cases'], 3)
        self.assertEqual(verdict['candidate_count'], 2)
        self.assertEqual(verdict['input_sha256'], report['normalized_csv_sha256'])

    def test_cli_demo_and_invalid_input_status(self):
        script = str(Path(fb.__file__).resolve())
        good = subprocess.run([sys.executable, '-B', script, 'demo'], capture_output=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)['check']['status'], 'complete_observations')
        bad = subprocess.run([sys.executable, '-B', script, 'freeze', '--spec', '.'], capture_output=True)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(bad.stdout, b'')
        self.assertIn(b'error:', bad.stderr)


if __name__ == '__main__':
    unittest.main()
