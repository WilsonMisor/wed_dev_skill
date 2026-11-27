#!/usr/bin/env python3
"""Route invocations using the versioned metadata shipped to Codex.

Routing chooses a workflow. It never grants task, exception or release authority.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / 'orchestration/pasv2-invocation-routes.json'


def load_routes(path=ROUTES, root=ROOT):
    raw = Path(path).read_bytes()
    data = json.loads(raw)
    if data.get('schema_version') != 'pasv2-routing-v1':
        raise ValueError('unsupported invocation routing contract')
    identities = set()
    for row in data['routes']:
        if row['id'] in identities or not row.get('match_any'):
            raise ValueError('duplicate or unmatchable route')
        identities.add(row['id'])
        metadata = row['metadata']
        target = (Path(root)/metadata['path']).resolve()
        if not target.is_relative_to(Path(root).resolve()) or not target.is_file():
            raise ValueError('route metadata artifact is unavailable')
        content = target.read_text(encoding='utf-8')
        if metadata.get('heading') and not re.search(r'^#{1,6} '+re.escape(metadata['heading'])+r'\s*$',content,re.M):
            raise ValueError('route metadata heading does not resolve')
        if metadata.get('route_token') and not re.search(r'(?<![\w-])'+re.escape(metadata['route_token'])+r'(?![\w-])',content):
            raise ValueError('specialist route is unavailable in the routing contract')
        for pattern in row['match_any'] + row.get('exclude_any',[]):
            re.compile(pattern)
    return data, hashlib.sha256(raw).hexdigest()


def evaluate_invocation(prompt, *, approved_packet=False, production_context=True, routes_path=ROUTES, root=ROOT):
    # This compatibility flag is inert. Neither a caller boolean nor the word
    # approved supplies a durable authority artifact.
    data, digest = load_routes(routes_path, root)
    text = prompt.casefold()
    result = {'prompt':prompt,'selected_route':data['default_route'],'route_kind':'scope-unclassified',
              'authority':'no production authority granted','preos_required':False,
              'gstack_route':None,'bounded':False,'implementation_authorized':False,
              'prerequisites':['Classify scope before taking consequential action.'],
              'rationale':'No unambiguous executable intent matched the routing contract.',
              'routing_version':data['schema_version'],'routing_sha256':digest,'matched_rule':None}
    for row in data['routes']:
        if not any(re.search(p,text) for p in row['match_any']):
            continue
        if any(re.search(p,text) for p in row.get('exclude_any',[])):
            continue
        selected = row['route']
        specialist = row.get('gstack_route')
        prerequisites = []
        if row.get('requires_production_context') and not production_context:
            selected = row['context_fallback']
            specialist = None
            prerequisites.append('Bind the Project Contract before specialist execution.')
        if row.get('requires_approved_packet'):
            prerequisites.append('Load the approved AI Task Packet and verify its current source hashes and durable scoped human approval through PREOS before implementation.')
        result.update(selected_route=selected,route_kind=row['kind'],preos_required=row['preos_required'],
                      gstack_route=specialist,bounded=True,rationale=row['rationale'],
                      prerequisites=prerequisites,matched_rule=row['id'])
        return result
    return result


REPRESENTATIVE_CASES = [
    ('Build a new SaaS app.','ai-product-delivery-blueprint'),
    ('Review production risk on this branch.','preos-risk-model'),
    ('Run security audit.','gstack-cso'),
    ('QA this staging URL.','gstack-qa'),
    ('Implement the approved billing task packet.','blueprint-preos-codex-task-packet'),
    ('Fix README typo.','minimal-codex'),
]


def validate():
    results = []
    for prompt, expected in REPRESENTATIVE_CASES:
        observed = evaluate_invocation(prompt)
        if observed['selected_route'] != expected:
            raise ValueError(f'{prompt}: expected {expected}, got {observed["selected_route"]}')
        results.append({'prompt':prompt,'expected':expected,'observed':observed['selected_route'],'route':observed})
    cases = [('Can you make this app secure before launch?','gstack-cso'),
             ('Please fix the spelling typo in README','minimal-codex'),
             ('Explain vulnerability terminology.','clarify-scope'),
             ('Document QA staging URL usage.','clarify-scope')]
    for prompt, expected in cases:
        if evaluate_invocation(prompt)['selected_route'] != expected:
            raise ValueError('implicit invocation discrimination failed: '+prompt)
    return {'case_count':len(results),'implicit_checks':len(cases),'results':results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prompt',nargs='*')
    parser.add_argument('--no-production-context',action='store_true')
    parser.add_argument('--validate',action='store_true')
    args = parser.parse_args()
    if args.validate:
        result = validate()
    else:
        if not args.prompt:
            parser.error('a prompt is required unless --validate is used')
        result = evaluate_invocation(' '.join(args.prompt),production_context=not args.no_production_context)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
