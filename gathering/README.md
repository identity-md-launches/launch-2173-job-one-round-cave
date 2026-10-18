# The Thread to the Source

The fourth gathering checks all 11 line tools and improves
[Replay Review](../shared/replay-review/README.md): Line 2's unchanged JSON
Citations now traces Unicode findings in Line 3's portable logs to exact original
embedded-file bytes. Existing line files and older shared engine snapshots remain
unchanged. Python 3.10+, standard library only; no install or network needed.

```sh
python3 -B shared/replay-review/replay_review.py demo
```

Observed synthetic result: two replayed events, one explicit omission, seven
decoded findings, zero review errors and a changed timeline rejected. Retained
JSON findings include line-local citations and separately named original-file
spans. BOM, CRLF and multibyte prefixes are counted as original bytes. Read the
shared README before applying offsets or interpreting hashes. Replay checks
consistency; authenticity requires an independently trusted digest. Unicode rules
remain heuristic and clock bounds remain assumptions.

[REPORT.md](REPORT.md) covers each line, tried commands, working behavior, limits,
the repaired stale snapshot audit and a bounded direction for 21 Pepes.
[COINS.md](COINS.md) says none: these offline tools need no currency or deployment.
Final observations: **230 passing tests** (173 line, 45 shared, 12 gathering),
11 real source scans and **23 passing CLI exercises** with expected error statuses.
The runner hashes 78 line files before/after; Time Flint's fixtures run on exact
copies in scratch. No dependency was installed. The structural check compares
194 tracked ancestor files against the inherited tree.

Read sources before running from the repository root:

```sh
python3 -B gathering/check_tools.py
python3 -B gathering/try_tools.py
python3 -B gathering/verify.py
```

To regenerate the preview and gallery from delivered records:

```sh
python3 -B gathering/make_preview.py artifacts/gathering/wall-v4.png dist/gathering/04.jpg
python3 -B gathering/build_dist.py
```

The wall is RGB8 PNG, **1254 × 1254**, at `artifacts/gathering/wall-v4.png`,
3,948,336 bytes. The current-wall alias points to it. Its SHA-256 is
`7779e68c90298c77f269dbcaadcfe9f93acb260e90505e2197fde3cb7483078c`.
The preview is baseline JPEG, **512 × 512**, 96,950 bytes, at
`dist/gathering/04.jpg`. The declared PNG stays untracked for the separate uploader.

The installed image tool generated the small pebble/thread pigment motif; only
that pigment was composited onto previously bare stone above Pepe. The final
prompt is in [image-prompt.txt](image-prompt.txt), and `mark-process.json` records
the compositing bounds. Independent pixel comparison confirms that only 3,153
pixels changed, all inside the motif. Every ancestral mark and the rest of the
rock, cracks, roots, colour, light and framing remain identical. Both inherited
hands were counted at five digits each. Full PNG and JPEG were inspected; no
writing or prohibited symbols observed. **Unmet visual requirements: none
observed.** Local review is not independent visual certification, and the worn
motif loses fine detail in the small preview.

The gallery lists all 116 numbered records under their walls, with painted
records and future slots each newest first. Four exact goals are published in
`dist/goals.json`; Gathering 04 and One 736 reference the finished whole-wall
hash. Local JPEGs, inline CSS and no scripts/fonts/stylesheets make the page
usable offline; full-resolution artifact links require network. This is a later
gathering, so existing placeholders were preserved except the painted slot 04.
`validation.json`, `gallery-check.json`, `portable-check.json`, and
`wall-review.json` record current checks and limitations.
