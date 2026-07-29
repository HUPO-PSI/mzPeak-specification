# mzPeak file index JSON

Describe the JSON format of the file index

**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `files` | `array` of [`file`](#file) | Yes | The files described in the index |
| `metadata` | `object` | Yes | &nbsp; |

## Property Details

**`files`** - `array` of [`file`](#file) *(required)*

The files described in the index

**`metadata`** - `object` *(required)*

---

## Definitions

### file
<a name="file"></a>

A single file in the mzPeak archive of a certain type

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `name` | `string` | Yes | The name of the file, relative to the root of the archive |
| `entity_type` | `string` | Yes | The things being described in one facet or another by this file |
| `data_kind` | `string` | Yes | The facet of the thing being described in this file |
| `column_mapping` | `array` of [`column_mapping`](#column_mapping) | &nbsp; | A list of Parquet column to controlled vocabulary term mappings |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | &nbsp; | A list of parameters describing the file stored in the mzPeak archive itself |

#### Property Details

**`name`** - `string` *(required)*

The name of the file, relative to the root of the archive

**`entity_type`** - `string` *(required)*

The things being described in one facet or another by this file

*Examples:* `"spectrum"`, `"chromatogram"`, `"other"`, `"proprietary"`, `"wavelength_spectrum"`

**`data_kind`** - `string` *(required)*

The facet of the thing being described in this file

*Examples:* `"data_arrays"`, `"metadata"`, `"peaks"`, `"other"`, `"proprietary"`

**`column_mapping`** - `array` of [`column_mapping`](#column_mapping) *(optional)*

A list of Parquet column to controlled vocabulary term mappings

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(optional)*

A list of parameters describing the file stored in the mzPeak archive itself

---

### column_mapping
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

---
