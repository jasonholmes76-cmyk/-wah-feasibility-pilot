import json
import unittest
from pathlib import Path

from wah_sim.sequential import Episode


class MultiStepFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).parents[1] / "fixtures" / "multistep_episodes_draft.json"
        cls.fixtures = json.loads(path.read_text())

    def run_fixture(self, fixture):
        episode = Episode(episode_id=fixture["episode_id"], **fixture["initial"])
        owner_replies = set(fixture["owner_reply_after"])
        for action in fixture["agent_actions"]:
            if episode.complete or episode.uua or episode.steps >= episode.max_steps:
                break
            episode.step(action)
            if action in owner_replies and episode.steps < episode.max_steps:
                episode.owner_reply()
        result = episode.snapshot()
        result["timed_out"] = not episode.complete and not episode.uua and episode.steps >= episode.max_steps
        return result

    def test_all_draft_multistep_fixtures(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["episode_id"]):
                result = self.run_fixture(fixture)
                for key, expected in fixture["expected"].items():
                    self.assertEqual(result[key], expected)
                self.assertGreaterEqual(len(result["events"]), 1)

    def test_fixture_ids_are_unique(self):
        ids = [fixture["episode_id"] for fixture in self.fixtures]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
