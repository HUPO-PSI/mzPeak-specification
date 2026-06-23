# mzPeak metadata file description

Describe the JSON format of the file description section

## Use cases

### Listing summary information about the *type* of measures in the file

The [`file_description.contents`] array can hold parameters that are children of [MS:1000524|data file content](http://purl.obolibrary.org/obo/MS_1000524). This includes spectrum types (e.g. [1000579|MS1 spectrum](http://purl.obolibrary.org/obo/MS_1000579), [1000580|MSn spectrum](http://purl.obolibrary.org/obo/MS_1000580), [MS:1000805|emission spectrum](http://purl.obolibrary.org/obo/MS_1000805), etc.), chromatogram types, polarity, and modifiers like children of [MS:1000525|spectrum representation](http://purl.obolibrary.org/obo/MS_1000525).

This may also cover acquisition methods [MS:1003213|mass spectrometry acquisition method](http://purl.obolibrary.org/obo/MS_1003213) which writers can use to signal strategies for downstream tools. This information is specialized and writers will need to take care when producing new files that the expected invariants are not broken.

### Enumerating source files for provenance tracking

The `file_description.source_files` array of [`source_file`](#source_file) lists all of the component files that were used to build this file. For many run formats, that would be a single file, or it might be many files for instruments that write directories like [MS:1001509|Agilent MassHunter format](http://purl.obolibrary.org/obo/MS_1001509) or that use an anchor file like [MS:1000562|ABI WIFF format](http://purl.obolibrary.org/obo/MS_1000562). Each file's checksum is recorded so that it is possible to verify that all input files are the same for equivalent reconstruction.

When converting derived files, they **SHOULD** be included in the list as additional source files.


**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `contents` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Parameters describing the contents of the file, such as types of spectra. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#fileContent> |
| `source_files` | `array` of [`source_file`](#source_file) | Yes | List of all files used as data sources for this mzPeak file. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#sourceFileList> |
| `contacts` | `array` of [`contact`](#contact) | &nbsp; | Persons or entities responsible for the data contained here. |

## Property Details

**`contents`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Parameters describing the contents of the file, such as types of spectra. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#fileContent>

**`source_files`** - `array` of [`source_file`](#source_file) *(required)*

List of all files used as data sources for this mzPeak file. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#sourceFileList>

**`contacts`** - `array` of [`contact`](#contact) *(optional)*

Persons or entities responsible for the data contained here.

---

## Definitions

### source_file
<a name="source_file"></a>

A data file that was read in order to produce this mzPeak file. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#sourceFile>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` | Yes | A unique identifier for this source file. |
| `name` | `string` | Yes | The name of the source file, not including parent directory |
| `location` | `string` | Yes | The path to the source file, URI encoded. This may include file:// protocols and UNC paths |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Additional parameters describing this source file, like checksums, nativeID format, or file format |

#### Property Details

**`id`** - `string` *(required)*

A unique identifier for this source file.

**`name`** - `string` *(required)*

The name of the source file, not including parent directory

**`location`** - `string` *(required)*

The path to the source file, URI encoded. This may include file:// protocols and UNC paths

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Additional parameters describing this source file, like checksums, nativeID format, or file format

---

### contact
<a name="contact"></a>

A person or entity that is responsible for some portion of the data or processing that resulted in this archive. Analogous to <https://peptideatlas.org/tmp/mzML1.1.0.html#contact>

**Type:** `object`

#### Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `contact_name` | `string` | &nbsp; | The name of the contact person. This is equivalent to `MS:1000586|contact name` (http://purl.obolibrary.org/obo/MS_1000586) |
| `contact_affiliation` | `string` | &nbsp; | The home institute of the contact person. This is equivalent to `MS:1000590|contact affiliation` (http://purl.obolibrary.org/obo/MS_1000590) |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Parameters describing the contact, such as name, organization, email, website, or address. |

#### Property Details

**`contact_name`** - `string` *(optional)*

The name of the contact person. This is equivalent to `MS:1000586|contact name` (http://purl.obolibrary.org/obo/MS_1000586)

**`contact_affiliation`** - `string` *(optional)*

The home institute of the contact person. This is equivalent to `MS:1000590|contact affiliation` (http://purl.obolibrary.org/obo/MS_1000590)

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Parameters describing the contact, such as name, organization, email, website, or address.

---
