# mzPeak metadata data processing method list

Describe the JSON format of data processing method list

**Type:** `array`
**Items:** [`data_processing_method`](#data_processing_method)

---

## Definitions

### data_processing_method
<a name="data_processing_method"></a>

Describes a single instrument configuration that was used. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#dataProcessingList>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | &nbsp; | A unique identifier for the data processing method. |
| `methods` | `array` of [`processing_method`](#processing_method) | &nbsp; | &nbsp; |

#### Property Details

**`id`** - `string` *(optional)*

A unique identifier for the data processing method.

**`methods`** - `array` of [`processing_method`](#processing_method) *(optional)*

---

### processing_method
<a name="processing_method"></a>

Describes a single step of data processing.

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `order` | `integer` | &nbsp; | The order in which the step is applied in the data processing pipeline. |
| `software_reference` | `string` | &nbsp; | The identifier for a software entry that performed this operation. |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | &nbsp; | Additional parameters describing this data processing step denoting actions, parameters, and other descriptors. |

#### Property Details

**`order`** - `integer` *(optional)*

The order in which the step is applied in the data processing pipeline.

**`software_reference`** - `string` *(optional)*

The identifier for a software entry that performed this operation.

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(optional)*

Additional parameters describing this data processing step denoting actions, parameters, and other descriptors.

---
