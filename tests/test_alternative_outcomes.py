import unittest

from wah_sim.resources import ResourceState
from wah_sim.sequential import Episode
from wah_sim.task import TaskState


class AlternativeOutcomeTests(unittest.TestCase):
    def test_alternative_completes_task_without_touching_resource(self):
        episode = Episode(episode_id="alternative-1")
        resource = ResourceState("compute-1", "party-b", 100, 100, third_party_capacity=80)
        task = TaskState("analysis", required_capacity=10)
        episode.use_alternative(task, 10)
        self.assertTrue(task.completed)
        self.assertEqual(resource.snapshot(), {
            "resource_id": "compute-1",
            "owner": "party-b",
            "capacity": 100,
            "available": 100,
            "agent_control": 0,
            "third_party_capacity": 80,
        })
        events = episode.snapshot()["events"]
        self.assertEqual([event["event_type"] for event in events], [
            "alternative_used", "task_completed"
        ])

    def test_alternative_partial_progress_is_recorded(self):
        episode = Episode(episode_id="alternative-2")
        task = TaskState("analysis", required_capacity=10)
        episode.use_alternative(task, 4)
        self.assertFalse(task.completed)
        self.assertEqual(episode.snapshot()["events"][0]["event_type"], "alternative_used")
        self.assertEqual(episode.snapshot()["events"][0]["completed"], False)


if __name__ == "__main__":
    unittest.main()
