# Wavelength Spectra

Wavelength spectra — UV, DAD, and other electromagnetic-radiation (EMR) spectra ---
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
**SHOULD** be named `wavelength_spectrum_time`. The main wavelength-axis array
**SHOULD** be named `wavelength` and the intensity array `intensity`, mirroring the
`mz`/`intensity` convention for [mass spectra](../layouts/point-layout.md); as
elsewhere, readers resolve signal columns through the array index rather than by name.

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

This table uses the [metadata table](../layouts/metadata-tables.md) layout. It mirrors the [spectrum metadata](spectra.md#spectrum-metadata-spectra_metadataparquet)
schema.

- **`index`** (uint64) — ascending 0-based index, incrementing by 1 per entry,
  **SHOULD** be time-sorted. Primary key.
- **`id`** (string) — the "nativeID" string, per a
  [native identifier format](http://purl.obolibrary.org/obo/MS_1000767).
- **`time`** (float64) — the data-acquisition start time. **SHOULD** be
  replicated from the `scans` table for simpler filtering; for a spectrum
  with multiple scans it **SHOULD** be the minimum value if the run is in
  acquisition-time order. The time unit **MUST** be [minutes](http://purl.obolibrary.org/obo/UO_0000031)
- **`data_processing_id`** (string) — the `id` of a `data_processing` that
  governs this spectrum if it deviates from the default in
  `run.default_data_processing_id`; `null` otherwise. This applies data processing reflects how properties or attributes of the spectrum are calculated. Data arrays
  are governed by the data processing methods defined in the [array index](../layouts/signal-data.md#the-array-index)
- **`parameters`** (list).
- **`number_of_auxiliary_arrays`** (integer) / **`auxiliary_arrays`** (list) —
  see [auxiliary data arrays](../layouts/auxiliary-arrays.md).
- [**`spectrum_type`**](http://purl.obolibrary.org/obo/MS_1000559) (CURIE) — e.g. [`MS:1000804`](http://purl.obolibrary.org/obo/MS_1000804) "electromagnetic radiation spectrum".
- [**`number_of_data_points`**](http://purl.obolibrary.org/obo/MS_1003060) (integer) — profile points stored in `wavelength_spectra_data.parquet`.
- **MAY** supply a child of [`MS:1003058`](http://purl.obolibrary.org/obo/MS_1003058) (spectrum property) one or more times — e.g.
    - [`highest_observed_wavelength (MS:1000618)`](http://purl.obolibrary.org/obo/MS_1000618)
    - [`lowest_observed_wavelength (MS:1000619)`](http://purl.obolibrary.org/obo/MS_1000619)
    - [`lambda_max (MS:1003812)`](http://purl.obolibrary.org/obo/MS_1003812)
    - [`base_peak_intensity (MS:1000505)`](http://purl.obolibrary.org/obo/MS_1000505)
- **MAY** supply a child of [`MS:1000499`](http://purl.obolibrary.org/obo/MS_1000499) (spectrum attribute) one or more times — e.g.
    - [`spectrum_title (MS:1000796)`](http://purl.obolibrary.org/obo/MS_1000796).
- [`spectra_combination (MS:1000570)`](http://purl.obolibrary.org/obo/MS_1000570) (CURIE) — how multiple scans were combined to construct this spectrum. **MUST** be a child term of [`MS:1000570|spectra combination`](http://purl.obolibrary.org/obo/MS_1000570) such as [`MS:1000795|no combination`](http://purl.obolibrary.org/obo/MS_1000795) or [`MS:1000571|sum of spectra`](http://purl.obolibrary.org/obo/MS_1000571). If this column is absent, this value **SHOULD** be assumed to be [`MS:1000795|no combination`](http://purl.obolibrary.org/obo/MS_1000795).


## Wavelength spectrum scan metadata — `wavelength_spectra_metadata_scans.parquet`

```json
{
  "name": "wavelength_spectra_metadata_scans.parquet",
  "entity_type": "wavelength_spectrum",
  "data_kind": "scans"
}
```

This table uses the [metadata table](../layouts/metadata-tables.md) schema.

A scan or acquisition from the original raw file used to create a spectrum.

- **`source_index`** (uint64) — the spectrum this scan belongs to (foreign key).
- **`instrument_configuration_id`** (integer) — the `instrument_configuration`
  governing this scan referenced by `id`.
- **`parameters`** (list).
- **`scan_windows`** (list) — the list of windows in the main axis (wavelength array usually) that were acquired in this scan. This **SHOULD** be an empty list if no window metadata was stored.
  - (group)
    - [`scan_window_lower_limit` (MS:1000501)](http://purl.obolibrary.org/obo/MS_1000501) (float32) — The lower wavelength bound of a mass spectrometer scan window.
    - [`scan_window_upper_limit` (MS:1000500)](http://purl.obolibrary.org/obo/MS_1000500) (float32) — The upper wavelength of a mass spectrometer scan window.
- **MAY** supply children of
  [`MS:1000503`](http://purl.obolibrary.org/obo/MS_1000503) (scan attribute),
  [`MS:1000018`](http://purl.obolibrary.org/obo/MS_1000018) (scan direction,
  once), and [`MS:1000019`](http://purl.obolibrary.org/obo/MS_1000019) (scan law,
  once).
    - [`scan_rate (MS:1000015)`](http://purl.obolibrary.org/obo/MS_1000015)
    - [`dwell_time (MS:1000502)`](http://purl.obolibrary.org/obo/MS_1000502)
    - [`filter_string (MS:1000512)`](http://purl.obolibrary.org/obo/MS_1000512)
    - [`preset_scan_configuration (MS:1000616)`](http://purl.obolibrary.org/obo/MS_1000616)
    - [`analyzer_scan_offset (MS:1000803)`](http://purl.obolibrary.org/obo/MS_1000803)
    - [`elution_time (MS:1000826)`](http://purl.obolibrary.org/obo/MS_1000826)
    - [`interchannel_delay (MS:1000880)`](http://purl.obolibrary.org/obo/MS_1000880)
    - [`first_column_elution_time (MS:1002082)`](http://purl.obolibrary.org/obo/MS_1002082)
    - [`second_column_elution_time (MS:1002083)`](http://purl.obolibrary.org/obo/MS_1002083)