# Glossary

A reference for terms used throughout this specification.

Apache Arrow
:   An in-memory columnar data model that shares Parquet's columnar abstraction; Arrow and Parquet schemas map to one another and are straightforward to convert between.

Apache Parquet
:   The strongly-typed, compressed, columnar on-disk format in which each facet of an mzPeak archive is stored. See [Anatomy of a Parquet file](../foundations/parquet.md).

Centroid
:   A spectrum (or peak list) reduced to discrete m/z–intensity peaks, as opposed to profile data.

Chromatogram
:   A measurement over time (for example a total ion current or extracted-ion trace); one of the mzPeak entity types. See [Entity Type](../archive/entity-types.md).

Chunked layout
:   A signal-data layout that cuts the sorted main axis into non-overlapping chunks (for example fixed m/z windows) — recording each chunk's start, end, and index — to allow random access along the axis. See [Chunked Layout](../layouts/chunked-layout.md).

Controlled vocabulary (CV)
:   A curated set of defined terms with stable accessions, used to annotate metadata unambiguously. mzPeak uses the PSI-MS controlled vocabulary.

CURIE
:   A compact URI of the form `prefix:reference` (for example `MS:1000559`) used to reference a controlled-vocabulary term.

Data kind
:   An index-file field declaring a member's semantics and expected schema family: `data arrays`, `peaks`, `metadata`, `proprietary`, or `other`. See [Data Kind](../archive/data-kinds.md).

Delta encoding
:   An opaque transform that stores successive differences instead of absolute values, compressing sorted axes such as m/z efficiently.

Entity type
:   An index-file field declaring what a member describes: `spectrum`, `chromatogram`, `wavelength spectrum`, or `other`. See [Entity Type](../archive/entity-types.md).

HUPO-PSI
:   The Human Proteome Organization Proteomics Standards Initiative, the body that governs mzPeak and maintains the PSI-MS controlled vocabulary.

imzML
:   The mzML-derived open standard for mass-spectrometry imaging data (XML plus an `.ibd` binary sidecar).

Index file (`mzpeak_index.json`)
:   The JSON manifest listing every archive member with its `entity_type` and `data_kind`, so a reader resolves files by meaning rather than by name. See [Index File](../archive/index-file.md).

Ion mobility
:   A gas-phase separation dimension (for example drift time or 1/K0) that may be stored as an array parallel to m/z and intensity.

m/z
:   Mass-to-charge ratio; the primary measurement axis of a mass spectrum.

mzML
:   The HUPO-PSI XML standard for mass-spectrometry data; mzPeak draws on its data model and reuses concepts such as controlled vocabularies where feasible.

mzPeak
:   An open, columnar mass-spectrometry data format: a ZIP archive (or directory) of Apache Parquet facets plus a JSON index, annotated using the PSI-MS controlled vocabulary under HUPO-PSI.

Null marking
:   A profile-data compression technique that replaces flanking zero-intensity points with `null` m/z and intensity values — so Parquet stores only a validity bit — reconstructing positions from a fitted m/z-spacing model. See [Null Marking](../layouts/signal-data.md#null-marking).

Numpress (MS-Numpress)
:   A family of lossy and lossless numeric compression schemes for m/z and intensity arrays, usable in mzPeak as an opaque transform.

Opaque transform
:   A per-array encoding (for example delta encoding or Numpress) applied within a chunk and recorded so a reader can decode it. Some transforms (such as certain Numpress modes) are lossy.

Packed parallel metadata tables
:   The metadata layout that stores several related sub-tables (spectrum, scan, precursor, selected ion) side by side, linked by primary- and foreign-key index columns. See [Packed Parallel Metadata Tables](../layouts/metadata-tables.md).

Page index
:   A Parquet footer structure — which mzPeak writers MUST emit — that enables random access below the row-group level.

Point layout
:   A signal-data layout that stores arrays as-is in parallel columns alongside a repeated entity-index column. See [Point Layout](../layouts/point-layout.md).

Profile
:   A spectrum stored as a quasi-continuous trace of m/z–intensity samples, as opposed to centroid data.

PSI-MS CV
:   The controlled vocabulary of mass-spectrometry terms maintained by HUPO-PSI; the semantic backbone of mzPeak metadata.

Row group
:   A horizontal partition of a Parquet file — the unit of columnar compression and coarse random access.

Sorting rank
:   An array's ordering role within a signal layout; sorting rank 0 is the sorted "main axis" around which all parallel arrays are arranged. Arrays of differing length SHOULD instead be stored as auxiliary arrays.

Total ion current (TIC)
:   The summed intensity recorded for a spectrum; frequently traced over time as a chromatogram.

Zero-run stripping
:   A profile-data size reduction that removes all but the first and last zero-intensity points in empty regions of a spectrum. See [Zero Run Stripping](../layouts/signal-data.md#zero-run-stripping).
