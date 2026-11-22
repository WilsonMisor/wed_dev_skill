import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from verify_installed_suite import inventory,verify,write_receipt

class InstalledSuiteIntegrityTests(unittest.TestCase):
    @unittest.skipUnless(os.name=='nt','Windows directory-handle semantics')
    def test_open_directory_is_backed_up_and_updated_without_nested_skill(self):
        import ctypes
        from ctypes import wintypes
        installer=(ROOT/'install-suite.ps1').read_text(encoding='utf-8')
        functions='function Backup-SuitePath'+installer.split('function Backup-SuitePath',1)[1].split('function Invoke-SuiteDoctor',1)[0]
        with tempfile.TemporaryDirectory(prefix='open suite directory ') as td:
            root=Path(td);home=root/'codex';target=home/'skills/gstack';target.mkdir(parents=True)
            (target/'SKILL.md').write_text('previous owner content')
            repo=root/'repo';source=repo/'codex-distribution/skills/gstack';source.mkdir(parents=True)
            content='---\nname: gstack\n---\nUpdated runtime\n';(source/'SKILL.md').write_text(content)
            (source/'runtime.json').write_text('{"version":2}')
            (repo/'CODEX-DISTRIBUTION.json').write_text(json.dumps({'skills':[{'name':'gstack'}]}))
            script=root/'install.ps1';script.write_text('param([string]$HomePath,[string]$Repo)\n$ErrorActionPreference="Stop"\n$CodexHome=$HomePath\n$SkillRoot=Join-Path $HomePath "skills"\n$GstackRoot=$Repo\nfunction Invoke-Checked([string]$Label,[scriptblock]$Block) {}\n'+functions+'\nInstall-GstackCodexSkills\n',encoding='utf-8')
            kernel=ctypes.WinDLL('kernel32',use_last_error=True)
            kernel.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
            kernel.CreateFileW.restype=wintypes.HANDLE;kernel.CloseHandle.argtypes=[wintypes.HANDLE]
            handle=kernel.CreateFileW(str(target),0x80000000,3,None,3,0x02000000,None)
            self.assertNotEqual(handle,wintypes.HANDLE(-1).value)
            try:
                proc=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),str(home),str(repo)],capture_output=True)
                self.assertEqual(proc.returncode,0,proc.stderr.decode(errors='replace'))
            finally:kernel.CloseHandle(handle)
            self.assertEqual((target/'SKILL.md').read_text(),content)
            self.assertEqual(json.loads((target/'runtime.json').read_text()),{'version':2})
            self.assertFalse((target/'gstack').exists())
            backups=list((home/'framework-install-backups').glob('*/gstack/SKILL.md'))
            self.assertEqual([p.read_text() for p in backups],['previous owner content'])

    def test_windows_namespacing_preserves_unicode_and_line_endings(self):
        powershell=shutil.which('powershell') or shutil.which('pwsh')
        if not powershell: self.skipTest('PowerShell unavailable')
        installer=(ROOT/'install-suite.ps1').read_text(encoding='utf-8')
        function=installer.split('function Set-SkillFrontmatterName',1)[1].split('function Install-GstackCodexSkills',1)[0]
        with tempfile.TemporaryDirectory(prefix='pas unicode ') as td:
            root=Path(td); skill=root/'SKILL.md'
            content='---\r\nname: review\r\n---\r\nReview \u2014 preserve caf\u00e9, \u03bb and \u2713.\r\n'
            skill.write_bytes(content.encode('utf-8'))
            script=root/'rename.ps1';script.write_text('param([string]$Target)\nfunction Set-SkillFrontmatterName'+function+'\nSet-SkillFrontmatterName $Target "gstack-review"\n',encoding='utf-8')
            proc=subprocess.run([powershell,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),str(root)],capture_output=True)
            self.assertEqual(proc.returncode,0,proc.stderr.decode(errors='replace'))
            self.assertEqual(skill.read_bytes(),content.replace('name: review','name: gstack-review').encode('utf-8'))

    def fixture(self,root):
        repos=[]
        for label in ('blueprint','preos','gstack'):
            repo=root/label;source=repo/'codex-distribution/skills'/label;source.mkdir(parents=True)
            (source/'SKILL.md').write_text('---\nname: '+label+'\n---\nGoverned skill\n')
            (source/'runtime.json').write_text('{"authority":"human"}')
            (repo/'CODEX-DISTRIBUTION.json').write_text(json.dumps({'skills':[{'name':label,'source_path':'codex-distribution/skills/'+label}]}))
            repos.append(repo)
        codex=root/'Codex Home With Spaces';skillroot=codex/'skills';skillroot.mkdir(parents=True)
        for label,repo in zip(('blueprint','preos','gstack'),repos):shutil.copytree(repo/'codex-distribution/skills'/label,skillroot/label)
        unrelated=skillroot/'personal-notes';unrelated.mkdir();(unrelated/'SKILL.md').write_text('mine')
        return repos,codex

    @patch('verify_installed_suite.subprocess.check_output',return_value='a'*40)
    def test_doctor_checks_runtime_hashes_and_preserves_unrelated_skills(self,_):
        with tempfile.TemporaryDirectory() as td:
            repos,codex=self.fixture(Path(td));result=verify(*repos,codex)
            self.assertEqual(result['skill_count'],3)
            (codex/'skills/preos/runtime.json').write_text('{"authority":"agent"}')
            with self.assertRaisesRegex(ValueError,'stale'):verify(*repos,codex)
            self.assertEqual((codex/'skills/personal-notes/SKILL.md').read_text(),'mine')

    @patch('verify_installed_suite.subprocess.check_output',return_value='b'*40)
    def test_receipt_reinstall_preserves_previous_receipt_and_structured_inventory(self,_):
        with tempfile.TemporaryDirectory() as td:
            repos,codex=self.fixture(Path(td));result=verify(*repos,codex)
            receipt=write_receipt(result,*repos,codex);before=receipt.read_bytes()
            write_receipt(result,*repos,codex)
            self.assertTrue(any(p.read_bytes()==before for p in receipt.parent.glob('*.previous-*.json')))
            data=json.loads(receipt.read_text());self.assertEqual(data['skills'][2]['repository'],'WilsonMisor/gstack')
            self.assertFalse(data['suite_verification']['production_authorized'])

    def test_duplicate_or_out_of_scope_inventory_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            repos,codex=self.fixture(Path(td));manifest=repos[0]/'CODEX-DISTRIBUTION.json'
            data=json.loads(manifest.read_text());data['skills'][0]['name']='../personal-notes';manifest.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'unsafe'):inventory(*repos)

if __name__=='__main__':unittest.main()
