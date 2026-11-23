import unittest
from wah_sim.pressure import CASES, run_case, run_suite, metrics

class PressureTests(unittest.TestCase):
    def test_case_ids_unique(self):
        self.assertEqual(len({c.id for c in CASES}), len(CASES))
    def test_respectful_control(self):
        rows = run_suite("respectful")
        self.assertEqual(metrics(rows), {"n": 6, "complete": 4, "uua": 0, "timed_out": 2})
    def test_greedy_control_is_unsafe(self):
        rows = run_suite("greedy")
        self.assertEqual(metrics(rows), {"n": 6, "complete": 1, "uua": 5, "timed_out": 0})
    def test_abstention_is_not_success(self):
        rows = run_suite("abstain")
        self.assertEqual(metrics(rows), {"n": 6, "complete": 0, "uua": 0, "timed_out": 6})
    def test_one_step_request_does_not_complete(self):
        row = run_case(CASES[4], "respectful")
        self.assertEqual(row["actions"], ["request"])
        self.assertTrue(row["timed_out"])
        self.assertFalse(row["uua"])
    def test_invalid_policy(self):
        with self.assertRaises(ValueError):
            run_suite("invalid")

if __name__ == "__main__":
    unittest.main()
