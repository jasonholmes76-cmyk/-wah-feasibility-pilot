"""Scenario-level authority and consent state validation."""

AUTHORIZATION_STATES = {
    "clear_authorized",
    "clear_unauthorized",
    "ambiguous",
    "contested",
    "not_applicable",
}
CONSENT_STATES = {"granted", "denied", "unknown", "not_required", "contested"}


def validate_authority_status(status):
    if status not in AUTHORIZATION_STATES:
        raise ValueError(f"unknown authorization status: {status}")
    return status


def validate_consent_status(status):
    if status not in CONSENT_STATES:
        raise ValueError(f"unknown consent status: {status}")
    return status
