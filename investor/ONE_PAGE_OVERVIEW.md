# OsteoQuant — one-page overview (November 2026)

**What:** auditable micro-CT analysis for preclinical bone-graft and bone-healing studies — separating newly formed bone,
residual graft and host bone, with reviewer correction, locked model versions and a traceable DefectFill report.

**Stage:** research prototype, pre-incorporation, pre-revenue. Not validated on real graft materials; no GLP/Part 11 claim.

**Problem:** bone-void-filler makers must show resorption and replacement by new bone in animal studies (21 CFR 888.3046
special controls). Labs separate graft from new bone with manual ROIs and global thresholds, which fail as resorbable
ceramics approach bone density.

**What exists:** working software (7 input formats incl. Zeiss TXM; QC; automatic defect ROI; classical + learned
three-class segmentation with uncertainty; verified morphometry; longitudinal registration; viewer with correction and
re-authenticated sign-off; hash-chained audit trail; reports); 61 automated tests; 16 experiments; independent review.

**Evidence:**
* REAL public data: trabecular thickness agrees with Scanco IPL (ICC 0.98, 8 samples); real micro-CT bone segmentation
  Dice 0.83 (10 training scans) and 0.79 with synthetic pre-training + 1 real labelled scan.
* SYNTHETIC: three-class graft Dice 0.92 / new bone 0.87 vs 0.77/0.67 for a CTAn-style workflow; when graft mimics new
  bone, only a registered day-0 scan keeps graft Dice ≥0.8.

**Differentiation:** known-truth, material-specific separability assessment (phantoms + physics simulator); day-0
longitudinal protocol; audit-ready per-study reports for firms without imaging staff.

**Market (bottom-up):** ≈16 bone-void-filler 510(k)s/yr, 41 active applicants, 24 dental-graft applicants, 67 NIH
bone-repair projects using micro-CT (lower bound). Graft-defect reports at hypothesised prices ≈ $0.9–4.3M/yr → a
services-plus-software lab; venture scale requires CRO licensing and expansion modules (osseointegration, spine, histology).

**Pricing (hypotheses to test, not prices charged; no interviews yet):** offline desktop application plus services:
paid pilot $2.5–5K · non-GLP study analysis $8–15K · material characterisation $5–15K · academic licence $4–10K/yr ·
enterprise licence $30–75K/yr. No GLP-study offering until a validation report exists. Compute cost ≈ $0 (runs locally);
analyst time is the main cost (assumed 22–90 h/study across scenarios). Published anchor: one academic core lists $200/h for corporate
analysis (HSS, accessed 2026-11-27). Serviceable pool at these Base prices ≈ $0.8–3.9M/yr. Hypothetical 2031 revenue:
$58K / $288K / $1.05M (bootstrapped conservative / base / optimistic). Validation plan and thresholds:
business/PRICING_VALIDATION_PLAN.md; model: business/REVENUE_MODEL.md.

**Next 90 days:** OTM/IP clearance → physical phantom study on the Beckman Zeiss Versa 630 → 15 buyer interviews →
Cozad (Feb 2) → first retrospective pilot. **Decision gate ~25 Feb 2027:** ≥3/15 buyers at ≥$10K/study and a separable path.

**Contact:** [founder name, email] · repository and data room on request.
