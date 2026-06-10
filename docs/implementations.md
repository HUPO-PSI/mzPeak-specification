# Implementations

mzPeak is backed by five independent, from-scratch implementations — not bindings
to a single core. Building on the widely available
[Apache Parquet](https://parquet.apache.org/) and
[Apache Arrow](https://arrow.apache.org/) libraries keeps the on-disk structure
language-independent, so each implementation reads and writes the same archives
natively.

| Language | Capability | API style |
| :-- | :-- | :-- |
| **Rust** | read / write | The reference reader and writer. |
| **Python** | read | Zero-copy Arrow / Pandas. |
| **R** | read | `dplyr`-compatible table access. |
| **C#** | read / write | Includes a Thermo RawFileReader demo. |
| **JavaScript / TypeScript** | read | Runs in the browser, Node, and Deno. |

## Rust — reference implementation

[`HUPO-PSI/mzPeak`](https://github.com/HUPO-PSI/mzPeak) (`mzpeak_prototyping`) is
the reference reader and writer. As the canonical implementation, it tracks the
specification most closely and is the place to confirm intended behaviour when
the prose is ambiguous.

## Python

A read-only library exposing mzPeak data as zero-copy
[Apache Arrow](https://arrow.apache.org/) tables and
[Pandas](https://pandas.pydata.org/) DataFrames, so metadata and signal can be
queried with the analytical tooling proteomics and metabolomics users already
know.

## R

A read-only library offering `dplyr`-compatible access to the packed metadata and
signal tables, developed in coordination with the
[R for Mass Spectrometry](https://www.rformassspectrometry.org/) community. The
current interface uses S6-style classes; an S4 interface (for full Bioconductor
ecosystem compatibility) is planned.

## C#

[`HUPO-PSI/mzPeak.NET`](https://github.com/HUPO-PSI/mzPeak.NET) is a read/write
implementation for the .NET ecosystem. It ships with a demonstration that reads
vendor data through Thermo's RawFileReader and writes it to mzPeak.

## JavaScript / TypeScript

A read-only implementation that runs in the browser, Node.js, and Deno, making
mzPeak archives directly inspectable on the web. An
[online viewer](https://hupo-psi.github.io/mzpeakts/) demonstrates reading local
and remote files — including extracted-ion chromatograms, base-peak
chromatograms, and metadata inspection — entirely client-side.

!!! note "A common cross-language API is in progress"
    A language-agnostic, OpenAPI-style description of the shared reader/writer
    interface (`open`, `get_spectrum`, `get_chromatogram`, `iterate`, `slice`,
    and related methods) is planned, to keep the implementations aligned as the
    format matures.

!!! tip "Building your own?"
    The format is language-independent — start from this specification and
    validate your output against the conformance validator (see [Tools](tools.md)).
    Contributions and feedback are welcome via the
    [HUPO-PSI repositories](https://github.com/HUPO-PSI).
