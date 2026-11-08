# The Index File — `mzpeak_index.json`

An mzPeak archive is made up of multiple named files. To leave room for future
files and avoid complicated file-name resolution, an **index file** identifies
the contents of each file and broadly defines the kind of schema it carries. The
file **MUST** be serialized as UTF-8.


<div class="code-height-limit" markdown>

```json
{
  "files": [
    {
      "name": "spectra_data.parquet",
      "entity_type": "spectrum",
      "data_kind": "data_arrays",
      "column_mapping": [],
      "parameters": [],
      "checksum": "f054c947b6f0a92af17c6e6bda79f7c55618bdebb91a36934905d26b1cb7ba56bbc2f1874a9a0c3861a4a13caaca24974e50373c9c9381f8f6f249fcf0a603f6"
    },
    {
      "name": "spectra_peaks.parquet",
      "entity_type": "spectrum",
      "data_kind": "peaks",
      "column_mapping": [],
      "parameters": [],
      "checksum": "22d444170a02e2826bded97382b3f8a299bb265d742efc489a8b50170bbbc7af0400a8b3ffaf4fe431c29d3c3b7860dfba9dbc06b0e8a706e000dc7225942c87"
    },
    {
      "name": "spectra_metadata.parquet",
      "entity_type": "spectrum",
      "data_kind": "metadata",
      "column_mapping": [
        {
          "name": "ms level",
          "path": "ms_level",
          "accession": "MS:1000511"
        },
        {
          "name": "scan polarity",
          "path": "scan_polarity",
          "accession": "MS:1000465"
        },
        {
          "name": "spectrum representation",
          "path": "spectrum_representation",
          "accession": "MS:1000525",
          "term_marker": true
        },
        {
          "name": "spectrum type",
          "path": "spectrum_type",
          "accession": "MS:1000559",
          "term_marker": true
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
          "accession": "MS:1003060"
        },
        {
          "name": "number of peaks",
          "path": "number_of_peaks",
          "accession": "MS:1003059"
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
        },
        {
          "name": "polynomial delta coordinate interpolation",
          "path": "polynomial_delta_coordinate_interpolation",
          "accession": "MS:1003821"
        }
      ],
      "parameters": [],
      "checksum": "cddf8e537b82445f25f0f6759324b396000fb7e8aafae6400870763f2ed34d39416ecc24ae9aca2a7c2094f8386b2608b1c0849222a0d56f1608a1bc5b4c89e3"
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
          "accession": "MS:1000616"
        },
        {
          "name": "filter string",
          "path": "filter_string",
          "accession": "MS:1000512"
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
      "parameters": [],
      "checksum": "d82816a7e20751b95eb3bdca59bbdff99d3a8dc11eacd07f8941843b7e9733f4b342e982c2a88075aae197733c2632308fca33e39c7f7aaad5add773fd251415"
    },
    {
      "name": "spectra_metadata_precursors.parquet",
      "entity_type": "spectrum",
      "data_kind": "precursors",
      "column_mapping": [
        {
          "name": "isolation window target m/z",
          "path": "isolation_window.isolation_window_target",
          "accession": "MS:1000827",
          "unit": "MS:1000040"
        },
        {
          "name": "isolation window lower offset",
          "path": "isolation_window.isolation_window_lower_offset",
          "accession": "MS:1000828",
          "unit": "MS:1000040"
        },
        {
          "name": "isolation window upper offset",
          "path": "isolation_window.isolation_window_upper_offset",
          "accession": "MS:1000829",
          "unit": "MS:1000040"
        },
        {
          "name": "dissociation method",
          "path": "activation.dissociation_method",
          "accession": "MS:1000044",
          "term_marker": true
        },
        {
          "name": "collision energy",
          "path": "activation.collision_energy",
          "accession": "MS:1000045",
          "unit": "UO:0000266"
        }
      ],
      "parameters": [],
      "checksum": "8f9ee73d08c9536c44f7c937778217bde56c41bcd9bea287d8174174c1f7f0967823d58815f167e6703c0e0d03a3c3f0d3db9eeb3599f429cf14b420e0bb8179"
    },
    {
      "name": "spectra_metadata_selected_ions.parquet",
      "entity_type": "spectrum",
      "data_kind": "selected_ions",
      "column_mapping": [
        {
          "name": "selected ion m/z",
          "path": "selected_ion_mz",
          "accession": "MS:1000744",
          "unit": "MS:1000040"
        },
        {
          "name": "charge state",
          "path": "charge_state",
          "accession": "MS:1000041"
        },
        {
          "name": "intensity",
          "path": "peak_intensity",
          "accession": "MS:1000042",
          "unit": "MS:1000131"
        }
      ],
      "parameters": [],
      "checksum": "55dc29a675fa4a33806d7bc78095d0a07155d5257053682cd67f3d1ab062b6fc7b4e000f8835e32b5e18cb9652a94f934c4bb7ae10b4fa52210c826f653eb8ba"
    },
    {
      "name": "chromatograms_metadata.parquet",
      "entity_type": "chromatogram",
      "data_kind": "metadata",
      "column_mapping": [
        {
          "name": "scan polarity",
          "path": "scan_polarity",
          "accession": "MS:1000465"
        },
        {
          "name": "chromatogram type",
          "path": "chromatogram_type",
          "accession": "MS:1000626",
          "term_marker": true
        },
        {
          "name": "number of data points",
          "path": "number_of_data_points",
          "accession": "MS:1003060"
        }
      ],
      "parameters": [],
      "checksum": "c7a9057fae09f61cdce964a225828f53d4317d66b5d7eea02ddf363078dcf3ba04653faef7214ea40da57a1b65011496d95f309e57e043ba688eea204dc52db3"
    },
    {
      "name": "chromatograms_metadata_precursors.parquet",
      "entity_type": "chromatogram",
      "data_kind": "precursors",
      "column_mapping": [
        {
          "name": "isolation window target m/z",
          "path": "isolation_window.isolation_window_target",
          "accession": "MS:1000827",
          "unit": "MS:1000040"
        },
        {
          "name": "isolation window lower offset",
          "path": "isolation_window.isolation_window_lower_offset",
          "accession": "MS:1000828",
          "unit": "MS:1000040"
        },
        {
          "name": "isolation window upper offset",
          "path": "isolation_window.isolation_window_upper_offset",
          "accession": "MS:1000829",
          "unit": "MS:1000040"
        },
        {
          "name": "dissociation method",
          "path": "activation.dissociation_method",
          "accession": "MS:1000044",
          "term_marker": true
        },
        {
          "name": "collision energy",
          "path": "activation.collision_energy",
          "accession": "MS:1000045",
          "unit": "UO:0000266"
        }
      ],
      "parameters": [],
      "checksum": "48716c3b565ecebf883419f925b03ce4623c24ce20a13facfb42c5dfcd7069674c30d056ee31a40907e87e3828fa0f53111c16f527718b55d1928e1cf8296edb"
    },
    {
      "name": "chromatograms_metadata_selected_ions.parquet",
      "entity_type": "chromatogram",
      "data_kind": "selected_ions",
      "column_mapping": [
        {
          "name": "selected ion m/z",
          "path": "selected_ion_mz",
          "accession": "MS:1000744",
          "unit": "MS:1000040"
        },
        {
          "name": "charge state",
          "path": "charge_state",
          "accession": "MS:1000041"
        },
        {
          "name": "intensity",
          "path": "peak_intensity",
          "accession": "MS:1000042",
          "unit": "MS:1000131"
        }
      ],
      "parameters": [],
      "checksum": "e1167e9da3e6b59037a983e96180748308007a0454b58b7d94ca1a9f9e448a88f6e60d25c4899e60bea61888438841f7cd3ae769c461fccc7e4afb298f969b2a"
    },
    {
      "name": "chromatograms_data.parquet",
      "entity_type": "chromatogram",
      "data_kind": "data_arrays",
      "column_mapping": [],
      "parameters": [],
      "checksum": "6a927ac3063a04fe7fb6f961a82e7ac0d3cf5545b0e335db024348c45fe07c73d54d4c759a72761b3b049b49d0efc9f16e433e660e97609b4adfd64a9d7f23b9"
    }
  ],
  "metadata": {
    "instrument_configuration_list": [
      {
        "components": [
          {
            "component_type": "ionsource",
            "order": 1,
            "parameters": [
              {
                "accession": "MS:1000073",
                "name": "electrospray ionization"
              },
              {
                "accession": "MS:1000057",
                "name": "electrospray inlet"
              }
            ]
          },
          {
            "component_type": "analyzer",
            "order": 2,
            "parameters": [
              {
                "accession": "MS:1000083",
                "name": "radial ejection linear ion trap"
              }
            ]
          },
          {
            "component_type": "detector",
            "order": 3,
            "parameters": [
              {
                "accession": "MS:1000253",
                "name": "electron multiplier"
              }
            ]
          }
        ],
        "id": 1,
        "parameters": [
          {
            "accession": "MS:1000448",
            "name": "LTQ FT"
          },
          {
            "accession": "MS:1000529",
            "name": "instrument serial number",
            "value": "SN06061F"
          }
        ],
        "software_reference": "Xcalibur"
      },
      {
        "components": [
          {
            "component_type": "ionsource",
            "order": 1,
            "parameters": [
              {
                "accession": "MS:1000073",
                "name": "electrospray ionization"
              },
              {
                "accession": "MS:1000057",
                "name": "electrospray inlet"
              }
            ]
          },
          {
            "component_type": "analyzer",
            "order": 2,
            "parameters": [
              {
                "accession": "MS:1000079",
                "name": "fourier transform ion cyclotron resonance mass spectrometer",
                "unit": null,
                "value": null
              }
            ]
          },
          {
            "component_type": "detector",
            "order": 3,
            "parameters": [
              {
                "accession": "MS:1000624",
                "name": "inductive detector",
                "unit": null,
                "value": null
              }
            ]
          }
        ],
        "id": 0,
        "parameters": [
          {
            "accession": "MS:1000448",
            "name": "LTQ FT",
            "unit": null,
            "value": null
          },
          {
            "accession": "MS:1000529",
            "name": "instrument serial number",
            "unit": null,
            "value": "SN06061F"
          }
        ],
        "software_reference": "Xcalibur"
      }
    ],
    "file_description": {
      "contents": [
        {
          "accession": "MS:1000579",
          "name": "MS1 spectrum"
        },
        {
          "accession": "MS:1000580",
          "name": "MSn spectrum"
        }
      ],
      "source_files": [
        {
          "id": "RAW1",
          "location": "file:///examples",
          "name": "small.RAW",
          "parameters": [
            {
              "accession": "MS:1000569",
              "name": "SHA-1",
              "value": "b43e9286b40e8b5dbc0dfa2e428495769ca96a96"
            },
            {
              "accession": "MS:1000563",
              "name": "Thermo RAW format"
            },
            {
              "accession": "MS:1000768",
              "name": "Thermo nativeID format"
            }
          ]
        }
      ]
    },
    "software_list": [
      {
        "id": "Xcalibur",
        "parameters": [
          {
            "accession": "MS:1000532",
            "name": "Xcalibur"
          }
        ],
        "version": "1.1 Beta 7"
      },
      {
        "id": "pwiz",
        "parameters": [
          {
            "accession": "MS:1000615",
            "name": "ProteoWizard software"
          }
        ],
        "version": "3.0.23307"
      },
      {
        "id": "mzpeak_prototyping_convert1",
        "parameters": [
          {
            "accession": "MS:1000799",
            "name": "custom unreleased software tool",
            "value": "mzpeak_prototyping_convert"
          }
        ],
        "version": "0.1.0"
      }
    ],
    "data_processing_method_list": [
      {
        "id": "pwiz_Reader_Thermo_conversion",
        "methods": [
          {
            "order": 0,
            "parameters": [
              {
                "accession": "MS:1000544",
                "name": "Conversion to mzML"
              }
            ],
            "software_reference": "pwiz"
          }
        ]
      },
      {
        "id": "mzpeak_conversion1",
        "methods": [
          {
            "order": 1,
            "parameters": [
              {
                "name": "conversion options",
                "value": "-p -c -y -z -u small.mzML -o small.chunked.mzpeak"
              }
            ],
            "software_reference": "mzpeak_prototyping_convert1"
          }
        ]
      }
    ],
    "scan_settings_list": [],
    "run": {
      "default_data_processing_id": "pwiz_Reader_Thermo_conversion",
      "default_instrument_id": 0,
      "default_source_file_id": "RAW1",
      "id": "small",
      "params": [],
      "start_time": "2005-07-20T19:44:22Z"
    },
    "cv_list": [
      {
        "full_name": "Proteomics Standards Initiative Mass Spectrometry Ontology",
        "id": "MS",
        "uri": "http://purl.obolibrary.org/obo/ms/4.1.249/psi-ms.obo",
        "version": "4.1.249"
      },
      {
        "full_name": "Units of measurement ontology",
        "id": "UO",
        "uri": "http://purl.obolibrary.org/obo/uo/releases/2026-01-16/uo.obo",
        "version": "2026-01-16"
      }
    ],
    "version": "0.9.0",
    "sample_list": [
      {
        "id": "_x0031_",
        "name": "",
        "parameters": [
          {
            "accession": "MS:1000002",
            "name": "sample name",
            "value": "1"
          }
        ]
      }
    ]
  }
}
```

</div>

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
`path` being the actual column name. When not defined, the column name **MUST** start with `opt_`. This
provision ensures that if we later decide to add a new column to the specification, it will not collide
with an existing user-defined column name.

More is described in [the components section](./index_file_components.md)


## File-level metadata

File-level metadata **MUST** be stored in `mzpeak_index.metadata` encoded according to the schemas
below.

- [`cv_list`](./cv_list.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/cv_list.json)
- [`file_description`](./file_description.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/file_description.json)
- [`instrument_configuration_list`](./instrument_configuration.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/instrument_configuration.json)
- [`data_processing_method_list`](./data_processing.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/data_processing.json)
- [`software_list`](./software.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/software.json)
- [`sample_list`](./sample.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/sample.json)
- [`scan_settings_list`](./scan_settings_list.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/scan_settings_list.json)
- [`run`](./ms_run.md) [(schema)](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/ms_run.json)


!!! question "Open item — cleartext vs. encrypt-able metadata"
    Anything in `mzpeak_index.json` is necessarily cleartext to all readers
    unless ZIP encryption is used — and ZIP encryption is known to be flawed and
    inconsistent. Anything in a Parquet footer's key–value pairs *is*
    encrypt-able. The index is JSON for convenience and ease of access from
    scripting languages; whether some fields should move to encrypt-able Parquet
    metadata is unresolved.

## Format Versioning

The mzPeak archive's format version is written in `mzpeak_index.metadata.version`. The
value is formatted as a semantic version `#!js /(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)/`.
Version compatibility **SHOULD** be consistent with semantic versioning rules.

If a reader encounters a file with a major `version` greater than it knows how to read, it **SHOULD**
report an error. Attempting to parse the data under the previous rules **MAY** lead to a cascade of additional
errors.

A greater minor `version` indicates there **MAY** be columns that are read using
additional rules not compatible with previous versions, but which are not required for the overall
integrity of the file outside of proprietary extensions.

A greater patch version does not introduce new parsing rules, but **MAY** add additional defined columns
so they no longer require the `opt_` prefix, or add new `entity_type` or `data_kind` types which would
otherwise be treated as `other` in previous versions.

### Profiles

Profiles are separately versioned entities that add additional validation rules and contextual metadata.
An archive that follows a profile declares it in `metadata`. For example, [Imaging profile](../profiles/imaging.md)
is declared by setting `metadata.imaging.is_imaging` to `true`.

### For validation

New minor or patch versions **MAY** add additional validation rules, but new minor versions **SHOULD** not
make files valid under previous minor versions that were valid no longer valid. Profiles **SHOULD** abide
by the same rules.
