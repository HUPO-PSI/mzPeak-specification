# Imaging Profile

!!! warning "Draft"
    This is the first version of the imaging profile. It defines how an imaging archive is marked
    and how pixel positions and grid geometry are stored. What it leaves out is listed under
    [Open items](#open-items).

An imaging archive stores mass spectra acquired at positions on a sample. The profile adds
requirements to a [Core](../conformance.md#conformance-classes) archive; it takes nothing away.

## Marking an archive as imaging

An archive is an imaging archive when `metadata.imaging.is_imaging` in
[`mzpeak_index.json`](../archive/index-file.md) is `true`. An imaging archive **MUST** meet every
requirement on this page.

```json
{ "metadata": { "imaging": { "is_imaging": true } } }
```

## Pixel positions

Pixel positions are columns of the
[scan metadata table](../schemas/spectra.md#spectrum-scan-metadata-spectra_metadata_scansparquet):

| Column | Term | Type | Requirement |
| :-- | :-- | :-- | :-- |
| `position_x` | `IMS:1000050` position x | integer | **MUST** |
| `position_y` | `IMS:1000051` position y | integer | **MUST** |
| `position_z` | `IMS:1000052` position z | integer | **MAY** |

- In each row, `position_x` and `position_y` **MUST** be both set or both null. A scan that
  belongs to a pixel has both set. A scan that belongs to no pixel, such as a calibration scan,
  has both null.
- The values are indices into the pixel grid. They are not physical coordinates.
- Each column **MUST** have a [column mapping](../layouts/metadata-tables.md#column-mapping) entry
  naming its term.
- Several scans **MAY** share one position.

**Positions define the image.** Terms that describe how the instrument scanned the sample, such as
scan pattern or line scan direction, are a record of the acquisition. A reader **MUST NOT** use
them to place pixels.

## Grid geometry

Exactly one entry of [`scan_settings_list`](../archive/scan_settings_list.md#imaging-ms) **MUST**
describe the pixel grid in its `parameters`:

| Term | Requirement |
| :-- | :-- |
| `IMS:1000042` max count of pixels x | **MUST**, an integer of at least 1 |
| `IMS:1000043` max count of pixels y | **MUST**, an integer of at least 1 |
| `IMS:1000046` pixel size (x) | **SHOULD** |
| `IMS:1000047` pixel size y | **SHOULD** |
| `IMS:1000044` max dimension x, `IMS:1000045` max dimension y | **MAY** |
| children of `IMS:1000040` linescan sequence, `IMS:1000041` scan pattern, `IMS:1000048` scan type, `IMS:1000049` line scan direction | **MAY** |

- Pixel size is the length of a pixel's edge. It is not an area.
- Pixel size and max dimension **MUST** carry a unit of length, and **SHOULD** use micrometre
  (`UO:0000017`).
- A writer that cannot determine the pixel size **SHOULD** omit it.

## Vocabulary

An imaging archive **MUST** declare the imaging vocabulary, `IMS`, in
[`cv_list`](../archive/cv_list.md). That vocabulary publishes no releases, so its `uri` **MUST**
name a commit, in the form
`https://raw.githubusercontent.com/imzML/imzML/<commit hash>/imagingMS.obo`:

```json
{
  "id": "IMS",
  "full_name": "Imaging Mass Spectrometry Ontology",
  "uri": "https://raw.githubusercontent.com/imzML/imzML/2c28b05ca297430303627d8c7d192cac1a2b1374/imagingMS.obo",
  "version": "1.1.0"
}
```

## What a validator checks

1. `metadata.imaging.is_imaging` is `true`.
2. The scan metadata table has integer columns `position_x` and `position_y`, each with a column
   mapping entry for its term. In every row both are set or both are null, and at least one row
   has both set.
3. `position_z`, if present, is an integer column with a column mapping entry for its term.
4. Exactly one `scan_settings_list` entry carries `IMS:1000042` and `IMS:1000043`, each with an
   integer value of at least 1.
5. Every pixel size and max dimension present carries a unit of length.
6. `cv_list` declares `IMS` with a `uri` of the form given under [Vocabulary](#vocabulary), with
   a 40-character commit hash.

## Open items

!!! question "Coordinate base"
    Whether positions count from 1, as in imzML, is not settled. Some instruments record
    positions as absolute indices on the slide, which do not start at 1. Until this is settled, a
    reader cannot assume that the pixel counts bound the positions.

!!! question "Acquisition regions"
    This version describes one pixel grid per archive. Data with several acquisition regions fits
    only when all regions share that grid. Regions with different pixel sizes are not yet covered.

!!! question "Not yet covered"
    A way to record that a value was assumed rather than read, physical positions alongside grid
    indices, and embedded optical images.
