import unittest
from pathlib import Path

from wah_sim.manifest_io import load_manifest


class DraftFixtureTests(unittest.TestCase):
    def test_endpoint_fixture_manifest_is_structurally_valid(self):
        path = Path(__file__).parents[1] / "fixtures" / "endpoint_scenarios_draft.json"
        scenarios = load_manifest(path)
        self.assertEqual(len(scenarios), 5)
        self.assertEqual(
            {scenario["scenario_id"] for scenario in scenarios},
            {"FIX-R-001", "FIX-A-001", "FIX-C-001", "FIX-B-001", "FIX-P-001"},
        )

    def test_fixture_splits_are_not_confirmatory_holdouts(self):
        path = Path(__file__).parents[1] / "fixtures" / "endpoint_scenarios_draft.json"
        scenarios = load_manifest(path)
        self.assertTrue(all(scenario["split"] == "development" for scenario in scenarios))
        self.assertTrue(all(not scenario["provenance"]["canonical_holdout"] for scenario in scenarios))


if __name__ == "__main__":
    unittest.main()
