# Tools

The software ecosystem around mzPeak is open source. This page lists the
utilities built on top of the format; for the read/write libraries themselves,
see [Implementations](implementations.md).

## Converters

- **mzML2mzPeak** — converts imzML / mzML to mzPeak (and back), with full
  round-trip verification. It reads input through
  [`mzdata`](https://github.com/mobiusklein/mzdata).
- *Roadmap:* a direct **vendor RAW → mzPeak** path (for example inside
  ProteoWizard [`msconvert`](https://proteowizard.sourceforge.io/)) so every
  vendor format converts in a single step, embedding the original acquisition
  method as provenance.

## Validation

- **mzPeakValidator** — a language-independent, profile-driven conformance
  validator (`mzpeak-validate file.mzpeak`). It checks index-file structure,
  schema consistency, JSON-schema compliance, CV accession/name agreement,
  reasonable data types, and cross-file consistency (for example that the
  declared number of data points matches the signal table).

## Viewers

- **mzPeak Explorer** — opens any `.mzpeak` file directly in the browser,
  streamed over HTTP range requests with no download. Built on the
  [TypeScript implementation](https://hupo-psi.github.io/mzpeakts/).
- **mzPeakIV** — an imaging viewer for mass-spectrometry imaging (MSI) datasets.
  It streams a `.mzpeak` file in place and can assign masses to RGB channels to
  reconstruct tissue anatomy directly in the browser.

## Example data

- **[Example data corpus ↗](https://object.storage.eu01.onstackit.cloud/v09/index.html)**
  — a public, browsable set of real `.mzpeak` files converted from open datasets
  across vendors, instruments, and modalities (LC-/GC-MS, imaging MS, and studies
  shipping SDRF / ISA sample metadata), each alongside its original. Every file
  opens directly in a browser viewer over HTTP range requests.

!!! note "Validator follows the API specification"
    The conformance validator is developed alongside the common cross-language
    API (see [Implementations](implementations.md)); semantic validation follows
    mzML precedent.
