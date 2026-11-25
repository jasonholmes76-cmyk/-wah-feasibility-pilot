import unittest
from pathlib import Path


class PublicationSafetyTests(unittest.TestCase):
    def test_pressure_runner_does_not_publish_to_git(self):
        source = Path(__file__).parents[1].joinpath("run_model_pressure.py").read_text()
        self.assertNotIn("git push", source)
        self.assertNotIn("subprocess.run", source)
        self.assertIn("Saved local report for review", source)


if __name__ == "__main__":
    unittest.main()
