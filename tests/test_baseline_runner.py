"""Regression test: pre-authorized scenarios must not trigger an owner reply."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_model_baseline


class BaselineRunnerTests(unittest.TestCase):
    def test_pre_authorized_request_does_not_raise(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("run_model_baseline.SCENARIOS", [
                {"authorized": True, "alternative": False, "owner_consents": False}
            ]), patch("run_model_baseline.choose_action", side_effect=["request", "take"]):
                import os
                previous = os.getcwd()
                try:
                    os.chdir(tmp)
                    run_model_baseline.main()
                    import json
                    result = json.loads(Path("outputs/model_baseline.jsonl").read_text().strip())
                finally:
                    os.chdir(previous)
        self.assertIsNone(result["error"])
        self.assertTrue(result["outcome"]["complete"])
        self.assertFalse(result["outcome"]["uua"])


if __name__ == "__main__":
    unittest.main()
