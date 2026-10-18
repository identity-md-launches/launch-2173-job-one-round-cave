# Frozen Benchmark

Freeze the protocol for a **fixed paired binary benchmark**, then reject incomplete
or changed observations before running a statistical comparison. Python 3.10+
and its standard library only; this folder can run by itself, offline.

One command from the repository root shows a working synthetic protocol:

```sh
python3 -B line-1/tools/frozen-benchmark/frozen_benchmark.py demo
```

When tried locally, it admitted three complete cases, reordered them into the
planned order, and rejected a missing case, an extra case and a renamed candidate.
Its plan SHA-256 was
`13d5c3882c0082a7c603ad464645f312f6ebe6bee4622cc9f4c35710e8086f8e`.
These are synthetic observations, not measured improvements. The demo requires
no files, network, coins, account or installation and writes JSON to stdout.

## Freeze before collecting outcomes

Prepare a UTF-8 JSON protocol in your workspace. Every field below is required;
unknown fields and duplicate JSON members fail. Use immutable version labels for
your real baseline and candidates, a precise pass rule, the complete planned
family and every independent case ID. This example is deliberately synthetic:

```json
{
  "schema": "frozen-benchmark-v1",
  "baseline": "synthetic-parser-v1",
  "candidates": ["synthetic-fast-v1", "synthetic-careful-v1"],
  "pass_rule": "Synthetic fixture only: output equals the case expected value exactly.",
  "alpha": "0.05",
  "cases": ["empty", "unicode", "truncated"]
}
```

Save your protocol as `protocol.json` inside your workspace, then run:

```sh
python3 -B line-1/tools/frozen-benchmark/frozen_benchmark.py freeze --spec protocol.json > manifest.json
```

Keep the emitted `plan_sha256` **separately before collecting observations**.
It is SHA-256 of the normalized plan's JSON: sorted keys, ASCII escaping,
compact separators, no NaN, and one trailing LF. Alpha is normalized as a plain
decimal string, so `0.0500` and `0.05` have the same pin. Case and candidate
order are significant; JSON indentation and object key order are not.
The manifest contains the full normalized plan, its digest, and a schema name.
No timestamp is invented. A digest by itself proves neither publication time
nor preregistration; retain a trusted copy through your own review process.

## Admit the complete observations

Collect one binary outcome for the baseline and **every** planned candidate on
**every** planned case. The baseline column is literally `baseline`; its version
label comes from the pinned protocol. Headers must match candidate names and
order exactly. For the synthetic protocol:

```csv
case,baseline,synthetic-fast-v1,synthetic-careful-v1
truncated,0,0,1
empty,1,1,1
unicode,0,1,1
```

For that example only, save the CSV as `results.csv`, then check against the
separately retained example pin:

```sh
python3 -B line-1/tools/frozen-benchmark/frozen_benchmark.py check --manifest manifest.json --results results.csv --expected-plan-sha256 13d5c3882c0082a7c603ad464645f312f6ebe6bee4622cc9f4c35710e8086f8e
```

For a real experiment, supply **its original retained pin**, rather than a fresh
hash of the manifest you are checking. Replacing a plan and its internal digest
is rejected against that original pin. Missing cases, new cases, duplicates,
missing candidates, changed candidate labels/order, malformed CSV and nonbinary
outcomes all fail. Row order may differ; admitted rows are normalized into
planned order. BOM, CRLF and quoted case IDs containing commas are supported.

The JSON report records the plan pin, raw manifest and observation byte digests,
normalized CSV digest, baseline version, pass rule, candidates, case count and
alpha. `complete_observations` means the input passed these consistency checks;
it says nothing about statistical significance or which system is better.

Add `--emit-csv` to emit the admitted CSV **instead of** JSON. The entire input
is checked before any CSV is printed. For example, append
`--emit-csv > admitted.csv` to the check command, then analyze it using the
unchanged Candidate Ladder with the pinned protocol's alpha:

```sh
python3 -B line-1/tools/candidate-ladder/candidate_ladder.py --input admitted.csv --alpha 0.05
```

Its `input_sha256` must equal the checker report's `normalized_csv_sha256`.
Keep the raw observations too: normalization deliberately changes ordering and
possibly quoting or line endings. Do not analyze a stale `admitted.csv` after a
failed check. Both commands exit 0 for valid input, regardless of the statistical
conclusion. Invalid input exits 2 with stderr and no partial stdout.

## Limits and remaining responsibilities

Inputs must resolve to regular files inside the current working directory and
are each bounded at 2 MiB. Limits are 1–10,000 unique case IDs, 2–16 unique
candidates, labels of at most 256 characters, and a pass rule of at most 8,192
characters. Edge whitespace, C0/C1 controls and surrogate characters fail.
Candidate labels cannot equal `case`, `baseline`, or the baseline version.
Alpha is a plain decimal string from 0.000001 to 0.2, with at most 18 fractional
places. A freeze whose emitted manifest would exceed 2 MiB fails explicitly.
Paths are resolved before opening; this guard is not protection against a
concurrent adversary swapping files. No environment variables are read and no
input files are changed. Redirect stdout only to a new file you intend to write.

This tool binds **declared IDs and rules**, not case payloads or executed code.
Preserve the actual inputs and versioned systems separately. It cannot verify
truthful measurements, correct pass-rule application, independence, representative
case selection, when a plan was chosen, or that it was followed. It does not
execute candidate systems or provide a new statistical method. Use the existing
fixed-size McNemar/Holm analysis once at the planned endpoint. No equivalence,
optional stopping or generalization guarantee is supplied.

## Checks performed

```sh
python3 -B -m unittest discover -s line-1/tools/frozen-benchmark -v
```

All 15 tests passed. They cover complete admission, canonical hash agreement,
self-consistent tampering against an independent pin, full-case and family
membership, CSV failure modes, quoted Unicode-capable IDs, BOM/CRLF, duplicate
JSON keys, schema/type/label/alpha checks, bounded expansion, CLI exits, and
actual downstream Candidate Ladder parsing/analysis with matching hashes. That
last integration skips when the folder is copied without Candidate Ladder.
All 32 predecessor tests also passed unchanged. A separate local CLI exercise
froze the example, admitted it, emitted CSV, ran Candidate Ladder, and rejected
a changed pin with exit 2 and empty stdout.
