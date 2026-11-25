import json
import unittest
from unittest.mock import patch
from wah_sim.gemini_adapter import choose_action, discover_model

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

    def test_discovery_prefers_newest_non_preview_flash_model(self):
        payload = {
            "models": [
                {"name": "models/gemini-2.0-flash", "supportedGenerationMethods": ["generateContent"]},
                {"name": "models/gemini-3.1-flash-lite", "supportedGenerationMethods": ["generateContent"]},
                {"name": "models/gemini-4.0-flash-preview", "supportedGenerationMethods": ["generateContent"]},
            ]
        }
        with patch("wah_sim.gemini_adapter.urlopen", return_value=FakeResponse(payload)):
            self.assertEqual(discover_model("fake"), "gemini-3.1-flash-lite")

if __name__ == "__main__": unittest.main()
