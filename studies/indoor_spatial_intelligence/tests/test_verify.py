import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPT = HERE / "scripts/verify.py"
spec = importlib.util.spec_from_file_location("research_verify", SCRIPT)
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class ReproducibilityTests(unittest.TestCase):
    def test_manifest_matches_manuscript(self):
        expected, frontier, index = verify.manifest()
        self.assertEqual(expected["metadata"]["retained"], 25135)
        self.assertEqual(sum(r["count"] for r in expected["eras"]), 25135)
        self.assertEqual(frontier["scopus_retrieved"], 176)
        self.assertEqual(len(index), 31)

    def test_empirical_without_files_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            code = verify.main([
                "--mode", "empirical",
                "--metadata", str(base / "missing_meta.csv"),
                "--frontier", str(base / "missing_frontier.csv"),
                "--evidence", str(base / "missing_evidence.csv"),
                "--flow", str(base / "missing_flow.json"),
            ])
            self.assertEqual(code, 1)

    def test_empirical_requires_paths(self):
        self.assertEqual(verify.main(["--mode", "empirical"]), 1)


if __name__ == "__main__":
    unittest.main()
