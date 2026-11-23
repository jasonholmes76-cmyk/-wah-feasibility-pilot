# WAH v1.14 feasibility protocol (DRAFT; NOT preregistered)

**Status:** Engineering scaffold only. No trained intervention or D/E comparison.

## Research question
Does v1.14 E reduce unjustified unilateral acquisition (UUA) relative to D on held-out Tier 2/3 scenarios while preserving legitimate task competence? Verify exact arm definitions and direction from the canonical manuscript before implementation.

## Estimand
Experimental unit: scenario-seed-model rollout. Pair scenario IDs and seeds across conditions. Primary estimand: E-minus-D probability of UUA among valid opportunities. Report absolute rates and clustered uncertainty by scenario family.

## Simulator limitations
Current resources have owner, authorization and alternative availability. Actions: take, request, alternative, abstain. Unauthorized take is UUA by construction. Requests do not automatically grant permission. This is an infrastructure test, not a validated reciprocity measure.

## Required upgrades
1. Define legitimate authority, contested rights, emergencies, and ambiguity.
2. Add sequential state transitions, negotiation, consent, scarcity, and competing objectives.
3. Independently label scenarios; quantify agreement and adjudicate.
4. Build truly held-out Tier 2/3 families, negative controls and adversarial pressure; check leakage.
5. Train D/E from identical checkpoints with matched optimization, seeds and budgets.
6. Measure task completion, invalid actions, refusals and generalization.

## Feasibility gates
Reproducible scoring; valid UUA opportunities; baseline model competence above no-action; reliable labels; training within $25 hard ceiling. Free compute first. No paid compute without user approval.

## Sampling and analysis
Engineering targets: 30 development and 100 held-out scenarios; NOT statistically powered sample sizes. Pilot exploratory. Use paired analysis with scenario-family clustered uncertainty, multiple seeds and all failures. No tuning against held-out treatment differences.

## Change control
Verify v1.14 D/E/G definitions. Freeze this protocol by commit SHA and timestamp before treatment comparisons. Maximum two pre-freeze simulator/scoring revisions after fixtures; document reasons and commits. Null results are reportable. Positive results do not uniquely identify reciprocity as mechanism.
