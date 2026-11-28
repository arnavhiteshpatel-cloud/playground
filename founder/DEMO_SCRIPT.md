# Product Demonstration Script (≈12 minutes)

Audience: orthobiologic R&D lead, CRO imaging lead, or faculty advisor. Tone: research prototype, honest about status.

**Setup (before the call):** `OQ_DEMO_PASSWORD=<choose> python scripts/demo_seed.py && OQ_DB=runtime/demo.db osteoquant serve`; open
http://127.0.0.1:8765; have `reports_samples/` PDFs and `experiments/results/figures/` open in another window.

| Time | Show | Say (accurately) |
|---|---|---|
| 0:00 | Banner at top | "This is a research prototype. Nothing here is validated on your graft material yet — that's what a pilot would test." |
| 0:30 | Log in as `demo_analyst`; Studies list | "Studies are organised by groups, specimens and timepoints. Blinding hides group names from analysts." |
| 1:30 | SYNTHETIC phantom study table | "These six specimens are computational phantoms where we know every voxel's true class. The table shows new-bone and residual-graft fractions per specimen." |
| 2:30 | Open viewer on PH01 | Axial/coronal/sagittal synchronised views; window presets; ROI outline (white); orange new bone, blue graft, pink host bone. |
| 4:00 | Toggle uncertainty | "Yellow/red marks voxels the model is unsure about — the reviewer looks there first instead of re-drawing everything." |
| 5:00 | Brush a few voxels → reason → *Save as new version* | "Every correction becomes a new version with who/when/why; the original is never overwritten." |
| 6:00 | Compare v1 vs v2 (magenta difference) | "You can see exactly what the human changed." |
| 6:30 | Measure tool; 3D graft surface; Export OBJ | |
| 7:30 | Sign as `demo_reviewer` (re-enter password) | "Signatures state their meaning and go into a hash-chained audit trail." |
| 8:30 | Audit trail → *Verify hash chain* | "If anyone edits the database outside the app, verification fails at that row." |
| 9:00 | Open `DefectFill_SAMPLE4_gen2_synthetic_betatcp.pdf` (current code; the Gen-1 SAMPLE1-3 are superseded) | Banners (SYNTHETIC DATA), methods, group stats with bounded CIs, per-specimen table with "n/m" and the reasons, analysis parameters with the timepoint, sign-off. |
| 10:00 | `exp_C_separability.png` and L2 result | "Key finding so far — in simulation only: when graft and new bone have similar density *and* similar shape, single-scan methods fail; a registered day-0 scan keeps graft Dice above 0.8. Do your studies acquire a post-op scan?" |
| 11:00 | Ask | "Could we test this on 3–5 of your retrospective scans, alongside your current analysis, to measure time and agreement?" |

**Never claim**: validated accuracy on real graft, GLP/Part 11 compliance, customer use, regulatory acceptance.

## Recording a demo video
`node scripts/screenshot_demo.js` drives the app with Playwright and saves stills to `investor/screenshots/`. For video,
add `recordVideo: { dir: 'investor/video/' }` to `browser.newContext()` in that script and rerun (tested pattern for
Playwright; video not produced in this session).
