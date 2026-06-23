# mzPeak metadata sample list

Describe the JSON format of the sample list. Multiple samples can be present in a single run in scenarios like multiplexing or pooling.

**Type:** `array`
**Items:** [`sample`](#sample)

---

## Definitions

### sample
<a name="sample"></a>

A description (one) of the samples used to generate this dataset. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#sample.>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | Yes | A unique identifier for this sample. |
| `name` | `string` | &nbsp; | A human-readable name for this sample that might be easier to recognize. |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Additional parameters describing this sample. |

#### Property Details

**`id`** - `string` *(required)*

A unique identifier for this sample.

**`name`** - `string` *(optional)*

A human-readable name for this sample that might be easier to recognize.

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Additional parameters describing this sample.

---
