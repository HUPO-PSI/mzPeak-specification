# Data Kinds

The `data_kind` field tells the reader the *semantics* of the data in a file, and
roughly what schema to expect.

| `data_kind`    | Expected layout | Used With Entity | Meaning |
| :------------- | :-------------- | :--------------- | :------ |
| `data_arrays`  | [point](../layouts/point-layout.md) or [chunked](../layouts/chunked-layout.md) | Any entity with continuous signal data | Signal data, usually in its "raw" form, for the file's `entity_type`. |
| `peaks`        | [point](../layouts/point-layout.md) or [chunked](../layouts/chunked-layout.md) | Any entity with discretized signal data | Like `data_arrays`, but *processed* — implies a less-refined entry exists in a `data_arrays` file. This is how profile **and** centroid signal coexist for a `spectrum`. |
| `metadata`     | [metadata table](../layouts/metadata-tables.md) | Any entity | Primary metadata facet of the `entity_type`, includes its `index` values and other top-level information. |
| `scans`        | [metadata table](../layouts/metadata-tables.md) | `spectrum`, `wavelength_spectrum` | Instrument scan events for the `entity_type`, expected for `spectrum`, not `chromatogram` |
| `precursors`   | [metadata table](../layouts/metadata-tables.md) | `spectrum`, `chromatogram` | Precursor isolation and activation event tying the product scan to the precursor scan. Expected for `spectrum` and MRM or SRM `chromatogram` or similar |
| `selected_ions`| [metadata table](../layouts/metadata-tables.md) | `spectrum`, `chromatogram` | Ions isolated during precursor selection. Like `precursors`, this is expected for `spectrum` and MRM or SRM `chromatogram` or similar |
| `products`     | [metadata table](../layouts/metadata-tables.md) | `spectrum`, `chromatogram` | Target isolation windows used for reaction monitoring. May appear SRM or MRM `spectrum` and `chromatogram`, but rare. |
| `signature`    | [provenance](../schemas/provenance.md) | `provenance` | A table of cryptographic signatures of components of the archive used for certifying that the content as written was attested to by an instrument known to its owner or vendor. The public key chain of trust certificates are encoded in the file metadata |
| `proprietary`  | implementation-defined | Any | Entirely the purview of the writer (often an instrument vendor). May not be Parquet. Should be ignored unless the reader is for that vendor. |
| `other`        | implementation-defined | Any | None of the above. May not be Parquet. |

Any value outside this list is treated as `other`, but implementations **MUST** preserve
the value provided rather than discarding the data kind label and recording an
undifferentiated "other". This permits forward compatibility as new data kinds are
added without updating existing code.

Files marked `proprietary` and `other` are implementation-defined, but `other`
files may still be of interest to non-vendor readers (for example, text or XML
configuration files in an evolving metadata landscape). Vendors are encouraged
to use `proprietary` for binary or hard-to-digest contents.


## Adding a new data kind

This list is necessarily incomplete — new use-cases will emerge. For example, one
might store extracted LC-(IM)-MS feature bounding boxes as a separate file. To
add a new data kind:

1. **Pick a name** that fits in the index JSON. Prefer lower-case — e.g.
   `feature_map` for extracted features.
2. **Pick a layout** (or layouts) for the data kind — e.g. the
   [metadata table](../layouts/metadata-tables.md) for lists of bounding
   boxes with associated metadata.
3. **Describe the relationships** with valid [entity types](entity-types.md).
   Prefer simple relationships (one-to-one, one-to-many). If no existing entity
   type fits, create a new one — an LC-MS feature might associate with
   `spectrum`, but there is no clean one-to-one or one-to-many relationship
   between spectra and LC-MS features, so a new entity type may be needed.
