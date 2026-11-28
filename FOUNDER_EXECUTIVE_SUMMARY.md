# OsteoQuant — Founder Executive Summary (Generation 2, 28 November 2026)

For the founder. Plain language; every number names the file it comes from. Nothing here is legal, tax or investment
advice. Status in one line: a working research prototype, pre-revenue and unincorporated, with no customers,
interviews or pilots, and no test on real graft materials.

## 1. What exists
* **A desktop application**, not a website: you install it on a computer and the scans never leave that machine. It
  imports scans with mandatory voxel-size confirmation and quality checks, shows linked 2D/3D views, lets an analyst
  correct the segmentation (every edit saved as a new version with a reason), runs the analysis in the background,
  requires a second person to sign off, keeps a hash-chained audit trail and writes PDF/CSV reports
  (`docs/desktop/USER_GUIDE.md`). The only packaged build is a local Linux build of 28 November (commit `cf6fea7`, advisor 1.4.3); it
  passed its packaged self-test and licence check (`packaging/dist/build-info.json`) and is not distributed. In CI on 28 Nov, macOS (Apple silicon) and Linux builds passed their
  self-tests; the Windows build fails on a headless desktop-test crash (DF-044) (`docs/user/INSTALLATION.md`).
* **The core idea, the measurement-support advisor** (shipped version 1.4.3 in the source,
  `osteoquant/advisor/separability.py`; no packaged build contains it yet). Before reporting graft, new-bone or total
  mineral volume, it decides whether the scan can support that number for this material, noise, blur and timepoint.
  If not, the report says "not measured" and why. It is the default segmentation method (`advisor_threshold`), the
  only one carrying measurement support. Total mineral is reported only when the scan's blur and noise allow it, which
  in held-out simulation was rare (§2).
* **Supporting work:** tests and coverage from one file, `docs/qa/test_summary.json`: 636 passed, 1 skipped; 93.4%
  line+branch coverage of the `osteoquant` package (98.7% on critical modules), desktop UI excluded (local full run,
  28 Nov). CI passed for the
  first time on 28 Nov. Review cycles by automated reviewer agents — not human experts — with cycle 3 under
  way (`REVIEW_REGISTRY.md`); a financial model, pricing
  hypotheses and a competitor matrix (`business/`, `docs/research/`); three rebuilt decks whose every figure is read
  from these files (`investor/build_decks.py`).

## 2. What the evidence shows — including what failed
All graft and new-bone evidence is **simulation** (computational phantoms with a known answer).
* **The final held-out test.** In the pre-registered held-out simulation S1H4 (advisor 1.4.3; 720 synthetic specimens from 36 phantom structures, knowledge-base and Unspecified material paths; a failure is a volume error above 20%): residual graft volume supported in 10% of specimens (HA only), every failing measurement refused and none of the supported ones failed (95% upper bound on the supported-failure rate 0.14 counting phantom structures as the unit; 0.052 if the 69 supported measurements were independent); supported graft volumes: median error 2.2%, maximum 11.4%; total mineral volume supported in 2% of specimens (β-TCP at PSF 40 µm only); supported mineral volumes: maximum error 16.9%; new-bone volume never supported; no volume endpoint supported for 89% of specimens. An earlier held-out test of advisor 1.4.1 (S1H3, 9 phantom structures) is recorded in the experiment registry.
  (`experiments/results/exp_S1H3_heldout.json`) The shipped advisor 1.4.3 differs from 1.4.1 in rules S1H3 does not exercise, and in one it does (the
  total-mineral rim gate), only in the stricter direction. The simulator and the advisor share attenuation physics, so this shows internal safety, not accuracy on
  real scans. No physical validation exists.
* **The failures that came first.** S1H (advisor 1.3.3) failed on new bone: wider scanner blur pushed graft edges into
  the new-bone range. S1H2 (advisor 1.4.0) failed on total mineral: the ambiguous rim around graft was too narrow under
  heavy blur. Each failure led to a rule change that was then tested on new, unseen conditions
  (`EXPERIMENT_REGISTRY.md`). Safety was bought with coverage: most graft and all new-bone measurements are refused.
* **The honest consequence.** By intensity alone, residual graft volume can be supported only for dense calcium
  phosphates at low noise and early, known timepoints (`scripts/material_support_table.py`, run on the shipped
  advisor). New-bone volume was never supported in the held-out tests, for any material. Total mineral is not a safe
  fallback: in S1H4 (shipped advisor), total mineral volume supported in 2% of held-out specimens (β-TCP at one
  imaging condition only), and no volume endpoint supported for 89% of held-out specimens. A buyer must expect many
  scans with no volume reported.
* **Day-0 scans are fragile.** In simulation, naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion: 0.35 (`experiments/results/exp_L3_displacement.json`). No day-0 analysis is offered.
* **Real data is two-class only.** Bone versus background on public dog scans: U-Net trained on 10 real scans Dice 0.826
  (`experiments/results/exp_H_I_real.json`); Tb.Th ICC(2,1) 0.983 against Scanco IPL on 8 public cubes, with a
  border convention chosen after seeing them (`experiments/results/exp_G_morphometry.json`). The Generation-0 synthetic
  model, applied to the real dog test scans without real training data, reached Dice 0.377 at native scale and 0.513
  with 2× upsampling (`experiments/results/exp_S2v2_sim2real_a.json`). Status per `EXPERIMENT_REGISTRY.md`: S2 part b
  (domain-randomised pretraining, one seed) was worse than the Gen-0 model on every test scan (0.353 native, 0.457 at
  2×); part c: with 1–3 real labelled scans, training from scratch (0.805 / 0.816) matched or beat synthetic pretraining;
  S3 (self-supervised pretraining) did not help either (0.782 / 0.794); U1 (SYNTHETIC): ensemble failure flags work (volume-CV failure-detection score 0.95), conformal
  intervals hold in distribution (15/16) but not for a new material (25/40); O2 (ONNX runtime) is being re-run.

## 3. What is unknown
* Whether real graft materials behave like the simulator: no physical phantom has been scanned
  (`validation/PHANTOM_EXPERIMENT_PROTOCOL.md`: not approved, not started).
* Whether anyone will pay: 0 interviews logged (`business/interview_log_template.csv`); every price is a hypothesis.
* The market is small: about $0.8M–$3.9M a year in the US at the hypothesised prices (`business/FINANCIAL_MODEL.xlsx`,
  Market check; `business/REVENUE_MODEL.md` §5d) — a founder-scale business unless adjacent modules or non-US demand
  appear.
* The money in the model is hypothetical (`business/financial_model_outputs.json`).
  * Bootstrapped Base 2031 revenue $259K.
  * Bootstrapped Base needs about $96K at its deepest point without grants; if the assumed grants were won the need would fall to about $45K.
  * Licences are 56% of Bootstrapped Base 2031 revenue; without licence revenue Base 2031 revenue is $114K.
  * The Venture Base scenario needs about $4.2M of equity without grants. Venture capital is not justified on today's
    evidence (`investor/FUNDING_STRATEGY.md` §1).
* Who owns the code (university determination not requested), and how much protection AI-generated code carries
  (`docs/security/IP_PROVENANCE.md`).

## 4. Five decisions with deadlines
`FOUNDER_DECISIONS.md` lists 25 decisions only you can make (#17–#25 added after review cycle 3). These six carry
the hardest deadlines:

| # | Decision | Deadline | Ask |
|---|---|---|---|
| 17, 2 | The standing instruction on pushing (today: your 27 Nov decision to push everything publicly, under which new mechanisms were pushed on 28 Nov), then whether inventive work stays public and the repository's licence (#3, removing sensitive files, shares this deadline) | **Now** | counsel; IP Clinic |
| 18 | Whether to offer any evaluation on customer data before M0 and Gate 1 (none is offered today) | Before outreach mentions pilots | counsel; insurer |
| 4 | Request the university (OTM) ownership determination | Before Cozad registration (deadline **2 Feb 2027**) and any Cozad pitch (finals April 2027), and before any SAFE, grant sub-award, Beckman scan or paid pilot | OTM |
| 8 | Approve the corrected financial-model assumptions, and the rebuilt decks, before using them | Before any investor, Cozad or I-Corps material uses the numbers | accountant; counsel |
| 5 | Incorporation and founder-to-company IP assignment | Before the first paid pilot (mid-2027 at the earliest) and before any SAFE | counsel; accountant |
| 1, 19 | File or forgo a US provisional, and any filings in grace-period jurisdictions | Decide by **2027-09**; US bar dates **2027-11-27** (27 Nov material) and **2027-11-28** (28 Nov material) | IP Clinic (spring intake); patent attorney |

## 5. The next 90 days (to the price gate around 25 February 2027)
**Weeks 1–2 (to mid-December).** Decide the standing instruction on pushing (#17): the only instruction on record is
your 27 Nov decision to push all work publicly (`docs/ip/IP_STRATEGY.md` Addendum), and new advisor mechanisms were
pushed on 28 Nov under it; confirm it, or tell the development process to keep new inventive work on a private branch
or remote until #2 is decided. Request the OTM determination (#4) with a written record of your lab history. Run the trademark knockout search (#6).
Read the financial model and the rebuilt decks, and approve or change them (#8); until then, send nothing.
**December–January.** Join an Illinois I-Corps workshop and run Wave 1 discovery interviews, aiming for at least 20 logged
and coded by February (`investor/FUNDING_STRATEGY.md` §3, M1). Register for Cozad, writing every application yourself
(#10). Approach an imaging scientist about the 14 open phantom-protocol decisions
(`validation/DECISIONS_FOR_IMAGING_SCIENTIST.md`) and the Beckman facility and data agreement (#11). Recruit at least one
human expert (imaging scientist, bone biologist or biostatistician) to review the advisor rules and the held-out designs.
**February.** Cozad registration closes on 2 February (register only after #4; the Demo Showcase and Finals are in
April 2027, date not confirmed, and a pitch carries no confidentiality). Around 25 February apply the price gate
(`business/PRICING_VALIDATION_PLAN.md` §7): does the study-analysis price signal hold? The separability gate (does
the phantom study show a separable path?) can only follow the phantom read-out: M2 is spring 2027 at the earliest,
and its protocol is not approved (14 imaging-scientist decisions, the OTM determination and a Beckman agreement are
still needed). Proceed with services only if both pass; otherwise lead with licences, or keep the project as
research.
**Throughout.** About 8 hours a week on `founder/LEARNING_CURRICULUM.md` Part A (you should be able to explain all seven
concepts by February). Make dated commits yourself.
**Not in these 90 days:** paid pilots (they need M0 and Gate 2), any evaluation on customer data (none is agreed;
#18), equity, and more software features. Rebuild the Linux package before anyone uses it. The next value comes from
physical data, buyer conversations and human expert review.
