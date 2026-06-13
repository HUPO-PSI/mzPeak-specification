# Chromatograms

Chromatograms are described by a **signal** file (`chromatograms_data.parquet`)
and a **metadata** file (`chromatograms_metadata.parquet`). Diagnostic traces are
currently carried here as well, pending their
[dedicated entity-type namespace](../archive/entity-types.md#decided-at-hupo-psi-2026-rome).

## Chromatogram signal data — `chromatograms_data.parquet`

```json
{
  "name": "chromatograms_data.parquet",
  "entity_type": "chromatogram",
  "data_kind": "data arrays"
}
```

The signal data is encoded using either
[point layout](../layouts/point-layout.md) or
[chunked layout](../layouts/chunked-layout.md). The entity index column **MUST**
be named `chromatogram_index`. The default primary axis is a
[`MS:1000595` time array](http://purl.obolibrary.org/obo/MS_1000595), though the
unit is up to the writer.

### Recommended Parquet encodings

| Column | Encoding |
| :-- | :-- |
| `chromatogram_index` | [delta encoding](https://parquet.apache.org/docs/file-format/data-pages/encodings/#delta-encoding-delta_binary_packed--5) |
| time arrays | [byte stream split](https://parquet.apache.org/docs/file-format/data-pages/encodings/#byte-stream-split-byte_stream_split--9) (byte shuffling) |

## Chromatogram metadata — `chromatograms_metadata.parquet`

```json
{
  "name": "chromatograms_metadata.parquet",
  "entity_type": "chromatogram",
  "data_kind": "metadata"
}
```

This table uses the
[packed parallel metadata table](../layouts/metadata-tables.md) schema.

### `chromatogram` (group)

- **`index`** (integer) — the ascending 0-based index, incrementing by 1 per
  entry and **SHOULD** be time-sorted ascending. Primary key for the
  `chromatogram` facet.
- **`id`** (string) — a unique string identifier.
- [**`MS_1000465_scan_polarity`**](http://purl.obolibrary.org/obo/MS_1000465)
  (integer) — `1`, `-1`, or `null`.
- [**`MS_1000626_chromatogram_type`**](http://purl.obolibrary.org/obo/MS_1000626)
  (CURIE) — e.g. total ion current
  ([`MS:1000235`](http://purl.obolibrary.org/obo/MS_1000235)), selected ion
  current ([`MS:1000627`](http://purl.obolibrary.org/obo/MS_1000627)), base peak
  ([`MS:1000628`](http://purl.obolibrary.org/obo/MS_1000628)), absorption
  ([`MS:1000812`](http://purl.obolibrary.org/obo/MS_1000812)).
- **`data_processing_ref`** (string) — a `data_processing` governing this
  chromatogram if it deviates from `run.default_data_processing_id`; `null`
  otherwise.
- **`parameters`** (list) — controlled or uncontrolled parameters; see
  [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
- **`number_of_auxiliary_arrays`** (integer) and **`auxiliary_arrays`** (list) —
  see [auxiliary data arrays](../layouts/auxiliary-arrays.md).
- [**`MS_1003060_number_of_data_points`**](http://purl.obolibrary.org/obo/MS_1003060)
  (integer) — data points stored in `chromatograms_data.parquet`.
- **MAY** supply a child of
  [`MS:1000808`](http://purl.obolibrary.org/obo/MS_1000808) (chromatogram
  attribute) one or more times.

### `precursor` (group)

The method of precursor-ion selection and activation. Outside of sequential, multiple or parallel reaction monitoring, this group will be unilaterally `null`.

- **`source_index`** (integer) — the chromatogram this precursor belongs to
  (foreign key).
- **`precursor_index`** (integer) — the chromatogram the precursor was created
  from (foreign key). See [spectra](spectra.md#precursor-group) for more details.
- **`precursor_id`** (string) — the `id` of the chromatogram referenced by
  `precursor_index`. See [spectra](spectra.md#precursor-group) for more details.
- **`isolation_window`** (group) — as for
  [spectra](spectra.md#precursor-group): **MUST** supply children of
  [`MS:1000792`](http://purl.obolibrary.org/obo/MS_1000792).
- **`activation`** (group) — as for [spectra](spectra.md#precursor-group):
  **MUST** supply [`MS:1000044`](http://purl.obolibrary.org/obo/MS_1000044)
  (dissociation method) or a child.

### `selected_ion` (group)

Like the `precursor` group, outside of sequential, multiple or parallel reaction monitoring, this group will be unilaterally `null`.

- **`source_index`** (integer) / **`precursor_index`** (integer) — foreign keys.
- **`ion_mobility_value`** (float) / **`ion_mobility_type`** (CURIE) — optional.
- **`parameters`** (list) — controlled or uncontrolled parameters; see
  [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
- **MUST** supply a child of
  [`MS:1000455`](http://purl.obolibrary.org/obo/MS_1000455) (ion selection
  attribute) one or more times — selected-ion m/z, charge state, intensity.
