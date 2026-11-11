---
title: mzPeak File Format
description: A next-generation open standard for mass spectrometry data, built on Apache Parquet.
hide:
  - navigation
---

<div class="mzp-hero" markdown>
<img class="mzp-hero__logo" src="assets/img/mzpeak-logo.png" alt="mzPeak">

<span class="mzp-hero__eyebrow">HUPO-PSI Recommendation · Working Draft</span>

# File Format Specification
<p class="mzp-hero__tagline">
An open, columnar, random-access file format for storing mass spectra,
chromatograms, and rich instrument metadata — designed to succeed mzML for
modern, large-scale mass spectrometry.
</p>
<div class="mzp-badges">
  <span class="mzp-badge">Status: Draft</span>
  <span class="mzp-badge">Version 0.9 - Draft 6</span>
  <span class="mzp-badge mzp-badge--ghost">Built on Apache Parquet</span>
  <span class="mzp-badge mzp-badge--ghost">CC-BY-ND 4.0</span>
</div>
</div>

!!! warning "This is a working draft"
    This document is a **DRAFT** under active revision and has **not** yet been
    ratified through the [HUPO-PSI Document Process](https://www.psidev.info/).
    Content, schemas, and controlled-vocabulary terms may change. Feedback is
    explicitly solicited, please [open an issue](https://github.com/HUPO-PSI/mzPeak-specification/issues).

## Abstract

mzPeak is an open, next-generation file format for mass spectrometry data.
Advances in MS instrumentation have sharply increased the volume and dimensionality.
Established open formats struggle with the resulting file sizes, data-access patterns,
and metadata demands. mzPeak is designed to address these needs as a community standard,
the motivation and design rationale are set out in the accompanying white paper [(1)](reference/references.md).

The on-disk structure is language-independent, but uses widely available libraries across
many languages to decode a entries without parsing an entire run. It works with any byte storage,
on local disk, object storage, or over HTTP. This document specifies that format: its
container, data layouts, index file, and metadata model.

## What you'll find here

<div class="grid cards" markdown>

-   __Introduction__

    ---

    Why mzPeak exists, what problems it solves, and a high-level tour of an archive.

    [:octicons-arrow-right-24: Overview & motivation](introduction/overview.md)

-   __Foundations__

    ---

    A short Parquet primer and how multiple Parquet files are bundled into one archive.

    [:octicons-arrow-right-24: Parquet & containers](foundations/parquet.md)

-   __Data Layouts__

    ---

    Packed metadata tables, the array index, and the point & chunked signal layouts.

    [:octicons-arrow-right-24: Layouts](layouts/metadata-tables.md)

-   __Archive Organization__

    ---

    The `mzpeak_index.json` file, data kinds, and entity types that organise a run.

    [:octicons-arrow-right-24: The index file](archive/index-file.md)

-   __File Schemas__

    ---

    Concrete column-level schemas for spectra, chromatograms, and wavelength spectra.

    [:octicons-arrow-right-24: Schemas](schemas/spectra.md)

-   __Implementations__

    ---

    The read/write libraries — Rust, Python, R, C#, Java, JavaScript/TypeScript, and C++.

    [:octicons-arrow-right-24: Implementations](implementations.md)

-   __Tools__

    ---

    Converters, the conformance validator, browser viewers, and example data.

    [:octicons-arrow-right-24: Tools](tools.md)

-   __Reference__

    ---

    Glossary, bibliography, authorship, and the intellectual-property statement.

    [:octicons-arrow-right-24: Reference](reference/glossary.md)

</div>

## Reference implementations

mzPeak is backed by seven independent, from-scratch implementations (not bindings
to a single core):

- **Rust**: read/write reference implementation · [HUPO-PSI/mzPeak](https://github.com/HUPO-PSI/mzPeak)
- **Python**: read-only, zero-copy Arrow/Pandas API · [mzpeak_prototyping](https://github.com/mobiusklein/mzpeak_prototyping/tree/main/python)
- **R**: read-only, `dplyr`-compatible access · [mzpeak_prototyping](https://github.com/mobiusklein/mzpeak_prototyping/tree/main/R)
- **C#**: read/write · [HUPO-PSI/mzPeak.NET](https://github.com/HUPO-PSI/mzPeak.NET)
- **Java**: read/write demonstrator · [okohlbacher/mzPeakJ](https://github.com/okohlbacher/mzPeakJ)
- **JavaScript / TypeScript**: read-only, runs in the browser, Node, and Deno · [online viewer](https://hupo-psi.github.io/mzpeakts/)
- **C++**: read-only, work in progress · [OpenMS/mzpeak](https://github.com/OpenMS/mzpeak)

See [Implementations](implementations.md) for details, and [Tools](tools.md) for
converters, the conformance validator, and viewers.

## Status of this document

This document provides information to the proteomics community about the mzPeak
file format. Distribution is unlimited. It will be ratified via the HUPO
Proteomics Standards Initiative (PSI) Document Process, and any alterations
must also follow the HUPO-PSI Document Process.

> **Version:** Draft 6 of version 0.9
