# Entity Types

The `entity_type` tells the reader what is *being* described in a file and, in
concert with the [`data_kind`](data-kinds.md), helps connect the right file to
the right reader API. There are currently four controlled values:

| `entity_type` | Description |
| :-- | :-- |
| `spectrum` | Mass spectra — entities occurring at a single point in time (or as close to that as framed or cycled acquisition allows), with a mass-related coordinate such as m/z or neutral mass. |
| `chromatogram` | Measurements *over time* — chromatograms and, for now, diagnostic traces (see below). |
| `wavelength_spectrum` | Like `spectrum`, but the coordinate is an electromagnetic wavelength. Analyzers measuring wavelength are far more heterogeneous than mass analyzers. Time series over wavelength may instead be stored as `chromatogram` entries. |
| `provenance`   | A cryptographic signature of components of the archive used for certifying that the content as written was attested to by an instrument known to its owner or vendor |
| `proprietary`  | implementation-defined | Entirely the purview of the writer (often an instrument vendor). Should be ignored unless the reader is for that vendor. |
| `other` | None of the above — something not yet covered by this living specification. |

Any value outside this list is treated as `other`, but implementations **MUST** preserve
the value provided rather than discarding the entity type label and recording an
undifferentiated "other". This permits forward compatibility as new entity types are
added without updating existing code.

<!-- !!! success "Diagnostic traces become their own namespace"
    Instrument **diagnostic traces** (pump pressure, source current, temperature,
    voltages, flow rate, …) will be stored under a **new entity-type namespace**
    (working name: *diagnostic traces*), distinct from `chromatogram`. They share
    the time-axis machinery of chromatograms but are semantically different
    measurements, and separating them keeps chromatogram queries clean. Until the
    dedicated namespace is specified, such traces may be carried as
    `chromatogram` entries with appropriate CV typing. -->

<!-- !!! info "Ion mobilograms — likely a future facet"
    Ion **mobilograms** (ion mobility as the primary axis) may be formalised as a
    separate facet. This was judged not yet required, but the format leaves room
    for it. -->

## Adding a new entity type

When a genuinely new kind of measured entity appears that does not fit
`spectrum`, `chromatogram`, or `wavelength spectrum`, a new entity type may be
introduced. Prefer a short, lower-case name, define its primary coordinate axis
and the [data kinds](data-kinds.md) it supports, and describe its relationship to
existing entity types.

!!! question "Open item — naming"
    Should the `chromatogram` entity type be renamed to something broader such as
    *traces*, now that diagnostic traces are moving to their own namespace? Left
    open.
