import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "select_virtual_team.py"


class VirtualTeamRoutingTests(unittest.TestCase):
    def run_selector(self, *args, check=True):
        proc = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def test_lists_capability_routes(self):
        proc = self.run_selector("--list")
        data = json.loads(proc.stdout)
        self.assertEqual(data["count"], 24)
        self.assertIn("/prod-intake", data["capabilities"])

    def test_known_capability_resolves_canonical_roles_and_cards(self):
        proc = self.run_selector("--capability", "/prod-intake")
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "READY")
        self.assertEqual(data["role_ids"], ["VT-R01-product-manager", "VT-R02-business-analyst", "VT-R03-domain-specialist"])
        self.assertEqual(len(data["role_cards"]), 3)
        self.assertEqual(data["role_gaps"], [])

    def test_unknown_capability_is_rejected(self):
        proc = self.run_selector("--capability", "/prod-made-up", check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("UNKNOWN_CAPABILITY", proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
