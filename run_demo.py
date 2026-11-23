"""Hand-coded policy sanity checks, not WAH efficacy results."""
from pathlib import Path
import json
from wah_sim.core import make_scenarios, run, summarize, naive_policy, cautious_policy

def main():
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    scenarios = make_scenarios()
    for label, policy in [("naive_rule", naive_policy), ("cautious_rule", cautious_policy)]:
        rows = run(policy, scenarios)
        (out / f"{label}.jsonl").write_text("".join(json.dumps(r, sort_keys=True)+"\n" for r in rows))
        print(label, json.dumps(summarize(rows), sort_keys=True))
    print("Software sanity checks only; NOT WAH efficacy results.")

if __name__ == "__main__":
    main()
