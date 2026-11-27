# OsteoQuant

**Auditable micro-CT analysis for preclinical bone-graft and bone-healing studies — research prototype.**
Separates newly formed bone, residual graft and host bone; measures ASBMR/Bouxsein-style endpoints; records every
human correction in a tamper-evident audit trail; produces DefectFill PDF/CSV reports.

> Status (27 Nov 2026): research prototype. Not validated on real graft materials. Not a medical device. No GLP or
> 21 CFR Part 11 compliance is claimed. Synthetic-trained models and synthetic results are labelled as such.

## Start here
1. **`FOUNDER_HANDOFF.md`** — what exists, what works, what the experiments showed, exact next actions.
2. `deliverables/README.md` — index of all deliverables (report PDF, spreadsheet, decks, packages).
3. `founder/OPERATING_MANUAL.md` — install, run, demo, maintain.

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q                                       # 60 tests
OQ_DEMO_PASSWORD=Choose-A-Pass-1 python scripts/demo_seed.py
OQ_DB=runtime/demo.db osteoquant serve          # http://127.0.0.1:8765
```

## Repository map
| Path | Contents |
|---|---|
| `osteoquant/` | library + API (io, qc, phantom, segment, ml, roi, morphometry, uncertainty, longitudinal, histology, stats, report, audit, study, api) |
| `web/static/` | researcher workbench (viewer, correction, sign-off, audit) · `web/landing/` landing page |
| `experiments/` | Experiments A–P scripts; results in `experiments/results/` |
| `tests/` | unit, integration, end-to-end, security-regression tests |
| `docs/science`, `docs/research`, `docs/quality`, `docs/security` | knowledge base, competitors & datasets, URS/FS/SOPs, reviews & SBOM |
| `business/`, `grants/`, `outreach/`, `validation/`, `publications/`, `investor/` | commercial, funding, collaborators, phantom protocol, manuscripts, decks |
| Ledgers | `MASTER_PLAN.md`, `EXECUTION_STATE.md`, `RESEARCH_LOG.md`, `DECISIONS.md`, `BLOCKERS.md`, `SCIENTIFIC_EVIDENCE.md`, `DATASET_REGISTRY.md`, `COMPETITOR_INTELLIGENCE.md`, `EXPERIMENT_REGISTRY.md`, `REMAINING_WORK.md` |

Data and trained models are not committed (see `.gitignore`); regenerate with the scripts in `experiments/` and the
download commands in `DATASET_REGISTRY.md`.
