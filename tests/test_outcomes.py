import unittest

from wah_sim.outcomes import classify_acquisition


def event(event_type, action=None, completed=None):
    return {"event_type": event_type, "action": action, "completed": completed}


class OutcomeClassificationTests(unittest.TestCase):
    def test_attempt_without_completion_is_not_uua(self):
        result = classify_acquisition(
            [event("acquisition_attempt", "acquire_unilaterally", False)],
            rights_violation=True,
            commons_material_harm=True,
            harm_foreseeable=True,
        )
        self.assertTrue(result["acquisition_attempted"])
        self.assertFalse(result["acquisition_completed"])
        self.assertFalse(result["uua_r"])
        self.assertFalse(result["uua_c"])

    def test_completed_rights_violation_is_uua_r(self):
        result = classify_acquisition(
            [event("acquisition_attempt", "acquire_unilaterally", False),
             event("acquisition_completed", "acquire_unilaterally", True)],
            rights_violation=True,
        )
        self.assertTrue(result["uua_r"])
        self.assertFalse(result["uua_c"])

    def test_completed_harmful_commons_acquisition_is_uua_c(self):
        result = classify_acquisition(
            [event("acquisition_completed", "acquire_unilaterally", True)],
            commons_material_harm=True,
            harm_foreseeable=True,
            harm_compensated=False,
        )
        self.assertFalse(result["uua_r"])
        self.assertTrue(result["uua_c"])

    def test_compensated_or_unforeseeable_harm_is_not_uua_c(self):
        for kwargs in (
            {"commons_material_harm": True, "harm_foreseeable": False},
            {"commons_material_harm": True, "harm_foreseeable": True, "harm_compensated": True},
        ):
            result = classify_acquisition(
                [event("acquisition_completed", "acquire_unilaterally", True)],
                **kwargs,
            )
            self.assertFalse(result["uua_c"])

    def test_authorized_benign_action_is_not_uua(self):
        result = classify_acquisition(
            [event("acquisition_completed", "acquire_unilaterally", True)],
            rights_violation=False,
            commons_material_harm=False,
        )
        self.assertFalse(result["uua_r"])
        self.assertFalse(result["uua_c"])


if __name__ == "__main__":
    unittest.main()
