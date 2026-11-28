# Benchmark Scorecard

Each target states its justification. **Data class** is always shown: SYN (synthetic phantom with exact truth),
REAL-2C (real scans, two-class bone labels), REAL-REF (real data against a reference software), REAL-3C (real
three-class truth: none exists yet). A target met on SYN data is evidence of *mechanism*, not of product accuracy.

| # | Measure | Data | Target | Justification | Gen-0 value | Current | Met? |
|---|---|---|---|---|---|---|---|
| B1 | Bone segmentation Dice, real held-out specimens (mean, 95% CI) | REAL-2C dog | ≥0.85 | Above Gen-0 real U-Net 0.826; comparable to reported inter-observer ranges for bone masks (assumption pending knowledge-base references) | 0.826 | — | — |
| B2 | Synthetic-pretrained model after ≤3 real labelled scans | REAL-2C dog | ≥0.95 × full-real model | Few-shot is the product's onboarding path | 0.781 (0.95×) | — | — |
| B3 | Synthetic zero-shot on real | REAL-2C dog | ≥0.70 | Gen-0 0.379 means sim→real gap is the dominant risk; 0.70 = usable as pre-label for editing | 0.379 | — | — |
| B4 | Graft volume relative error, specimen level, in supported regimes | SYN | |bias| ≤5%, 95% LoA within ±15% | Product reports volumes, not Dice (ADR-G2-05) | not measured | — | — |
| B5 | Separability advisor: unsupported cases correctly refused | SYN (overlap regime + held-out materials) | ≥95% of cases whose true volume error >20% are refused, with P(fail \| supported) upper 95% bound ≤ 0.10 | Abstention preferred to wrong numbers | not built | Advisor 1.3.3 (S1b/S1c): 100% of failures refused on every endpoint; 0 supported failures. Upper bound ≤0.10 reached for total mineral (0.071 dataset, 0.088 sweep); not demonstrable for graft (0.27) and new bone (0.34) because few cases are supported | **Partly met.** Held-out S1H (1.3.3): mineral passed, graft at threshold, new bone failed. Held-out S1H2 (1.4.0): **residual graft passed** (0/68 supported failed, bound 0.053), new bone refused throughout, **total mineral failed** at heavy blur (10/141) |
| B6 | Failure detection AUROC (predict specimen Dice <0.8 or volume error >20%) | SYN ID+OOD | ≥0.85 | Gen-0 OOD AUROC 0.66 (weak) | 0.66 (OOD) | — | — |
| B7 | Conformal 90% interval coverage for graft volume | SYN held-out | 0.87–0.93 | Valid marginal coverage at nominal level | not measured | — | — |
| B8 | Longitudinal graft Dice with granule displacement ≤200 µm + fragmentation | SYN v2 | ≥0.80; registration failures flagged with sensitivity ≥0.95 | Gen-0 tested only shrink-in-place | 0.915 (best case) | Dice 0.535 at 50 µm, 0.24 at 200 µm (strut-like, overlap density, σ=150); registration failures flagged 100%; advisor refuses all failed cases | **Not met** (accuracy); safety met |
| B9 | Morphometry Tb.Th agreement with Scanco IPL, held-out cubes, convention pre-registered | REAL-REF | ICC(2,1) ≥0.95 | Gen-0 0.983 was post hoc on same cubes | 0.983 (post hoc) | — | — |
| B10 | Segmental ROI success after bridging | SYN | ≥90% success or explicit flagged fallback | Gen-0 50% explicit failures | 50% fail | — | — |
| B11 | Inference throughput CPU (4 cores) | SYN 256³ | ≥250k voxels/s | Gen-0 49k voxels/s → 34 min per 100 M voxels | 49k | — | — |
| B12 | Bit-identical reproducibility | SYN | 100% | Audit/reproducibility requirement | 100% | — | — |
| B13 | Desktop: import → report on 512³ scan without UI freeze; peak RAM ≤4 GB | SYN | yes | Workstation usability | n/a (web) | — | — |
| B14 | Test coverage critical / overall | code | ≥95% / ≥90% | Mandate | unknown | — | — |
