# OsteoQuant — Founder Operating Manual (Generation 2: the desktop application)

Written for a founder who is still learning software engineering. Read it once from top to bottom, then use it as a
reference. Commands marked *checked* were run in the Generation-2 build environment (Linux); everything else says what
it is based on. The detailed user documentation is `docs/desktop/USER_GUIDE.md` and `docs/user/`; this manual tells
you what you, as the person responsible, need to do and to know.

**Status you must keep repeating:** research prototype; not tested on real graft materials; not a medical device; no
GLP or Part 11 claim; all graft-versus-new-bone evidence is from computational phantoms (SYNTHETIC).

---

## 1. What exists

| Layer | Where | Purpose |
|---|---|---|
| Desktop application | `osteoquant/desktop/` (PySide6 + VTK) | the product: projects, import, viewer, editing, analysis, review, reports, audit trail |
| Analysis library | `osteoquant/` (`io/`, `qc/`, `roi/`, `segment/`, `morphometry/`, `report/`, `audit/`, ...) | everything the desktop calls; also usable from Python |
| Measurement-support advisor | `osteoquant/advisor/` (version in `separability.py`, `ADVISOR_VERSION`) | decides per scan which endpoints may be reported; the scientific core |
| Packaging | `packaging/` | PyInstaller builds, licence notices, bundle licence check |
| Experiments | `experiments/*.py` → `experiments/results/*.json` | every result number comes from here |
| Tests and CI | `tests/`, `.github/workflows/ci.yml`, `desktop-release.yml` | run before any change you keep |
| Ledgers | root `*.md` (`EXPERIMENT_REGISTRY.md`, `EVIDENCE_LEDGER.md`, `FOUNDER_DECISIONS.md`, ...) | what is known, what is claimed, what you must decide |
| Web server (Generation 0) | `osteoquant/api/`, `web/` | kept as an optional interface; not the product |

## 2. Install

### From source (your own Mac, Linux or Windows machine)
Python 3.12 or later is required (`docs/user/INSTALLATION.md`: the Zarr codec package needs 3.12).
```bash
git clone <repository> osteoquant && cd osteoquant
python3 -m venv .venv && source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[desktop,dev]"                           # application + test tools
python -m osteoquant.desktop --selftest                   # checked: prints PASS/FAIL per step, exit code 0 = all passed
```
PyTorch is only needed to train models (`pip install -e ".[train]"`). The desktop uses classical segmentation and,
optionally, ONNX models.

### From a built package
Linux: unpack the archive and start `OsteoQuant/OsteoQuant`; check it with `OsteoQuant/osteoquant-desktop-console
--selftest`. The only packaged Linux build (`packaging/dist/`, built 27 Nov 2026) predates advisor 1.3.1–1.4.3 and
the cycle-2/3 fixes; rebuild it (§11) before any use. Windows and macOS packages are configured in CI but **have never been built or run**; their first CI run
is their first test (`docs/user/INSTALLATION.md`). Builds are unsigned: SmartScreen and Gatekeeper will warn.

## 3. Run
```bash
osteoquant-desktop                        # or: python -m osteoquant.desktop
osteoquant-desktop --project /path/to/project --theme dark
python -m osteoquant.desktop --version    # checked: prints "OsteoQuant Desktop 0.1.0"
```
The start page offers *New project*, *Open project* and recent projects, and shows the licence state ("Evaluation
mode" is normal today).

## 4. Create a project and users
1. *File > New project*: name, a **new empty folder**, your user name, full name and a password (policy in
   `docs/desktop/USER_GUIDE.md` §2: minimum length, an upper-case letter and a digit). You become administrator.
2. *Project > Users...*: add one account per person. Roles: analyst, reviewer, study director, administrator.
3. **Sign-off needs two people.** An author can never approve their own ROI, segmentation or report (separation of
   duties). For practice, create a second "reviewer" account for yourself, but never use one person's two accounts on
   real work.
4. *Project > Idle lock...* sets the automatic lock; *Project > Lock now* (Ctrl+L) locks immediately.

A project is a folder (database + `data/` + `osteoquant-project.json`). Keep it on a local, backed-up drive. Never put a
project folder, a customer scan or a result into the git repository.

## 5. Create a study and import scans
1. *Study > New study*: species, defect model (condyle, calvarial, segmental), graft material, **data class**
   (own research, customer, public dataset, synthetic/demo; printed on every report page) and whether it is blinded.
2. *Study > Add group* for each treatment arm.
3. *File > Import scans* (four steps): select files or folders → **confirm voxel spacing** (no default is assumed; every
   physical number depends on it) → assign animal, group, timepoint and **days since implantation** → import and QC.
4. Read the QC panel: *deterministic* checks are facts about the file; *heuristic* checks use developer-chosen
   thresholds and are prompts, not standards. Rejected files are listed with the reason; nothing is silently dropped.

## 6. Analyse and read the results
1. Select scans, an animal, a group or the study → **Analyse...**. Set the defect model, nominal diameter, the graft
   material actually implanted (or *Unspecified*, the conservative choice) and the time since implantation.
2. Jobs run in the background (*Jobs* panel) and can be cancelled. *needs ROI* means automatic ROI detection failed:
   put the crosshair at the defect centre, *Study > Define cylindrical ROI at crosshair*, analyse again.
3. **Results** tab: the *Support* column reads supported, flagged, not supported or not analysed. An endpoint the
   advisor refuses reads **not measured** — in the table, the CSV and the PDF — and never shows a number. Select a row
   to see the reasons.

How to explain a refusal: "the graft and new bone cannot be told apart for this material, scan and timepoint, so the
software says why it will not split them, and reports total mineral only if the scan's blur and noise allow it." In
the held-out simulation S1H3 (SYNTHETIC), total mineral volume supported in 10% of held-out specimens (sharp imaging
only) and no volume endpoint supported for 58% of held-out specimens, so expect many scans with no volume at all.
Per-material behaviour of the shipped advisor:
`python3 scripts/material_support_table.py` (prints the table from the shipped code).

## 7. Correct, review and sign off
1. Open a scan; *Segmentation* panel: brush (B), eraser (E), region grow (G), fill holes (H), interpolation; Ctrl+Z
   undoes. **Save as new revision** (Ctrl+S) asks for a reason; the original is never overwritten.
2. As a second user: *Review* panel → check the yellow ROI outline → **Accept ROI...** (password); select the
   segmentation version → *What changed* (tick *Highlight changes vs parent*) → **Approve / Request changes / Reject**
   with the meaning of the signature.
3. **Blinded review mode** hides allocation everywhere. For a study created as blinded, only the study director or an
   administrator can unblind it (*Study > Unblind study...*), as a signed and recorded action.

## 8. Reports
*Reports* tab → **Generate defect-fill report** → page through the preview → **Export...** (PDF, CSV, signed copy).
Before approval the PDF and the stored bundle are re-hashed; a changed file refuses the signature. Unlicensed reports
carry "EVALUATION COPY - NOT FOR STUDY DECISIONS". Current sample reports (SYNTHETIC, made through the desktop path):
`reports_samples/DefectFill_SAMPLE4_gen2_synthetic_betatcp.pdf` and `..._SAMPLE5_gen2_synthetic_ha.pdf`
(regenerate with `python3 scripts/make_gen2_sample_reports.py`). SAMPLE1–3 are Generation 1 and superseded.

## 9. Licences
* Without a licence the application runs fully in **evaluation mode** with watermarked reports.
* Only a **published test key** exists (`osteoquant/licensing/keys.py`; `PRODUCTION_KEYS` is empty). Test licences
  (`tools/make_test_licence.py`) prove nothing and must never be given to anyone.
* Creating a production key (offline machine, private key never in git or CI) and the EULA with its LGPL carve-out are
  founder decision #12 in `FOUNDER_DECISIONS.md`; procedure in `docs/desktop/PACKAGING.md` §Licence signing key.
* While the source code is public with no licence file, licence revenue has no enforceable basis (decision #2).

## 10. Backups and the audit trail
* **Back up:** close the project (or quit), copy the whole project folder to a second device; database and `data/`
  belong together (`docs/user/DATA_PROTECTION.md` §Backups).
* **Restore check:** copy the backup to a new place, open it, *Audit trail > Verify chain*, regenerate one report and
  compare it with the archived one.
* **Anchor:** after each working session write the event count and head hash shown by *Verify chain* somewhere outside
  the project. A later shorter chain means events were deleted.
* *Audit trail > Export...* writes CSV/JSON with the chain-verification result, re-checkable from the file alone.

## 11. Build packages
```bash
pip install -e ".[desktop]" pyinstaller pypdfium2 onnxruntime
python packaging/build.py      # -> packaging/dist/OsteoQuant/ and an archive; runs the licence check and the self-test
```
`packaging/dist/build-info.json` records the result. The build **fails** on any GPL-only Qt module or unmapped bundled
library. Do not distribute or use any archive yet: the Linux build on disk (27 Nov) predates the complete notices,
advisor 1.3.1–1.4.3 and the cycle-2/3 fixes (`docs/desktop/PACKAGING.md` §Distribution status), and the LGPL source
arrangement and the EULA are counsel questions (decision #12). Windows/macOS builds run only in CI
(`.github/workflows/desktop-release.yml`) and have never been run. That workflow creates no GitHub Release, but on a
manual dispatch or a `desktop-v*` tag it uploads the unsigned application archives as workflow artifacts, which any
signed-in GitHub user can download from this public repository: starting it is a distribution (decisions #12, #21;
B-013). Pull-request runs upload only the licence report and build information. Code signing needs certificates
issued to a company, so it waits for incorporation (decision #5).

## 12. The synthetic demo project
```bash
QT_QPA_PLATFORM=offscreen python3 -c "from osteoquant.desktop.demo import build_demo_project; \
build_demo_project('demo/demo_project')"                                  # checked: about 20 s on 4 CPU cores
osteoquant-desktop --project demo/demo_project
```
Users `analyst` (administrator) and `reviewer`; their passwords are the constants in `osteoquant/desktop/demo.py`.
They are **public**, so use this project for demonstrations only. The project contains β-TCP condyle phantoms at
"Week 4", one raw NumPy file that needed its spacing typed in, and one deliberately corrupt file (rejected on import).
The demo walk-through is `founder/DEMO_SCRIPT.md`.

## 13. Making changes safely
1. **Before pushing anything, check the standing instruction on pushing (`FOUNDER_DECISIONS.md` #2 and #17).** The
   only instruction on record is the founder's 27 Nov decision to push all work publicly (`docs/ip/IP_STRATEGY.md`
   Addendum); under it, new advisor mechanisms were pushed on 28 Nov. Each public push of new inventive work starts
   its own one-year US patent clock and ends confidentiality; record its date in `docs/ip/INVENTION_REGISTER.md`.
2. Create a branch; change code; run the tests as CI does:
   `python -m pytest -q --ignore=tests/desktop -m "not slow"` then `python -m pytest -q tests/desktop`.
3. If you changed analysis or advisor code: bump `ADVISOR_VERSION`, re-run the affected experiment, and record the
   change in `EXPERIMENT_REGISTRY.md` and `docs/science/PREREGISTRATION.md` (deviations log). A changed advisor needs a
   **new** pre-registered held-out test; re-running old held-out sets is only a development check.
4. Run `python3 scripts/check_claims.py` (numbers in documents against result files; banned wording).
5. Rebuild outward material from the files: `python3 investor/build_decks.py` (the three decks),
   `python3 scripts/build_gen2_report.py` (technical report).
6. Commit with a message that says *why*; make dated commits yourself, so your own contribution is on record.

## 14. Reproducing results
Every experiment is a script in `experiments/`; each writes `experiments/results/<name>.json` and is listed in
`EXPERIMENT_REGISTRY.md` with its data class and status. Generation-2 held-out advisor tests: `exp_S1H_heldout.py`,
`exp_S1H2_heldout.py`, `exp_S1H3_heldout.py` (each pre-registered in `docs/science/PREREGISTRATION.md` §7–9).
Longitudinal: `exp_L3_displacement.py`, `exp_L4_registration_qc.py`, `exp_F2_roi_propagation.py`. Real data:
`exp_H_I_real.py`, `exp_S2_sim2real.py`, `exp_S3_selfsupervised.py`. Real datasets: `DATASET_REGISTRY.md`.

## 15. When something breaks
| Symptom | Likely cause | What to do |
|---|---|---|
| Application will not start (Linux) | missing OpenGL/X libraries | install the list in `docs/user/INSTALLATION.md` |
| Cannot continue the import wizard | spacing not confirmed | type the spacing in µm from the scanner log, tick *Confirmed* |
| Scan marked *needs ROI* | ROI detection failed (common for bridged segmental defects) | define a cylindrical ROI at the crosshair; analyse again |
| Everything *not measured*, even total mineral | noisy scan, or new bone not separable from soft tissue | check the QC noise figures; rescan or reconstruct with less noise |
| *Approve* greyed out | you are the author, or your role cannot sign | a second person signs; hover for the reason |
| *Verify chain* reports an altered event | database edited outside the app or damaged | stop working in that project; restore from backup |
| Unexpected error dialog | bug | `error.log` in the settings folder (`docs/user/TROUBLESHOOTING.md`) |

## 16. Words you must not use
Never call anything "validated", "verified" or "independently reviewed"; describe the audit trail only as a
"tamper-evident audit trail (research prototype; not validated)"; never claim GLP or Part 11 compliance; never present SYNTHETIC results as real-world accuracy; never describe the product as AI or an assistant.
Reviews so far were automated reviewer agents, not human experts (`REVIEW_REGISTRY.md`). Quote advisor-validation
results only in the standard S1H3 wording (`EXPERIMENT_REGISTRY.md`), with its caveat.
