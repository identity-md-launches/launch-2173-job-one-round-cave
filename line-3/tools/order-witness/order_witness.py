#!/usr/bin/env python3
"""Check pairwise temporal order using verified Timeline Replay evidence."""
import argparse
from datetime import datetime
import json
import re
import sys
import replay


def instant(text):
    return datetime.fromisoformat(text.replace('Z', '+00:00'))


def citation(event):
    return {key: event[key] for key in ('source', 'line', 'line_sha256',
            'start_utc', 'end_utc_exclusive', 'overlap_group')}


def select(events, source, line):
    if type(line) is not int or line < 1:
        raise replay.ReplayError('line must be a positive integer')
    matches = [e for e in events if e['source'] == source and e['line'] == line]
    if len(matches) != 1:
        raise replay.ReplayError('citation must identify exactly one parsed event')
    return matches[0]


def compare(pack, left_source, left_line, right_source, right_line):
    verified = replay.verify_pack(pack)
    events = pack['timeline']['events']
    left = select(events, left_source, left_line)
    right = select(events, right_source, right_line)
    if (left_source, left_line) == (right_source, right_line):
        relation = 'same-event'
    elif instant(left['end_utc_exclusive']) <= instant(right['start_utc']):
        relation = 'left-before-right'
    elif instant(right['end_utc_exclusive']) <= instant(left['start_utc']):
        relation = 'right-before-left'
    else:
        relation = 'unresolved-overlap'
    return {'format': 'order-witness/1', 'replay': verified,
            'relation': relation, 'left': citation(left), 'right': citation(right),
            'clock_model': pack['timeline'].get('clock_model', {'uncertainty_ms': 0}),
            'interpretation': 'Temporal order under asserted clock bounds; no causal claim.'}


def demo():
    # All three events share one transitive overlap group. A and C do not overlap.
    pack = replay.make_pack([
        ('a.log', b'2026-10-18T10:00:00Z A\n'),
        ('bridge.log', b'2026-10-18T10:00Z B\n'),
        ('c.log', b'2026-10-18T10:00:02Z C\n')])
    certain = compare(pack, 'a.log', 1, 'c.log', 1)
    ambiguous = compare(pack, 'a.log', 1, 'bridge.log', 1)
    wide = replay.make_pack([
        ('a.log', b'2026-10-18T10:00:00Z A\n'),
        ('c.log', b'2026-10-18T10:00:02Z C\n')], clock_uncertainty_ms=750)
    return {'example': 'synthetic, not a real incident', 'same_group_certain_order': certain,
            'overlap': ambiguous,
            'widened': compare(wide, 'a.log', 1, 'c.log', 1)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('demo')
    check = commands.add_parser('compare')
    check.add_argument('pack')
    check.add_argument('--left', nargs=2, metavar=('SOURCE', 'LINE'), required=True)
    check.add_argument('--right', nargs=2, metavar=('SOURCE', 'LINE'), required=True)
    check.add_argument('--expect-sha256')
    args = parser.parse_args(argv)
    try:
        if args.command == 'demo':
            result = demo()
        else:
            raw = replay.read_workspace(args.pack, replay.MAX_PACK_BYTES)
            if args.expect_sha256 is not None:
                if not re.fullmatch('[0-9a-f]{64}', args.expect_sha256):
                    raise replay.ReplayError('expected hash must be 64 lowercase hex digits')
                if replay.digest(raw) != args.expect_sha256:
                    raise replay.ReplayError('pack does not match expected SHA-256')
            result = compare(replay.load_pack(raw), args.left[0], int(args.left[1]),
                             args.right[0], int(args.right[1]))
            result['pack_sha256'] = replay.digest(raw)
        sys.stdout.buffer.write(replay.canonical(result) + b'\n')
        return 0
    except (OSError, ValueError, RecursionError) as exc:
        print('order-witness: ' + replay.engine.visible(str(exc)), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
