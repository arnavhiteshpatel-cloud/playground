# Evidence Ledger (Generation 2)

Every statement in customer-, investor- or grant-facing material must map to a row here or in the Generation-1
ledger `SCIENTIFIC_EVIDENCE.md` (rows 1–7, R1–R12, which remain valid with the caveats recorded there).

## Evidence classes
| Class | Meaning | May be stated as |
|---|---|---|
| E1 VERIFIED-SOURCE | Fact checked against a primary source this project fetched | fact, with citation |
| E2 PUBLISHED | Peer-reviewed finding by others | "X et al. reported…" |
| E3 REAL-RESULT | Result computed by this project on real public data | result with n, CI, dataset |
| E4 SYN-RESULT | Result on synthetic phantoms | "in simulation…" only |
| E5 CLAIM | Vendor/company claim | "X states…" |
| E6 ASSUMPTION | Parameter chosen without measurement | assumption, never as a result |
| E7 HYPOTHESIS | Commercial or scientific hypothesis under test | hypothesis |
| E8 UNKNOWN | Not known | say unknown |

## Generation-2 entries
| ID | Statement | Class | Source / evidence |
|---|---|---|---|
| G2-001 | The Gen-0 product UI required a local server and a browser | E3 (code fact) | FORENSIC_AUDIT FA-13 |
| G2-002 | "≈78% analyst time saving" is an assumption-derived model output, not a measurement | E6 | FORENSIC_AUDIT FA-06; exp_K_M effort_model |
| G2-003 | Synthetic-trained U-Net zero-shot on real dog micro-CT: Dice 0.379 | E3 | exp_H_I_real.json (n=5 test) |
| G2-004 | Day-0 graft-footprint propagation degrades sharply with post-implantation granule motion: graft Dice 0.80 → 0.535 (50 µm) → 0.35 (100 µm) in the overlap regime | E4 | exp_L3_displacement.json (3 specimens/condition) |
| G2-005 | With advisor 1.3.2 and conservative tracking, all 59 failing day-0 measurements in L3 were refused (all 60 measurements were refused, including 1 that was accurate); none supported failed | E4 | exp_L3_displacement.json |
| G2-006 | Assumption-based material profiles can mis-set thresholds (BCP profile vs simulated scanner: −42…−49% graft volume while "supported"); advisor 1.3.1 adds a scan-vs-profile consistency check | E4 | exp_S1b_advisor_threshold.json (1.3.0 run) |
| G2-007 | ONNX Runtime inference matches PyTorch (max probability difference 5×10⁻⁶, identical labels) and is ≈8× faster on this CPU | E3/E4 (spot check, 1 specimen) | O2 queued for the full benchmark |
| G2-008 | No openly downloadable dataset labels residual graft vs new bone voxel-wise (12 sources searched) | E1 | docs/research/DATASET_DISCOVERY_R2.md |

| G2-009 | On a pre-registered held-out simulation (unseen blur, noise texture, densities, phantoms), the advisor kept total-mineral measurements safe (0/47 supported failed) but did not keep new-bone (10/10 supported failed) or all graft measurements (4/16) safe | E4 | exp_S1H_heldout.json; PREREGISTRATION §7 |
| G2-010 | Within the tuning simulator, advisor 1.3.3 refused every failing measurement for all endpoints (S1b/S1c) — an in-sample result | E4 | exp_S1b_advisor_threshold.json, exp_S1c_control_reference.json |

| G2-011 | On a second pre-registered held-out simulation (216 specimens, unseen seeds/densities/blur), advisor 1.4.0 kept every supported residual-graft measurement within 20% (0/68 failed; 95% upper bound on failure rate 0.053) but let 10 of 151 supported total-mineral measurements fail at heavy blur | E4 | exp_S1H2_heldout.json; PREREGISTRATION §8 |

| G2-012 | On the final pre-registered held-out simulation (216 specimens, unseen seeds/densities/blur/noise), advisor 1.4.1 refused every failing measurement on every endpoint; no supported residual-graft (0/80, from 9 phantom structures; 95% upper bound 0.34 with structures as the pre-registered unit, 0.045 if rows were independent) or total-mineral (0/22) measurement failed; new bone was never supported. The precision criterion (bound ≤0.10) is not demonstrated at the structure level | E4 | exp_S1H3_heldout.json; PREREGISTRATION §9 |
| G2-013 | The advisor's safety was reached by sacrificing coverage: residual graft supported in 37%, total mineral in 10% and new bone in 0% of the final held-out specimens; for 58% of specimens no volume endpoint was supported at all | E4 | exp_S1H3_heldout.json |

(Entries are appended as Generation-2 experiments complete.)
| G2-014 | Registration QC that projects block shifts onto directions the anatomy constrains flagged all 6 harmful misalignments, passed 78% of harmless ones, and passed 16/16 correctly propagated segmental ROIs (propagated ROI Dice mean 0.984, min 0.963) | E4 | exp_L4_registration_qc.json, exp_F2_roi_propagation.json (re-runs 2026-11-28) |
| G2-015 | The Gen-0 synthetic U-Net segments real dog bone at Dice 0.377 zero-shot; upsampling the real scan 2× (zoom chosen on training scans only) raises it to 0.513, pointing to a structure-scale mismatch between phantom and real trabeculae | E3 (real, 5 test scans) | exp_S2v2_sim2real_a.json |
| G2-016 | Among held-out specimens the advisor supported, graft-volume bias was +0.1% (95% LoA −9.7…+9.8%, n=80) and total-mineral bias −1.2% (LoA −4.0…+1.6%, n=22); derived, not pre-registered, and conditional on support | E4 | analysis_B4_volume_agreement.json |
| G2-017 | Registration QC that verifies only the directions anatomy constrains must fail closed: on segmental phantoms without axial structure in the QC shell, 0/18 misregistrations (160–400 µm, every axis) passed after the fix, and aligned cases are reported as not verifiable rather than passed; on short bridged specimens (F2) the bone ends make the axis verifiable and QC passed 16/16 | E4 | exp_L5_qc_axial.json, exp_F2_roi_propagation.json |
| G2-018 | With the graft material unspecified, advisor ≤1.4.2 supported total mineral with +21…+44% error next to dense, blurred graft; 1.4.3 uses voxels brighter than host bone as the graft proxy for the ambiguous-rim gate and refused all such cases in the probe (at the cost of also refusing some accurate ones) | E4 | cycle-3 review C3-SCI-01; tests/test_advisor.py |
| G2-019 | On the pre-registered held-out simulation S1H4 of the shipped advisor 1.4.3 (720 specimens from 36 unseen phantom structures, the application's knowledge-base and Unspecified material paths), every failing measurement was refused on every endpoint and no supported measurement failed (residual graft 0/69 from 24 structures, 95% upper bound 0.14 with structures as the unit; total mineral 0/12); the precision criterion (≤0.10) is not demonstrated | E4 | exp_S1H4_heldout.json |
| G2-020 | On the application's material paths the shipped advisor reports little: residual graft supported only for HA (9.6% of specimens), total mineral in 1.7% (β-TCP at one imaging condition, values 7–17% low), new bone never; with the material Unspecified nothing; no volume endpoint for 89% of specimens | E4 | exp_S1H4_heldout.json |
| G2-021 | The advisor's scan-measured blur matches the reference at low noise (median ratio 1.06) but under-reads by up to half at high noise (0.47× at relative noise 0.26; 38% of the noisiest cases more than 20% low) | E4 | exp_B1_blur_estimator.json |
| G2-022 | In the pre-registered held-out precision test S1H5 (advisor 1.4.3; sintered HA residual graft on condyle and segmental phantoms; 192 specimens from 48 structures), residual graft was supported in 70% of specimens, none of the supported measurements failed (95% upper bound 0.074 with structures as the unit; maximum error 12.3%); no residual-graft measurement in that scope failed at all, so refusal ability was not tested | E4 | exp_S1H5_heldout.json |
| G2-023 | Domain-randomised synthetic pretraining (one seed) transferred worse to 5 real dog-forelimb test scans than the Gen-0 synthetic model without any real training data: Dice 0.353 vs 0.377 at native scale and 0.457 vs 0.513 at 2× zoom, worse on every specimen | E3 | exp_S2v2_sim2real_b.json, exp_S2v2_sim2real_a.json |
| G2-024 | On 5 real dog-forelimb test scans (2-class bone), fine-tuning from scratch with 1 real labelled scan reached Dice 0.805 and with 3 scans 0.816; synthetic pretraining (Gen-0 or domain-randomised) did not improve on it (Gen-0 − scratch −0.031 [−0.052, −0.012] at k=1) | E3 | exp_S2v2_sim2real_c.json |

