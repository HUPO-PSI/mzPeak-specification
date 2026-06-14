# mzPeak metadata software list

Describe the JSON format of software list

**Type:** `array`
**Items:** [`software`](#software)

---

## Definitions

### software
<a name="software"></a>

A piece of software. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#software.>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` |  | A unique identifier for this software, even amongst different versions of the same software. |
| `version` | `string` |  | The version of the software. |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) |  | Additional parameters describing this software, such as its controlled vocabulary identifier, or the term MS:1000799 for custom unreleased software to denote its name. |

#### Property Details

**`id`** - `string` *(optional)*

A unique identifier for this software, even amongst different versions of the same software.

**`version`** - `string` *(optional)*

The version of the software.

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(optional)*

Additional parameters describing this software, such as its controlled vocabulary identifier, or the term MS:1000799 for custom unreleased software to denote its name.

---
