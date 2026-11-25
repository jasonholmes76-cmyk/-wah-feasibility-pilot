"""Scheduled opportunity events for draft WAH episodes."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    step: int
    resource_id: str
    eligible: bool = True

    def __post_init__(self):
        if not self.opportunity_id or not self.resource_id:
            raise ValueError("opportunity_id and resource_id are required")
        if self.step < 0:
            raise ValueError("step must be non-negative")

    def snapshot(self):
        return {
            "opportunity_id": self.opportunity_id,
            "step": self.step,
            "resource_id": self.resource_id,
            "eligible": self.eligible,
        }
