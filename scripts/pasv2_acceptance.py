#!/usr/bin/env python3
"""Run Section 94/95 fixtures through the three repository-owned runtime paths."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

from classify_pasv2_project import classify_project
from evaluate_pasv2_invocations import evaluate_invocation
from pasv2_agents import apply_agents, check_agents

ROOT=Path(__file__).resolve().parents[1]


def load_runtime(preos,gstack):
    preos=Path(preos).resolve();gstack=Path(gstack).resolve()
    sys.path.insert(0,str(preos/'scripts'))
    import assurance_engines
    import control_assurance
    spec=importlib.util.spec_from_file_location('pasv2_specialist_routes',gstack/'scripts/pasv2_specialist_routes.py')
    specialist=importlib.util.module_from_spec(spec);spec.loader.exec_module(specialist)
    return assurance_engines,control_assurance,specialist


def high_fixture():
    return {'project_id':'pasv2-high-assurance-fixture','release_id':'fixture-first-release','product_type':'SaaS',
        'tenant_model':'multi-tenant','payments':True,'money_movement':True,'personal_data':True,
        'architecture':['REST','relational database','queue','external payment provider','web UI'],
        'external_providers':['payment provider'],'jurisdictions':['Nigeria'],'features':['withdrawal'],
        'actors':['tenant user','admin','payment provider'],'first_production_release':True,
        'production_intent':True,'maturity_stage':'Stage 1 Early Production','threat_stage':'Stage 2',
        'business_rules':['at most one payment per idempotency key','tenant boundary enforced','ledger/provider totals reconcile']}


def evaluate_high_assurance(preos,gstack,*,project=None):
    if project is None:
        with tempfile.TemporaryDirectory(prefix='pasv2-high-') as temporary:
            return evaluate_high_assurance(preos,gstack,project=Path(temporary))
    project=Path(project);project.mkdir(parents=True,exist_ok=True)
    engines,controls,specialist=load_runtime(preos,gstack)
    facts=high_fixture()
    (project/'project-facts.json').write_text(json.dumps(facts,indent=2))
    classification=classify_project(facts)
    contract={**facts,'classification':classification,'profiles':classification['profiles']}
    state=project/'.ai-product-delivery';state.mkdir(exist_ok=True)
    (state/'PROJECT-CLASSIFICATION.json').write_text(json.dumps(classification,indent=2))
    (state/'PROJECT-CONTRACT.json').write_text(json.dumps(contract,indent=2))
    apply_agents(project)
    route=evaluate_invocation('Build a new SaaS app.')
    catalogue=engines.RiskCatalogue()
    generated=engines.risk_generation_engine(contract,limit=50,catalogue=catalogue,queue=state/'preos/candidates')
    gate=controls.evidence_gate_engine(contract,evidence={},repo=project)
    requests=specialist.route_specialists(contract,root=Path(gstack))
    records=generated['selected_records']
    facets={f for row in records for f in row['matched_facets']}
    by_control={r['nondeferrable_control_id']:r for r in gate['nondeferrable']['results']}
    outcomes={
        'blueprint_profiles':route['selected_route']=='ai-product-delivery-blueprint' and set(classification['profiles'])=={'saas','web','api','data','infrastructure'} and check_agents(project)['valid'],
        'universal_risks':any(r['dimension']=='universal' for r in records),
        'payment_finance_risks':'money' in facets,
        'saas_risks':'product' in facets and any(r['dimension']=='product' and 'saas' in r['category'].casefold() for r in records),
        'nigeria_risks':any(r['dimension']=='jurisdiction' and r['category']=='Nigeria' for r in records),
        'architecture_risks':{'architecture:REST','architecture:relational database','architecture:queue'}<=facets,
        'contextual_risk_generation':bool(generated['bounded_contextual_candidates']) and len(list((state/'preos/candidates').glob('*.json')))==len(generated['bounded_contextual_candidates']),
        'financial_correctness':by_control['NDC-02']['applicability']=='APPLICABLE' and {'FS-021','FS-027','FS-028'}<=set(by_control['NDC-02']['preos_control_ids']),
        'cross_tenant_isolation':by_control['NDC-05']['applicability']=='APPLICABLE' and 'FS-074' in by_control['NDC-05']['preos_control_ids'],
        'payment_idempotency':by_control['NDC-12']['applicability']=='APPLICABLE' and 'FS-012' in by_control['NDC-12']['preos_control_ids'],
        'reconciliation':by_control['NDC-18']['applicability']=='APPLICABLE' and 'FS-028' in by_control['NDC-18']['preos_control_ids'],
        'gstack_specialists':{'gstack-cso','gstack-review','gstack-qa','gstack-benchmark'}=={r['skill'] for r in requests['requests']},
        'missing_evidence_unknown_red':gate['gate_state']=='RED' and all(by_control[c]['blockers'] for c in ('NDC-02','NDC-05','NDC-12','NDC-18')),
        'production_not_auto_approved':gate['production_authorized'] is False and requests['production_authorized'] is False and route['implementation_authorized'] is False,
    }
    if not all(outcomes.values()):
        raise ValueError('high-assurance acceptance failed: '+', '.join(k for k,v in outcomes.items() if not v))
    return {'fixture':facts,'classification':classification,'outcomes':outcomes,'pass':True,
            'selected_risk_ids':generated['selected_context_variants'],'selection_facets':sorted(facets),
            'candidate_count':len(generated['bounded_contextual_candidates']),'specialist_routes':requests,
            'gate':gate,'catalogue_io':catalogue.stats,'model2_authority':'CONTEXT_ONLY_PENDING_MODEL2_APPROVAL'}


def evaluate_low_risk(preos,gstack):
    engines,controls,specialist=load_runtime(preos,gstack)
    facts={'product_type':'documentation-only','documentation_only':True,'features':['README typo'],
           'architecture':[],'money_movement':False,'personal_data':False,'changes_runtime':False,
           'changes_security':False,'changes_dependencies':False,'changes_production_configuration':False}
    classification=classify_project(facts)
    route=evaluate_invocation('Fix README typo.')
    catalogue=engines.RiskCatalogue()
    # An accidental corpus load fails this runtime acceptance immediately.
    def forbidden_read(): raise ValueError('documentation-only path opened the risk corpus')
    catalogue.records=forbidden_read
    generated=engines.risk_generation_engine(facts,catalogue=catalogue)
    requests=specialist.route_specialists(facts,root=Path(gstack))
    outcomes={'no_full_4337_scan':catalogue.stats['records_read']==0 and catalogue.stats['files_opened']==0,
        'no_unnecessary_architecture_review':classification['architecture_review_required'] is False,
        'no_expensive_specialist_routing':requests['requests']==[] and requests['metadata_files_read']==0 and route['gstack_route'] is None,
        'no_4337_risk_context_load':generated['selected_context_variants']==[] and generated['bounded_contextual_candidates']==[]}
    if not all(outcomes.values()): raise ValueError('low-risk proportionality failed')
    return {'fixture':facts,'outcomes':outcomes,'loaded_risk_count':catalogue.stats['records_read'],
            'catalogue_io':catalogue.stats,'specialist_routes':[],'pass':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preos',type=Path,required=True);parser.add_argument('--gstack',type=Path,required=True)
    parser.add_argument('--case',choices=['high','low','both'],default='both');parser.add_argument('--output',type=Path)
    args=parser.parse_args();result={}
    if args.case in ('high','both'): result['high']=evaluate_high_assurance(args.preos,args.gstack)
    if args.case in ('low','both'): result['low']=evaluate_low_risk(args.preos,args.gstack)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(rendered,encoding='utf-8',newline='\n')
    print(rendered,end='')


if __name__=='__main__': main()
