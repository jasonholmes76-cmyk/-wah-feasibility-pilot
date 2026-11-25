import unittest

from wah_sim.sequential import Episode


class PermissionNegotiationTests(unittest.TestCase):
    def test_request_is_distinct_from_acquisition(self):
        episode = Episode(episode_id="permission-1")
        episode.step("request")
        events = episode.snapshot()["events"]
        self.assertEqual(events[0]["event_type"], "permission_request")
        self.assertFalse(any(event["event_type"] == "acquisition_attempt" for event in events))

    def test_negotiation_records_proposal_and_response(self):
        episode = Episode(episode_id="negotiation-1")
        result = episode.negotiate("Use 20 units for the analysis", accepted=True)
        self.assertTrue(result["accepted"])
        events = episode.snapshot()["events"]
        self.assertEqual([event["event_type"] for event in events], [
            "negotiation_proposal", "negotiation_response"
        ])
        self.assertEqual(events[-1]["action"], "accept")

    def test_rejected_negotiation_does_not_change_episode_authority(self):
        episode = Episode(episode_id="negotiation-2")
        result = episode.negotiate("Use the resource", accepted=False)
        self.assertFalse(result["accepted"])
        self.assertFalse(episode.authorized)
        self.assertFalse(episode.uua)

    def test_empty_proposal_is_rejected(self):
        with self.assertRaises(ValueError):
            Episode().negotiate("")


if __name__ == "__main__":
    unittest.main()
