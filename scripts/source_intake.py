#!/usr/bin/env python3
"""Deterministic, non-executing source intake helper for the Blueprint."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
from datetime import datetime, timezone
import zipfile

CODE_EXTENSIONS = {
    ".php", ".js", ".jsx", ".ts", ".tsx", ".py", ".java", ".kt", ".kts",
    ".swift", ".dart", ".go", ".rs", ".rb", ".cs", ".cpp", ".cc", ".c",
    ".h", ".hpp", ".vue", ".svelte", ".sql", ".sh", ".ps1",
}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".idea", ".vscode"}


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


def atomic_json(path: Path, obj) -> None:
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
            data = zf.read(info)
            record = {
                "source_id": "",
                "path": str(rel),
                "source_type": "ZIP_MEMBER",
                "size": len(data),
                "sha256": sha256_bytes(data),
                "authority": "UNCLASSIFIED",
                "status": "CURRENT_CANDIDATE",
            }
            records.append(record)
            if extract_root is not None:
                target = (extract_root / Path(*rel.parts)).resolve()
                base = extract_root.resolve()
                if target != base and base not in target.parents:
                    raise ValueError(f"ZIP extraction escaped staging root: {info.filename}")
                target.parent.mkdir(parents=True, exist_ok=True)
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
            out.append({"duplicate_group": f"DUP-{n:04d}", "sha256": digest, "paths": paths})
            n += 1
    return out


def assign_ids(records: list[dict]) -> None:
    for idx, record in enumerate(records, 1):
        record["source_id"] = f"SRC-{idx:04d}"


def write_summary(path: Path, intake: dict) -> None:
    lines = [
        "# Source Intake Summary",
        "",
        f"Generated: {intake['generated_at']}",
        f"Project mode: **{intake['project_mode']}**",
        f"Sources inventoried: **{len(intake['sources'])}**",
        f"Exact duplicate groups: **{len(intake['duplicate_groups'])}**",
        "",
        "## Authority",
        "",
        "All sources begin as `UNCLASSIFIED`. A filename, timestamp, or existing implementation does not establish authority. Resolve authority through `orchestration/source-intake.md`.",
        "",
        "## Warnings",
        "",
    ]
    warnings = intake.get("warnings", [])
    lines += [f"- {w}" for w in warnings] if warnings else ["- None."]
    lines += [
        "",
        "## Next governed step",
        "",
        "Resolve source authority/conflicts and extract source requirements before Blueprint discovery. PREOS Project Contract creation occurs only after approved PRD and Project Classification.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Safely inventory project source material without executing it.")
    ap.add_argument("source", help="Directory, repository, file, or ZIP archive to inspect")
    ap.add_argument("--project-root", default=".", help="Application repository root (default: current directory)")
    ap.add_argument("--output", help="Output directory (default: <project-root>/.ai-product-delivery/source-intake)")
    ap.add_argument("--extract-zip", action="store_true", help="Safely extract ZIP members into derived staging under the output directory")
    ap.add_argument("--intent", default="", help="Optional short human intent statement; recorded separately from documentary truth")
    args = ap.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"source does not exist: {source}")
    project_root = Path(args.project_root).expanduser().resolve()
    output_root = Path(args.output).expanduser().resolve() if args.output else project_root / ".ai-product-delivery" / "source-intake"
    output_root.mkdir(parents=True, exist_ok=True)

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
            "source_id": "",
            "path": source.name,
            "source_type": "FILE",
            "size": source.stat().st_size,
            "sha256": sha256_file(source),
            "authority": "UNCLASSIFIED",
            "status": "CURRENT_CANDIDATE",
        }]
        warnings = []
        source_kind = "FILE"
    else:
        raise SystemExit("unsupported source type")

    assign_ids(records)
    intake = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "intent": args.intent,
        "source_kind": source_kind,
        "source_root": str(source),
        "project_mode": detect_mode(records),
        "sources": records,
        "duplicate_groups": build_duplicate_groups(records),
        "source_conflicts": [],
        "source_requirements": [],
        "observed_architecture": {},
        "declared_architecture": {},
        "approved_architecture": {},
        "observed_stack": {},
        "declared_stack": {},
        "approved_stack": {},
        "assumptions": [],
        "unknowns": [],
        "role_gaps": [],
        "human_decisions_required": [],
        "warnings": warnings,
        "staging_root": str(staging) if staging else None,
    }

    atomic_json(output_root / "SOURCE-INTAKE.json", intake)
    atomic_json(output_root / "source-manifest.json", {"generated_at": intake["generated_at"], "sources": records, "duplicate_groups": intake["duplicate_groups"]})
    atomic_json(output_root / "source-conflicts.json", {"generated_at": intake["generated_at"], "conflicts": []})
    write_summary(output_root / "SOURCE-INTAKE.md", intake)
    print(json.dumps({"status": "SOURCE_INTAKE_COMPLETE", "output": str(output_root), "project_mode": intake["project_mode"], "sources": len(records)}, indent=2))


if __name__ == "__main__":
    main()
