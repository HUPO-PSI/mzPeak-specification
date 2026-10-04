#!/usr/bin/env python3
"""Validate an mzPeak JSON document against CV mapping rules.

Usage:
    python validate_cv.py <rules.json> <data.json>

Exit codes: 0 = all MUST rules satisfied, 1 = one or more MUST failures.

Path notation used in rule files:
    /a/b          - property access
    /a/b[]        - iterate over an array
    /a/b[k=v]     - filter array items where item["k"] == "v"

Limitation: 'allow_children' rules (which permit any ontology child of the
listed term) are approximated by a CV-namespace prefix check (e.g. "MS:").
Full hierarchy validation would require an OLS/OBO lookup.
"""

import json
import re
import sys

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from psims.document import VocabularyResolver, CV

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------


def split_path(path: str) -> list[str]:
    return [s for s in path.strip("/").split("/") if s]


def resolve(node: Any, segs: list[str]) -> list[Any]:
    """Recursively walk *node* following *segs*, collecting all matching values."""
    if not segs:
        return [node]
    seg, rest = segs[0], segs[1:]
    m = re.fullmatch(r"(\w+)(?:\[([^\]]*)\])?", seg)
    if not m or not isinstance(node, dict):
        return []
    prop, bracket = m.group(1), m.group(2)
    val = node.get(prop)
    if val is None:
        return []
    if bracket is None:
        return resolve(val, rest)
    items = val if isinstance(val, list) else [val]
    if bracket == "":
        return [leaf for item in items for leaf in resolve(item, rest)]
    key, fval = bracket.split("=", 1)
    return [
        leaf
        for item in items
        if isinstance(item, dict) and str(item.get(key)) == fval
        for leaf in resolve(item, rest)
    ]


def _common_prefix_len(a: list[str], b: list[str]) -> int:
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    return i


def get_params(scope_node: Any, rel_segs: list[str]) -> list[dict]:
    """
    Resolve param objects from *scope_node* given the relative path to the CV
    element.  The trailing 'accession' leaf is dropped; we want the full param
    objects so we can read both name and accession.
    """
    param_segs = rel_segs[:-1] if rel_segs and rel_segs[-1] == "accession" else rel_segs
    if not param_segs:
        return [scope_node] if isinstance(scope_node, dict) else []
    return [p for p in resolve(scope_node, param_segs) if isinstance(p, dict)]


# ---------------------------------------------------------------------------
# Term matching
# ---------------------------------------------------------------------------


PARENT_CACHE = {}


def parent_match(parent_accession: str, query_accession: str, cv_resolver: VocabularyResolver) -> bool:
    if (parent_accession, query_accession) in PARENT_CACHE:
        return PARENT_CACHE[parent_accession, query_accession]
    param_term = cv_resolver.term(query_accession)
    term_queue = deque([param_term])
    is_child = False
    while term_queue:
        next_term = term_queue.popleft()
        if next_term.id == parent_accession:
            is_child = True
            break
        else:
            parent = next_term.parent()
            if isinstance(parent, list):
                term_queue.extend(parent)
            elif parent and parent != next_term:
                term_queue.append(parent)
    PARENT_CACHE[parent_accession, query_accession] = is_child
    return is_child


def match_term(
    params: list[dict], term_rule: dict, cv_resolver: VocabularyResolver
) -> tuple[bool, str]:
    """Return (matched, note).

    Matching strategy:
    - use_term_name=True  -> compare param['name'] to term_rule['term_name']
    - use_term=True       -> exact param['accession'] == term_rule['term_accession']
    - allow_children=True -> if no exact match, accept any param whose accession
                            shares the same CV namespace prefix (approximation)
    """
    use_name = term_rule.get("use_term_name", False)
    use_term = term_rule.get("use_term", True)
    allow_child = term_rule.get("allow_children", False)
    accession = term_rule["term_accession"]
    name = term_rule["term_name"]

    # Exact / name match
    if use_term:
        key, want = ("name", name) if use_name else ("accession", accession)
        if any(p.get(key) == want for p in params):
            return True, ""

    if allow_child:
        kept_params = []
        for p in params:
            query_acc = p.get("accession")
            if not query_acc:
                continue

            param_term = cv_resolver.term(query_acc)
            if parent_match(accession, query_acc, cv_resolver):
                kept_params.append(param_term)

        if kept_params:
            return True, ""

    return False, ""


# ---------------------------------------------------------------------------
# Rule validation
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    rule_id: str
    level: str  # MUST / SHOULD / MAY
    passed: bool
    scope_index: int
    message: str
    note: str = ""  # non-empty when approximation was used


def validate_rule(
    rule: dict, data: dict, cv_resolver: VocabularyResolver
) -> list[Finding]:
    rule_id = rule["id"]
    scope_p = rule["scope_path"]
    elem_p = rule["cv_element_path"]
    level = rule["requirement_level"]
    logic = rule["cv_terms_combination_logic"]
    cv_terms = rule["cv_terms"]

    scope_segs = split_path(scope_p)
    elem_segs = split_path(elem_p)
    n = _common_prefix_len(scope_segs, elem_segs)
    rel_segs = elem_segs[n:]

    scope_nodes = resolve(data, scope_segs)
    if not scope_nodes:
        return []  # Scope absent – rule does not apply to this document

    findings: list[Finding] = []
    for idx, scope_node in enumerate(scope_nodes):
        params = get_params(scope_node, rel_segs)
        # is_repeatable=false check (applies regardless of requirement level)
        for term in cv_terms:
            try:
                _entity = cv_resolver.term(term["term_accession"])
            except KeyError:
                continue

            if not term.get("is_repeatable", True):
                key = "name" if term.get("use_term_name") else "accession"
                want = (
                    term["term_name"]
                    if term.get("use_term_name")
                    else term["term_accession"]
                )
                hits = [p for p in params if p.get(key) == want]
                if len(hits) > 1:
                    findings.append(
                        Finding(
                            rule_id=rule_id,
                            level=level,
                            passed=False,
                            scope_index=idx,
                            message=(
                                f"Term {term['term_accession']} (is_repeatable=false) "
                                f"appears {len(hits)} times in scope"
                            ),
                        )
                    )

        if level == "MAY":
            continue  # MAY imposes no mandatory constraint

        # --- combination logic ---
        results = [match_term(params, t, cv_resolver) for t in cv_terms]
        matched = [r[0] for r in results]
        notes = [r[1] for r in results if r[1]]

        if not params:
            ok = False
            detail = (
                f"no parameters found at scope[{idx}]; "
                f"{logic} constraint on "
                + ", ".join(t["term_accession"] for t in cv_terms)
                + " cannot be satisfied"
            )
        elif logic == "OR":
            ok = any(matched)
            detail = (
                "at least one of "
                + ", ".join(t["term_accession"] for t in cv_terms)
                + (" -- satisfied" if ok else " -- none found")
            )
        elif logic == "AND":
            ok = all(matched)
            missing = [
                cv_terms[i]["term_accession"] for i, m in enumerate(matched) if not m
            ]
            detail = "all terms required" + (
                f"; missing: {missing}" if not ok else " -- all present"
            )
        elif logic == "XOR":
            ok = sum(matched) == 1
            detail = (
                f"exactly one of {[t['term_accession'] for t in cv_terms]} required; "
                f"matched {sum(matched)}"
            )
        else:
            ok, detail = True, f"unknown logic {logic!r}"

        findings.append(
            Finding(
                rule_id=rule_id,
                level=level,
                passed=ok,
                scope_index=idx,
                message=detail if not ok else f"{len(params)} param(s) -- {detail}",
                note="; ".join(notes),
            )
        )

    return findings


def validate(rules_path: Path, data_path: Path) -> list[Finding]:
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    data = json.loads(data_path.read_text(encoding="utf-8"))
    cv_list = data["metadata"]["cv_list"]
    resolver = VocabularyResolver([CV(**cv) for cv in cv_list])
    resolver.load_vocabularies()
    out: list[Finding] = []
    for rule in rules["cv_mapping_rule_list"]:
        out.extend(validate_rule(rule, data, resolver))
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _tag(f: Finding) -> str:
    return f"[{f.scope_index}]" if f.scope_index > 0 else ""


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <rules.json> <data.json>")

    rules_path = Path(sys.argv[1])
    data_path = Path(sys.argv[2])

    for p in (rules_path, data_path):
        if not p.exists():
            sys.exit(f"File not found: {p}")

    findings = validate(rules_path, data_path)

    failures = [f for f in findings if not f.passed and f.level == "MUST"]
    warnings = [f for f in findings if not f.passed and f.level == "SHOULD"]
    approx = [f for f in findings if f.passed and f.note]
    ok_count = len(findings) - len(failures) - len(warnings)

    print(
        f"Validated {data_path.name} against {rules_path.name}: "
        f"{ok_count} OK, {len(warnings)} warning(s), {len(failures)} failure(s)"
        + (f", {len(approx)} approximated" if approx else "")
    )

    if approx:
        print("\nAPPROXIMATED (child-term check — ontology not loaded):")
        for f in approx:
            print(f"  {f.rule_id}{_tag(f)}: {f.note}")

    if warnings:
        print("\nWARNINGS (SHOULD):")
        for f in warnings:
            print(f"  {f.rule_id}{_tag(f)}: {f.message}")

    if failures:
        print("\nFAILURES (MUST):")
        for f in failures:
            print(f"  {f.rule_id}{_tag(f)}: {f.message}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
