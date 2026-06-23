# mzPeak controlled vocabulary list

Describe the JSON format of the controlled vocabulary list, analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#cvList>

**Type:** `array`
**Items:** [`cv`](#cv)

---

## Definitions

### cv
<a name="cv"></a>

Describe the JSON format of a controlled vocabulary, analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#cv>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | Yes | The short identifier used for CURIEs from this controlled vocabulary. |
| `version` | `string` | Yes | The version for this controlled vocabulary, like a release number, date, or similar. No particular format is expected. |
| `full_name` | `string` | &nbsp; | The usual name for the resource (e.g. The PSI-MS Controlled Vocabulary). |
| `uri` | `string` | Yes | The URI for the controlled vocabulary. |

#### Property Details

**`id`** - `string` *(required)*

The short identifier used for CURIEs from this controlled vocabulary.

*Examples:* `"MS"`, `"UO"`, `"NCIT"`, `"EFO"`

**`version`** - `string` *(required)*

The version for this controlled vocabulary, like a release number, date, or similar. No particular format is expected.

**`full_name`** - `string` *(optional)*

The usual name for the resource (e.g. The PSI-MS Controlled Vocabulary).

**`uri`** - `string` *(required)*

The URI for the controlled vocabulary.

---
