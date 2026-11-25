"""Observable task-progress and competence outcomes."""
from dataclasses import dataclass


@dataclass
class TaskState:
    task_id: str
    required_capacity: int
    progress: int = 0
    steps: int = 0
    deadline: int | None = None
    completed: bool = False
    timed_out: bool = False

    def __post_init__(self):
        if not self.task_id:
            raise ValueError("task_id is required")
        if self.required_capacity <= 0:
            raise ValueError("required_capacity must be positive")
        if self.progress < 0 or self.steps < 0:
            raise ValueError("progress and steps must be non-negative")
        if self.deadline is not None and self.deadline <= 0:
            raise ValueError("deadline must be positive when provided")
        self._refresh_status()

    def _refresh_status(self):
        self.completed = self.progress >= self.required_capacity
        self.timed_out = (
            self.deadline is not None
            and self.steps >= self.deadline
            and not self.completed
        )

    def snapshot(self):
        return {
            "task_id": self.task_id,
            "required_capacity": self.required_capacity,
            "progress": self.progress,
            "steps": self.steps,
            "deadline": self.deadline,
            "completed": self.completed,
            "timed_out": self.timed_out,
        }

    def apply_capacity(self, amount: int):
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be a positive integer")
        before = self.snapshot()
        if not self.completed and not self.timed_out:
            self.progress += amount
            self._refresh_status()
        return {"state_before": before, "state_after": self.snapshot()}

    def advance_step(self):
        if not self.completed and not self.timed_out:
            self.steps += 1
            self._refresh_status()
        return self.snapshot()
