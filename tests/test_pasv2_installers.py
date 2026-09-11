import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PASV2InstallerTests(unittest.TestCase):
    def test_blueprint_codex_installers_exist_and_preserve_targets(self):
        ps1 = ROOT / 'scripts' / 'install-codex.ps1'
        sh = ROOT / 'scripts' / 'install-codex.sh'
        self.assertTrue(ps1.is_file())
        self.assertTrue(sh.is_file())
        ps1_text = ps1.read_text(encoding='utf-8')
        sh_text = sh.read_text(encoding='utf-8')
        for text in (ps1_text, sh_text):
            self.assertIn('ai-product-delivery-blueprint', text)
            self.assertIn('framework-install-backups', text)
            self.assertIn('CODEX_SKILLS_HOME', text)
            self.assertIn('codex-distribution', text)
        self.assertIn('Move-Item', ps1_text)
        self.assertIn('mv ', sh_text)

    def test_suite_installer_routes_all_three_repositories(self):
        ps1 = ROOT / 'install-suite.ps1'
        sh = ROOT / 'install-suite.sh'
        self.assertTrue(ps1.is_file())
        self.assertTrue(sh.is_file())
        combined = ps1.read_text(encoding='utf-8') + sh.read_text(encoding='utf-8')
        for token in ['validate-preos.py', 'validate-preos-integration.py', 'validate-three-repo-acceptance.py', '--host codex --prefix', 'install-codex']:
            self.assertIn(token, combined)

if __name__ == '__main__':
    unittest.main()
