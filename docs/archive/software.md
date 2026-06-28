# mzPeak metadata software list

Describe the JSON format of software list

# software

Data acquisition, file conversion, and processing is all facilitated by software. The [software](#software)
list records the discrete software programs and versions used. The software list is a centralized list that
other components will reference members of by their *id* attribute.

A piece of software **MUST** be named using a parameter deriving from [`MS:1000531|software`](http://purl.obolibrary.org/obo/MS_1000531)
with software not included in the controlled vocabulary using [`MS:1000799|custom unreleased software tool`](http://purl.obolibrary.org/obo/MS_1000799)
with the custom software's name as the value.



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
| `id` | `string` | &nbsp; | A unique identifier for this software, even amongst different versions of the same software. |
| `version` | `string` | &nbsp; | The version of the software. |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | &nbsp; | Additional parameters describing this software, such as its controlled vocabulary identifier, or the term MS:1000799 for custom unreleased software to denote its name. |

#### Property Details

**`id`** - `string` *(optional)*

A unique identifier for this software, even amongst different versions of the same software.

**`version`** - `string` *(optional)*

The version of the software.

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(optional)*

Additional parameters describing this software, such as its controlled vocabulary identifier, or the term MS:1000799 for custom unreleased software to denote its name.

---
