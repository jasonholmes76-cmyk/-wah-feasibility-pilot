import unittest

from wah_sim.authority import validate_authority_status, validate_consent_status
from wah_sim.resources import ResourceState
from wah_sim.sequential import Episode


class AuthorityConsentTests(unittest.TestCase):
    def test_valid_states_are_accepted(self):
        self.assertEqual(validate_authority_status("ambiguous"), "ambiguous")
        self.assertEqual(validate_consent_status("contested"), "contested")

    def test_invalid_states_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_authority_status("maybe")
        with self.assertRaises(ValueError):
            validate_consent_status("maybe")

    def test_states_are_recorded_without_automatic_classification(self):
        episode = Episode(episode_id="authority-1")
        resource = ResourceState("compute-1", "party-b", 10, 10)
        episode.acquire_resource(
            resource,
            2,
            authorization_status="contested",
            consent_status="unknown",
        )
        event = episode.snapshot()["events"][0]
        self.assertEqual(event["state_delta"]["authorization_status"], "contested")
        self.assertEqual(event["state_delta"]["consent_status"], "unknown")
        self.assertFalse("uua" in event["state_delta"])


if __name__ == "__main__":
    unittest.main()
