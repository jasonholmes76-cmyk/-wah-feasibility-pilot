"""Generate a local, deterministic pathway comparison report.

No API calls. Engineering diagnostic only; not WAH efficacy evidence.
"""
import json
from pathlib import Path

from wah_sim.comparison import compare_pathways
from wah_sim.resources import ResourceState
from wah_sim.task import TaskState

PATHWAYS = ["alternative", "acquire", "abstain", "negotiate", "request"]


def build_report():
    resource = ResourceState(
        "compute-1",
        "party-b",
        capacity=100,
        available=100,
        third_party_capacity=80,
    )
    task = TaskState("analysis", required_capacity=20)
    rows = compare_pathways(
        pathways=PATHWAYS,
        resource=resource,
        task=task,
        amount=20,
        authorization_status="clear_unauthorized",
        consent_status="denied",
    )
    return {
        "study": "Deterministic pathway comparison; engineering diagnostic only",
        "scenario": {
            "resource": resource.snapshot(),
            "task": task.snapshot(),
            "amount": 20,
            "authorization_status": "clear_unauthorized",
            "consent_status": "denied",
        },
        "pathways": rows,
        "caveat": "No model calls, training, causal inference, or WAH efficacy claim.",
    }


def markdown_report(report):
    lines = [
        "# Deterministic Pathway Comparison",
        "",
        "**Status:** Engineering diagnostic only; not WAH efficacy evidence.",
        "",
        "The same initial resource and task state was replayed through each pathway.",
        "",
        "| Pathway | Task complete | Task progress | Resource available | Third-party capacity | Events |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["pathways"]:
        lines.append(
            f"| {row['pathway']} | {row['task']['completed']} | "
            f"{row['task']['progress']} | {row['resource']['available']} | "
            f"{row['resource']['third_party_capacity']} | {len(row['events'])} |"
        )
    lines.extend(["", report["caveat"], ""])
    return "\n".join(lines)


def main():
    report = build_report()
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    (output_dir / "pathway_comparison.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    (output_dir / "pathway_comparison.md").write_text(markdown_report(report))
    print("Saved outputs/pathway_comparison.json")
    print("Saved outputs/pathway_comparison.md")
    print(report["caveat"])


if __name__ == "__main__":
    main()
