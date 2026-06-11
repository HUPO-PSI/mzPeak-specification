# Data Kinds

The `data_kind` field tells the reader the *semantics* of the data in a file, and
roughly what schema to expect. There are currently five controlled values:

| `data_kind` | Expected layout | Meaning |
| :-- | :-- | :-- |
| `data arrays` | [point](../layouts/point-layout.md) or [chunked](../layouts/chunked-layout.md) | Signal data, usually in its "raw" form, for the file's `entity_type`. |
| `peaks` | [point](../layouts/point-layout.md) or [chunked](../layouts/chunked-layout.md) | Like `data arrays`, but *processed* — implies a less-refined entry exists in a `data arrays` file. This is how profile **and** centroid signal coexist for a spectrum. |
| `metadata` | [packed parallel table](../layouts/metadata-tables.md) | Everything but the homogeneous signal arrays. May still be large. |
| `proprietary` | implementation-defined | Entirely the purview of the writer (often an instrument vendor). May not be Parquet. Should be ignored unless the reader is for that vendor. |
| `other` | implementation-defined | None of the above. May not be Parquet. |

Any value outside this list is treated as `other`. Files marked `proprietary`
and `other` are implementation-defined, but `other` files may still be of
interest to non-vendor readers (for example, text or XML configuration files in
an evolving metadata landscape). Vendors are encouraged to use `proprietary` for
binary or hard-to-digest contents.

## Adding a new data kind

This list is necessarily incomplete — new use-cases will emerge. For example, one
might store extracted LC-(IM)-MS feature bounding boxes as a separate file. To
add a new data kind:

1. **Pick a name** that fits in the index JSON. Prefer lower-case — e.g.
   `feature map` for extracted features.
2. **Pick a layout** (or layouts) for the data kind — e.g. the
   [packed parallel table](../layouts/metadata-tables.md) for lists of bounding
   boxes with associated metadata.
3. **Describe the relationships** with valid [entity types](entity-types.md).
   Prefer simple relationships (one-to-one, one-to-many). If no existing entity
   type fits, create a new one — an LC-MS feature might associate with
   `spectrum`, but there is no clean one-to-one or one-to-many relationship
   between spectra and LC-MS features, so a new entity type may be needed.
