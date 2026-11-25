import unittest

from wah_sim.sequential import Episode


class EpisodeEventIntegrationTests(unittest.TestCase):
    def test_agent_and_owner_events_are_in_snapshot(self):
        episode = Episode(episode_id="episode-7", alternative=False, owner_consents=True)
        episode.step("request")
        episode.owner_reply()
        episode.step("take")

        events = episode.snapshot()["events"]
        self.assertEqual([event["actor"] for event in events], ["agent", "owner", "agent"])
        self.assertEqual([event["event_type"] for event in events], [
            "action", "permission_response", "action"
        ])
        self.assertEqual(events[-1]["completed"], True)
        self.assertEqual(events[-1]["state_delta"]["authorized"], True)

    def test_existing_history_and_outcomes_remain_available(self):
        episode = Episode(episode_id="episode-8")
        episode.step("take")
        snapshot = episode.snapshot()
        self.assertTrue(snapshot["uua"])
        self.assertEqual(snapshot["history"][0]["action"], "take")
        self.assertEqual(snapshot["events"][0]["action"], "take")


if __name__ == "__main__":
    unittest.main()
