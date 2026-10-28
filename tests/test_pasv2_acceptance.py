import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from classify_pasv2_project import classify_project
from pasv2_acceptance import evaluate_high_assurance, evaluate_low_risk, high_fixture, load_runtime


class PASV2AcceptanceTests(unittest.TestCase):
    def test_exact_high_assurance_fixture_computes_all_fourteen_outcomes(self):
        with tempfile.TemporaryDirectory() as temporary:
            project=Path(temporary)
            result=evaluate_high_assurance(ROOT.parent/'PREOS',ROOT.parent/'gstack',project=project)
            self.assertEqual(len(result['outcomes']),14)
            self.assertTrue(all(result['outcomes'].values()))
            self.assertTrue((project/'.ai-product-delivery/PROJECT-CLASSIFICATION.json').is_file())
            self.assertGreater(result['candidate_count'],0)
            self.assertEqual(result['gate']['gate_state'],'RED')
            self.assertFalse(result['gate']['production_authorized'])

    def test_low_risk_fixture_guards_actual_corpus_reads_and_specialist_routing(self):
        result=evaluate_low_risk(ROOT.parent/'PREOS',ROOT.parent/'gstack')
        self.assertTrue(all(result['outcomes'].values()))
        self.assertEqual(result['catalogue_io']['files_opened'],0)
        self.assertEqual(result['loaded_risk_count'],0)
        self.assertEqual(result['specialist_routes'],[])

    def test_acceptance_fails_when_selector_omits_required_jurisdiction(self):
        engines,_,_=load_runtime(ROOT.parent/'PREOS',ROOT.parent/'gstack')
        original=engines.RiskCatalogue.select
        def missing_jurisdiction(catalogue,context,limit=25):
            return [r for r in original(catalogue,context,limit) if r['dimension']!='jurisdiction']
        with patch.object(engines.RiskCatalogue,'select',missing_jurisdiction):
            with self.assertRaisesRegex(ValueError,'nigeria_risks'):
                evaluate_high_assurance(ROOT.parent/'PREOS',ROOT.parent/'gstack')

    def test_declared_profile_list_is_not_itself_proof_of_activation(self):
        facts=high_fixture();facts['profiles']=['mobile']
        result=classify_project(facts)
        self.assertEqual(set(result['profiles']),{'web','saas','api','data','infrastructure'})
        self.assertNotIn('mobile',result['profiles'])
        self.assertEqual(classify_project({})['production_assurance'],'UNKNOWN')

    def test_contradictory_documentation_only_scope_and_missing_references_fail(self):
        with self.assertRaises(ValueError): classify_project({'documentation_only':True,'changes_runtime':True})
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError,'reference is unavailable'):
                classify_project(high_fixture(),root=Path(temporary))


if __name__=='__main__': unittest.main()
