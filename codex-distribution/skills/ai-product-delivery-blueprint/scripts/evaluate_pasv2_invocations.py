#!/usr/bin/env python3
"""Evaluate PAS v2 representative invocation routing against Blueprint metadata."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GSTACK_ROUTES = ROOT / "orchestration" / "gstack-routing.md"
PREOS_ROUTES = ROOT / "orchestration" / "preos-routing.md"
CODEX_ROUTES = ROOT / "orchestration" / "codex-routing.md"


def _contains_route(route: str) -> bool:
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in [GSTACK_ROUTES, PREOS_ROUTES, CODEX_ROUTES] if path.is_file())
    return route in corpus


def evaluate_invocation(prompt: str, *, approved_packet: bool = False, production_context: bool = True) -> dict:
    text = prompt.lower()
    route = {
        "prompt": prompt,
        "selected_route": "direct",
        "route_kind": "direct",
        "authority": "no production authority granted",
        "preos_required": False,
        "gstack_route": None,
        "bounded": True,
        "rationale": "No production-relevant delivery route matched.",
    }

    if re.search(r"\bbuild\b.*\bsaas\b|\bnew saas app\b", text):
        route.update(
            selected_route="ai-product-delivery-blueprint",
            route_kind="blueprint-governed-start",
            preos_required=True,
            rationale="New SaaS work starts with Blueprint classification and Project Contract creation before implementation.",
        )
    elif "production risk" in text or "risk on this branch" in text:
        route.update(
            selected_route="preos-risk-model",
            route_kind="preos-assurance",
            preos_required=True,
            rationale="Branch production-risk review is a PREOS risk/evidence/gate pass.",
        )
    elif "security audit" in text or "threat" in text or "vulnerability" in text or "secure" in text:
        selected = "gstack-cso" if production_context else "preos-risk-model"
        route.update(
            selected_route=selected,
            route_kind="governed-gstack-specialist" if production_context else "preos-assurance",
            preos_required=True,
            gstack_route="gstack-cso" if production_context else None,
            rationale="Security audit routes through governed PREOS context to the gstack CSO specialist when project context is available.",
        )
    elif "qa" in text and ("staging" in text or "url" in text):
        route.update(
            selected_route="gstack-qa",
            route_kind="gstack-qa",
            preos_required=False,
            gstack_route="gstack-qa",
            rationale="Staging URL QA is a gstack browser QA route; findings return as evidence and do not approve release.",
        )
    elif approved_packet or ("approved" in text and "billing" in text and "packet" in text):
        route.update(
            selected_route="blueprint-preos-codex-task-packet",
            route_kind="approved-implementation",
            preos_required=True,
            gstack_route="gstack-review",
            rationale="Approved billing implementation remains bounded to the AI Task Packet with PREOS controls and post-implementation review.",
        )
    elif "readme" in text and ("typo" in text or "fix" in text or "spelling" in text):
        route.update(
            selected_route="minimal-codex",
            route_kind="low-risk-minimal",
            preos_required=False,
            gstack_route=None,
            rationale="A trivial documentation typo should not trigger full PREOS or expensive specialist review.",
        )
    return route


REPRESENTATIVE_CASES = [
    ("Build a new SaaS app.", "ai-product-delivery-blueprint"),
    ("Review production risk on this branch.", "preos-risk-model"),
    ("Run security audit.", "gstack-cso"),
    ("QA this staging URL.", "gstack-qa"),
    ("Implement the approved billing task packet.", "blueprint-preos-codex-task-packet"),
    ("Fix README typo.", "minimal-codex"),
]


def validate() -> dict:
    missing_routes = [route for route in ["preos-risk-model", "gstack-cso", "gstack-qa", "gstack-review"] if not _contains_route(route)]
    if missing_routes:
        raise SystemExit("missing route metadata: " + ", ".join(missing_routes))
    results = []
    failures = []
    for prompt, expected in REPRESENTATIVE_CASES:
        observed = evaluate_invocation(prompt, approved_packet="billing task packet" in prompt.lower())
        results.append({"prompt": prompt, "expected": expected, "observed": observed["selected_route"], "route": observed})
        if observed["selected_route"] != expected:
            failures.append(f"{prompt!r}: expected {expected}, got {observed['selected_route']}")
    implicit = evaluate_invocation("Can you make this app secure before launch?")
    if implicit["selected_route"] != "gstack-cso" or not implicit["preos_required"]:
        failures.append("implicit security invocation did not route through governed gstack CSO path")
    typo = evaluate_invocation("Please fix the spelling typo in README")
    if typo["preos_required"] or typo["gstack_route"]:
        failures.append("low-risk README typo triggered unnecessary PREOS/gstack route")
    if failures:
        raise SystemExit("\n".join(failures))
    return {"case_count": len(REPRESENTATIVE_CASES), "implicit_checks": 2, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="*")
    parser.add_argument("--approved-packet", action="store_true")
    parser.add_argument("--no-production-context", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if args.validate:
        print(json.dumps(validate(), indent=2))
        return 0
    prompt = " ".join(args.prompt).strip()
    if not prompt:
        raise SystemExit("prompt is required unless --validate is used")
    print(json.dumps(evaluate_invocation(prompt, approved_packet=args.approved_packet, production_context=not args.no_production_context), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())