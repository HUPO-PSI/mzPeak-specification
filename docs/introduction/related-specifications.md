# Relationship to Other Specifications

This format is not developed in isolation. It is designed to be complementary to —
and used in conjunction with — several existing and emerging community models:

- **[PSI Universal Spectrum Identifier (USI)](http://psidev.info/USI)** — a
  universal mechanism for referring to a specific spectrum in public
  repositories. mzPeak uses USIs in the `scan.spectrum_reference` field for
  spectra drawn from external sources (see
  [Spectrum metadata](../schemas/spectra.md#scan-group)).
- **[mzML](https://www.psidev.info/mzML)** — the current PSI recommendation for
  storing raw or processed mass spectrometry data. mzPeak draws on the mzML data
  model and re-uses concepts such as controlled vocabularies where feasible.
- **[SDRF (Sample and Data Relationship Format)](https://www.psidev.info/sdrf-sample-data-relationship-format)**
  — a representation of sample metadata. SDRF known at acquisition time may be
  carried alongside the data in an mzPeak archive.
- **[imzML](https://github.com/imzML/imzML/)** — the mzML-derived standard for
  mass-spectrometry imaging. mzPeak addresses imaging within the same archive via
  spatial coordinates in the spectrum metadata (see
  [Entity Types](../archive/entity-types.md)).

## Controlled vocabularies

mzPeak metadata is anchored in the **PSI-MS controlled vocabulary**. The
controlled vocabularies an archive relies on — with their versions and source
URIs — are declared in the archive's `cv_list` (see
[file-level metadata](../archive/index-file.md#file-level-metadata)), so a reader
can resolve every CURIE unambiguously and reproducibly.
