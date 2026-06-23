# mzPeak metadata JSON parameter

Describe the JSON format of controlled vocabulary or user-defined parameters.

**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `name` | `string` | Yes | The name of the parameter. If controlled, this should be the name from the source controlled vocabulary. |
| `accession` | `string` or `null` | &nbsp; | The compact CURIE for the controlled vocabulary term, if it exists, null otherwise |
| `value` | `number` or `string` or `boolean` or `null` | &nbsp; | The value for this parameter, if any. This may be omitted if null |
| `unit` | `string` or `null` | &nbsp; | The compact CURIE for the unit describing the measurement for this parameter |

## Property Details

**`name`** - `string` *(required)*

The name of the parameter. If controlled, this should be the name from the source controlled vocabulary.

*Examples:* `"Q Exactive"`, `"SHA-1"`, `"MSn spectrum"`

**`accession`** - `string` or `null` *(optional)*

The compact CURIE for the controlled vocabulary term, if it exists, null otherwise

*Examples:* `"MS:1000580"`, `"MS:1000768"`

**`value`** - `number` or `string` or `boolean` or `null` *(optional)*

The value for this parameter, if any. This may be omitted if null

**`unit`** - `string` or `null` *(optional)*

The compact CURIE for the unit describing the measurement for this parameter
