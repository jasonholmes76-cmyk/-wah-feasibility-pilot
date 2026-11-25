"""Append-only episode event logging.

The logger records observable events and state deltas. It deliberately does
not infer UUA, harm, or ethical justification.
"""
import json
from pathlib import Path


class EventLog:
    def __init__(self, episode_id):
        if not episode_id:
            raise ValueError("episode_id is required")
        self.episode_id = episode_id
        self._events = []

    @property
    def events(self):
        return list(self._events)

    def append(self, *, step, actor, event_type, action=None, resource_id=None,
               completed=None, state_delta=None, metadata=None):
        if not isinstance(step, int) or step < 0:
            raise ValueError("step must be a non-negative integer")
        if not actor or not event_type:
            raise ValueError("actor and event_type are required")
        event = {
            "episode_id": self.episode_id,
            "event_index": len(self._events),
            "step": step,
            "actor": actor,
            "event_type": event_type,
            "action": action,
            "resource_id": resource_id,
            "completed": completed,
            "state_delta": state_delta or {},
            "metadata": metadata or {},
        }
        self._events.append(event)
        return dict(event)

    def write_jsonl(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as output:
            for event in self._events:
                output.write(json.dumps(event, sort_keys=True) + "\n")
        return path
