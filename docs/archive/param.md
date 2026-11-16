# mzPeak metadata JSON parameter

The JSON format of controlled vocabulary or user-defined parameters.

## Controlled and custom metadata values.

The controlled vocabulary/ontology (CVs) parameter or `cvParam` is the foundation of mzPeak's flexible metadata model. Like [mzML](https://www.psidev.info/mzml),
mzPeak uses parameters to add metadata to an entity in an extensible way. The controlled vocabularies define semantics for a set of common terms
used for parameters with `accession` tied back to the CV, but if a suitable term does not exist a user is free to add arbitrary parameters without
an accession. mzML used a separate `userParam` element to signal that a parameter was uncontrolled, but mzPeak simply assumes that a parameter is
uncontrolled if its `accession` attribute is `null`.

Parameters attached to a CV will have an `accession`, a human readable name, and may be related to other terms through the hierarchical definition.
These relationships may constrain its acceptable value types, which units it may be associated with, and the contexts it is appropriate in. Readers
[SHOULD]{class="should-chip"} prefer to refer to controlled parameters by their stable `accession`, not their `name` which is not guaranteed to remain the same over time.

A parameter may be used in three contexts in mzPeak. One is in the JSON metadata, where this JSON schema is most appropriate. The other two are in
Parquet tables as either columns, or as a member of the `parameters` list of structs, which are both described in greater detail in the
[metadata table layout](../layouts/metadata-tables.md).


**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `name` | `string` | Yes | The name of the parameter. If controlled, this should be the name from the source controlled vocabulary. |
| `accession` | `string` or `null` | No | The compact CURIE for the controlled vocabulary term, if it exists, null otherwise |
| `value` | `number` or `integer` or `string` or `boolean` or `null` or `array` | No | The value for this parameter, if any. This may be omitted if null |
| `unit` | `string` or `null` | No | The compact CURIE for the unit describing the measurement for this parameter |

## Property Details

**`name`** - `string` *(required)*

The name of the parameter. If controlled, this should be the name from the source controlled vocabulary.

*Examples:* `"Q Exactive"`, `"SHA-1"`, `"MSn spectrum"`

**`accession`** - `string` or `null` *(optional)*

The compact CURIE for the controlled vocabulary term, if it exists, null otherwise

*Examples:* `"MS:1000580"`, `"MS:1000768"`

**`value`** - `number` or `integer` or `string` or `boolean` or `null` or `array` *(optional)*

The value for this parameter, if any. This may be omitted if null

**`unit`** - `string` or `null` *(optional)*

The compact CURIE for the unit describing the measurement for this parameter
