#!/usr/bin/env bash
set -euo pipefail
BLUEPRINT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SUITE_ROOT=$(cd "$BLUEPRINT_ROOT/.." && pwd)
PREOS_ROOT="${PREOS_REPO:-$SUITE_ROOT/PREOS}"
GSTACK_ROOT="${GSTACK_REPO:-$SUITE_ROOT/gstack}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
AGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}"
SKILL_ROOT="${CODEX_SKILLS_HOME:-$AGENTS_HOME/skills}"
AGENT_ROOT="$CODEX_HOME/agents"
SKIP_GSTACK_SETUP=0
for arg in "$@"; do
  case "$arg" in
    --skip-gstack-setup) SKIP_GSTACK_SETUP=1 ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 2; }
}
run_checked() {
  label="$1"
  shift
  printf '==> %s\n' "$label"
  "$@"
}

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
agent_count=$(find "$AGENT_ROOT" -maxdepth 1 -name 'vt_*.toml' -type f | wc -l)
[ "$agent_count" -ge 9 ] || { echo 'Virtual Team agent metadata is incomplete' >&2; exit 3; }
printf 'Suite install health: PASS\n'
printf 'Blueprint %s\n' "$(git -C "$BLUEPRINT_ROOT" rev-parse --short HEAD)"
printf 'PREOS %s\n' "$(git -C "$PREOS_ROOT" rev-parse --short HEAD)"
printf 'gstack %s\n' "$(git -C "$GSTACK_ROOT" rev-parse --short HEAD)"
printf 'Skills: %s\n' "$SKILL_ROOT"
printf 'Agents: %s\n' "$AGENT_ROOT"
