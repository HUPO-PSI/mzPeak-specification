# Spectra

Spectra are described by up to three files: a **signal** file
(`spectra_data.parquet`), an optional **peaks** file
(`spectra_peaks.parquet`), and a **metadata** file
(`spectra_metadata.parquet`).

!!! abstract "Profile vs. centroid — where each goes"
    By consensus at HUPO-PSI 2026, **profile** data goes in
    `spectra_data.parquet` and **centroid** data goes in
    `spectra_peaks.parquet`, *always*. When a file contains both for the same
    spectrum, both files are present and the metadata row carries both
    [`MS_1003060_number_of_data_points`](http://purl.obolibrary.org/obo/MS_1003060)
    and
    [`MS_1003059_number_of_peaks`](http://purl.obolibrary.org/obo/MS_1003059) so
    a reader knows which file(s) to read. A reader exposes a mode flag
    (profile / centroid) indicating which representation the caller wants.

    For timsTOF-style data that is centroided in m/z but profiled in ion
    mobility, the consensus is to treat it as centroid for the mass-spectrum
    dimension and place it in `spectra_peaks.parquet`. The presence of the metadata column [`MS_1003439_ion_mobility_frame_representation`](http://purl.obolibrary.org/obo/MS_1003439) **SHOULD** tell the reader if the ion mobility centroids have been pre-picked or not.

## Spectrum signal data — `spectra_data.parquet`

```json
{
  "name": "spectra_data.parquet",
  "entity_type": "spectrum",
  "data_kind": "data arrays"
}
```

The spectrum signal data is encoded using either
[point layout](../layouts/point-layout.md) or
[chunked layout](../layouts/chunked-layout.md). The entity index column **MUST**
be named `spectrum_index`, and a co-located time column, if written, **SHOULD**
be named `spectrum_time`. Non-mass spectra (UV, DAD) belong in
[`wavelength_spectra_data.parquet`](wavelength-spectra.md).

When using [null marking](../layouts/signal-data.md#null-marking), follow the
[null semantics for signal data](../layouts/signal-data.md#null-semantics-for-signal-data)
carefully for profile data.

!!! warning "Profile only"
    Only **profile** spectra are written here. Centroid spectra — including
    centroided views of profile spectra when both modes are stored — **MUST**
    instead be written to [`spectra_peaks.parquet`](#spectrum-peak-data-spectra_peaksparquet).
    The number of points written here for a spectrum **MUST** be recorded in the
    [`MS_1003060_number_of_data_points`](http://purl.obolibrary.org/obo/MS_1003060)
    column of `spectra_metadata.parquet`, to support read planning.

### Recommended Parquet encodings

| Column | Encoding |
| :-- | :-- |
| `spectrum_index` | [delta encoding](https://parquet.apache.org/docs/file-format/data-pages/encodings/#delta-encoding-delta_binary_packed--5) — ideal for repetitive or slowly increasing integers. |
| `spectrum_time` | [byte stream split](https://parquet.apache.org/docs/file-format/data-pages/encodings/#byte-stream-split-byte_stream_split--9) |
| m/z arrays | [byte stream split](https://parquet.apache.org/docs/file-format/data-pages/encodings/#byte-stream-split-byte_stream_split--9) (byte shuffling), or [RLE dictionary](https://parquet.apache.org/docs/file-format/data-pages/encodings/#dictionary-encoding-plain_dictionary--2-and-rle_dictionary--8) when there is ion-mobility data. |
| ion-mobility arrays | [RLE dictionary](https://parquet.apache.org/docs/file-format/data-pages/encodings/#dictionary-encoding-plain_dictionary--2-and-rle_dictionary--8); byte shuffling tends not to help. Consider increasing the dictionary page size. |

## Spectrum peak data — `spectra_peaks.parquet`

```json
{
  "name": "spectra_peaks.parquet",
  "entity_type": "spectrum",
  "data_kind": "peaks"
}
```

The spectrum peak lists, stored separately from the raw signal in
`spectra_data.parquet`. The entity index column **MUST** be named
`spectrum_index`, and a co-located time column, if written, **SHOULD** be named
`spectrum_time`. Any centroid spectra **MUST** be written here, not to
`spectra_data.parquet`. The number of peaks written for a spectrum **MUST** be
recorded in the
[`MS_1003059_number_of_peaks`](http://purl.obolibrary.org/obo/MS_1003059) column
of `spectra_metadata.parquet`, to support read planning.

## Spectrum metadata — `spectra_metadata.parquet`

```json
{
  "name": "spectra_metadata.parquet",
  "entity_type": "spectrum",
  "data_kind": "metadata"
}
```

This table uses the
[packed parallel metadata table](../layouts/metadata-tables.md) schema. Column
order is generally unspecified, but `spectrum.index`, `scan.source_index`,
`precursor.source_index`, and `selected_ion.source_index` **MUST** be the first
column of their respective facets. Where the lists below say **MAY**, that value
may be stored either as a column or as an entry in the
[parameters list](../layouts/metadata-tables.md#the-parameters-list) — a column
usually makes more sense when the value is usually present.

### `spectrum` (group)

- **`index`** (uint64) — the ascending 0-based index. **MUST** increment by 1 per
  entry and **SHOULD** be written in time-sorted ascending order. This is the
  primary key for the `spectrum` facet and the root unit of addressability.
- **`id`** (string) — the "nativeID" string identifier, formatted per a
  [native identifier format](http://purl.obolibrary.org/obo/MS_1000767). The
  specific format **SHOULD** be given in the
  [file-level metadata](../archive/index-file.md#file-level-metadata) under
  `file_description.source_files[0].parameters`, as in mzML.
- **`time`** (float64) — the data-acquisition start time. **SHOULD** be
  replicated from the parallel `scan` facet for simpler filtering; for a spectrum
  with multiple scans it **SHOULD** be the minimum value if the run is in
  acquisition-time order. The time unit **MUST** be [minutes](http://purl.obolibrary.org/obo/UO_0000031).
- [**`MS_1000511_ms_level`**](http://purl.obolibrary.org/obo/MS_1000511) (integer)
  — the MS stage number, or `null` for non-mass spectra.
- **`data_processing_id`** (string) — the `id` of a `data_processing` that
  governs this spectrum if it deviates from the default in
  `run.default_data_processing_id`; `null` otherwise. This applies data processing reflects how properties or attributes of the spectrum are calculated. Data arrays
  are governed by the data processing methods defined in the [array index](../layouts/signal-data.md#the-array-index)
- **`parameters`** (list) — controlled or uncontrolled parameters; see
  [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
- **`number_of_auxiliary_arrays`** (integer) — the count of
  [auxiliary arrays](../layouts/auxiliary-arrays.md) in this row's
  `auxiliary_arrays` column; lets a reader cheaply decide whether to decode them.
- **`auxiliary_arrays`** (list) — structures describing arrays that did not fit
  the [arrays-and-columns](../layouts/signal-data.md#arrays-and-columns)
  constraints. These may be large; load eagerly with care.
- **`mz_delta_model`** (list of float64) — coefficients of the per-row axis model
  used to reconstruct [null-marked data](../layouts/signal-data.md#null-marking) or a
  [parametric axis](../layouts/signal-data.md#parametric-axis-reconstruction). The
  list is interpreted according to the reconstruction-model `transform` CURIE on the
  corresponding array-index entry (which model family — `spacing`, `linear`,
  `sqrt_linear`); for the `spacing` model the terms are polynomial coefficients in
  descending power, including any zeros. There is no fixed length requirement, and
  this value **MAY** be `null` or empty if no model was learned.
  :octicons-tasklist-16: Add CV term name (<http://purl.obolibrary.org/obo/MS_1003820>)
- [**`MS_1000525_spectrum_representation`**](http://purl.obolibrary.org/obo/MS_1000525)
  (CURIE) — e.g.
  [`MS:1000128`](http://purl.obolibrary.org/obo/MS_1000128) "profile spectrum" or
  [`MS:1000127`](http://purl.obolibrary.org/obo/MS_1000127) "centroid spectrum".
- [**`MS_1000465_scan_polarity`**](http://purl.obolibrary.org/obo/MS_1000465)
  (integer) — `1` (positive), `-1` (negative), or `null`.
- [**`MS_1000559_spectrum_type`**](http://purl.obolibrary.org/obo/MS_1000559)
  (CURIE) — a child of MS:1000559, e.g. MS1 spectrum
  ([`MS:1000579`](http://purl.obolibrary.org/obo/MS_1000579)), MSn spectrum
  ([`MS:1000580`](http://purl.obolibrary.org/obo/MS_1000580)).
- [**`MS_1003060_number_of_data_points`**](http://purl.obolibrary.org/obo/MS_1003060)
  (integer) — profile points stored in `spectra_data.parquet`.
- [**`MS_1003059_number_of_peaks`**](http://purl.obolibrary.org/obo/MS_1003059)
  (integer) — discrete peaks stored in `spectra_peaks.parquet`.
- **MAY** supply a child of
  [`MS:1003058`](http://purl.obolibrary.org/obo/MS_1003058) (spectrum property)
  one or more times — e.g. base peak m/z, total ion current.
- **MAY** supply a child of
  [`MS:1000499`](http://purl.obolibrary.org/obo/MS_1000499) (spectrum attribute)
  one or more times — e.g.
  [`MS_1000796_spectrum_title`](http://purl.obolibrary.org/obo/MS_1000796).
- [`MS_1000570_spectra_combination](http://purl.obolibrary.org/obo/MS_1000570) (CURIE) — how multiple scans were combined to construct this spectrum. **MUST** be a child term of [`MS:1000570|spectra combination`](http://purl.obolibrary.org/obo/MS_1000570) such as [`MS:1000795|no combination`](http://purl.obolibrary.org/obo/MS_1000795) or [`MS:1000571|sum of spectra`](http://purl.obolibrary.org/obo/MS_1000571). If this column is absent, this value **SHOULD** be assumed to be [`MS:1000795|no combination`](http://purl.obolibrary.org/obo/MS_1000795).

### `scan` (group)

A scan or acquisition from the original raw file used to create a spectrum.

- **`source_index`** (uint64) — the `index` of the spectrum this scan belongs to
  (foreign key).
- **`scan_index`** (uint64) — the ascending 0-based index, incrementing by 1 per
  entry; uniquely identifies a scan, especially with multiple scans per spectrum
  (summing/averaging), chained together to form ion mobility frames while preserving the original data.
- **`spectrum_reference`** (string) — another spectrum corresponding to this
  scan. For local spectra, its `id`; for *external* sources, a
  [USI](https://www.psidev.info/usi) **SHOULD** be used. For unpublished
  collections, use `USI000000` as the collection identifier with the `id` of a
  source file in `file_description.source_files`. This might happen when summing and
  averaging spectra to improve signal quality (e.g. building a consensus spectrum), or
  when collating spectra across ion mobility measurements into an ion mobility frame.
- **`instrument_configuration_id`** (integer) — the `instrument_configuration`
  governing this scan referenced by `id`.
- **`parameters`** (list) — controlled or uncontrolled parameters; see
  [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
- **`ion_mobility_value`** (float64) — optional ion-mobility measurement for this
  scan. If multiple ion mobility values are used and combined on the instrument, such as with a FAIMS compensation voltage ramp, the writer **SHOULD** record multiple `scan` records per `spectrum` with the [ramp start](http://purl.obolibrary.org/obo/MS_1003450) and [ramp end](http://purl.obolibrary.org/obo/MS_1003451) values in this column, using the [`MS:1000571|sum of spectra`](http://purl.obolibrary.org/obo/MS_1000571) combinator. If multiple ion mobility values are separately acquired per frame, then an ion mobility dimension **MUST** instead be used in the [signal data](#spectrum-signal-data--spectra_dataparquet) and/or [peak data](#spectrum-peak-data--spectra_peaksparquet).
- **`ion_mobility_type`** (CURIE) — optional; a child of
  [`MS:1002892`](http://purl.obolibrary.org/obo/MS_1002892). See **`scan.ion_mobility_value`** for more details on ion mobility ramps.
- **`scan_windows`** (list) — the list of windows in the main axis (m/z array usually) that were acquired in this scan. This **SHOULD** be an empty list if no window metadata was stored.
  - (group)
    - [MS_1000501_scan_window_lower_limit](http://purl.obolibrary.org/obo/MS_1000501) (float32) — The lower m/z bound of a mass spectrometer scan window.
    - [MS_1000500_scan_window_upper_limit](http://purl.obolibrary.org/obo/MS_1000500) (float32) — The upper m/z bound of a mass spectrometer scan window.
- **MAY** supply children of
  [`MS:1000503`](http://purl.obolibrary.org/obo/MS_1000503) (scan attribute),
  [`MS:1000018`](http://purl.obolibrary.org/obo/MS_1000018) (scan direction,
  once), and [`MS:1000019`](http://purl.obolibrary.org/obo/MS_1000019) (scan law,
  once).

### `precursor` (group)

The method of precursor-ion selection and activation.

- **`source_index`** (uint64) — the spectrum index this precursor belongs to (foreign
  key).
- **`precursor_index`** (uint64) — the spectrum index of the precursor was created from, the parent spectrum (foreign key). When this spectrum is not present in the current archive, this **SHOULD** be `null`
- **`precursor_id`** (string) — the `id` of the spectrum referenced by
  `precursor_index`. If `precursor_index` is `null`, this may still be populated, but a [USI](https://www.psidev.info/usi) **SHOULD** be used. For unpublished collections, use `USI000000` as the collection identifier with the `id` of a source file in `file_description.source_files`.
- **`isolation_window`** (group) — the isolation/selection window.
    - **`parameters`** (list) — controlled or uncontrolled parameters; see [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
    - **MUST** supply children of
      [`MS:1000792`](http://purl.obolibrary.org/obo/MS_1000792) (isolation-window
      attribute) one or more times; promote to columns when available — e.g.
      isolation-window target m/z, lower offset, upper offset.
- **`activation`** (group) — the activation/dissociation type and energy.
    - **`parameters`** (list) — controlled or uncontrolled parameters; see [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
    - **MAY** supply children of
      [`MS:1000510`](http://purl.obolibrary.org/obo/MS_1000510) (precursor
      activation attribute).
    - **MUST** supply [`MS:1000044`](http://purl.obolibrary.org/obo/MS_1000044)
      (dissociation method) or a child, one or more times.

### `selected_ion` (group)

An ion isolated for dissociation.

- **`source_index`** (uint64) — the spectrum this selected ion belongs to
  (foreign key).
- **`precursor_index`** (uint64) — the spectrum the selected ion was created from
  (foreign key).
- **`ion_mobility_value`** (float64) / **`ion_mobility_type`** (CURIE) — See the [`scan.ion_mobility_value`](#scan-group) for details storing scalar values. If multiple ion mobility values are available for the selected ion that have been combined, but no ion mobility centroid is available as when a ramp has been used, report multiple `selected_ion` records, one for the ramp start and one for the ramp end.
- **`parameters`** (list) — controlled or uncontrolled parameters; see [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
- **MUST** supply a child of
  [`MS:1000455`](http://purl.obolibrary.org/obo/MS_1000455){.cvparam} (ion selection
  attribute) one or more times — e.g. selected-ion m/z, charge state, intensity.


### `product` (group) (optional)

When describing single reaction monitoring (SRM) or multiple reaction monitoring (MRM) experiments, each product ion is isolated separately with a different isolation window. This group is optional and **MAY** be omitted when the relevant data is absent.

- **`source_index`** (integer) — the spectrum this product belongs to
  (foreign key).
- **`product_index`** (integer) — the ascending 0-based index, incrementing by 1 per
  entry. This number uniquely identifies each product ion selection across all rows.
- **`isolation_window`** (group) — the isolation/selection window for this product ion, like the Q3 transmission window on a triple-quadrupole instrument.
    - **`parameters`** (list) — controlled or uncontrolled parameters; see [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
    - **MUST** supply children of
      [`MS:1000792`](http://purl.obolibrary.org/obo/MS_1000792) (isolation-window
      attribute) one or more times; promote to columns when available — e.g.
      isolation-window target m/z, lower offset, upper offset.
- **`parameters`** (list) — controlled or uncontrolled parameters; see
  [the parameters list](../layouts/metadata-tables.md#the-parameters-list).
