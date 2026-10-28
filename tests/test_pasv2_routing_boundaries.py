import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from pasv2_agents import BEGIN, END, ROUTING_RULES, apply_agents, check_agents, upsert_text, remove_text
from evaluate_pasv2_invocations import ROUTES, evaluate_invocation, validate


class AgentsBoundaryTests(unittest.TestCase):
    def test_unrelated_bytes_survive_install_update_and_rollback(self):
        samples = [b'',b'  # Personal rules\r\n\r\nDo not change.  \r\n\r\n',
                   b'No final newline',b'\xef\xbb\xbf# Rules\r\n', '# Rules\n\nCafé\t\n'.encode()]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'AGENTS.md'
            for original in samples:
                path.write_bytes(original)
                apply_agents(path.parent)
                installed = path.read_bytes()
                self.assertTrue(check_agents(path.parent)['valid'])
                self.assertFalse(apply_agents(path.parent)['changed'])
                self.assertEqual(installed,path.read_bytes())
                apply_agents(path.parent,remove=True)
                self.assertEqual(path.read_bytes(),original)

    def test_legacy_block_replacement_preserves_prefix_and_suffix_exactly(self):
        prefix,suffix = '  USER\r\n\r\n','\r\n  TAIL\r\n\r\n'
        updated,_ = upsert_text(prefix+BEGIN+'\r\nold routing\r\n'+END+suffix)
        self.assertTrue(updated.startswith(prefix+BEGIN))
        self.assertTrue(updated.endswith(END+'\r\n'+suffix))
        self.assertEqual(remove_text(updated)[0],prefix+suffix)

    def test_malformed_duplicate_and_reversed_markers_are_rejected_without_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'AGENTS.md'
            for text in [BEGIN,END,END+BEGIN,BEGIN+BEGIN+END,BEGIN+END+BEGIN+END]:
                path.write_bytes(text.encode())
                for remove in (False,True):
                    with self.assertRaises(ValueError):
                        apply_agents(path.parent,remove=remove)
                    self.assertEqual(path.read_bytes(),text.encode())

    def test_all_eight_master_routing_obligations_are_in_managed_block(self):
        self.assertEqual(len(ROUTING_RULES),8)
        obligations = ['Substantial product work routes to Blueprint','Production assurance routes through PREOS',
                       'gstack provides specialist execution','Implementation uses approved AI Task Packets',
                       'Blueprint/PREOS gates cannot be bypassed','Direct specialist invocation is allowed for narrow tasks',
                       'Conversation memory is not authoritative project state','Irreversible operations require appropriate']
        for obligation in obligations:
            self.assertTrue(any(obligation in rule for rule in ROUTING_RULES),obligation)

    def test_check_does_not_count_rules_outside_managed_block(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp)/'AGENTS.md').write_text('\n'.join(ROUTING_RULES)+'\n'+BEGIN+'\nempty\n'+END)
            self.assertFalse(check_agents(Path(temp))['valid'])


class InvocationBoundaryTests(unittest.TestCase):
    def test_representative_routes_and_untrusted_approval_claims(self):
        self.assertEqual(validate()['case_count'],6)
        for flag in (False,True):
            result = evaluate_invocation('Implement the approved billing task packet.',approved_packet=flag)
            self.assertEqual(result['selected_route'],'blueprint-preos-codex-task-packet')
            self.assertFalse(result['implementation_authorized'])
            self.assertIn('durable scoped human approval',result['prerequisites'][0])
        self.assertEqual(evaluate_invocation('Explain a packet.',approved_packet=True)['selected_route'],'clarify-scope')

    def test_implicit_intent_is_discriminated_from_keywords_and_mixed_scope(self):
        for prompt in ['Explain the word secure.', 'Document vulnerability terminology.',
                       'What does security audit mean?', 'Document QA this staging URL.',
                       'Fix README typo and implement billing.', 'Fix payment code and README typo.']:
            result = evaluate_invocation(prompt)
            self.assertEqual(result['selected_route'],'clarify-scope',prompt)
            self.assertIsNone(result['gstack_route'])
        self.assertEqual(evaluate_invocation('Can you make this app secure before launch?')['selected_route'],'gstack-cso')
        self.assertEqual(evaluate_invocation('Fix secure spelling typo in README')['selected_route'],'minimal-codex')

    def test_router_executes_metadata_and_binds_its_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'routes.json'
            data = json.loads(ROUTES.read_text())
            data['routes'][0]['match_any']=['^custom narrow request$']
            path.write_text(json.dumps(data))
            result = evaluate_invocation('custom narrow request',routes_path=path)
            self.assertEqual(result['selected_route'],'minimal-codex')
            self.assertNotEqual(result['routing_sha256'],evaluate_invocation('Fix README typo.')['routing_sha256'])
            self.assertEqual(evaluate_invocation('Fix README typo.',routes_path=path)['selected_route'],'clarify-scope')

    def test_missing_metadata_and_unknown_contract_version_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'routes.json'
            for change in ('missing','version'):
                data = json.loads(ROUTES.read_text())
                if change == 'missing':
                    data['routes'][0]['metadata']['path']='absent.md'
                else:
                    data['schema_version']='unsupported'
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    evaluate_invocation('Fix README typo.',routes_path=path)

    def test_missing_production_context_requires_preos_intake(self):
        result = evaluate_invocation('Run security audit.',production_context=False)
        self.assertEqual(result['selected_route'],'preos-risk-model')
        self.assertIsNone(result['gstack_route'])
        self.assertTrue(result['prerequisites'])


if __name__ == '__main__':
    unittest.main()
