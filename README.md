# mzPeak specification

This repository hosts the specification for the **mzPeak** file format — an open,
Parquet-based standard for storing mass spectrometry spectra, chromatograms, and
instrument metadata. It is a HUPO-PSI recommendation (working draft).

The published site: **https://hupo-psi.github.io/mzPeak-specification/**

## Where the specification lives

The specification is written in Markdown and built into a static website with
[MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. The
canonical source is the multi-page document under [`docs/`](docs/), organised as:

| Section | Path |
| :-- | :-- |
| Home / abstract | `docs/index.md` |
| Introduction | `docs/introduction/` |
| Format foundations | `docs/foundations/` |
| Data layouts | `docs/layouts/` |
| Archive index | `docs/archive/` |
| File schemas | `docs/schemas/` |
| Reference (glossary, bibliography, authors, IP) | `docs/reference/` |

JSON Schemas that govern the file formats live in [`schema/`](schema/), and
figures in [`docs/assets/img/`](docs/assets/img/).

> **Note** — the original single-file draft, [`index.md`](index.md), is retained
> for historical reference only. The `docs/` tree is now the source of truth.

## Building locally

The site needs Python 3.9+ and the dependencies in
[`requirements.txt`](requirements.txt). The simplest path uses
[`uv`](https://docs.astral.sh/uv/) and the provided [`Justfile`](Justfile):

```bash
just setup     # create .venv and install MkDocs Material
just serve     # live-reload preview at http://127.0.0.1:8000
just build     # strict production build into ./site
```

Without `just`:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt
.venv/bin/mkdocs serve
```

Or with a plain virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Deployment

Pushes to `main` trigger the [`Pages`](.github/workflows/pages.yml) GitHub Actions
workflow, which runs `mkdocs build --strict` (failing on any broken link) and
publishes the result to GitHub Pages.

## Contributing

Review of the specification is the most valuable contribution right now — please
[open an issue](https://github.com/HUPO-PSI/mzPeak-specification/issues) for
anything unclear, missing, or incorrect. When editing prose, edit the relevant
file under `docs/`; the "Edit this page" pencil on each page links straight to it.
