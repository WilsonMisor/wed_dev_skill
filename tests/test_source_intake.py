import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_intake", ROOT / "scripts" / "source_intake.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class SourceIntakeTests(unittest.TestCase):
    def records(self):
        rows = [
            {"source_id": "", "path": "requirements-v1.md", "source_type": "FILE", "size": 2, "sha256": "a" * 64, "authority": "UNCLASSIFIED", "status": "CURRENT_CANDIDATE", "supersedes": [], "superseded_by": [], "conflict_group": None},
            {"source_id": "", "path": "requirements-final.md", "source_type": "FILE", "size": 2, "sha256": "b" * 64, "authority": "UNCLASSIFIED", "status": "CURRENT_CANDIDATE", "supersedes": [], "superseded_by": [], "conflict_group": None},
        ]
        MOD.assign_ids(rows)
        return rows

    def test_directory_inventory_and_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            out = root / "out"
            src.mkdir()
            (src / "a.md").write_text("same", encoding="utf-8")
            (src / "b.md").write_text("same", encoding="utf-8")
            records, warnings = MOD.inspect_directory(src, out)
            MOD.assign_ids(records)
            self.assertEqual(warnings, [])
            self.assertEqual(MOD.detect_mode(records), "GREENFIELD")
            self.assertEqual(len(MOD.build_duplicate_groups(records)), 1)
            self.assertEqual([r["source_id"] for r in records], ["SRC-0001", "SRC-0002"])

    def test_code_means_brownfield_evidence(self):
        records = [{"path": "app.py", "sha256": "x"}]
        self.assertEqual(MOD.detect_mode(records), "BROWNFIELD")

    def test_zip_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "bad.zip"
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr("../escape.txt", "no")
            with self.assertRaises(ValueError):
                MOD.inspect_zip(z)

    def test_zip_absolute_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "bad-absolute.zip"
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr("/escape.txt", "no")
            with self.assertRaises(ValueError):
                MOD.inspect_zip(z)

    def test_zip_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "bad-symlink.zip"
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr(info, "target")
            with self.assertRaises(ValueError):
                MOD.inspect_zip(z)

    def test_directory_symlink_is_skipped_not_followed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            outside = root / "outside.txt"
            out = root / "out"
            src.mkdir()
            outside.write_text("secret", encoding="utf-8")
            link = src / "escape.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable")
            records, warnings = MOD.inspect_directory(src, out)
            self.assertEqual(records, [])
            self.assertTrue(any("symlink skipped" in w for w in warnings))

    def test_version_candidates_do_not_infer_supersession(self):
        rows = self.records()
        groups = MOD.build_version_candidate_groups(rows)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["rule"], "CANDIDATE_ONLY_DO_NOT_INFER_SUPERSESSION")
        self.assertEqual(rows[0]["supersedes"], [])
        self.assertEqual(rows[1]["supersedes"], [])

    def test_explicit_supersession_and_authority_are_applied(self):
        rows = self.records()
        MOD.apply_source_decisions(rows, [
            {"path": "requirements-v1.md", "authority": "DRAFT_REFERENCE_HISTORY"},
            {"path": "requirements-final.md", "authority": "HUMAN_APPROVED", "status": "CURRENT", "supersedes": ["requirements-v1.md"]},
        ])
        self.assertEqual(rows[0]["status"], "SUPERSEDED")
        self.assertEqual(rows[0]["superseded_by"], ["SRC-0002"])
        self.assertEqual(rows[1]["supersedes"], ["SRC-0001"])
        self.assertEqual(rows[1]["authority"], "HUMAN_APPROVED")

    def test_unique_higher_authority_resolves_explicit_conflict_group(self):
        rows = self.records()
        MOD.apply_source_decisions(rows, [
            {"path": "requirements-v1.md", "authority": "DRAFT_REFERENCE_HISTORY", "conflict_group": "REQ"},
            {"path": "requirements-final.md", "authority": "HUMAN_APPROVED", "conflict_group": "REQ"},
        ])
        groups = MOD.build_conflict_groups(rows)
        self.assertEqual(groups[0]["status"], "RESOLVED_BY_EXPLICIT_AUTHORITY")
        self.assertFalse(groups[0]["blocking"])
        self.assertEqual(groups[0]["winning_source_id"], "SRC-0002")

    def test_equal_authority_conflicting_content_blocks(self):
        rows = self.records()
        MOD.apply_source_decisions(rows, [
            {"path": "requirements-v1.md", "authority": "DECLARED_PRIMARY", "conflict_group": "REQ"},
            {"path": "requirements-final.md", "authority": "DECLARED_PRIMARY", "conflict_group": "REQ"},
        ])
        groups = MOD.build_conflict_groups(rows)
        self.assertEqual(groups[0]["status"], "SOURCE CONFLICT")
        self.assertTrue(groups[0]["blocking"])

    def test_stable_requirement_ids_do_not_depend_on_input_order(self):
        rows = self.records()
        reqs = [
            {"source_path": "requirements-final.md", "source_location": "H2", "original_wording": "Second"},
            {"source_path": "requirements-v1.md", "source_location": "H1", "original_wording": "First"},
        ]
        a = MOD.normalize_requirements(reqs, rows)
        b = MOD.normalize_requirements(list(reversed(reqs)), rows)
        self.assertEqual(a, b)
        self.assertEqual([x["requirement_id"] for x in a], ["SRCREQ-0001", "SRCREQ-0002"])

    def test_architecture_stack_and_unknowns_are_explicit_not_inferred(self):
        payload = {
            "observed_architecture": {"api": "REST"},
            "declared_architecture": {"api": "REST v2"},
            "approved_architecture": {"api": "REST v1"},
            "observed_stack": {"language": "PHP"},
            "declared_stack": {"language": "PHP"},
            "approved_stack": {"language": "PHP 8.3"},
            "unknowns": ["hosting"],
        }
        self.assertEqual(MOD._object(payload, "approved_architecture")["api"], "REST v1")
        self.assertEqual(MOD._object(payload, "approved_stack")["language"], "PHP 8.3")
        self.assertEqual(MOD._list(payload, "unknowns"), ["hosting"])

    def test_invalid_authority_is_rejected(self):
        rows = self.records()
        with self.assertRaises(ValueError):
            MOD.apply_source_decisions(rows, [{"path": "requirements-v1.md", "authority": "FINAL_FILENAME_WINS"}])

    def test_atomic_json_is_parseable(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "state.json"
            MOD.atomic_json(p, {"ok": True})
            self.assertEqual(json.loads(p.read_text(encoding="utf-8")), {"ok": True})


if __name__ == "__main__":
    unittest.main()
