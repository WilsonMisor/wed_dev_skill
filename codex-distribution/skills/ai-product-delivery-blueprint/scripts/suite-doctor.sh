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
require_cmd git
require_cmd python
[ -f "$SUITE_LOCK" ] || { echo "Suite lock missing: $SUITE_LOCK" >&2; exit 2; }
python - "$SUITE_LOCK" "$SUITE_ROOT" <<'PY'
import json, pathlib, subprocess, sys
lock = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
required = [
'suite_version','preos_version','preos_commit','blueprint_version','blueprint_commit',
'gstack_version','gstack_commit','integration_contract_version','risk_catalogue_version',
'risk_schema_version','readiness_framework_mapping_version','gate_schema_version',
'virtual_team_contract_version','tested_codex_host_profile','os_runtime_profile'
]
for field in required:
    if not lock.get(field):
        raise SystemExit(f'Suite lock missing {field}')
root = pathlib.Path(sys.argv[2])
for component in lock.get('components', []):
    repo = root / component['path']
    actual = subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    if component.get('commit') and actual != component['commit']:
        raise SystemExit(f"Suite lock drift for {component['name']}: expected {component['commit']}, got {actual}")
PY
printf 'Suite lock: PASS %s\n' "$SUITE_LOCK"
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
  python - "$SUITE_LOCK" "$SKILL_ROOT" "$CODEX_HOME" <<'PY'
import json, pathlib, sys
lock=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
skill_root=pathlib.Path(sys.argv[2])
for skill in lock.get('owned_skill_ids') or ['ai-product-delivery-blueprint','preos','gstack']:
    if not (skill_root / skill / 'SKILL.md').is_file():
        raise SystemExit(f'Installed skill missing SKILL.md: {skill_root / skill}')
agent_root=pathlib.Path(sys.argv[3]) / 'agents'
if len(list(agent_root.glob('vt_*.toml'))) < 9:
    raise SystemExit('Virtual Team agent metadata is incomplete')
PY
  printf 'Installed skills: PASS %s\n' "$SKILL_ROOT"
else
  printf 'Installed skills: SKIPPED by caller\n'
fi
printf 'Suite doctor: PASS\n'
