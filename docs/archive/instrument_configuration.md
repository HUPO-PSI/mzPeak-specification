# mzPeak metadata instrument configurations

Describe the JSON format of instrument configurations used to acquire a mass spectrometry experiment

## Use cases

This describes which components are engaged for a particular scan configuration. This includes the inlet and ion source which may be configured independently of the mass analyzer. This is also the place to note the [MS:1000031|instrument model](http://purl.obolibrary.org/obo/MS_1000031), [MS:1000529|serial number](http://purl.obolibrary.org/obo/MS_1000529) and any [MS:1000032|customization](http://purl.obolibrary.org/obo/MS_1000032) done to the hardware.

### Multiple configurations

When handling an instrument with multiple mass analyzers like an [MS:1003768|ion trap orbitrap instrument](http://purl.obolibrary.org/obo/MS_1003768), there **SHOULD** be multiple [`instrument_configuration`](#instrument_configuration) instances.

??? example
    ```json
    [
        {
        "components": [
        {
            "component_type": "ionsource",
            "order": 1,
            "parameters": [
            {
                "accession": "MS:1000073",
                "name": "electrospray ionization",
            },
            {
                "accession": "MS:1000057",
                "name": "electrospray inlet",
            }
            ]
        },
        {
            "component_type": "analyzer",
            "order": 2,
            "parameters": [
            {
                "accession": "MS:1000079",
                "name": "fourier transform ion cyclotron resonance mass spectrometer",
            }
            ]
        },
        {
            "component_type": "detector",
            "order": 3,
            "parameters": [
            {
                "accession": "MS:1000624",
                "name": "inductive detector",
            }
            ]
        }
        ],
        "id": 0,
        "parameters": [
        {
            "accession": "MS:1000448",
            "name": "LTQ FT",
        },
        {
            "accession": "MS:1000529",
            "name": "instrument serial number",
            "value": "SN06061F"
        }
        ],
        "software_reference": "Xcalibur"
        }
        {
        "components": [
            {
            "component_type": "ionsource",
            "order": 1,
            "parameters": [
                {
                "accession": "MS:1000073",
                "name": "electrospray ionization",
                },
                {
                "accession": "MS:1000057",
                "name": "electrospray inlet",
                }
            ]
            },
            {
            "component_type": "analyzer",
            "order": 2,
            "parameters": [
                {
                "accession": "MS:1000083",
                "name": "radial ejection linear ion trap",
                }
            ]
            },
            {
            "component_type": "detector",
            "order": 3,
            "parameters": [
                {
                "accession": "MS:1000253",
                "name": "electron multiplier",
                }
            ]
            }
        ],
        "id": 1,
        "parameters": [
            {
            "accession": "MS:1000448",
            "name": "LTQ FT",
            },
            {
            "accession": "MS:1000529",
            "name": "instrument serial number",
            "value": "SN06061F"
            }
        ],
        "software_reference": "Xcalibur"
        }
    ]
    ```

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
| `components` | `array` of [`component_type`](#component_type) | Yes | &nbsp; |
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
