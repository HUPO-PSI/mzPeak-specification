# mzPeak metadata instrument configurations

Describe the JSON format of instrument configurations used to acquire a mass spectrometry experiment

**Type:** `array`
**Items:** [`instrument_configuration`](#instrument_configuration)

---

## Definitions

### instrument_configuration
<a name="instrument_configuration"></a>

Describes a single instrument configuration that was used. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#instrumentConfiguration>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `components` | `array` of [`component_type`](#component_type) | Yes |  |
| `software_reference` | `string` | Yes | The identifier for a software that was associated with the data acquisition process. |
| `id` | `integer` | Yes | A unique identifier for this instrument configuration. |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Additional parameters describing this configuration, like the instrument model and serial number |

#### Property Details

**`components`** - `array` of [`component_type`](#component_type) *(required)*

**`software_reference`** - `string` *(required)*

The identifier for a software that was associated with the data acquisition process.

**`id`** - `integer` *(required)*

A unique identifier for this instrument configuration.

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Additional parameters describing this configuration, like the instrument model and serial number

---

### component_type
<a name="component_type"></a>

Describes an instrument component like the ion source, mass analyzer, or detector

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `component_type` | `enum` | Yes | The kind of component this is |
| `order` | `integer` | Yes | The order in which the analytes travels through the component |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Additional parameters describing this component, like the particular hardware type or components |

#### Property Details

**`component_type`** - `enum` *(required)*

The kind of component this is

*Allowed values:* `"ionsource"`, `"analyzer"`, `"detector"`

**`order`** - `integer` *(required)*

The order in which the analytes travels through the component

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Additional parameters describing this component, like the particular hardware type or components

---
