# Conformance

## Minimum archive

A conformant archive MUST contain `mzpeak_index.json` at its root. All other members are
discovered through it; readers MUST NOT depend on member names other than `mzpeak_index.json`.
mzPeak files containing only metadata (no spectra, no chromatograms) are thus still legal
mzPeak archives.

## Conformant archive

A conformant archive **MUST**:

1. have `mzpeak_index.json` valid against `schema/mzpeak_index.json`, carrying `metadata.version`
   (SemVer `MAJOR.MINOR.PATCH`);
2. reference only present, valid Parquet files whose Arrow schema matches their
   `entity_type`/`data_kind`;
3. declare in `metadata.cv_list` every CV prefix used anywhere, with `uri` and `version`;
4. use exactly one signal layout per data/peak file (`point` or `chunk`), identified by the
   array-index `prefix`;
5. satisfy the [semantic invariants](#validation).

Additional members and metadata keys are permitted and MUST NOT cause rejection.

## Conformant writer

A conformant writer **MUST**:

- produce a conformant archive;
- write a Parquet **page index** for the index/coordinate columns;
- declare every CV used (version-pinned) in `cv_list`;
- record an array index sufficient to reconstruct every array **without parsing column names**.

## Conformant reader

A conformant reader **MUST**:

- resolve all members through `mzpeak_index.json`;
- support both the `point` and `chunk` layouts;
- treat `list`≡`large_list`, `string`≡`large_string`, `binary`≡`large_binary`;
- resolve signal columns and transforms **via the array index**, not by column name;
- resolve CV parameters by **accession** (name is advisory);
- ignore unrecognized members, columns, metadata keys, `entity_type`/`data_kind`, or CV terms
  without error, preserving their literal values.

## Validation

**Syntactic.** A conformant archive **MUST** satisfy:

- `mzpeak_index.json` and JSON metadata MUST validate against the `schema/` JSON Schemas;
- each Parquet file's Arrow schema MUST match this specification.

**Semantic.** A conformant archive **MUST** satisfy:

- parallel columns of an entity have equal length;
- the sorting-rank-0 coordinate array is ascending;
- every non-null foreign key resolves to an existing key/id;
- chunks of an entity are ascending by `chunk_start` and non-overlapping.

## Conformance classes

**Core** — satisfies every MUST above. **Profiles** (OPTIONAL, e.g. *Imaging*) register through
the index extension mechanism and add requirements; a Core reader MUST still read Core content
and ignore profile content it does not implement.

## Demonstrating compliance

- Archives SHOULD pass the reference validator (mzPeakValidator) at both levels (syntactic, semantic).
- The specification ships a reference implementation and a public conformance **test corpus**.
- Specification conformance is demonstrated by independent implementations round-tripping the entire corpus and each other's output without loss.