# OsteoQuant — Performance Qualification (PQ) Plan

> **Revision pending (2026-11-27, cycle-1 review QA-REG-02).** This draft describes the Generation-1 architecture (FastAPI server + browser workbench). The Generation-2 product is an offline desktop application (PySide6/VTK, in-process analysis library; the API is an optional integration interface). Requirements and protocols must be re-baselined to the desktop product before any qualification activity. Draft only; no compliance is claimed.


| Field | Value |
|---|---|
| Document ID | OQ-QMS-PQ-001 |
| Version | 0.1 (DRAFT) |
| Date | 2026-11-27 |
| Prerequisite | Approved IQ and OQ on the instance used |
| Owner | Scientific Lead (with Quality) |

> **Status: DRAFT — not validated; not a claim of Part 11 compliance or GLP validation.**
> Numeric acceptance criteria below are **proposals** to be justified and approved by the Scientific Lead before execution; they are not derived from any regulation.

## 1. Objective
Demonstrate that OsteoQuant, operated by trained users following SOP-001…009, produces scientifically fit-for-purpose results for a **defined context of use**:

> *Context of use (proposed):* quantification of new bone, residual graft and host bone volumes within a standardized defect ROI in ex vivo micro-CT of [species, e.g., rat/rabbit] [defect model, e.g., critical-size calvarial or femoral defect] treated with [graft material class], scanned at [voxel size range] on [scanner models].

Each new species, defect model, graft material class, or scanner family is a separate context of use requiring its own PQ (or a justified bridging study).

## 2. Reference data ("truth")
| Ref set | Description | Use |
|---|---|---|
| REF-PH | Physical phantoms (e.g., HA calibration phantom, machined plates/rods) and synthetic phantoms | Accuracy of geometry and density |
| REF-GT | ≥ N specimens (proposed N ≥ 20 across groups and time points) manually segmented by two independent experts blinded to group, adjudicated consensus; experts not involved in model training | Segmentation agreement |
| REF-HIS | Subset with co-registered histology/histomorphometry (if available) | Biological plausibility of new-bone vs graft discrimination |
| REF-ALT | Same specimens analysed with an established reference workflow (e.g., the lab's current validated or published method) | Method comparison |

Training/validation/test split of model data must be documented; PQ specimens must be **disjoint** from model training data (by animal, ideally by study).

## 3. PQ studies
| ID | Study | Design | Proposed acceptance criteria | Risks |
|---|---|---|---|---|
| PQ-01 | Segmentation agreement | Automated (pre-correction) vs REF-GT, per class | Report Dice, volume error, and Bland–Altman bias/limits per class. Proposed: new bone Dice ≥ 0.80; NBV relative bias within ±10%; graft class reported separately with its own criterion | RSK-09 |
| PQ-02 | Human-in-the-loop performance | Trained analysts (≥ 3) follow SOP-003 on REF-GT set | Post-correction ICC(2,1) for NBV/TV ≥ 0.90; record correction magnitude and time | RSK-09, RSK-35 |
| PQ-03 | ROI reproducibility | ≥ 3 analysts place ROI on ≥ 10 specimens twice, ≥ 1 week apart | Intra- and inter-operator CV of TV ≤ 5%; NBV/TV ICC ≥ 0.90 | RSK-06 |
| PQ-04 | Longitudinal consistency (if in-vivo serial scans) | Repeated scans/time points | Pre-defined; ROI repositioning error ≤ 1 voxel-equivalent ×k | RSK-07 |
| PQ-05 | Robustness | Vary voxel size within range, scanner, reconstruction setting, graft batch | Change in primary metric within pre-set equivalence margin; out-of-domain inputs flagged | RSK-11 |
| PQ-06 | Method comparison | OsteoQuant vs REF-ALT on same specimens | Bland–Altman bias and 95% LoA within pre-set margin; no proportional bias | RSK-14 |
| PQ-07 | End-to-end dry-run study | Full workflow incl. blinding, SAP lock, unblinding, sign-off, archive export, restore | All records complete; audit trail review (SOP-005) finds no unexplained events; archive restores and report regenerates identically | RSK-12, RSK-16, RSK-18, RSK-30 |
| PQ-08 | Sensitivity to known effect | Specimen groups with expected difference (e.g., empty defect vs autograft) | Effect direction and magnitude consistent with REF-ALT / histology | RSK-09 |

## 4. Statistics for PQ
Pre-specify sample sizes with rationale, equivalence margins, and analysis methods (Dice, Bland–Altman, ICC model, Passing–Bablok/Deming as appropriate). Report all specimens; exclusions only per pre-defined criteria.

## 5. Personnel
Analysts trained on SOP-001…009 with training records; experts producing REF-GT documented with qualifications; Quality reviews protocol and report.

## 6. Deliverables
PQ protocol (instantiated from this plan, with fixed criteria), raw results, PQ report with conclusion per context of use, limitations statement to be reproduced in user documentation and in report footers ("Validated context of use: …" — only once PQ is approved).

## 7. Re-qualification triggers
New model release (SOP-007), change in context of use, major software change affecting segmentation/morphometry (CHANGE_CONTROL), adverse trend in periodic review.
