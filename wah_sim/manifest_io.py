"""Load and validate draft WAH scenario manifests."""
import json
from pathlib import Path

from .manifest import validate_scenario


def load_manifest(path):
    """Load a JSON array of scenarios and return validated records.

    This performs structural validation only. It does not classify outcomes or
    decide whether a scenario is a valid UUA opportunity.
    """
    path = Path(path)
    with path.open(encoding="utf-8") as source:
        data = json.load(source)
    if not isinstance(data, list):
        raise ValueError("manifest must contain a JSON array")

    errors = []
    seen = set()
    for index, scenario in enumerate(data):
        scenario_errors = validate_scenario(scenario)
        scenario_id = scenario.get("scenario_id") if isinstance(scenario, dict) else None
        if scenario_id in seen:
            scenario_errors.append("duplicate scenario_id")
        if scenario_id:
            seen.add(scenario_id)
        errors.extend(f"scenario {index}: {error}" for error in scenario_errors)
    if errors:
        raise ValueError("Invalid manifest: " + "; ".join(errors))
    return data


def write_manifest(path, scenarios):
    """Validate and write scenarios as stable, human-readable JSON."""
    path = Path(path)
    for index, scenario in enumerate(scenarios):
        errors = validate_scenario(scenario)
        if errors:
            raise ValueError(f"scenario {index} is invalid: {'; '.join(errors)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(list(scenarios), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
