# mzPeak metadata data processing method list

Describe the JSON format of data processing method list

## Use cases

The data processing section is meant to describe a data processing pipeline, assigning one or more [MS:1000452|data transformations](http://purl.obolibrary.org/obo/MS_1000452) actions to each step associated with a particular piece of software, with additional user-defined parameters if necessary. Data processing pipelines may combine steps that do different things, which are only important in certain contexts.

??? example "An example pipeline with two stages"
    ```json
    {
      "id": "pwiz_Reader_Thermo_conversion",
      "methods": [
        {
          "order": 0,
          "parameters": [
            {
              "accession": "MS:1000544",
              "name": "Conversion to mzML"
            }
          ],
          "software_reference": "pwiz"
        },
        {
          "order": 1,
          "parameters": [
            {
              "accession": "MS:1000035",
              "name": "peak picking",
            },
            {
              "accession": "MS:1000593",
              "name": "baseline reduction",
            },
            {
              "accession": "MS:1000780",
              "name": "precursor recalculation"
            }
          ],
          "software_reference": "superSecretTool3214"
        }
      ]
    }
    ```

The pipeline above converted some Thermo data to mzML with ProteoWizard, and then another tool (imaginary) performs some transformation
of the signal data and recalculates the precursor ion m/z. When referenced in another context, the caller is responsible for reasoning
about which components of the processing steps are relevant to that context. For instance, this same data processing pipeline does precursor
recalculation, but that is meaningless in the context of the m/z array. Data processing scopes do not cascade, only one `data_processing_method`
is applicable at a time to avoid stacking contradictory operations.

File writers **SHOULD** take care to avoid introducing contradictory steps like conflicting peak picking methods. If multiple configurations
that the writer wants to distinguish between, the writer **SHOULD** write multiple `data_processing_method` entries and reference them. If
processing derived data, writers **SHOULD** append new steps to the source data's existing data processing methods to reflect the full chain
of operations, not create a separate `data_processing_method` describing only the new steps.

## FAIR Data and Reproducibility

When publishing files that contain processed data, data transformations alone may not be enough to explain how the software used produced
the data published. Providing a [`MS:1001885|command-line parameters`](http://purl.obolibrary.org/obo/MS_1001885) parameter that embeds the
command line used may help future readers to understand how the software was instructed to operate. This is a compromise between creating a
parameter for each and every setting or argument that a piece of software took, which tells you semantically what was done in-so-far as the
software functionality can be defined by its inputs, but doesn't explain *how* it was told to do that. The command line tells the reader how
the software was invoked, and the same software and version with the same command line and input data should, if the software is reproducible,
be able to recreate the same output.

## Precedence and Scope

Data processing pipelines can be modular and complex. Describing all of the details of each step is difficult. Like mzML, mzPeak attempts
to describe high level configurations, covering broad classes of data transformations applied in sequence, and then provides tools for marking
which scopes they apply to.

<figure class="mzp-figure" markdown>
<img src="../../assets/img/data-processing-resolution-order.svg" alt="The precedence of the data processing methods applied to the scopes." height="520"/>
</figure>

The data processing resolution order shown in the figure above demonstrates the process where each scope falls back to a higher level description.
A data array may be processed in a specific way that is distinct from how the rest of its source entity was processed, such as when describing
centroid and profile data processed with different software. A single spectrum might be processed differently than another, such as when applying
one transformation to data from one mass analyzer and a different transformation to data acquired on another mass analyzer in hybrid instruments.


**Type:** `array`
**Items:** [`data_processing_method`](#data_processing_method)

---

## Definitions

### data_processing_method
<a name="data_processing_method"></a>

Describes a single pipeline of data processing pipeline that was used on an entity or data array. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#dataProcessingList>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | &nbsp; | A unique identifier for the data processing method. |
| `methods` | `array` of [`processing_method`](#processing_method) | &nbsp; | &nbsp; |

#### Property Details

**`id`** - `string` *(optional)*

A unique identifier for the data processing method.

**`methods`** - `array` of [`processing_method`](#processing_method) *(optional)*

---

### processing_method
<a name="processing_method"></a>

Describes a single step of data processing.

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `order` | `integer` | &nbsp; | The order in which the step is applied in the data processing pipeline. Values **MUST** be ascending, and **SHOULD** be contiguous. |
| `software_reference` | `string` | &nbsp; | The identifier for a software entry that performed this operation. This **MUST** be a software_list[].id in the software list of the mzPeak archive. |
| `parameters` | `array` of [`param`](param.md) | &nbsp; | Additional parameters describing this data processing step denoting actions, parameters, and other descriptors. |

#### Property Details

**`order`** - `integer` *(optional)*

The order in which the step is applied in the data processing pipeline. Values **MUST** be ascending, and **SHOULD** be contiguous.

**`software_reference`** - `string` *(optional)*

The identifier for a software entry that performed this operation. This **MUST** be a software_list[].id in the software list of the mzPeak archive.

**`parameters`** - `array` of [`param`](param.md) *(optional)*

Additional parameters describing this data processing step denoting actions, parameters, and other descriptors.

---
