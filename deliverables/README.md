# Deliverables Index (directive §42)

> **Superseded (2026-11-27):** the PDF report, workbook and decks listed below were built in Generation 1 and contain
> outdated pricing, financial outputs (incl. a GLP study offer) and pre-advisor results. They are rebuilt in the
> Generation-2 final-deliverables phase; until then use `FORENSIC_AUDIT.md`, `EXPERIMENT_REGISTRY.md`,
> `business/REVENUE_MODEL.md` and `investor/FUNDING_STRATEGY.md` as the current sources.

| # | Deliverable | Location |
|---|---|---|
| 1 | Technical & commercial report (PDF, cited) | `deliverables/OsteoQuant_Technical_and_Commercial_Report.pdf` (built by `scripts/build_final_report.py`) |
| 2 | Spreadsheet: datasets, experiments, benchmarks, competitors, costs, funding, prospects | `deliverables/OsteoQuant_Master_Workbook.xlsx` (built by `scripts/build_master_spreadsheet.py`); financial model `business/FINANCIAL_MODEL.xlsx` |
| 3 | Founder operating manual | `founder/OPERATING_MANUAL.md` |
| 4 | Scientific learning curriculum | `founder/LEARNING_CURRICULUM.md` |
| 5 | Physical phantom experiment package | `validation/` — protocol, BOM, Beckman access, decisions for imaging scientist, printable worksheets, label CSVs |
| 6 | Grant application preparation package | `grants/` — opportunities (27), NSF vs NIH eligibility, Specific Aims, NSF Project Pitch, Cozad package, budget, letters, checklist |
| 7 | Customer discovery package | `business/` — 103 prospects, interview guide + coding scheme + log template, pricing experiment, SOW/pilot/quote/DPA/QA templates, market inputs |
| 8 | Collaborator outreach package | `outreach/` — collaborators (verified), draft emails (unsent), OTM/IP questions |
| 9 | Publication manuscript package | `publications/` — Manuscript 1 (separability), 2 (border-convention technical note), 3 (adaptation & uncertainty scaffold) |
| 10 | Investor presentation (+ research & pilot decks, one-page overview, founder intro template) | `investor/OsteoQuant_Investor_Deck.pptx`, `..._Research_Collaboration_Deck.pptx`, `..._Commercial_Pilot_Deck.pptx`; screenshots `investor/screenshots/` |
| 11 | Reproducible product demonstration | `founder/DEMO_SCRIPT.md`, `scripts/demo_seed.py`, `scripts/screenshot_demo.js`; sample reports `reports_samples/`: **current** (desktop report code, advisor 1.4.2, default `advisor_threshold` segmentation; regenerate with `python3 scripts/make_gen2_sample_reports.py`): `DefectFill_SAMPLE4_gen2_synthetic_betatcp.*` (β-TCP, week 4: graft and new-bone endpoints refused with reasons; total mineral reported) and `DefectFill_SAMPLE5_gen2_synthetic_ha.*` (HA, week 8: residual graft supported in 6/6, new bone refused, total mineral refused in 3/6 by the ambiguous-rim rule). **Superseded** (Gen-1, before every cycle-1 fix; no support table, "16 phantoms", "Study director" role): `DefectFill_SAMPLE1/2/3_*` and `reports_samples/fig/` — do not show them to prospects |
| 12 | Prioritised remaining-work checklist | `REMAINING_WORK.md` |

Also: `FOUNDER_HANDOFF.md` (start here), `EXPERIMENT_REGISTRY.md`, `SCIENTIFIC_EVIDENCE.md`, `DECISIONS.md`,
`BLOCKERS.md`, `docs/quality/` (URS/FS/risk/IQ/OQ/PQ/SOPs/traceability), `docs/security/` (reviews, response, SBOM, IP
provenance), landing page `web/landing/index.html`.
