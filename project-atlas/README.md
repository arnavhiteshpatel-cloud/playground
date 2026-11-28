# Project Atlas — Master Index

Evidence-driven search for the strongest from-scratch operating business to serve as the founder's first
cash-generating company and the base of a future diversified holding company.
Separate from OsteoQuant/Concord. This folder is self-contained and can be moved to its own repository.

**Status:** see `00_governance/PROGRESS_LEDGER.md` (single source of truth for what is done / in progress).

## Start here (founder)
1. `10_deliverables/EXECUTIVE_DECISION_MEMO.md` — the recommendation (when complete).
2. `10_deliverables/MASTER_RESEARCH_REPORT.md` — full findings.
3. `10_deliverables/Atlas_Opportunity_Workbook.xlsx` — every opportunity, sortable/filterable, with scores.
4. `06_playbooks/` — standalone finalist playbooks; `08_financial_models/` — editable models.
5. `10_deliverables/CHATGPT_DEEP_RESEARCH_HANDOFF.md` — for independent verification.

## Folder map
| Folder | Contents |
|---|---|
| `00_governance/` | Mandate & founder brief, methodology, scoring framework, evidence standards, agent protocol, progress ledger, decision log, limitations, unresolved questions |
| `01_taxonomy/` | Workstream definitions, industry taxonomy, commercial-mechanism taxonomy |
| `02_discovery/` | Stage A raw outputs per workstream (`WSnn_opportunities.jsonl`, `WSnn_sources.jsonl`, `WSnn_summary.md`) |
| `03_screening/` | Stage B: merged scores, blind re-scores, calibration analysis, advancement + rejection lists |
| `04_industry_investigations/` | Stage C memos |
| `05_deep_dives/` | Stage D commercial deep dives |
| `06_playbooks/` | Stage E finalist playbooks |
| `07_review/` | Stage F adversarial reviews and pre-mortems |
| `08_financial_models/` | Model assumption files (JSON) and generated XLSX workbooks |
| `09_databases/` | Canonical machine-readable datasets: opportunities, sources, evidence, suppliers, prospects, risks |
| `10_deliverables/` | Final reports, workbook, memos, handoff |
| `tools/` | Python utilities (validation, merge, scoring, workbook and model builders) |

## How to resume after an interruption
1. Read `00_governance/PROGRESS_LEDGER.md` — the last completed step and the next step are recorded there.
2. Read `00_governance/DECISION_LOG.md` for decisions already made (do not re-litigate them without new evidence).
3. Check data integrity: `python3 tools/validate_discovery.py --all`, then `python3 tools/merge.py` and
   `python3 tools/score.py` (both idempotent; they rebuild `09_databases/` and `03_screening/` from raw files).
4. Agent briefs for each stage live in `00_governance/` (protocol files); reuse them for new agents.
5. Rebuild deliverables: `python3 tools/build_workbook.py` and `python3 tools/build_fin_model.py --all`.

## Authorization boundaries
Research and drafting only. Nothing in this folder has been sent to anyone; no accounts, contracts, bids,
applications, or spending. Drafted outreach materials are for the founder's review.
