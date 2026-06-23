## Use cases

The data processing section is meant to describe a data processing pipeline, assigning one or more [MS:1000452|data transformations](http://purl.obolibrary.org/obo/MS_1000452) actions to each step associated with a particular piece of software. Data processing pipelines may combine steps that do different things, which are only important in certain contexts.

```json
{
  "id": "pwiz_Reader_Thermo_conversion",
  "methods": [
    {
      "order": 0,
      "parameters": [
        {
          "accession": "MS:1000544",
          "name": "Conversion to mzML",
        },
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
        }
      ],
      "software_reference": "superSecretTool3214"
    }
  ]
}
```
