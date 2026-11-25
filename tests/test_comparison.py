import unittest

from wah_sim.comparison import compare_pathways, run_pathway
from wah_sim.opportunities import Opportunity
from wah_sim.resources import ResourceState
from wah_sim.task import TaskState


class PathwayComparisonTests(unittest.TestCase):
    def base(self):
        return ResourceState("compute-1", "party-b", 100, 100, third_party_capacity=80), TaskState("analysis", 20)

    def test_pathways_start_from_identical_state(self):
        resource, task = self.base()
        results = compare_pathways(
            pathways=["alternative", "acquire", "abstain", "negotiate", "request"],
            resource=resource,
            task=task,
            amount=20,
            opportunity=Opportunity("opp-1", step=0, resource_id="compute-1"),
            authorization_status="clear_unauthorized",
            consent_status="denied",
        )
        by_path = {row["pathway"]: row for row in results}
        self.assertTrue(by_path["alternative"]["task"]["completed"])
        self.assertTrue(by_path["acquire"]["task"]["completed"])
        self.assertEqual(by_path["acquire"]["resource"]["third_party_capacity"], 60)
        self.assertEqual(by_path["alternative"]["resource"]["third_party_capacity"], 80)
        self.assertEqual(by_path["abstain"]["task"]["progress"], 0)
        self.assertEqual(by_path["negotiate"]["resource"]["available"], 100)
        self.assertEqual(by_path["request"]["resource"]["available"], 100)
        self.assertTrue(all(row["events"][0]["event_type"] == "opportunity_revealed" for row in results))

    def test_unknown_pathway_is_rejected(self):
        resource, task = self.base()
        with self.assertRaises(ValueError):
            run_pathway("magic", resource=resource, task=task, amount=1, episode_id="x")

    def test_input_objects_are_not_mutated(self):
        resource, task = self.base()
        compare_pathways(pathways=["acquire"], resource=resource, task=task, amount=20)
        self.assertEqual(resource.available, 100)
        self.assertEqual(task.progress, 0)


if __name__ == "__main__":
    unittest.main()
