import unittest

from wah_sim.opportunities import Opportunity
from wah_sim.sequential import Episode


class OpportunityTests(unittest.TestCase):
    def test_scheduled_opportunity_is_recorded_as_environment_event(self):
        episode = Episode(episode_id="opportunity-1")
        opportunity = Opportunity("opp-1", step=3, resource_id="compute-1")
        snapshot = episode.reveal_opportunity(opportunity)
        event = episode.snapshot()["events"][0]
        self.assertEqual(snapshot["step"], 3)
        self.assertEqual(event["event_type"], "opportunity_revealed")
        self.assertEqual(event["actor"], "environment")
        self.assertEqual(event["state_delta"]["opportunity"]["opportunity_id"], "opp-1")

    def test_invalid_opportunity_is_rejected(self):
        with self.assertRaises(ValueError):
            Opportunity("", step=0, resource_id="x")
        with self.assertRaises(ValueError):
            Opportunity("x", step=-1, resource_id="x")


if __name__ == "__main__":
    unittest.main()
