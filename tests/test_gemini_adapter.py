import json
import unittest
from unittest.mock import patch
from wah_sim.gemini_adapter import choose_action

class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, *args):
        return json.dumps(self.payload).encode()

class GeminiAdapterTests(unittest.TestCase):
    def test_requires_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                choose_action({})
    def test_rejects_bad_model(self):
        with self.assertRaises(ValueError):
            choose_action({}, api_key="fake", model="../invalid")
    def test_accepts_action(self):
        payload = {"candidates": [{"content": {"parts": [{"text": "request"}]}}]}
        with patch("wah_sim.gemini_adapter.urlopen", return_value=FakeResponse(payload)):
            self.assertEqual(choose_action({}, api_key="fake", model="gemini-test"), "request")
    def test_rejects_invalid_action(self):
        payload = {"candidates": [{"content": {"parts": [{"text": "grant"}]}}]}
        with patch("wah_sim.gemini_adapter.urlopen", return_value=FakeResponse(payload)):
            with self.assertRaises(ValueError):
                choose_action({}, api_key="fake", model="gemini-test")

if __name__ == "__main__": unittest.main()
