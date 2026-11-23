"""Run the selected model baseline and publish only a minimal, sanitized summary.

No API keys, prompts, raw responses, or exception text are committed.
Requires Codespaces git push permission. Does not alter unrelated files.
"""
import json
import os
import subprocess
from pathlib import Path

from run_model_baseline import main as run_baseline

RESULTS = Path("outputs/model_baseline.jsonl")
PROVIDER = os.environ.get("WAH_PROVIDER", "gemini").lower()
if PROVIDER not in {"gemini", "claude", "openai"}:
    raise ValueError("Unsupported WAH_PROVIDER")
REPORT = Path(f"reports/latest_{PROVIDER}_baseline.json")

def main():
    run_baseline()
    records = [json.loads(line) for line in RESULTS.read_text().splitlines() if line.strip()]
    if len(records) != 4 or any(record.get("error") is not None for record in records):
        print("Baseline had errors or missing scenarios. Nothing published.")
        print("Check the Scenario lines above; share only the error descriptions, never keys.")
        return
    summary = {
        "study": "WAH exploratory baseline (not a treatment comparison)",
        "provider": PROVIDER,
        "model": (os.environ.get("WAH_CLAUDE_MODEL") if PROVIDER == "claude" else os.environ.get("WAH_GEMINI_MODEL") if PROVIDER == "gemini" else os.environ.get("WAH_MODEL_NAME")) or "auto",
        "scenario_count": len(records),
        "scenarios": [
            {
                "scenario_id": rec["scenario_id"],
                "authorized_initially": rec["scenario"]["authorized"],
                "alternative_available": rec["scenario"]["alternative"],
                "owner_consents": rec["scenario"]["owner_consents"],
                "complete": rec["outcome"]["complete"],
                "uua": rec["outcome"]["uua"],
                "actions": [h["action"] for h in rec["outcome"]["history"] if h["actor"] == "agent"],
            } for rec in records
        ],
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(summary, indent=2) + "\n")
    subprocess.run(["git", "add", "--", str(REPORT)], check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", str(REPORT)])
    if staged.returncode == 0:
        print("Report unchanged; already available in GitHub.")
        return
    if staged.returncode != 1:
        raise RuntimeError("Could not inspect staged report")
    subprocess.run(["git", "commit", "-m", f"Record sanitized {PROVIDER} baseline summary", "--", str(REPORT)], check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True)
    print(f"Published sanitized report to GitHub: {REPORT}")

if __name__ == "__main__":
    main()
