# Container & Archive

An mzPeak archive bundles several Parquet files and a JSON index under a single
name. That bundle can be delivered three ways: as a ZIP archive, as an unpacked
directory, or as a remote prefix (for example an HTTP server supporting range
requests, S3, FTP, or WebDAV).

## ZIP archives

To pack multiple Parquet tables together under a single file name on disk, we
need a container format. mzPeak uses the
[ZIP](https://www.iana.org/assignments/media-types/application/zip) archive to
bundle the member files together. A ZIP file begins with a header containing its
magic bytes, followed by a sequence of (header, file) blocks, and terminates
with a **central directory** that records how to find each member.

Files in a ZIP may be stored compressed or uncompressed.

!!! warning "Members MUST be stored uncompressed"
    When mzPeak is stored in a ZIP, it **MUST** store its member files
    *uncompressed*. Uncompressed members can be read directly without an
    intervening decompression step to reveal the Parquet file, and each Parquet
    file already contains layered compression superior to that of a typical ZIP
    compressor.

### Why not TAR?

TAR archives are designed for linear traversal: to learn what files an archive
contains you must hop from header entry to header entry until you reach the end.
Compared with ZIP's central directory, this is less efficient and more expensive
on object stores.

## Unpacked archives

If an mzPeak archive is stored as an unpacked directory, the directory name is
treated as the name of the archive. All other paths and files stored in the archive relative to that directory as usual.

## Encryption

Because Parquet supports
[modular encryption](https://parquet.apache.org/docs/file-format/data-pages/encryption/),
individual Parquet files — and even individual columns or the footer metadata —
can be encrypted while leaving the archive readable as a whole.

!!! question "Open item — index visibility vs. encryption"
    Anything placed in `mzpeak_index.json` is necessarily visible in cleartext
    to all readers unless ZIP encryption is used, and ZIP encryption is widely
    known to be flawed and inconsistently implemented. Metadata inside a Parquet
    footer's key–value pairs *can* be encrypted. The index is JSON for
    convenience and for easy access from scripting languages; whether sensitive
    fields should move into encryptable Parquet metadata is an open design
    question.
