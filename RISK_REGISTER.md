# Risk Register

Likelihood (L) and impact (I) on 1–5; score = L×I. Owner "F" = founder decision required.

| ID | Risk | L | I | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-01 | Graft and new bone are not separable for common materials (autograft, allograft, DBBM, some HA) by any single-timepoint method | 4 | 5 | 20 | Separability advisor + abstention; day-0 registration workflow; material characterisation service; honest scope | lead | open |
| R-02 | Synthetic-trained models fail on real scans | 5 | 4 | 20 | Phantom v2, domain randomisation, few-shot fine-tuning; require customer calibration scans. Status 28 Nov: Gen-0 synthetic model 0.377 zero-shot on real dog scans (0.513 with 2× zoom); domain randomisation was worse on every test scan (S2 b); few-shot results pending (S2 c) | lead | open (materialised) |
| R-03 | No real three-class labelled data obtainable without partners | 4 | 5 | 20 | Physical phantom programme (validation/); pilot data agreements (F) | F | open |
| R-04 | Customers already satisfied with CTAn/Dragonfly + manual workflows | 3 | 5 | 15 | Customer discovery before scaling; focus on audit trail + abstention + study reports | F | open |
| R-05 | University IP ownership claim over work done while a student | 3 | 5 | 15 | Review university IP policy with OTM/counsel; documented separation of resources (docs/ip) | F | open |
| R-06 | Desktop packaging fails on Windows/macOS (untestable here) | 3 | 3 | 9 | CI matrix runs the test suites on all three OS (green); bundle workflow never run (founder decision #21); selftest flag; early founder test on own machine | desktop | open |
| R-07 | LGPL (Qt) compliance error in commercial distribution | 2 | 4 | 8 | Dynamic linking, one-folder build, notices, relink instructions | desktop | open |
| R-08 | Overclaiming (GLP/Part 11/validation) in sales materials | 2 | 5 | 10 | Claims checker; review cycles; mandatory disclaimers | lead | open |
| R-09 | CPU-only inference too slow for full-resolution studies | 4 | 3 | 12 | ONNX/int8, tiling, ROI-cropped inference, optional GPU; measure | lead | open |
| R-10 | Training on non-commercial datasets contaminates commercial weights | 2 | 4 | 8 | Licence enforcement in training (FA-26); model cards | lead | open |
| R-11 | Single founder, no imaging-scientist co-founder | 4 | 4 | 16 | Advisor recruitment plan (outreach drafts, unsent) | F | open |
| R-12 | Time-saving claim unproven | 4 | 3 | 12 | Instrumented timing in app; timed user study | F | open |
| R-13 | Data loss / corruption of customer studies | 2 | 5 | 10 | Atomic writes, audit chain, backup guidance, destructive tests | QA | open |
| R-14 | Pricing far from willingness to pay | 3 | 4 | 12 | Pricing validation plan in discovery interviews | F | open |
| R-15 | The shipped advisor reports almost nothing on the materials customers use: in S1H4 residual graft only for HA, total mineral in 2% of specimens, new bone never, nothing with the material Unspecified | 4 | 5 | 20 | Position as material characterisation and feasibility assessment (founder decision #20); physical phantom study (stage B) to measure real profiles; next advisor version only with a held-out test | F | open |
| R-16 | Scan-measured blur under-reads at high noise, so the advisor's partial-volume margins are too narrow in noisy scans (B1-blur, DF-041) | 3 | 4 | 12 | Held-out conditions so far stayed above 0.88× the reference; fix in the next advisor version (treat blur as unmeasured at high noise) with a held-out test | lead | open |
| R-17 | Public repository discloses inventive work daily (US and grace-period clocks; foreign rights) | 4 | 4 | 16 | Founder decisions #1, #2, #17, #19 with counsel; invention register records disclosure dates | F | open |
| R-18 | Container restarts interrupt long CPU experiments | 3 | 2 | 6 | Per-structure checkpointing (S1H4/S1H5), models saved before evaluation, queue resumable; interruptions recorded in the deviations log | lead | mitigated |

