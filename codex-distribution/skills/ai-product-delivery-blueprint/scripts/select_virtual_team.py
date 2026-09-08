#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "references" / "virtual-team" / "role-registry.json"
ROUTER = ROOT / "references" / "virtual-team" / "role-router.json"
ROLE_CARDS = ROOT / "references" / "virtual-team" / "role-cards"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select canonical Blueprint virtual-team roles by governed capability.")
    parser.add_argument("--capability", help="Capability route such as /prod-intake or /prod-architecture")
    parser.add_argument("--list", action="store_true", help="List available capability routes")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    registry = load_json(REGISTRY)
    router = load_json(ROUTER)
    roles = {role["id"]: role for role in registry.get("roles", [])}
    routes = router.get("routes", [])
    if args.list:
        print(json.dumps({"count": len(routes), "capabilities": [route["capability"] for route in routes]}, indent=2))
        return
    if not args.capability:
        raise SystemExit("--capability is required unless --list is used")
    route = next((item for item in routes if item.get("capability") == args.capability), None)
    if route is None:
        raise SystemExit("UNKNOWN_CAPABILITY")
    role_ids = route.get("required_role_ids", [])
    missing = [role_id for role_id in role_ids if role_id not in roles]
    card_paths = []

    for role_id in role_ids:
        card = ROLE_CARDS / f"{role_id}.md"
        if not card.is_file():
            missing.append(role_id)
        else:
            card_paths.append(str(card.relative_to(ROOT)).replace("\\", "/"))
    result = {
        "capability": args.capability,
        "status": "ROLE_GAP" if missing else "READY",
        "role_ids": role_ids,
        "role_cards": card_paths,
        "role_gaps": sorted(set(missing)),
        "routing_basis": route.get("routing_basis"),
        "purpose": route.get("purpose", []),
        "outputs": route.get("outputs", []),
        "authority_boundary": router.get("authority_boundary"),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
