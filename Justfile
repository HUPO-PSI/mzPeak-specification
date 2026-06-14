# mzPeak specification site — common tasks.
# Requires `uv` (https://docs.astral.sh/uv/). Run `just setup` once, then `just serve`.

venv := ".venv"
py   := venv / "bin"

# Create the build environment and install dependencies.
setup:
    uv venv --python 3.12 {{venv}}
    uv pip install --python {{venv}} -r requirements.txt

# Live-reload preview at http://127.0.0.1:8000
serve:
    {{py}}/mkdocs serve

# Strict production build into ./site (fails on broken links).
build:
    {{py}}/mkdocs build --clean --strict

# Build and deploy to the gh-pages branch (CI normally does this).
deploy:
    {{py}}/mkdocs gh-deploy --force

# Legacy single-file pandoc build, kept for reference.
build-legacy:
    pandoc --from markdown+smart --to=html5 --css=static/css/styling.css -s \
        index.md \
        -o index.html

# Validate the JSON Schemas under schema/.
validate-jsonschema:
    {{py}}/check-jsonschema -v --schemafile http://json-schema.org/draft-07/schema \
        schema/array_index.json \
        schema/auxiliary_array.json \
        schema/cv_list.json \
        schema/data_processing.json \
        schema/file_description.json \
        schema/instrument_configuration.json \
        schema/ms_run.json \
        schema/mzpeak_index.json \
        schema/param.json \
        schema/sample.json \
        schema/scan_settings_list.json \
        schema/software.json

render-jsonschema:
    uv run "script/schema_to_md.py" "schema/param.json" -o "docs/archive/param.md"
    uv run "script/schema_to_md.py" "schema/cv_list.json" -o "docs/archive/cv_list.md"
    uv run "script/schema_to_md.py" "schema/file_description.json" -o "docs/archive/file_description.md"
    uv run "script/schema_to_md.py" "schema/instrument_configuration.json" -o "docs/archive/instrument_configuration.md"
    uv run "script/schema_to_md.py" "schema/data_processing.json" -o "docs/archive/data_processing.md"
    uv run "script/schema_to_md.py" "schema/software.json" -o "docs/archive/software.md"
    uv run "script/schema_to_md.py" "schema/sample.json" -o "docs/archive/sample.md"
    uv run "script/schema_to_md.py" "schema/scan_settings_list.json" -o "docs/archive/scan_settings_list.md"
    uv run "script/schema_to_md.py" "schema/ms_run.json" -o "docs/archive/ms_run.md"