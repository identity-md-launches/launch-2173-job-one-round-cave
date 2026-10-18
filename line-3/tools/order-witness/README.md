# Order Witness

Check whether two cited log events have a definite temporal order, using a verified
Timeline Replay pack. Python 3.10+, standard library only. Copy this whole folder
(including `replay.py` and `vendor/`) for independent offline use.

One command from the repository root demonstrates it without writing files:

```sh
python3 -B line-3/tools/order-witness/order_witness.py demo
```

Observed locally: the synthetic A and C events share transitive overlap group 1
but return `left-before-right`; A and the bridging minute-precision event return
`unresolved-overlap`. A 750 ms asserted clock bound also makes A/C unresolved.
These are synthetic conformance examples, not a real incident or measured clocks.

For an existing Timeline Replay pack:

```sh
python3 -B line-3/tools/order-witness/order_witness.py compare test/scratch/timeline-pack.json --left client.log 1 --right server.log 2
```

Use the exact source strings and physical line numbers recorded in your pack.
The two names above illustrate the syntax; they must identify actual parsed
events in that pack. Missing, blank, or omitted lines fail explicitly. Source
names are inert citations; their paths are never opened during comparison.
`--expect-sha256 DIGEST` optionally pins the exact pack bytes against an
independently retained lowercase SHA-256. The command verifies the entire pack
before selecting events, and includes the pack digest in successful CLI output.

Relations are `left-before-right`, `right-before-left`, `unresolved-overlap`, or
`same-event`. For distinct events with intervals [s,e), left is definitely before
right when left.e <= right.s; equality counts because endpoints are exclusive.
UTC endpoints from the verified fixed parser are parsed as exact microsecond
datetimes, including mixed displayed fractional precision. The result
includes both interval endpoints, physical citations, line hashes, overlap groups,
and clock assumptions. It does not use transitive overlap groups to infer pairs.
Exit 0 means a valid comparison, including unresolved overlap; exit 2 means invalid
input. Terminal JSON and diagnostics escape control characters.

This establishes order only under the pack's truncation and clock assumptions.
It proves neither causality nor truthful, complete logs, and unresolved intervals
do not establish simultaneity. Comparing an event with itself is identity, not
uncertainty about two occurrences. Replay hashes establish consistency, not author
authenticity; an independently trusted digest is needed to bind exact evidence.
Packs contain original unredacted logs. No services, wallet, keys, transactions,
network, environment access, or coins are needed. Inputs must be explicit regular
workspace files; inherited limits are 16 MiB per pack, 2 MiB embedded raw evidence,
64 sources, and the parser's line/depth/calendar bounds. No streaming mode.

```sh
python3 -B -m unittest discover -s line-3/tools/order-witness -v
```

Observed: 13 tests passed, including half-open adjacency, reversed order,
transitive bridging, identical intervals, identity, bound widening, omitted/missing
citations, offset normalization, tamper rejection, preserved hashes and immutable
input. A separate CLI round trip and bad digest rejection were also checked.

`replay.py` is an unchanged copy of the predecessor's `timeline_replay.py`;
`vendor/time_flint.py` and `vendor/__init__.py` are unchanged copies from its
vendor folder. `PROVENANCE.json` records source paths and hashes. No dependency
installation is needed.
