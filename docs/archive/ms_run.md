# mzPeak metadata MS run

Describe the JSON format of the run-level metadata section, analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#run>

## Use cases

The `run` object stores metadata describing the data acquisition process itself that does not live anywhere else, such as `start_time`
describing when the acquisition run physically started. Other parts of this object provide default context for the described data, such
as `default_data_processing_id` and `default_instrument_id`.

### Complete or partial runs

When storing a single instrument run, this object **SHOULD** be populated with as much information as possible. The more information that
can be passed on, the less information is lost when the data are accessed later. When storing a subset of a single run, all the relevant
metadata from the full run still applies. The `data_processing` entries **SHOULD** be updated to describe the subset-ing process itself.



**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `parameters` | `array` of [`param`](param.md) | &nbsp; | Parameters describing the run not otherwise covered by the attributes. |
| `id` | `string` | Yes | A unique identifier for the run |
| `default_data_processing_id` | `string` | Yes | The default data processing identifier, as drawn from [`data_processing_list`](../data_processing/) <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/data_processing.json> |
| `default_instrument_configuration_id` | `integer` | &nbsp; | The default instrument configuration, as drawn from [`instrument_configuration_list`](../instrument_configuration/) <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/instrument_configuration.json> |
| `default_source_file_id` | `string` | Yes | The default source file the content references, as drawn from [`file_description.source_files`](../file_description/) <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/file_description.json> |
| `start_time` | `string` or `null` | &nbsp; | The time that data acquistion started, encoded in an RFC 3339 format <<https://datatracker.ietf.org/doc/html/rfc3339>.> If UTC is not used, the local time offset **SHOULD** be defined. |

## Property Details

**`parameters`** - `array` of [`param`](param.md) *(optional)*

Parameters describing the run not otherwise covered by the attributes.

**`id`** - `string` *(required)*

A unique identifier for the run

**`default_data_processing_id`** - `string` *(required)*

The default data processing identifier, as drawn from [`data_processing_list`](../data_processing/) <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/data_processing.json>

**`default_instrument_configuration_id`** - `integer` *(optional)*

The default instrument configuration, as drawn from [`instrument_configuration_list`](../instrument_configuration/) <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/instrument_configuration.json>

**`default_source_file_id`** - `string` *(required)*

The default source file the content references, as drawn from [`file_description.source_files`](../file_description/) <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/file_description.json>

**`start_time`** - `string` or `null` *(optional)*

The time that data acquistion started, encoded in an RFC 3339 format <<https://datatracker.ietf.org/doc/html/rfc3339>.> If UTC is not used, the local time offset **SHOULD** be defined.

*Examples:* `"2005-07-20T19:44:22Z"`, `null`
