# OsteoQuant

**Offline micro-CT analysis for preclinical bone-graft and bone-healing studies — research prototype.**
A desktop workstation that measures defect-fill endpoints and, before it reports graft or new-bone volume, decides per
scan whether that split is identifiable for the material, scan and design. When it is not, it refuses the endpoint and
says why. Every human correction and sign-off is kept in a tamper-evident audit trail; reports are DefectFill PDF/CSV.

> Status (28 Nov 2026): research prototype, unincorporated, no customers. Not validated on real graft materials; all
> graft/new-bone evidence is SYNTHETIC (computational phantoms). Not a medical device. No GLP or 21 CFR Part 11
> compliance is claimed. In the pre-registered held-out simulations the measurement-support advisor reported few
> endpoints: residual graft only for sintered HA, new bone never (`EXPERIMENT_REGISTRY.md`, S1H4 and S1H5).

## Start here
1. **`FOUNDER_HANDOFF.md`** — what exists, what works, what the experiments showed, next actions.
2. `deliverables/README.md` — index of the deliverables (technical report PDF, workbook, decks, packages).
3. `docs/desktop/USER_GUIDE.md` and `docs/user/` — using the desktop application; what can and cannot be measured.
4. `founder/OPERATING_MANUAL.md` — install, run, demo, maintain.

## Quick start (source install)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,desktop]"
python -m osteoquant.desktop --selftest       # headless end-to-end check; must end with "selftest": "PASS"
osteoquant-desktop                            # the desktop application
pytest -q                                     # test counts and coverage: docs/qa/test_summary.json
python scripts/check_claims.py                # customer-facing numbers against their result files
```
Bundles are built with `python packaging/build.py` (`docs/desktop/PACKAGING.md`) or the `desktop-build` CI workflow,
which produced self-tested macOS (Apple silicon) and Linux bundles on 28 Nov; the Windows build fails on a headless
desktop-test crash (DF-044). Nothing is signed or distributed.

## Repository map
| Path | Contents |
|---|---|
| `osteoquant/` | library, measurement-support advisor, desktop application, report generator, audit trail, development API |
| `experiments/` | experiment scripts; results with advisor version and git commit in `experiments/results/` |
| `tests/` | unit, property, fuzz, destructive, desktop and security-regression tests |
| `docs/science`, `docs/user`, `docs/desktop`, `docs/quality`, `docs/security`, `docs/reviews` | methods and pre-registration, user documentation, architecture and packaging, draft quality documents, security reviews, review cycles and responses |
| `business/`, `grants/`, `outreach/`, `validation/`, `publications/`, `investor/`, `website/` | commercial hypotheses, funding drafts, unsent outreach drafts, phantom protocol (not started), manuscript drafts (not submitted), decks, unpublished website |
| Ledgers | `EXECUTION_STATE.md`, `TASK_REGISTRY.md`, `EXPERIMENT_REGISTRY.md`, `EVIDENCE_LEDGER.md`, `BENCHMARK_SCORECARD.md`, `DEFECT_REGISTRY.md`, `REVIEW_REGISTRY.md`, `DECISIONS.md`, `RISK_REGISTER.md`, `BLOCKERS.md`, `FOUNDER_DECISIONS.md`, `REMAINING_WORK.md` |

Data and trained model weights are not committed (see `.gitignore`); regenerate them with the scripts in
`experiments/` and the download commands in `DATASET_REGISTRY.md`. The reviews in `docs/reviews/` were performed by
automated reviewer agents, not by human experts.
