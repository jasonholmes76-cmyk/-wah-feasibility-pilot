"""Observable resource state transitions for draft WAH scenarios.

This module models state changes only. It does not determine authorization,
harm, UUA, or ethical justification.
"""
from dataclasses import dataclass


@dataclass
class ResourceState:
    resource_id: str
    owner: str | None
    capacity: int
    available: int
    agent_control: int = 0
    third_party_capacity: int = 0

    def __post_init__(self):
        if not self.resource_id:
            raise ValueError("resource_id is required")
        if self.capacity < 0 or self.available < 0:
            raise ValueError("capacity and available must be non-negative")
        if self.available > self.capacity:
            raise ValueError("available cannot exceed capacity")
        if self.agent_control < 0 or self.third_party_capacity < 0:
            raise ValueError("control and third-party capacity must be non-negative")

    def snapshot(self):
        return {
            "resource_id": self.resource_id,
            "owner": self.owner,
            "capacity": self.capacity,
            "available": self.available,
            "agent_control": self.agent_control,
            "third_party_capacity": self.third_party_capacity,
        }

    def acquire(self, amount: int):
        """Apply an observable acquisition if capacity is available.

        Authorization and ethical classification are intentionally not inputs.
        The caller records those separately as scenario/adjudication data.
        """
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be a positive integer")
        if amount > self.available:
            return {
                "completed": False,
                "amount": amount,
                "state_before": self.snapshot(),
                "state_after": self.snapshot(),
            }
        before = self.snapshot()
        self.available -= amount
        self.agent_control += amount
        if self.third_party_capacity:
            self.third_party_capacity = max(0, self.third_party_capacity - amount)
        return {
            "completed": True,
            "amount": amount,
            "state_before": before,
            "state_after": self.snapshot(),
        }

    def release(self, amount: int):
        """Release agent-controlled capacity back to the resource."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be a positive integer")
        if amount > self.agent_control:
            raise ValueError("cannot release more than agent control")
        self.agent_control -= amount
        self.available += amount
        return self.snapshot()
