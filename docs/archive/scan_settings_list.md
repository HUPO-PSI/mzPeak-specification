# mzPeak metadata scan settings list

Describe the JSON format of the scan settings list. Analogous to https://peptideatlas.org/tmp/mzML1.1.0.html#scanSettingsList.

**Type:** `array`
**Items:** [`scan_settings`](#scan_settings)

---

## Definitions

### scan_settings
<a name="scan_settings"></a>

Description of the acquisition settings of the instrument prior to the start of the run. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#scanSettings>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` |  | The unique identifier for this scan settings configuration |
| `source_file_references` | `array` of `string` |  |  |

#### Property Details

**`id`** - `string` *(optional)*

The unique identifier for this scan settings configuration

**`source_file_references`** - `array` of `string` *(optional)*

---
