import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "source_intake.py"


class SemanticExtractionAcceptanceTests(unittest.TestCase):
    def run_intake(self, source: Path, project: Path):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(source), "--project-root", str(project)],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads((project / ".ai-product-delivery/source-intake/SOURCE-INTAKE.json").read_text(encoding="utf-8"))

    def test_clean_pack_extracts_requirements_architecture_and_stack_without_decisions_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"; project = root / "project"
            src.mkdir(); project.mkdir()
            (src / "requirements.md").write_text(
                "# Requirements\n"
                "- The application must require authentication for the admin area.\n"
                "- Checkout shall complete without duplicate payment.\n\n"
                "# Architecture\n"
                "The architecture uses a frontend, REST API backend, PostgreSQL database, and Redis cache.\n"
                "The technology stack uses TypeScript with React and PostgreSQL.\n",
                encoding="utf-8",
            )
            (src / "package.json").write_text(json.dumps({
                "dependencies": {"react": "1.0.0", "express": "1.0.0", "pg": "1.0.0", "redis": "1.0.0"}
            }), encoding="utf-8")
            (src / "frontend/app.tsx").parent.mkdir()
            (src / "frontend/app.tsx").write_text("export const App = () => null;", encoding="utf-8")
            (src / "backend/routes/api.ts").parent.mkdir(parents=True)
            (src / "backend/routes/api.ts").write_text("export const route = true;", encoding="utf-8")

            intake = self.run_intake(src, project)
            wording = [r["original_wording"] for r in intake["source_requirements"]]
            self.assertTrue(any("must require authentication" in w for w in wording))
            self.assertTrue(any("shall complete" in w for w in wording))
            self.assertTrue(all(r["requires_governed_review"] for r in intake["source_requirements"]))
            self.assertEqual(intake["approved_architecture"], {})
            self.assertEqual(intake["approved_stack"], {})
            self.assertIn("Frontend", intake["observed_architecture"]["components"])
            self.assertIn("Backend", intake["observed_architecture"]["components"])
            self.assertIn("TypeScript", intake["observed_stack"]["languages"])
            self.assertIn("React", intake["observed_stack"]["frameworks"])
            self.assertGreaterEqual(len(intake["declared_architecture"]["statements"]), 1)
            self.assertGreaterEqual(len(intake["declared_stack"]["statements"]), 1)
            self.assertFalse(intake["semantic_extraction"]["automatic_approval"])

    def test_messy_pack_extracts_candidates_but_does_not_promote_old_or_final_filename(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"; project = root / "project"
            src.mkdir(); project.mkdir()
            (src / "requirements-v1-draft.md").write_text(
                "The service must support username login.\nArchitecture: monolith using Python and SQLite.\n",
                encoding="utf-8",
            )
            (src / "requirements-final.md").write_text(
                "The service must support email login.\nArchitecture: REST API using Python and PostgreSQL.\n",
                encoding="utf-8",
            )
            (src / "requirements-copy.md").write_text(
                "The service must support email login.\nArchitecture: REST API using Python and PostgreSQL.\n",
                encoding="utf-8",
            )
            intake = self.run_intake(src, project)
            self.assertGreaterEqual(len(intake["source_requirements"]), 3)
            self.assertEqual(len(intake["duplicate_groups"]), 1)
            self.assertGreaterEqual(len(intake["version_candidate_groups"]), 1)
            by_path = {s["path"]: s for s in intake["sources"]}
            self.assertEqual(by_path["requirements-final.md"]["authority"], "UNCLASSIFIED")
            self.assertEqual(by_path["requirements-v1-draft.md"]["authority"], "UNCLASSIFIED")
            self.assertEqual(by_path["requirements-final.md"]["supersedes"], [])
            self.assertEqual(intake["approved_architecture"], {})
            self.assertEqual(intake["approved_stack"], {})

    def test_governed_architecture_and_stack_are_preserved_separately_from_extraction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"; project = root / "project"
            src.mkdir(); project.mkdir()
            (src / "architecture.md").write_text(
                "The architecture uses a monolith with SQLite. The service must expose an API.\n",
                encoding="utf-8",
            )
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({
                "observed_architecture": {"reviewed_shape": "modular monolith"},
                "declared_stack": {"reviewed_language": "Python"},
                "approved_architecture": {"shape": "modular monolith"},
                "approved_stack": {"language": "Python", "database": "PostgreSQL"},
            }), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(src), "--project-root", str(project), "--decisions", str(decisions)],
                cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            intake = json.loads((project / ".ai-product-delivery/source-intake/SOURCE-INTAKE.json").read_text(encoding="utf-8"))
            self.assertIn("extracted", intake["observed_architecture"])
            self.assertEqual(intake["observed_architecture"]["governed"]["reviewed_shape"], "modular monolith")
            self.assertEqual(intake["approved_architecture"]["shape"], "modular monolith")
            self.assertEqual(intake["approved_stack"]["database"], "PostgreSQL")


if __name__ == "__main__":
    unittest.main()
