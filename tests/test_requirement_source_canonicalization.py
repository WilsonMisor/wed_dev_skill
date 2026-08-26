import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "source_intake.py"


class CanonicalRequirementSourceMergeTests(unittest.TestCase):
    def test_governed_source_path_replaces_extracted_source_id_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            project = root / "project"
            src.mkdir()
            project.mkdir()
            wording = "The service must retain an immutable audit trail."
            (src / "requirements.md").write_text(wording + "\n", encoding="utf-8")
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({
                "source_requirements": [{
                    "source_path": "requirements.md",
                    "source_location": "approved requirement 1",
                    "original_wording": wording,
                    "normalized_interpretation": "Retain immutable audit records.",
                    "category": "SECURITY",
                    "authority": "HUMAN_APPROVED",
                    "confidence": "HIGH",
                    "conflict_state": "NONE",
                    "extraction_method": "GOVERNED_INPUT",
                    "requires_governed_review": False,
                }]
            }), encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(src), "--project-root", str(project),
                 "--decisions", str(decisions)],
                cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            intake = json.loads(
                (project / ".ai-product-delivery/source-intake/SOURCE-INTAKE.json").read_text(encoding="utf-8")
            )
            matches = [r for r in intake["source_requirements"] if r["original_wording"] == wording]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["source_id"], "SRC-0001")
            self.assertEqual(matches[0]["extraction_method"], "GOVERNED_INPUT")
            self.assertEqual(matches[0]["authority"], "HUMAN_APPROVED")


if __name__ == "__main__":
    unittest.main()
