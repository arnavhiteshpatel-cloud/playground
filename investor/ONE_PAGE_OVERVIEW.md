# OsteoQuant — one-page overview (November 2026)

**What:** offline desktop micro-CT analysis for preclinical bone-graft and bone-healing studies. It separates newly
formed bone, residual graft and host bone **where the material and scan allow it**, refuses to report endpoints it
cannot support (a measurement-support advisor), and writes study reports with a tamper-evident audit trail (research
prototype; not validated).

**Stage:** research prototype, pre-incorporation, pre-revenue. No customers, interviews, pilots or letters of intent.
Not validated on real graft materials; no GLP or Part 11 claim.

**Problem:** bone-void-filler makers must show resorption and replacement by new bone in animal studies (21 CFR 888.3045
special controls). Labs separate graft from new bone with manual ROIs and global thresholds, which fail as resorbable
ceramics approach bone density.

**What exists:** working desktop software (7 input formats incl. Zeiss TXM; QC; automatic defect ROI; classical
three-class segmentation with an optional locked model; morphometry that agrees with Scanco IPL on 8 public cubes
(border convention chosen post hoc); measurement-support advisor 1.3.3; viewer with correction and re-authenticated
sign-off; hash-chained audit trail; reports); an automated test suite (556 tests in the full run of 2026-11-28); 16+
experiments; internal automated review (reviewer agents, not independent reviewers — `REVIEW_REGISTRY.md`).

**Evidence:**
* REAL public data: Tb.Th ICC(2,1) 0.983 against Scanco IPL on 8 cubes (convention chosen post hoc); real micro-CT
  bone-versus-background segmentation, U-Net trained on 10 real scans Dice 0.826; synthetic pre-training
  fine-tuned on 1 real scan 0.787 (a two-class task, not graft separation).
* SYNTHETIC: when graft density overlaps new bone, intensity-only rules fail. The day-0 method works in simulation only
  without granule motion: naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion:
  0.35, and the advisor refuses those cases. Validation of the advisor under version 1.3.3 is in progress
  (`EXPERIMENT_REGISTRY.md`).

**Differentiation:** simulation-based, material-specific separability assessment (physical phantoms planned, not
started); abstention instead of a plausible but unidentifiable number; reports with a tamper-evident audit trail
(research prototype; not validated) for firms without imaging staff.

**Market (bottom-up):** ≈16 bone-void-filler 510(k)s/yr, 41 active applicants, 24 dental-graft applicants, 67 NIH
bone-repair projects using micro-CT (lower bound). Graft-defect reports at the hypothesised prices ≈ $0.8–3.9M/yr (US
ceiling, `business/REVENUE_MODEL.md`) → a services-plus-software lab; venture scale requires CRO licensing and
expansion modules (osseointegration, spine, histology).

**Pricing (hypotheses to test, not prices charged; no interviews yet):** paid pilot $2.5–5K · non-GLP study analysis
$8–15K · material characterisation $5–15K (lower end under review) · academic licence $4–10K/yr · enterprise licence
$30–75K/yr. No GLP-related offering. Compute cost ≈ $0 (runs locally); analyst time is the main cost (assumed
22–90 h/study). Published anchor: one academic core lists $200/h for corporate analysis (HSS, accessed 2026-11-27).

**Model (hypothetical; `business/FINANCIAL_MODEL.xlsx`):** no revenue before incorporation and a first signed pilot.
Bootstrapped Base 2031 revenue $259K (all scenarios: `business/REVENUE_MODEL.md` §5a). **Cash without grants is the lead case:**
Bootstrapped Base needs about $96K at its deepest point. Grants are conditional (none applied for, eligibility
unresolved) and restricted to their projects; if the assumed awards were won the need would fall to about $45K.
Licences are 56% of Base 2031 revenue and need a code licence/EULA that does not exist yet.

**Next 90 days:** OTM/IP clearance and entity decision (M0) → 15 buyer interviews → physical phantom study on the
Beckman Zeiss Versa 630 → Cozad (Feb 2) → first retrospective pilot only after M0. **Decision gate ~25 Feb 2027:** the
combined gate in `business/PRICING_VALIDATION_PLAN.md` §7 — H2 interview signal (≥8 industry acceptable ranges
overlapping $8–15K and ≥40% of decision-makers saying yes at ≥$8K) **and** a separable path in the phantom study.

**Key dates:** US patent bar date for everything already public: **2027-11-27** (`FOUNDER_DECISIONS.md`).

**Contact:** [founder name, email] · repository and data room on request.
