#!/usr/bin/env python3
"""Build and validate the AI Product Delivery Blueprint Codex distribution."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "codex-distribution"
MANIFEST = ROOT / "CODEX-DISTRIBUTION.json"

SKILL = {
    "name": "ai-product-delivery-blueprint",
    "source_path": "codex-distribution/skills/ai-product-delivery-blueprint",
    "implicit_invocation": True,
}

SKILL_ITEMS = [
    "SKILL.md",
    "agents",
    "orchestration",
    "references",
    "schemas",
    "scripts",
    "templates",
    "README.md",
]

AGENT_FILES = [
    "vt_application_engineering.toml",
    "vt_data.toml",
    "vt_infrastructure_and_operations.toml",
    "vt_product_and_business.toml",
    "vt_quality.toml",
    "vt_release_and_support.toml",
    "vt_security_and_trust.toml",
    "vt_transaction_and_commerce.toml",
    "vt_user_experience.toml",
]

IGNORE_NAMES = {"__pycache__", ".pytest_cache"}
IGNORE_SUFFIXES = {".pyc", ".pyo", ".log"}


def ignore_runtime(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in IGNORE_NAMES or any(name.endswith(suffix) for suffix in IGNORE_SUFFIXES):
            ignored.add(name)
    return ignored


def copy_item(rel: str, dest_root: Path, target_rel: str | None = None) -> None:
    src = ROOT / rel
    if not src.exists():
        raise SystemExit(f"missing source artifact: {rel}")
    dst = dest_root / (target_rel if target_rel is not None else Path(rel).name)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, ignore=ignore_runtime)
    else:
        shutil.copy2(src, dst)


def frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        raise SystemExit(f"SKILL.md lacks frontmatter: {skill_md}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"malformed frontmatter: {skill_md}")
    match = re.search(r"(?mi)^name\s*:\s*['\"]?([^'\"\r\n]+)", parts[1])
    if not match:
        raise SystemExit(f"frontmatter lacks name: {skill_md}")
    return match.group(1).strip()


def toml_name(toml_path: Path) -> str:
    text = toml_path.read_text(encoding="utf-8-sig")
    match = re.search(r'(?m)^name\s*=\s*"([^"]+)"', text)
    if not match:
        raise SystemExit(f"custom agent lacks name: {toml_path}")
    return match.group(1).strip()


def manifest(agent_names: list[str]) -> dict:
    return {
        "schema_version": "1.0",
        "repository": "WilsonMisor/wed_dev_skill",
        "component": "ai-product-delivery-blueprint",
        "skills": [SKILL],
        "agents": [
            {"name": name, "source_path": f"codex-distribution/agents/{name}.toml"}
            for name in agent_names
        ],
    }


def build_tree(target: Path) -> dict:
    skill_dest = target / "skills" / SKILL["name"]
    for item in SKILL_ITEMS:
        copy_item(item, skill_dest)

    agent_dest = target / "agents"
    agent_dest.mkdir(parents=True, exist_ok=True)
    agent_names: list[str] = []
    for filename in AGENT_FILES:
        src_rel = f"templates/virtual-team/codex-agents/{filename}"
        src = ROOT / src_rel
        if not src.is_file():
            raise SystemExit(f"missing custom-agent template: {src_rel}")
        name = toml_name(src)
        agent_names.append(name)
        shutil.copy2(src, agent_dest / f"{name}.toml")

    data = manifest(agent_names)
    validate_distribution(target, data)
    return data


def validate_distribution(target: Path, data: dict) -> None:
    skill_path = target / "skills" / SKILL["name"]
    actual_skill = frontmatter_name(skill_path / "SKILL.md")
    if actual_skill != SKILL["name"]:
        raise SystemExit(f"skill name mismatch: manifest={SKILL['name']}, SKILL.md={actual_skill}")

    seen_agents: set[str] = set()
    for item in data["agents"]:
        name = item["name"]
        if name in seen_agents:
            raise SystemExit(f"duplicate custom-agent name: {name}")
        seen_agents.add(name)
        rel = Path(item["source_path"]).relative_to("codex-distribution")
        path = target / rel
        if not path.is_file():
            raise SystemExit(f"declared custom-agent source missing: {item['source_path']}")
        actual = toml_name(path)
        if actual != name:
            raise SystemExit(f"custom-agent name mismatch: manifest={name}, TOML={actual}")


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    files: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        files[path.relative_to(root).as_posix()] = file_hash(path)
    return files


def compare_tree(expected_root: Path) -> list[str]:
    expected = snapshot(expected_root)
    current = snapshot(DIST)
    diffs: list[str] = []
    for rel in sorted(set(expected) | set(current)):
        if rel not in current:
            diffs.append(f"missing: {rel}")
        elif rel not in expected:
            diffs.append(f"extra: {rel}")
        elif current[rel] != expected[rel]:
            diffs.append(f"changed: {rel}")
    return diffs


def write_manifest(data: dict) -> str:
    return json.dumps(data, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated distribution is stale")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="blueprint-codex-distribution-") as td:
        expected = Path(td) / "codex-distribution"
        data = build_tree(expected)
        manifest_text = write_manifest(data)
        if args.check:
            diffs = compare_tree(expected)
            if not MANIFEST.exists() or MANIFEST.read_text(encoding="utf-8-sig") != manifest_text:
                diffs.insert(0, "changed: CODEX-DISTRIBUTION.json")
            if diffs:
                print("Blueprint Codex distribution is stale:")
                for diff in diffs[:50]:
                    print(f"- {diff}")
                return 1
            print("Blueprint Codex distribution is fresh")
            return 0

        if DIST.exists():
            shutil.rmtree(DIST)
        shutil.copytree(expected, DIST)
        MANIFEST.write_text(manifest_text, encoding="utf-8")
        print(f"wrote {MANIFEST.relative_to(ROOT)}")
        print(f"wrote {DIST.relative_to(ROOT)}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
