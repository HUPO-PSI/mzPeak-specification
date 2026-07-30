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
unit is up to the writer. For consistency, we recommend using minutes.

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

This table uses the [metadata table](../layouts/metadata-tables.md) schema.

- **`index`** (integer) — the ascending 0-based index, incrementing by 1 per
  entry and **SHOULD** be time-sorted ascending. Primary key for the
  `chromatogram` facet.
- **`id`** (string) — a unique string identifier. Unlike for spectra, there is no "nativeId" format definition for chromatograms at this time.
- [**`scan_polarity (MS:1000465)`**](http://purl.obolibrary.org/obo/MS_1000465)
  (integer) — `1`, `-1`, or `null`.
- [**`chromatogram_type (MS:1000626)`**](http://purl.obolibrary.org/obo/MS_1000626)
  (CURIE) — e.g. total ion current
  ([`MS:1000235`](http://purl.obolibrary.org/obo/MS_1000235)), selected ion
  current ([`MS:1000627`](http://purl.obolibrary.org/obo/MS_1000627)), base peak
  ([`MS:1000628`](http://purl.obolibrary.org/obo/MS_1000628)), absorption
  ([`MS:1000812`](http://purl.obolibrary.org/obo/MS_1000812)),
  or selected ion current ([`MS:1000627`](http://purl.obolibrary.org/obo/MS_1000627)).
- **`data_processing_id`** (string) — the `id` of a `data_processing` that
  governs this chromatogram if it deviates from the default in
  `run.default_data_processing_id`; `null` otherwise. This applies data processing reflects how properties or attributes of the chromatogram are calculated. Data arrays
  are governed by the data processing methods defined in the [array index](../layouts/signal-data.md#the-array-index)
- **`parameters`** (list) — controlled or uncontrolled parameters; see
  [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
- **`number_of_auxiliary_arrays`** (integer) and **`auxiliary_arrays`** (list) ---
  see [auxiliary data arrays](../layouts/auxiliary-arrays.md).
- [**`number_of_data_points (MS:1003060)`**](http://purl.obolibrary.org/obo/MS_1003060)
  (integer) — data points stored in `chromatograms_data.parquet`.
- **MAY** supply a child of [`MS:1000808`](http://purl.obolibrary.org/obo/MS_1000808) (chromatogram attribute)
  one or more times.
    - [`chromatogram_title (MS:1000809)`](http://purl.obolibrary.org/obo/MS_1000809)
    - [`lowest_observed_mz (MS:1000528)`](http://purl.obolibrary.org/obo/MS_1000528)
    - [`highest_observed_mz (MS:1000527)`](http://purl.obolibrary.org/obo/MS_1000527)
    - [`lowest_observed_wavelength (MS:1000619)`](http://purl.obolibrary.org/obo/MS_1000619)
    - [`highest_observed_wavelength (MS:1000618)`](http://purl.obolibrary.org/obo/MS_1000618)
    - [`lowest_observed_ion_mobility (MS:1003437)`](http://purl.obolibrary.org/obo/MS_1003437)
    - [`highest_observed_ion_mobility (MS:1003438)`](http://purl.obolibrary.org/obo/MS_1003438)

## Chromatogram precursor metadata — `chromatograms_metadata_precursors.parquet`

```json
{
  "name": "chromatograms_metadata_precursors.parquet",
  "entity_type": "chromatogram",
  "data_kind": "metadata"
}
```

The method of precursor-ion selection and activation. Outside of sequential, multiple or parallel reaction monitoring,
this table will be empty or absent. Its schema is identical to the [spectrum precursor schema](./spectra.md#spectrum-precursor-metadata--spectra_metadata_precursorsparquet)



## Chromatogram selected ion metadata — `chromatograms_metadata_selected_ions.parquet`

```json
{
  "name": "chromatograms_metadata_selected_ions.parquet",
  "entity_type": "chromatogram",
  "data_kind": "selected_ions"
}
```

This table uses the [metadata table](../layouts/metadata-tables.md) schema.

Like the `precursor` group, outside of sequential, multiple or parallel reaction monitoring, this table will be empty
or absent. Its schema is identical to the [spectrum selected ion schema](./spectra.md#spectrum-selected-ion-metadata--spectra_metadata_selected_ionsparquet).

## Chromatogram product selection metadata — `chromatograms_metadata_products.parquet`

```json
{
  "name": "chromatograms_metadata_products.parquet",
  "entity_type": "chromatogram",
  "data_kind": "products"
}
```

This table uses the [metadata table](../layouts/metadata-tables.md) schema.

When describing single reaction monitoring (SRM) or multiple reaction monitoring (MRM) experiments, each product ion is
isolated separately with a different isolation window. This table is usually empty or absent. Its schema is identical to
the [spectrum products schema](./spectra.md#spectrum-product-selection-metadata--spectra_metadata_productsparquet).
