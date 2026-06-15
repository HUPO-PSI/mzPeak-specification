# Auxiliary Data Arrays

When an array is present in an entry but is **not** encoded as a column in the
schema, it must be stored as an **auxiliary array**. This happens when mixing
different kinds of detectors in a single collection, and especially with
[diagnostic traces](../archive/entity-types.md), where every array might have a
different length along a shared time axis, or be sub-sampled.

Auxiliary data arrays have a schema similar to mzML's
[`binaryDataArray`](https://peptideatlas.org/tmp/mzML1.1.0.html#binaryDataArray), encoded in Parquet. They are
governed by the JSON Schema
[`schema/auxiliary_array.json`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/auxiliary_array.json).

??? info "Parquet Schema"
    ```text
    optional group auxiliary_arrays (List) {
      repeated group list {
        optional group item {
          optional group data (List) {
            repeated group list {
              required int32 item (Int(bitWidth=8, isSigned=false));
            }
          }
          optional group name {
            optional group value {
              optional int64   integer;
              optional double  float;
              optional binary  string (String);
              optional boolean boolean;
            }
            optional binary accession (String);
            optional binary name (String);
            optional binary unit (String);
          }
          optional binary data_type (String);
          optional binary compression (String);
          optional binary unit (String);
          optional group parameters (List) {
            repeated group list {
              optional group item {
                optional group value {
                  optional int64   integer;
                  optional double  float;
                  optional binary  string (String);
                  optional boolean boolean;
                }
                optional binary accession (String);
                optional binary name (String);
                optional binary unit (String);
              }
            }
          }
          optional binary data_processing_ref (String);
        }
      }
    }
    ```

!!! warning "Auxiliary arrays cannot be sliced"
    Because an auxiliary array is stored as an opaque encoded buffer rather than
    a first-class column, it **cannot** be searched or sliced without decoding
    the whole array — exactly as in mzML. The associated metadata row records the
    count in `number_of_auxiliary_arrays`, so a reader can cheaply decide whether
    the more expensive decoding step is worthwhile before attempting it.

## Data Type and Storage
Auxiliary arrays' data **MUST** stored as raw byte arrays in *little endian* order.
The data type for the data stored **MUST** be written in the `data_type` field of
the auxiliary array structure referencing a child term of [MS:1000518|binary data type](http://purl.obolibrary.org/obo/MS_1000518) such as [MS:1000523|64-bit float](http://purl.obolibrary.org/obo/MS_1000523) or [MS:1000519|32-bit integer](http://purl.obolibrary.org/obo/MS_1000519).


## Compression
Auxiliary arrays' data are stored as raw byte arrays, with no data type-specific transformations
to make them more compressable, but they receive the blanket compression codec and level that the
entire Parquet file receives. Their `compression` field **SHOULD** be [`MS:1000576|no compression`](http://purl.obolibrary.org/obo/MS_1000576) for no additional compression.
If you wish to apply a specific compression algorithm to the data of a single entry *before* it
is compressed by Parquet, set the `compression` field for that entry to the appropriate controlled
vocabulary term descending from [`MS:1000572|binary compression type`](http://purl.obolibrary.org/obo/MS_1000572)
and store the compressed bytes in the `data` column.