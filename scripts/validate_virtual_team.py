#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIRTUAL_TEAM = ROOT / "references" / "virtual-team"
ROLE_CARDS = VIRTUAL_TEAM / "role-cards"
SCHEMAS = ROOT / "schemas"
PROFILE_SEEDS = ROOT / "orchestration" / "profile-seeds"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

def validate_registry_and_cards() -> set[str]:
    registry = load_json(VIRTUAL_TEAM / "role-registry.json")
    roles = registry.get("roles", [])
    if registry.get("role_count") != 40 or len(roles) != 40:
        fail("virtual-team registry must contain exactly 40 roles")
    role_ids = [role.get("id") for role in roles]
    if len(role_ids) != len(set(role_ids)):
        fail("virtual-team registry contains duplicate role IDs")

    missing_cards = [role_id for role_id in role_ids if not (ROLE_CARDS / f"{role_id}.md").is_file()]
    if missing_cards:
        fail("missing virtual-team role cards: " + ", ".join(missing_cards[:5]))
    card_ids = {path.stem for path in ROLE_CARDS.glob("VT-R*.md")}
    if card_ids != set(role_ids):
        fail("virtual-team role card set does not match registry IDs")
    principle = registry.get("principle", "")
    if "canonical roles" not in principle or "not forty mandatory" not in principle:
        fail("virtual-team bounded role principle changed")
    print("PASS: virtual-team registry and 40 role cards are present")
    return set(role_ids)

def validate_router(role_ids: set[str]) -> None:
    router = load_json(VIRTUAL_TEAM / "role-router.json")
    routes = router.get("routes", [])
    if len(routes) != 24:
        fail(f"virtual-team router must contain 24 routes, found {len(routes)}")

    capabilities = [route.get("capability") for route in routes]
    if len(capabilities) != len(set(capabilities)):
        fail("virtual-team router contains duplicate capabilities")
    for route in routes:
        missing = sorted(set(route.get("required_role_ids", [])) - role_ids)
        if missing:
            fail(f"route {route.get('capability')} references missing roles: {missing[:5]}")
    boundary = router.get("authority_boundary", "")
    if "must not invent" not in boundary or "canonical role IDs" not in boundary:
        fail("virtual-team router authority boundary must prohibit invented routing")
    print("PASS: virtual-team router has 24 bounded routes and valid role references")

def validate_schemas_and_profile_seeds() -> None:
    schema_names = [
        "virtual-team-role-registry.schema.json",
        "virtual-team-role-router.schema.json",
        "virtual-team-handoff.schema.json",
    ]

    for name in schema_names:
        schema = load_json(SCHEMAS / name)
        if schema.get("type") != "object":
            fail(f"schema {name} must be an object schema")
        if not schema.get("required"):
            fail(f"schema {name} must declare required fields")
    seeds = sorted(PROFILE_SEEDS.glob("*.json"))
    if len(seeds) != 4:
        fail(f"expected 4 profile seeds, found {len(seeds)}")
    for seed in seeds:
        data = load_json(seed)
        for key in ["profile_id", "name", "activation_rule", "required_evidence", "stop_conditions"]:
            if key not in data:
                fail(f"profile seed {seed.name} missing {key}")
    print("PASS: virtual-team schemas and profile seeds parse with required anchors")

def validate_selector_contract() -> None:
    selector = ROOT / "scripts" / "select_virtual_team.py"
    text = selector.read_text(encoding="utf-8")

    for token in ["role-router.json", "role-registry.json", "UNKNOWN_CAPABILITY", "ROLE_GAP", "authority_boundary"]:
        if token not in text:
            fail(f"select_virtual_team.py missing {token}")
    disallowed = [
        ROOT / "virtual-team" / "source-prod-skill-registry.json",
        ROOT / "virtual-team" / "role-reference-resolution.json",
    ]
    present = [str(path.relative_to(ROOT)) for path in disallowed if path.exists()]
    if present:
        fail("migration-only virtual-team registries installed as runtime: " + ", ".join(present))
    print("PASS: virtual-team selector uses installed router/registry and excludes migration-only registries")

def main() -> None:
    role_ids = validate_registry_and_cards()
    validate_router(role_ids)
    validate_schemas_and_profile_seeds()
    validate_selector_contract()
    print("PASS: Blueprint virtual-team validation complete")

if __name__ == "__main__":
    main()
