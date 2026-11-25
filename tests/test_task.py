import unittest

from wah_sim.task import TaskState
from wah_sim.sequential import Episode


class TaskStateTests(unittest.TestCase):
    def test_capacity_completes_task(self):
        task = TaskState("analysis", required_capacity=10)
        result = task.apply_capacity(10)
        self.assertTrue(result["state_after"]["completed"])
        self.assertEqual(task.progress, 10)

    def test_partial_capacity_is_not_completion(self):
        task = TaskState("analysis", required_capacity=10)
        task.apply_capacity(4)
        self.assertFalse(task.completed)
        self.assertFalse(task.timed_out)

    def test_deadline_can_fail_task(self):
        task = TaskState("analysis", required_capacity=10, deadline=2)
        task.advance_step()
        task.advance_step()
        self.assertFalse(task.completed)
        self.assertTrue(task.timed_out)

    def test_episode_records_task_outcome(self):
        episode = Episode(episode_id="task-episode")
        task = TaskState("analysis", required_capacity=5)
        episode.apply_task_capacity(task, 5)
        event = episode.snapshot()["events"][-1]
        self.assertEqual(event["event_type"], "task_completed")
        self.assertTrue(event["completed"])

    def test_invalid_task_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            TaskState("", required_capacity=1)
        with self.assertRaises(ValueError):
            TaskState("x", required_capacity=0)
        task = TaskState("x", required_capacity=1)
        with self.assertRaises(ValueError):
            task.apply_capacity(0)


if __name__ == "__main__":
    unittest.main()
