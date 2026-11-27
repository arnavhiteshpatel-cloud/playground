# Founder Handoff — OsteoQuant (27 November 2026)

This is the exact state of the project after the autonomous build session, written for you to act on. Every number
comes from a result file in this repository; synthetic results are labelled. Start with §1, then §16 (next actions).

## 1. What I completed
* A working, tested research prototype: analysis library + web workbench + reports (`osteoquant/`, `web/static/`).
* 16 computational experiments (A–P), several re-run after an independent review corrected my mistakes.
* Seven research packages written by parallel research streams: bone science, micro-CT physics and calibration,
  competitors (36), datasets (41), customers (103 prospects), funding (27 programmes), collaborators and a physical
  phantom protocol, quality/regulatory drafts (URS/FS/risk/IQ/OQ/PQ/9 SOPs).
* Deliverables: technical & commercial report PDF, master spreadsheet, financial model, 3 decks, 3 sample reports,
  3 manuscript drafts, landing page, operating manual, curriculum, demo script (index: `deliverables/README.md`).

## 2. What genuinely works (tested)
| Works | How tested |
|---|---|
| Reading real vendor data (Zeiss TXM 2.1 GB slice-lazily, DICOM 829 slices, NIfTI/NRRD/TIFF/OME/Zarr) | real public files; tests |
| QC incl. missing slices, saturation/metal, rings, cupping, CNR | synthetic artefacts + real ovine scans |
| Automatic defect ROI for plate defects (condyle, calvarial) | Dice 0.97–0.98 with nominal diameter (Exp F) |
| Morphometry (BV/TV, Tb.Th/Sp/N, Conn.D, BS) | exact on analytic objects; ICC 0.98 vs Scanco IPL on 8 public samples |
| Three-class segmentation on synthetic data | U-Net graft Dice 0.92 / new bone 0.87 (Exp B) |
| Viewer, correction with versioning, re-authenticated sign-off, audit trail, PDF/CSV reports | 58 automated tests + a real headless-browser session |

## 3. What was tested — and how many tests
58 pytest tests (unit, integration, end-to-end API, security regressions, numerical reference values); 16 experiments;
a headless-browser run of the full UI workflow; an independent adversarial review (21 security + 18 scientific findings).

## 4. Models trained (all CPU, all research prototypes)
| Model | Data | Use | Status |
|---|---|---|---|
| `unet_noctx_s0` | 48 synthetic phantoms | 3-class, no ROI input (fairest) | SYNTHETIC-TRAINED |
| `unet_ctx_s0` | same + ROI channel | context ablation | SYNTHETIC-TRAINED |
| `adapt_k{1,3,5,10,20}_*` | fine-tuned on held-out simulated materials | Exp J | SYNTHETIC-TRAINED |
| `unet_dog_bone_real` | 10 real dog-forelimb micro-CT (CC-BY-4.0) | real bone segmentation (Exp H): Dice 0.826 | research |
| `unet_synth_ft_dog_k{1,3}` | synthetic model fine-tuned on 1/3 real scans | transfer (Exp I) | research |
Registry with SHA-256: `models/registry.json` (model files are git-ignored; regenerate with the experiment scripts).

## 5. Data used
Real public (all CC-BY-4.0): ovine distraction callus (Zenodo 17255310), Scanco-IPL trabecular references (11061947),
dog forelimb micro-CT (24047383), mouse knee DICOM (3909552), NuInsSeg H&E nuclei (10518968). Plus 120 synthetic
specimens. **No customer, university or restricted data.** Blocked: BONe (Dryad token), MarrowQuant H&E (EBI TLS).

## 6. What the experiments showed (short version)
1. **Thresholding is fine only while the graft is clearly denser than new bone.** Once densities overlap, the best
   possible intensity-only rule falls to graft Dice 0.52–0.77 (0.36 when granules are bone-like). [SYNTHETIC]
2. **Shape/texture helps only if granules look different from new bone** (0.86–0.89 compact vs 0.65–0.70 strut-like). [SYNTHETIC]
3. **A registered day-0 scan is the most robust strategy** (graft Dice 0.82 where single-scan methods give 0.66), but
   it needs an in-vivo post-op scan and is best-case in simulation. [SYNTHETIC]
4. **Adaptation to a new simulated material needs 1–3 labelled scans** — optimistic; real materials will need more. [SYNTHETIC]
   On **real** micro-CT (dog forelimb bone), synthetic-only training failed zero-shot (Dice 0.38) but synthetic pre-training
   plus **one** labelled real scan reached 0.79 vs 0.83 for a model trained on 10 real scans. [REAL] — strongest evidence so
   far that a "phantom-pretrained + few customer labels" workflow is viable; never use synthetic-only models on real scans.
5. **Morphometry matches Scanco IPL** once the border convention is handled (−2.4% Tb.Th) — but I chose the convention
   after seeing the data, so confirm on new references. [REAL]
6. **Real scans break naive code**: zero padding, saturated hardware, unlabelled anatomy. Fixed or made explicit. [REAL]
Full table: `EXPERIMENT_REGISTRY.md`. Figures: `experiments/results/figures/`.

## 7. Assumptions that failed
* "Explicit spatial context improves the model" — not supported (U-Net without ROI input was as good).
* "Context can always rescue overlapping densities" — fails when graft morphology mimics bone.
* Playbook: ovine dataset voxel 3.72 µm → actually **24.6 µm**; Mark Anastasio moved to WashU (2025); Dragonfly *does*
  have bone reports; graft-defect reports alone are a **low-single-digit-$M/yr** market at playbook prices.
* My own errors caught by review: the "Bayes bound" was not a Dice bound; RF baselines were under-trained; report
  statistics could pseudo-replicate; two critical security holes. All fixed; see `docs/security/REVIEW_RESPONSE.md`.

## 8. Most promising technical approaches
1. **Material separability assessment** with physical phantoms + the simulator (tells a sponsor *before* a study what
   micro-CT can and cannot measure for their graft).
2. **Longitudinal day-0 protocol** (study-design guidance + registration) for resorbable/bone-like grafts.
3. **nnU-Net-scale models trained on real labelled phantom/pilot data**, with uncertainty-guided review.
4. Histology as the fallback modality where micro-CT is underdetermined (integrate Cellpose/StarDist/QuPath).

## 9. What competitors already do / what remains differentiated
Dragonfly (DL + bone analysis + reports), CTAn/IPL (standard morphometry), CROs (Part 11 algorithms, histology endpoints)
already exist. Still differentiated (no public evidence of others): known-truth per-material separability benchmarking,
the day-0 graft-propagation protocol, and audit-ready per-study reports sold to firms without imaging staff.

## 10. Requires physical experiments
Real graft-vs-new-bone separability (phantom protocol `validation/`), calibration (HA phantom), real cross-scanner
transfer, analyst time saving (timed study), micro-CT vs histology agreement.

## 11. Requires a research collaborator
Imaging scientist to sign the 14 phantom decisions (`validation/DECISIONS_FOR_IMAGING_SCIENTIST.md`) — first choice
**Mariana Kersh** (MechSE; Beckman-based; lab uses the Versa 630). Bone-biology/histomorphometry adjudicator. A CRO
(CSU PSRL) for real study scans. For NIH STTR: a UIUC faculty PI.

## 12. Requires funding
Phantom pilot ≈$2.1–3.8K; minimal phantom design ≈$4.8–9.8K; full ≈$10.8–19.7K (`validation/BILL_OF_MATERIALS.csv`;
Beckman rates from 2021 may be stale). Cloud GPU ≈$3–8K once real labels exist. Legal/IP ≈$10–25K at incorporation.

## 13. What you should learn (in order)
`founder/LEARNING_CURRICULUM.md` — weeks 1–4 (bone biology, graft materials, micro-CT physics, calibration) while
interviewing; then morphometry standards (Bouxsein 2010), statistics (ICC/Bland–Altman), regulation (Part 11/58, OECD 17).

## 14. Who to contact first (drafts in `outreach/OUTREACH_EMAILS.md`; nothing has been sent)
1. **UIUC OTM** (otm@illinois.edu) and **Landuyt IP Clinic** (landuyt@illinois.edu) — ownership before using Beckman equipment.
2. **Beckman Microscopy Suite** (itg-ms@beckman.illinois.edu) — Versa 630 access, billing category, training, current rates.
3. **Mariana Kersh** (mkersh@illinois.edu) — advisor for phantom design and endpoints.
4. Customer interviews, top 5: **Kuros Biosciences, Geistlich, Bone Solutions, Prosidyan, CSU PSRL** (`business/PROSPECTS.md`).
5. Then Amy Wagoner Johnson, Brendan Harley, Kirk McGilvray (CSU), BONe author Andrew H. Lee.

## 15. What to spend money on first
Nothing on software. First: the **pilot phantom** (~$2–4K: graft samples, ex vivo bone, scan hours) — only after OTM
clarifies ownership. Second: legal/IP at incorporation. Do **not** pay for MedTech Innovator/BioTools fees ($15K) now.

## 16. Exact next actions (dates)
| By | Action |
|---|---|
| **Mon 30 Nov** | Email OTM + book Landuyt IP Clinic; email Beckman for Versa access/rates; send Kersh the advisor email (edit drafts in your words). Decide *not* to enter MedTech/BioTools Innovator (Dec 1; fee, too early). |
| **Tue 1 Dec** | Cozad 2027 registration opens — register (window to Feb 2, 2027). |
| **1–11 Dec** | Send 15 discovery emails (top 15 prospects; template in `business/INTERVIEW_GUIDE.md`). Book ≥5 interviews. |
| **by 18 Dec** | Run the demo (`founder/DEMO_SCRIPT.md`) for Kersh/advisors; finalise phantom decisions; order pilot materials if OTM clears. |
| **Jan 2027** | Pilot phantom scan (3 materials, 1 voxel size); run `osteoquant analyze`; code interviews; decide PI route (co-founder vs NIH STTR with faculty). |
| **31 Jan** | AO Innovation Funding (if a faculty/collaborator route exists) [deadline per page; verify]. |
| **by 2 Feb** | Cozad application written in your own words from `grants/COZAD_APPLICATION_PACKAGE.md`. |
| **25 Feb (gate)** | Go/pivot: ≥3/15 buyers at ≥$10K/study **and** phantom shows a separable path (single-scan or day-0). Else pivot per playbook §15. |
| **Mar–Jul** | Retrospective pilot (20–30 scans) → ICC, Bland–Altman, timed analysts → LOI; NSF Project Pitch → Phase I (Jul 7) if PI eligible, or NIH STTR (Apr 5 / Sep). |

## 17. How to demonstrate the product
`OQ_DEMO_PASSWORD=<pick> python scripts/demo_seed.py` → `OQ_DB=runtime/demo.db osteoquant serve` → follow
`founder/DEMO_SCRIPT.md`. Show the sample reports in `reports_samples/` and Figure `exp_C_separability.png`.
Say clearly: research prototype; synthetic results; real validation pending.

## 18. How to pursue the first paying study
Interview → offer a **free/discounted retrospective pilot** (template `business/templates/PILOT_PROPOSAL.md`) under a
DPA (`business/templates/DPA_ISSUES_CHECKLIST.md`) → deliver agreement statistics + time per scan + a separability
assessment for their graft → ask for an LOI or a paid next non-GLP study (price ladder from interviews; playbook
hypothesis ≈$12K). Incorporate before signing anything paid.

## 19. How to prepare the first grant application
Cozad first (no company needed). For federal: read `grants/NSF_vs_NIH_ELIGIBILITY.md`; the PI constraint decides NSF
SBIR (needs >50% company-employed PI — not you while a full-time student) vs **NIH STTR with a UIUC faculty PI**.
Rewrite `grants/SPECIFIC_AIMS_DRAFT.md` in your own words (NIH AI-authorship policy) and replace each
`[PENDING RESULT]` with phantom data. SAM.gov registration takes ≥6 weeks — start right after incorporation.

## 20. How to turn this into a legitimate company
OTM disclosure → IP Clinic → incorporate (Delaware C-corp typical for venture; LLC acceptable for a services lab — get
counsel) → founder IP assignment → EIN, bank, SAM.gov/UEI → MSA/DPA/quality-agreement templates reviewed
(`business/templates/LEGAL_REVIEW_TERMS.md`) → insurance → first pilot contract. Keep company code on personal/company
accounts, not university computing (already the case).

## 21. Honest bottom line
The software is far ahead of the evidence. The next bottleneck is not code: it is (a) one physical phantom study and
(b) fifteen conversations with buyers. Both are achievable by February 2027.
