#!/usr/bin/env python3
"""Exact-source requirements and executable proof validation for PAS v2.

The register is an assertion to check, never evidence. No status supplied by a
register, evidence index, package builder, or previous run grants compliance.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

MASTER_SHA256 = '74e547225f0af2e0f64d0930f7f4317e86823bf6b103c96f648936b1dfa823c3'
REPOSITORIES = {'PREOS', 'wed_dev_skill', 'gstack'}
SELF_EVIDENCE = ('requirement-audit', 'compliance-register', 'requirements-evidence-index', 'artifact-registry', 'section-summary')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise ValueError(f'path escapes repository workspace: {relative}')
    if not path.is_file():
        raise ValueError(f'missing artifact: {relative}')
    return path


def resolve_reference(workspace: Path, ref: dict):
    """Resolve the smallest named object, not merely existence of its file."""
    path = safe_path(workspace, ref['path'])
    kind, target = ref['kind'], ref['target']
    if not target:
        raise ValueError('an exact reference must select an object inside its artifact')
    text = path.read_text(encoding='utf-8-sig')
    if kind == 'symbol':
        nodes = ast.parse(text).body
        node = None
        for part in target.split('.'):
            node = next((n for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == part), None)
            if node is None:
                raise ValueError(f'unresolved Python symbol: {path}:{target}')
            nodes = node.body
        return ast.get_source_segment(text, node)
    if kind == 'json_pointer':
        if not target.startswith('/') or target == '/':
            raise ValueError('JSON reference must address a specific object')
        node = json.loads(text)
        try:
            for token in target[1:].split('/'):
                token = token.replace('~1', '/').replace('~0', '~')
                node = node[int(token)] if isinstance(node, list) else node[token]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise ValueError(f'unresolved JSON pointer: {path}:{target}') from exc
        return node
    if kind == 'jsonl_record':
        key, value = target.split('=', 1)
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        matches = [r for r in rows if str(r.get(key)) == value]
        if len(matches) != 1:
            raise ValueError(f'JSONL reference must resolve exactly once: {path}:{target}')
        return matches[0]
    if kind == 'heading':
        lines = text.splitlines()
        starts = [i for i, line in enumerate(lines) if re.sub(r'^#{1,6}\s+', '', line) == target and line.startswith('#')]
        if len(starts) != 1:
            raise ValueError(f'heading must resolve exactly once: {path}:{target}')
        start = starts[0]
        level = len(lines[start]) - len(lines[start].lstrip('#'))
        end = next((i for i in range(start + 1, len(lines)) if re.match(r'^#{1,' + str(level) + r'} ', lines[i])), len(lines))
        return '\n'.join(lines[start:end])
    if kind == 'literal':
        if target not in text:
            raise ValueError(f'unresolved literal: {path}')
        return target
    raise ValueError(f'unsupported reference kind: {kind}')


def reparse_requirements(master: Path, locations: list[dict]) -> list[dict]:
    """Reconstruct immutable IDs from anchored source, discarding prior statuses.

Locations preserve the established 525 IDs. They only carry character ranges;
the actual text is always read from the hash-bound master. Numbered lists and
subsections remain in each complete section's obligation text.
"""
    raw = master.read_bytes()
    if digest(raw) != MASTER_SHA256:
        raise ValueError('wrong governing master hash')
    text = raw.decode('utf-8').replace('\r\n', '\n')
    ids, ranges, result = set(), set(), []
    headings = list(re.finditer(r'^(#{1,6}) (\d+(?:\.\d+)*)\.? (.+)$', text, re.M))
    for loc in locations:
        rid = loc['requirement_id']
        start, end = loc['start'], loc['end']
        if rid in ids or (start, end) in ranges or not 0 <= start < end <= len(text):
            raise ValueError('duplicate ID/location or invalid source range')
        ids.add(rid)
        ranges.add((start, end))
        exact = text[start:end]
        if digest(exact.encode()) != loc['text_sha256']:
            raise ValueError(f'source text changed for {rid}')
        heading = next((h for h in reversed(headings) if h.start() <= start), None)
        if heading is None:
            raise ValueError(f'requirement has no parent section: {rid}')
        result.append({'requirement_id': rid, 'exact_text': exact, 'parent_section': heading.group(2), 'parent_title': heading.group(3), 'source_start': start, 'source_end': end})
    if ids != {f'MP-REQ-{i:05d}' for i in range(1, 526)}:
        raise ValueError('established master requirement IDs missing or unexpected')
    return result


def validate_mappings(rows: list[dict], workspace: Path, *, require_proofs: bool = True) -> None:
    if not rows:
        raise ValueError('empty requirement register')
    ids = [r.get('requirement_id') for r in rows]
    if len(set(ids)) != len(ids) or None in ids:
        raise ValueError('duplicate or absent requirement ID')
    for row in rows:
        rid = row['requirement_id']
        owners = set(row.get('affected_repos', []))
        if not owners or not owners <= REPOSITORIES:
            raise ValueError(f'{rid}: invalid affected repositories')
        if owners == REPOSITORIES and not row.get('cross_repository_rationale'):
            raise ValueError(f'{rid}: unjustified all-three-repos blanket assignment')
        if not row.get('exact_text') or not row.get('parent_section') or not row.get('requirement_class'):
            raise ValueError(f'{rid}: missing exact requirement classification')
        proofs = row.get('proofs', [])
        if not proofs:
            if require_proofs or row.get('status') == 'PASS':
                raise ValueError(f'{rid}: no executable/deterministic proof')
            continue
        for proof in proofs:
            for ref in [proof['implementation'], proof['verification']]:
                if any(name in ref['path'].lower() for name in SELF_EVIDENCE):
                    raise ValueError(f'{rid}: evidence-index/register self-reference')
                if ref['path'].split('/')[0] not in owners:
                    raise ValueError(f'{rid}: implementation/test owner not in affected repositories')
                resolve_reference(workspace, ref)
            if proof['kind'] not in {'unittest', 'immutable_source'}:
                raise ValueError(f'{rid}: unsupported proof type')
            if not proof.get('claim') or not proof.get('evidence_output', '').endswith('/' + rid + '.json'):
                raise ValueError(f'{rid}: proof/evidence must be requirement-specific')
            if proof['kind'] == 'unittest':
                selector = proof.get('test_selector', '')
                if not re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){2,}', selector):
                    raise ValueError(f'{rid}: exact unittest method selector required')
                if proof['verification']['kind'] != 'symbol' or not selector.endswith(proof['verification']['target']):
                    raise ValueError(f'{rid}: executed test does not resolve to verification method')
            elif not re.fullmatch('[0-9a-f]{64}', proof.get('expected_sha256', '')):
                raise ValueError(f'{rid}: immutable artifact hash required')
    # A single broad validator/evidence file cannot prove unrelated sections.
    proved = [r for r in rows if r.get('proofs')]
    if len({str(r['parent_section']).split('.')[0] for r in proved}) > 3:
        verifiers = {json.dumps(p['verification'], sort_keys=True) for r in proved for p in r['proofs']}
        if len(verifiers) == 1:
            raise ValueError('one generic validator for unrelated requirements')


def run_proof(proof: dict, workspace: Path, *, timeout: int = 300) -> dict:
    """Compute a result now; never consume a previous status as evidence."""
    implementation = safe_path(workspace, proof['implementation']['path'])
    verification = safe_path(workspace, proof['verification']['path'])
    before = {str(p.relative_to(workspace)): digest(p.read_bytes()) for p in (implementation, verification)}
    started = time.perf_counter()
    if proof['kind'] == 'immutable_source':
        passed = digest(implementation.read_bytes()) == proof['expected_sha256']
        result = {'returncode': 0 if passed else 1, 'stdout': '', 'stderr': ''}
    else:
        repo = proof['verification']['path'].split('/')[0]
        command = [sys.executable, '-m', 'unittest', proof['test_selector']]
        proc = subprocess.run(command, cwd=workspace / repo / 'tests', capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
        # unittest can exit zero for skipped tests. Such a run is not proof.
        skipped = bool(re.search(r'OK \(skipped=|Ran 0 tests', proc.stderr))
        result = {'command': command, 'returncode': proc.returncode or (1 if skipped else 0), 'stdout': proc.stdout, 'stderr': proc.stderr}
    after = {str(p.relative_to(workspace)): digest(p.read_bytes()) for p in (implementation, verification)}
    if before != after:
        raise ValueError('proof inputs changed during verification')
    return {**result, 'input_sha256': before, 'elapsed_seconds': time.perf_counter() - started}


def validate_artifact_registry(rows: list[dict], workspace: Path, requirement_ids: set[str]) -> None:
    if not rows:
        raise ValueError('empty artifact registry')
    fields = {'requirement_ids', 'source_documents', 'repository', 'path', 'purpose', 'format', 'schema', 'generated', 'generator', 'sha256', 'validators', 'tests', 'canonical', 'final_commit', 'freshness_rule'}
    for row in rows:
        if not fields <= row.keys():
            raise ValueError('artifact metadata incomplete')
        if not row['requirement_ids'] or not set(row['requirement_ids']) <= requirement_ids:
            raise ValueError('artifact has unresolved requirements')
        if not row['path'].startswith(row['repository'] + '/'):
            raise ValueError('artifact repository/path mismatch')
        path = safe_path(workspace, row['path'])
        if digest(path.read_bytes()) != row['sha256']:
            raise ValueError(f'artifact checksum mismatch: {path}')
        if row['generated'] and not row['generator']:
            raise ValueError('generated artifact has no versioned generator')
        for ref in ([row['generator']] if row['generator'] else []) + row['validators'] + row['tests']:
            resolve_reference(workspace, ref)
        if not row['validators'] or not row['tests'] or not row['purpose'] or not row['freshness_rule']:
            raise ValueError('artifact lacks validation, test, purpose or freshness')
        commit = row['final_commit']
        if not re.fullmatch('[0-9a-f]{40}', commit):
            raise ValueError('artifact final commit missing')
        rel = row['path'].split('/', 1)[1]
        blob = subprocess.run(['git', '-C', str(workspace / row['repository']), 'show', f'{commit}:{rel}'], capture_output=True)
        if blob.returncode or digest(blob.stdout) != row['sha256']:
            raise ValueError('artifact bytes are not those committed at final_commit')
    if len(rows) > 3:
        for field in ('requirement_ids', 'purpose', 'validators', 'tests', 'freshness_rule'):
            if len({json.dumps(r[field], sort_keys=True) for r in rows}) == 1:
                raise ValueError(f'generic artifact registry: all rows have the same {field}')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('register', type=Path)
    parser.add_argument('--workspace', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--allow-unassessed', action='store_true')
    args = parser.parse_args()
    try:
        rows = json.loads(args.register.read_text(encoding='utf-8'))['requirements']
        validate_mappings(rows, args.workspace.resolve(), require_proofs=not args.allow_unassessed)
    except (ValueError, KeyError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print('Mapping structure checked; compliance statuses have not been inferred.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
