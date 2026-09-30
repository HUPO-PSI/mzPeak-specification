# Imaging Profile

!!! warning "Draft"
    This profile follows the imaging discussion of June 2026 (Kohlbacher, Klein, Römpp) and the
    review in [issue #23](https://github.com/HUPO-PSI/mzPeak-specification/issues/23). What it
    leaves out is listed under [Open items](#open-items).

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
- Positions are indices into the pixel grid, counted **from 1** along each axis. They are not
  physical coordinates.
- A writer whose source records positions on another origin, such as absolute raster indices on
  a slide, **MUST** shift them so that the smallest position on each axis is 1, and **SHOULD**
  record the shift with `IMS:1000053` and `IMS:1000054` (absolute position offset x, y) in the
  scan settings.
- The columns are stored as signed 64-bit or unsigned 32-bit integers. Readers **MUST** accept
  both.
- Each column **MUST** have a [column mapping](../layouts/metadata-tables.md#column-mapping) entry
  naming its term.
- Several scans **MAY** share one position, for example the scans of an ion-mobility frame.

**Positions define the image.** Pixel (1, 1) is the top-left corner; `position_x` increases to
the right and `position_y` downward, so a reader using 0-based arrays places a pixel at
`image[position_y - 1][position_x - 1]`. Terms that describe how the instrument scanned the
sample, such as scan pattern or line scan direction, are a record of the acquisition. A reader
**MUST NOT** use them to place pixels.

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
| `IMS:1000053` absolute position offset x, `IMS:1000054` absolute position offset y | **MAY**; **SHOULD** when positions were shifted |
| children of `IMS:1000040` linescan sequence, `IMS:1000041` scan pattern, `IMS:1000048` scan type, `IMS:1000049` line scan direction | **MAY** |

- Pixel size is the length of a pixel's edge. It is not an area.
- Pixel size, max dimension and offsets **MUST** carry a unit of length, and **SHOULD** use
  micrometre (`UO:0000017`).
- A writer that cannot determine the pixel size **SHOULD** omit it.

## Signal data

An image whose spectra share one m/z axis (imzML *continuous* mode) **SHOULD** store that axis
once, using [grid encoding](../layouts/chunked-layout.md#grid-encoding). Storing the full axis
with every spectrum is permitted and is the fallback when the axis does not fit a grid model.
Either way, the source's storage mode (`IMS:1000030` continuous, `IMS:1000031` processed) is
recorded as [provenance](#provenance).

## Provenance

When the source is an imzML file, `file_description.contents` **SHOULD** carry its storage mode
(`IMS:1000030` or `IMS:1000031`), its identifier (`IMS:1000080` universally unique identifier)
and the `.ibd` checksum (`IMS:1000090` MD5, `IMS:1000091` SHA-1 or `IMS:1000092` SHA-256).
Data converted directly from an instrument's own format has none of these; they are never
required.

## Fidelity

An imaging archive states how faithfully it holds the source signal:

| Level | Meaning |
| :-- | :-- |
| **L0** | Provenance kept: identifier and checksum of the source, as above. |
| **L1** | Decoded arrays equal the source values exactly, with no change of numeric type. **This is the default.** |
| **L2** | A lossy transform was applied and is declared in the array index with its error bound. Proposed bounds: relative m/z error at most 10⁻⁷, relative intensity error at most 10⁻³. |

Embedded images are not part of the L1 contract: a missing or mismatched image is a warning, not
a failure.

## The imaging block

`metadata.imaging` carries values a reader needs before it opens any Parquet file. The scan
columns and the scan settings stay authoritative: the block **MUST** agree with them where it
repeats them, and it **MAY** be partial.

| Field | Meaning |
| :-- | :-- |
| `is_imaging` | `true` for an imaging archive. |
| `coordinate_base` | The origin of the position columns. When present it **MUST** be `1`. |
| `pixel_count` | `{x, y[, z]}`, the pixel counts of the grid. |
| `pixel_count_source` | `declared` when copied from the source, `observed_max` when derived from the positions. |
| `mz_range` | `{min, max}` over the MS1 spectra. |
| `images` | The embedded images, see below. |

## Embedded images

An archive **MAY** carry optical, histological or derived images, each as its own member under
`images/`, copied verbatim. TIFF is recommended. Each member is listed in `files` with
`entity_type` and `data_kind` set to `other`, and described by one entry of
`metadata.imaging.images`:

| Field | Meaning |
| :-- | :-- |
| `archive_path` | Member name, for example `images/image_0000.tiff`. **Required.** |
| `media_type` | Its media type, for example `image/tiff`. |
| `width`, `height` | Size in image pixels. |
| `sha256`, `size_bytes` | Checksum and size of the member. |
| `role` | `optical`, `histology`, `overview`, `fluorescence` or `derived`. `optical` when absent. |
| `derived_subtype` | For a derived image: `tic` or `base_peak`. |
| `source_name` | The file the image was taken from. |
| `affine` | `{matrix: [a, b, c, d, e, f], maps: "image_px -> ms_px", registration_quality}`. Maps 0-based image pixels to 1-based MS pixels: `x_ms = a·col + b·row + c`, `y_ms = d·col + e·row + f`. |

The affine is a display hint, not a registration. `registration_quality` is
`assumed_full_extent` until a better registration is recorded.

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

Terms this profile introduces, such as image roles, are string values until they are minted in
the PSI-MS vocabulary; the imaging vocabulary itself has no active governance.

## What a validator checks

1. `metadata.imaging.is_imaging` is `true`, and `coordinate_base`, if present, is `1`.
2. The scan metadata table has integer columns `position_x` and `position_y`, each with a column
   mapping entry for its term. In every row both are set or both are null, at least one row has
   both set, and the smallest set value on each axis is 1.
3. `position_z`, if present, is an integer column with a column mapping entry for its term.
4. Exactly one `scan_settings_list` entry carries `IMS:1000042` and `IMS:1000043`, each with an
   integer value of at least 1.
5. Every pixel size, max dimension and offset present carries a unit of length.
6. `cv_list` declares `IMS` with a `uri` of the form given under [Vocabulary](#vocabulary), with
   a 40-character commit hash.
7. `pixel_count` and `mz_range`, if present, agree with the scan settings and the data.
8. Every image in `metadata.imaging.images` exists as a member and matches its `sha256` and
   `size_bytes`. A failure here is a warning.

## Open items

!!! question "Acquisition regions"
    This version describes one pixel grid per archive. Data with several acquisition regions fits
    only when all regions share that grid. A region column and a region-to-name mapping are not
    yet defined.

!!! question "Ion images"
    Reading one ion image means decoding every spectrum. An optional, recomputable index keyed by
    m/z (an m/z-major copy, a binned pyramid, or both) would bound that read. Its layout and its
    vocabulary terms are undecided.

!!! question "Not yet covered"
    A way to record that a value was assumed rather than read; physical positions alongside grid
    indices; registration beyond a single affine; regions of interest as spatial annotations;
    sub-images and 3D stacks (`IMS:1000055` to `IMS:1000057`).
