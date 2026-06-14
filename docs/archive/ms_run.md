# mzPeak metadata MS run

Describe the JSON format of the run-level metadata section, analogous to https://peptideatlas.org/tmp/mzML1.1.0.html#run

**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) |  | Parameters describing the run not otherwise covered by the attributes. |
| `id` | `string` | Yes | A unique identifier for the run |
| `default_data_processing_id` | `string` | Yes | The default data processing identifier, as drawn from https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/data_processing.json |
| `default_instrument_id` | `integer` | Yes | The default instrument configuration, as drawn from https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/instrument_configuration.json |
| `default_source_file_id` | `string` | Yes | The default source file the content references, as drawn from https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/file_description.json |
| `start_time` | `string` | `null` |  | The time that data acquistion started, encoded in an RFC 3339 format (https://datatracker.ietf.org/doc/html/rfc3339) |

## Property Details

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(optional)*

Parameters describing the run not otherwise covered by the attributes.

**`id`** - `string` *(required)*

A unique identifier for the run

**`default_data_processing_id`** - `string` *(required)*

The default data processing identifier, as drawn from <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/data_processing.json>

**`default_instrument_id`** - `integer` *(required)*

The default instrument configuration, as drawn from <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/instrument_configuration.json>

**`default_source_file_id`** - `string` *(required)*

The default source file the content references, as drawn from <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/file_description.json>

**`start_time`** - `string` | `null` *(optional)*

The time that data acquistion started, encoded in an RFC 3339 format (<https://datatracker.ietf.org/doc/html/rfc3339)>

*Examples:* `"2005-07-20T19:44:22Z"`
