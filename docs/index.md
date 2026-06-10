---
title: mzPeak File Format
description: A next-generation open standard for mass spectrometry data, built on Apache Parquet.
hide:
  - navigation
---

<div class="mzp-hero" markdown>
<span class="mzp-hero__eyebrow">HUPO-PSI Recommendation · Working Draft</span>
# mzPeak File Format
<p class="mzp-hero__tagline">
An open, columnar, random-access file format for storing mass spectra,
chromatograms, and rich instrument metadata — designed to succeed mzML for
modern, large-scale mass spectrometry.
</p>
<div class="mzp-badges">
  <span class="mzp-badge">Status: Draft</span>
  <span class="mzp-badge">Version 0.9 · Draft 5</span>
  <span class="mzp-badge mzp-badge--ghost">Built on Apache Parquet</span>
  <span class="mzp-badge mzp-badge--ghost">CC-BY-ND 4.0</span>
</div>
</div>

!!! warning "This is a working draft"
    This document is a **DRAFT** under active revision and has **not** yet been
    ratified through the [HUPO-PSI Document Process](https://www.psidev.info/).
    Content, schemas, and controlled-vocabulary terms may change. Feedback is
    explicitly solicited — please [open an issue](https://github.com/HUPO-PSI/mzPeak-specification/issues).

## Abstract

mzPeak is an open, next-generation file format for mass spectrometry data.
Advances in MS instrumentation — higher resolution, faster scan rates, greater
sensitivity, and the growing use of ion mobility and imaging — have sharply
increased the volume and dimensionality of the data produced in proteomics,
metabolomics, and lipidomics. Established open formats such as mzML and imzML
increasingly struggle with the resulting file sizes, data-access patterns, and
metadata demands, while vendor-specific formats offer faster access at the cost
of interoperability and long-term archival stability. mzPeak is designed to
address these needs as a community standard; the motivation and design rationale
are set out in the accompanying white paper [(1)](reference/references.md).

The format takes a hybrid approach: an archive of
[Apache Parquet](https://parquet.apache.org/) tables — packaged in an
uncompressed ZIP container, or an unpacked directory, together with a small JSON
index — that stores numerical signal data as compact, columnar binary while
keeping metadata both human- and machine-readable and anchored in the PSI-MS
controlled vocabulary. Building on the widely available Apache Parquet and Apache
Arrow libraries rather than a single core implementation, the on-disk structure
is language-independent. Uncompressed archive members and a required Parquet page
index let a reader locate and decode a single spectrum without parsing an entire
run, the basis for random access from local disk, object storage, or over HTTP.
This document specifies that format: its container, signal-data layouts, index
file, and metadata model.

## What you'll find here

<div class="mzp-cards" markdown>

<a class="mzp-card" href="introduction/overview/" markdown>
### Introduction
Why mzPeak exists, what problems it solves, and a high-level tour of an archive.
</a>

<a class="mzp-card" href="foundations/parquet/" markdown>
### Foundations
A short Parquet primer and how multiple Parquet files are bundled into one archive.
</a>

<a class="mzp-card" href="layouts/metadata-tables/" markdown>
### Data Layouts
Packed metadata tables, the array index, and the point & chunked signal layouts.
</a>

<a class="mzp-card" href="archive/index-file/" markdown>
### Archive Organization
The `mzpeak_index.json` file, data kinds, and entity types that organise a run.
</a>

<a class="mzp-card" href="schemas/spectra/" markdown>
### File Schemas
Concrete column-level schemas for spectra, chromatograms, and wavelength spectra.
</a>

<a class="mzp-card" href="reference/glossary/" markdown>
### Reference
Glossary, bibliography, authorship, and the intellectual-property statement.
</a>

</div>

## Anatomy of an archive

An mzPeak archive (`.mzpeak`) is a small set of named files:

| File | Contents |
| :--- | :--- |
| `mzpeak_index.json` | Manifest describing every file in the archive by entity type and data kind. |
| `spectra_metadata.parquet` | Spectrum-level and file-level metadata (descriptions, scans, precursors, selected ions). |
| `spectra_data.parquet` | Spectrum **profile** signal data, in point or chunked layout. |
| `spectra_peaks.parquet` *(optional)* | Spectrum **centroid** signal, stored separately from profile data. |
| `chromatograms_metadata.parquet` | Chromatogram-level and file-level metadata. |
| `chromatograms_data.parquet` | Chromatogram signal data, in point or chunked layout. |

Additional Parquet files may be added to cover further modalities (for example
[wavelength spectra](schemas/wavelength-spectra.md)) as the format grows.

## Reference implementations

mzPeak is backed by five independent, from-scratch implementations (not bindings
to a single core):

- **Rust** — read/write reference implementation · [HUPO-PSI/mzPeak](https://github.com/HUPO-PSI/mzPeak)
- **Python** — read-only, zero-copy Arrow/Pandas API
- **R** — read-only, `dplyr`-compatible access
- **C#** — read/write · [HUPO-PSI/mzPeak.NET](https://github.com/HUPO-PSI/mzPeak.NET)
- **JavaScript / TypeScript** — read-only, runs in the browser, Node, and Deno · [online viewer](https://hupo-psi.github.io/mzpeakts/)

See [Implementations](implementations.md) for details, and [Tools](tools.md) for
converters, the conformance validator, and viewers.

## Status of this document

This document provides information to the proteomics community about the mzPeak
file format. Distribution is unlimited. It will be ratified via the HUPO
Proteomics Standards Initiative (PSI) Document Process, and any alterations
**MUST** also follow the HUPO-PSI Document Process.

> **Version:** Draft 5 of version 0.9
