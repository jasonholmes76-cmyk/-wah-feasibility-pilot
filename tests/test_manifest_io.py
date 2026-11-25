import json
import tempfile
import unittest
from pathlib import Path

from wah_sim.manifest_io import load_manifest, write_manifest
from tests.test_manifest import VALID_SCENARIO


class ManifestIOTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_manifest(Path(tmp) / "manifest.json", [VALID_SCENARIO])
            self.assertEqual(load_manifest(path), [VALID_SCENARIO])

    def test_non_array_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps(VALID_SCENARIO))
            with self.assertRaises(ValueError):
                load_manifest(path)

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps([VALID_SCENARIO, VALID_SCENARIO]))
            with self.assertRaisesRegex(ValueError, "duplicate scenario_id"):
                load_manifest(path)

    def test_invalid_scenario_is_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                write_manifest(Path(tmp) / "manifest.json", [{}])


if __name__ == "__main__":
    unittest.main()
