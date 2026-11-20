# Conformance

## Minimum archive

A conformant archive [MUST]{class="must-chip"} contain `mzpeak_index.json` at its root. All other members are
discovered through it; readers [MUST NOT]{class="must-not-chip"} depend on member names other than `mzpeak_index.json`.
mzPeak files containing only metadata (no spectra, no chromatograms) are thus still legal
mzPeak archives. Additionally, any of the Parquet files [MAY]{class="may-chip"} be empty but present, and readers must gracefully handle these files being valid schematically but containing no rows.

### Archive file order

There is no required order of files in an mzPeak archive. As a matter of course the `mzpeak_index.json` will be the last file written to a ZIP archive. Some data files rely on information from other files, making reading the archive incrementally impractical at this time. File names within the archive [SHOULD]{class="should-chip"} be unique, but in some unusual scenarios a ZIP archive may contain multiple files with the same name, in which case the last instance [SHOULD]{class="should-chip"} be used.

### Unpacked archives

The same requirements apply to an unpacked archive. There is no "ordering" on the host file system. File systems versioning is not considered here, but it is usually preferable to use the latest version of the files in the unpacked archive.

## Conformant archive

A conformant archive [MUST]{class="must-chip"}:

- Have `mzpeak_index.json` valid against `schema/mzpeak_index.json`, carrying `metadata.version`
   (SemVer `MAJOR.MINOR.PATCH`).
- Reference only present, valid Parquet files whose Arrow schema matches their
   `entity_type`/`data_kind`.
- Declare in `metadata.cv_list` every CV prefix used anywhere, with `uri` and `version`.
- Use exactly one signal layout per data/peak file (`point` or `chunk`), identified by the
   array-index `prefix`.
- Satisfy the [semantic invariants](#validation).

Additional members and metadata keys are permitted and [MUST NOT]{class="must-not-chip"} cause rejection.

## Conformant writer

A conformant writer [MUST]{class="must-chip"}:

- Produce a conformant archive.
- Write a Parquet **page index** for all columns and column statistics for row groups.
- Declare every CV used in `cv_list`, with a `uri` that identifies a fixed release or snapshot
  and the matching `version`.
- Record an array index sufficient to reconstruct every array **without parsing column names**.

## Conformant reader

A conformant reader [MUST]{class="must-chip"}:

- Resolve all members through `mzpeak_index.json`.
- Support both the `point` and `chunk` layouts.
- Treat `list`≡`large_list`, `string`≡`large_string`, `binary`≡`large_binary`.
- Resolve signal columns and transforms **via the array index**, not by column name.
- Resolve CV parameters by **accession** (name is advisory).
- Ignore unrecognized members, columns, metadata keys, `entity_type`/`data_kind`, or CV terms
  without error, preserving their literal values.

## Validation

**Syntactic.** A conformant archive [MUST]{class="must-chip"} satisfy:

- `mzpeak_index.json` and JSON metadata [MUST]{class="must-chip"} validate against the `schema/` JSON Schemas.
- Each Parquet file's Arrow schema [MUST]{class="must-chip"} match this specification.

**Semantic.** A conformant archive [MUST]{class="must-chip"} satisfy:

- Parallel columns of an entity have equal length.
- The sorting-rank-0 coordinate array is ascending, and each successive sorting-rank-n column sorts ascending within
  the same value of the sorting-rank-0 column.
- Every non-null foreign key resolves to an existing key/id.
- Chunks of an entity are ascending by `chunk_start` and non-overlapping.
- Within an entity, all `array_index` entries share one layout family — either every entry
  is `point` or every entry is one of the `chunk_*` formats. the two [MUST NOT]{class="must-not-chip"} be mixed.
- Time columns (for example `spectrum.time` and `wavelength_spectrum_time`) are expressed in
  [minutes](http://purl.obolibrary.org/obo/UO_0000031).
- Each signal Parquet file carries a [page index](https://parquet.apache.org/docs/file-format/pageindex/).
- `data_type`, `array_type`, and `unit` CURIEs in the array index descend from their required
  CV parents (`MS:1000518`, `MS:1000513`, and a unit term respectively).

The last four cannot be expressed in JSON Schema or the CvMapping rules, so a conformant
validator [MUST]{class="must-chip"} check them programmatically.

### Basic Integrity

All data storage media eventually degrades, and data transmission may also introduce small errors. Conformant mzPeak
files [MUST]{class="must-chip"} include a SHA-512 checksum for each file described in the `mzpeak_index.json`. The mzML file format uses
SHA-1 or MD5 for integrity checks, and while these are suitable for detecting bit rot, they are known to be vulnerable
to exploitation. SHA-512 is quantum-resistant and has no known exploitation. An mzPeak file may be checked for integrity
by rehashing each contained file and confirming the hex-digested checksum, stored in lowercase without separators, matches
the value shown in the `mzpeak_index.json` file for that file. For encrypted Parquet files, this hashing should be done on the
encrypted bytes. Files not described in `mzpeak_index.json` are not governed by this specification and should not be tested.
Additionally, the entire ZIP archive for packed archives should not be hashed because the packed and unpacked versions of the
same mzPeak file are equally valid.

Nothing prevents a malicious user from replacing a file and editing the `mzpeak_index.json` to show the new file's checksum.
For basic integrity testing, this mzPeak file would appear correct. For these scenarios, see the [Provenance](#provenance) section
below.

### Provenance

Confirming that the file was not modified following data acquisition is more challenging when the chain of custody
contains unknown or untrusted intermediate parties. To allow users to verify that an mzPeak file has not been manipulated, without
encrypting all of the data, the `provenance.parquet` [SHOULD]{class="should-chip"} be provided when the chain of trust from the instrument is available.
Failure to do so does not render the .mzPeak archive invalid, but does make it unverifiable and unsuitable for some forms of
regulatory evidence submission.

## Conformance classes

**Core** - satisfies every [MUST]{class="must-chip"} above. **Profiles** are optional and add requirements for one kind
of data. An archive declares a profile in the `metadata` of `mzpeak_index.json`; the
[Imaging profile](profiles/imaging.md) is declared by setting `metadata.imaging.is_imaging` to
`true`. A Core reader MUST still read Core content and ignore profile content it does not
implement.

## Demonstrating compliance

- Archives [SHOULD]{class="should-chip"} pass the reference validator (mzPeakValidator) at both levels (syntactic, semantic).
- The specification ships a reference implementation and a public conformance **test corpus**.
- Specification conformance is demonstrated by independent implementations round-tripping the entire corpus and each other's output without loss.