# Unmodified source snapshots

Each file is copied byte-for-byte from the indicated line. No external dependency.

- `shared/replay-review/engines/timeline-replay/timeline_replay.py` from `line-3/tools/timeline-replay/timeline_replay.py`; SHA-256 `d77a8a28268ce860aac890926720d4cd278535ff89b7930e2f6fad45acf2f0c8`.
- `shared/replay-review/engines/timeline-replay/vendor/time_flint.py` from `line-3/tools/timeline-replay/vendor/time_flint.py`; SHA-256 `caa513722a9767e908dc4a5e49711e623e0a34c8b18753c3d01cda8167988e38`.
- `shared/replay-review/engines/timeline-replay/vendor/__init__.py` from `line-3/tools/timeline-replay/vendor/__init__.py`; SHA-256 `7b170ee8a9c7182e7232fb81e1ac60be5a08619dce449c9500e2b3b740248ea2`.
- `shared/replay-review/engines/json-lantern/json_lantern.py` from `line-2/tools/json-lantern/json_lantern.py`; SHA-256 `2a30a232b22c9a85744609cce3324a83361172276e961e8195a4acd6e8c0f87e`.
- `shared/replay-review/engines/unicode-lantern/unicode_lantern.py` from `line-2/tools/unicode-lantern/unicode_lantern.py`; SHA-256 `e50d1fb77bd6cfd723c2dbd3749bedf2034c96ea3a2eaf88e4beac4610f6e2f5`.
- `shared/replay-review/engines/unit-flint/unit_flint.py` from `line-4/tools/unit-flint/unit_flint.py`; SHA-256 `ae71dba710f25c1940af9400253769f1efa4a83bb4ec80454be723221c46f09d`.

## Fourth gathering additions and version policy

- `engines/json-citations/json_citations.py` is copied unchanged from
  `line-2/tools/json-citations/json_citations.py`; SHA-256
  `11d92b07459f3fd7e1007ba408221501fce37d6c58b9ef04bf544c801aba766f`.
  Its two sibling dependencies already exist here with matching hashes above.
- The quantity snapshot above remains mark 23. The current line has advanced
  to inclusive bounds, so equal bytes with the latest upstream are no longer a
  valid expectation. The initial audit exposed that stale test assumption.
  `provenance.json` explicitly marks this one historical source; tests continue
  checking its original pinned digest. No shipped engine bytes were replaced.

`replay_review.py` is the gathering's glue: JSON review now calls the cited
engine; physical byte slicing adds an explicit original-file coordinate domain.
The source/line hashes and all original citation fields remain intact. No
external runtime dependency was introduced.
