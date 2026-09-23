#!/usr/bin/env bash
# SUITE-LOCK owned_skill_count must remain 63 from CODEX-DISTRIBUTION.json manifests.
set -euo pipefail
BLUEPRINT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SUITE_ROOT=$(cd "$BLUEPRINT_ROOT/.." && pwd)
PREOS_ROOT="${PREOS_REPO:-$SUITE_ROOT/PREOS}"
GSTACK_ROOT="${GSTACK_REPO:-$SUITE_ROOT/gstack}"
SUITE_LOCK="$SUITE_ROOT/SUITE-LOCK.json"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_ROOT="${CODEX_SKILL_ROOT:-${CODEX_SKILLS_HOME:-$CODEX_HOME/skills}}"
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
case "$MODE" in install|verify|repair|update|uninstall) ;; *) exit 2 ;; esac
require_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 2; }; }
run_checked() { label="$1"; shift; printf '==> %s\n' "$label"; "$@"; }
suite_owned_skills() {
  python - "$BLUEPRINT_ROOT" "$PREOS_ROOT" "$GSTACK_ROOT" <<'PY'
import json
import pathlib
import sys
roots = [(pathlib.Path(sys.argv[1]), False), (pathlib.Path(sys.argv[2]), False), (pathlib.Path(sys.argv[3]), True)]
names = []
for root, prefix_gstack in roots:
    manifest = root / "CODEX-DISTRIBUTION.json"
    if not manifest.is_file():
        raise SystemExit(f"Missing distribution manifest: {manifest}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for skill in data.get("skills", []):
        name = skill.get("name")
        if not name:
            raise SystemExit(f"Malformed skill entry in {manifest}")
        if prefix_gstack and not name.startswith("gstack"):
            name = "gstack-" + name
        names.append(name)
if len(names) != len(set(names)):
    raise SystemExit("Duplicate suite skill names after manifest derivation")
for name in names:
    print(name)
PY
}
require_cmd python
mapfile -t OWNED_SKILLS < <(suite_owned_skills)
[ "${#OWNED_SKILLS[@]}" -eq 63 ] || { echo "Expected 63 suite-owned skills, derived ${#OWNED_SKILLS[@]}" >&2; exit 2; }
lock_commit() {
  [ -f "$SUITE_LOCK" ] || return 0
  python - "$SUITE_LOCK" "$1" <<'PY'
import json, sys
lock=json.loads(open(sys.argv[1], encoding='utf-8').read())
name=sys.argv[2]
for item in lock.get('components', []):
    if item.get('path') == name and item.get('commit'):
        print(item['commit']); raise SystemExit(0)
print(lock.get({'PREOS':'preos_commit','wed_dev_skill':'blueprint_commit','gstack':'gstack_commit'}.get(name,''),'') or '')
PY
}
repo_dirty() { [ -n "$(git -C "$1" status --porcelain=v1)" ]; }
ensure_repo() {
  name="$1"; path="$2"; url="$3"; component="$4"
  if [ ! -e "$path" ]; then
    case "$MODE" in install|repair|update) mkdir -p "$(dirname "$path")"; run_checked "clone $name" git clone "$url" "$path" ;; *) echo "$name repository missing: $path" >&2; exit 2 ;; esac
  fi
  [ -d "$path/.git" ] || { echo "$name repository missing .git: $path" >&2; exit 2; }
  expected="$(lock_commit "$component")"
  if [ "$MODE" = update ] || [ "$MODE" = repair ]; then
    [ "$ALLOW_UPDATE" -eq 1 ] || { echo "Mode $MODE requires --allow-update" >&2; exit 2; }
    ! repo_dirty "$path" || { echo "$name repository is dirty; refusing controlled update" >&2; exit 2; }
    run_checked "fetch $name" git -C "$path" fetch --all --tags
    [ -z "$expected" ] || run_checked "checkout locked $name" git -C "$path" checkout "$expected"
  fi
  if [ -n "$expected" ] && [ "$MODE" != install ]; then
    actual="$(git -C "$path" rev-parse HEAD)"
    [ "$actual" = "$expected" ] || { echo "$name lock drift: expected $expected got $actual" >&2; exit 2; }
  fi
}
run_doctor() {
  args=(--preos "$PREOS_ROOT" --gstack "$GSTACK_ROOT" --suite-lock "$SUITE_LOCK")
  [ "$SKIP_INSTALLED" -eq 1 ] && args+=(--skip-installed-skill-check)
  CODEX_HOME="$CODEX_HOME" CODEX_SKILL_ROOT="$SKILL_ROOT" CODEX_SKILLS_HOME="$SKILL_ROOT" "$BLUEPRINT_ROOT/scripts/suite-doctor.sh" "${args[@]}"
}
if [ "$MODE" = verify ]; then run_doctor; exit 0; fi
if [ "$MODE" = update ] && [ "$ALLOW_UPDATE" -ne 1 ]; then
  echo 'Mode update requires --allow-update so suite drift cannot happen implicitly.' >&2
  exit 2
fi
if [ "$MODE" = uninstall ]; then
  [ "$ALLOW_UPDATE" -eq 1 ] || { echo 'Mode uninstall requires --allow-update before installed files are removed.' >&2; exit 2; }
  mkdir -p "$SKILL_ROOT"
  root_real="$(cd "$SKILL_ROOT" && pwd -P)"
  for skill in "${OWNED_SKILLS[@]}"; do
    target="$SKILL_ROOT/$skill"
    target_abs="$root_real/$skill"
    case "$target_abs" in
      "$root_real"/*) [ -e "$target" ] && rm -rf "$target" ;;
      *) echo "Refusing to remove path outside skill root: $target" >&2; exit 2 ;;
    esac
  done
  if [ -d "$AGENT_ROOT" ]; then
    python - "$BLUEPRINT_ROOT/CODEX-DISTRIBUTION.json" "$AGENT_ROOT" <<'PY'
import json, pathlib, sys
manifest = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
agent_root = pathlib.Path(sys.argv[2])
for agent in manifest.get('agents', []):
    source = pathlib.PurePosixPath(agent.get('source_path', ''))
    name = source.name
    if name.startswith('vt_') and name.endswith('.toml'):
        path = agent_root / name
        if path.is_file():
            path.unlink()
PY
  fi
  printf 'Suite uninstall: PASS\n'
  exit 0
fi
require_cmd git
require_cmd bun
export CODEX_HOME
export CODEX_SKILL_ROOT="$SKILL_ROOT"
export CODEX_SKILLS_HOME="$SKILL_ROOT"
ensure_repo PREOS "$PREOS_ROOT" https://github.com/WilsonMisor/PREOS.git PREOS
ensure_repo gstack "$GSTACK_ROOT" https://github.com/WilsonMisor/gstack.git gstack
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
run_doctor
printf 'Suite %s health: PASS\n' "$MODE"