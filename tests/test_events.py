import json
import tempfile
import unittest
from pathlib import Path

from wah_sim.events import EventLog


class EventLogTests(unittest.TestCase):
    def test_events_are_append_only_and_indexed(self):
        log = EventLog("episode-1")
        first = log.append(step=0, actor="environment", event_type="opportunity_revealed")
        second = log.append(
            step=1,
            actor="agent",
            event_type="acquisition_attempt",
            action="acquire_unilaterally",
            resource_id="resource-1",
            completed=False,
        )
        self.assertEqual(first["event_index"], 0)
        self.assertEqual(second["event_index"], 1)
        self.assertEqual(len(log.events), 2)
        self.assertEqual(log.events[0]["event_type"], "opportunity_revealed")

    def test_invalid_events_are_rejected(self):
        log = EventLog("episode-1")
        with self.assertRaises(ValueError):
            log.append(step=-1, actor="agent", event_type="timeout")
        with self.assertRaises(ValueError):
            log.append(step=0, actor="", event_type="timeout")

    def test_write_jsonl(self):
        log = EventLog("episode-2")
        log.append(step=0, actor="environment", event_type="opportunity_revealed")
        with tempfile.TemporaryDirectory() as tmp:
            path = log.write_jsonl(Path(tmp) / "events.jsonl")
            rows = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual(rows[0]["episode_id"], "episode-2")
        self.assertEqual(rows[0]["event_index"], 0)


if __name__ == "__main__":
    unittest.main()
