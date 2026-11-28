# Product demonstration script: the desktop workstation in 10 minutes

**Audience:** an orthobiologic R&D lead, a CRO imaging lead, or a prospective scientific advisor.
**Tone:** research prototype; honest about what is synthetic. The point of the demo is the *refusal*: the software
reports a graft or new-bone number only when the scan can support it, and says why when it cannot.

**Everything you show is SYNTHETIC.** The demo project contains computational phantoms (simulated micro-CT of a rabbit
condyle-like defect with β-TCP granules). Their results say nothing about real tissue. Say this at the start and again
whenever a number is on screen.

## Before the call (15 minutes)
1. Build a fresh demo project (`founder/OPERATING_MANUAL.md` §12):
   ```bash
   QT_QPA_PLATFORM=offscreen python3 -c "from osteoquant.desktop.demo import build_demo_project; \
   build_demo_project('demo/demo_project')"
   osteoquant-desktop --project demo/demo_project
   ```
   Sign in as `analyst`. Keep the `reviewer` password at hand (both are demo-only constants in
   `osteoquant/desktop/demo.py`; they are public, so never reuse them).
2. Run `python -m osteoquant.desktop --selftest` once from the source checkout; it must end with `"selftest": "PASS"`.
   The packaged Linux build in `packaging/dist/` (28 Nov, commit `cf6fea7`, advisor 1.4.3) passed its self-test; check
   `build-info.json` against the current commit before demoing it, and do not hand the archive out (B-016).
3. Open in a second window the two sample reports (regenerated at commit `14141db` under advisor 1.4.3, watermarked
   "SAMPLE - SYNTHETIC DATA - NOT FOR STUDY DECISIONS"):
   * `reports_samples/DefectFill_SAMPLE4_gen2_synthetic_betatcp.pdf` (β-TCP, week 4): graft and new-bone endpoints
     refused in 6/6; total mineral reported in 5/6;
   * `reports_samples/DefectFill_SAMPLE5_gen2_synthetic_ha.pdf` (HA, week 8): residual graft reported but flagged "(f)"
     in 6/6 (automatic ROI not yet accepted / QC verdict "review"); new bone refused in 6/6; total mineral reported in 3/6;

   plus the held-out slide of `investor/OsteoQuant_Commercial_Pilot_Deck.pptx` ("Evidence so far, including what
   failed").
4. Close everything else: no customer data, no email, no repository pages with prospect lists on screen.

## The ten minutes

| Time | Show | Say (accurately) |
|---|---|---|
| 0:00 | Start page, "Evaluation mode" | "This is a research prototype running entirely on this laptop: no server, no cloud. It has not been tested on real graft materials, and it makes no GLP or Part 11 claim. Everything you will see is a computational phantom, so I know the true answer for every voxel." |
| 0:45 | Project tree; *Rejected imports (1)* | "Studies are organised by group, animal, timepoint and scan. This file was corrupt; it is listed with the reason instead of being dropped silently." |
| 1:30 | Import wizard on the raw `R99_export.npy` scan (or screenshot `docs/screenshots/desktop/05_import_metadata.png`) | "When a file carries no voxel size, you must type and confirm it. There is no default, because every physical number depends on it." |
| 2:15 | Viewer: double-click `R01_week4`; yellow ROI outline; 3D panel; QC panel | "Linked slices and 3D. The yellow outline is the analysis volume. QC is split into facts about the file and heuristic prompts; the heuristics are ours, not standards." |
| 3:15 | **Results** tab; select `R01_week4`; read the reasons | "This is the core idea. For β-TCP at four weeks, graft and new bone are *not measured*: the material's appearance is uncertain and resorbing β-TCP reaches the bone intensity range. Total mineral is reported only when the scan's blur and noise allow it; read what the screen shows for this scan. Most tools would print a plausible number here." |
| 4:30 | Segmentation panel: brush a few voxels, *Save as new revision*, type a reason; Review panel → *What changed*, tick *Highlight changes* | "Every correction becomes a new version with who, when and why; the original is never overwritten. The reviewer sees exactly what changed." |
| 5:30 | Sign out; sign in as `reviewer`; *Accept ROI...*, then *Approve* the segmentation (password, meaning) | "Two people are needed. The author cannot approve their own work; each signature states its meaning and goes into a hash-chained audit trail." |
| 6:30 | **Reports** tab: *Generate defect-fill report*; page to the per-specimen table | "Refused endpoints print as n/m, with the reason. The report records the advisor version, the timepoint it used and the data class, and carries an evaluation watermark because no production licence exists." |
| 7:30 | **Audit trail**: *Verify chain*; toggle *Blinded review mode* | "If anyone edits the database outside the application, verification fails at that event. Blinded mode replaces animal IDs and groups with random codes everywhere." |
| 8:15 | The held-out slide in the pilot deck | Read the evidence below. Then: "So in simulation the refusals held, but at a cost: for most specimens no volume was given at all, and nobody has tested any of this on real scans yet." |
| 9:15 | The ask | "We are not taking any customer scans today. An evaluation on your data is planned only after we incorporate, sign a data-processing agreement and meet our first release gate; that is still an open founder decision. What I would value now is your view: would a retrospective comparison on completed scans be useful to you later, and what would it have to show?" |

## What to say about the evidence (read it; do not paraphrase the numbers)
* "In the pre-registered held-out simulation S1H4 (advisor 1.4.3; 720 synthetic specimens from 36 phantom structures, knowledge-base and Unspecified material paths; a failure is a volume error above 20%): residual graft volume supported in 10% of specimens (HA only), every failing measurement refused and none of the supported ones failed (95% upper bound on the supported-failure rate 0.14 counting phantom structures as the unit; 0.052 if the 69 supported measurements were independent); supported graft volumes: median error 2.2%, maximum 11.4%; total mineral volume supported in 2% of specimens (β-TCP at PSF 40 µm only); supported mineral volumes: maximum error 16.9%; new-bone volume never supported; no volume endpoint supported for 89% of specimens. An earlier held-out test of advisor 1.4.1 (S1H3, 9 phantom structures) is recorded in the experiment registry." (`experiments/results/exp_S1H3_heldout.json`)
* The caveat, always: "This test used the shipped advisor 1.4.3, frozen before the run. The simulator and the
  advisor share attenuation physics, so this shows internal safety, not accuracy on real scans. No physical validation
  exists."
* The failures, without numbers: "Two earlier held-out tests failed — S1H (advisor 1.3.3) on new bone, S1H2 (advisor
  1.4.0) on total mineral — and each failure led to a rule change that was then tested on new data."
  (`EXPERIMENT_REGISTRY.md`)
* Day-0 scans, only if asked: "In simulation the day-0 method is fragile once granules move: naive day-0 footprint graft Dice — no motion: 0.80; 50 µm motion: 0.535; 100 µm motion: 0.35. We do not offer day-0 analysis."
  (`experiments/results/exp_L3_displacement.json`)

## Honest answers to the questions you will get
| Question | Answer |
|---|---|
| "Does it work on my material?" | "I don't know yet. In simulation, residual graft volume can be supported only for dense calcium phosphates at low noise and early known timepoints, and new-bone volume was never supported in the held-out tests. Real scans would be the first real test, and we are not taking customer data before incorporation, a data-processing agreement and our first release gate." |
| "Is it validated?" | "No. It is a research prototype. The safety results are simulations; a physical phantom study is planned but not started." |
| "Can I use it for a GLP study or a submission?" | "No. We make no GLP or Part 11 claim, and nothing it produces should go into a submission without your own QA." |
| "How much time does it save?" | "Unmeasured. The application can record timing during a pilot; that is one of the things a pilot would measure." |
| "Who reviewed this?" | "Automated reviewer agents so far, not human experts. Human expert review is one of the next milestones." |
| "What does it cost?" | "We are testing prices, not quoting them. A paid pilot would only follow incorporation, counsel-reviewed contracts and our pilot-readiness gate (Gate 2), which needs real-data validation first." |

**Never claim:** accuracy on real grafts, validation, GLP/Part 11 compliance, customers or pilots, regulatory
acceptance, or a time saving. Never call the product AI or an assistant.

## Recording
For screenshots of every screen: `python -m osteoquant.desktop --screenshots OUT_DIR` (synthetic demo project; the
images in `docs/screenshots/desktop/` were made this way). For a video, record the screen with the operating system's
own recorder while following this script; no recording has been produced yet.
