# Prioritised Remaining-Work Checklist

Priority: P0 = blocks the 90-day gate (≈25 Feb 2027); P1 = needed before first paid study; P2 = before GLP/scale.
Owner: F = founder; C = collaborator/advisor; E = engineering (founder + AI-assisted); X = external professional.

| # | Pri | Item | Owner | Needs | Done when |
|---|---|---|---|---|---|
| 1 | P0 | File OTM invention/ownership disclosure; book Landuyt IP Clinic; get written answer on Beckman-equipment use | F | 1–2 meetings | written ownership position |
| 2 | P0 | 15 discovery interviews (business/INTERVIEW_GUIDE.md) with price ladder; code in interview_log_template.csv | F | outreach (business/PROSPECTS.md top 15) | ≥15 coded interviews; go/pivot decision |
| 3 | P0 | Beckman Versa 630 access: confirm billing category, training, current rates (2021 rates may be stale) | F | email itg-ms@beckman.illinois.edu | scheduled training + quote |
| 4 | P0 | Imaging scientist signs the 14 decisions in validation/DECISIONS_FOR_IMAGING_SCIENTIST.md | C | advisor (e.g. M. Kersh) | signed protocol |
| 5 | P0 | Pilot phantom scans (3 materials, 1 voxel size) → run `osteoquant analyze` + separability scripts on real scans | F+C | materials (BOM), scanner time | first real graft/new-bone separability result |
| 6 | P0 | Cozad registration (Dec 1 2026 – Feb 2 2027 window [CC]); adapt grants/COZAD_APPLICATION_PACKAGE.md in own words | F | — | submitted |
| 7 | P0 | NSF Project Pitch (needs eligible PI plan; see grants/NSF_vs_NIH_ELIGIBILITY.md) | F | PI decision | pitch submitted or NIH STTR path chosen |
| 8 | P1 | Retrospective pilot with one company/CRO on 20–30 scans under a DPA (business/templates/PILOT_PROPOSAL.md) | F | partner | ICC, Bland–Altman, time per scan; LOI |
| 9 | P1 | Timed reviewer study to replace the assumed 20 s/90 s effort constants (Experiment M) | F+C | 2–3 analysts | measured hands-on time |
| 10 | P1 | GPU training: nnU-Net (or current U-Net on GPU) once real labelled scans exist; port device to Apple `mps` | E | personal/company cloud GPU (not NCSA) | model trained on real data with specimen-level CV |
| 11 | P1 | Address independent security/scientific review findings (docs/security/*_REVIEW.md) | E | — | all high/critical closed, tests added |
| 12 | P1 | Close traceability gaps (45 GAP, 24 PARTIAL of 81 in docs/quality/traceability_matrix.csv) — prioritise review state machine, signature invalidation on change, report self-approval, retention locks, TLS | E | — | matrix ≥ PARTIAL everywhere |
| 13 | P1 | Histology: integrate Cellpose/StarDist or QuPath export; fix Macenko normalisation (degrades synthetic bone quantification) | E | — | nuclei F1 ≥0.6 on NuInsSeg held-out |
| 14 | P1 | Download blocked datasets on a normal network: BONe subset (Dryad), MarrowQuant H&E (EBI) → rerun H/I and N | F | browser | experiments rerun |
| 15 | P1 | Incorporate (after OTM); MSA, DPA, quality-agreement templates reviewed by counsel (business/templates/LEGAL_REVIEW_TERMS.md) | F+X | counsel | signed templates |
| 16 | P1 | Device-status opinion for any human-clinical extension; keep product research-only meanwhile | X | counsel/513(g) | written opinion |
| 17 | P2 | Fractional CSV consultant scoping quote (A6); IQ/OQ execution on a locked release | X | $ | executed IQ/OQ |
| 18 | P2 | Multi-scanner benchmark (Bruker, Scanco, Zeiss) with collaborators; cross-scanner adaptation on real data | C | data-sharing agreements | multi-site paper |
| 19 | P2 | Cone-beam CT simulation (ASTRA/TIGRE on GPU) to add cone-beam artefacts to the phantom library | E | GPU | Mode C simulator |
| 20 | P2 | Deformable longitudinal registration validation (biological deformation) | E+C | longitudinal in vivo data | TRE under deformation |
| 21 | P2 | PostgreSQL + HTTPS deployment for multi-user lab installs | E | — | deployment guide executed |
| 22 | P1 | Founder rewrites grant drafts in own words (NIH AI-authorship policy) | F | — | drafts rewritten |
