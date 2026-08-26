#!/usr/bin/env python3
"""Deterministic, non-executing source intake helper for the Blueprint.

The helper inventories and hashes supplied material, performs safe deterministic
candidate extraction for requirements plus observed/declared architecture and
technology stack, and then applies explicit governed decisions. Extraction is
never authority: approved architecture/stack and source authority remain human
or otherwise governed decisions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from datetime import datetime, timezone
from typing import Any
import zipfile

from source_semantic_extract import merge_fact_objects, semantic_extract

CODE_EXTENSIONS = {
    ".php", ".js", ".jsx", ".ts", ".tsx", ".py", ".java", ".kt", ".kts",
    ".swift", ".dart", ".go", ".rs", ".rb", ".cs", ".cpp", ".cc", ".c",
    ".h", ".hpp", ".vue", ".svelte", ".sql", ".sh", ".ps1",
}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".idea", ".vscode"}
AUTHORITY_RANK = {
    "UNRESOLVED_CONFLICT": -1,
    "UNCLASSIFIED": 0,
    "DRAFT_REFERENCE_HISTORY": 1,
    "IMPLEMENTATION_EVIDENCE": 2,
    "APPROVED_SUPPORTING": 3,
    "DECLARED_PRIMARY": 4,
    "HUMAN_APPROVED": 5,
}
SOURCE_STATUS = {
    "CURRENT_CANDIDATE", "CURRENT", "SUPERSEDED", "STALE", "MISSING", "REFERENCE_ONLY"
}
PROJECT_MODES = {"GREENFIELD", "BROWNFIELD", "HYBRID_OR_MIGRATION", "UNKNOWN"}
AUTHORITATIVE_SOURCE_AUTHORITIES = {"HUMAN_APPROVED", "DECLARED_PRIMARY", "APPROVED_SUPPORTING"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def safe_member_name(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise ValueError(f"unsafe absolute ZIP path: {name}")
    p = PurePosixPath(normalized)
    if any(part in {"..", ""} for part in p.parts):
        raise ValueError(f"unsafe ZIP traversal path: {name}")
    return p


def is_zip_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def is_zip_reparse(info: zipfile.ZipInfo) -> bool:
    return bool((info.external_attr & 0xFFFF) & 0x0400)


def inspect_zip(path: Path, extract_root: Path | None = None) -> tuple[list[dict], list[str]]:
    records: list[dict] = []
    warnings: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            rel = safe_member_name(info.filename)
            if is_zip_symlink(info):
                raise ValueError(f"unsafe ZIP symlink entry: {info.filename}")
            if is_zip_reparse(info):
                raise ValueError(f"unsafe ZIP reparse/junction entry: {info.filename}")
            data = zf.read(info)
            record = {
                "source_id": "",
                "path": str(rel),
                "source_type": "ZIP_MEMBER",
                "size": len(data),
                "sha256": sha256_bytes(data),
                "authority": "UNCLASSIFIED",
                "status": "CURRENT_CANDIDATE",
                "supersedes": [],
                "superseded_by": [],
                "conflict_group": None,
            }
            records.append(record)
            if extract_root is not None:
                target = (extract_root / Path(*rel.parts)).resolve()
                base = extract_root.resolve()
                if target != base and base not in target.parents:
                    raise ValueError(f"ZIP extraction escaped staging root: {info.filename}")
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    if not target.is_file() or sha256_file(target) != sha256_bytes(data):
                        raise ValueError(f"unsafe ZIP overwrite with different content: {info.filename}")
                else:
                    target.write_bytes(data)
    return records, warnings


def inspect_directory(path: Path, output_root: Path) -> tuple[list[dict], list[str]]:
    records: list[dict] = []
    warnings: list[str] = []
    for p in sorted(path.rglob("*")):
        try:
            rel = p.relative_to(path)
        except ValueError:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        try:
            if output_root.resolve() == p.resolve() or output_root.resolve() in p.resolve().parents:
                continue
        except OSError:
            pass
        if p.is_symlink():
            warnings.append(f"symlink skipped during intake: {rel.as_posix()}")
            continue
        if not p.is_file():
            continue
        records.append({
            "source_id": "",
            "path": rel.as_posix(),
            "source_type": "FILE",
            "size": p.stat().st_size,
            "sha256": sha256_file(p),
            "authority": "UNCLASSIFIED",
            "status": "CURRENT_CANDIDATE",
            "supersedes": [],
            "superseded_by": [],
            "conflict_group": None,
        })
    return records, warnings


def detect_mode(records: list[dict]) -> str:
    has_code = any(Path(r["path"]).suffix.lower() in CODE_EXTENSIONS for r in records)
    return "BROWNFIELD" if has_code else "GREENFIELD"


def build_duplicate_groups(records: list[dict]) -> list[dict]:
    groups: dict[str, list[str]] = {}
    for r in records:
        groups.setdefault(r["sha256"], []).append(r["path"])
    out = []
    n = 1
    for digest, paths in sorted(groups.items()):
        if len(paths) > 1:
            out.append({"duplicate_group": f"DUP-{n:04d}", "sha256": digest, "paths": sorted(paths)})
            n += 1
    return out


def _version_family(path_text: str) -> str:
    stem = Path(path_text).stem.lower()
    stem = re.sub(r"(?:^|[-_. ]+)(?:final|draft|copy|old|archive|rev(?:ision)?[-_. ]*\d*|v\d+(?:\.\d+)*|\d{4}[-_.]\d{2}(?:[-_.]\d{2})?)(?=$|[-_. ]+)", " ", stem)
    return re.sub(r"[^a-z0-9]+", "", stem)


def build_version_candidate_groups(records: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for r in records:
        family = _version_family(r["path"])
        if family:
            groups.setdefault(family, []).append(r)
    out: list[dict] = []
    n = 1
    for family, members in sorted(groups.items()):
        hashes = {m["sha256"] for m in members}
        if len(members) > 1 and len(hashes) > 1:
            out.append({
                "version_candidate_group": f"VER-{n:04d}",
                "family": family,
                "source_ids": sorted(m["source_id"] for m in members),
                "paths": sorted(m["path"] for m in members),
                "rule": "CANDIDATE_ONLY_DO_NOT_INFER_SUPERSESSION",
            })
            n += 1
    return out


def detect_source_hash_drift(previous_records: list[dict], current_records: list[dict]) -> list[dict]:
    previous = {
        str(record.get("path")): record
        for record in previous_records
        if record.get("path") and record.get("authority") in AUTHORITATIVE_SOURCE_AUTHORITIES
    }
    current = {str(record.get("path")): record for record in current_records if record.get("path")}
    drift: list[dict] = []
    for source_path, prior in sorted(previous.items()):
        now = current.get(source_path)
        prior_hash = str(prior.get("sha256") or "")
        if now is None:
            drift.append({
                "path": source_path, "authority": prior.get("authority"),
                "state": "MISSING_AUTHORITATIVE_SOURCE", "previous_sha256": prior_hash,
                "current_sha256": None, "impact_analysis_required": True, "blocking": True,
            })
            continue
        current_hash = str(now.get("sha256") or "")
        if current_hash != prior_hash:
            drift.append({
                "path": source_path, "authority": prior.get("authority"),
                "state": "CHANGED_AUTHORITATIVE_SOURCE", "previous_sha256": prior_hash,
                "current_sha256": current_hash, "impact_analysis_required": True, "blocking": True,
            })
    return drift


def assign_ids(records: list[dict]) -> None:
    for idx, record in enumerate(records, 1):
        record["source_id"] = f"SRC-{idx:04d}"


def _source_lookup(records: list[dict]) -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for r in records:
        lookup[r["source_id"]] = r
        lookup[r["path"]] = r
    return lookup


def _resolve_source_ref(ref: str, lookup: dict[str, dict]) -> dict:
    if ref not in lookup:
        raise ValueError(f"governed decision references unknown source: {ref}")
    return lookup[ref]


def apply_source_decisions(records: list[dict], decisions: list[dict]) -> None:
    lookup = _source_lookup(records)
    explicit_status: set[str] = set()
    for decision in decisions:
        ref = decision.get("source_id") or decision.get("path")
        if not ref:
            raise ValueError("source decision requires source_id or path")
        record = _resolve_source_ref(str(ref), lookup)
        if "authority" in decision:
            authority = str(decision["authority"])
            if authority not in AUTHORITY_RANK:
                raise ValueError(f"invalid source authority: {authority}")
            record["authority"] = authority
        if "status" in decision:
            status_value = str(decision["status"])
            if status_value not in SOURCE_STATUS:
                raise ValueError(f"invalid source status: {status_value}")
            record["status"] = status_value
            explicit_status.add(record["source_id"])
        if "conflict_group" in decision:
            record["conflict_group"] = decision.get("conflict_group")
        if "topic" in decision:
            record["topic"] = decision.get("topic")
        if "declared_version" in decision:
            record["declared_version"] = decision.get("declared_version")
        supersedes = decision.get("supersedes", [])
        if isinstance(supersedes, str):
            supersedes = [supersedes]
        record["supersedes"] = sorted({_resolve_source_ref(str(x), lookup)["source_id"] for x in supersedes})
    by_id = {r["source_id"]: r for r in records}
    for r in records:
        r["superseded_by"] = []
    for r in records:
        for old_id in r.get("supersedes", []):
            old = by_id[old_id]
            old["superseded_by"].append(r["source_id"])
            if old["source_id"] not in explicit_status:
                old["status"] = "SUPERSEDED"
    for r in records:
        r["superseded_by"] = sorted(set(r["superseded_by"]))


def build_conflict_groups(records: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for r in records:
        if r.get("conflict_group"):
            grouped.setdefault(str(r["conflict_group"]), []).append(r)
    conflicts: list[dict] = []
    for group_id, members in sorted(grouped.items()):
        hashes = {m["sha256"] for m in members}
        if len(hashes) <= 1:
            conflicts.append({
                "conflict_group": group_id,
                "source_ids": sorted(m["source_id"] for m in members),
                "status": "NOT_A_CONTENT_CONFLICT_EXACT_DUPLICATES", "blocking": False,
            })
            continue
        ranks = {m["source_id"]: AUTHORITY_RANK.get(m.get("authority", "UNCLASSIFIED"), 0) for m in members}
        highest = max(ranks.values())
        winners = [sid for sid, rank in ranks.items() if rank == highest and rank > 0]
        if len(winners) == 1:
            conflicts.append({
                "conflict_group": group_id,
                "source_ids": sorted(m["source_id"] for m in members),
                "status": "RESOLVED_BY_EXPLICIT_AUTHORITY", "winning_source_id": winners[0], "blocking": False,
            })
        else:
            conflicts.append({
                "conflict_group": group_id,
                "source_ids": sorted(m["source_id"] for m in members),
                "status": "SOURCE CONFLICT", "blocking": True,
                "reason": "conflicting content has no unique higher-authority governed source",
            })
    return conflicts


def normalize_requirements(requirements: list[dict], records: list[dict]) -> list[dict]:
    lookup = _source_lookup(records)
    normalized: list[dict] = []
    for item in requirements:
        ref = item.get("source_id") or item.get("source_path")
        if not ref:
            raise ValueError("source requirement requires source_id or source_path")
        source = _resolve_source_ref(str(ref), lookup)
        wording = str(item.get("original_wording") or "").strip()
        if not wording:
            raise ValueError("source requirement original_wording is required")
        normalized.append({
            "source_id": source["source_id"],
            "source_location": str(item.get("source_location") or "UNKNOWN"),
            "original_wording": wording,
            "normalized_interpretation": str(item.get("normalized_interpretation") or ""),
            "category": str(item.get("category") or "UNCLASSIFIED"),
            "authority": str(item.get("authority") or source.get("authority") or "UNCLASSIFIED"),
            "confidence": str(item.get("confidence") or "UNKNOWN"),
            "conflict_state": str(item.get("conflict_state") or "NONE"),
            "extraction_method": str(item.get("extraction_method") or "GOVERNED_INPUT"),
            "requires_governed_review": bool(item.get("requires_governed_review", False)),
        })
    normalized.sort(key=lambda x: (
        x["source_id"], x["source_location"], x["original_wording"], x["normalized_interpretation"]
    ))
    for idx, item in enumerate(normalized, 1):
        item["requirement_id"] = f"SRCREQ-{idx:04d}"
    return normalized


def _merge_requirement_inputs(extracted: list[dict], governed: list[dict]) -> list[dict]:
    """Merge candidates deterministically; governed duplicates replace extracted metadata."""
    merged: dict[tuple[str, str], dict] = {}
    for item in extracted:
        key = (str(item.get("source_path") or item.get("source_id")), str(item.get("original_wording", "")).casefold())
        merged[key] = item
    for item in governed:
        key = (str(item.get("source_path") or item.get("source_id")), str(item.get("original_wording", "")).casefold())
        merged[key] = item
    return list(merged.values())


def _object(payload: dict, key: str) -> dict:
    value = payload.get(key, {})
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def _list(payload: dict, key: str) -> list:
    value = payload.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be an array")
    return value


def write_summary(path: Path, intake: dict) -> None:
    blocking = [c for c in intake.get("source_conflicts", []) if c.get("blocking")]
    lines = [
        "# Source Intake Summary", "",
        f"Generated: {intake['generated_at']}",
        f"Project mode: **{intake['project_mode']}**",
        f"Sources inventoried: **{len(intake['sources'])}**",
        f"Semantic documents examined: **{len(intake.get('semantic_extraction', {}).get('documents_examined', []))}**",
        f"Source requirements extracted/merged: **{len(intake['source_requirements'])}**",
        f"Exact duplicate groups: **{len(intake['duplicate_groups'])}**",
        f"Version candidate groups: **{len(intake['version_candidate_groups'])}**",
        f"Blocking source conflicts: **{len(blocking)}**",
        f"Authoritative source drift items: **{len(intake.get('source_drift', []))}**", "",
        "## Authority", "",
        "Automatic semantic extraction produces candidates/evidence only. It never grants source authority and never creates approved architecture or approved technology stack. Human/governed decisions remain authoritative.",
        "", "## Warnings", "",
    ]
    warnings = intake.get("warnings", [])
    lines += [f"- {w}" for w in warnings] if warnings else ["- None."]
    lines += ["", "## Source drift", ""]
    drift = intake.get("source_drift", [])
    if drift:
        lines += [f"- {item['state']} `{item['path']}` requires downstream impact analysis before affected work advances." for item in drift]
    else:
        lines += ["- No authoritative source-hash drift detected against the supplied baseline manifest."]
    lines += ["", "## Conflicts", ""]
    if blocking:
        lines += [f"- SOURCE CONFLICT `{c['conflict_group']}` blocks affected downstream work." for c in blocking]
    else:
        lines += ["- No unresolved blocking source conflicts recorded."]
    lines += ["", "## Next governed step", "",
              "Review extracted candidates, resolve source authority/conflicts and complete source requirements before Blueprint discovery. PREOS Project Contract creation occurs only after approved PRD and Project Classification.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def load_decisions(path: str | None) -> dict:
    if not path:
        return {}
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("governed decisions file must contain a JSON object")
    return data


def load_baseline_sources(path: str | None) -> list[dict]:
    if not path:
        return []
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        raise ValueError("baseline manifest must be a JSON object containing a sources array")
    return data["sources"]


def main() -> None:
    ap = argparse.ArgumentParser(description="Safely inventory and semantically extract project source material without executing it.")
    ap.add_argument("source", help="Directory, repository, file, or ZIP archive to inspect")
    ap.add_argument("--project-root", default=".", help="Application repository root (default: current directory)")
    ap.add_argument("--output", help="Output directory (default: <project-root>/.ai-product-delivery/source-intake)")
    ap.add_argument("--extract-zip", action="store_true", help="Safely extract ZIP members into derived staging under the output directory")
    ap.add_argument("--intent", default="", help="Optional short human intent statement; recorded separately from documentary truth")
    ap.add_argument("--project-mode", choices=sorted(PROJECT_MODES), help="Explicit governed mode override; otherwise evidence-only detection is used")
    ap.add_argument("--decisions", help="Optional governed JSON decisions for authority/supersession/conflicts/requirements/architecture/stack")
    ap.add_argument("--baseline-manifest", help="Optional immutable prior source-manifest.json used to detect authoritative source-hash drift")
    ap.add_argument("--no-semantic-extraction", action="store_true", help="Emergency/debug option: inventory only; production Blueprint workflow must not use this to claim Phase-2 extraction complete")
    args = ap.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"source does not exist: {source}")
    project_root = Path(args.project_root).expanduser().resolve()
    output_root = Path(args.output).expanduser().resolve() if args.output else project_root / ".ai-product-delivery" / "source-intake"
    output_root.mkdir(parents=True, exist_ok=True)

    baseline_path = Path(args.baseline_manifest).expanduser().resolve() if args.baseline_manifest else None
    output_manifest = (output_root / "source-manifest.json").resolve()
    if baseline_path is not None and baseline_path == output_manifest:
        raise ValueError("baseline manifest must be immutable and separate from the output source-manifest.json")

    staging = None
    if source.is_file() and zipfile.is_zipfile(source) and args.extract_zip:
        digest = sha256_file(source)[:12]
        staging = output_root / "staging" / f"{source.stem}-{digest}"
        staging.mkdir(parents=True, exist_ok=True)

    if source.is_dir():
        records, warnings = inspect_directory(source, output_root)
        source_kind = "DIRECTORY"
    elif source.is_file() and zipfile.is_zipfile(source):
        records, warnings = inspect_zip(source, staging)
        source_kind = "ZIP"
    elif source.is_file():
        records = [{
            "source_id": "", "path": source.name, "source_type": "FILE",
            "size": source.stat().st_size, "sha256": sha256_file(source),
            "authority": "UNCLASSIFIED", "status": "CURRENT_CANDIDATE",
            "supersedes": [], "superseded_by": [], "conflict_group": None,
        }]
        warnings = []
        source_kind = "FILE"
    else:
        raise SystemExit("unsupported source type")

    assign_ids(records)
    decisions = load_decisions(args.decisions)
    apply_source_decisions(records, _list(decisions, "source_decisions"))
    conflicts = build_conflict_groups(records)

    extracted = {
        "source_requirements": [], "observed_architecture": {}, "declared_architecture": {},
        "observed_stack": {}, "declared_stack": {}, "warnings": [], "documents_examined": [],
        "semantic_extraction_version": "DISABLED", "authority_boundary": "NO_EXTRACTION",
    }
    if not args.no_semantic_extraction:
        extracted = semantic_extract(source, records)
        warnings.extend(extracted.get("warnings", []))

    requirement_inputs = _merge_requirement_inputs(extracted.get("source_requirements", []), _list(decisions, "source_requirements"))
    requirements = normalize_requirements(requirement_inputs, records)
    project_mode = args.project_mode or decisions.get("project_mode") or detect_mode(records)
    if project_mode not in PROJECT_MODES:
        raise SystemExit(f"invalid governed project mode: {project_mode}")

    baseline_sources = load_baseline_sources(str(baseline_path) if baseline_path else None)
    source_drift = detect_source_hash_drift(baseline_sources, records)

    observed_architecture = merge_fact_objects(extracted.get("observed_architecture", {}), _object(decisions, "observed_architecture"))
    declared_architecture = merge_fact_objects(extracted.get("declared_architecture", {}), _object(decisions, "declared_architecture"))
    observed_stack = merge_fact_objects(extracted.get("observed_stack", {}), _object(decisions, "observed_stack"))
    declared_stack = merge_fact_objects(extracted.get("declared_stack", {}), _object(decisions, "declared_stack"))

    intake = {
        "schema_version": "1.2",
        "generated_at": utc_now(), "intent": args.intent,
        "source_kind": source_kind, "source_root": str(source), "project_mode": project_mode,
        "sources": records,
        "duplicate_groups": build_duplicate_groups(records),
        "version_candidate_groups": build_version_candidate_groups(records),
        "source_conflicts": conflicts, "source_drift": source_drift,
        "source_requirements": requirements,
        "observed_architecture": observed_architecture,
        "declared_architecture": declared_architecture,
        "approved_architecture": _object(decisions, "approved_architecture"),
        "observed_stack": observed_stack,
        "declared_stack": declared_stack,
        "approved_stack": _object(decisions, "approved_stack"),
        "semantic_extraction": {
            "version": extracted.get("semantic_extraction_version"),
            "documents_examined": extracted.get("documents_examined", []),
            "authority_boundary": extracted.get("authority_boundary"),
            "automatic_approval": False,
        },
        "assumptions": _list(decisions, "assumptions"),
        "unknowns": _list(decisions, "unknowns"),
        "role_gaps": _list(decisions, "role_gaps"),
        "human_decisions_required": _list(decisions, "human_decisions_required"),
        "warnings": warnings,
        "staging_root": str(staging) if staging else None,
    }

    atomic_json(output_root / "SOURCE-INTAKE.json", intake)
    atomic_json(output_root / "source-manifest.json", {
        "generated_at": intake["generated_at"], "sources": records,
        "duplicate_groups": intake["duplicate_groups"],
        "version_candidate_groups": intake["version_candidate_groups"],
        "source_drift": intake["source_drift"],
    })
    atomic_json(output_root / "source-conflicts.json", {"generated_at": intake["generated_at"], "conflicts": conflicts})
    write_summary(output_root / "SOURCE-INTAKE.md", intake)

    blocking = [c for c in conflicts if c.get("blocking")]
    status = "SOURCE_INTAKE_BLOCKED" if blocking or source_drift else "SOURCE_INTAKE_COMPLETE"
    print(json.dumps({
        "status": status, "output": str(output_root), "project_mode": intake["project_mode"],
        "sources": len(records), "source_requirements": len(requirements),
        "semantic_documents_examined": len(extracted.get("documents_examined", [])),
        "blocking_conflicts": len(blocking), "source_drift": len(source_drift),
    }, indent=2))
    if blocking or source_drift:
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"SOURCE_INTAKE_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
