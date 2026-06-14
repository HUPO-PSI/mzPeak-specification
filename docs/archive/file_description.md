# mzPeak metadata file description

Describe the JSON format of the file description section

**Type:** `object`

## Properties

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `contents` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Parameters describing the contents of the file, such as types of spectra. Analogous to https://peptideatlas.org/tmp/mzML1.1.0.html#fileContent |
| `source_files` | `array` of [`source_file`](#source_file) | Yes | List of all files used as data sources for this mzPeak file. Analogous to https://peptideatlas.org/tmp/mzML1.1.0.html#sourceFileList |
| `contacts` | `array` of [`contact`](#contact) |  | Persons or entities responsible for the data contained here. |

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
| `contact_name` | `string` |  | The name of the contact person. This is equivalent to `MS:1000586|contact name` (http://purl.obolibrary.org/obo/MS_1000586) |
| `contact_affiliation` | `string` |  | The home institute of the contact person. This is equivalent to `MS:1000590|contact affiliation` (http://purl.obolibrary.org/obo/MS_1000590) |
| `parameters` | `array` of [`param`](/mzPeak-specification/archive/param) | Yes | Parameters describing the contact, such as name, organization, email, website, or address. |

#### Property Details

**`contact_name`** - `string` *(optional)*

The name of the contact person. This is equivalent to `MS:1000586|contact name` (<http://purl.obolibrary.org/obo/MS_1000586)>

**`contact_affiliation`** - `string` *(optional)*

The home institute of the contact person. This is equivalent to `MS:1000590|contact affiliation` (<http://purl.obolibrary.org/obo/MS_1000590)>

**`parameters`** - `array` of [`param`](/mzPeak-specification/archive/param) *(required)*

Parameters describing the contact, such as name, organization, email, website, or address.

---
