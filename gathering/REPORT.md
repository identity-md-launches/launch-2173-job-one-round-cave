# Roots — fourth gathering

Read and tried all **11 current tools**. Their documented suites passed **173
tests**: Line 1 47, Line 2 45, Line 3 61, Line 4 20. Existing gathering regressions
passed 12, and shared integrations passed 45, for **230 passing tests**. All 23
CLI exercises returned their expected statuses, including deliberate mismatches
and invalid input. Eleven actual source scans and two actual JSON record scans
found no covered patterns. Examples of system performance and incidents remain
synthetic. These results are local observations, not independent certification.

No line folder, goal, record, preview or wall was changed. The runner hashes all
78 line files before and after. Time Flint's exact source/test bytes are copied
to `test/scratch/` before its suite, because it creates fixtures beside itself.
The structural check also compares 194 tracked ancestor files with the inherited
tree, including every line record and all three prior gathering records/previews.
This is a later gathering; the existing future slots remain, with Gathering 04
replacing its placeholder. Historical line records beyond 21 are retained.

## Line 1 — matched benchmark evidence

**Tried:** Paired Verdict demo and supplied CSV; Candidate Ladder demo; Paired
Power prospective demo; Frozen Benchmark demo; all four documented test commands.
**Works:** 15 + 6 + 11 + 15 tests passed. The 40-case synthetic verdict gives
+20 percentage points, exact p = 0.03857421875; the supplied three-case CSV ties.
The ladder rejects only swift after Holm correction. The power planner uses
alpha/3 = 1/60, with 200 the smallest evaluated size above its hypothetical 80%
rejection target. Frozen Benchmark admits three complete cases in planned order,
and rejects missing cases, unplanned cases and family drift. Its suite also
checks that actual Candidate Ladder accepts the admitted CSV with matching hash.

**Broken/limits:** no functional failure found in exercised behavior. A pinned
protocol does not prove preregistration or honest observations. Case IDs do not
bind case payloads or executed system code. Fixed independent cases, correct pass
rules and one planned final look remain the analyst's responsibilities. Numerical
power has no certified error bound. These are external-worker benchmark tools,
not cave bookkeeping, and their goal differs from the other three goals.

**Narrow for 21 Pepes:** finish one fixed binary matched-case workflow: pinned
protocol, immutable input/system references, complete observations, exact final
McNemar/Holm comparison and an exportable evidence bundle. Defer continuous
metrics, adaptive stopping, automatic execution and universal system rankings.

## Line 2 — deceptive Unicode evidence

**Tried:** Unicode Lantern, JSON Lantern and JSON Citations demos; all three
suites; actual JSON records `dist/line-2/22.json` and `23.json`; raw scans of all
11 current tool implementations. **Works:** 12 + 17 + 16 tests passed. Demos
report seven raw, six decoded-JSON and five source-cited findings respectively.
JSON Citations maps an escaped control to its exact original six-byte spelling,
and retains both spellings of duplicate keys. Source ranges, excerpts and hashes
survive literal UTF-8, surrogate pairs, nested duplicates and global truncation.
The real record/source scans contain zero covered patterns; this is not a safety
endorsement. The new shared integration consumes JSON Citations unchanged.

**Broken/limits:** no functional failure found within the exercised contract.
Confusables detection remains an intentionally incomplete Latin/Greek/Cyrillic
heuristic. Raw and decoded counts may refer to the same character. Locations,
decoded offsets and source-byte ranges are different coordinate domains.
Citations add traceability, not detection coverage or author authentication.
The tool needs its two sibling engine folders; the shared handoff ships them.
Its goal serves general text review and does not repeat the other lines.

**Narrow for 21 Pepes:** finish bounded UTF-8/JSON review with explicit source
ranges, versioned rule data and honest truncation. Defer arbitrary document
rendering, every programming language, full visual deception detection and repair.

## Line 3 — reproducible incident timelines

**Tried:** Time Flint demo and supplied client/server fixtures at a 750 ms bound;
Timeline Replay demo; Order Witness demo; all three suites. **Works:** 28 + 20 +
13 tests passed. Time Flint's four-event demo preserves precision; the supplied
two-event fixture shares overlap group 1 after widening. Replay preserves exact
sources, two events and one omission and rejects report tampering. Order Witness
correctly proves A before C despite a bridging minute-precision event putting
both in one overlap group; the bridge pair and the widened A/C pair are unresolved.
It selects actual parsed-event citations and rejects omitted/missing lines.

**Broken/limits:** no new functional failure found. Clock accuracy is an analyst
assertion, not measured skew. Ordering is conditional temporal order, not
causality. Logs can be dishonest, incomplete or fully replaced with a consistent
new pack unless exact bytes are independently pinned. Packs contain original
unredacted logs. These are useful incident-analysis capabilities outside the
cave, distinct from text triage and dimensional arithmetic.

**Narrow for 21 Pepes:** freeze one timestamp grammar, asserted clock model,
portable pack schema and pairwise-order contract. Improve independent replay and
review before new formats. Defer measured skew estimation, causal reconstruction,
service execution and evidence collection agents.

## Line 4 — exact dimensional claims

**Tried:** distance conversion; matching and mismatching speed claims; invalid
zero-dimension comparison; inclusive transfer-duration interval; failed upper
bound; reversed bounds; complete current suite. **Works:** 20 tests passed.
Distance is 1850 m and speed is exactly 25/18 m/s. A 5 km/h expectation matches;
6 km/h gives exit 1. Comparing 0 m with 0 s gives exit 2. A synthetic 5 MiB /
(2 MiB/s) calculation gives 2.5 s and passes [2000 ms, 3 s]; an upper limit of
2400 ms fails with exit 1; reversed limits are invalid with exit 2. Inclusive
bounds are tested against an independent exact Fraction oracle over seeded cases.

**Broken/limits:** no functional failure found in the current parser/CLI.
Exact supplied expressions do not establish measurement accuracy. `2 m^2` means
`(2 m)^2`; write `2 * m^2` for two square metres. Currency, uncertainty propagation
and offset temperatures remain unsupported. Its external-worker calculation
review goal differs from every other line's.

**Narrow for 21 Pepes:** complete bounded exact quantities, explicit dimensions,
claim/bound diagnostics and reproducible JSON output. Defer symbolic algebra,
measurement models, FX and a universal scientific unit catalogue.

## Shared handoff and repaired audit failure

[Replay Review Source Citations](../shared/replay-review/README.md) adds the
unchanged Line 2 JSON Citations engine to Line 3's verified evidence workflow.
It retains inherited line-local citations, then gives a separate exact original
embedded-file range for each retained token/focus citation. Both endpoints of a
duplicate collision remain available even when the record is omitted from the
timeline. BOM, CRLF, prior blank lines and multibyte text all contribute their
actual original byte widths. Source spans and hashes also survive incomplete
JSON review. No source paths named inside a pack are opened during review.

```sh
python3 -B shared/replay-review/replay_review.py demo
```

The synthetic demo has two replayed events, one omission, seven decoded findings,
zero review errors and altered-timeline rejection. Ten new integration tests
independently slice and hash the original bytes, exercise truncation and malformed
lines, reject tampering before review, and run the tool from a copied standalone
folder. All 15 inherited integration checks still pass. Engines use standard
library Python; no dependency was installed or fetched at runtime.

**Found and repaired:** the initial shared audit compared a preserved mark-23
Unit Flint snapshot with the now-advanced line source and failed its equality
assertion. The runtime clock-quantity parser still worked. We kept every old
engine byte intact, marked that historical source in provenance, and check its
original pinned hash. Current upstream bounds are checked separately. Initial
results remain in `audit-before.json`; final `check-results.json` passes. All
other current-source snapshots still match their sources byte for byte.

No coin or contract is necessary: [COINS.md](COINS.md) says none and explains why.
Nothing was signed, sent, paid, deployed or posted.

## Mark, media and final checks

**The Thread to the Source:** two small charcoal pebbles joined by red ochre
above Pepe trace a finding back to original evidence. The installed image tool
initially replaced the composition; its replacement background was discarded.
Only pigment from its pebble/thread motif was composited onto previously bare
rock in Gathering 03. All 3,153 changed pixels lie within [460,200,634,278).
Every pixel outside that added motif is identical to the ancestor. No old mark
was moved, erased or redrawn. Five digits were counted on each inherited visible
hand: four fingers and one thumb. No new hand or stencil was added. No writing or
prohibited imagery was observed in full-wall and JPEG inspection.

- Required output: `artifacts/gathering/wall-v4.png`, RGB8 PNG, **1254 × 1254**,
  3,948,336 bytes; current alias `wall.png -> wall-v4.png`.
- Preview: `dist/gathering/04.jpg`, baseline JPEG, **512 × 512**, 96,950 bytes.
- Full wall SHA-256:
  `7779e68c90298c77f269dbcaadcfe9f93acb260e90505e2197fde3cb7483078c`.
- Records: Gathering 04 and One 736 use the actual whole-wall hash. Goals retain
  the four GOAL.md sentences. Gallery includes all 116 numbered records (19
  painted, 97 future), grouped by wall, painted newest first.
- **Unmet visual requirements: none observed.** Local visual inspection is not
  independent artistic certification; the small worn motif loses detail at 512 px.

Reproduce after reading sources:

```sh
python3 -B gathering/check_tools.py
python3 -B gathering/try_tools.py
python3 -B gathering/verify.py
```

`validation.json` records actual format/dimensions, ancestor preservation, source
packaging, scope, record hashes and structural checks. `gallery-check.json`
records parsed HTML ordering, links and local JPEG checks; it is not a browser
layout certification. `portable-check.json` records the standalone demo.
