import unittest

from wah_sim.resources import ResourceState
from wah_sim.sequential import Episode


class ResourceEventIntegrationTests(unittest.TestCase):
    def test_completed_acquisition_emits_attempt_and_completion(self):
        episode = Episode(episode_id="resource-episode-1")
        resource = ResourceState("compute-1", "party-b", 100, 100, third_party_capacity=80)
        result = episode.acquire_resource(resource, 20)
        self.assertTrue(result["completed"])
        events = episode.snapshot()["events"]
        self.assertEqual([event["event_type"] for event in events], [
            "acquisition_attempt", "acquisition_completed"
        ])
        self.assertEqual(events[0]["completed"], False)
        self.assertEqual(events[1]["completed"], True)

    def test_failed_acquisition_emits_no_state_change_completion(self):
        episode = Episode(episode_id="resource-episode-2")
        resource = ResourceState("compute-2", "party-b", 10, 5)
        result = episode.acquire_resource(resource, 6)
        self.assertFalse(result["completed"])
        events = episode.snapshot()["events"]
        self.assertEqual(events[-1]["event_type"], "acquisition_failed")
        self.assertEqual(events[-1]["completed"], False)
        self.assertEqual(events[0]["state_delta"]["resource_before"], events[-1]["state_delta"]["resource_after"])


if __name__ == "__main__":
    unittest.main()
