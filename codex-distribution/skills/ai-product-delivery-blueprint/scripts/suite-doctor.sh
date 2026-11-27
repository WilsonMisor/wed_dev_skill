#!/usr/bin/env bash
set -euo pipefail
BLUEPRINT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SUITE_ROOT=$(cd "$BLUEPRINT_ROOT/.." && pwd)
PREOS_ROOT="${PREOS_REPO:-$SUITE_ROOT/PREOS}"
GSTACK_ROOT="${GSTACK_REPO:-$SUITE_ROOT/gstack}"
SUITE_LOCK="$SUITE_ROOT/SUITE-LOCK.json"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_ROOT="${CODEX_SKILL_ROOT:-${CODEX_SKILLS_HOME:-$CODEX_HOME/skills}}"
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
python - "$SUITE_LOCK" "$SUITE_ROOT" "$BLUEPRINT_ROOT" "$PREOS_ROOT" "$GSTACK_ROOT" "$SKILL_ROOT" "$CODEX_HOME" "$SKIP_INSTALLED" <<'PY'
import json
import pathlib
import subprocess
import sys
lock_path = pathlib.Path(sys.argv[1])
suite_root = pathlib.Path(sys.argv[2])
blueprint_root = pathlib.Path(sys.argv[3])
preos_root = pathlib.Path(sys.argv[4])
gstack_root = pathlib.Path(sys.argv[5])
skill_root = pathlib.Path(sys.argv[6])
codex_home = pathlib.Path(sys.argv[7])
skip_installed = sys.argv[8] == "1"
lock = json.loads(lock_path.read_text(encoding="utf-8"))
required = [
    'suite_version','preos_version','preos_commit','blueprint_version','blueprint_commit',
    'gstack_version','gstack_commit','integration_contract_version','risk_catalogue_version',
    'risk_schema_version','readiness_framework_mapping_version','gate_schema_version',
    'virtual_team_contract_version','tested_codex_host_profile','os_runtime_profile',
    'selected_skill_root','owned_skill_source','owned_skill_count','owned_skill_ids'
]
for field in required:
    if not lock.get(field):
        raise SystemExit(f'Suite lock missing {field}')

def manifest_skills(root: pathlib.Path, prefix_gstack: bool = False) -> list[str]:
    manifest = root / 'CODEX-DISTRIBUTION.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    names = []
    for skill in data.get('skills', []):
        name = skill.get('name')
        if prefix_gstack and not name.startswith('gstack'):
            name = 'gstack-' + name
        names.append(name)
    return names
expected = manifest_skills(blueprint_root) + manifest_skills(preos_root) + manifest_skills(gstack_root, True)
if not expected or len(set(expected)) != len(expected):
    raise SystemExit(f'Manifest-derived suite inventory must contain unique skills, got {len(expected)}')
if lock.get('owned_skill_count') != len(expected):
    raise SystemExit(f"Suite lock owned_skill_count mismatch: {lock.get('owned_skill_count')} != {len(expected)}")
if lock.get('owned_skill_ids') != expected:
    raise SystemExit('Suite lock owned_skill_ids do not match manifest-derived inventory')
if lock.get('selected_skill_root') != 'CODEX_HOME/skills':
    raise SystemExit('Suite lock selected_skill_root must be CODEX_HOME/skills')
repo_by_path = {'wed_dev_skill': blueprint_root, 'PREOS': preos_root, 'gstack': gstack_root}
for component in lock.get('components', []):
    repo = repo_by_path.get(component.get('path')) or suite_root / component.get('path', '')
    actual = subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    if component.get('commit') and actual != component['commit']:
        raise SystemExit(f"Suite lock drift for {component['name']}: expected {component['commit']}, got {actual}")
if not skip_installed:
    for skill in expected:
        if not (skill_root / skill / 'SKILL.md').is_file():
            raise SystemExit(f'Installed skill missing SKILL.md: {skill_root / skill}')
    agents = json.loads((blueprint_root / 'CODEX-DISTRIBUTION.json').read_text(encoding='utf-8')).get('agents', [])
    agent_root = codex_home / 'agents'
    for agent in agents:
        name = pathlib.PurePosixPath(agent.get('source_path', '')).name
        if not (agent_root / name).is_file():
            raise SystemExit(f'Virtual Team agent metadata missing: {agent_root / name}')
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
  printf 'Installed skills: PASS %s\n' "$SKILL_ROOT"
else
  printf 'Installed skills: SKIPPED by caller\n'
fi
if [ "$SKIP_INSTALLED" -eq 0 ]; then
  python "$BLUEPRINT_ROOT/scripts/verify_installed_suite.py" --preos "$PREOS_ROOT" --gstack "$GSTACK_ROOT" --codex-home "$CODEX_HOME" --skill-root "$SKILL_ROOT"
fi
printf 'Suite doctor: PASS\n'
