# Deliverables Index (directive §42)

> **Status (2026-11-28).** Generation-2 index. Everything here describes a research prototype: pre-revenue,
> unincorporated, no customers or pilots, no evaluation on customer data agreed, no test on real graft materials, no
> GLP or Part 11 claim. Release gates (`RELEASE_READINESS.md`): Gate 1 not met, Gate 2 not met, Gate 3 never claimed.
> All graft and new-bone evidence is SYNTHETIC (computational phantoms). Before sharing any file, rebuild it from its
> script and run `python3 scripts/check_claims.py` (it reads Markdown, HTML, the decks and PDF text).

| # | Deliverable | Location |
|---|---|---|
| 1 | Technical report, Generation 2 (PDF, cited) | `deliverables/OsteoQuant_Gen2_Technical_Report.pdf` (built by `scripts/build_gen2_report.py`; check its build date and rebuild before use). **Superseded:** the Generation-1 `deliverables/OsteoQuant_Technical_and_Commercial_Report.pdf` (27 Nov; outdated pricing, a GLP study offer and pre-advisor results) — do not share it |
| 2 | Spreadsheet: datasets, experiments, benchmarks, competitors, costs, funding, prospects | `deliverables/OsteoQuant_Master_Workbook.xlsx` (built by `scripts/build_master_spreadsheet.py`); financial model `business/FINANCIAL_MODEL.xlsx` (built by `business/build_financial_model.py`; every figure a hypothesis) |
| 3 | Founder operating manual | `founder/OPERATING_MANUAL.md` |
| 4 | Scientific learning curriculum | `founder/LEARNING_CURRICULUM.md` |
| 5 | Physical phantom experiment package | `validation/` — protocol (not approved, not started), BOM, Beckman access, decisions for the imaging scientist, printable worksheets, label CSVs; programme stages A–F in `validation/VALIDATION_PROGRAM.md` |
| 6 | Grant application preparation package | `grants/` — opportunities, NSF vs NIH eligibility, Specific Aims, NSF Project Pitch, Cozad package, budget, letters, checklist (scaffolds only; the founder writes every application) |
| 7 | Customer discovery package | `business/` — prospects, interview guide + coding scheme + log template, pricing experiment and validation plan, SOW/pilot/quote/DPA/QA templates (none to be sent before M0 and Gate 1), market inputs, revenue model |
| 8 | Collaborator outreach package | `outreach/` — collaborators, draft emails (unsent), OTM/IP questions. Contains personal data of named academics; whether to keep it in the public repository is founder decision #3 |
| 9 | Publication manuscript package | `publications/` — Manuscript 1 (separability), 2 (border-convention technical note), 3 (adaptation & uncertainty scaffold); submission is founder decision #23 |
| 10 | Investor presentation (+ research and pilot decks, one-page overview, founder intro template) | `investor/OsteoQuant_Investor_Deck.pptx`, `..._Research_Collaboration_Deck.pptx`, `..._Commercial_Pilot_Deck.pptx` (rebuild with `python3 investor/build_decks.py`; every figure read from repository files), `investor/ONE_PAGE_OVERVIEW.md`, `investor/FUNDING_STRATEGY.md`; screenshots `investor/screenshots/`. Founder approval needed before external use (decision #8) |
| 11 | Reproducible product demonstration | `founder/DEMO_SCRIPT.md`, `scripts/demo_seed.py`, `scripts/screenshot_demo.js`. Sample reports in `reports_samples/` — **current** (regenerated at commit `14141db` under advisor 1.4.3, from committed code only; default `advisor_threshold` segmentation; watermarked "SAMPLE - SYNTHETIC DATA - NOT FOR STUDY DECISIONS"; regenerate with `python3 scripts/make_gen2_sample_reports.py`, which refuses to run when `osteoquant/` has uncommitted changes): `DefectFill_SAMPLE4_gen2_synthetic_betatcp.*` (β-TCP, week 4: graft and new-bone endpoints refused in 6/6; total mineral reported in 5/6) and `DefectFill_SAMPLE5_gen2_synthetic_ha.*` (HA, week 8: residual graft reported but flagged "(f)" in 6/6 because the automatic ROI is not yet accepted / QC verdict "review"; new bone refused in 6/6; total mineral reported in 3/6). **Superseded** (Gen-1, before every cycle-1 fix; no support table, "16 phantoms", "Study director" role): `reports_samples/superseded/DefectFill_SAMPLE1/2/3_*` (moved there on 28 Nov with a README) and `reports_samples/fig/` — do not show them to prospects |
| 12 | Prioritised remaining-work checklist | `REMAINING_WORK.md` |
| 13 | Founder summary and decisions | `FOUNDER_EXECUTIVE_SUMMARY.md` (start here), `FOUNDER_DECISIONS.md` (25 open decisions), `RELEASE_READINESS.md`, `BLOCKERS.md` |

Also: `EXPERIMENT_REGISTRY.md` (every experiment and its status), `BENCHMARK_SCORECARD.md`, `SCIENTIFIC_EVIDENCE.md`,
`DECISIONS.md`, `docs/user/` (user documentation), `docs/qa/test_summary.json` (test counts and coverage, single
source), `docs/quality/` (URS/FS/risk/IQ/OQ/PQ/SOPs/traceability, all DRAFT and not executed), `docs/security/`
(reviews, response, SBOM of the 27 Nov build, IP provenance), `docs/ip/` (IP strategy and invention register,
preliminary, not legal advice), and the website draft `website/` (unpublished). The Generation-1 landing page
`web/landing/` is superseded by `website/`. The only packaged desktop build (`packaging/dist/`, Linux, 28 Nov 2026,
commit `cf6fea7`, advisor 1.4.3) passed its packaged self-test and licence check; it is not distributed (B-016).
