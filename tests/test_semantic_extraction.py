import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "source_intake.py"


def write_ooxml(path: Path, members: dict[str, str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, text in members.items():
            zf.writestr(name, text)


class SemanticExtractionAcceptanceTests(unittest.TestCase):
    def run_intake(self, source: Path, project: Path, *extra: str):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(source), "--project-root", str(project), *extra],
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
            self.assertIn("PostgreSQL", intake["observed_stack"]["databases"])
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
            intake = self.run_intake(src, project, "--decisions", str(decisions))
            self.assertIn("extracted", intake["observed_architecture"])
            self.assertEqual(intake["observed_architecture"]["governed"]["reviewed_shape"], "modular monolith")
            self.assertEqual(intake["approved_architecture"]["shape"], "modular monolith")
            self.assertEqual(intake["approved_stack"]["database"], "PostgreSQL")

    def test_documentary_technology_mentions_are_declared_not_observed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"; project = root / "project"
            src.mkdir(); project.mkdir()
            (src / "plan.md").write_text(
                "Legacy architecture uses React and MySQL. Proposed architecture uses Vue and PostgreSQL.\n"
                "The technology stack should use Vue with PostgreSQL.\n",
                encoding="utf-8",
            )
            (src / "requirements.txt").write_text("flask==3.0.0\n", encoding="utf-8")
            (src / "app.py").write_text("from flask import Flask\napp = Flask(__name__)\n", encoding="utf-8")
            intake = self.run_intake(src, project)
            observed = intake["observed_stack"]
            self.assertIn("Flask", observed["frameworks"])
            self.assertNotIn("React", observed["frameworks"])
            self.assertNotIn("Vue", observed["frameworks"])
            self.assertNotIn("MySQL", observed["databases"])
            self.assertNotIn("PostgreSQL", observed["databases"])
            declared = [x["statement"] for x in intake["declared_stack"]["statements"]]
            self.assertTrue(any("Vue" in statement for statement in declared))

    def test_docx_and_pptx_preserve_requirement_paragraph_boundaries(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"; project = root / "project"
            src.mkdir(); project.mkdir()
            docx_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:p><w:r><w:t>The portal must require administrator authentication.</w:t></w:r></w:p>
<w:p><w:r><w:t>Checkout shall prevent duplicate payment.</w:t></w:r></w:p>
</w:body></w:document>'''
            pptx_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:txBody>
<a:p><a:r><a:t>The dashboard must expose an audit trail.</a:t></a:r></a:p>
<a:p><a:r><a:t>The export shall preserve source identifiers.</a:t></a:r></a:p>
</p:txBody></p:sp></p:spTree></p:cSld></p:sld>'''
            write_ooxml(src / "requirements.docx", {"word/document.xml": docx_xml})
            write_ooxml(src / "requirements.pptx", {"ppt/slides/slide1.xml": pptx_xml})
            intake = self.run_intake(src, project)
            requirements = intake["source_requirements"]
            wording = [r["original_wording"] for r in requirements]
            self.assertIn("The portal must require administrator authentication.", wording)
            self.assertIn("Checkout shall prevent duplicate payment.", wording)
            self.assertIn("The dashboard must expose an audit trail.", wording)
            self.assertIn("The export shall preserve source identifiers.", wording)
            selected = [r for r in requirements if r["original_wording"] in wording]
            self.assertGreaterEqual(len({r["source_location"] for r in selected}), 2)
            self.assertTrue(all(" line " not in r["original_wording"].lower() for r in requirements))

    def test_governed_duplicate_by_source_id_replaces_extracted_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"; project = root / "project"
            src.mkdir(); project.mkdir()
            wording = "The service must retain an immutable audit trail."
            (src / "requirements.md").write_text(wording + "\n", encoding="utf-8")
            decisions = root / "decisions.json"
            decisions.write_text(json.dumps({
                "source_requirements": [{
                    "source_id": "SRC-0001",
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
            intake = self.run_intake(src, project, "--decisions", str(decisions))
            matches = [r for r in intake["source_requirements"] if r["original_wording"] == wording]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]["source_id"], "SRC-0001")
            self.assertEqual(matches[0]["extraction_method"], "GOVERNED_INPUT")
            self.assertEqual(matches[0]["authority"], "HUMAN_APPROVED")


if __name__ == "__main__":
    unittest.main()
