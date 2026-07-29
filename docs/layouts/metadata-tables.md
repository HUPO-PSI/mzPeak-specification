# Metadata Tables

Mass spectra and other entities described in `mzPeak` are complex, multi-faceted entities.
Each facet is described by a `data_kind` associated with the `entity_type`. The columns of
a metadata table can vary widely based upon context, but they have the following rules:

For `data_kind == metadata`:
- The first column **MUST** be named `index` and be an integer value that **MUST** be unique. It **SHOULD** also be
  sorted. This is akin to a primary key in relational databases.

For all other kinds:
- The first column **MUST** be `source_index` and be an integer value that *references* the `index` of
  the `metadata` table for the instance that this row is associated. There may be zero or more rows
  with the same `source_index` value. This is akin to a foreign key in relational databases.
- There **MAY** be another column or a set of columns that function as a primary or composite primary key.
  This will be defined by the particular file's schema.

In addition, all `data_kind` must support the following:
- There **MAY** be a `parameters` column that is a list column as described [below](#the-parameters-list) in
  the [Controlled Vocabulary Terms](#controlled-vocabulary-terms) section. If there are nested columns, each
  `struct`-like group may have its own `parameters` column.
- Additional columns described in the [index file](../archive/index-file.md)'s column mapping may be present
  that map a controlled vocabulary term to a column as described in [Controlled Vocabulary Terms](#controlled-vocabulary-terms) section.
- Additional columns may be defined specifically for a combination of `entity_type` and `data_kind`.
- If a column value is `null`, treat its value as absent from that row. The `index` or `source_index` columns' values **MUST** not be `null`.

## Column naming

When a column is not otherwise controlled by the schema, it is assumed to map to a parameter. The schemas that follow metadata tables
in this document will use specific names associated with CURIEs. These are the *canonical* names for those parameters, and writers **SHOULD**
use them and readers **SHOULD** expect them. While the correct meaning can always be recovered by using the [column mapping](#column-mapping)
process described below, some readers may be treating mzPeak component files like generic Parquet files, and will expect a stable, consistent
schema.

## Examples

### Example 1: `entity_type=spectrum` `data_kind=metadata`

This is the primary metadata table for mass spectra. There is an `index` column that uniquely identifies rows.

|   **index** | id                                         |   ms_level |       time |   scan_polarity | spectrum_representation   | spectrum_type   |   lowest_observed_mz |   highest_observed_mz |   number_of_data_points |   number_of_peaks |   base_peak_mz |   base_peak_intensity |   total_ion_current | data_processing_id   | parameters   | auxiliary_arrays   |   number_of_auxiliary_arrays | mz_delta_model                                    |
|--------:|:-------------------------------------------|-----------:|-----------:|----------------:|:--------------------------|:----------------|---------------------:|----------------------:|------------------------:|------------------:|---------------:|----------------------:|--------------------:|:---------------------|:-------------|:-------------------|-----------------------------:|:--------------------------------------------------|
|       0 | controllerType=0 controllerNumber=1 scan=1 |          1 | 0.004935   |               1 | MS:1000128                | MS:1000579      |              200     |               1999.99 |                   13589 |               null |        810.415 |           1.47122e+06 |         7.12632e+07 |                      | []           | []                 |                            0 | [-2.21139275e-08  9.69754604e-11  6.05422863e-09] |
|       1 | controllerType=0 controllerNumber=1 scan=2 |          1 | 0.00789667 |               1 | MS:1000128                | MS:1000579      |              200.091 |               2000    |                   18177 |               null |        810.545 |      183839           |         1.29013e+07 |                      | []           | []                 |                            0 | [0.09090909]                                      |
|       2 | controllerType=0 controllerNumber=1 scan=3 |          2 | 0.0112183  |               1 | MS:1000127                | MS:1000580      |              231.389 |               1560.72 |                     null |               485 |        736.637 |      161141           |    586279           |                      | []           | []                 |                            0 |                                                   |
|       3 | controllerType=0 controllerNumber=1 scan=4 |          2 | 0.0228383  |               1 | MS:1000127                | MS:1000580      |              236.047 |               1636.43 |                     null |              1006 |        780.536 |       29161.9         |    441570           |                      | []           | []                 |                            0 |                                                   |
|       4 | controllerType=0 controllerNumber=1 scan=5 |          2 | 0.034925   |               1 | MS:1000127                | MS:1000580      |              203.222 |               1412.57 |                     null |               837 |        578.986 |        8601.8         |    114332           |                      | []           | []                 |                            0 |                                                   |

### Example 2: `entity_type=spectrum` `data_kind=selected_ion`

This is a secondary metadata file, it has `source_index` column. This identifies the `index` value of the `spectrum` row in the table above in [Example 1](#example-1-entity_typespectrum-data_kindmetadata). It has a second key, `precursor_index` denoting the index of the precursor spectrum that the selected ion was isolated in. When there is only one selected ion per spectrum, this will look unique, but this isn't guaranteed!

|   source_index |   precursor_index |   selected_ion_mz |   charge_state |        intensity |   ion_mobility_value | ion_mobility_type   | parameters   |
|---------------:|------------------:|------------------:|---------------:|-----------------:|---------------------:|:--------------------|:-------------|
|              2 |                 1 |           810.789 |            null |      1.99404e+06 |                  null |                     | []           |
|              3 |                 1 |           837.345 |            null | 999937           |                  null |                     | []           |
|              4 |                 1 |           725.362 |            null | 313667           |                  null |                     | []           |
|              5 |                 1 |           558.869 |            null | 202178           |                  null |                     | []           |
|              6 |                 1 |           812.325 |            null |      1.16189e+06 |                  null |                     | []           |

## Controlled Vocabulary Terms

Like mzML, mzPeak makes heavy use of controlled vocabularies to represent rich
metadata. mzPeak uses CV terms in three ways:

1. **As columns.** When a term is used as a column name, that column's values are
   either the defined value of the term's expected type (e.g. via
   `has_value_type`) *or* a CURIE for a child of the column-name term. For
   example:
    - The column [`spectrum_representation (MS:1000525)`](http://purl.obolibrary.org/obo/MS_1000525)
      holds CURIEs for a child term —
      [`MS:1000127`](http://purl.obolibrary.org/obo/MS_1000127) "centroid
      spectrum" or [`MS:1000128`](http://purl.obolibrary.org/obo/MS_1000128)
      "profile spectrum" — as appropriate for the spectrum in that row.
    - The column [`ms_level (MS:1000511)`](http://purl.obolibrary.org/obo/MS_1000511)
      holds an integer value.
2. **As structural elements.** In several places — such as the
   [array index](signal-data.md#the-array-index) — CURIEs reference named
   concepts that explain the semantics of a data structure without changing its
   shape.
3. **As pluggable metadata carriers** in `parameters` arrays, analogous to
   `<cvParam/>` in mzML. Every schema facet of a metadata table may carry a
   `parameters` column.

### The `parameters` list

The `parameters` column may be present in any `struct`-like group of a metadata table. It
**MUST** be a list of the following schema:

```
optional group field_id=-1 parameters (List) {
  repeated group field_id=-1 list {
    optional group field_id=-1 item {
      optional group field_id=-1 value {
        optional int64   field_id=-1 integer;
        optional double  field_id=-1 float;
        optional binary  field_id=-1 string (String);
        optional boolean field_id=-1 boolean;
      }
      optional binary field_id=-1 accession (String);
      optional binary field_id=-1 name (String);
      optional binary field_id=-1 unit (String);
    }
  }
}
```

The `parameters.list.item.value` group has a slot for each data type, so a
parameter can take exactly one of these value types; unused slots **MUST** be
`null`. A parameter **MAY** carry a unit, given as a CV-term CURIE in
`parameters.list.item.unit`. As with mzML's `<userParam/>`, an *uncontrolled*
parameter may be stored simply by leaving `parameters.list.item.accession` empty.

!!! note "Naming and column promotion"
    - Parquet columns **MUST** be uniquely named, so if a parameter appears more
      than once in a single row it **MUST** be stored in the `parameters`
      column.
    - Writers **SHOULD** to promote parameters that are present with zero or one times per row
      to *columns* unless there is ambiguity or insufficient context. This is more space-efficient and enables predicate filtering. Examples where ambiguity might prevent promotion:
        - The parameter *MAY* be repeated, but until all records are written, it is impossible to know.
        - The parameter is a user-defined term, leaving it up to the implementation to know whether it may be repeated multiple times for the same row.
        - The parameter's value type varies from case to case (e.g. sometimes a number, sometimes a string)

!!! question "Open item - auxiliary data arrays"
    Whether `auxiliary_data_array` are subjecto to parameter-to-column promotion if they are recurring.
    Technically they are under the current wording, but they are already a special case escape hatch and
    complicated enough to parse.

!!! question "Open item — lists and maps"
    Whether `parameters` values should also support list- or map-valued types is
    still under discussion.

### Typing parameter values

When a term has a value and it is stored in the `parameters` list, the value
**MUST** use one of the value types in the fixed schema above. When a term is
instead promoted to its own column, the value may use any Parquet data type.
This flexibility lets writers pick an appropriate size and precision, but it can
create redundant reader code — a column expected to hold an integer might be
written as an 8-, 16-, 32-, or 64-bit integer, signed or unsigned. Some
languages handle this naturally with dynamic typing or generics; others need a
separate implementation per physical type.

Recommended physical types:

- **Integral values that are *not* indices or identifiers** — prefer signed 32-
  or 64-bit, as needed to cover the value's domain.
- **Indices or identifiers represented as integers** — prefer unsigned 32- or
  64-bit. Dictionary encoding reduces most cases to ~8 bits per variant on disk
  anyway.
- **Floating-point values** — prefer 64-bit doubles unless precision is truly of
  no concern. For repetitive values (e.g. collision energy), dictionary encoding
  drops the on-disk cost well below 32 bits per value.
- **Strings and lists** — prefer 64-bit offsets ("large strings"/"large lists"),
  but write code that supports both 32- and 64-bit offsets. This matters
  especially for strings, where the offset is a *byte* offset, not an item
  offset.

### Column Mapping

When a CV-term concept is represented as a column, the column name **SHOULD** unless otherwise
stated be named according to the following rules and have a corresponding entry in the file's
[file index](../archive/index-file.md)'s column mappings.

1. If defined by the schema, match the *expected* name, often derived from the CV-term's name.
2. Otherwise, begin with the prefix `opt_` followed by a unique name that is descriptive of the value being stored.
     1. If the value is a CV-term, the term's name with non-identifier-safe characters (`/[^a-zA-Z0-9_\\-]+/`) replaced
      with `_`
     2. If not, provide as succinct unique name in the column name after the `opt_` prefix, with a more complete name defined
        in the column mapping.

#### Traversing a column mapping instruction

Column mappings' `.path` attribute tells the reader where to find the column corresponding to the parameter.
As described in the [index documentation](../archive/index-file.md#column-mapping), the path skips over the
layers of the file schema denoting lists and elements. For top-level objects, this is the column name itself.

```json
{
  "name": "preset scan configuration",
  "path": "preset_scan_configuration",
  "accession": "MS:1000616"
},
{
  "name": "scan window lower limit",
  "path": "scan_windows.scan_window_lower_limit",
  "accession": "MS:1000501",
  "unit": "MS:1000040"
}
```

```
required group scan_schema {
  optional int64 source_index (Int(bitWidth=64, isSigned=false));
  optional int64 scan_index (Int(bitWidth=64, isSigned=false));
  optional float scan_start_time;
  optional int32 preset_scan_configuration (Int(bitWidth=32, isSigned=false)); <<< first mapping, `preset_scan_configuration`
  optional binary filter_string (String);
  optional float ion_injection_time;
  optional double ion_mobility_value;
  optional binary ion_mobility_type (String);
  optional int32 instrument_configuration_id (Int(bitWidth=32, isSigned=false));
  optional binary spectrum_reference (String);
  ...
  optional group scan_windows (List) {
    repeated group list {
      optional group item {
        optional float scan_window_lower_limit; <<< second mapping, `scan_windows.scan_window_lower_limit` skips the `list.item` tokens.
        optional float scan_window_upper_limit;
      }
    }
  }
}
```

##### Example 3: `entity_type=spectrum` `data_kind=scans`

|   source_index |   scan_index |   scan_start_time | *preset_scan_ configuration* <<< | filter_string                                        |   ion_injection_ time |   instrument_ configuration_id | scan_windows |
|---------------:|-------------:|------------------:|------------------------------:|:-------------------------------------------------------|---------------------:|------------------------------:| --------:|
|              0 |            0 |        0.004935   |                           1 | FTMS + p ESI Full ms [200.00-2000.00]                    |             68.2275  |                             0 | [{**scan_lower_limit <<<** : 200, scan_upper_limit: 2000}]
|              1 |            1 |        0.00789667 |                           2 | ITMS + p ESI Full ms [200.00-2000.00]                    |              2.07659 |                             1 | [{**scan_lower_limit**: 200, scan_upper_limit: 2000}]
|              2 |            2 |        0.0112183  |                           3 | ITMS + c ESI d Full ms2 810.79@cid35.00 [210.00-1635.00] |              7.99301 |                             1 | [{**scan_lower_limit**: 200, scan_upper_limit: 2000}]
|              3 |            3 |        0.0228383  |                           4 | ITMS + c ESI d Full ms2 837.34@cid35.00 [220.00-1685.00] |             15.5505  |                             1 | [{**scan_lower_limit**: 200, scan_upper_limit: 2000}]

In the first case, [preset scan configuration (MS:1000616)](https://ontobee.org/ontology/MS?iri=http://purl.obolibrary.org/obo/MS_1000616) maps to `preset_scan_configuration`. The second is more complex as it maps [scan lower limit (MS:1000501)](https://ontobee.org/ontology/MS?iri=http://purl.obolibrary.org/obo/MS_1000501) to a column nested under of the `scan_windows` list. This arrangement encourages readers to use some form of tree traversal approach.
