# Motivation

## Description of the need

[mzML](https://www.psidev.info/mzML) has served the mass spectrometry community
well as an open, vendor-neutral interchange format. As instruments have become
faster and experiments larger — ion-mobility separations, imaging, data-
independent acquisition — several of mzML's design choices have become limiting:

- **Size and access are at odds.** mzML stores binary arrays as base64-encoded
  text inside XML. The encoding inflates files, and the usual remedy
  (whole-file `gzip`) destroys the random access needed to read a single
  spectrum or an extracted-ion chromatogram without decompressing everything.
- **Imaging data fits poorly.** Spatial coordinates have to be bolted on;
  imzML exists but integrates awkwardly with the rest of the ecosystem.
- **Vendor metadata is lost.** Much of what an instrument records has no place
  in the mzML model and is discarded at conversion time.
- **Profile and centroid cannot coexist.** A single mzML spectrum cannot carry
  both its raw profile signal and a centroided peak list at the same time.
- **No encryption.** mzML offers no mechanism for protecting parts of a file.

mzPeak is designed to remove these limitations while remaining open, language-
agnostic, and grounded in the controlled vocabularies the community already
uses.

## Issues to be addressed

The format is shaped by a small number of concrete goals:

1. **Compact storage with preserved random access** — files smaller than mzML
   (often by half or more) that can still be sliced by spectrum, m/z range, or
   time range without decoding the whole file.
2. **Fast analytical queries** — extracted-ion chromatograms and similar reads
   served efficiently through columnar page indices.
3. **Profile *and* centroid signal** for the same spectrum, stored side by side.
4. **Richer metadata** — room for the vendor and acquisition metadata mzML
   cannot express, without forcing it into a rigid schema.
5. **Additional modalities** — ion mobility, imaging coordinates, wavelength
   spectra, and diagnostic traces, with room to grow.
6. **Optional encryption** of sensitive parts of an archive.
7. **A stable, cross-language data substrate** that many implementations can
   read and write independently.
