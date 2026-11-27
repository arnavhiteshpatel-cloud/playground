# Low-label adaptation and uncertainty-guided review for three-class bone-graft segmentation (simulation study)

**Status: DRAFT scaffold (2026-11-27). Results below are SYNTHETIC. The decisive version of this paper needs real
labelled scans of at least two graft materials (physical phantoms or pilot data). Do not submit on synthetic data alone
except as a workshop/methods abstract.**

## Question
Playbook hypothesis U3: a model can be adapted to a new graft material or scanner with ≤10 labelled scans; and
uncertainty can direct analyst review to cut hands-on time while preserving accuracy.

## Completed experiments
* **J — adaptation** (`exp_J_adaptation.json`): 3D U-Net pre-trained on four simulated ceramics, adapted to two held-out
  simulated materials (45S5 glass, deproteinised bovine bone mineral); 16 held-out test specimens. Zero-shot graft Dice
  0.843; fine-tuned with k = 1 / 3 / 5 / 10 / 20 labelled scans: 0.874 / 0.908 / 0.900 / 0.914 / 0.919 (fitted asymptote
  0.921). RF from scratch: 0.654 / 0.847 / 0.849 / 0.864 / 0.874. Interpretation: in simulation, ≤3 labelled scans
  suffice to exceed 0.8 — **optimistic**, because held-out materials differ from training materials only in simulated
  density/porosity/resorption, not in morphology or scanner.
* **K/M — uncertainty and modelled review effort** (`exp_K_M_uncertainty.json`, rerun with temperature scaling applied
  and validation-derived thresholds after independent review): see results file for risk–coverage, AURC, ECE, ID-vs-OOD
  AUROC and failure-detection sensitivity/specificity. Effort model uses ASSUMED constants (20 s per reviewed slice,
  90 s per manually delineated slice) and must be replaced by a timed user study.

* **H/I — real-data transfer (completed)**: SPROUT dog forelimb micro-CT (Zenodo 10.5281/zenodo.24047383, CC-BY-4.0),
  10 train / 5 test specimens, bone vs non-bone within a band around labelled bones. U-Net trained on 10 real scans Dice
  0.826; synthetic-trained U-Net zero-shot 0.379 (domain gap); fine-tuned with 1 / 3 real scans 0.787 / 0.781; RF on 10
  real scans 0.758; Otsu 0.508. This is the first real-data evidence for the low-label premise (bone/soft tissue, not graft).

## Pending (requires real data) — [PENDING RESULT]
* Adaptation across real scanners (Bruker/Scanco/Zeiss) and real materials.
* Timed analyst study (n ≥ 3 analysts, ≥ 10 scans) measuring hands-on time and inter-operator ICC with/without
  uncertainty-guided review — this is what tests the playbook's ≥70% time-saving hypothesis.

## Target
MICCAI/ISBI workshop (methods), then a journal version with real data (Medical Physics, Bone, or Tissue Eng Part C).
