# mzPeak metadata MS run

Describe the JSON format of the run-level metadata section, analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#run>

## Use cases

The `run` object stores metadata describing the data acquisition process itself that does not live anywhere else, such as [`start_time`] describing when the acquisition run physically started. Other parts of this object provide default context for the described data, such as [`default_data_processing_id`] and [`default_instrument_id`].

### Complete or partial runs

When storing a single instrument run, this object **SHOULD** be populated with as much information as possible. The more information that can be passed on, the less information is lost when the data are accessed later. When storing a subset of a single run, all the relevant metadata from the full run still applies. A `data_processing` entry may be added to describe the subsetting process itself, but unless it alters the reported measures of the acquired data, that process need not be set as the `default_data_processing_id`

### Mixtures of runs

While mzPeak was designed as a single run format, it can, like mzML before it, be used to store spectra from disparate sources. In this case, the properties stored here are less useful.

!!! question "Sorting multiple peak list files"
    When storing spectra from many source files, like when converting from an [MGF](http://purl.obolibrary.org/obo/MS_1001062), spectra may not be time-ordered. Additionally, time no longer means the same thing between spectra anymore. This is not strictly part of mzPeak as a run file format anymore and isn't critical for core use cases. Should they be sorted at the expense of breaking the 1:1 mapping with the source file?

    **Yes**: The `time` index is useful for many kinds of queries and even if they aren't all from the same time sequence, we may filter records after we select them by time from the sorted index. MGF conversion *already* breaks the 1:1 mapping to the source file so re-breaking it is irrelevant. The index identifier usually a surrogate for the more detailed title line.

    **No**: There should be another mechanism to denote the time column is sorted or not, possibly a parameter added here! Breaking the 1:1 mapping would also produce misleading `nativeId`s, for instance [MS:1000774|multiple peak list nativeID format](http://purl.obolibrary.org/obo/MS_1000774) is with respect to their index in the MGF file. If we sort the file and break that index relationship, we break the semantics of that ID.


**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | &nbsp; | Parameters describing the run not otherwise covered by the attributes. |
| `id` | `string` | Yes | A unique identifier for the run |
| `default_data_processing_id` | `string` | Yes | The default data processing identifier, as drawn from <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/data_processing.json> |
| `default_instrument_id` | `integer` | Yes | The default instrument configuration, as drawn from <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/instrument_configuration.json> |
| `default_source_file_id` | `string` | Yes | The default source file the content references, as drawn from <https://raw.githubusercontent.com/HUPO-PSI/mzPeak-specification/refs/heads/main/schema/file_description.json> |
| `start_time` | `string` or `null` | &nbsp; | The time that data acquistion started, encoded in an RFC 3339 format (https://datatracker.ietf.org/doc/html/rfc3339) |

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

**`start_time`** - `string` or `null` *(optional)*

The time that data acquistion started, encoded in an RFC 3339 format (https://datatracker.ietf.org/doc/html/rfc3339)

*Examples:* `"2005-07-20T19:44:22Z"`, `null`
