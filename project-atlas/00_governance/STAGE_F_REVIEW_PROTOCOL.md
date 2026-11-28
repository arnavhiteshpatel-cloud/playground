# Stage F Protocol — Independent Adversarial Review

You did not write the material you are reviewing. Your job is to find substantive weaknesses — wrong facts,
unsupported claims, broken math, unrealistic customer acquisition, inaccessible suppliers, legal problems,
underestimated competitors, unachievable margins, insufficient working capital, founder-execution risk,
implausible delegation, exaggerated wealth projections. Superficial criticism is useless; so is reflexive
pessimism. Where the material is right, say so briefly and move on.

Read: `MANDATE_AND_FOUNDER_BRIEF.md`, `EVIDENCE_STANDARDS.md`, `SCORING_FRAMEWORK.md`; then for each assigned
finalist: its playbook, materials, deep dive, Stage C memo, model JSON/results, supplier and prospect CSVs, and the
cited sources (spot-check ≥8 consequential citations per finalist by actually opening them).

## Output per finalist — `07_review/<ID>_review.md`
1. **Verdict:** survives / survives with major revisions / fails — and the corrected evidence-adjusted view.
2. **Factual errors found** (claim · what the source actually says · correction).
3. **Unsupported or over-stated claims** (claim · evidence level actually warranted).
4. **Financial model audit** — recompute key numbers; challenge each top-5 driver with independent evidence;
   propose corrected conservative/base values (with source). Check working capital and the founder-draw logic.
5. **Customer acquisition challenge** — is the funnel realistic for an unknown newcomer? What do incumbents' sales
   motions look like? What would the first 10 customers really require?
6. **Supplier/partner accessibility challenge** — which assumed relationships are most likely to refuse a new firm?
7. **Legal/regulatory challenge** — anything missed, mis-stated, or that requires professional advice.
8. **Competitive response** — how incumbents would react; underestimated advantages.
9. **Founder execution & delegation realism.**
10. **Pre-mortem**: the 3 most plausible ways this fails; early indicators; cheapest preventive test.
11. **Corrected scores** (10 criteria) and a one-paragraph bottom line.
Also append a line to `03_screening/stage_updates/stageF_<batch>.jsonl` (`"stage":"F"`, corrected scores,
evidence, profit range, verdict) and add any new sources to `07_review/sources_<batch>.jsonl` (IDs `F<batch>-S###`).
Preserve genuine disagreements — do not converge artificially.

Rules: read-only; never contact anyone; never fabricate. Final reply ≤200 words.
