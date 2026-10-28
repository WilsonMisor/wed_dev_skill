#!/usr/bin/env python3
"""Manage the PAS/Blueprint routing block in a project AGENTS.md file."""
from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path

BEGIN = "<!-- BEGIN MANAGED PASV2 BLUEPRINT ROUTING -->"
END = "<!-- END MANAGED PASV2 BLUEPRINT ROUTING -->"

ROUTING_RULES = [
    "Substantial product work routes to Blueprint for lifecycle classification, approved baselines, profile routing, and change control.",
    "Production assurance routes through PREOS for risk, economics, evolution, evidence, and gate evaluation.",
    "gstack provides specialist execution, review, and QA evidence; specialist results do not grant risk acceptance or release authority.",
    "Implementation uses approved AI Task Packets and stays within their approved scope and current source bindings.",
    "Blueprint/PREOS gates cannot be bypassed; UNKNOWN, RED, unresolved HUMAN REVIEW, stale evidence, or missing authority blocks the affected production path.",
    "Direct specialist invocation is allowed for narrow tasks; it does not waive applicable Blueprint/PREOS gates.",
    "Conversation memory is not authoritative project state. Read the application repository's `.ai-product-delivery/` artifacts and PREOS_STATE_ROOT recovery state.",
    "Irreversible operations require appropriate accountable human authority; production release requires durable PRODUCTION_RELEASE_AUTHORITY.",
]
OWNED_NEWLINE = "<!-- PASV2 owns the newline immediately after its end marker. -->"


def managed_block() -> str:
    lines = [
        BEGIN,
        "## PAS / Blueprint Routing",
        "",
        "Use this block as the governed routing contract for AI-assisted delivery in this repository.",
        "",
    ]
    lines.extend(f"{idx}. {rule}" for idx, rule in enumerate(ROUTING_RULES, start=1))
    lines.extend(["", OWNED_NEWLINE, END])
    return "\n".join(lines) + "\n"


def _find_block(text: str) -> tuple[int, int] | None:
    starts, ends = text.count(BEGIN), text.count(END)
    if starts == ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise ValueError("AGENTS.md must contain exactly one complete managed block or no markers")
    start = text.find(BEGIN)
    end = text.find(END, start)
    if end == -1:
        raise ValueError("AGENTS.md contains PAS routing block start marker without end marker")
    stop = end + len(END)
    if OWNED_NEWLINE in text[start:end]:
        if text[stop:stop+2] == "\r\n":
            stop += 2
        elif text[stop:stop+1] == "\n":
            stop += 1
    return start, stop


def upsert_text(text: str) -> tuple[str, bool]:
    newline = "\r\n" if "\r\n" in text else "\n"
    block = managed_block().replace("\n", newline)
    found = _find_block(text)
    if found:
        start, end = found
        updated = text[:start] + block + text[end:]
    else:
        # Prepend so a missing trailing newline in user content is never edited.
        offset = 1 if text.startswith("\ufeff") else 0
        updated = text[:offset] + block + text[offset:]
    return updated, updated != text


def remove_text(text: str) -> tuple[str, bool]:
    found = _find_block(text)
    if not found:
        return text, False
    start, end = found
    updated = text[:start] + text[end:]
    return updated, updated != text


def block_count(text: str) -> int:
    return text.count(BEGIN)


def apply_agents(repo: Path, *, remove: bool = False, dry_run: bool = False) -> dict:
    path = repo / "AGENTS.md"
    original = path.read_bytes().decode("utf-8") if path.exists() else ""
    updated, changed = remove_text(original) if remove else upsert_text(original)
    if block_count(updated) > 1:
        raise ValueError("managed PAS routing block would be duplicated")
    if changed and not dry_run:
        path.write_bytes(updated.encode("utf-8"))
    return {
        "path": str(path),
        "changed": changed,
        "dry_run": dry_run,
        "removed": remove,
        "managed_block_count": block_count(updated),
        "rules": len(ROUTING_RULES),
    }


def diff_agents(repo: Path, *, remove: bool = False) -> str:
    path = repo / "AGENTS.md"
    original = path.read_bytes().decode("utf-8") if path.exists() else ""
    updated, _changed = remove_text(original) if remove else upsert_text(original)
    return "".join(
        difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile="AGENTS.md.before",
            tofile="AGENTS.md.after",
        )
    )


def check_agents(repo: Path) -> dict:
    path = repo / "AGENTS.md"
    text = path.read_bytes().decode("utf-8") if path.exists() else ""
    count = block_count(text)
    found = _find_block(text)
    block = text[slice(*found)] if found else ""
    rules_present = all(rule in block for rule in ROUTING_RULES)
    return {
        "path": str(path),
        "exists": path.exists(),
        "managed_block_count": count,
        "rules_present": rules_present,
        "valid": count == 1 and rules_present,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--remove", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if args.check:
        result = check_agents(repo)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("PASS" if result["valid"] else "FAIL")
        return 0 if result["valid"] else 1

    if args.diff:
        print(diff_agents(repo, remove=args.remove), end="")
        return 0

    result = apply_agents(repo, remove=args.remove, dry_run=args.dry_run)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        state = "changed" if result["changed"] else "unchanged"
        print(f"PAS AGENTS routing block {state}: {result['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
