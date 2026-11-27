# OsteoQuant Validation Programme — Stages A–F

No stage beyond A has started. Every physical stage needs founder authorisation, facility access, OTM/IP answers and,
for animal work, a partner's IACUC-approved study; OsteoQuant never conducts animal work itself. Acceptance criteria
are pre-registered in `docs/science/PREREGISTRATION.md` and are frozen before each stage's data are seen.

| Stage | Question | Design | Truth source | Exit criteria | Status |
|---|---|---|---|---|---|
| **A — Computational** | Are the algorithms correct, and where can separation work in principle? | Analytic objects, phantoms (generator v2), public real data | exact (synthetic); Scanco IPL maps; manual bone labels | Morphometry exact on analytic objects; advisor refuses ≥95% of failures with P(fail \| supported) upper bound ≤0.10 (S1/S1b/S1c); ROI propagation (F2), registration QC (L4) and granule tracking (L3) behave | **In progress.** Met so far: morphometry (G), ROI propagation (F2), registration QC detection (L4). **Not met:** L3 showed day-0 propagation collapses with granule motion (graft Dice 0.80 → 0.535 at 50 µm) and the first tracking version produced false matches that the advisor accepted (29/30 supported-but-failed); tracking was made conservative and L3 is being re-run. S1/S1b/S1c are being re-run with advisor 1.3.0 |
| **B — Ex vivo physical phantom** | Can real commercial grafts be separated from bone tissue on a real scanner, and are volumes accurate? | Protocol OQ-P1: bovine cores, weighed graft fills, 10/20/40 µm, scan–rescan, HA calibration | Gravimetric mass + material density; empty-core pre-scan | Per material: graft volume bias ≤5%, LoA ±15% where the advisor says *supported*; advisor decisions match observed separability (B5) | Protocol drafted (`PHANTOM_EXPERIMENT_PROTOCOL.md`), not approved |
| **C — Material characterisation** | Can the advisor be driven by measured material intensity instead of assumptions? | Scan each material alone (and in saline/agarose) on the same protocol; measure relative-unit intensity and granule size distributions | Physical sample | Measured profiles replace assumption profiles in `osteoquant/knowledge`; advisor decisions stable across repeated scans | Not started — can run in the same scanner session as B |
| **D — Retrospective partner data** | Does the software agree with expert analysts on real in vivo scans, and how much time does it save? | De-identified scans from a partner study (with day-0 scans if available); ≥2 blinded analysts; timed manual vs software-assisted review | Analyst consensus (and histology if available) | ICC(2,1) vs consensus ≥ analyst–analyst ICC; measured hands-on time reduction (no assumed constants) | Needs data-use agreement + counsel (founder) |
| **E — Prospective pilot with histology** | In a real graft study, are residual-graft and new-bone measurements right? | Partner's planned study adds day-0 scan + end-point histology on matched planes; pre-specified analysis | Histomorphometry by partner pathologist (blinded) | Pre-registered agreement criteria met for at least one material class; refusals concordant with histology-defined overlap | Needs partner study (founder) |
| **F — Independent / multi-site** | Does it transfer across scanners and sites, and can another lab reproduce it? | ≥2 sites, ≥2 scanner vendors, same SOP; independent analyst runs the software | as D/E | Between-site bias within pre-specified limits; independent reproduction of key results | Future |

**Gate mapping.** Stage A ⇒ Release Gate 1 eligibility; A + B (+C) ⇒ Gate 2 (pilot-ready research tool) for the
supported materials only; D–F are required before any claim of validation for a defined context of use (Gate 3,
never self-declared).

**What each stage cannot show.** B/C contain no biological new bone (bone chips are surrogates). D lacks ground truth
unless histology exists. E is limited to the materials and species studied. Every report states the stage of evidence
behind each endpoint.
