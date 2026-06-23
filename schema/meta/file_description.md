## Use cases

### Listing summary information about the *type* of measures in the file

The [`file_description.contents`] array can hold parameters that are children of [MS:1000524|data file content](http://purl.obolibrary.org/obo/MS_1000524). This includes spectrum types (e.g. [1000579|MS1 spectrum](http://purl.obolibrary.org/obo/MS_1000579), [1000580|MSn spectrum](http://purl.obolibrary.org/obo/MS_1000580), [MS:1000805|emission spectrum](http://purl.obolibrary.org/obo/MS_1000805), etc.), chromatogram types, polarity, and modifiers like children of [MS:1000525|spectrum representation](http://purl.obolibrary.org/obo/MS_1000525).

This may also cover acquisition methods [MS:1003213|mass spectrometry acquisition method](http://purl.obolibrary.org/obo/MS_1003213) which writers can use to signal strategies for downstream tools. This information is specialized and writers will need to take care when producing new files that the expected invariants are not broken.

### Enumerating source files for provenance tracking

The `file_description.source_files` array of [`source_file`](#source_file) lists all of the component files that were used to build this file. For many run formats, that would be a single file, or it might be many files for instruments that write directories like [MS:1001509|Agilent MassHunter format](http://purl.obolibrary.org/obo/MS_1001509) or that use an anchor file like [MS:1000562|ABI WIFF format](http://purl.obolibrary.org/obo/MS_1000562). Each file's checksum is recorded so that it is possible to verify that all input files are the same for equivalent reconstruction.

When converting derived files, they **SHOULD** be included in the list as additional source files.
