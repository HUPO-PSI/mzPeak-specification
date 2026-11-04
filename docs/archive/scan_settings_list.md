# mzPeak metadata scan settings list

The list of scan settings pre-configuring acquisition settings. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#scanSettingsList.>

## Use cases

This is primarily used for high-level configuration of data-independent acquisition strategies like SWATH or targeted MS.
Additionally used for imaging MS to define the spatial scanning parameters. These settings are associated with the rest of
the data in the archive through a link to an [instrument configuration](../instrument_configuration).

### Targeted MS

Targeted mass spectrometry methods may list their targeted ions **MAY** be added to a [`scan_settings`](#scan_settings)
entry's `targets` list. [Targets](#target) are described by any list of appropriate parameters, including terms like children
of [`MS:1000455|ion selection attribute`](http://purl.obolibrary.org/obo/MS_1000455), [`MS:1000792|isolation window attribute`](http://purl.obolibrary.org/obo/MS_1000792)
or [`MS:1000510|precursor activation attribute`](http://purl.obolibrary.org/obo/MS_1000510).

### Data-Independent Acquisition (DIA)

Like targeted MS, DIA methods may define their windows scheme with terms like children of [`MS:1000455|ion selection attribute`](http://purl.obolibrary.org/obo/MS_1000455),
[`MS:1000792|isolation window attribute`](http://purl.obolibrary.org/obo/MS_1000792) or [`MS:1000510|precursor activation attribute`](http://purl.obolibrary.org/obo/MS_1000510),
using a `target` for each window.

A target list describing a window list would look like:

```json
[
  {
    "parameters": [
      {
        "accession": "MS:1000827",
        "name": "isolation window target m/z",
        "value": 813.0,
        "unit": "MS:1000040"
      },
      {
        "accession": "MS:1000828",
        "name": "isolation window lower offset",
        "value": 13.0,
        "unit": "MS:1000040"
      },
      {
        "accession": "MS:1000829",
        "name": "isolation window upper offset",
        "value": 13.0,
        "unit": "MS:1000040"
      },
      {
        "accession": "MS:1000045",
        "name": "collision energy",
        "value": 41.57222844344905,
        "unit": "UO:0000266"
      }
    ]
  },
  {
    "parameters": [
      {
        "accession": "MS:1000827",
        "name": "isolation window target m/z",
        "value": 413.0,
        "unit": "MS:1000040"
      },
      {
        "accession": "MS:1000828",
        "name": "isolation window lower offset",
        "value": 13.0,
        "unit": "MS:1000040"
      },
      {
        "accession": "MS:1000829",
        "name": "isolation window upper offset",
        "value": 13.0,
        "unit": "MS:1000040"
      },
      {
        "accession": "MS:1000045",
        "name": "collision energy",
        "value": 24.945128779395297,
        "unit": "UO:0000266"
      }
    ]
  }
  // and more
]
```

This pre-registration makes it possible for software to scan just the header metadata of the file to find the window schema,
rather than scanning all unique entries in the [spectrum precursor table](../schemas/spectra.md#spectrum-precursor-metadata-spectra_metadata_precursorsparquet).

### Imaging MS

An imaging archive describes its pixel grid in the `parameters` list of one [`scan_settings`](#scan_settings) entry. The [Imaging profile](../profiles/imaging.md#grid-geometry) states which terms are required.

```json
{
  "id": "scansettings1",
  "parameters": [
    {
      "accession": "IMS:1000401",
      "name": "top down"
    },
    {
      "accession": "IMS:1000413",
      "name": "flyback"
    },
    {
      "accession": "IMS:1000480",
      "name": "horizontal line scan"
    },
    {
      "accession": "IMS:1000491",
      "name": "linescan left right"
    },
    {
      "accession": "IMS:1000042",
      "name": "max count of pixels x",
      "value": 3
    },
    {
      "accession": "IMS:1000043",
      "name": "max count of pixels y",
      "value": 3
    },
    {
      "accession": "IMS:1000044",
      "name": "max dimension x",
      "unit": "UO:0000017",
      "value": 300
    },
    {
      "accession": "IMS:1000045",
      "name": "max dimension y",
      "unit": "UO:0000017",
      "value": 300
    },
    {
      "accession": "IMS:1000046",
      "name": "pixel size (x)",
      "unit": "UO:0000017",
      "value": 100.0
    },
    {
      "accession": "IMS:1000047",
      "name": "pixel size y",
      "unit": "UO:0000017",
      "value": 100.0
    }
  ],
  "source_file_references": [],
  "targets": []
}
```


**Type:** `array`
**Items:** [`scan_settings`](#scan_settings)

---

## Definitions

### scan_settings
<a name="scan_settings"></a>

Description of the acquisition settings of the instrument prior to the start of the run. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#scanSettings>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | Yes | The unique identifier for this scan settings configuration |
| `source_file_references` | `array` of `string` | &nbsp; | &nbsp; |
| `targets` | `array` of [`target`](#target) | &nbsp; | A list of targeted ions or intervals on an inclusion list. |
| `parameters` | `array` of [`param`](param.md) | Yes | Additional parameters describing the scan settings. |

#### Property Details

**`id`** - `string` *(required)*

The unique identifier for this scan settings configuration

**`source_file_references`** - `array` of `string` *(optional)*

**`targets`** - `array` of [`target`](#target) *(optional)*

A list of targeted ions or intervals on an inclusion list.

**`parameters`** - `array` of [`param`](param.md) *(required)*

Additional parameters describing the scan settings.

---

### target
<a name="target"></a>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `parameters` | `array` of [`param`](param.md) | Yes | Additional parameters describing this target. |

#### Property Details

**`parameters`** - `array` of [`param`](param.md) *(required)*

Additional parameters describing this target.

---
