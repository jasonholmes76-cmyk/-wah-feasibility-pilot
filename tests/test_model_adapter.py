import unittest
from unittest.mock import patch
from wah_sim.model_adapter import choose_action

class ModelAdapterTests(unittest.TestCase):
    def test_requires_configuration(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                choose_action({})
    def test_rejects_insecure_remote_url(self):
        with self.assertRaises(ValueError):
            choose_action({}, endpoint="http://example.com/v1/chat/completions", model="test")
    def test_accepts_mocked_response(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, *args): return b'{"choices":[{"message":{"content":"request"}}]}'
        with patch("wah_sim.model_adapter.urlopen", return_value=FakeResponse()):
            self.assertEqual(choose_action({}, endpoint="https://example.com/v1/chat/completions", model="test"), "request")
    def test_rejects_invalid_model_action(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, *args): return b'{"choices":[{"message":{"content":"grant"}}]}'
        with patch("wah_sim.model_adapter.urlopen", return_value=FakeResponse()):
            with self.assertRaises(ValueError):
                choose_action({}, endpoint="https://example.com/v1/chat/completions", model="test")

if __name__ == "__main__": unittest.main()
