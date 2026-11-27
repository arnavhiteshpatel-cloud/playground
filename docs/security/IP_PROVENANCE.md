# IP Provenance Log and Dependency Scan

_Status: prepared 2026-11-27 for review with UIUC OTM and the Landuyt IP Clinic. Not legal advice._

## 1. Where and how this code was created
* All code, documents and synthetic data in this repository were generated on **2026-11-27** by an AI coding agent
  (Claude Code, cloud session) acting on the founder's written directive, in a commercial cloud container — **not on
  university computers, NCSA allocations, or university-licensed software**.
* No university laboratory data, specimens, unpublished results or university-owned code were used.
* External data used are **public** datasets under CC-BY-4.0 (attribution required) — see DATASET_REGISTRY.md.
* Physics constants: NIST XCOM mass attenuation tables (US Government work).
* Literature informed parameter choices; no code was copied from papers or proprietary software. The "CTAn-style"
  baseline implements a generic two-threshold workflow and is not derived from Bruker code.
* **Open questions for OTM** (see outreach/IP_AND_OTM_QUESTIONS.md): does the founder's student status, prior lab
  work, or any future use of the Beckman Versa (university equipment) affect ownership? Agree terms *before* scanning.
* AI-assisted authorship: ownership/copyright of AI-assisted code and documents should be raised with counsel;
  NIH policy treats AI-written applications as not the applicant's own work (see BLOCKERS B-007).

## 2. Components and provenance
| Component | Origin | Licence |
|---|---|---|
| `osteoquant/` package, `web/static/*.js|html|css`, experiments, docs | written in this project | proprietary to founder/company (pending OTM confirmation) |
| `web/static/vendor/three.module.min.js`, `OrbitControls.js` | three.js r160 (npm) | MIT (licence file vendored) |
| `osteoquant/phantom/data/nist_xcom.json` | NIST XCOM web tables | US Government work |
| Trained models in `models/` | trained here on synthetic data (project-generated) and CC-BY-4.0 SPROUT data | weights proprietary; CC-BY attribution for SPROUT-derived models |
| Python dependencies | PyPI | permissive (BSD/MIT/Apache/PSF/MIT-CMU) — see SBOM.csv; no GPL dependency linked |

GPL tools (ITK-SNAP, QuPath) are **not** linked; if used, run them as separate programs.

## 3. Dependency vulnerability scan (pip-audit, 2026-11-27)
Raw output: `docs/security/pip_audit_output.txt`.
* **No known vulnerabilities in OsteoQuant's declared runtime dependencies** (pyproject.toml list).
* Flagged packages are pre-installed in the cloud container and **not used by OsteoQuant**: pypdf, pip, setuptools,
  soupsieve, wheel, oauthlib, httplib2, opentelemetry-api. Action: use a clean virtual environment (`python -m venv`)
  for deployment and keep pip/setuptools current.
* Not auditable from PyPI: `torch 2.15.0+cpu` (PyTorch index build) and `pillow 13.0.0.post1` — check vendor advisories.
* Recommended CI step: `pip-audit -r requirements.lock` on every release (see QUALITY change control).

## 4. Publication / open-source caution
Do not publish the phantom generator, separability benchmark or longitudinal protocol as open source until OTM has
confirmed ownership and the founder has decided what to keep proprietary. A defensible strategy is to publish the
**evaluation benchmark and metrics** (credibility) while keeping trained weights, the material reference library and
the analysis service process proprietary.
