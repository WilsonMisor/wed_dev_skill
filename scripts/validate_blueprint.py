#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "references" / "INDEX.md"
SKILL = ROOT / "SKILL.md"
OPENAI = ROOT / "agents" / "openai.yaml"
RECOMMENDATION_COVERAGE = ROOT / "orchestration" / "recommendation-coverage.md"
ARCHITECTURE_COVERAGE = ROOT / "orchestration" / "coverage-matrix.md"
GSTACK_ROUTING = ROOT / "orchestration" / "gstack-routing.md"
CODEX_ROUTING = ROOT / "orchestration" / "codex-routing.md"
PREOS_ROUTING = ROOT / "orchestration" / "preos-routing.md"
PREOS_INTEGRATION = ROOT / "references" / "production-assurance" / "preos-integration.md"
AI_TASK_PACKET_GUIDE = ROOT / "references" / "core" / "ai-task-packets.md"
AI_TASK_PACKET_TEMPLATE = ROOT / "templates" / "ai-task-packet.md"
LEGACY_SKILL_SNAPSHOT = ROOT / "references" / "wordpress" / "legacy-ai-web-delivery-blueprint.md"
SOURCE_INTAKE = ROOT / "orchestration" / "source-intake.md"
SESSION_CONTINUITY = ROOT / "references" / "core" / "session-continuity.md"
SOURCE_INTAKE_SCRIPT = ROOT / "scripts" / "source_intake.py"
SOURCE_INTAKE_TEMPLATE = ROOT / "templates" / "source-intake-record.json"
UPGRADE_RECONCILIATION = ROOT / "orchestration" / "upgrade-reconciliation.md"

LEGACY_BASE_COMMIT = "aee7f8f7ba8e9e6d4af8dc681892e51bef411a7b"
LEGACY_SKILL_BLOB = "74698dfa2c6fb631af5c1399cefaaaee9f0548c2"

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
    for path in [SOURCE_INTAKE, SESSION_CONTINUITY, SOURCE_INTAKE_SCRIPT, SOURCE_INTAKE_TEMPLATE, UPGRADE_RECONCILIATION]:
        if not path.is_file():
            fail(f"upgrade governed file missing: {path.relative_to(ROOT)}")
    if not LEGACY_SKILL_SNAPSHOT.is_file():
        fail("legacy WordPress SKILL.md snapshot is missing")
    print(f"PASS: manifest paths exist, {len(paths)} indexed files checked; source-intake/continuity additions present")


def validate_skill_identity() -> None:
    skill_text = SKILL.read_text(encoding="utf-8")
    agent_text = OPENAI.read_text(encoding="utf-8")
    required_skill_tokens = [
        "name: ai-product-delivery-blueprint",
        "orchestration/project-classification.md",
        "orchestration/profile-routing.md",
        "orchestration/preos-routing.md",
        "orchestration/gstack-routing.md",
        "orchestration/cross-platform-routing.md",
        "references/production-assurance/preos-integration.md",
        "## PREOS production assurance",
        "UNKNOWN never silently becomes GREEN",
        "PREOS_STATE_ROOT",
        ".ai-product-delivery/preos/",
        "## WordPress preservation rule",
        "references/saas/saas-lifecycle.md",
        "references/mobile/mobile-lifecycle.md",
    ]
    for token in required_skill_tokens:
        if token not in skill_text:
            fail(f"SKILL.md missing required routing token: {token}")
    if "AI Product Delivery Blueprint" not in agent_text:
        fail("agents/openai.yaml has not been upgraded")
    print("PASS: skill identity, profile routing, and PREOS assurance anchors are present")


def validate_source_intake_and_continuity() -> None:
    intake = SOURCE_INTAKE.read_text(encoding="utf-8")
    continuity = SESSION_CONTINUITY.read_text(encoding="utf-8")
    codex = CODEX_ROUTING.read_text(encoding="utf-8")
    lifecycle = (ROOT / "references" / "core" / "lifecycle.md").read_text(encoding="utf-8")
    reconciliation = UPGRADE_RECONCILIATION.read_text(encoding="utf-8")
    for token in ["SHA-256", "SOURCE CONFLICT", "UNCLASSIFIED", "safe", ".ai-product-delivery/source-intake/", "PREOS project-init"]:
        if token not in intake:
            fail(f"source-intake contract missing semantic anchor: {token}")
    for token in ["Conversation memory is never authoritative execution state", "PREOS_STATE_ROOT", "RECOVERY_CONFLICT", "first unverified action", "gstack semantic context"]:
        if token not in continuity:
            fail(f"session-continuity contract missing semantic anchor: {token}")
    for token in ["SAFE_TO_RESUME", "RECOVERY_CONFLICT", "gstack context restore"]:
        if token not in codex:
            fail(f"Codex recovery routing missing anchor: {token}")
    for token in ["Governed source intake", "AI-session interruption rule", "source-intake.md"]:
        if token not in lifecycle:
            fail(f"lifecycle missing source/continuity anchor: {token}")
    for token in ["one canonical Project Contract", "one canonical 75-control baseline", "Conversation memory is never authoritative execution state"]:
        if token not in reconciliation:
            fail(f"upgrade reconciliation missing invariant: {token}")
    print("PASS: source intake, authority, AI-session continuity and recovery routing are explicit")


def validate_recommendation_coverage() -> None:
    required_files = [
        RECOMMENDATION_COVERAGE,
        ARCHITECTURE_COVERAGE,
        GSTACK_ROUTING,
        CODEX_ROUTING,
        PREOS_ROUTING,
        PREOS_INTEGRATION,
        AI_TASK_PACKET_GUIDE,
        AI_TASK_PACKET_TEMPLATE,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    if missing:
        fail("recommendation coverage files missing:\n" + "\n".join(missing))

    ledger_text = RECOMMENDATION_COVERAGE.read_text(encoding="utf-8")
    for number in range(1, 39):
        token = f"| R{number:02d} |"
        if token not in ledger_text:
            fail(f"recommendation coverage ledger missing {token}")

    required_ledger_tokens = [
        "ai-product-delivery-blueprint",
        "WordPress as a specialised web profile",
        "tenant isolation as a hard security boundary",
        "canonical cross platform",
        "bounded AI Task Packets",
        "exact namespaced commands",
        "separate responsibility layers",
        "application repository the execution surface",
        "branches, worktrees, forks, pull requests, CI, and review",
        "byte identically",
        "PREOS as a production-assurance overlay",
        "Project Contract",
        "Deferred Complexity Registry",
        "UNKNOWN never silently becomes GREEN",
        "PREOS_STATE_ROOT",
        "PREOS production learning",
    ]
    for token in required_ledger_tokens:
        if token not in ledger_text:
            fail(f"recommendation coverage ledger missing semantic anchor: {token}")

    gstack_text = GSTACK_ROUTING.read_text(encoding="utf-8")
    required_gstack_tokens = [
        "Keep the blueprint, gstack, Codex, and the application repository as separate responsibility layers.",
        "Do not merge the blueprint repository, gstack repository, and application repository merely to make them cooperate.",
        "gstack-plan-ceo-review",
        "gstack-plan-eng-review",
        "gstack-cso",
        "gstack-review",
        "gstack-investigate",
        "gstack-qa",
        "gstack-ship",
        "gstack-retro",
    ]
    for token in required_gstack_tokens:
        if token not in gstack_text:
            fail(f"gstack routing missing recommendation anchor: {token}")

    codex_text = CODEX_ROUTING.read_text(encoding="utf-8")
    required_codex_tokens = [
        "The application repository is the execution surface",
        "Do not merge or vendor the blueprint repository or gstack repository into an application repository merely to make the layers cooperate.",
        "isolated branch, worktree, or fork",
        "pull request or equivalent review boundary",
        "Preserve naming, folder, schema, API, and environment conventions",
        "smallest coherent change",
    ]
    for token in required_codex_tokens:
        if token not in codex_text:
            fail(f"Codex routing missing recommendation anchor: {token}")

    preos_text = PREOS_ROUTING.read_text(encoding="utf-8")
    required_preos_tokens = [
        "PREOS is the Production Risk, Economics, and Evolution Operating System",
        "inactive",
        "lightweight",
        "standard",
        "high-assurance",
        "Stage 0: Prototype",
        "preos-project-init",
        "preos-risk-model",
        "preos-architecture-economics",
        "preos-production-plan",
        "preos-production-implement",
        "preos-production-learn",
        "G0 Source / Project Contract",
        "G11 Evidence / Authority",
        "UNKNOWN` never silently becomes `GREEN",
        ".ai-product-delivery/",
        "PREOS_STATE_ROOT",
        "Deferred Complexity Registry",
    ]
    for token in required_preos_tokens:
        if token not in preos_text:
            fail(f"PREOS routing missing semantic anchor: {token}")

    integration_text = PREOS_INTEGRATION.read_text(encoding="utf-8")
    for token in [
        "WilsonMisor/PREOS",
        "does not silently replace",
        "canonical PREOS source corpus",
        "one implementation work unit",
        "PREOS runtime/recovery state belongs under `PREOS_STATE_ROOT`",
        "cannot authorize production by itself",
    ]:
        if token not in integration_text:
            fail(f"PREOS integration contract missing semantic anchor: {token}")

    packet_text = AI_TASK_PACKET_GUIDE.read_text(encoding="utf-8") + "\n" + AI_TASK_PACKET_TEMPLATE.read_text(encoding="utf-8")
    for token in ["PREOS risk IDs", "control IDs", "G0-G11", "evidence", "failure tests", "monitoring", "reconciliation", "Deferred Complexity", "Change impact"]:
        if token not in packet_text:
            fail(f"AI Task Packet PREOS integration missing anchor: {token}")

    coverage_text = ARCHITECTURE_COVERAGE.read_text(encoding="utf-8")
    for token in ["Recommendation coverage checks", "PREOS as a production-assurance overlay", "PREOS_STATE_ROOT", "production-learning"]:
        if token not in coverage_text:
            fail(f"architecture coverage matrix missing PREOS semantic check: {token}")

    print("PASS: recommendation coverage, PREOS assurance integration, tool boundaries, and source control safeguards are present")


def validate_legacy_wordpress() -> None:
    missing = [path for path in LEGACY_WORDPRESS if not (ROOT / path).is_file()]
    if missing:
        fail("legacy WordPress references missing:\n" + "\n".join(missing))

    baseline = subprocess.run(["git", "cat-file", "-e", f"{LEGACY_BASE_COMMIT}^{{commit}}"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if baseline.returncode != 0:
        fail("immutable legacy WordPress baseline commit is unavailable; fetch full repository history before validating preservation")

    diff = subprocess.run(["git", "diff", "--exit-code", LEGACY_BASE_COMMIT, "--", *LEGACY_WORDPRESS], cwd=ROOT)
    if diff.returncode != 0:
        fail("one or more preserved WordPress reference files differ from the immutable pre-upgrade baseline")

    original_skill = subprocess.run(["git", "show", f"{LEGACY_BASE_COMMIT}:SKILL.md"], cwd=ROOT, check=True, stdout=subprocess.PIPE).stdout
    if LEGACY_SKILL_SNAPSHOT.read_bytes() != original_skill:
        fail("legacy WordPress skill snapshot differs from immutable pre-upgrade SKILL.md")

    legacy_blob = subprocess.run(["git", "hash-object", str(LEGACY_SKILL_SNAPSHOT)], cwd=ROOT, check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
    if legacy_blob != LEGACY_SKILL_BLOB:
        fail(f"legacy WordPress skill snapshot Git blob changed: expected {LEGACY_SKILL_BLOB}, got {legacy_blob}")

    print("PASS: original WordPress references and legacy skill text are preserved against immutable pre-upgrade baseline")


def main() -> None:
    validate_manifest()
    validate_skill_identity()
    validate_source_intake_and_continuity()
    validate_recommendation_coverage()
    validate_legacy_wordpress()
    print("PASS: AI Product Delivery Blueprint + PREOS integration validation complete")


if __name__ == "__main__":
    main()
