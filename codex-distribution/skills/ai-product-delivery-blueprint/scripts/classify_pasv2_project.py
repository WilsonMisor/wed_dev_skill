#!/usr/bin/env python3
"""Deterministic profile activation from declared project facts, with unknowns."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILE_REFERENCES={'web':'references/web/web-architecture.md','saas':'references/saas/tenant-isolation.md',
    'api':'references/api/rest.md','data':'references/data/relational-modeling.md',
    'infrastructure':'references/infrastructure/environment-strategy.md'}


def classify_project(facts,*,root=ROOT):
    if facts.get('documentation_only') is True:
        if any(facts.get(k) is True for k in ('changes_runtime','changes_security','changes_dependencies','changes_production_configuration')):
            raise ValueError('documentation-only classification conflicts with consequential changed scope')
        return {'profiles':[],'production_assurance':'inactive','architecture_review_required':False,
                'profile_decisions':[],'unknowns':[],'rationale':'Explicit documentation-only changed scope; no runtime, security, dependency or production-configuration change.'}
    architecture={str(v).casefold() for v in facts.get('architecture',[])}
    surfaces={str(v).casefold() for v in facts.get('delivery_surfaces',[])}
    reasons={}
    if architecture & {'web ui','browser','web'} or surfaces & {'public web','authenticated web','web'}:
        reasons['web']='Browser delivered UI is declared.'
    if str(facts.get('product_type','')).casefold()=='saas' or facts.get('tenant_model')=='multi-tenant' or facts.get('recurring_hosted_software') is True:
        reasons['saas']='Hosted software or shared tenant lifecycle is declared.'
    if architecture & {'rest','rest api','graphql','api'} or 'api' in surfaces:
        reasons['api']='Programmatic service contract is declared.'
    if architecture & {'relational database','document database','event store','database'} or facts.get('persistent_data') is True:
        reasons['data']='Durable application or business state is declared.'
    if facts.get('production_intent') is True or facts.get('first_production_release') is True or 'saas' in reasons:
        reasons['infrastructure']='Hosted application or production environment is declared.'
    unknowns=[k for k in ('tenant_model','money_movement','personal_data','production_intent') if k not in facts]
    high=facts.get('tenant_model')=='multi-tenant' or any(facts.get(k) is True for k in ('money_movement','payments','personal_data','regulated','critical_operations'))
    assurance='high-assurance' if high else ('standard' if facts.get('production_intent') is True else ('UNKNOWN' if unknowns else 'lightweight'))
    decisions=[]
    for profile,reason in reasons.items():
        reference=PROFILE_REFERENCES[profile];path=Path(root)/reference
        if not path.is_file():
            raise ValueError('activated profile reference is unavailable: '+reference)
        decisions.append({'profile':profile,'trigger':reason,'reference':reference,'reference_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return {'profiles':list(reasons),'production_assurance':assurance,'architecture_review_required':bool(reasons),
            'profile_decisions':decisions,'unknowns':unknowns,'authority':'Classification does not approve requirements, architecture, risk or release.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('facts',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=classify_project(json.loads(args.facts.read_text(encoding='utf-8')))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(rendered,encoding='utf-8',newline='\n')
    print(rendered,end='')


if __name__=='__main__': main()
