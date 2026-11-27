# Decisions Log

Format: ID — date — decision — rationale — alternatives considered.

- **D-001** — 2026-11-27 — Build in the `playground` repository (empty) rather than `sandbox` (contains an unrelated app). — Avoid mixing projects. — sandbox subdirectory.
- **D-002** — 2026-11-27 — Single Python package + FastAPI + SQLite + dependency-free browser viewer (vanilla JS modules, no build step). — Founder is learning software engineering; one-command install; no microservices; runs on a laptop. — React/TypeScript SPA with a build pipeline (more moving parts; deferred until a frontend hire).
- **D-003** — 2026-11-27 — Own small 3D U-Net in PyTorch (CPU) rather than nnU-Net/MONAI for in-container experiments. — No GPU here (4 CPU, 15 GB RAM); nnU-Net's default plans are GPU-scale. The training pipeline mirrors nnU-Net conventions (specimen-level splits, Dice+CE, patch sampling, deep checkpoints) so the backbone can be swapped once a GPU is available. — MONAI UNet (heavier dependency; equivalent here).
- **D-004** — 2026-11-27 — Report physical density (mgHA/cm³) only when a scan carries a calibration record (slope/intercept from an HA phantom). Otherwise report grey-value statistics labeled "uncalibrated". — Grey values are not interchangeable across scanners/reconstructions (see docs/science).
- **D-005** — 2026-11-27 — All synthetic-trained models are tagged `provenance=synthetic` and the report generator watermarks any output produced by them "SYNTHETIC-TRAINED — NOT FOR STUDY DECISIONS". — Directive: do not present synthetic-trained models as customer-ready.
- **D-006** — 2026-11-27 — Licence-aware data loader: datasets tagged `commercial_use ∈ {allowed, research_only, unclear}`; training scripts refuse to write `commercial` model artifacts from anything but `allowed`. — Keep research-only models separate from potentially commercial ones.
- **D-007** — 2026-11-27 — Statistics at the specimen (animal) level only; voxel-level numbers are used solely for segmentation-agreement metrics, never as biological n. — Prevents pseudoreplication.
- **D-008** — 2026-11-27 — Audit log is an append-only SQLite table with a SHA-256 hash chain (each row hashes the previous row's hash + canonical JSON of the event); verification detects edits/deletions. — Part 11-style technical control; does not by itself constitute compliance.
