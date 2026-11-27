# Architecture Decision Records

Earlier product/science decisions D-001…D-019 are in `DECISIONS.md` and remain in force unless superseded here.

### ADR-G2-01 — Parallel workstreams with file ownership (2026-11-27)
**Context.** One repository, several concurrent workstreams. **Decision.** Each stream owns directories: desktop
(`osteoquant/desktop`, `osteoquant/licensing`, `packaging/`, `tests/desktop`, `docs/desktop`); QA (`tests/` except
desktop, `.github/workflows/ci.yml`, `docs/qa`); research (`docs/science/KNOWLEDGE_BASE.md`, `osteoquant/knowledge`,
`docs/research/*_R2*`); competitive/IP (`docs/ip`, `docs/research/COMPETITOR_MATRIX.md`); commercial (`business/`,
`investor/FUNDING_STRATEGY.md`); lead (science modules, experiments, root ledgers, version control). Cross-boundary
changes are additive only. **Consequence.** No merge conflicts; integration review by the lead.

### ADR-G2-02 — Desktop stack: PySide6 + VTK, in-process library calls (supersedes D-002 for end users)
**Context.** Mandate requires a native desktop application without a server, browser or terminal. **Options.**
(a) PySide6 + VTK; (b) Electron + Python backend (still a local server; heavy); (c) 3D Slicer extension (fast to
build but ties the product to Slicer's release cycle, BSD-licensed but brand/UX constrained); (d) napari plugin
(good for science users, weaker for regulated workflow UI). **Decision.** (a): LGPL Qt via PySide6 (dynamic linking
keeps commercial distribution permissible — must ship LGPL notices and allow relinking), BSD VTK, same Python
process as the analysis library, so there is one source of truth for science. The FastAPI layer stays as an
optional integration/automation interface, not the primary UI. **Risks.** Package size (~300–500 MB); macOS
notarisation and Windows signing need founder credentials.

### ADR-G2-03 — Packaging: PyInstaller one-folder per OS, built in CI
One-folder (faster start, easier LGPL compliance than one-file). Linux built and smoke-tested in this container;
Windows/macOS built only in CI (not verifiable here). Signing/notarisation deferred to founder-owned credentials.

### ADR-G2-04 — Measurement support is a first-class output
Every endpoint carries a support status (`supported`, `supported_with_conditions`, `not_supported`) and reason,
computed from material knowledge, measured intensity separability and model uncertainty. Unsupported endpoints are
reported as "not measured" with reason rather than a number. Rationale: FA-16; abstention preferred over plausible
wrong numbers.

### ADR-G2-05 — Model selection on measurement error
Candidate models are ranked on specimen-level volume/fraction error (bias, limits of agreement, ICC) for the
endpoints the product reports; Dice/HD95 are secondary. Rationale: FA-15.

### ADR-G2-06 — Offline licensing with Ed25519 signatures
Licence files are JSON payloads with detached Ed25519 signatures verified against a public key embedded in the
application. Only test keys exist in this repository; production key generation and custody are founder actions.
Evaluation mode runs without a licence and watermarks reports.

### ADR-G2-07 — Experiment outputs redirectable via `OQ_RESULTS`
Reproduction runs write to a separate directory so original results are never overwritten during audits.

### ADR-G2-08 — Projection-domain simulation: TIGRE/ASTRA evaluated, not adopted (FA-22)
**Findings (2026-11-27, this container: 4 CPU, no CUDA).** `astra-toolbox` 2.5.0 installs from PyPI but its 3-D
cone-beam projectors require CUDA (`create_sino3d_gpu` fails: "CUDA driver version is insufficient"); only 2-D CPU
projectors (parallel/fan) work. The TIGRE CT toolbox is not on PyPI: the PyPI package named `tigre` (2.0.4) is an
unrelated MIT-licensed bioinformatics tool ("Tool for InterGenic Region Extraction") — a name collision and a
dependency-confusion hazard; never `pip install tigre` for CT. The CT toolbox is built from its source repository
and its projectors are CUDA kernels, so it cannot run here.
**Licences.** ASTRA is GPL-3.0: it must not be linked into the commercial desktop distribution; TIGRE is BSD-3-Clause
(compatible). **Decision.** Keep the in-house simulator (image-domain mode A + skimage parallel-beam mode B) for
the product and CPU experiments. On a CUDA workstation, add an optional research-only TIGRE cone-beam path for
cone-beam artefacts (Feldkamp cone-angle artefacts, scatter) — record as future work; never ship ASTRA.
