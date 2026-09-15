#!/usr/bin/env bash
set -euo pipefail
BLUEPRINT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SUITE_ROOT=$(cd "$BLUEPRINT_ROOT/.." && pwd)
PREOS_ROOT="${PREOS_REPO:-$SUITE_ROOT/PREOS}"
GSTACK_ROOT="${GSTACK_REPO:-$SUITE_ROOT/gstack}"
SUITE_LOCK="$SUITE_ROOT/SUITE-LOCK.json"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
AGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}"
SKILL_ROOT="${CODEX_SKILLS_HOME:-$AGENTS_HOME/skills}"
AGENT_ROOT="$CODEX_HOME/agents"
MODE=install
SKIP_GSTACK_SETUP=0
SKIP_INSTALLED=0
ALLOW_UPDATE=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --mode) MODE="$2"; shift 2 ;;
    --preos) PREOS_ROOT="$2"; shift 2 ;;
    --gstack) GSTACK_ROOT="$2"; shift 2 ;;
    --suite-lock) SUITE_LOCK="$2"; shift 2 ;;
    --skip-gstack-setup) SKIP_GSTACK_SETUP=1; shift ;;
    --skip-installed-skill-check) SKIP_INSTALLED=1; shift ;;
    --allow-update) ALLOW_UPDATE=1; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

case "$MODE" in install|verify|repair|update|uninstall) ;; *) echo "Invalid --mode: $MODE" >&2; exit 2 ;; esac
require_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 2; }; }
run_checked() { label="$1"; shift; printf '==> %s\n' "$label"; "$@"; }
run_doctor() {
  args=("--preos" "$PREOS_ROOT" "--gstack" "$GSTACK_ROOT" "--suite-lock" "$SUITE_LOCK")
  [ "$SKIP_INSTALLED" -eq 1 ] && args+=("--skip-installed-skill-check")
  "$BLUEPRINT_ROOT/scripts/suite-doctor.sh" "${args[@]}"
}

if [ "$MODE" = verify ]; then
  run_doctor
  exit 0
fi
if [ "$MODE" = update ] && [ "$ALLOW_UPDATE" -ne 1 ]; then
  echo 'Mode update requires --allow-update so suite drift cannot happen implicitly.' >&2
  exit 2
fi
if [ "$MODE" = uninstall ]; then
  [ "$ALLOW_UPDATE" -eq 1 ] || { echo 'Mode uninstall requires --allow-update before installed files are removed.' >&2; exit 2; }
  for skill in ai-product-delivery-blueprint preos preos-risk-model preos-production-plan gstack; do
    target="$SKILL_ROOT/$skill"
    case "$(cd "$(dirname "$target")" && pwd)/$(basename "$target")" in
      "$(cd "$SKILL_ROOT" && pwd)"/*) [ -e "$target" ] && rm -rf "$target" ;;
      *) echo "Refusing to remove path outside skill root: $target" >&2; exit 2 ;;
    esac
  done
  [ -d "$AGENT_ROOT" ] && find "$AGENT_ROOT" -maxdepth 1 -name 'vt_*.toml' -type f -delete
  printf 'Suite uninstall: PASS\n'
  exit 0
fi

require_cmd git
require_cmd python
require_cmd bun
[ -d "$BLUEPRINT_ROOT/.git" ] || { echo 'Blueprint repository missing .git' >&2; exit 2; }
[ -d "$PREOS_ROOT/.git" ] || { echo 'PREOS repository missing .git' >&2; exit 2; }
[ -d "$GSTACK_ROOT/.git" ] || { echo 'gstack repository missing .git' >&2; exit 2; }

run_checked 'verify Blueprint repository' git -C "$BLUEPRINT_ROOT" rev-parse HEAD >/dev/null
run_checked 'verify PREOS repository' git -C "$PREOS_ROOT" rev-parse HEAD >/dev/null
run_checked 'verify gstack repository' git -C "$GSTACK_ROOT" rev-parse HEAD >/dev/null
run_checked 'validate Blueprint' python "$BLUEPRINT_ROOT/scripts/validate_blueprint.py"
run_checked 'validate Blueprint source semantics' python "$BLUEPRINT_ROOT/scripts/validate_source_semantics.py"
PYTHONPATH="$PREOS_ROOT/scripts" run_checked 'validate PREOS' python "$PREOS_ROOT/scripts/validate-preos.py"
PYTHONPATH="$PREOS_ROOT/scripts" run_checked 'validate PREOS PAS v2 remediation artifacts' python "$PREOS_ROOT/scripts/validate-pasv2-remediation-artifacts.py"
run_checked 'validate gstack PREOS integration' python "$GSTACK_ROOT/scripts/validate-preos-integration.py"
run_checked 'validate gstack Codex contract applicability' python "$GSTACK_ROOT/scripts/validate-codex-project-contract-applicability.py"
run_checked 'validate three-repo acceptance' python "$GSTACK_ROOT/scripts/validate-three-repo-acceptance.py" --blueprint "$BLUEPRINT_ROOT" --preos "$PREOS_ROOT" --gstack "$GSTACK_ROOT"
run_checked 'install Blueprint for Codex' "$BLUEPRINT_ROOT/scripts/install-codex.sh"
run_checked 'install PREOS for Codex' "$PREOS_ROOT/scripts/install-codex.sh"
if [ "$SKIP_GSTACK_SETUP" -eq 0 ]; then
  [ -x "$GSTACK_ROOT/setup" ] || { echo 'gstack setup script is missing or not executable' >&2; exit 2; }
  run_checked 'install gstack for Codex with namespaced prefix' "$GSTACK_ROOT/setup" --host codex --prefix
fi
for skill in ai-product-delivery-blueprint preos preos-risk-model preos-production-plan gstack; do
  [ -f "$SKILL_ROOT/$skill/SKILL.md" ] || { echo "Installed skill missing SKILL.md: $SKILL_ROOT/$skill" >&2; exit 3; }
done
agent_count=$(find "$AGENT_ROOT" -maxdepth 1 -name 'vt_*.toml' -type f 2>/dev/null | wc -l)
[ "$agent_count" -ge 9 ] || { echo 'Virtual Team agent metadata is incomplete' >&2; exit 3; }
run_doctor
printf 'Suite %s health: PASS\n' "$MODE"
printf 'Blueprint %s\n' "$(git -C "$BLUEPRINT_ROOT" rev-parse --short HEAD)"
printf 'PREOS %s\n' "$(git -C "$PREOS_ROOT" rev-parse --short HEAD)"
printf 'gstack %s\n' "$(git -C "$GSTACK_ROOT" rev-parse --short HEAD)"
printf 'Skills: %s\n' "$SKILL_ROOT"
printf 'Agents: %s\n' "$AGENT_ROOT"
