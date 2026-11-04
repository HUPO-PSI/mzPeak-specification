# Provenance and Signing

mzPeak includes a common mechanism for verifying the provenance of an archive using public key cryptography.
A writer **MAY** produce SHA-512 digests of each column chunk of a Parquet file or of an entire file for non-Parquet
files. These digests are then signed with a private key known only by the source instrument (or other data producer)
and the source's creator, usually the instrument vendor. The signed digest is then stored along with the associated
public key in [Cryptographic Messaging Syntax (CMS)](https://www.rfc-editor.org/info/rfc5652/) as
[Distinguished Object Encoding (DER)](https://en.wikipedia.org/wiki/X.690#DER_encoding) binary, described below.
The key pair used **SHOULD** be an Ed25519 for simplicity.

CMS defines a certificate verification chain whereby you can verify that the instrument's private key was used to
generate a signature using the encoded public key, and then verify that the public key is tied to that instrument
by confirming with a certificate authority that the public key embedded in the signature is valid for the claimed
signer's identity during the validity period defined within the certificate.


## Signature Table Schema

The signature table has the following layout

- `filename` (string): The name of the file this signature came from
- `row_group` (uint64, optional): For Parquet files, the row group index that a particular column chunk belongs to
- `column` (uint64, optional): For Parquet files, the column index that a particular column chunk belongs to
- `path` (string, optional): For Parquet files, the dotted path in the Parquet schema for this column
- `offset` (uint64, optional): For Parquet files, the offset into the raw byte stream this column begins at
- `length` (uint64, optional): For Parquet files, the number of bytes to read
- `signature` (binary): The digest of the bytes from `filename`, either in total or starting at `offset` and read to `length` using SHA-512 and signed in CMS DER.

## Signing Process

TODO

## Verification Process

When verifying an mzPeak file has not been tampered with or decayed, the following steps are performed for
each row in the signature table:

1. The `filename` is present in the mzPeak archive.
2. If `row_group`, `column`, and `path` are defined, then `filename` **MUST** be a Parquet file.
3. Open `filename` as a raw byte stream. If `offset` is defined, seek to `offset` bytes relative to the start.
4. Generate a SHA-512 digest of the bytes in `filename`. If `length` is defined, only read that many bytes from
   the stream.
5. Parse the CMS content in `signature` column of the row and confirm this is a `signed_data` message.
   The remaining operations are with respect to the CMS message and the recalculated digest.
6. Extract `signerInformation` from the CMS message and locate the issuing signer. This **SHOULD** be the first
   signer. The signer's `digestAlgorithm` **MUST** be SHA-512 and the `signatureAlgorithm` **MUST** be Ed25519.
7. Find the `signedData` certificate whose `sid` matches the issuer and serial number of the issuing signer and
   extract the public key for that certificate. All other certificates in `signedData` are treated as intermediate
   certificates.
8. Extract the bytes of the ASN.1 `signedAttributes` from issuing signer. Replace the leading `IMPLICIT` tag
   byte (0xA0) with the `SET` tag byte (0x31) per [RFC 5652 section 5.4](https://www.rfc-editor.org/info/rfc5652/#section-5.4).
   This will be used to verify that the signature hasn't been tampered with and was signed by the private key via
   the public key.
9. Extract `signature` from issuing signer. Using the public key from the certificate to verify that the
   `signature` value matches the the `signedAttributes` ASN.1 encoded bytes.
10. From the `signedAttributes` structure just verified, extract the attribute with a `type` of `messageDigest`
    and confirm it matches the recomputed SHA-512 digest for this row.
11. If available, verify that the certificate which provided the signing public key and associated intermediate
    are valid according to the X.509 verification procedure described in <https://www.rfc-editor.org/info/rfc5280/>.

Users **MUST NOT** treat the mere presence of a `provenance.parquet` as evidence of anything, including that a file is in
its rawest state, derived directly from a vendor file, or otherwise more trustworthy than its absence. Only after
verification against the roots of trust managed by the instrument vendor or trusted repository.

## Use beyond instrument linkage

It may be tempting to add additional roles beyond instrument -> vendor verification. To avoid increasing the complexity
of the signing and verification process, writers are not encouraged to not cryptographically sign
