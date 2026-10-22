#!/usr/bin/env python3
"""Reparse the hash-bound master into an unassessed implementation specification."""
import argparse
import json
from pathlib import Path
from pasv2_compliance import MASTER_SHA256, reparse_requirements, validate_mappings

PREOS = {3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,30,31,32,33,46,50,51,52,53,54,55,56,57,58,59,60,61,62,74,75,76,78,79,80,89,90,91,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,128,129,130,131}
BLUEPRINT = {5,34,35,39,40,41,42,43,45,48,49,70,71,72,73,82,83,84,85,87,88,95,99,100,133}
GSTACK = {36,37,38,47}
BEHAVIOR = {10,17,26,27,31,39,40,41,42,44,49,50,51,52,54,55,56,60,62,63,64,65,72,73,75,76,77,85,86,88,89,90,91,92,93,94,95,100,112,113,114,116,117,118,119,120,123,128,131,132,135}
AUTHORITY = {1,22,23,24,25,55,69,79,80,81,104,107,109,126,129}
DOCS = {38,66,67,68,70,71,82,83,84,96,98,99,101,102,103,122,127,130,133,134}


def scope(section):
    if section.startswith('1.'):
        return {'1.1':['wed_dev_skill'],'1.2':['PREOS'],'1.3':['gstack']}.get(section, ['PREOS','wed_dev_skill','gstack'])
    number = int(section.split('.')[0])
    if number in PREOS:
        return ['PREOS']
    if number in BLUEPRINT:
        return ['wed_dev_skill']
    if number in GSTACK:
        return ['gstack']
    return ['PREOS','wed_dev_skill','gstack']


def compile_requirements(master, locations):
    rows = reparse_requirements(master, locations)
    for row in rows:
        section = int(row['parent_section'].split('.')[0])
        kind = 'behavioral' if section in BEHAVIOR else ('authority' if section in AUTHORITY else ('documentary' if section in DOCS else 'data_or_integration'))
        owners = scope(row['parent_section'])
        row.update(requirement_class=kind, affected_repos=owners,
                   cross_repository_rationale=(f"Section {row['parent_section']} governs the composed suite: {row['parent_title']}. Each implementation proof must resolve to its actual owner." if len(owners) == 3 else None),
                   expected_implementation_type=('executable runtime and negative behavioral test' if kind == 'behavioral' else 'deterministic validation of canonical artifact'),
                   implementation_path=None, exact_reference=None, required_verification=None,
                   evidence_output=f"evidence/requirements/{row['requirement_id']}.json", proofs=[], status='UNASSESSED')
    return {'governing_master_sha256':MASTER_SHA256, 'requirements':rows}


def main():
    root = Path(__file__).resolve().parents[1] / 'references/pasv2'
    ap = argparse.ArgumentParser()
    ap.add_argument('--master', type=Path, default=root/'master-prompt.md')
    ap.add_argument('--locations', type=Path, default=root/'requirement-locations.json')
    ap.add_argument('--output', type=Path, default=root/'requirements.unassessed.json')
    args = ap.parse_args()
    result = compile_requirements(args.master, json.loads(args.locations.read_text(encoding='utf-8')))
    validate_mappings(result['requirements'], Path(__file__).resolve().parents[2], require_proofs=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f"Reparsed {len(result['requirements'])} exact source requirements; all UNASSESSED.")


if __name__ == '__main__':
    main()
