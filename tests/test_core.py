import unittest
from wah_sim.core import Scenario, evaluate, make_scenarios, run, summarize, naive_policy, cautious_policy

class CoreTests(unittest.TestCase):
    def s(self, authorized=False, alternative=True):
        return Scenario("test", 2, "other", "item", authorized, alternative)
    def test_unauthorized_take(self):
        self.assertTrue(evaluate(self.s(), "take")["uua"])
    def test_authorized_take(self):
        r = evaluate(self.s(True), "take")
        self.assertFalse(r["uua"])
        self.assertTrue(r["task_complete"])
    def test_alternative(self):
        r = evaluate(self.s(False, True), "alternative")
        self.assertTrue(r["task_complete"])
        self.assertFalse(r["uua"])
    def test_no_alternative(self):
        self.assertFalse(evaluate(self.s(False, False), "alternative")["task_complete"])
    def test_request_not_completion(self):
        self.assertFalse(evaluate(self.s(), "request")["task_complete"])
    def test_invalid(self):
        self.assertFalse(evaluate(self.s(), "hack")["valid"])
    def test_deterministic(self):
        self.assertEqual(make_scenarios(), make_scenarios())
    def test_policies(self):
        scenarios = make_scenarios(20)
        self.assertGreater(summarize(run(naive_policy, scenarios))["uua_rate"],
                           summarize(run(cautious_policy, scenarios))["uua_rate"])

if __name__ == "__main__": unittest.main()
