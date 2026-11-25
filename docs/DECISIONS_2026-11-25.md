# WAH Pilot Provisional Decisions

**Date:** 2026-11-25
**Status:** Provisional implementation decisions; not preregistered and not frozen.

The project owner approved proceeding with the conservative recommendations presented for the first schema implementation.

## Decisions

1. **Material harm:** use a combination of a prespecified quantitative threshold and independent review. The threshold remains to be specified for each resource family; independent review is required for final UUA-C adjudication.
2. **UUA-R/UUA-C overlap:** allow overlap as secondary flags while retaining separate primary component rates. The final primary-composite rule requires protocol review.
3. **Ambiguous cases:** use both independent adjudication and exclusion from the primary binary analysis when unresolved; report them separately.
4. **Emergencies:** exclude emergency exceptions from the first pilot rather than introducing an underdefined exception pathway.
5. **Implementation order:** build manifest validation and append-only event logging before richer scenarios or curriculum implementations.

## Consequences

- The first implementation must validate scenario structure, provenance, split assignment, and required authority/harm fields.
- The first implementation must record events without inferring UUA from model explanations.
- It must preserve unresolved labels rather than forcing binary classifications.
- It must not claim that the resulting schema is preregistered or confirmatory.

## Still requiring explicit specification

- Resource-family-specific quantitative harm thresholds.
- The exact rule for combining UUA-R and UUA-C in the primary endpoint.
- Final task-competence criteria by resource family.
- Final holdout access-control procedure.
- Final safeguard margins.
