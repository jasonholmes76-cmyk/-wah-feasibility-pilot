import unittest

from wah_sim.resources import ResourceState


class ResourceStateTests(unittest.TestCase):
    def test_successful_acquisition_changes_observable_state(self):
        resource = ResourceState("compute-1", "party-b", 100, 100, third_party_capacity=80)
        result = resource.acquire(20)
        self.assertTrue(result["completed"])
        self.assertEqual(resource.available, 80)
        self.assertEqual(resource.agent_control, 20)
        self.assertEqual(resource.third_party_capacity, 60)
        self.assertNotEqual(result["state_before"], result["state_after"])

    def test_failed_acquisition_does_not_change_state(self):
        resource = ResourceState("compute-1", "party-b", 10, 5)
        before = resource.snapshot()
        result = resource.acquire(6)
        self.assertFalse(result["completed"])
        self.assertEqual(resource.snapshot(), before)

    def test_release_restores_capacity(self):
        resource = ResourceState("compute-1", "party-b", 10, 10)
        resource.acquire(4)
        resource.release(4)
        self.assertEqual(resource.available, 10)
        self.assertEqual(resource.agent_control, 0)

    def test_invalid_state_and_amounts_are_rejected(self):
        with self.assertRaises(ValueError):
            ResourceState("", "party-b", 10, 10)
        with self.assertRaises(ValueError):
            ResourceState("x", "party-b", 5, 6)
        resource = ResourceState("x", "party-b", 5, 5)
        with self.assertRaises(ValueError):
            resource.acquire(0)
        with self.assertRaises(ValueError):
            resource.release(1)


if __name__ == "__main__":
    unittest.main()
