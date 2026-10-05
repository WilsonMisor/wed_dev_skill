#!/usr/bin/env bash
# Manifest-owned Blueprint skill: ai-product-delivery-blueprint
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_ROOT="${CODEX_SKILL_ROOT:-${CODEX_SKILLS_HOME:-$CODEX_HOME/skills}}"
AGENT_ROOT="$CODEX_HOME/agents"
DIST="$ROOT/codex-distribution"
SKILL_NAME=$(python - "$ROOT/CODEX-DISTRIBUTION.json" <<'PY'
import json, pathlib, sys
manifest = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
skills = manifest.get('skills', [])
if len(skills) != 1 or not skills[0].get('name'):
    raise SystemExit('Blueprint CODEX-DISTRIBUTION.json must declare exactly one skill')
print(skills[0]['name'])
PY
)

if [ ! -d "$DIST/skills" ]; then
  python "$ROOT/scripts/build_codex_distribution.py"
fi

SKILL_SOURCE="$DIST/skills/$SKILL_NAME"
AGENTS_SOURCE="$DIST/agents"
[ -f "$SKILL_SOURCE/SKILL.md" ] || { echo 'Blueprint distribution missing SKILL.md' >&2; exit 2; }
[ -d "$AGENTS_SOURCE" ] || { echo 'Blueprint distribution missing agents directory' >&2; exit 2; }

mkdir -p "$SKILL_ROOT" "$AGENT_ROOT"
BACKUP_ROOT="$CODEX_HOME/framework-install-backups/blueprint-$(date -u +%Y%m%dT%H%M%SZ)"
backup_existing_path() {
  target="$1"
  if [ -e "$target" ]; then
    mkdir -p "$BACKUP_ROOT"
    mv "$target" "$BACKUP_ROOT/$(basename "$target")"
  fi
}

TARGET_SKILL="$SKILL_ROOT/$SKILL_NAME"
backup_existing_path "$TARGET_SKILL"
cp -R "$SKILL_SOURCE" "$TARGET_SKILL"

for file in "$AGENTS_SOURCE"/*.toml; do
  [ -e "$file" ] || continue
  target="$AGENT_ROOT/$(basename "$file")"
  backup_existing_path "$target"
  cp "$file" "$target"
done

[ -f "$TARGET_SKILL/SKILL.md" ] || { echo 'Installed Blueprint skill missing SKILL.md' >&2; exit 3; }
agent_count=$(find "$AGENT_ROOT" -maxdepth 1 -name 'vt_*.toml' -type f | wc -l)
[ "$agent_count" -ge 9 ] || { echo 'Installed Blueprint agents incomplete' >&2; exit 3; }
commit=$(git -C "$ROOT" rev-parse --short HEAD)
printf 'Installed Blueprint skill under %s\n' "$SKILL_ROOT"
printf 'Installed Blueprint agents under %s\n' "$AGENT_ROOT"
printf 'Blueprint commit %s\n' "$commit"
if [ -d "$BACKUP_ROOT" ]; then
  printf 'Previous governed targets backed up under %s\n' "$BACKUP_ROOT"
fi
