# WAH Feasibility Pilot — Code Audit

**Date:** 2026-11-25
**Status:** Review memo; no code changes made.

## Verified baseline

- `python -m unittest discover -s tests -v`: 37 tests passed.
- The repository is an engineering scaffold, not a D/E treatment implementation.
- Existing reports are exploratory and explicitly not WAH efficacy evidence.

## Findings

### High priority: automatic publication and push from a runner

`run_model_pressure.py` stages a report, commits it, and runs `git push origin HEAD:main` when the report changes.

This is unsafe for a research workflow because a model-execution script can publish artifacts directly to the protected/default branch without human review. It also couples data generation to publication and can make an accidental or malformed run externally visible.

**Recommendation:** separate execution, report generation, review, commit, and push. The runner should write only to an ignored or explicitly designated output path. A separate human-approved publication command or CI workflow should handle commits and pushes.

### High priority: no real pressure incentive

`PressureCase.reward` and `unauthorized_bonus` are placed into the model prompt but do not affect the simulator, utility, state transition, or task objective. The pressure scenarios therefore describe temptation but do not implement a consequential incentive conflict.

**Recommendation:** specify and implement a state transition or decision objective in which legitimate and unauthorized actions have prespecified consequences. Keep descriptive prompt fields separate from implemented rewards.

### High priority: treatment conditions are absent

The runners use fixed hand-coded environments and model calls. No D, E, or G training implementation is present. Results must not be described as treatment effects.

### Medium priority: scenario generation is not a validated holdout design

`wah_sim/core.py::make_scenarios` assigns tiers by alternating index and draws only authorization and alternative availability from a seeded RNG. It does not construct scenario families, development/holdout boundaries, negative controls, or normative distribution shifts.

**Recommendation:** use a versioned scenario manifest with family IDs, split assignments, and frozen holdout metadata.

### Medium priority: UUA construct is currently narrow

The core evaluator labels only unauthorized `take` as UUA. It has no representation of contested authority, delegated control, emergency exceptions, ambiguity, or multi-agent resource effects.

**Recommendation:** expand the scenario state and predefine independent scoring rules before claiming construct validity.

### Medium priority: Gemini model-ranking bug

`wah_sim/gemini_adapter.py::discover_model` uses a raw regex containing a doubled backslash (`r"gemini-(\\d+)..."`). This does not match ordinary numeric model names as intended, so the version-ranking logic does not reliably prefer the newest model. The adapter may still work, but model selection is not behaving as documented.

**Recommendation:** add tests for model ranking and correct the regex before relying on automatic discovery.

### Medium priority: small and non-independent exploratory reports

The checked-in reports contain four baseline scenarios and six pressure scenarios. These are useful smoke tests but are not powered samples and should not be analyzed as inferential evidence.

### Low/medium priority: failure and timeout semantics

Timeouts, invalid actions, and API errors are recorded, but no prespecified analysis rule yet determines whether they count against competence, are treated as missing, or trigger repeat attempts. This must be frozen before treatment comparisons.

## Recommended order of work

1. Remove automatic commit/push behavior from model runners.
2. Add model-discovery tests and correct the Gemini ranking bug.
3. Create a versioned scenario manifest and split policy.
4. Define implemented incentive consequences separately from prompt descriptions.
5. Expand the simulator only after D/E/G definitions are verified against v1.14.
6. Freeze failure, timeout, and indeterminate-outcome rules.
7. Keep all model outputs and reports outside the canonical branch until reviewed.
