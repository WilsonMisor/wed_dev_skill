import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from pasv2_compliance import resolve_reference, validate_mappings, validate_artifact_registry


class ComplianceProofTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'PREOS').mkdir()
        (self.root / 'PREOS/runtime.py').write_text('def evaluate():\n    return 3\n', encoding='utf-8')
        (self.root / 'PREOS/test_runtime.py').write_text('class Tests:\n    def test_value(self):\n        assert evaluate() == 3\n', encoding='utf-8')
        self.row = {'requirement_id':'MP-REQ-00001', 'exact_text':'Evaluate the real operation.', 'parent_section':'31', 'requirement_class':'behavioral', 'affected_repos':['PREOS'], 'status':'UNASSESSED', 'proofs':[{'kind':'unittest','claim':'computed value is 3','implementation':{'path':'PREOS/runtime.py','kind':'symbol','target':'evaluate'},'verification':{'path':'PREOS/test_runtime.py','kind':'symbol','target':'Tests.test_value'},'test_selector':'test_runtime.Tests.test_value','evidence_output':'evidence/requirements/MP-REQ-00001.json'}]}

    def test_resolves_specific_code_and_nested_test(self):
        validate_mappings([self.row], self.root)
        self.assertIn('assert evaluate() == 3', resolve_reference(self.root, self.row['proofs'][0]['verification']))

    def test_rejects_blanket_repository_assignment(self):
        self.row['affected_repos'] = ['PREOS','wed_dev_skill','gstack']
        with self.assertRaisesRegex(ValueError, 'blanket'):
            validate_mappings([self.row], self.root)

    def test_rejects_self_proving_evidence_index(self):
        self.row['proofs'][0]['implementation']['path'] = 'PREOS/requirements-evidence-index.json'
        with self.assertRaisesRegex(ValueError, 'self-reference'):
            validate_mappings([self.row], self.root)

    def test_pass_string_cannot_replace_runnable_proof(self):
        self.row['proofs'] = []
        self.row['status'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'no executable'):
            validate_mappings([self.row], self.root, require_proofs=False)

    def test_rejects_nonresolving_symbol(self):
        self.row['proofs'][0]['implementation']['target'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'unresolved Python symbol'):
            validate_mappings([self.row], self.root)

    def test_rejects_generic_validator_across_unrelated_sections(self):
        rows = []
        for n in range(4):
            row = copy.deepcopy(self.row)
            row.update(requirement_id=f'MP-REQ-{n+1:05d}', parent_section=str(n+1))
            row['proofs'][0]['evidence_output'] = f"evidence/{row['requirement_id']}.json"
            rows.append(row)
        with self.assertRaisesRegex(ValueError, 'generic validator'):
            validate_mappings(rows, self.root)

    def test_different_expected_test_is_not_the_executed_test(self):
        self.row['proofs'][0]['test_selector'] = 'test_runtime.Tests.test_other'
        with self.assertRaisesRegex(ValueError, 'executed test'):
            validate_mappings([self.row], self.root)

    def test_missing_reference_and_path_escape_fail(self):
        with self.assertRaisesRegex(ValueError, 'escapes'):
            resolve_reference(self.root, {'path':'../outside.py','kind':'symbol','target':'f'})
        with self.assertRaisesRegex(ValueError, 'missing artifact'):
            resolve_reference(self.root, {'path':'PREOS/absent.py','kind':'symbol','target':'f'})

    def test_unassessed_rows_cannot_be_used_as_closure(self):
        self.row['proofs'] = []
        validate_mappings([self.row], self.root, require_proofs=False)
        with self.assertRaisesRegex(ValueError, 'no executable'):
            validate_mappings([self.row], self.root)

    def test_old_generic_artifact_registry_fails_schema(self):
        legacy = [{'mp_req_ids':['MP-REQ-00001'], 'generator':'build_formal_closure.py', 'status':'PASS'}] * 160
        with self.assertRaisesRegex(ValueError, 'metadata incomplete'):
            validate_artifact_registry(legacy, self.root, {'MP-REQ-00001'})


if __name__ == '__main__':
    unittest.main()
