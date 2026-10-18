# JSON Citations

Locate JSON Lantern's Unicode findings in the **original UTF-8 source bytes**.
An escaped directional control, a visually similar key and a duplicate key now
have exact source ranges, bounded ASCII excerpts and SHA-256 hashes. Input is
reviewed without rewriting it or discarding repeated members.

Run from the repository root with Python 3.9+; no packages, installation or
network are needed:

```sh
python3 -B line-2/tools/json-citations/json_citations.py --demo
```

The synthetic demo returns five findings and exit 0. The directional override
has decoded character offset 9 and decoded UTF-8 byte offset 12, but its actual
JSON escape occupies original bytes **[54, 60)**. A duplicate `owner` key is
cited twice: the first original token is `[1, 8)`, and the differently encoded
second token is `[11, 23)`. These distinctions let a reviewer check the exact
spelling instead of guessing where a decoded offset belongs in a document.

For an explicitly selected, non-sensitive real JSON file inside the workspace:

```sh
python3 -B line-2/tools/json-citations/json_citations.py --file dist/line-2/22.json
```

File mode exits 0 for no covered patterns, 1 for findings, and 2 for invalid
input or exceeded budgets. Demo mode deliberately exits 0. Reports go to
stdout; argument usage errors go to stderr. `--max-findings 20` lowers the
global retained-finding limit without changing the complete finding count.

## Reading and checking a citation

All source citations use zero-based, half-open **original byte ranges**:
`raw[byte_start:byte_end]`. They include the span's byte count and lowercase
SHA-256. The complete original input also has a SHA-256 in the report.

- `source_token` includes both quotes around the original JSON string.
- `source_focus` covers precisely the original bytes encoding a decoded
  finding. An escape is included whole; a surrogate pair spans twelve bytes
  for one decoded code point. Literal UTF-8 keeps its original byte width.
- `first_source_token` cites the first key of an object-key collision.
- `first_source_focus` cites the first identifier of an identifier collision.
  Its scope remains the same decoded string, or the raw input for raw findings.

`excerpt_escaped_bytes` is ASCII **byte notation**, including after parsing
the outer JSON: backslashes are doubled, nonprinting/non-ASCII bytes use
`\xHH`, and ordinary printable ASCII is unchanged. It is not a JSON string
literal to decode again. At most 96 original bytes are shown; the separate
`excerpt_truncated` flag says when more existed. The span range and hash cover
all original bytes, including omitted ones. Excerpts can end within UTF-8 or an
escape because they describe bytes, not a rendered string. Preserve the original
input separately and hash its cited slice to check the claim.

The ancestral `evidence` object and structural `location` are retained
unchanged. Their offsets still refer to a decoded string for `decoded-string`
findings, and to original bytes for `raw-json`. The new citations have their
own fields, so these offset domains cannot be confused. Pair indexes preserve
duplicate keys and do not interpret slashes or tildes in key text as paths.
Raw/decoded findings can describe the same character and count it twice.

## Bounds and limitations

The original JSON Lantern validates input first: strict UTF-8 JSON, at most
2 MiB, 64 nested containers, 20,000 values, and at most 1,000 retained findings.
Malformed JSON, a BOM, nonfinite numbers, unpaired surrogates, over-budget input
and JSONL are errors. Numbers remain opaque, avoiding precision loss and integer
conversion limits. Input/report bounds and the total finding count are inherited.
Exceeding a budget produces an error, never a partial clean assessment.

Source indexing operates on validated bytes, preserving original escape casing,
whitespace and repeated members. It scans each cited string once to map only
needed decoded character boundaries; repeated token hashes are cached.

This adds citations, **not additional detection coverage**. The ancestral
Latin/Greek/Cyrillic heuristic is deliberately incomplete and is not UTS #39.
Findings require context; no findings does not establish safety. Hashes bind
bytes, not authorship or honest collection. Citation hashes do not authenticate
a report. There is no repair, rendering engine, language parser, HTTP request,
directory crawl, wallet access, signing, transaction, posting or environment read.
File inputs must resolve within the current working directory. Use stable files;
path checks cannot prevent another process from swapping a file during review.

The unchanged sibling folders `../json-lantern/` and `../unicode-lantern/` are
required dependencies. Copy all three folders, retaining their relative names,
when moving the tool. Everything is Python standard library; nothing is fetched
at runtime. The CLI reads only its explicit input, and imports these source files.

## What happened when tried

Sixteen new tests passed, alongside all 17 JSON Lantern and 12 Unicode Lantern
ancestral tests. Citation slices were independently decoded with `json.loads`
and compared against inherited evidence, including 60 deterministic generated
documents using both literal UTF-8 and ASCII escapes. Cases cover multibyte
prefixes, CRLF, escaped quotes/backslashes, supplementary variation selectors,
surrogate pairs, duplicate keys, both collision endpoints, truncation, long
excerpts, strict input bounds, CLI statuses and unchanged upstream findings.
The real existing `dist/line-2/22.json` produced zero covered patterns; this
is an observation about these rules, not an endorsement of that record.

```sh
python3 -B -m unittest discover -s line-2/tools/json-citations -v
```

The mark is a charcoal pebble linked to a chalk pebble by an ochre thread:
tracing a discovery back to its source.
