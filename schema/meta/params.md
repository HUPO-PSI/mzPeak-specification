## Controlled and custom metadata values.

The controlled vocabulary/ontology (CVs) parameter or `cvParam` is the foundation of mzPeak's flexible metadata model. Like [mzML](https://www.psidev.info/mzml),
mzPeak uses parameters to add metadata to an entity in an extensible way. The controlled vocabularies define semantics for a set of common terms
used for parameters with `accession` tied back to the CV, but if a suitable term does not exist a user is free to add arbitrary parameters without
an accession. mzML used a separate `userParam` element to signal that a parameter was uncontrolled, but mzPeak simply assumes that a parameter is
uncontrolled if its `accession` attribute is `null`.

Parameters attached to a CV will have an `accession`, a human readable name, and may be related to other terms through the hierarchical definition.
These relationships may constrain its acceptable value types, which units it may be associated with, and the contexts it is appropriate in. Readers
[SHOULD]{class="should-chip"} prefer to refer to controlled parameters by their stable `accession`, not their `name` which is not guaranteed to remain the same over time.

A parameter may be used in three contexts in mzPeak. One is in the JSON metadata, where this JSON schema is most appropriate. The other two are in
Parquet tables as either columns, or as a member of the `parameters` list of structs, which are both described in greater detail in the
[metadata table layout](../layouts/metadata-tables.md).
