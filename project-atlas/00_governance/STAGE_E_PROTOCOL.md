# Stage E Protocol — Finalist Playbooks

Read first: `MANDATE_AND_FOUNDER_BRIEF.md`, `EVIDENCE_STANDARDS.md`, `SCORING_FRAMEWORK.md`, the finalist's Stage A
record, Stage C memo (`04_industry_investigations/<ID>.md`), Stage D deep dive (`05_deep_dives/<ID>_deep_dive.md`),
its supplier/prospect CSVs (`09_databases/suppliers|prospects/`), its model (`08_financial_models/<ID>_*`), and any
review notes in `07_review/`. Fill gaps with new research; correct earlier errors explicitly ("Correction: …").

## Deliverable 1 — `06_playbooks/<ID>_playbook.md` (standalone; 5,000–9,000 words; no boilerplate)
Tailor every section to this business. Cite evidence inline as [level, source_id].
1. **Business explanation** — what it does, sells, who buys, why they pay, how it earns, why attractive; a
   plain-language explanation for someone new to the industry.
2. **Commercial entry** — initial niche, target customer, geography, named suppliers, named prospects (top 15 with
   rationale; full list in CSV), named competitors, positioning, pricing, sales strategy, acquisition strategy.
3. **Transaction economics** — ≥3 representative transactions, line by line; contribution; cash timing; failure
   risks; repeat potential.
4. **Validation** — minimum viable commercial offering; low-cost demand tests; supplier qualification steps;
   customer interview plan; budget; testable assumptions; success / failure criteria; conditions to invest more;
   conditions to abandon or pivot. Order experiments by information value per dollar.
5. **Operations** — full lead-to-cash workflow; human vs AI-assisted vs automatable vs professional-dependent vs
   not-automatable (classify each function); suppliers; fulfillment; support; QA; exceptions; software stack with
   prices; legal requirements; financial administration; post-Dec-2026 AI cost and fallback.
6. **Growth** — first 10 customers, first 100, hiring sequence (milestone that justifies each hire, cost,
   productivity), capacity limits, geographic expansion, adjacent products/services, vertical integration (with
   incremental return logic), management delegation (when a manager can run day-to-day), reinvestment slots.
7. **Financial analysis** — from the model: launch capital, working capital, 24-month monthly view, 5-year annual,
   breakeven, conservative/base/optimistic, sensitivity (top drivers), stress tests, profit milestones, capital
   accumulation to year 10, owner distributions, downside cases. Quote model outputs exactly; explain drivers.
8. **Capital deployment ladder** — what each of $0–500, $500–2k, $2–5k, $5–10k, $10–25k, $25–50k, $50–100k buys;
   the evidence gate required before each step; what could cause the capital to be lost.
9. **Strategic wealth creation** — how it becomes a durable cash asset; how much capital it could generate; when
   management could take over; whether it can fund other ventures; why it is / is not a strong first company for a
   diversified portfolio.
10. **Execution plan** — first 7 days, first 30 days (what founder does, what Claude prepares, named organizations
   to approach, questions to ask, evidence required, proposed spend, conditions to accept a first order / abandon),
   first 90 days, first year (milestones, slow-growth and failure branches).
11. **Pre-mortem** — lost $5k / $25k / $50k; revenue-but-no-profit; exhausting low-paid job; cash crunch; can't run
   without founder; no deployable surplus. Early warning indicators and cheap preventive tests.
12. **Required confirmations** — supplier, customer, regulatory, insurance facts that must be confirmed directly.

## Deliverable 2 — `06_playbooks/<ID>_materials.md`
Draft (never send) materials tailored to this business: supplier/partner inquiry template, customer discovery
interview questionnaire (non-leading, aimed at past behavior and spend), 3 outreach message variants (email,
call opener, in-person), sales call script with qualification questions, RFQ/quote template, one-page offer
sheet text, pricing calculator spec (inputs/outputs), order-intake/onboarding checklist, weekly KPI sheet spec.
Mark everything "DRAFT — not sent; requires founder review".

## Deliverable 3 — refreshed model
Update `08_financial_models/<ID>_assumptions.json` with any corrected drivers (keep `__evidence`/`__source`), rebuild
with `python3 tools/build_fin_model.py <path>`, and run `python3 tools/verify_fin_model.py 08_financial_models/<ID>_model.xlsx`.
Stage update line → `03_screening/stage_updates/stageE_<batch>.jsonl` (`"stage":"E"`). New sources →
`06_playbooks/sources_<batch>.jsonl` (IDs `E<batch>-S###`).

Rules: read-only research; nothing sent; never fabricate. Final reply ≤200 words.

## Standardization rules for refreshed models (added at launch — required for cross-finalist comparability)
- Owner draw: `founder_draw_per_month` = 4000 and `founder_draw_start_month` = 13 in all three scenarios (a modest
  living stipend; the comparison tool also reports peak funding with no draw). If the business cannot support it,
  keep it anyway — the resulting funding need is the honest answer.
- `tax_rate_pct` = 0.30 in all scenarios. `start_capital_injection` = the smallest amount that keeps the base-case
  cash balance ≥ 0 (state it).
- Long-term drivers (`lt_growth_y6_pct`, `lt_growth_decay`, `incremental_roic_pct`, `maint_capex_pct_op`,
  `reserve_months`, `ev_multiple`) must be set with stated evidence (e.g., small-service-business SDE/EBITDA multiples,
  agency book multiples) and `__evidence`/`__source` keys; conservative must be genuinely conservative.
- Do NOT run `verify_fin_model.py` (LibreOffice cannot run concurrently across agents); verification is central.
- Helper scripts in `/tmp/claude-0/atlas_scratch/E_<ID>/`. Web search ≈10 per agent; fetch primary sources directly.
