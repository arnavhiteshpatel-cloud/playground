# Progress Ledger

| Date (UTC) | Step | Status | Notes |
|---|---|---|---|
| 2026-11-28 | Workspace, governance, scoring framework, evidence standards, agent protocol, validator | done | `00_governance/`, `tools/validate_discovery.py` |
| 2026-11-28 | Stage A: 18 discovery workstreams launched in parallel | in progress | WS01–WS18 → `02_discovery/` |
| 2026-11-28 | Tooling: merge.py, score.py (weights, shrinkage, 13 ranking profiles, Dirichlet weight sensitivity), build_workbook.py, fin_engine.py + build_fin_model.py + verify_fin_model.py | done | Model formulas verified vs Python mirror (60/60 values match after LibreOffice recalc) |
| 2026-11-28 | Stage B–F protocols written | done | BLIND_RESCORE, STAGE_C, STAGE_D, STAGE_E, STAGE_F protocols in `00_governance/` |

## Next step
When Stage A files land: `python3 tools/validate_discovery.py --all` → `python3 tools/merge.py` →
`python3 tools/score.py` → launch blind re-scoring → Stage B selection.
