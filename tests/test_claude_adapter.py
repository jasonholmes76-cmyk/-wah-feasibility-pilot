import json
import unittest
from unittest.mock import patch
from wah_sim.claude_adapter import choose_action

class Response:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return json.dumps({"content": [{"type": "text", "text": "request"}]}).encode()

class ClaudeAdapterTests(unittest.TestCase):
    def test_requires_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                choose_action({}, model="test")
    def test_requires_model(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                choose_action({}, api_key="fake")
    def test_request(self):
        with patch("wah_sim.claude_adapter.urlopen", return_value=Response()) as mocked:
            self.assertEqual(choose_action({}, api_key="fake", model="test"), "request")
            req = mocked.call_args.args[0]
            self.assertEqual(req.headers["X-api-key"], "fake")
            self.assertIn(b'"max_tokens": 64', req.data)
if __name__ == "__main__": unittest.main()
