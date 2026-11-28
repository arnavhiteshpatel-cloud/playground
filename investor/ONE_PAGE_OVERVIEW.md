# OsteoQuant — one-page overview (November 2026)

**What:** offline desktop micro-CT analysis for preclinical bone-graft and bone-healing studies. It separates newly
formed bone, residual graft and host bone **where the material and scan allow it**, refuses to report endpoints it
cannot support (a measurement-support advisor), and writes study reports with a tamper-evident audit trail (research
prototype; not validated).

**Stage:** research prototype, pre-incorporation, pre-revenue. No customers, interviews, pilots or letters of intent;
no evaluation on customer data has been agreed. Not validated on real graft materials; no GLP or Part 11 claim.
Release gates (`RELEASE_READINESS.md`): Gate 1 not met, Gate 2 not met, Gate 3 never claimed.

**Problem:** bone-void-filler makers must show resorption and replacement by new bone in animal studies (21 CFR 888.3045
special controls). Labs separate graft from new bone with manual ROIs and global thresholds, which fail as resorbable
ceramics approach bone density.

**What exists:** working desktop software (7 input formats incl. Zeiss TXM; QC; automatic defect ROI; classical
three-class segmentation with an optional locked model; morphometry that agrees with Scanco IPL on 8 public cubes
(border convention chosen post hoc); measurement-support advisor 1.4.3; viewer with correction and re-authenticated
sign-off; hash-chained audit trail with external anchors; reports). Default segmentation: the advisor's own threshold
(`advisor_threshold`), the only method carrying measurement support. Builds: the only packaged build is a local Linux
build of 28 Nov 2026 (commit `1f568f4`, advisor 1.4.3; packaged self-test and licence check passed), not distributed;
Windows and macOS builds have never been run. Tests: 611 passed, 1 skipped; 93.4% line+branch coverage (99% on critical modules), desktop UI
excluded (single source `docs/qa/test_summary.json`); CI on Windows, macOS and Linux passed for the first time on
28 Nov 2026. 16+ experiments; internal automated review (reviewer agents, not independent reviewers — `REVIEW_REGISTRY.md`).

**Evidence:**
* REAL public data: Tb.Th ICC(2,1) 0.983 against Scanco IPL on 8 cubes (convention chosen post hoc); real micro-CT
  bone-versus-background segmentation, U-Net trained on 10 real scans Dice 0.826; synthetic pre-training
  fine-tuned on 1 real scan 0.787 (a two-class task, not graft separation).
* SYNTHETIC: when graft density overlaps new bone, intensity-only rules fail. The day-0 method works in simulation only
  without granule motion: naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion:
  0.35, and the advisor refuses those cases.
* SYNTHETIC, advisor safety: In the pre-registered held-out simulation S1H4 (advisor 1.4.3; 720 synthetic specimens from 36 phantom structures, knowledge-base and Unspecified material paths; a failure is a volume error above 20%): residual graft volume supported in 10% of specimens (HA only), every failing measurement refused and none of the supported ones failed (95% upper bound on the supported-failure rate 0.14 counting phantom structures as the unit; 0.052 if the 69 supported measurements were independent); supported graft volumes: median error 2.2%, maximum 11.4%; total mineral volume supported in 2% of specimens (β-TCP at PSF 40 µm only); supported mineral volumes: maximum error 16.9%; new-bone volume never supported; no volume endpoint supported for 89% of specimens. An earlier held-out test of advisor 1.4.1 (S1H3, 9 phantom structures) is recorded in the experiment registry. This test used the shipped advisor 1.4.3, frozen before the run. A further pre-registered held-out test was limited to sintered HA residual graft on condyle and segmental defects: in the held-out simulation S1H5 (advisor 1.4.3; 192 synthetic specimens from 48 phantom structures; a failure is a volume error above 20%), residual graft volume supported in 70% of specimens and none of the supported ones failed (95% upper bound on the supported-failure rate 0.074 counting phantom structures as the unit); supported graft volumes: median error 2.2%, maximum 12.3%. No residual-graft measurement in that scope failed at all, refused or not, so S1H5 shows precision for this narrow case, not that the advisor refuses failing HA measurements. The simulator and the advisor share attenuation physics, so this is evidence of internal safety, not of accuracy on real scans; no physical validation has been run.
  In plain terms: new-bone volume was never supported in the held-out tests; on the material paths the application
  uses, residual graft was supported only for HA and total mineral almost never; for most held-out specimens no volume
  endpoint was supported. A buyer should expect many scans with no volume reported.

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

**Next 90 days:** request the OTM determination and decide the entity type (first steps toward M0: entity, OTM
determination received, insurance, counsel-reviewed NDA/SOW/DPA) → Cozad registration (deadline 2 Feb 2027; finals
April 2027) → 15 buyer interviews → **price gate ~25 Feb 2027** (`business/PRICING_VALIDATION_PLAN.md` §7: ≥8 industry
acceptable ranges overlapping $8–15K and ≥40% of decision-makers saying yes at ≥$8K). The physical phantom study on
the Beckman Zeiss Versa 630 (M2) follows in spring 2027 at the earliest (protocol not approved); the **separability
gate** comes after its read-out. No pilot or evaluation on customer data before M0, a DPA and Gate 1; a paid pilot
also needs Gate 2.

**Key dates:** US patent bar dates for material already public: **2027-11-27** (pushed 2026-11-27) and
**2027-11-28** (the mechanisms added since advisor 1.4.0, and related work, pushed 2026-11-28)
(`FOUNDER_DECISIONS.md`).

**Contact:** [founder name, email] · repository and data room on request.
