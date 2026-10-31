# mzPeak controlled vocabulary list

Describe the JSON format of the controlled vocabulary list, analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#cvList>

**Type:** `array`
**Items:** [`cv`](#cv)

---

## Definitions

### cv
<a name="cv"></a>

Describe the JSON format of a controlled vocabulary, analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#cv.>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | Yes | The short identifier used for this controlled vocabulary. This **SHOULD** also the primary namespace identifier from CURIEs defined in these controlled vocabularies, though there may be others. |
| `version` | `string` | Yes | The version for this controlled vocabulary, like a release number, date, or similar. The format of the version is controlled by the controlled vocabulary. |
| `full_name` | `string` | &nbsp; | The declared name for the resource (e.g. The PSI-MS Controlled Vocabulary). |
| `uri` | `string` | Yes | The URI for the controlled vocabulary. The URI **SHOULD** refer a fixed version of controlled vocabulary. |

#### Property Details

**`id`** - `string` *(required)*

The short identifier used for this controlled vocabulary. This **SHOULD** also the primary namespace identifier from CURIEs defined in these controlled vocabularies, though there may be others.

*Examples:* `"MS"`, `"UO"`, `"NCIT"`, `"EFO"`, `"IMS"`, `"PATO"`

**`version`** - `string` *(required)*

The version for this controlled vocabulary, like a release number, date, or similar. The format of the version is controlled by the controlled vocabulary.

**`full_name`** - `string` *(optional)*

The declared name for the resource (e.g. The PSI-MS Controlled Vocabulary).

**`uri`** - `string` *(required)*

The URI for the controlled vocabulary. The URI **SHOULD** refer a fixed version of controlled vocabulary.

*Examples:* `"http://purl.obolibrary.org/obo/ms/releases/4.2.12/psi-ms.obo"`, `"http://purl.obolibrary.org/obo/ms/releases/4.1.186/psi-ms.obo"`, `"http://purl.obolibrary.org/obo/uo/releases/2026-10-12/uo.obo"`

---
