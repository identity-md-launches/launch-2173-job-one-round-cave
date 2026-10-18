import copy
import unittest
import order_witness as w


class OrderTests(unittest.TestCase):
    def pack(self, a='2026-10-18T10:00:00Z', b='2026-10-18T10:00:01Z', **options):
        return w.replay.make_pack([('a', (a+' first\n').encode()),
                                   ('b', (b+' second\n').encode())], **options)

    def relation(self, pack):
        return w.compare(pack, 'a', 1, 'b', 1)['relation']

    def test_adjacent_half_open(self):
        self.assertEqual(self.relation(self.pack()), 'left-before-right')

    def test_mixed_fractional_precision(self):
        self.assertEqual(self.relation(self.pack(a='2026-10-18T10:00:00.500Z',
                                                b='2026-10-18T10:00:00Z')), 'unresolved-overlap')

    def test_reverse(self):
        p = self.pack()
        self.assertEqual(w.compare(p, 'b', 1, 'a', 1)['relation'], 'right-before-left')

    def test_overlap(self):
        self.assertEqual(self.relation(self.pack(b='2026-10-18T10:00Z')), 'unresolved-overlap')

    def test_identical_intervals_distinct_events(self):
        self.assertEqual(self.relation(self.pack(b='2026-10-18T10:00:00Z')), 'unresolved-overlap')

    def test_same_event(self):
        self.assertEqual(w.compare(self.pack(), 'a', 1, 'a', 1)['relation'], 'same-event')

    def test_widening(self):
        self.assertEqual(self.relation(self.pack(clock_uncertainty_ms=1)), 'unresolved-overlap')

    def test_bridge_not_pairwise_ambiguity(self):
        d = w.demo()
        certain = d['same_group_certain_order']
        self.assertEqual(certain['left']['overlap_group'], certain['right']['overlap_group'])
        self.assertEqual(certain['relation'], 'left-before-right')
        self.assertEqual(d['widened']['relation'], 'unresolved-overlap')

    def test_tamper_rejected_before_citation(self):
        p = self.pack()
        p['timeline']['events'][0]['end_utc_exclusive'] = '0000'
        with self.assertRaises(w.replay.ReplayError):
            self.relation(p)

    def test_missing_and_omitted_citations(self):
        p = w.replay.make_pack([('a', b'invalid\n2026-10-18T10:00:00Z event\n')], True)
        for line in (1, 3, 0, True):
            with self.assertRaises(w.replay.ReplayError):
                w.compare(p, 'a', line, 'a', 2)

    def test_input_not_mutated(self):
        p = self.pack()
        original = copy.deepcopy(p)
        self.relation(p)
        self.assertEqual(p, original)

    def test_offset_normalization(self):
        self.assertEqual(self.relation(self.pack(a='2026-10-18T12:00:00+02:00')), 'left-before-right')

    def test_citations_preserve_hashes(self):
        p = self.pack()
        r = w.compare(p, 'a', 1, 'b', 1)
        self.assertEqual(r['left']['line_sha256'], p['timeline']['events'][0]['line_sha256'])


if __name__ == '__main__':
    unittest.main()
