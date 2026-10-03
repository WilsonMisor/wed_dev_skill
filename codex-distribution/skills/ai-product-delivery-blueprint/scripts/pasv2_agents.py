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
    "Blueprint owns project lifecycle classification, approved baselines, profile routing, and change control.",
    "Substantial production-relevant work routes through PREOS for risk, economics, evolution, evidence, and gate evaluation.",
    "gstack is specialist review and QA evidence only; it cannot approve risk, change the Blueprint baseline, or authorize release.",
    "Codex implements only the approved AI Task Packet scope and must stop on unbounded scope, stale source truth, or conflicting instructions.",
    "UNKNOWN, RED, unresolved HUMAN REVIEW, stale evidence, or missing authority fails closed for the affected production path.",
    "Accountable humans, not AI roles, accept consequential risk, waive material controls, and authorize production release.",
    "Project truth belongs in the application repository under `.ai-product-delivery/`; PREOS runtime state belongs under `PREOS_STATE_ROOT`.",
    "Do not deploy or mutate production data unless `PRODUCTION_RELEASE_AUTHORITY` is explicitly and durably approved.",
]


def managed_block() -> str:
    lines = [
        BEGIN,
        "## PAS / Blueprint Routing",
        "",
        "Use this block as the governed routing contract for AI-assisted delivery in this repository.",
        "",
    ]
    lines.extend(f"{idx}. {rule}" for idx, rule in enumerate(ROUTING_RULES, start=1))
    lines.extend(["", END])
    return "\n".join(lines)


def _find_block(text: str) -> tuple[int, int] | None:
    start = text.find(BEGIN)
    if start == -1:
        return None
    end = text.find(END, start)
    if end == -1:
        raise ValueError("AGENTS.md contains PAS routing block start marker without end marker")
    return start, end + len(END)


def upsert_text(text: str) -> tuple[str, bool]:
    block = managed_block()
    found = _find_block(text)
    if found:
        start, end = found
        prefix = text[:start].rstrip()
        suffix = text[end:].lstrip("\r\n")
        pieces = [piece for piece in (prefix, block, suffix.rstrip()) if piece]
        updated = "\n\n".join(pieces) + "\n"
    else:
        base = text.rstrip()
        updated = (base + "\n\n" if base else "") + block + "\n"
    return updated, updated != text


def remove_text(text: str) -> tuple[str, bool]:
    found = _find_block(text)
    if not found:
        return text, False
    start, end = found
    prefix = text[:start].rstrip()
    suffix = text[end:].lstrip("\r\n").rstrip()
    updated = "\n\n".join(piece for piece in (prefix, suffix) if piece)
    if updated:
        updated += "\n"
    return updated, updated != text


def block_count(text: str) -> int:
    return text.count(BEGIN)


def apply_agents(repo: Path, *, remove: bool = False, dry_run: bool = False) -> dict:
    path = repo / "AGENTS.md"
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    updated, changed = remove_text(original) if remove else upsert_text(original)
    if block_count(updated) > 1:
        raise ValueError("managed PAS routing block would be duplicated")
    if changed and not dry_run:
        path.write_text(updated, encoding="utf-8")
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
    original = path.read_text(encoding="utf-8") if path.exists() else ""
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
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    count = block_count(text)
    rules_present = all(rule in text for rule in ROUTING_RULES)
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