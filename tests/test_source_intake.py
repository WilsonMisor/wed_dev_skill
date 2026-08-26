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

    def test_atomic_json_is_parseable(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "state.json"
            MOD.atomic_json(p, {"ok": True})
            self.assertEqual(json.loads(p.read_text(encoding="utf-8")), {"ok": True})


if __name__ == "__main__":
    unittest.main()
