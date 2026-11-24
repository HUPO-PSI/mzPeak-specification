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
with a **central directory** that records how to find each member. The headers [MUST]{class="must-chip"}
store each file's name using UTF-8 encoding and use ZIP64 extended headers for members
larger than 4GB.

When an mzPeak archive is stored in a ZIP archive, it [MUST]{class="must-chip"} store its member files *uncompressed*.
Uncompressed members can be read directly without an intervening decompression step to decode the raw
Parquet file, and each Parquet file already contains layered compression superior to that of a
typical ZIP compressor. An mzPeak archive does not require or forbid members to be aligned to a specific
file system page size.

<figure class="mzp-figure wide" markdown>
<img src="../../assets/img/zip-structure-p1.svg" width="100%" />
<figcaption>
The arrangement of members in a packed mzPeak archive
</figcaption>
</figure>

To read an mzPeak archive from an uncompressed ZIP archive, the ZIP reader follows the
normal process of reading the central directory, finding `mzpeak_index.json`, and using
that to identify which other files are needed. Each required file's start offset is read
from the central directory, and the length is queried from the local header, or the central
directory if it is not written in the local header. These are then used to obtain the byte
ranges needed to read Parquet metadata, then read the relevant parts of the Parquet file.

<figure class="mzp-figure wide" markdown>
<img src="../../assets/img/zip-structure-p2.svg" width="100%" />
<figcaption>
The steps to initiate the reading of a packed mzPeak archive
</figcaption>
</figure>

### Why not TAR?

TAR archives are designed for linear traversal: to learn what files an archive
contains, a reader must hop from header entry to header entry until it reaches the end.
Compared with ZIP's central directory, this is less efficient and more expensive
on object stores.

## Unpacked archives

If an mzPeak archive is stored as an unpacked directory, the directory name is
treated as the name of the archive. All other paths and files stored in the archive are described
relative to that directory. The directory may be stored on disk or as a URI prefix on a network.
The sole advantage to working with unpacked archives is that they are easier to write multiple
files to in parallel. There is no practical difference in efficiency when reading. When reading
an unpacked archive, the file system or host often provides a mechanism for enumerating files in
a directory or prefix so that member files can be found. Otherwise the reader [MUST]{class="must-chip"} infer
the available names by requesting `<prefix>/mzpeak_index.json` and use the index to infer the
names of member files.

## Member order

There is no fixed order in which members are written to a ZIP archive, save that in the
majority of cases members are written one at a time. As a consequence, the `mzpeak_index.json`
file is usually written last, after all other members have been registered and written.
This means that the entire mzPeak archive [MUST]{class="must-chip"} be completely written in order for it to
be readable. This limitation may be revisited in the future to enable streaming.

An unpacked archive has no defined "order" as directories have platform and/or locale orderings
that are independent of write order. Even more so, a ZIP archive produced by using the common
`zip` utility program may write files in an arbitrary order. To preserve compatibility, mzPeak
avoids placing requirements on this to keep the equivalence between packed and unpacked archives.

## Encryption

Because Parquet supports
[modular encryption](https://parquet.apache.org/docs/file-format/data-pages/encryption/),
individual Parquet files — and even individual columns or the footer metadata —
can be encrypted while leaving the archive readable as a whole.

ZIP encryption [MUST NOT]{class="must-not-chip"} be used. ZIP encryption is widely known to be flawed and
inconsistently implemented. If additional files must be stored encrypted that are not already
written in Parquet columns or key-value metadata, these proprietary files [SHOULD]{class="should-chip"} be stored
encrypted at rest within the archive using whatever means the intended reader knows to use to decrypt
them.

## Reading remotely hosted archives

When reading an mzPeak archive from a remote host, the hosting system must support retrieving an arbitrary
range of bytes from a name. [HTTP Range Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests)
are commonly supported by many production- and development-grade web servers, and this forms the basis for
range requests for many object storage services like AWS S3 and other protocols that build upon HTTP like
WebDAV. How they are retrieved is beyond the scope of this specification.

<figure class="mzp-figure wide" markdown>
<img src="../../assets/img/remote-access.svg" width="100%" title="A sequence of steps for reading from an HTTP-like remote host" />
<figcaption>
Decision flow for opening an archive hosted on a remote host
</figcaption>
</figure>

Different hosts will handle non-leaf nodes in a URL's path differently. For instance, some HTTP servers will render
a human-readable index page when serving a directory, while others will return an error. Two heuristics are available,
the first is to treat the path like a ZIP archive and try to read its central directory, and when that fails fall
back to the unpacked strategy. The second is to treat the path as an unpacked archive and request `<path>/mzpeak_index.json`
which will return an error if it doesn't exist and then assume the ZIP strategy.

When opening a Parquet file, the reader must parse the footer to extract the schema, metadata and indices. This may be more
expensive to do on a remote file. Some Parquet implementations allow this data to be cached and re-used on successive requests
for the same Parquet file.

<figure class="mzp-figure wide" markdown>
<img src="../../assets/img/remote-access-sequence.svg" width="100%" title="A sequence of steps for reading from an HTTP-like remote host" />
<figcaption>
A sequence diagram describing the interactions between the reading client and the remote host
</figcaption>
</figure>
