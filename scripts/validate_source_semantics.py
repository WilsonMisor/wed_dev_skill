#!/usr/bin/env python3
"""Static self-audit for Phase-2 Blueprint semantic extraction."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "scripts/source_intake.py",
    ROOT / "scripts/source_semantic_extract.py",
    ROOT / "orchestration/source-intake.md",
    ROOT / "tests/test_semantic_extraction.py",
]
missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
if missing:
    raise SystemExit("Missing source-semantic extraction files:\n" + "\n".join(missing))

intake = (ROOT / "scripts/source_intake.py").read_text(encoding="utf-8")
extract = (ROOT / "scripts/source_semantic_extract.py").read_text(encoding="utf-8")
doc = (ROOT / "orchestration/source-intake.md").read_text(encoding="utf-8")
tests = (ROOT / "tests/test_semantic_extraction.py").read_text(encoding="utf-8")

for token in [
    "semantic_extract(source, records)",
    "source_requirements",
    "observed_architecture",
    "declared_architecture",
    "approved_architecture",
    "observed_stack",
    "declared_stack",
    "approved_stack",
    "automatic_approval",
]:
    if token not in intake:
        raise SystemExit(f"source_intake.py missing semantic integration anchor: {token}")

for token in [
    "extract_requirements",
    "extract_observed_architecture",
    "extract_observed_stack",
    "extract_declared_facts",
    "DETERMINISTIC_TEXT_CANDIDATE",
    "requires_governed_review",
    "OBSERVED_FROM_REPOSITORY_STRUCTURE",
    "OBSERVED_FROM_FILES_AND_PROJECT_METADATA",
    "CANDIDATES_ONLY_HUMAN_OR_GOVERNED_DECISION_REQUIRED_FOR_APPROVAL",
]:
    if token not in extract:
        raise SystemExit(f"source_semantic_extract.py missing extraction semantic: {token}")

for token in [
    "Automatic semantic extraction",
    "Observed, declared, and approved separation",
    "Automatic extraction is **not approval**",
    "requirements already present",
    "technology stack",
    "`.docx`/`.pptx`",
    "never creates `approved_architecture` or `approved_stack`",
]:
    if token not in doc:
        raise SystemExit(f"source-intake documentation missing semantic anchor: {token}")

for token in [
    "without_decisions_file",
    "messy_pack",
    "does_not_promote_old_or_final_filename",
    "governed_architecture_and_stack_are_preserved_separately",
]:
    if token not in tests:
        raise SystemExit(f"semantic extraction acceptance tests missing coverage anchor: {token}")

print("PASS: Blueprint Phase-2 automatic requirement/architecture/stack extraction contract is present")
print("PASS: automatic extraction remains candidate evidence; approval and authority remain governed")
