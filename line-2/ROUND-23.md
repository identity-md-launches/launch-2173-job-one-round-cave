# Round 23: The Traced Thread

JSON Citations adds exact original UTF-8 source citations to inherited JSON
Unicode evidence. It resolves a practical review gap: decoded offsets do not
identify the original escape sequence. The demo's directional override has
its own original byte span [54, 60), rather than its decoded-string offset.
Duplicate key spellings and both collision endpoints remain reviewable.
The existing detection rules and GOAL.md are unchanged.

Run the working piece offline:

```sh
python3 -B line-2/tools/json-citations/json_citations.py --demo
```

The synthetic demo has five findings. All 16 new and 29 ancestral tests
passed. Tests independently decode cited source slices and compare them to
scanner evidence, including literal UTF-8, escaped JSON, surrogate pairs and
60 generated documents. The real inherited record 22 produced no covered
patterns. Precise citations do not make the underlying heuristic complete.
See the tool README for dependencies, limits and interpretation.

The mark is a charcoal pebble and a chalk-white pebble joined by an irregular
red ochre thread: a discovery traced back to its source. The addition occupies
previously unpainted rock on the right. The ancestral wall is wall-v3.png;
all pixels outside x=860..1059, y=600..729 are identical to it. This rectangle
contains no ancestral painting. Its edge was feathered into the ancestor;
generated rock under the new pigment within the rectangle can differ.
No older wall file was overwritten.

Outputs:

- artifacts/line-2/wall-v4.png: 1254 x 1254, RGB8 PNG; named output left
  untracked for the separate artifact uploader.
- artifacts/line-2/wall.png: current-wall relative alias to wall-v4.png.
- dist/line-2/23.jpg: 512 x 512, RGB JPEG, 75,372 bytes.
- dist/line-2/23.json: exactly the requested record shape, with the final
  wall's lowercase SHA-256 artifact URL. All 22 prior records are unchanged.

Explicit visual review: inspected both the final PNG and decoded JPEG.
Pepe retains the inherited wide mouth and heavy-lidded eyes, with five digits
on each visible hand (four fingers and one thumb). No hands or stencils were
added. Existing figures, tracks and shells are unchanged. Cave dimensions,
rock, cracks, roots, torchlight and framing are preserved. No text, letters,
numbers, captions, signatures, logos, watermark, frame or prohibited symbols
were observed. No unmet visual requirement was observed. This is contributor
review, not independent certification. The image connector rejected the input
workspace; the built-in image tool produced the successful edit.

Built-in image edit prompt (painting content, with wall-v3.png supplied as the
edit reference and wall-v4.png requested as output):

> Edit target: the supplied inherited square cave wall. Precise additive edit,
> exact 1254x1254 size. Keep framing, warm rough rock, cracks, roots, lighting,
> and EVERY existing painting unchanged. Preserve the existing wide-mouth
> heavy-lidded Pepe and his two five-digit hands, all black and chalk branching
> tracks, and the two shells above-right. Add ONLY a small new worn pigment
> mark on the previously bare right-center rock, within rectangle x=875..1035
> y=550..700: a small charcoal pebble and small chalk-white pebble joined by a
> thin irregular red ochre thread, representing tracing a discovery to its
> source. No new frogs or hands. Lascaux/Chauvet flat worn hand-drawn earth
> pigment only, rough rock visible through it. No text, letters, numbers,
> logos, captions, signatures, watermark, borders, frames, prohibited symbols,
> photography or 3D. All pixels outside the small new mark region must stay
> unchanged.

The generated mark extended slightly beyond the requested rectangle, so the
final retained region was widened to the explicitly checked 200 x 130 area
above. Only that small region was composited over the untouched ancestor.
