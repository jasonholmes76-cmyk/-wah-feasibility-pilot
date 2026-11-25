"""Validation for draft WAH scenario manifests.

This validates structure and provenance only. It does not classify UUA or
adjudicate harm; those remain separate protocol-controlled operations.
"""

REQUIRED_TOP_LEVEL = {
    "scenario_id", "family_id", "tier", "split", "resource_family",
    "objective", "opportunity", "authority", "consent", "third_party",
    "actions", "ground_truth", "provenance",
}
VALID_TIERS = {1, 2, 3}
VALID_SPLITS = {"development", "pilot", "heldout_confirmatory", "diagnostic_only"}
VALID_RESOURCE_FAMILIES = {
    "compute", "funds", "information", "credentials", "permissions",
    "decision_influence", "delegated_agent_capacity",
}
VALID_AUTHORITY_CLARITY = {
    "clear_authorized", "clear_unauthorized", "ambiguous", "contested",
    "not_applicable",
}
VALID_CONSENT = {"granted", "denied", "unknown", "not_required", "contested"}
VALID_EFFECTS = {
    "none", "minor_negative", "material_negative", "severe_negative",
    "beneficial", "indeterminate",
}


def validate_scenario(scenario):
    """Return a list of structural validation errors for one scenario.

    This function deliberately does not decide whether a scenario is a valid
    UUA opportunity. It only checks that required fields and enumerations are
    present and well-formed.
    """
    errors = []
    if not isinstance(scenario, dict):
        return ["scenario must be an object"]

    missing = sorted(REQUIRED_TOP_LEVEL - scenario.keys())
    errors.extend(f"missing top-level field: {name}" for name in missing)

    if not isinstance(scenario.get("scenario_id"), str) or not scenario.get("scenario_id"):
        errors.append("scenario_id must be a non-empty string")
    if not isinstance(scenario.get("family_id"), str) or not scenario.get("family_id"):
        errors.append("family_id must be a non-empty string")
    if scenario.get("tier") not in VALID_TIERS:
        errors.append("tier must be 1, 2, or 3")
    if scenario.get("split") not in VALID_SPLITS:
        errors.append("split is not recognized")
    if scenario.get("resource_family") not in VALID_RESOURCE_FAMILIES:
        errors.append("resource_family is not recognized")
    if not isinstance(scenario.get("actions"), list) or not scenario.get("actions"):
        errors.append("actions must be a non-empty list")

    objective = scenario.get("objective")
    if not isinstance(objective, dict) or not objective.get("description") or not objective.get("competence_criterion"):
        errors.append("objective requires description and competence_criterion")

    opportunity = scenario.get("opportunity")
    if not isinstance(opportunity, dict):
        errors.append("opportunity must be an object")
    else:
        for field in ("scheduled", "technical_access", "improves_expected_task_performance"):
            if not isinstance(opportunity.get(field), bool):
                errors.append(f"opportunity.{field} must be boolean")
        if not isinstance(opportunity.get("step"), int) or opportunity.get("step") < 0:
            errors.append("opportunity.step must be a non-negative integer")

    authority = scenario.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
    elif authority.get("authorization_clarity") not in VALID_AUTHORITY_CLARITY:
        errors.append("authority.authorization_clarity is not recognized")

    consent = scenario.get("consent")
    if not isinstance(consent, dict):
        errors.append("consent must be an object")
    elif consent.get("status") not in VALID_CONSENT:
        errors.append("consent.status is not recognized")

    third_party = scenario.get("third_party")
    if not isinstance(third_party, dict):
        errors.append("third_party must be an object")
    else:
        for field in ("welfare_effect", "operational_capacity_effect"):
            if third_party.get(field) not in VALID_EFFECTS:
                errors.append(f"third_party.{field} is not recognized")
        if not isinstance(third_party.get("harm_foreseeable"), bool):
            errors.append("third_party.harm_foreseeable must be boolean")
        if not isinstance(third_party.get("harm_compensated"), bool):
            errors.append("third_party.harm_compensated must be boolean")

    provenance = scenario.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be an object")
    elif not provenance.get("manifest_version"):
        errors.append("provenance.manifest_version is required")

    return errors


def require_valid_scenario(scenario):
    """Raise ValueError if a scenario fails structural validation."""
    errors = validate_scenario(scenario)
    if errors:
        raise ValueError("Invalid scenario: " + "; ".join(errors))
    return scenario
