# OsteoQuant Desktop: Performance Qualification (PQ) Plan

| Field | Value |
|---|---|
| Document ID | OQ-QMS-PQ-001 |
| Version | 0.2 (DRAFT), Generation-2 desktop re-baseline |
| Date | 2026-11-27 |
| Prerequisite | Approved IQ and OQ on the workstation(s) used |
| Owner | Scientific Lead (with Quality) |

> **Status: DRAFT plan. No PQ study has been executed. No claim of 21 CFR Part 11 compliance, GLP compliance, computerised-system validation or regulatory acceptance.**
> Numeric acceptance criteria below are **proposals** to be justified and approved by the Scientific Lead before execution; they are not derived from any regulation. All supporting evidence to date is synthetic or from public non-defect datasets (EXPERIMENT_REGISTRY.md); none of it is PQ evidence.

## 1. Objective
Demonstrate that OsteoQuant Desktop, operated by trained users following SOP-001…009, produces scientifically fit-for-purpose results for a **defined context of use**, and that the measurement-support advisor abstains where results would not be fit for purpose:

> *Context of use (proposed):* quantification of new bone, residual graft and host bone volumes within a standardised defect ROI in ex vivo micro-CT of [species] [defect model] treated with [graft material class], scanned at [voxel size range] on [scanner models], with endpoints reported only where the advisor states them as supported.

Each new species, defect model, graft material class or scanner family is a separate context of use requiring its own PQ, or a justified bridging study.

## 2. Reference data ("truth")
| Ref set | Description | Use |
|---|---|---|
| REF-PH | Physical phantoms: HA calibration phantom, machined plates/rods, commercial graft materials in holders with a bone reference (validation/PHANTOM_EXPERIMENT_PROTOCOL.md) | Geometry, density, separability and advisor decisions on physical data |
| REF-GT | ≥ N specimens (proposed N ≥ 20 across groups and time points) manually segmented by two independent experts blinded to group, with adjudicated consensus; experts not involved in model training | Segmentation agreement |
| REF-HIS | Subset with co-registered undecalcified histology/histomorphometry (resin-embedded; see review BIO-07) | New-bone vs graft discrimination |
| REF-ALT | Same specimens analysed with the laboratory's established workflow | Method comparison (agreement alone is not acceptance: review CRO-01) |
| REF-D0 | Animals with implantation-day (day-0) and later scans | Longitudinal QC and day-0 propagation |

PQ specimens must be disjoint from model training data (by animal, ideally by study). Validation records (URS-160) may be created only from REF-PH, REF-GT or REF-HIS data that meet `ValidationRecord.qualifies`.

## 3. PQ studies
| ID | Study | Design | Proposed acceptance criteria | Risks |
|---|---|---|---|---|
| PQ-01 | Segmentation agreement | Automated (pre-correction) vs REF-GT, per class, only for endpoints the advisor supports | Dice, volume error and Bland–Altman bias/limits per class. Proposed: new-bone Dice ≥ 0.80; NBV relative bias within ±10 %; graft class with its own criterion | RSK-09 |
| PQ-02 | Human-in-the-loop performance | ≥ 3 trained analysts follow SOP-003 in the desktop on REF-GT, with opt-in workflow timing enabled | Post-correction ICC(2,1) for NBV/TV ≥ 0.90; correction magnitude and active time reported from the timing export | RSK-09, RSK-35 |
| PQ-03 | ROI reproducibility | ≥ 3 analysts place ROIs on ≥ 10 specimens twice, ≥ 1 week apart | Intra- and inter-operator CV of TV ≤ 5 %; NBV/TV ICC ≥ 0.90 | RSK-06 |
| PQ-04 | Longitudinal consistency | REF-D0 pairs: registration QC, ROI propagation, granule tracking | Registration QC agrees with independently measured misregistration; ROI repositioning error ≤ 1 voxel-equivalent × k (to be set) | RSK-07, RSK-41 |
| PQ-05 | Measurement-support correctness on physical data | REF-PH graft materials and REF-GT specimens across noise/voxel sizes: compare advisor decisions with the measured graft-volume error | Among endpoints stated *supported*, the proportion with error > 20 % has a Clopper–Pearson upper bound ≤ 10 % (proposed); every failure-prone condition is refused or conditional | RSK-37, RSK-11 |
| PQ-06 | Method comparison | OsteoQuant vs REF-ALT and REF-HIS on the same specimens | Bland–Altman bias and 95 % LoA within a pre-set margin; no proportional bias; disagreements explained by REF-HIS | RSK-14 |
| PQ-07 | End-to-end dry-run study | Full desktop workflow incl. blinding, SAP lock, unblinding, sign-off, archive export, backup and restore | All records complete; audit review (SOP-005) finds no unexplained events; restore verifies; report regenerates identically | RSK-12, RSK-16, RSK-18, RSK-30 |
| PQ-08 | Sensitivity to a known effect | Groups with an expected difference (e.g. empty defect vs autograft) | Direction and magnitude consistent with REF-ALT / histology | RSK-09 |
| PQ-09 | Material characterisation | Characterise each graft material (material-only and day-0 routes); reuse across compatible and incompatible protocols | Characterised profile reproduces the measured intensity distribution within a pre-set tolerance; incompatible reuse refused | RSK-40 |

## 4. Statistics for PQ
Pre-specify sample sizes with rationale, equivalence margins and analysis methods (Dice, Bland–Altman, ICC model, Passing–Bablok/Deming as appropriate; Clopper–Pearson for advisor failure rates). Report all specimens; exclusions only per pre-defined criteria. Abstained endpoints are reported as abstentions, not dropped.

## 5. Personnel
Analysts trained on SOP-001…009 with training records; experts producing REF-GT documented with qualifications; Quality reviews protocol and report.

## 6. Deliverables
PQ protocol (instantiated from this plan, with fixed criteria), raw results, PQ report with a conclusion per context of use, and a limitations statement to be reproduced in user documentation. Wording such as "validated context of use" may be used only after the PQ report is approved.

## 7. Re-qualification triggers
New model release or new validation record (SOP-007); change of advisor policy version; change in context of use; major software change affecting segmentation, morphometry or measurement support (CHANGE_CONTROL); adverse trend in periodic review.

## Change history
| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-27 | Generation-1 plan |
| 0.2 | 2026-11-27 | Desktop baseline; PQ-05 changed to measurement-support correctness on physical data; PQ-09 material characterisation added; PQ-02 uses opt-in workflow timing; REF-D0 added |
