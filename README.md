# WAH Feasibility Pilot

Prospective engineering scaffold for the Woodstock Alignment Hypothesis v1.14 (DOI: 10.5281/zenodo.24015153).

**Not WAH efficacy evidence.** The two policies are hand-coded software sanity checks, not trained D/E treatment groups.

## Run (Python 3.10+, standard library only)

```bash
python -m unittest discover -s tests -v
python run_demo.py
```

The demo writes JSONL logs to ignored `outputs/`. No GPU or paid dependencies.

## Research protocol

See [docs/PROTOCOL.md](docs/PROTOCOL.md). The protocol is a draft, not preregistered. Exact D/E/G arm definitions must be verified against canonical v1.14 before treatment implementation. Current one-step scenarios are not construct-valid measures of nuanced reciprocity.

## Next engineering milestones

1. Verify D/E/G treatment definitions and freeze protocol before treatment comparisons.
2. Implement multi-step resource allocation with permissions, negotiation and consent.
3. Validate held-out Tier 2/3 scenario families and scoring with independent reviewers.
4. Integrate a real model and measure baseline competence.
5. Train matched curricula only after feasibility gates pass.

**Compute:** Free resources first. **Total spend ceiling:** $25. No paid compute without explicit approval.
