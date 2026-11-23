# Provenance and Signing

mzPeak includes a common mechanism for verifying the provenance of an archive using public key cryptography.
A writer [MAY]{class="may-chip"} produce SHA-512 digests of each column chunk of a Parquet file or of an entire file for non-Parquet
files. These digests are then signed with a private key known only by the source instrument (or other data producer)
and the source's creator, usually the instrument vendor. The signed digest is then stored along with the associated
public key in [Cryptographic Message Syntax (CMS)](https://datatracker.ietf.org/doc/html/rfc5652/) as
[Distinguished Encoding Rules (DER)](https://en.wikipedia.org/wiki/X.690#DER_encoding) binary, described below.
The key pair used [MUST]{class="must-chip"} be any of the following cipher + encoding pairs, which will be described in the CMS payload.

??? info "Cryptographic standards and Object Identifiers (OIDs)"
    Most named entities in cryptographic standards use an Object Identifier (OID) to uniquely identify that
    entity independent of its commonly used name. OIDs take the form of a sequence of digits separated by `.`
    to denote partition namespaces.


## Accepted Signatures

- Ed25519 (signature OID `1.3.101.112`) of the SHA-512 digest (digest OID `2.16.840.1.101.3.4.2.3`) of the data.
- ECDSA of the SHA-512 digest of the data (signature OID `1.2.840.10045.4.3.4`). The following common curves [SHOULD]{class="should-chip"}
  be supported:
    - P-256
    - P-521
- ML-DSA of the SHA-512 digest of the data. The following variants [SHOULD]{class="should-chip"} be supported:
  - ML-DSA 44 (signature OID `2.16.840.1.101.3.4.3.17`)
  - ML-DSA 65 (signature OID `2.16.840.1.101.3.4.3.18`)
  - ML-DSA 87 (signature OID `2.16.840.1.101.3.4.3.19`)

Unlike in the [index file](../archive/index-file.md), when a SHA digest is mentioned, the *raw bytes* of the digest are used,
not the hexadecimal text encoding. Additionally, while SHA-256 is much more common in cryptography, the cryptographic standards
do [NOT]{class="not-chip"} consistently distinguish between the hash used to digest the message and the hash used to prepare the signed attributes
for signing ([RFC 5652 section 5.4](https://www.rfc-editor.org/info/rfc5652/#section-5.4)). For simplicity, it is better to be
consistent everywhere.

## Chain of Trust

CMS defines a certificate verification chain whereby someone can verify that the instrument's private key was used to
generate a signature using the encoded public key, and then verify that the public key is tied to that instrument. If
a public key validates a signature, it can be checked that the certificate was issued by another entity by comparing
the signatures in the issued certificate against the issuing certificate's public key. This process is repeated until
we reach the end of the chain, a "root" of trust, who is and [MUST]{class="must-chip"} be trusted implicitly.

Either a vendor-specific or community managed body [MAY]{class="may-chip"} provide the roots of trust certificates for these chains,
acting as a certificate authority (CA) and certificate revocation list (CRL) issuer. A validator that checks signatures
[MUST]{class="must-chip"} obtain its root certificates and CRLs from a trusted source.

## Signature Table Schema

The signature table has the following layout

- **`index`** (uint64): the ascending 0-based index, incrementing by 1 per entry. Primary key for the `provenance` table.
- **`filename`** (string): the name of the file entry this signature came from or the special token `"*"` denoting a glob node, see below [Glob Nodes](#glob-nodes).
- **`row_group`** (uint64, optional): for Parquet files, the row group index that a particular column chunk belongs to.
- **`column`** (uint64, optional): for Parquet files, the column index that a particular column chunk belongs to.
- **`path`** (string, optional): for Parquet files, the dotted path in the Parquet schema for this column.
- **`offset`** (uint64, optional): for Parquet files, the offset into the raw byte stream this column begins at. When `null`, the offset is 0.
- **`length`** (uint64, optional): for Parquet files, the number of bytes to read. When `null`, the length is the length of the entire file.
- **`signature`** (binary): the digest of the bytes from `filename`, either in total or only a segment using SHA-512 and signed in CMS DER.

When signing an archive member file, the entire file [MUST]{class="must-chip"} be signed first, and only then [MAY]{class="may-chip"} segments be signed.
A signature on the entire file determines it is valid. Signing the segments is only performed if the writer wants to be able to explain
which part of the file was invalidated.

When signing or digesting a Parquet column chunk, consult the Parquet column chunk metadata. This is read from the file footer
and the ER diagram showing where these are found is available at <https://parquet.apache.org/docs/file-format/metadata/>.

- `offset` is `dictionary_page_offset` if present, `data_page_offset` otherwise.
- `length` is `total_compressed_size` of the column chunk.
- `row_group` is the index of the source row group in the Parquet file.
- `column` is the index in the column list for this column in the Parquet schema.
- `path` is the `name` in the Parquet schema, the dotted path from the root of the schema.

For Parquet file entries `row_group` and `column` indices are sufficient to retrieve the `path`, `offset`, and `length` metadata from a
well-formed Parquet file. The `offset` and `length` fields of the signature table [SHOULD NOT]{class="should-chip"} be trusted.

While whole-file signatures alone are sufficient to detect if the content has been changed, they do not tell the
reader what has changed, and data corruption is indistinguishable from tampering when the data are still technically
readable. By signing segments of the file, it is possible to determine where the changes were made and potentially
retain trust in parts of the file.

The final row in the table [MUST]{class="must-chip"} be a glob node. There [MAY]{class="may-chip"} be multiple glob nodes, but the final glob node [MUST]{class="must-chip"} be the
most recent. The order of entries in the table [MUST NOT]{class="must-not-chip"} change when an mzPeak archive is rewritten, even if none of the data
changed.

### Digest Process

When digesting a file or file segment for signing *or* verification, the following steps [MUST]{class="must-chip"} be followed to produce a valid digest
that is more difficult for an attacker to defeat. When operating on uncompressed ZIP archives, as always, file
offsets are relative to the ZIP member. When handling glob nodes, instead follow the instructions [listed below](#glob-nodes).

1. Initialize SHA-512 digest hash. All hashing operations are with respect to this hash.
2. Open the byte stream for `filename` in the archive.
3. If `offset` is not `null`, seek the byte stream to `offset` and hash `offset` as a little endian (LE) uint64 integer.
4. If `length` is not `null`, hash it as a LE uint64 integer. Read the byte stream in batches, hashing each batch until
   `length` bytes have been read *or* the end of the stream is reached.
5. Finalize the hash to produce the digest.

### Glob Nodes

When `filename` is `"*"`, digestion does not hash a specific file, but the `signature` of all rows of the `provenance` table of
all preceding rows whose `index` is less than the index of this row in ascending order of `index`. It [MUST]{class="must-chip"} have an `offset`
and `length` of `null`.

## Signing Process

When signing an mzPeak file, the following steps are performed for each member file:

1. A SHA-512 digest of the file is produced according to the [Digest Process](#digest-process) shown above stored as `digest`.
2. A `SignedAttributes`, a list of attributes, stored as `signedAttrs` is constructed containing the following entries in DER encoding order:
      - `attrType` = "content-type" (`1.2.840.113549.1.9.3`), `attrValues` = "data" (`1.2.840.113549.1.7.1`)
      - `attrType` = "signing-time" (`1.2.840.113549.1.9.5`), `attrValues` = the current time in UTC, or generalized time after the year 2049
      - `attrType` = "message-digest" (`1.2.840.113549.1.9.4`), `attrValues` = `digest` computed above
   The writer [MAY]{class="may-chip"} additionally follow [RFC 5126 CAdES](https://www.rfc-editor.org/info/rfc5126/) guidelines and add additional signing attributes such as:
      - `attrType` = "commitment-type-indication" (`1.2.840.113549.1.9.16.2.16`), with any appropriate list of claims for values, but especially "proof-of-creation" (`1.2.840.113549.1.9.16.6.5`)
      - `attrType` = "signing-certificate-v2" (`1.2.840.113549.1.9.16.2.47`), with `attrValues` being defined by [RFC 5035](https://www.rfc-editor.org/info/rfc5035/), using SHA-512 as the hash algorithm.
      - `attrType` = "content-identifier" (`1.2.840.113549.1.9.16.2.7`), `attrValues` = an octet string formatted as described in [RFC 2634 section 2.7](https://www.rfc-editor.org/info/rfc2634/#page-21). This is required for signing derived data, [see below](#use-beyond-instrument-linkage).
3. The private key is loaded and used to sign the DER representation of `signedAttrs` to form a
   `signed_digest` value per [RFC 5652 section 5.4](https://www.rfc-editor.org/info/rfc5652/#section-5.4),
   and then clear the key from memory. A PKCS #11 implementation [MAY]{class="may-chip"} be used to perform the signing using
   dedicated hardware for the purpose, in which case the private key remains in secure storage.
   When using ECDSA, the DER encoding must again be SHA-512 hashed, but the EdDSA and ML-DSA methods use the
   "pure" form of signing, signing the DER encoding directly, not rehashing the signing attributes
   first.
4. The companion public key certificate for the private key is loaded. Its identifier, either as an
   [`IssuerAndSerialNumber`](https://datatracker.ietf.org/doc/html/rfc5652/#section-10.2.4) instance or as a
   [`SubjectKeyIdentifier`](https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.2) instance stored as
   `signer_id`.
5. The writer [MAY]{class="may-chip"} acquire an [RFC 3161](https://datatracker.ietf.org/doc/html/rfc3161) timestamp token from
   a trusted timestamp authority (TSA) using a SHA-512 digest of the `signed_digest`'s octet string, excluding the DER
   tag and length as the message imprint of the timestamp request. The resulting timestamp token is used to write
   `UnsignedAttributes`, a list of attributes, stored as `unsignedAttrs` with the following entry:
      - `attrType` = "signature-time-stamp-token"(`1.2.840.113549.1.9.16.2.14`), `attrValues` = the timestamp token, itself a CMS `ContentInfo` structure signed by the TSA with content type `TSTInfo` (`1.2.840.113549.1.9.16.1.4`). Without this token, it is impossible to prove
      when a file was actually signed.
   The writer [MAY]{class="may-chip"} additionally follow [RFC 5126 CAdES](https://www.rfc-editor.org/info/rfc5126/) guidelines and add more unsigned attributes such as:
      - `attrType` "revocation-values" (`1.2.840.113549.1.9.16.2.24`)
6. A [`SignerInfo`](https://datatracker.ietf.org/doc/html/rfc5652/#section-5.3) instance `signerInfo` is constructed
   with a version according to the signing certificate per the RFC, with signed attributes `signedAttrs`,
   signature `signed_digest`, signature algorithm and digest algorithm OIDs appropriate for the private key as
   [described above](#accepted-signatures). If `unsignedAttrs` is defined, it is stored in `signerInfo`. The
   algorithm parameters [MUST]{class="must-chip"} be absent.
7. A [`SignedData`](https://datatracker.ietf.org/doc/html/rfc5652/#section-5.1) `signedData` is constructed with
   `version` defined per the RFC section, digest algorithms appropriate to the method used (SHA-512),
   encapsulated content info of type `data` (`1.2.840.113549.1.7.1`) and no content, and the signing certificate
   as well as any number of additional certificates required to link that certificate to a root of trust
   as the `certificates` set. The `signerInfo` value from step 6 is used as the `SignerInfos` member. Additional
   signers [MAY]{class="may-chip"} be included, repeating steps 3-6 for each additional signer. Any certificate revocation lists
   and expiration information available [MAY]{class="may-chip"} be included in the `signedData`'s `crls` field.
8. A [`ContentInfo`](https://datatracker.ietf.org/doc/html/rfc5652/#section-3) message is constructed with content type
   of "signed-data" (`1.2.840.113549.1.7.2`) and content of `signedData` is produced as the final CMS envelope
   content.

## Verification Process

When verifying an mzPeak file has not been tampered with or decayed, the following steps are performed for
each row in the signature table. Rows should be processed in reverse order, walking in descending `index`
order. If a row refers to a file that is replaced by derived data later in the table, it may fail verification
because the file being hashed is no longer the file that was signed, this failure.

1. Generate a SHA-512 digest according to the [Digest Process](#digest-process) described above.
2. Parse the CMS content in `signature` column of the row and confirm this is a signed-data message.
   The remaining operations are with respect to the CMS message and the recalculated digest.
3. Extract `signerInformation` from the CMS message and locate the issuing signer. This [SHOULD]{class="should-chip"} be the first
   signer. The signer's `digestAlgorithm` [MUST]{class="must-chip"} be SHA-512 and the `signatureAlgorithm` [MUST]{class="must-chip"}
   be one of the supported signature algorithms listed [above](#accepted-signatures) and the algorithm parameters
   [MUST]{class="must-chip"} be absent or empty.
4. Find the `SignedData` certificate whose `sid` matches the issuer and serial number or subject key identifier of the issuing signer and
   extract the public key for that certificate. All other certificates in `SignedData` are treated as intermediate
   certificates needed to tie the issuing certificate to a root of trust, or are the issuing certificate for an additional signer.
5. Extract the bytes of the DER `signedAttributes` from issuing signer. Replace the leading `IMPLICIT` tag
   byte (0xA0) with the `SET` tag byte (0x31) per [RFC 5652 section 5.4](https://www.rfc-editor.org/info/rfc5652/#section-5.4).
   This will be used to verify that the signature hasn't been tampered with and was signed by the private key via
   the public key. If the signed attributes include a "content-identifier" (`1.2.840.113549.1.9.16.2.7`) attribute, check that
   it has not superseded by another row with a greater `index` and if so, skip this step.
6. Extract `signature` from issuing signer. Using the public key from the certificate to verify that the
   `signature` value matches the `signedAttributes` DER encoded bytes. As noted previously, ECDSA keys
   require that the `signedAttributes` DER be hashed with SHA-512, while the other keys work on the DER bytes
   directly.
7. From the `signedAttributes` structure just verified, extract the attribute with a `type` of "message-digest" (`1.2.840.113549.1.9.4`)
   and confirm it matches the recomputed SHA-512 digest bytes (not text) for this row.
8. Verify that the certificate which provided the signing public key and associated intermediate
   are valid according to the X.509 verification procedure described in [RFC 5280](https://www.rfc-editor.org/info/rfc5280/).
   If embedded certificate revocation information is provided, it [MAY]{class="may-chip"} be used if no appropriate information is
   available from a trusted CA. If an [RFC 3161](https://datatracker.ietf.org/doc/html/rfc3161) "signature-time-stamp-token" is
   present, it [SHOULD]{class="should-chip"} also be verified, and then that time used to determine if the signing key was valid
   at the time of signing. Only if a timestamp token is present can the time-of-signing be known, the `signing-time` attribute is
   an unverifiable claim.

Users [MUST NOT]{class="must-not-chip"} treat the mere presence of a `provenance.parquet` as evidence of anything, including that a file is in
its rawest state, derived directly from a vendor file, or otherwise more trustworthy than its absence. Only after
verification against the roots of trust managed by the instrument vendor or trusted repository is an mzPeak archive verified.

## Use Beyond Instrument Linkage

It may be tempting to add additional roles beyond instrument -> vendor verification. To avoid increasing the complexity
of the signing and verification process, writers are [NOT]{class="not-chip"} encouraged to cryptographically sign non-raw datasets. In
practice, it is difficult for the average piece of software to secure its private keys when it is run on untrusted
hardware or distributed as source code.

Regulated software systems where such infrastructure can be put in place [MAY]{class="may-chip"} add more applications as defined below.
Each operation [MUST]{class="must-chip"} add a new row to the provenance table, and ensure that the table ends with a new glob node once
all new records are added.

### Registration/Approval

Another authority may add a [countersignature (RFC 5652 section 11.4)](https://www.rfc-editor.org/info/rfc5652/#section-11.4) to
indicate the approval or attestation. The most recent glob node is countersigned, which does not require rehashing or resigning.

### Derivative Data

If derived data needs to be attributable and traceable after replacing an existing archive member, writers [MAY]{class="may-chip"} add a signed
attribute "content-reference" (`1.2.840.113549.1.9.16.2.10`) whose value is a [`ContentReference (RFC 2634)`](https://www.rfc-editor.org/info/rfc2634/#section-2.11) referring to a previous version of the file being replaced. Someone who has access to the original file may then
check that it matches the claim made here. The correctness of the derivation process remains unverifiable. The existing row for this file
is [NOT]{class="not-chip"} removed from the provenance table, but [SHOULD]{class="should-chip"} be skipped when checking the remaining rows in the table according to the
"content-reference" and a matching "content-identifier" (`1.2.840.113549.1.9.16.2.7`). The presence of a "content-reference" [SHOULD]{class="should-chip"}
disqualify a file as being considered the original data.

When derivative data adds a new file without replacing an existing file, there does not exist a previously signed file to refer to.
In this case, it [MUST]{class="must-chip"} refer to the last glob node in the table.

In either case, in addition to writing any additional rows to the provenance table, a new glob node [MUST]{class="must-chip"} be added.
