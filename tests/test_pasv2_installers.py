import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


def suite_owned_skills():
    names = []
    for repo, prefix_gstack in ((ROOT, False), (WORKSPACE / 'PREOS', False), (WORKSPACE / 'gstack', True)):
        manifest = json.loads((repo / 'CODEX-DISTRIBUTION.json').read_text(encoding='utf-8'))
        for skill in manifest['skills']:
            name = skill['name']
            if prefix_gstack and not name.startswith('gstack'):
                name = 'gstack-' + name
            names.append(name)
    return names


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
            self.assertIn('CODEX_SKILL_ROOT', text)
            self.assertIn('CODEX_HOME', text)
            self.assertIn('codex-distribution', text)
            self.assertIn('CODEX-DISTRIBUTION.json', text)
        self.assertIn('Move-Item', ps1_text)
        self.assertIn('mv ', sh_text)
        self.assertIn('if [ -d "$BACKUP_ROOT" ]; then', sh_text)
        self.assertIn("tr -d '\\r'", sh_text)
        self.assertNotIn('[ -d "$BACKUP_ROOT" ] && printf', sh_text)

    def test_suite_installer_routes_all_three_repositories(self):
        ps1 = ROOT / 'install-suite.ps1'
        sh = ROOT / 'install-suite.sh'
        self.assertTrue(ps1.is_file())
        self.assertTrue(sh.is_file())
        combined = ps1.read_text(encoding='utf-8') + sh.read_text(encoding='utf-8')
        for token in ['validate-preos.py', 'validate-preos-integration.py', 'validate-three-repo-acceptance.py', 'Install-GstackCodexSkills', 'install_gstack_codex_skills', 'materialize gstack Codex distribution', 'Get-OwnedSkillInventory', 'owned_skill_inventory', 'owned_skill_ids', 'install-codex', 'suite-doctor', 'install', 'verify', 'repair', 'update', 'uninstall', 'SUITE-LOCK.json', 'git clone', 'fetch --all --tags', 'repository is dirty', 'Blueprint repository is dirty; refusing controlled self-update', 'Ensure-BlueprintSelf', 'blueprint_self_update', 'CODEX_HOME/skills', 'CODEX-DISTRIBUTION.json', 'owned_skill_count', '63']:
            self.assertIn(token, combined)
        self.assertNotIn('--host codex --prefix', combined)
        self.assertLess(ps1.read_text(encoding='utf-8').index("Ensure-Repo 'gstack'"), ps1.read_text(encoding='utf-8').index('$OwnedSkills = @(Get-SuiteOwnedSkills)'))
        self.assertLess(sh.read_text(encoding='utf-8').index('ensure_repo gstack'), sh.read_text(encoding='utf-8').index('mapfile -t OWNED_SKILLS < <(suite_owned_skills)'))


    def test_posix_installer_invokes_non_executable_shell_scripts_with_bash_and_installs_gstack_natively(self):
        sh = (ROOT / 'install-suite.sh').read_text(encoding='utf-8')
        self.assertIn('bash "$BLUEPRINT_ROOT/scripts/suite-doctor.sh"', sh)
        self.assertIn('bash "$BLUEPRINT_ROOT/scripts/install-codex.sh"', sh)
        self.assertIn('bash "$PREOS_ROOT/scripts/install-codex.sh"', sh)
        self.assertIn('install_gstack_codex_skills', sh)
        self.assertIn('gstack-', sh)
        self.assertIn('CODEX-DISTRIBUTION.json', sh)
        self.assertNotIn('bash "$GSTACK_ROOT/setup"', sh)
        self.assertNotIn("run_checked 'install Blueprint for Codex' \"$BLUEPRINT_ROOT/scripts/install-codex.sh\"", sh)

    def test_suite_doctor_scripts_are_bounded_and_lock_aware(self):
        ps1 = ROOT / 'scripts' / 'suite-doctor.ps1'
        sh = ROOT / 'scripts' / 'suite-doctor.sh'
        self.assertTrue(ps1.is_file())
        self.assertTrue(sh.is_file())
        combined = ps1.read_text(encoding='utf-8') + sh.read_text(encoding='utf-8')
        for token in ['SUITE-LOCK.json', 'validate-pasv2-remediation-artifacts.py', 'SkipInstalledSkillCheck', 'skip-installed-skill-check', 'validate-three-repo-acceptance.py', 'owned_skill_ids', 'owned_skill_count', 'CODEX-DISTRIBUTION.json', 'selected_skill_root', 'suite_version', 'preos_commit', 'gstack_commit']:
            self.assertIn(token, combined)

    def test_suite_uninstall_removes_only_manifest_owned_skills_from_codex_root(self):
        powershell = shutil.which('powershell') or shutil.which('pwsh')
        if not powershell:
            self.skipTest('PowerShell is not available')
        skills = suite_owned_skills()
        self.assertEqual(len(skills), 63)
        self.assertEqual(len(set(skills)), 63)
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            codex_home = temp_root / 'codex-home'
            skill_root = codex_home / 'skills'
            agent_root = codex_home / 'agents'
            skill_root.mkdir(parents=True)
            agent_root.mkdir(parents=True)
            for skill in skills:
                path = skill_root / skill
                path.mkdir()
                (path / 'SKILL.md').write_text('# test\n', encoding='utf-8')
            unrelated = skill_root / 'personal-notes'
            unrelated.mkdir()
            (unrelated / 'SKILL.md').write_text('# mine\n', encoding='utf-8')
            (agent_root / 'vt_quality.toml').write_text('name = "vt_quality"\n', encoding='utf-8')
            env = os.environ.copy()
            env['CODEX_HOME'] = str(codex_home)
            env['CODEX_SKILL_ROOT'] = str(skill_root)
            env['CODEX_SKILLS_HOME'] = str(skill_root)
            cmd = [
                powershell,
                '-NoProfile',
                '-ExecutionPolicy',
                'Bypass',
                '-File',
                str(ROOT / 'install-suite.ps1'),
                '-Mode',
                'uninstall',
                '-AllowUpdate',
                '-PreosPath',
                str(WORKSPACE / 'PREOS'),
                '-GstackPath',
                str(WORKSPACE / 'gstack'),
                '-SuiteLockPath',
                str(WORKSPACE / 'SUITE-LOCK.json'),
            ]
            proc = subprocess.run(cmd, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            for skill in skills:
                self.assertFalse((skill_root / skill).exists(), skill)
            self.assertTrue((unrelated / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
