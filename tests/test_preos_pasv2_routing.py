import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PreosPasV2RoutingTests(unittest.TestCase):
    def test_pasv2_is_preos_owned_not_blueprint_corpus(self):
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        integration = (ROOT / 'references' / 'production-assurance' / 'preos-integration.md').read_text(encoding='utf-8')
        routing = (ROOT / 'orchestration' / 'preos-routing.md').read_text(encoding='utf-8')
        combined = skill + integration + routing
        self.assertIn('PAS v2', combined)
        self.assertIn('Do not duplicate the PREOS model2 corpus', combined)
        self.assertIn('PREOS_MODEL2_CROSSWALK_APPROVAL', combined)
        self.assertIn('RiskDefinition, RiskAssessment, RiskEconomics, RiskEvolution, RiskEvidence, and RiskAcceptance', combined)
        self.assertIn('Source 2 readiness gates remain R0-R17', combined)


if __name__ == '__main__':
    unittest.main()
