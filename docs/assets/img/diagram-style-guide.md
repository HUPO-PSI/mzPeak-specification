# Chunk process diagram style guide

Conventions used by `chunk_decoding_processes.svg` and `chunk_encoding_processes.svg`
(and to be reused by any future "process" diagram in this family — e.g. a null-marking
or page-index diagram). These are flat, hand-authored SVGs (no rough.js sketch style,
unlike `chunk_decode.svg`), meant to read cleanly at documentation scale.

## Canvas

- `viewBox="0 0 1300 820"`, width/height matching.
- Background: solid white `#ffffff` rect.
- Diagram title: centered, `x=650 y=38`, 26px bold.

## Row layout

- One row per concept (encoding/decoding scheme, etc.), 140px tall.
- Row bands start at `y=60` and alternate background colors for scannability:
  `#ffffff` (even rows) / `#e3dbde` (odd rows), with `1px #dee2e6` divider lines
  between rows and a final divider before the legend.
- Left label column (`x=20`, ~300px wide) holds, top to bottom:
  - `row-title` — 17px bold, e.g. `"4. Grid encoding"`.
  - `row-cv` — 12.5px, `#555555`, the CV term, e.g. `"MS:1003826 — coordinate grid encoding"`.
  - `row-note` — 11.5px italic, `#555555`, one or two caveats (nullability, emptied
    columns, etc.). Extra note lines just add another `y` a few px lower; they don't
    collide with the flow diagram since that starts further right (`x≈332`).
- The flow diagram (boxes/arrows) starts around `x=332` and runs left→right.

## Color roles

| Role | Fill | Used for |
|---|---|---|
| Raw / logical array value | `#b2f2bb` (green) | The real-valued array — decode's final output, encode's starting input |
| Stored column (as encoded) | `#80e5ff` (cyan) | The actual Parquet column(s) — decode's starting input, encode's final output |
| Intermediate / computed value | `#b7bec8` (gray) | A value computed mid-pipeline that isn't itself a stored column (e.g. absolute grid index before delta-encoding) |
| Side parameters | `#fff3bf` (yellow) | Read-only inputs to an operation that aren't part of the main left-to-right flow (e.g. `grid_type + parameters`) |

Decode and encode diagrams are intentionally color-symmetric: green is always "the
real values" (output when decoding, input when encoding) and cyan is always "the
stored bytes/columns" (input when decoding, output when encoding). This makes the
two diagrams visually rhyme as inverses of each other.

All boxes: `rx="8"`, `stroke="#1e1e1e"`, `stroke-width="1.5"`.

## Typography

- Font: `Arial, "Segoe UI", sans-serif`.
- Default weight is **bold** (`font-weight: 700` on the base `text` selector) —
  every label in these diagrams is bold, not just titles.
- Text classes:
  - `.box-label` — 12.5px, centered, the main name inside a box (e.g. `mz_grid.indices`).
  - `.box-sub` — 10px, centered, a parenthetical detail line inside a box
    (e.g. `(Δ-encoded u32)`).
  - `.op-label` — 11.5px, centered, `#333333`, the verb on an arrow
    (e.g. `cumsum`, `g(v) = (v·s−a)/b`).
  - `.out-label` / `.legend-text` — 11.5px / 12.5px as needed.

## Arrows

- Single-input/single-output steps: one straight `<line>` with
  `marker-end="url(#arrowhead)"` (black triangle marker defined once in `<defs>`).
- Merge (two inputs → one output) or split (one input → two outputs): a short plain
  line from/to the trunk, then two diagonal lines to/from each box, each with its
  own arrowhead. No curves — straight segments only, in the style of the rest of
  the diagram.
- A side-parameter box (yellow) connects into its consuming arrow with a short
  vertical arrow dropping straight down into the horizontal flow line.
- Label placement: short single-word/phrase op-labels go **above** their arrow
  (`y` ≈ row center − 14); longer formula labels go **below** (`y` ≈ row center + 20)
  to avoid crowding a parameter box that sits above the arrow.

## Critical gotcha: z-order

Labels must be drawn **after** every shape in the row, not interleaved
box → label → box → label. If a label's text is wide enough to overlap a
neighboring box and that box is drawn later in document order, the box's opaque
fill silently paints over part of the text (observed: a formula label losing its
closing character). The safe pattern used in both files is: emit all `<rect>`/
`<line>`/`<path>` shapes for a row first, then emit all of that row's `<text>`
elements in a second pass.

Keep op-labels short enough to fit the gap between the two boxes they sit between
(measure: roughly `0.6 × font-size` px per character for this bold Arial); when a
label doesn't fit, shorten the words rather than widening the gap, so columns stay
aligned across rows.

## Legend

- Fixed row at `y=776`, 16×16 swatches with 1.5px `#1e1e1e` stroke, one per color
  role, `12.5px` label text starting 22px after each swatch.

## QA workflow

Before considering a diagram done:

1. Validate well-formed XML (e.g. in PowerShell: `[xml](Get-Content file.svg -Raw)`).
2. Render a PNG via headless Edge/Chrome and visually check for clipped or
   overlapping text:
   `msedge.exe --headless --disable-gpu --screenshot=out.png --window-size=W,H file:///path/to.svg`
3. Delete the scratch PNG afterward — it's not a repo asset.
