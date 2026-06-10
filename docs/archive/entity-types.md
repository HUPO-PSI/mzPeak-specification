# Entity Types

The `entity_type` tells the reader what is *being* described in a file and, in
concert with the [`data_kind`](data-kinds.md), helps connect the right file to
the right reader API. There are currently four controlled values:

| `entity_type` | Description |
| :-- | :-- |
| `spectrum` | Mass spectra — entities occurring at a single point in time (or as close to that as framed or cycled acquisition allows), with a mass-related coordinate such as m/z or neutral mass. |
| `chromatogram` | Measurements *over time* — chromatograms and, for now, diagnostic traces (see below). |
| `wavelength spectrum` | Like `spectrum`, but the coordinate is an electromagnetic wavelength. Analyzers measuring wavelength are far more heterogeneous than mass analyzers. Time series over wavelength may instead be stored as `chromatogram` entries. |
| `other` | None of the above — something not yet covered by this living specification. |

Any value outside this list is treated as `other`.

## Decided at HUPO-PSI 2026 (Rome)

The May 2026 working session reached consensus on several additions. These are
recorded here as direction for upcoming drafts; their concrete schemas are still
being specified.

!!! success "Diagnostic traces become their own namespace"
    Instrument **diagnostic traces** (pump pressure, source current, temperature,
    voltages, flow rate, …) will be stored under a **new entity-type namespace**
    (working name: *diagnostic traces*), distinct from `chromatogram`. They share
    the time-axis machinery of chromatograms but are semantically different
    measurements, and separating them keeps chromatogram queries clean. Until the
    dedicated namespace is specified, such traces may be carried as
    `chromatogram` entries with appropriate CV typing.

!!! info "Ion mobilograms — likely a future facet"
    Ion **mobilograms** (ion mobility as the primary axis) may be formalised as a
    separate facet. This was judged not yet required, but the format leaves room
    for it.

!!! info "Imaging MS and regions of interest"
    Imaging MS is currently handled via pixel coordinates in the
    [spectrum metadata](../schemas/spectra.md) table. **Regions of interest** can
    be layered on top as spatial-annotation polygons (for example, feature-
    extraction bounding boxes). Parquet was chosen over ZARR for long-term
    stability and cross-language support.

!!! info "Intelligent data-acquisition traces"
    Traceability of an instrument's **decision-making during acquisition** (e.g.
    intelligent/IAPI-driven acquisition) is a recognised future need. It can be
    encoded as CV parameters per scan; cross-instrument interoperability will
    require dedicated ontology work.

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
