# OsteoQuant — Founder Executive Summary (Generation 2, 28 November 2026)

For the founder. Plain language; every number names the file it comes from. Nothing here is legal, tax or investment
advice. Status in one line: a working research prototype, pre-revenue and unincorporated, with no customers,
interviews or pilots, and no test on real graft materials.

## 1. What exists
* **A desktop application**, not a website: you install it on a computer and the scans never leave that machine. It
  imports scans with mandatory voxel-size confirmation and quality checks, shows linked 2D/3D views, lets an analyst
  correct the segmentation (every edit saved as a new version with a reason), runs the analysis in the background,
  requires a second person to sign off, keeps a hash-chained audit trail and writes PDF/CSV reports
  (`docs/desktop/USER_GUIDE.md`). The Linux build passes its packaged self-test (`packaging/dist/build-info.json`);
  Windows and macOS builds are configured but have never been built or run (`docs/user/INSTALLATION.md`).
* **The core idea, the measurement-support advisor** (shipped version 1.4.2, `osteoquant/advisor/separability.py`).
  Before reporting graft or new-bone volume, it decides whether the scan can support that number for this material,
  noise, blur and timepoint. If not, the report says "not measured" and why. Total mineral is reported whenever the
  scan allows.
* **Supporting work:** about 88% line+branch test coverage of the analysis library, desktop UI excluded (measured
  2026-11-28; the target is 90%); review cycles by automated reviewer agents — not human experts — with cycle 3 under
  way (`REVIEW_REGISTRY.md`); a financial model, pricing
  hypotheses and a competitor matrix (`business/`, `docs/research/`); three rebuilt decks whose every figure is read
  from these files (`investor/build_decks.py`).

## 2. What the evidence shows — including what failed
All graft and new-bone evidence is **simulation** (computational phantoms with a known answer).
* **The final held-out test.** In the pre-registered held-out simulation S1H3 (advisor 1.4.1; 216 synthetic specimens; a failure is a volume error above 20%): residual graft volume supported in 37% of specimens, every failing measurement refused and none of the supported ones failed (95% upper bound on the supported-failure rate 0.045); supported graft volumes: median error 4.2%, maximum 13.0%; total mineral volume supported in 10% of specimens (sharp imaging only); supported mineral volumes: maximum error 3.2%; new-bone volume never supported.
  (`experiments/results/exp_S1H3_heldout.json`) The shipped advisor 1.4.2 differs only in rules S1H3 does not
  exercise. The simulator and the advisor share attenuation physics, so this shows internal safety, not accuracy on
  real scans. No physical validation exists.
* **The failures that came first.** S1H (advisor 1.3.3) failed on new bone: wider scanner blur pushed graft edges into
  the new-bone range. S1H2 (advisor 1.4.0) failed on total mineral: the ambiguous rim around graft was too narrow under
  heavy blur. Each failure led to a rule change that was then tested on new, unseen conditions
  (`EXPERIMENT_REGISTRY.md`). Safety was bought with coverage: most graft and all new-bone measurements are refused.
* **The honest consequence.** By intensity alone, graft and new bone can be separated only for dense calcium phosphates
  at low noise and early, known timepoints (`scripts/material_support_table.py`, run on the shipped advisor). Total
  mineral is the robust endpoint, but under heavy blur even it is now refused.
* **Day-0 scans are fragile.** In simulation, naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion: 0.35 (`experiments/results/exp_L3_displacement.json`). No day-0 analysis is offered.
* **Real data is two-class only.** Bone versus background on public dog scans: U-Net trained on 10 real scans Dice 0.826
  (`experiments/results/exp_H_I_real.json`); Tb.Th ICC(2,1) 0.983 against Scanco IPL on 8 public cubes, with a
  border convention chosen after seeing them (`experiments/results/exp_G_morphometry.json`). The Generation-0 synthetic
  model, applied to the real dog test scans without real training data, reached Dice 0.377 at native scale and 0.513
  with 2× upsampling (`experiments/results/exp_S2v2_sim2real_a.json`). The domain-randomised, self-supervised and
  uncertainty experiments (S2b/c, S3, U1, O2) are still running; no numbers yet.

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
`FOUNDER_DECISIONS.md` lists 16 decisions only you can make. These five carry the hardest deadlines:

| # | Decision | Deadline | Ask |
|---|---|---|---|
| 2 | Whether new inventive work stays public, and the repository's licence (#3, removing sensitive files, shares this deadline) | **Now, before the next push** | counsel; IP Clinic |
| 4 | Request the university (OTM) ownership determination | Before Cozad registration and the **2 Feb 2027** pitch, and before any SAFE, grant sub-award, Beckman scan or paid pilot | OTM |
| 8 | Approve the corrected financial-model assumptions, and the rebuilt decks, before using them | Before any investor, Cozad or I-Corps material uses the numbers | accountant; counsel |
| 5 | Incorporation and founder-to-company IP assignment | Before the first paid pilot (mid-2027 at the earliest) and before any SAFE | counsel; accountant |
| 1 | File or forgo a US provisional patent application | Decide by **2027-09**; US bar date **2027-11-27** | IP Clinic (spring intake); patent attorney |

## 5. The next 90 days (to the decision gate around 25 February 2027)
**Weeks 1–2 (to mid-December).** Stop pushing new inventive work publicly until decision #2 is made with counsel.
Request the OTM determination (#4) with a written record of your lab history. Run the trademark knockout search (#6).
Read the financial model and the rebuilt decks, and approve or change them (#8); until then, send nothing.
**December–January.** Join an Illinois I-Corps workshop and run Wave 1 discovery interviews, aiming for at least 20 logged
and coded by February (`investor/FUNDING_STRATEGY.md` §3, M1). Register for Cozad, writing every application yourself
(#10). Approach an imaging scientist about the 14 open phantom-protocol decisions
(`validation/DECISIONS_FOR_IMAGING_SCIENTIST.md`) and the Beckman facility and data agreement (#11). Recruit at least one
human expert (imaging scientist, bone biologist or biostatistician) to review the advisor rules and the held-out designs.
**February.** Cozad pitch on 2 February (only after #4; a pitch carries no confidentiality). Start phantom scans if
access and agreements are in place. Around 25 February apply the combined gate
(`business/PRICING_VALIDATION_PLAN.md` §7): proceed only if the study-analysis price signal holds **and** the phantom
work shows a separable path; otherwise lead with licences, or keep the project as research.
**Throughout.** About 8 hours a week on `founder/LEARNING_CURRICULUM.md` Part A (you should be able to explain all seven
concepts by February). Make dated commits yourself.
**Not in these 90 days:** paid pilots (need an entity), equity, and more software features. The next value comes from
physical data, buyer conversations and human expert review.
