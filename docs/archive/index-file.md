# The Index File — `mzpeak_index.json`

An mzPeak archive is made up of multiple named files. To leave room for future
files and avoid complicated file-name resolution, an **index file** identifies
the contents of each file and broadly defines the kind of schema it carries. The
file **MUST** be serialised as UTF-8.

```json
{
  "files": [
    {
      "name": "spectra_data.parquet",
      "entity_type": "spectrum",
      "data_kind": "data_arrays",
      "column_mapping": [],
      "parameters": []
    },
    {
      "name": "spectra_peaks.parquet",
      "entity_type": "spectrum",
      "data_kind": "peaks",
      "column_mapping": [],
      "parameters": []
    },
    {
      "name": "spectra_metadata.parquet",
      "entity_type": "spectrum",
      "data_kind": "metadata",
      "column_mapping": [
        {
          "name": "ms level",
          "path": "ms_level",
          "accession": "MS:1000511",
        },
        {
          "name": "scan polarity",
          "path": "scan_polarity",
          "accession": "MS:1000465",
        },
        {
          "name": "spectrum representation",
          "path": "spectrum_representation",
          "accession": "MS:1000525",
        },
        {
          "name": "spectrum type",
          "path": "spectrum_type",
          "accession": "MS:1000559",
        },
        {
          "name": "lowest observed m/z",
          "path": "lowest_observed_mz",
          "accession": "MS:1000528",
          "unit": "MS:1000040"
        },
        {
          "name": "highest observed m/z",
          "path": "highest_observed_mz",
          "accession": "MS:1000527",
          "unit": "MS:1000040"
        },
        {
          "name": "number of data points",
          "path": "number_of_data_points",
          "accession": "MS:1003060",
        },
        {
          "name": "number of peaks",
          "path": "number_of_peaks",
          "accession": "MS:1003059",
        },
        {
          "name": "base peak m/z",
          "path": "base_peak_mz",
          "accession": "MS:1000504",
          "unit": "MS:1000040"
        },
        {
          "name": "base peak intensity",
          "path": "base_peak_intensity",
          "accession": "MS:1000505",
          "unit": "MS:1000131"
        },
        {
          "name": "total ion current",
          "path": "total_ion_current",
          "accession": "MS:1000285",
          "unit": "MS:1000131"
        }
      ],
      "parameters": []
    },
    {
      "name": "spectra_metadata_scans.parquet",
      "entity_type": "spectrum",
      "data_kind": "scans",
      "column_mapping": [
        {
          "name": "scan start time",
          "path": "scan_start_time",
          "accession": "MS:1000016",
          "unit": "UO:0000031"
        },
        {
          "name": "preset scan configuration",
          "path": "preset_scan_configuration",
          "accession": "MS:1000616",
        },
        {
          "name": "filter string",
          "path": "filter_string",
          "accession": "MS:1000512",
        },
        {
          "name": "ion injection time",
          "path": "ion_injection_time",
          "accession": "MS:1000927",
          "unit": "UO:0000028"
        },
        {
          "name": "scan window lower limit",
          "path": "scan_windows.scan_window_lower_limit",
          "accession": "MS:1000501",
          "unit": "MS:1000040"
        },
        {
          "name": "scan window upper limit",
          "path": "scan_windows.scan_window_upper_limit",
          "accession": "MS:1000500",
          "unit": "MS:1000040"
        }
      ],
      "parameters": []
    },
    ...
  ],
  "metadata": {
    "version": "0.9.0",
    "cv_list": [
      {
        "id": "MS",
        "full_name": "Proteomics Standards Initiative Mass Spectrometry Ontology",
        "uri": "http://purl.obolibrary.org/obo/ms/4.1.249/psi-ms.obo",
        "version": "4.1.249"
      },
      {
        "id": "UO",
        "full_name": "Units of measurement ontology",
        "uri": "http://purl.obolibrary.org/obo/uo/releases/2026-01-16/uo.obo",
        "version": "2026-01-16"
      }
    ],
    "file_description": { ... },
    ...
  }
}
```

The `metadata` object carries the archive `version`, the `cv_list` declaring every
controlled vocabulary used (with source URI and version, so CURIEs resolve
reproducibly), and the [file-level metadata](#file-level-metadata) objects.

Governed by the JSON Schema
[`schema/mzpeak_index.json`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/mzpeak_index.json).

Each entry pairs a [`data_kind`](data-kinds.md) with an
[`entity_type`](entity-types.md). Both are *loose enumerations* expected to grow
over time; resolving files by these controlled terms is more robust than matching
file names.

## Column mapping

By mapping controlled vocabulary terms to Parquet columns, we can make mzPeak more efficient at storing,
searching, and indexing cvParam-like data. The `column_mapping` object defines an explicit mapping from
column to an externally controlled definition like a controlled vocabulary term or a user-defined column.

When a column is defined in the appropriate schema, its `path` is pre-defined with the last entry in the
`path` being the actual column name. When not defined, the colum name **MUST** start with `opt_`. This
provision ensures that if we later decide to add a new column to the specification, it will not collide
with an existing user-defined column name.

### JSON schema
<a name="column_mapping"></a>

A mapping from a Parquet column to a controlled vocabulary term

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `name` | `string` | &nbsp; | The human-readable term name |
| `path` | `string` | &nbsp; | The path in a Parquet schema for the mapped column delimited at nesting levels by '.', omitting [list, item|element] tokens |
| `accession` | `string` or `null` | &nbsp; | The CURIE for the controlled vocabulary term, or null if no controlled vocabulary term is available. Null may be used to indicate that a column has a human readable name but does not map to a controlled vocabulary term |
| `unit` | `string` or `null` | &nbsp; | &nbsp; |

#### Property Details

**`name`** - `string` *(optional)*

The human-readable term name

*Examples:* `"ms level"`, `"filter string"`, `"selected ion m/z"`, `"collision energy"`, `"scan lower limit"`

**`path`** - `string` *(optional)*

The path in a Parquet schema for the mapped column delimited at nesting levels by '.', omitting [list, item|element] tokens

*Examples:* `"ms_level"`, `"isolation_window.target_mz"`, `"activation.collision_energy"`, `"scan_window.scan_lower_limit"`

**`accession`** - `string` or `null` *(optional)*

The CURIE for the controlled vocabulary term, or null if no controlled vocabulary term is available. Null may be used to indicate that a column has a human readable name but does not map to a controlled vocabulary term

**`unit`** - `string` or `null` *(optional)*



## File-level metadata

File-level metadata **SHOULD** be stored in `mzpeak_index.metadata` *and* in the
metadata Parquet files' key–value pairs, as JSON encoded according to the schemas
below:

- [`cv_list`](./cv_list.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/cv_list.json)
- [`file_description`](./file_description.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/file_description.json)
- [`instrument_configuration_list`](./instrument_configuration.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/instrument_configuration.json)
- [`data_processing_method_list`](./data_processing.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/data_processing.json)
- [`software_list`](./software.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/software.json)
- [`sample_list`](./sample.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/sample.json)
- [`scan_settings_list`](./scan_settings_list.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/scan_settings_list.json)
- [`run`](./ms_run.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/ms_run.json)

!!! question "Open item — cleartext vs. encryptable metadata"
    Anything in `mzpeak_index.json` is necessarily cleartext to all readers
    unless ZIP encryption is used — and ZIP encryption is known to be flawed and
    inconsistent. Anything in a Parquet footer's key–value pairs *is*
    encryptable. The index is JSON for convenience and ease of access from
    scripting languages; whether some fields should move to encryptable Parquet
    metadata is unresolved.

## Format Versioning

The mzPeak archive's format version is written in `mzpeak_index.metadata.version`. The
value is formatted as a semantic version `#!js /(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)/`.
Version compatibility **SHOULD** be consistent with semantic versioning rules.
