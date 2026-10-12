<!-- Automatically generated from schema\mzpeak_index.json ->

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
| `parameters` | `array` of [`param`](param.md) | &nbsp; | A list of parameters describing the file stored in the mzPeak archive itself |
| `checksum` | `string` | Yes | The 128 byte SHA-512 hex digest of the entire file, excluding any ZIP-related headers or padding, rendered without byte separators and all alphabetic characters lowercase. |

#### Property Details

**`name`** - `string` *(required)*

The name of the file, relative to the root of the archive

**`entity_type`** - `string` *(required)*

The things being described in one facet or another by this file

*Examples:* `"spectrum"`, `"chromatogram"`, `"other"`, `"proprietary"`, `"wavelength_spectrum"`

**`data_kind`** - `string` *(required)*

The facet of the thing being described in this file

*Examples:* `"data_arrays"`, `"metadata"`, `"peaks"`, `"scans"`, `"precursors"`, `"selected_ions"`, `"products"`, `"other"`, `"proprietary"`

**`column_mapping`** - `array` of [`column_mapping`](#column_mapping) *(optional)*

A list of Parquet column to controlled vocabulary term mappings

**`parameters`** - `array` of [`param`](param.md) *(optional)*

A list of parameters describing the file stored in the mzPeak archive itself

**`checksum`** - `string` *(required)*

The 128 byte SHA-512 hex digest of the entire file, excluding any ZIP-related headers or padding, rendered without byte separators and all alphabetic characters lowercase.

*Examples:* `"b3350bbd8ff55e3aca1f3e3b0e20da79b8ffcf7a8a0de1dad09b51fc7ad6c01dcd6179e76d7dd06a1a6d7162edd3e2d0be790b2b9bb35b7bd4113952b7fe665d"`, `"44655c4a48320cb90ad366690857543e4882059730f6cc364d6500ff02c1b43b918364bbcae25d99c99c7b4366b0d184a7e2f50fea8632a0d44e90ccff03f46d"`, `"314da0d112ed0cb150b140af703951f5c8ca4a08725c0bcc7bd5b58e9031f707767c3035debb3284e4e53fc1a4fff7592be132bc55394e284132bf223be507c4"`

---

### column_mapping
<a name="column_mapping"></a>

A mapping from a Parquet column to a controlled vocabulary term

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `name` | `string` | Yes | The human-readable term name |
| `path` | `string` | Yes | The path in a Parquet schema for the mapped column delimited at nesting levels by '.', omitting [list, item|element] tokens |
| `accession` | `string` or `null` | &nbsp; | The CURIE for the controlled vocabulary term, or null if no controlled vocabulary term is available. Null may be used to indicate that a column has a human readable name but does not map to a controlled vocabulary term |
| `unit` | `string` or `null` | &nbsp; | &nbsp; |
| `term_marker` | `boolean` | &nbsp; | Whether this column is marks the presence/absence of a specific value-less controlled vocabulary term or subtree. When the column is a string, the value MUST be a CURIE for a child of this mapping's accession. When the column is boolean true when the term is present in the row, false or null otherwise. |

#### Property Details

**`name`** - `string` *(required)*

The human-readable term name

*Examples:* `"ms level"`, `"filter string"`, `"selected ion m/z"`, `"collision energy"`, `"scan window lower limit"`

**`path`** - `string` *(required)*

The path in a Parquet schema for the mapped column delimited at nesting levels by '.', omitting [list, item|element] tokens

*Examples:* `"ms_level"`, `"isolation_window.target_mz"`, `"activation.collision_energy"`, `"scan_window.scan_window_lower_limit"`

**`accession`** - `string` or `null` *(optional)*

The CURIE for the controlled vocabulary term, or null if no controlled vocabulary term is available. Null may be used to indicate that a column has a human readable name but does not map to a controlled vocabulary term

**`unit`** - `string` or `null` *(optional)*

**`term_marker`** - `boolean` *(optional)*

Whether this column is marks the presence/absence of a specific value-less controlled vocabulary term or subtree. When the column is a string, the value MUST be a CURIE for a child of this mapping's accession. When the column is boolean true when the term is present in the row, false or null otherwise.

---
