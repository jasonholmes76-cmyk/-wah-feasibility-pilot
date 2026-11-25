import unittest

from wah_sim.resources import ResourceState
from wah_sim.sequential import Episode
from wah_sim.task import TaskState


class ResourceTaskCouplingTests(unittest.TestCase):
    def test_successful_acquisition_advances_task_and_reduces_third_party_capacity(self):
        episode = Episode(episode_id="coupled-1")
        resource = ResourceState("compute-1", "party-b", 100, 100, third_party_capacity=80)
        task = TaskState("analysis", required_capacity=20)
        result = episode.acquire_for_task(resource, task, 20)
        self.assertTrue(result["acquisition"]["completed"])
        self.assertTrue(result["task"]["state_after"]["completed"])
        self.assertEqual(resource.third_party_capacity, 60)
        self.assertEqual([event["event_type"] for event in episode.snapshot()["events"]], [
            "acquisition_attempt", "acquisition_completed", "task_completed"
        ])

    def test_failed_acquisition_does_not_advance_task(self):
        episode = Episode(episode_id="coupled-2")
        resource = ResourceState("compute-2", "party-b", 10, 5, third_party_capacity=5)
        task = TaskState("analysis", required_capacity=6)
        result = episode.acquire_for_task(resource, task, 6)
        self.assertFalse(result["acquisition"]["completed"])
        self.assertEqual(task.progress, 0)
        self.assertEqual(resource.third_party_capacity, 5)
        self.assertEqual(len(episode.snapshot()["events"]), 2)


if __name__ == "__main__":
    unittest.main()
