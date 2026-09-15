#!/usr/bin/env bash
set -euo pipefail
BLUEPRINT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SUITE_ROOT=$(cd "$BLUEPRINT_ROOT/.." && pwd)
PREOS_ROOT="${PREOS_REPO:-$SUITE_ROOT/PREOS}"
GSTACK_ROOT="${GSTACK_REPO:-$SUITE_ROOT/gstack}"
SUITE_LOCK="$SUITE_ROOT/SUITE-LOCK.json"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
AGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}"
SKILL_ROOT="${CODEX_SKILLS_HOME:-$AGENTS_HOME/skills}"
SKIP_INSTALLED=0
SKIP_GSTACK=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --preos) PREOS_ROOT="$2"; shift 2 ;;
    --gstack) GSTACK_ROOT="$2"; shift 2 ;;
    --suite-lock) SUITE_LOCK="$2"; shift 2 ;;
    --skip-installed-skill-check) SKIP_INSTALLED=1; shift ;;
    --skip-gstack-validation) SKIP_GSTACK=1; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

require_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 2; }; }
run_checked() { label="$1"; shift; printf '==> %s\n' "$label"; "$@"; }
head_of() { git -C "$1" rev-parse HEAD; }

require_cmd git
require_cmd python
[ -d "$BLUEPRINT_ROOT/.git" ] || { echo 'Blueprint repository missing .git' >&2; exit 2; }
[ -d "$PREOS_ROOT/.git" ] || { echo 'PREOS repository missing .git' >&2; exit 2; }
[ -d "$GSTACK_ROOT/.git" ] || { echo 'gstack repository missing .git' >&2; exit 2; }
run_checked 'verify Blueprint repository' git -C "$BLUEPRINT_ROOT" rev-parse HEAD >/dev/null
run_checked 'verify PREOS repository' git -C "$PREOS_ROOT" rev-parse HEAD >/dev/null
run_checked 'verify gstack repository' git -C "$GSTACK_ROOT" rev-parse HEAD >/dev/null

if [ -f "$SUITE_LOCK" ]; then
  python - "$SUITE_LOCK" "$SUITE_ROOT" <<'PY'
import json, pathlib, subprocess, sys
lock = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
root = pathlib.Path(sys.argv[2])
for component in lock.get('components', []):
    repo = root / component['path']
    actual = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    expected = component.get('commit')
    if expected and actual != expected:
        raise SystemExit(f"Suite lock drift for {component['name']}: expected {expected}, got {actual}")
PY
  printf 'Suite lock: PASS %s\n' "$SUITE_LOCK"
else
  printf 'Suite lock: NOT FOUND %s\n' "$SUITE_LOCK"
fi

run_checked 'validate Blueprint' python "$BLUEPRINT_ROOT/scripts/validate_blueprint.py"
run_checked 'validate Blueprint source semantics' python "$BLUEPRINT_ROOT/scripts/validate_source_semantics.py"
PYTHONPATH="$PREOS_ROOT/scripts" run_checked 'validate PREOS' python "$PREOS_ROOT/scripts/validate-preos.py"
PYTHONPATH="$PREOS_ROOT/scripts" run_checked 'validate PREOS PAS v2 remediation artifacts' python "$PREOS_ROOT/scripts/validate-pasv2-remediation-artifacts.py"

if [ "$SKIP_GSTACK" -eq 0 ]; then
  run_checked 'validate gstack PREOS integration' python "$GSTACK_ROOT/scripts/validate-preos-integration.py"
  run_checked 'validate gstack Codex contract applicability' python "$GSTACK_ROOT/scripts/validate-codex-project-contract-applicability.py"
  run_checked 'validate three-repo acceptance' python "$GSTACK_ROOT/scripts/validate-three-repo-acceptance.py" --blueprint "$BLUEPRINT_ROOT" --preos "$PREOS_ROOT" --gstack "$GSTACK_ROOT"
else
  printf 'gstack bounded validators: SKIPPED by caller\n'
fi

if [ "$SKIP_INSTALLED" -eq 0 ]; then
  for skill in ai-product-delivery-blueprint preos preos-risk-model preos-production-plan gstack; do
    [ -f "$SKILL_ROOT/$skill/SKILL.md" ] || { echo "Installed skill missing SKILL.md: $SKILL_ROOT/$skill" >&2; exit 3; }
  done
  agent_count=$(find "$CODEX_HOME/agents" -maxdepth 1 -name 'vt_*.toml' -type f 2>/dev/null | wc -l)
  [ "$agent_count" -ge 9 ] || { echo 'Virtual Team agent metadata is incomplete' >&2; exit 3; }
  printf 'Installed skills: PASS %s\n' "$SKILL_ROOT"
else
  printf 'Installed skills: SKIPPED by caller\n'
fi

printf 'Suite doctor: PASS\n'
printf 'Blueprint %s\n' "$(head_of "$BLUEPRINT_ROOT")"
printf 'PREOS %s\n' "$(head_of "$PREOS_ROOT")"
printf 'gstack %s\n' "$(head_of "$GSTACK_ROOT")"
