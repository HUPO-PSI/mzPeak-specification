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
      "data_kind": "data arrays"
    },
    {
      "name": "spectra_metadata.parquet",
      "entity_type": "spectrum",
      "data_kind": "metadata"
    },
    {
      "name": "chromatograms_data.parquet",
      "entity_type": "chromatogram",
      "data_kind": "data arrays"
    },
    {
      "name": "chromatograms_metadata.parquet",
      "entity_type": "chromatogram",
      "data_kind": "metadata"
    }
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

## File-level metadata

File-level metadata **SHOULD** be stored in `mzpeak_index.metadata` *and* in the
metadata Parquet files' key–value pairs, as JSON encoded according to the schemas
below:

- [`cv_list`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/cv_list.json)
- [`file_description`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/file_description.json)
- [`instrument_configuration_list`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/instrument_configuration.json)
- [`data_processing_method_list`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/data_processing.json)
- [`software_list`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/software.json)
- [`sample_list`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/sample.json)
- [`scan_settings_list`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/scan_settings_list.json)
- [`run`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/ms_run.json)

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
