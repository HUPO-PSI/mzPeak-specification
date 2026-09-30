# Imaging Profile

!!! warning "Draft"
    Draft profile. The design discussion is in
    [issue #23](https://github.com/HUPO-PSI/mzPeak-specification/issues/23); what the profile
    leaves out is listed under [Open items](#open-items).

An imaging archive stores mass spectra acquired at positions on a sample. The profile adds
requirements to a [Core](../conformance.md#conformance-classes) archive; it takes nothing away.

## Marking an archive as imaging

An archive is an imaging archive when `metadata.imaging.is_imaging` in
[`mzpeak_index.json`](../archive/index-file.md) is `true`. An archive that carries pixel
positions **MUST** set it, whether or not it embeds images. An imaging archive **MUST** meet every
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
  has both null. At least one scan **MUST** belong to a pixel.
- Positions are indices into the pixel grid, counted **from 1** along each axis, so every set
  value is at least 1. They are not physical coordinates. A grid need not be fully sampled.
- A source that counts positions from another origin, such as absolute raster indices on a
  slide, is shifted by one constant per axis for the whole archive, and the constants are
  recorded in `metadata.imaging.position_offset`. A source that already counts from 1 is left
  as it is.
- The columns are integer columns. Readers **MUST** accept 32-bit and 64-bit widths, signed or
  unsigned.
- Each column **MUST** have a [column mapping](../layouts/metadata-tables.md#column-mapping) entry
  naming its term. The column names are those given above, not `opt_` names.
- Several scans **MAY** share one position, for example the scans of an ion-mobility frame.

**Positions define the image.** Pixel (1, 1) is the top-left corner; `position_x` increases to
the right and `position_y` downward. Terms that describe how the instrument scanned the sample,
such as scan pattern or line scan direction, are a record of the acquisition. A reader
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
| `IMS:1000053` absolute position offset x, `IMS:1000054` absolute position offset y — the physical position of the image's top-left corner on the target | **MAY** |
| children of `IMS:1000040` linescan sequence, `IMS:1000041` scan pattern, `IMS:1000048` scan type, `IMS:1000049` line scan direction | **MAY** |

- Pixel size is the length of a pixel's edge. It is not an area.
- Pixel size, max dimension and absolute position offset **MUST** carry a unit of length, and
  **SHOULD** use micrometre (`UO:0000017`).
- A writer that cannot determine the pixel size **SHOULD** omit it.

## Signal data

Spectra that share one m/z axis (imzML *continuous* mode) **MAY** be stored with
[grid encoding](../layouts/chunked-layout.md#grid-encoding), which keeps per spectrum only grid
indices and model parameters. Grid encoding changes the stored values unless the model is exact,
so it moves the archive to fidelity level L2 (below). Storing the shared axis once for the whole
archive is not defined.

## Provenance

When the source is an imzML file, `file_description.contents` **SHOULD** carry its storage mode
(`IMS:1000030` continuous, `IMS:1000031` processed), its identifier (`IMS:1000080` universally
unique identifier) and the `.ibd` checksum (`IMS:1000090` ibd MD5, `IMS:1000091` ibd SHA-1 or
`IMS:1000092` ibd SHA-256). These terms apply only to imzML sources.

## Fidelity

| Level | Meaning |
| :-- | :-- |
| **L0** | The source's identifier and checksum are kept, where the source has them. |
| **L1** | Decoded arrays equal the source values exactly, with no change of numeric type. |
| **L2** | A lossy transform was applied and its error bound is declared. |

How an archive declares its level, and the error bounds for L2, are [open items](#open-items).
Embedded images are outside these levels: a problem with an image does not change the fidelity
of the signal.

## The imaging block

`metadata.imaging` summarises the imaging metadata. The scan columns and the scan settings stay
authoritative: where a value appears both here and there, the two **MUST** be equal. The block
**MAY** be partial.

| Field | Meaning |
| :-- | :-- |
| `is_imaging` | `true` for an imaging archive. |
| `coordinate_base` | Always `1`. Kept for readers written against earlier drafts. |
| `position_offset` | `{x, y[, z]}`, the constant subtracted from each source position; absent when nothing was shifted. |
| `pixel_count` | `{x, y[, z]}`, the pixel counts of the grid, equal to the scan settings. |
| `pixel_count_source` | `declared` when the source declared the counts; `observed_max` when the writer derived them from the largest positions because the source declared none. |
| `mz_range` | `{min, max}` over the MS1 spectra; absent when there are none. |
| `images` | The embedded images, see below. |

## Embedded images

An archive **MAY** carry optical, histological or derived images, each as its own member under
`images/`, copied verbatim. TIFF is recommended. Each member is listed in `files` with
`entity_type` `image` and `data_kind` `other`, carries the Core checksum like every member, and
is described by one entry of `metadata.imaging.images`:

| Field | Meaning |
| :-- | :-- |
| `archive_path` | Member name, for example `images/image_0000.tiff`. **Required.** |
| `media_type` | Its media type, for example `image/tiff`. |
| `width`, `height` | Size in image pixels. |
| `sha256`, `size_bytes` | SHA-256 and size of the member, for readers that handle images without the index. |
| `role` | `optical`, `histology`, `overview`, `fluorescence` or `derived`. `optical` when absent. |
| `derived_subtype` | For a derived image: `tic` or `base_peak`. |
| `source_name` | The file the image was taken from. |
| `affine` | `{matrix: [a, b, c, d, e, f], maps: "image_px -> ms_px", registration_quality}`. Maps 0-based image pixel centres to 1-based MS pixel centres: `x_ms = a·col + b·row + c`, `y_ms = d·col + e·row + f`. |

The affine positions the image for display. `registration_quality` is `assumed_full_extent`
when the mapping was estimated from the image and grid extents rather than from landmarks.

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

Image roles are string values; no vocabulary terms exist for them yet.

## What a validator checks

1. `metadata.imaging.is_imaging` is `true`, and `coordinate_base`, if present, is `1`.
2. The scan metadata table has integer columns `position_x` and `position_y`, each with a column
   mapping entry for its term. In every row both are set or both are null, at least one row has
   both set, and every set value is at least 1.
3. `position_z`, if present, is an integer column with a column mapping entry for its term, and
   every set value is at least 1.
4. Exactly one `scan_settings_list` entry carries `IMS:1000042` and `IMS:1000043`, each with an
   integer value of at least 1.
5. Every pixel size, max dimension and absolute position offset present carries a unit of length.
6. `cv_list` declares `IMS` with a `uri` of the form given under [Vocabulary](#vocabulary), with
   a 40-character commit hash.
7. `pixel_count` and `mz_range`, if present, agree with the scan settings and the data.
8. Every image in `metadata.imaging.images` is listed in `files` with `entity_type` `image`, and
   its `sha256` and `size_bytes`, where present, match the member. A mismatch here is a warning;
   the Core checksum requirement still applies to the member.

## Open items

!!! question "Physical positions"
    Sources that record physical positions rather than grid indices, such as laser positions in
    millimetres, need a rule for deriving indices, pixel size and origin. Until then such data
    cannot claim the profile.

!!! question "Fidelity declaration"
    Where an archive declares its fidelity level, and the error bounds for L2 (the June
    discussion proposed a relative m/z error of at most 10⁻⁷ and a relative intensity error of at
    most 10⁻³), are undecided.

!!! question "Acquisition regions"
    This version describes one pixel grid per archive. Data with several acquisition regions fits
    only when all regions share that grid. A region column and a region-to-name mapping are not
    yet defined.

!!! question "Not yet covered"
    An m/z-oriented index to speed up ion images; a way to record that a value was assumed
    rather than read; registration beyond a single affine; regions of interest as spatial
    annotations; sub-images (`IMS:1000055` to `IMS:1000057`) and 3D stacks.
