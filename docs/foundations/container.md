# Container & Archive

An mzPeak archive bundles several Parquet files and a JSON index under a single
name, usually with the `.mzpeak` or `.mzPeak` extension. That bundle can be delivered
three ways: as a ZIP archive, as an unpacked directory, or as a remote prefix
(for example an HTTP server supporting range requests, S3, FTP, or WebDAV).
Nested directories within an mzPeak archive are permitted but as of v1.0 all
required files are stored at the root of the archive's structure.

## ZIP archives

To pack multiple Parquet tables together under a single file name on disk requires
a container format. mzPeak uses the [ZIP](https://www.iana.org/assignments/media-types/application/zip)
archive to bundle the member files together. A ZIP file begins with a header containing
its magic bytes, followed by a sequence of (header, file) blocks, and terminates
with a **central directory** that records how to find each member. The headers **MUST**
store each file's name using UTF-8 encoding and use ZIP64 extended headers for members
larger than 4GB.

<figure class="mzp-figure wide" markdown>
<img src="../../assets/img/zip-structure-p1.svg" width="100%" />
</figure>

To read an mzPeak archive from an uncompressed ZIP archive, the ZIP reader follows the
normal process of reading the central directory, finding `mzpeak_index.json`, and using
that to identify which other files are needed. Each required file's start offset is read
from the central directory, and the length is queried from the local header. These are
then used to obtain the byte ranges needed to read Parquet metadata, then read the
relevant parts of the Parquet file.

<figure class="mzp-figure wide" markdown>
<img src="../../assets/img/zip-structure-p2.svg" width="100%" />
</figure>

mzPeak is stored in a ZIP **MUST** store its member files *uncompressed*. Uncompressed members
can be read directly without an intervening decompression step to reveal the Parquet file, and
each Parquet file already contains layered compression superior to that of a typical ZIP
compressor.

### Why not TAR?

TAR archives are designed for linear traversal: to learn what files an archive
contains you must hop from header entry to header entry until you reach the end.
Compared with ZIP's central directory, this is less efficient and more expensive
on object stores.

## Unpacked archives

If an mzPeak archive is stored as an unpacked directory, the directory name is
treated as the name of the archive. All other paths and files stored in the archive relative to
that directory. The directory may be stored on disk or as a URI prefix on a network.
The sole advantage to working with unpacked archives is that they are easier to write multiple
files to in parallel. There is no practical difference in efficiency when reading. When reading
an unpacked archive, the file system or host often provides a mechanism for enumerating files in
a directory or prefix so that member files can be found. Otherwise the reader **MUST** infer
the available names by guessing the URI for the `mzpeak_index.json` relative to the archive
root name and use the index to infer the names of member files.

## Encryption

Because Parquet supports
[modular encryption](https://parquet.apache.org/docs/file-format/data-pages/encryption/),
individual Parquet files — and even individual columns or the footer metadata —
can be encrypted while leaving the archive readable as a whole.

ZIP encryption **MUST** not be used. and ZIP encryption is widely known to be flawed and
inconsistently implemented. If additional files must be stored encrypted that are not already
written in Parquet columns or key-value metadata, these files **SHOULD** be stored encrypted
at rest within the archive.
