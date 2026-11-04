## Use cases

The `run` object stores metadata describing the data acquisition process itself that does not live anywhere else, such as `start_time`
describing when the acquisition run physically started. Other parts of this object provide default context for the described data, such
as `default_data_processing_id` and `default_instrument_id`.

### Complete or partial runs

When storing a single instrument run, this object **SHOULD** be populated with as much information as possible. The more information that
can be passed on, the less information is lost when the data are accessed later. When storing a subset of a single run, all the relevant
metadata from the full run still applies. The `data_processing` entries **SHOULD** be updated to describe the subset-ing process itself.

