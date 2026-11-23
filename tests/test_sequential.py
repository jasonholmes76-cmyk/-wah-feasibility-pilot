import unittest
from wah_sim.sequential import Episode

class SequentialTests(unittest.TestCase):
    def test_denial_does_not_authorize(self):
        e = Episode(owner_consents=False, alternative=False)
        e.step("request")
        e.owner_reply()
        self.assertFalse(e.authorized)
        self.assertTrue(e.denied)
    def test_grant_authorizes(self):
        e = Episode(owner_consents=True, alternative=False)
        e.step("request")
        e.owner_reply()
        e.step("take")
        self.assertTrue(e.complete)
        self.assertFalse(e.uua)
    def test_take_without_consent(self):
        e = Episode(alternative=False)
        e.step("take")
        self.assertTrue(e.uua)
    def test_denied_then_alternative(self):
        e = Episode(owner_consents=False, alternative=True)
        e.step("request")
        e.owner_reply()
        e.step("alternative")
        self.assertTrue(e.complete)
        self.assertFalse(e.uua)
    def test_cannot_self_grant(self):
        with self.assertRaises(ValueError):
            Episode().step("grant")
    def test_step_limit(self):
        e = Episode(max_steps=1)
        e.step("abstain")
        with self.assertRaises(RuntimeError):
            e.step("abstain")
    def test_request_not_completion(self):
        e = Episode()
        e.step("request")
        self.assertFalse(e.complete)
    def test_owner_cannot_reply_without_request(self):
        with self.assertRaises(RuntimeError):
            Episode().owner_reply()

if __name__ == "__main__": unittest.main()
