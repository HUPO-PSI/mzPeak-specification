import argparse
import json
from pathlib import Path

import jsonschema
import mzpeak
from mzpeak.file_index import DataKindTag, FileEntry
from pyarrow import parquet as pq

SCHEMA_LOCATION = Path(__file__).parent.parent / 'schema'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_path", type=str, help="The path to the mzPeak archive to do JSONSchema validation on")
    return parser.parse_args()


def main():
    args = parse_args()
    path: str = args.archive_path

    archive = mzpeak.MzPeakFile(path)

    print("Validating file index")
    index_json_text: str = archive.open_stream('mzpeak_index.json').read()
    index = json.loads(index_json_text)
    schema = json.loads((SCHEMA_LOCATION / 'mzpeak_index.json').read_text())
    jsonschema.validate(index, schema)

    for key, sub_obj in index['metadata'].items():
        schema = None
        match key:
            case "sample_list":
                schema = json.loads((SCHEMA_LOCATION / 'sample.json').read_text())
            case "file_description":
                schema = json.loads((SCHEMA_LOCATION / 'file_description.json').read_text())
            case "instrument_configuration_list":
                schema = json.loads((SCHEMA_LOCATION / 'instrument_configuration.json').read_text())
            case "run":
                schema = json.loads((SCHEMA_LOCATION / 'ms_run.json').read_text())
            case _:
                print(f"Skipping {key}, unknown metadata key")
                continue
        if schema is None: raise KeyError(f"Failed to infer schema for {key}")
        jsonschema.validate(sub_obj, schema)

    schema = json.loads((SCHEMA_LOCATION / 'array_index.json').read_text())

    entry: FileEntry
    for entry in archive.file_index:
        if entry.data_kind in (DataKindTag.DataArrays, DataKindTag.Peaks):
            print(f"Validating array index for {entry.name}")
            handle = pq.ParquetFile(archive.open_stream(entry))
            had_array_index = False
            for key, sub_obj in handle.metadata.metadata.items():
                if key.endswith(b"_array_index"):
                    had_array_index = True
                    array_index = json.loads(sub_obj)
                    jsonschema.validate(array_index, schema)
            if not had_array_index:
                raise ValueError(f"No array index found for {entry.name}")

    print("Valid JSON")


if __name__ == '__main__':
    main()