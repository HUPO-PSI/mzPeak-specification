# Auxiliary Data Arrays

When an array is present in an entry but is **not** encoded as a column in the
schema, it must be stored as an **auxiliary array**. This happens when mixing
different kinds of detectors in a single collection, and especially with
[diagnostic traces](../archive/entity-types.md), where every array might have a
different length along a shared time axis, or be sub-sampled.

Auxiliary data arrays have a schema similar to mzML's
[`binaryDataArray`](https://www.psidev.info/mzML), encoded in Parquet. They are
governed by the JSON Schema
[`schema/auxiliary_array.json`](https://github.com/HUPO-PSI/mzPeak-specification/blob/main/schema/auxiliary_array.json).

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
