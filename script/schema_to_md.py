#!/usr/bin/env python3
"""Translate a JSON Schema file to Markdown documentation."""
import sys
import json
import argparse
import re

from urllib.request import urlopen
from pathlib import Path
from io import FileIO

def resolve_ref(ref: str, root: dict) -> dict:
    if not ref.startswith("#"):
        return {"description": f"External reference: `{ref}`"}
    parts = ref.lstrip("#").lstrip("/").split("/")
    node = root
    for part in parts:
        if part:
            node = node.get(part, {})
    return node


def ref_name(ref: str) -> str:
    if ref.startswith("http"):
        token = ref.rsplit('/', 1)[-1].replace(".json", '')
        return f"/mzPeak-specification/archive/{token.lower()}", token
    else:
        token = ref.rsplit("/", 1)[-1]
        return '#' + token, token


def type_str(schema: dict, root: dict) -> str:
    if "$ref" in schema:
        uri, name = ref_name(schema["$ref"])
        return f"[`{name}`]({uri})"
    t = schema.get("type")
    if t is None:
        for keyword in ("anyOf", "oneOf"):
            if keyword in schema:
                return " or ".join(type_str(s, root) for s in schema[keyword])
        if "enum" in schema:
            return "`enum`"
        return ""
    if isinstance(t, list):
        return " or ".join(f"`{x}`" for x in t)
    if t == "array":
        items = schema.get("items")
        return f"`array` of {type_str(items, root)}" if items else "`array`"
    return f"`{t}`"


def fmt_examples(examples: list) -> str:
    return ", ".join(f"`{json.dumps(e)}`" for e in examples)

def _mklink(mat):
    return f'<{mat.group(1)}>'

def detect_link(text: str):
    return re.sub(r"(?<!\()(http(?:s)?://\S+)", _mklink, text)

def render_properties(schema: dict, root: dict, level: int) -> list[str]:
    properties = schema.get("properties", {})
    if not properties:
        return []
    required = schema.get("required", [])
    h = "#" * level
    lines = []

    lines += [f"{h} Properties", ""]
    lines += [
        "| Property | Type | Required | Description |",
        "|----------|------|:--------:|-------------|",
    ]
    for name, prop in properties.items():
        resolved = resolve_ref(prop["$ref"], root) if "$ref" in prop else prop
        req = "Yes" if name in required else "&nbsp;"
        desc = detect_link(resolved.get("description", "&nbsp;").replace("\n", " "))
        lines.append(f"| `{name}` | {type_str(prop, root)} | {req} | {desc} |")
    lines.append("")

    lines += [f"{h} Property Details", ""]
    for name, prop in properties.items():
        resolved = resolve_ref(prop["$ref"], root) if "$ref" in prop else prop
        req_label = "*(required)*" if name in required else "*(optional)*"
        lines.append(f"**`{name}`** - {type_str(prop, root)} {req_label}")
        lines.append("")
        if desc := resolved.get("description", ""):
            lines += [detect_link(desc), ""]
        if examples := resolved.get("examples", []):
            lines += [f"*Examples:* {fmt_examples(examples)}", ""]
        if enum := resolved.get("enum", []):
            vals = ", ".join(f"`{json.dumps(v)}`" for v in enum)
            lines += [f"*Allowed values:* {vals}", ""]
    return lines


def render_node(schema: dict, root: dict, level: int) -> list[str]:
    h = "#" * level
    lines = []
    if title := schema.get("title"):
        lines += [f"{h} {title}", ""]
    if desc := schema.get("description"):
        lines += [detect_link(desc), ""]
    t = schema.get("type")
    if t == "array" and "items" in schema:
        items = schema["items"]
        if "$ref" in items:
            uri, name = ref_name(items["$ref"])
            lines += [
                "**Type:** `array`",
                f"**Items:** [`{name}`]({uri})",
                "",
            ]
        else:
            lines += [f"**Type:** `array` of {type_str(items, root)}", ""]
    elif t:
        lines += [f"**Type:** `{t}`", ""]

    lines.extend(render_properties(schema, root, level + 1))

    for keyword, label in (("anyOf", "Any of"), ("oneOf", "One of"), ("allOf", "All of")):
        if keyword in schema:
            lines += [f"**{label}:**", ""]
            for sub in schema[keyword]:
                sub_t = type_str(sub, root)
                sub_d = sub.get("description", "")
                lines.append(f"- {sub_t}" + (f" — {detect_link(sub_d)}" if sub_d else ""))
            lines.append("")
    return lines


def render_definitions(defs: dict, root: dict) -> list[str]:
    lines = ["---", "", "## Definitions", ""]
    for name, schema in defs.items():
        lines += [f"### {name}", f'<a name="{name.lower()}"></a>', ""]
        lines.extend(render_node(schema, root, level=3))
        lines += ["---", ""]
    return lines


def schema_to_markdown(schema: dict) -> str:
    root = schema
    lines = [f"# {schema.get('title', 'JSON Schema')}", ""]

    if desc := schema.get("description"):
        lines += [detect_link(desc), ""]

    if meta := schema.get("$meta"):
        if summary_uri := meta["summary"]:
            lines += [detect_link(urlopen(summary_uri).read().replace(b"\r", b"").decode('utf8')), ""]

    t = schema.get("type")
    if t == "array" and "items" in schema:
        items = schema["items"]
        if "$ref" in items:
            uri, name = ref_name(items["$ref"])
            lines += [
                "**Type:** `array`",
                f"**Items:** [`{name}`]({uri})",
                "",
            ]
        else:
            lines += [f"**Type:** `array` of {type_str(items, root)}", ""]
    elif t:
        lines += [f"**Type:** `{t}`", ""]

    lines.extend(render_properties(schema, root, level=2))

    defs = schema.get("definitions") or schema.get("$defs")
    if defs:
        lines.extend(render_definitions(defs, root))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Translate a JSON Schema file to Markdown documentation."
    )

    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Output Markdown file (default: stdout)",
    )
    parser.add_argument(
        "schema", type=Path, help="Path to the JSON Schema file", nargs="+"
    )
    args = parser.parse_args()
    outfh = None
    if args.output:
        outfh: FileIO = args.output.open("wt")
    for schema_path in args.schema:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        md = schema_to_markdown(schema)
        if outfh:
            outfh.write(md)
            print(f"Written to {args.output}")
        else:
            print(md)


if __name__ == "__main__":
    main()
