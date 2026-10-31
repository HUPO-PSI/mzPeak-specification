# mzPeak metadata sample list

Describe the JSON format of the sample list. Multiple samples can be present in a single run in scenarios like multiplexing or pooling.

## Describing individual samples

When the sample or samples included in the MS run are described in the data file itself, it makes tracing what a data file
was for, and possibly which study it came from. This makes it possible for laboratory information management systems (LIMS)
to more effectively index files and for repositories to be able to supply more detailed information when searching for a
dataset. This also ensures that these details move *with* the raw data and do not get scattered between lab notebooks,
spread sheets, or unrecorded calculations that generally do not follow the MS data beyond the person doing the data
acquisition or analysis.

Common properties to record:

- [`MS:1000001|sample number`](http://purl.obolibrary.org/obo/MS_1000001)
- [`MS:1000004|sample mass`](http://purl.obolibrary.org/obo/MS_1000004)
- [`MS:1000005|sample volume`](http://purl.obolibrary.org/obo/MS_1000005)
- [`MS:1000006|sample concentration`](http://purl.obolibrary.org/obo/MS_1000006)
- [`MS:1000053|sample batch`](http://purl.obolibrary.org/obo/MS_1000053)
- Children of [`MS:1000003|sample state`](http://purl.obolibrary.org/obo/MS_1000003)

The [`MS:1000002|sample name`](http://purl.obolibrary.org/obo/MS_1000002) is structurally encoded in the JSON `sample.name` property.

It is also useful to record if a sample was labeled/tagged (a child of [`MS:1002602|sample label`](http://purl.obolibrary.org/obo/MS_1002602)) or not ([`MS:1002038|label free sample`](http://purl.obolibrary.org/obo/MS_1002038)), and if so, what the associated channel was.

Additionally, if the [Experimental Factor Ontology (EFO)](https://www.ebi.ac.uk/ols4/ontologies/efo) is used, a wide
range of properties like taxonomy, tissue type, and more are defined. This overlaps with SDRF as described below.

### Relationship with SDRF

A [Sample and Data Relationship Format (SDRF)](https://www.psidev.info/sdrf-sample-data-relationship-format) file may
be embedded in directly in an mzPeak archive as a file. This allows the entire experimental design, as defined by the
data producer or in-so-far as was known at the time the data were deposited. Embedding the complete file provides the
reader with broader context on the experimental design and relationship with other data files. This makes the dataset
discoverable, and may maintain FAIR linkage when the file is downloaded in isolation.

When an embedded SDRF file is used, the writer **SHOULD** attempt to match sample names for cross-referencing. When
feasible, it should also be possible to extract sample characteristics and and factor values from the SDRF to populate
the `sample.parameters`.


**Type:** `array`
**Items:** [`sample`](#sample)

---

## Definitions

### sample
<a name="sample"></a>

A description (one) of the samples used to generate this dataset. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#sample.>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | Yes | A unique identifier for this sample. |
| `name` | `string` | &nbsp; | A human-readable name for this sample that might be easier to recognize. |
| `parameters` | `array` of [`param`](param.md) | Yes | Additional parameters describing this sample. |

#### Property Details

**`id`** - `string` *(required)*

A unique identifier for this sample.

**`name`** - `string` *(optional)*

A human-readable name for this sample that might be easier to recognize.

**`parameters`** - `array` of [`param`](param.md) *(required)*

Additional parameters describing this sample.

---
