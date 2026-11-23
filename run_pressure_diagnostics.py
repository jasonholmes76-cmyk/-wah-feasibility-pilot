"""Zero-cost pressure diagnostics. No LLM calls. No WAH treatment comparison."""
import json
from pathlib import Path
from wah_sim.pressure import CASES, run_suite, metrics

def main():
    result = {
        "study": "WAH pressure-fixture engineering controls; NOT efficacy evidence",
        "cases": [{"id": c.id, "family": c.family, "description": c.description,
                   "deadline": c.deadline, "reward": c.reward,
                   "unauthorized_bonus": c.unauthorized_bonus} for c in CASES],
        "controls": {p: {"metrics": metrics(rows), "episodes": rows}
                     for p in ("abstain", "respectful", "greedy")
                     for rows in [run_suite(p)]},
    }
    path = Path("outputs/pressure_diagnostics.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    for p, item in result["controls"].items():
        m = item["metrics"]
        print(f"{p}: {m['complete']}/{m['n']} completed; {m['uua']} UUA; {m['timed_out']} timeouts")
    print(f"Saved: {path}")
    print("Engineering fixtures only; pressure labels are not yet validated.")

if __name__ == "__main__":
    main()
