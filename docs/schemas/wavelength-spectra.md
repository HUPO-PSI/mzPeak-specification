# Wavelength Spectra

Wavelength spectra — UV, DAD, and other electromagnetic-radiation (EMR) spectra —
are stored independently from mass spectra so the two modalities can have
divergent schemas without inflating the number of empty columns, and so a reader
need not sift through mass spectra to find EMR spectra (or vice versa). These
files **SHOULD** be present only if wavelength spectra are included in the
archive.

## Wavelength spectrum signal data — `wavelength_spectra_data.parquet`

```json
{
  "name": "wavelength_spectra_data.parquet",
  "entity_type": "wavelength spectrum",
  "data_kind": "data arrays"
}
```

The signal data is encoded using either
[point layout](../layouts/point-layout.md) or
[chunked layout](../layouts/chunked-layout.md). The entity index column **MUST**
be named `wavelength_spectrum_index`, and a co-located time column, if written,
**SHOULD** be named `wavelength_spectrum_time`.

When using [null marking](../layouts/signal-data.md#null-marking), follow the
[null semantics for signal data](../layouts/signal-data.md#null-semantics-for-signal-data)
carefully for profile data.

## Wavelength spectrum metadata — `wavelength_spectra_metadata.parquet`

```json
{
  "name": "wavelength_spectra_metadata.parquet",
  "entity_type": "wavelength spectrum",
  "data_kind": "metadata"
}
```

This table uses the
[packed parallel metadata table](../layouts/metadata-tables.md) schema. It
mirrors the [spectrum metadata](spectra.md#spectrum-metadata-spectra_metadataparquet)
layout but omits the `precursor` and `selected_ion` facets, because EMR spectra
have not been observed with isolation and fragmentation. `spectrum.index` and
`scan.source_index` **MUST** be the first column of their respective facets.

### `spectrum` (group)

- **`index`** (uint64) — ascending 0-based index, incrementing by 1 per entry,
  **SHOULD** be time-sorted. Primary key.
- **`id`** (string) — the "nativeID" string, per a
  [native identifier format](http://purl.obolibrary.org/obo/MS_1000767).
- **`time`** (float64) — the data-acquisition start time. **SHOULD** be
  replicated from the parallel `scan` facet for simpler filtering; for a spectrum
  with multiple scans it **SHOULD** be the minimum value if the run is in
  acquisition-time order. The time unit **MUST** be [minutes](http://purl.obolibrary.org/obo/UO_0000031)
- **`data_processing_ref`** (string) — a `data_processing` governing this
  spectrum if it deviates from the default; `null` otherwise.
- **`parameters`** (list).
- **`number_of_auxiliary_arrays`** (integer) / **`auxiliary_arrays`** (list) —
  see [auxiliary data arrays](../layouts/auxiliary-arrays.md).
- [**`MS_1000559_spectrum_type`**](http://purl.obolibrary.org/obo/MS_1000559)
  (CURIE) — e.g.
  [`MS:1000804`](http://purl.obolibrary.org/obo/MS_1000804) "electromagnetic
  radiation spectrum".
- [**`MS_1003060_number_of_data_points`**](http://purl.obolibrary.org/obo/MS_1003060)
  (integer) — profile points stored in `wavelength_spectra_data.parquet`.
- **MAY** supply a child of
  [`MS:1003058`](http://purl.obolibrary.org/obo/MS_1003058) (spectrum property)
  one or more times — e.g. λmax, lowest observed wavelength, total ion current.
- **MAY** supply a child of
  [`MS:1000499`](http://purl.obolibrary.org/obo/MS_1000499) (spectrum attribute)
  one or more times — e.g.
  [`MS_1000796_spectrum_title`](http://purl.obolibrary.org/obo/MS_1000796).

### `scan` (group)

- **`source_index`** (uint64) — the spectrum this scan belongs to (foreign key).
- **`instrument_configuration_ref`** (integer) — the `instrument_configuration`
  governing this scan referenced by `id`.
- **`parameters`** (list).
- **`scan_windows`** (list) — see the equivalent substructure for
  [spectra](spectra.md#scan-group).
- **MAY** supply a child of
  [`MS:1000503`](http://purl.obolibrary.org/obo/MS_1000503) (scan attribute) one
  or more times.
