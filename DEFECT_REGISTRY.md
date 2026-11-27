# Defect Registry

Single list of defects across the project. QA-stream details: `docs/qa/DEFECTS_FOUND.md`; security:
`docs/security/`. Severity: S1 wrong result/claim or data loss · S2 feature broken · S3 degraded · S4 cosmetic.

| ID | Sev | Area | Description | Found by | Status | Fix / evidence |
|---|---|---|---|---|---|---|
| DF-001 | S1 | docs | Manuscript 1 stated RF trained on 6 specimens with 15k voxels/class; code trains on 12 (3/material), ≤8,000 voxels/class/specimen | forensic audit FA-10 | fixed | publications/MANUSCRIPT_1_separability.md §2.4 |
| DF-002 | S3 | experiments | `experiments/common.py` always overwrote `experiments/results/` during reproduction | forensic audit | fixed | `OQ_RESULTS` override (ADR-G2-07) |
| DF-003 | S1 | pipeline | Graft volume is reported for any material, even when separation is known to be impossible | FA-16 | fixed | `osteoquant/advisor`; pipeline `reported_metrics` suppress unsupported endpoints; tests/test_advisor.py |
| DF-004 | S2 | ROI | Segmental ROI fails after bridging (explicit exception, no fallback) | FA-05 | open | T1.11 |
| DF-005 | S3 | docs | Day-18 ROI confidence quoted with inconsistent rounding across documents | FA-27 | fixed | `scripts/check_claims.py` (8 claims, all pass) |

Historical defects fixed in Generation 1 (S-01…S-19, Q-01…Q-14, RESEARCH_LOG errors) are recorded in
`docs/security/REVIEW_RESPONSE.md` and `RESEARCH_LOG.md`.
