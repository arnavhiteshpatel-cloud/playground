# Stage D Protocol — Commercial Deep Dives

Read first: `MANDATE_AND_FOUNDER_BRIEF.md`, `EVIDENCE_STANDARDS.md`, `SCORING_FRAMEWORK.md`,
`STAGE_C_PROTOCOL.md`, the opportunity's Stage A record (`09_databases/opportunities.jsonl`) and its Stage C memo
(`04_industry_investigations/<ID>.md`). Also read `tools/fin_engine.py` DRIVERS list (model driver definitions)
and `08_financial_models/TEMPLATE_assumptions.json` (format only — its numbers are placeholders).

Goal: turn the opportunity into something the founder could act on next week, using named, real organizations.

## Deliverable 1 — `05_deep_dives/<ID>_deep_dive.md` (2,000–3,500 words)
1. **Specific initial niche** (customer type × product/service × geography — e.g., "X for Y in Cook/DuPage").
2. **Named operators** (≥6): national, regional, Illinois-local; what is known (size, pricing, reviews, years).
3. **Named suppliers / partners** (≥5 where the model needs them): program pages, stated qualification criteria,
   published pricing/commissions/terms, MOQs, credit terms, geographic limits; mark each "documented" vs
   "assumed — requires direct confirmation".
4. **Named prospective customers**: ≥25 real Illinois organizations matching the initial niche, from lawful
   public sources (directories, licensing lists, association member lists, permit data, Google Maps-type
   listings, public procurement records). These are *prospects*, not leads. Record in the CSV below.
5. **Representative transactions** (≥3): line-item revenue and direct costs with evidence levels and sources;
   contribution per transaction; payment timing.
6. **Customer acquisition:** how to get customer #1, #2–10, #11–100; channels; funnel estimates (lead→meeting→
   proposal→win) with evidence levels; CAC, payback, LTV; human sales work required each week.
7. **Pricing strategy** with evidence of market prices (published rate cards, public bids/awards, competitor
   pages).
8. **Working capital & cash conversion cycle** at 10, 50, 200 customers.
9. **Regulatory path:** exact steps, agencies, fees, timing; insurance types and indicative premiums (with source
   or marked E).
10. **Operations workflow** from lead to cash; what is human, AI-assisted, automatable; software stack (existing
   tools first, with prices).
11. **Competitive position & defensibility over time** (what accumulates: density, contracts, data, certifications).
12. **Key risks + pre-mortem** (how this fails at $5k, $25k, $50k lost; early warning indicators).
13. **Validation plan**: the 3–5 cheapest experiments that produce real commercial evidence (paid > verbal),
   with costs, success and kill criteria.
14. **Revised scores & verdict** (finalist / reserve / drop).

## Deliverable 2 — data files
- `09_databases/prospects/<ID>_prospects.csv` columns: organization, industry, city, county, website,
  public_phone_or_contact_page, characteristics, likely_need, decision_maker_role, acquisition_channel,
  qualification_rationale, evidence_source_url, status (always "prospect — not contacted").
  Use only business contact info published by the organization itself; no personal emails/phones of individuals.
- `09_databases/suppliers/<ID>_suppliers.csv` columns: organization, website, categories, program_or_page_url,
  geography, qualification_requirements, published_pricing_or_terms, restrictions, accessibility
  ("documented" | "assumed"), evidence_level, follow_up_questions.
- `08_financial_models/<ID>_assumptions.json` — driver values for conservative/base/optimistic, each consequential
  driver with `<key>__evidence` and `<key>__source`; staff, overhead (mark AI/software items `is_ai`), capex,
  ≥3 `transactions`. Build it with `python3 tools/build_fin_model.py 08_financial_models/<ID>_assumptions.json` and
  sanity-check the results JSON (do not tune drivers to hit a target — derive them from evidence).
- Stage update line → `03_screening/stage_updates/stageD_<batch>.jsonl` (same schema as Stage C, `"stage":"D"`).
- New sources → `05_deep_dives/sources_<batch>.jsonl` (IDs `D<batch>-S###`).

## Rules
Read-only research. No contact, forms, accounts, quotes, spending. Never fabricate organizations, prices, or
contacts; unknown = "MISSING". Distinguish prospects from leads from customers. Final reply ≤200 words.

## Practical notes (added at launch)
- **Prospect data sources that work from this environment** (Socrata APIs, no key needed for modest use):
  Chicago food inspections `https://data.cityofchicago.org/resource/4ijn-s7e5.json` (filter with `$where`, e.g.
  violations like '%pest%'), Chicago building permits `.../resource/ydr8-5enu.json`, Chicago business licenses
  `.../resource/r5kz-chrr.json`, FMCSA carrier census `https://data.transportation.gov/resource/az4n-8mr2.json`,
  USASpending `https://api.usaspending.gov`. Cook County and Illinois data portals may also work. Respect rate limits.
- **Privacy:** prospects are organizations. Record business names, business addresses, websites and business
  contact pages only. Do not record personal emails, personal cell numbers, or names of individuals (for sole
  proprietors trading under their own name, record the business/DBA name and a public business contact page only).
- **Models:** build with `python3 tools/build_fin_model.py 08_financial_models/<ID>_assumptions.json`. Do NOT run
  `verify_fin_model.py` (LibreOffice cannot run concurrently across agents); verification is run centrally.
- Helper scripts go in `/tmp/claude-0/atlas_scratch/<batch>/`.
