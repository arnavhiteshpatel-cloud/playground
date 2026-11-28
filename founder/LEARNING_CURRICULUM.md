# Founder Learning Curriculum (Generation 2)

Two parts. **Part A** is the set of concepts you must be able to explain, in your own words and without notes, to an
imaging scientist, an investor or a lawyer; each ends with a self-test question (answers at the end, cover them
first). **Part B** is a 12-week reading and exercise plan (about 8 hours a week). References with DOIs are in
`docs/science/REFERENCES.md` (IDs R#).

---

## Part A — Seven concepts you must be able to explain

### A1. Identifiability and abstention
Graft and new bone are both mineral. If their X-ray attenuation overlaps, the image does not contain the information
needed to tell them apart, and *no* algorithm can recover it from intensity alone — a deep network included. A method
will still print a number; it is just not identifiable. OsteoQuant's measurement-support advisor
(`docs/science/MEASUREMENT_SUPPORT.md`) decides **before reporting**, per endpoint and per scan, whether the split is
identifiable for this material, noise, blur and timepoint, and refuses ("abstains") otherwise. Abstention trades
*coverage* (how often a number is given) for *safety* (how often a given number is wrong). Refusing everything is
perfectly safe and useless, which is why coverage is always reported next to safety.
**Self-test:** A customer says "your competitor gives us a graft volume for every scan; you refuse half of them —
why is yours better?" Answer in three sentences.

### A2. Partial volume and blur
A voxel at the edge of a granule contains graft and something else, so its grey value is a mixture (partial volume).
The scanner also blurs the image (its point-spread function, PSF), smearing every edge over several voxels. A dense
graft granule therefore has a halo of intermediate values — exactly the range of new bone. That is how the first
held-out test failed: the wider blur pushed graft edges into the new-bone range, so graft was under- and new bone
over-estimated (`EXPERIMENT_REGISTRY.md`, S1H). Advisor 1.4.0 (tested in S1H2) therefore measures the blur in each scan
and treats an ambiguous rim around graft as unidentifiable; advisor 1.4.1 (tested in S1H3) widened that rim with the
measured blur after S1H2 showed a one-voxel rim was too narrow.
**Self-test:** Why can halving the voxel size fail to fix a graft/new-bone overlap problem, and what else must change?

### A3. Pre-registration and held-out validation
If you tune rules on the same data you test them on, you will look better than you are. Pre-registration means writing
down the data, the endpoints and the pass/fail criterion **before** running the test, and promising not to change the
method afterwards (`docs/science/PREREGISTRATION.md` §7–9). Held-out means conditions the rules have never seen (new
seeds, densities, blur, noise). OsteoQuant's story is a chain: S1H failed on new bone → rules changed → S1H2 on new
conditions failed on total mineral → rules changed → S1H3 on new conditions, declared final before running. Two more
ideas belong here: the *unit of replication* is the independent structure, not the voxel or the repeated noise level
(pseudoreplication, review C2-SCI-17); and an acceptance rule can be too weak — S1H's graft result "passed" with a
quarter of its supported cases failing, so a stricter rule was added (deviations log). Finally, the simulator and the
advisor share the same attenuation physics, so even a clean held-out pass shows internal safety, not real-world
accuracy.
**Self-test:** After S1H3 you change one advisor threshold. Can you still quote S1H3 for the new version? What would
you have to do?

### A4. Error propagation: new bone = mineral − graft
New bone is not measured directly; it is total mineral minus graft. Any error in the graft volume moves into new bone
with the opposite sign, and *relative* errors grow when graft is a large share of the mineral. With p = graft share of
mineral, a relative graft error e becomes a relative new-bone error of about p/(1−p) × e. Advisor rule 11
(`docs/science/MEASUREMENT_SUPPORT.md`) uses this to refuse new-bone endpoints whose propagated error would be too
large; it is why new bone is the endpoint refused most often.
**Self-test (arithmetic):** Mineral is measured exactly. Graft is truly 60% of mineral and is under-estimated by 10%.
What is the relative error in new bone, and in which direction?

### A5. Conformal prediction intervals
A conformal interval turns any model's point estimate into an interval with a guaranteed long-run coverage (say 90%),
using a separate *calibration* set: you measure how wrong the model was on calibration cases and widen every new
prediction by the corresponding quantile. The guarantee is *marginal* (on average over cases, not for each scan) and
holds only if new cases resemble the calibration cases (exchangeability). Under distribution shift — a new graft
material, a new scanner — coverage can collapse, which is why Experiment U1 also tests *gating*: refusing scans the
failure detector flags before giving an interval (`docs/science/PREREGISTRATION.md` §6). U1 is still running; quote
no number from it.
**Self-test:** A CRO asks: "your 90% interval — does that mean 90% certainty for *my* scan?" What do you say?

### A6. LGPL obligations of the desktop bundle
The desktop ships Qt through PySide6 under the LGPL-3.0 (which incorporates the GPL-3.0). In short, when you
distribute it you must: ship both licence texts and the notices; let users replace the Qt libraries with their own
build (so they stay separate, replaceable shared libraries); not forbid, in your EULA, the modification and reverse
engineering needed to debug such replacements; and make the corresponding source of the exact Qt/PySide6 version
available (whether a pointer to upstream is enough or a mirrored archive/written offer is needed is an open counsel
question). Modules offered only under GPL (for example Qt Virtual Keyboard) must not ship in a closed product; the
build now fails if one appears (`docs/desktop/PACKAGING.md` §Licence compliance; `FOUNDER_DECISIONS.md` #12).
**Self-test:** Your future EULA says "no reverse engineering of any part of the software". Which obligation does that
break, and how do you fix the clause?

### A7. Public-repository disclosure
Everything pushed to the public repository on 2026-11-27 is a public disclosure. In the US an inventor has a one-year
grace period after their own disclosure, so the **bar date is 2027-11-27**; after it, your own repository is prior art
against you. Most other countries require absolute novelty, so foreign patent rights are likely already lost. Each new
push of inventive work starts its own clock and ends any trade-secret status. The public repository also exposes a
non-privileged patent triage, prospect lists and the full source — which undercuts licence revenue (decisions #1, #2,
#3 in `FOUNDER_DECISIONS.md`; `docs/ip/IP_STRATEGY.md`).
**Self-test:** You want to push a new day-0 tracking method next week. What should happen first, and who do you ask?

---

## Part B — 12-week plan

Each week: **read** (real sources), **do** (an exercise in this codebase), **check** (explain the answer to a bone
biologist without notes). Weeks 1–4 coincide with the first customer interviews; schedule reading around them.

| Wk | Topic | Read | Do in the codebase | Check |
|---|---|---|---|---|
| 1 | Bone biology and healing | Einhorn & Gerstenfeld 2015 (R45); Marsell & Einhorn 2011 (R46); `docs/science/BONE_BIOLOGY_AND_GRAFTS.md` §1 | Generate condyle phantoms at stages 0.2/0.5/0.8 (`osteoquant phantom --stage`), import them into a desktop project, view them | Woven vs lamellar bone; osteoconduction vs osteoinduction; why defects are "critical-size" |
| 2 | Graft materials | Bohner et al. 2020 β-TCP (R33); Jones 2013 bioactive glass (R37); `docs/science/SEPARABILITY_ANALYSIS.md` | Run `python3 scripts/material_support_table.py`; explain each refusal for β-TCP, DBBM and 45S5 | For HA, β-TCP, CaSO4, bioglass, DBM, allograft: when is separation easy, hard, impossible? (A1) |
| 3 | Micro-CT physics | Feldkamp et al. 1984 (R28); `docs/science/MICROCT_IMAGING_SCIENCE.md` | Generate phantoms with different `psf_sigma_um` and noise; look at the graft halo | Voxel size vs resolution; partial volume and blur (A2); beam hardening; why grey values differ between scanners |
| 4 | Calibration and QC | `MICROCT_IMAGING_SCIENCE.md` calibration tiers | `osteoquant qc` on phantoms with rings, cupping and noise; read Exp E | Deterministic vs heuristic QC checks, and why the report keeps them apart |
| 5 | Morphometry standards | Bouxsein et al. 2010 (R1); Hildebrand & Rüegsegger 1997 (R2); Salmon et al. 2015 on SMI (R5) | Re-run `exp_G_morphometry.py`; change `border` and watch the IPL agreement move | Why a convention chosen after seeing the data is not independent evidence (A3) |
| 6 | Measurement support | `docs/science/MEASUREMENT_SUPPORT.md` rules 1–12; `docs/science/ENDPOINT_DEFINITIONS.md` | Analyse the demo project with *Unspecified* vs β-TCP vs HA; compare the reasons in the Results tab | Identifiability (A1); error propagation (A4) |
| 7 | Validation design | `docs/science/PREREGISTRATION.md` §7–9 and deviations log; `EXPERIMENT_REGISTRY.md` S1H–S1H3 rows | Read `experiments/exp_S1H3_heldout.py`; find where the structures are bootstrapped | Pre-registration, held-out sets, pseudoreplication, coverage vs safety (A3) |
| 8 | Segmentation, uncertainty and conformal intervals | Isensee et al. 2021 nnU-Net (doi:10.1038/s41592-020-01008-z); Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction* (arXiv:2107.07511) | Read `experiments/exp_U1_ensemble_conformal.py` (`cover`, `gate`) | What marginal coverage means and when it fails (A5) |
| 9 | Statistics for preclinical studies | Koo & Li 2016 ICC (doi:10.1016/j.jcm.2016.02.012); Bland & Altman 1986 (Lancet 1:307) | `osteoquant/stats/core.py`: reproduce the Shrout–Fleiss ICC tests | ICC form for method agreement; animals, not voxels, are replicates |
| 10 | Longitudinal imaging | SimpleITK registration documentation; `EXPERIMENT_REGISTRY.md` L3, L4, F2 | Read `exp_L3_displacement.py`; find where granule motion is simulated | Why a day-0 scan helps only while granules stay put |
| 11 | Regulation, quality and licences | `docs/quality/REGULATORY_RESEARCH.md`; OECD GLP No. 17; 21 CFR 58 and 11; `docs/desktop/PACKAGING.md` §Licence compliance | Walk 5 requirements from `docs/quality/URS.md` through `traceability_matrix.csv`; read `THIRD_PARTY_NOTICES.txt` in a build | Technical controls ≠ Part 11 compliance; LGPL obligations (A6) |
| 12 | IP, customers and market | `docs/ip/IP_STRATEGY.md`; `FOUNDER_DECISIONS.md`; `business/INTERVIEW_GUIDE.md`; `business/REVENUE_MODEL.md` §5d | Conduct and code three interviews in `business/interview_log_template.csv` | Public disclosure and the bar date (A7); the bottom-up market and the assumption that moves it most |

**Practical skills alongside:** Python (NumPy/SciPy) → git (branches, dated commits of your own) → reading one desktop
service function (`osteoquant/desktop/services.py`) end to end → writing one test. Use `founder/OPERATING_MANUAL.md`
§13 as your change routine.

**Optional courses** (check current availability before enrolling): Illinois I-Corps workshops (Landuyt Center);
graduate courses in biomedical imaging or bone mechanics — ask your faculty advisor which they recommend.

---

## Answers to the self-tests (cover these until you have answered)
* **A1.** A number for every scan includes numbers the image cannot support; for overlapping materials those are
  plausible but unidentifiable, and nobody can tell which ones. We report what the scan supports, say why we refuse the
  rest, and always give total mineral. A wrong number in a study costs more than a missing one.
* **A2.** Smaller voxels reduce the partial-volume mixing per voxel, but blur is set by the scanner's PSF in µm; if the
  blur stays the same, the halo stays the same width in µm. You need sharper imaging (focal spot, reconstruction), a
  measured graft reference, or a different design (day-0 scan, histology).
* **A3.** No. S1H3 tested advisor 1.4.1 frozen; a changed rule needs a new pre-registered held-out test on conditions no
  version has seen. Re-running S1H3 is only a development check. (The shipped 1.4.3 differs from 1.4.1 in rules S1H3
  does not exercise and in one it does, only in the stricter direction, which is why S1H3 is still quoted, with that
  caveat. Note also that S1H3's 80 supported graft measurements come from only 9 phantom structures: the honest bound
  on the supported-failure rate is 0.34, not 0.045.)
* **A4.** Graft estimate = 0.54 × mineral instead of 0.60, so new bone = 0.46 instead of 0.40 of mineral: new bone is
  over-estimated by 15% (p/(1−p) = 1.5, times 10%). Illustrative arithmetic, not a result.
* **A5.** No. It means that across many scans like the calibration scans, about 90% of intervals contain the true value.
  It says nothing certain about one scan, and it can fail for a material or scanner unlike the calibration set — which
  is why we gate before giving an interval.
* **A6.** It conflicts with LGPL-3.0 §4: users must be allowed to modify the Qt part and to reverse engineer for
  debugging such modifications. Carve the LGPL components out of the restriction ("except as permitted by the licences
  of third-party components listed in THIRD_PARTY_NOTICES"), drafted by counsel.
* **A7.** First the decision in `FOUNDER_DECISIONS.md` #2: keep new inventive work private until a filing decision.
  Ask the Landuyt IP Clinic or a registered patent attorney, and check the university ownership question (#4) with OTM.
  The longitudinal area also has an open freedom-to-operate question (#15).
