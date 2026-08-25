#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "references" / "INDEX.md"
SKILL = ROOT / "SKILL.md"
OPENAI = ROOT / "agents" / "openai.yaml"
LEGACY_SKILL_SNAPSHOT = ROOT / "references" / "wordpress" / "legacy-ai-web-delivery-blueprint.md"

LEGACY_WORDPRESS = [
    "references/ai-delivery-artifact-templates.md",
    "references/ai-ui-ux-design-tool-prompt-workflow.md",
    "references/ai-visual-antipatterns-and-audit.md",
    "references/content-resilience-and-wordpress-visual-qa.md",
    "references/conversion-seo-security-applicability-matrix.md",
    "references/end-to-end-ai-assisted-web-development-blueprint.txt",
    "references/generic-ai-seo-compliance-prompt-for-any-website-architecture.txt",
    "references/human-design-governance.md",
    "references/human-design-scorecard.md",
    "references/seo-crawl-compliance-workflow.md",
    "references/ux-laws-and-ui-dos-donts.md",
    "references/wordpress-ai-delivery-flowchart.md",
    "references/wordpress-cybersecurity-build-workflow.md",
    "references/workplace-ux-ui-design-and-wireframing-framework.txt",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def manifest_paths() -> list[str]:
    if not INDEX.exists():
        fail("references/INDEX.md is missing")
    text = INDEX.read_text(encoding="utf-8")
    candidates = re.findall(r"`([^`]+)`", text)
    paths = []
    for item in candidates:
        if item.endswith((".md", ".txt", ".yaml")) and not item.startswith("http"):
            paths.append(item)
    return sorted(set(paths))


def validate_manifest() -> None:
    paths = manifest_paths()
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        fail("manifest paths missing:\n" + "\n".join(missing))
    if not LEGACY_SKILL_SNAPSHOT.is_file():
        fail("legacy WordPress SKILL.md snapshot is missing")
    print(f"PASS: manifest paths exist, {len(paths)} files checked")


def validate_skill_identity() -> None:
    skill_text = SKILL.read_text(encoding="utf-8")
    agent_text = OPENAI.read_text(encoding="utf-8")
    required_skill_tokens = [
        "name: ai-product-delivery-blueprint",
        "orchestration/project-classification.md",
        "orchestration/profile-routing.md",
        "orchestration/gstack-routing.md",
        "orchestration/cross-platform-routing.md",
        "## WordPress preservation rule",
        "references/saas/saas-lifecycle.md",
        "references/mobile/mobile-lifecycle.md",
    ]
    for token in required_skill_tokens:
        if token not in skill_text:
            fail(f"SKILL.md missing required routing token: {token}")
    if "AI Product Delivery Blueprint" not in agent_text:
        fail("agents/openai.yaml has not been upgraded")
    print("PASS: skill identity and routing anchors are present")


def validate_legacy_wordpress() -> None:
    missing = [path for path in LEGACY_WORDPRESS if not (ROOT / path).is_file()]
    if missing:
        fail("legacy WordPress references missing:\n" + "\n".join(missing))

    result = subprocess.run(
        ["git", "rev-parse", "--verify", "origin/main"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        print("WARN: origin/main is unavailable, legacy content comparison skipped")
        return

    diff = subprocess.run(
        ["git", "diff", "--exit-code", "origin/main", "--", *LEGACY_WORDPRESS],
        cwd=ROOT,
    )
    if diff.returncode != 0:
        fail("one or more preserved WordPress reference files differ from origin/main")

    original_skill = subprocess.run(
        ["git", "show", "origin/main:SKILL.md"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    if LEGACY_SKILL_SNAPSHOT.read_bytes() != original_skill:
        fail("legacy WordPress skill snapshot differs from origin/main:SKILL.md")

    print("PASS: original WordPress references and legacy skill text are preserved")


def main() -> None:
    validate_manifest()
    validate_skill_identity()
    validate_legacy_wordpress()
    print("PASS: AI Product Delivery Blueprint validation complete")


if __name__ == "__main__":
    main()
