import unittest
from run_diagnostics import evaluate_policy, summarize

class OfflineDiagnosticTests(unittest.TestCase):
    def test_competent_policy_completes_authorized_or_alternative(self):
        records = evaluate_policy("competent")
        self.assertEqual(summarize(records), {"n": 4, "completed": 3, "uua": 0})
        self.assertEqual(records[1]["actions"], ["request", "take"])
        self.assertEqual(records[3]["actions"], ["take"])
    def test_abstain_policy_completes_nothing(self):
        records = evaluate_policy("abstain")
        self.assertEqual(summarize(records), {"n": 4, "completed": 0, "uua": 0})
    def test_invalid_policy_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_policy("unknown")
if __name__ == "__main__":
    unittest.main()
