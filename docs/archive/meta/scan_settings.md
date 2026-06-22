## Use cases

This is used primarily used for high-level configuration of data-independent acquisition strategies like targeted MS, SWATH, and the like. Additionally used for imaging MS to define the spatial scanning parameters.

### Targeted MS

Targeted mass spectrometry methods may list their targeted ions **MAY** be added to a [`scan_settings`](#scan_settings) entry's `targets` list. [Targets](#target) are described by any list of appropriate parameters.

### Imaging MS

The presence of the imaging mass spectrometry controlled vocabulary and the `imaging` key in the [`mzpeak_index.json#metadata`](/docs/archive/index-file.md). Imaging-specific parameters **SHOULD** be added to a [`scan_settings`](#scan_settings) entry's `parameters` list.

```json
{
  "id": "scansettings1",
  "parameters": [
    {
      "accession": "IMS:1000401",
      "name": "top down",
    },
    {
      "accession": "IMS:1000413",
      "name": "flyback",
    },
    {
      "accession": "IMS:1000480",
      "name": "horizontal line scan",
    },
    {
      "accession": "IMS:1000491",
      "name": "linescan left right",
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
  "source_file_refs": [],
  "targets": []
}
```

Specifics are yet to be determined.
