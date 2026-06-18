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
| `id` | `string` | Yes | The unique identifier for this scan settings configuration |
| `source_file_references` | `array` of `string` |  |  |
| `targets` | `array` of [`target`](#target) |  | A list of targeted ions or intervals on an inclusion list. |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Additional parameters describing the scan settings. |

#### Property Details

**`id`** - `string` *(required)*

The unique identifier for this scan settings configuration

**`source_file_references`** - `array` of `string` *(optional)*

**`targets`** - `array` of [`target`](#target) *(optional)*

A list of targeted ions or intervals on an inclusion list.

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Additional parameters describing the scan settings.

---

### target
<a name="target"></a>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Additional parameters describing this target |

#### Property Details

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Additional parameters describing this target

---
