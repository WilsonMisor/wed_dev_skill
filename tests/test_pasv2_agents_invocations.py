import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_pasv2_invocations import REPRESENTATIVE_CASES, evaluate_invocation, validate
from pasv2_agents import BEGIN, apply_agents, check_agents, diff_agents


class PASV2AgentsAndInvocationTests(unittest.TestCase):
    def test_agents_updater_creates_idempotent_managed_block(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            first = apply_agents(repo)
            second = apply_agents(repo)
            text = (repo / "AGENTS.md").read_text(encoding="utf-8")
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual(text.count(BEGIN), 1)
            self.assertEqual(check_agents(repo)["rules_present"], True)

    def test_agents_updater_preserves_unrelated_content_and_removes_only_own_block(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            agents = repo / "AGENTS.md"
            agents.write_text("# Local Rules\n\nDo not erase this line.\n", encoding="utf-8")
            apply_agents(repo)
            after_insert = agents.read_text(encoding="utf-8")
            self.assertIn("Do not erase this line.", after_insert)
            self.assertIn("PAS / Blueprint Routing", after_insert)
            removed = apply_agents(repo, remove=True)
            self.assertTrue(removed["changed"])
            after_remove = agents.read_text(encoding="utf-8")
            self.assertIn("Do not erase this line.", after_remove)
            self.assertNotIn("PAS / Blueprint Routing", after_remove)

    def test_agents_updater_dry_run_and_diff_do_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            result = apply_agents(repo, dry_run=True)
            self.assertTrue(result["changed"])
            self.assertFalse((repo / "AGENTS.md").exists())
            diff = diff_agents(repo)
            self.assertIn("+## PAS / Blueprint Routing", diff)

    def test_invocation_evaluation_uses_computed_routes(self):
        for prompt, expected in REPRESENTATIVE_CASES:
            observed = evaluate_invocation(prompt, approved_packet="billing task packet" in prompt.lower())
            self.assertEqual(observed["selected_route"], expected, prompt)
        self.assertEqual(evaluate_invocation("Run security audit.")["gstack_route"], "gstack-cso")
        typo = evaluate_invocation("Fix README typo.")
        self.assertFalse(typo["preos_required"])
        self.assertIsNone(typo["gstack_route"])

    def test_invocation_validate_cli(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "evaluate_pasv2_invocations.py"), "--validate"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(validate()["case_count"], 6)


if __name__ == "__main__":
    unittest.main()