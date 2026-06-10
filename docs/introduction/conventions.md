# Notational Conventions

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Throughout the specification, controlled-vocabulary terms are written as CURIEs
of the form `MS:1000511` and, where helpful, linked to their definition in the
[PSI-MS controlled vocabulary](https://www.ebi.ac.uk/ols4/ontologies/ms). When a
term name is *inflected* into a Parquet column name, it appears in `code` font,
e.g. `MS_1000511_ms_level` — see
[Column Name Inflection](../layouts/metadata-tables.md#column-name-inflection).

## Code samples

This document describes both a file format and a set of suggested algorithms for
preparing data to be stored in that format. The original author (Joshua Klein)
includes snippets of Python code to illustrate these operations, under the
assumption that most technical programmers will be able to read Python and that
Python is effectively executable pseudocode.

The snippets rely on three components:

- **abstract base classes** from the Python standard library, used for type
  annotations;
- [**NumPy**](https://numpy.org/) v2.1, for array operations that are assumed to
  be understandable; and
- [**PyArrow**](https://arrow.apache.org/docs/python/index.html) v20.0, for
  operations on Apache Arrow arrays, which are conceptually equivalent to the
  in-memory representation of data stored in Parquet files.

!!! note "Algorithms are illustrative, not normative"
    Except where the prose explicitly uses RFC 2119 keywords, the code samples
    describe *one* correct way to produce conformant data. Implementations are
    free to use any method that yields an equivalent, conformant result.
