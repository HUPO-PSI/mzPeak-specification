## Use cases

The data processing section is meant to describe a data processing pipeline, assigning one or more [MS:1000452|data transformations](http://purl.obolibrary.org/obo/MS_1000452) actions to each step associated with a particular piece of software, with additional user-defined parameters if necessary. Data processing pipelines may combine steps that do different things, which are only important in certain contexts.


??? example "An example pipeline with two stages"
    ```json
    // A single data processing pipeline
    {
      "id": "pwiz_Reader_Thermo_conversion",
      "methods": [
        { // First `processing_method`
          "order": 0,
          "parameters": [
            {
              "accession": "MS:1000544",
              "name": "Conversion to mzML",
            },
          ],
          "software_reference": "pwiz"
        },
        { // Second `processing_method`
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
recalculation, but that is meaningless in the context of the m/z array.

File writers **SHOULD** take care to avoid introducing
contradictory steps like conflicting peak picking methods. If multiple configurations that the writer wants to distinguish between, the
writer **SHOULD** write multiple `data_processing_method` entries and reference them

## FAIR Data and Reproducibility

When publishing files that contain processed data, data transformations alone may not be enough to explain how the software used produced
the data published. Providing a [`MS:1001885|command-line parameters`](http://purl.obolibrary.org/obo/MS_1001885) parameter that embeds the
command line used may help future readers to understand how the software was instructed to operate. This is a compromise between creating a
parameter for each and every setting or argument that a piece of software took, which tells you semantically what was done in-so-far as the
software functionality can be defined by its inputs, but doesn't explain *how* it was told to do that. The command line tells the reader how
the software was invoked, and the same software and version with the same command line and input data should, if the software is reproducible,
be able to recreate the same output.
