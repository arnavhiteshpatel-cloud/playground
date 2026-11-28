# Research Agent Protocol (Stage A — Broad Discovery)

Workspace root: `/home/user/playground/project-atlas` (call it `$ATLAS`).
Read first: `00_governance/MANDATE_AND_FOUNDER_BRIEF.md`, `00_governance/EVIDENCE_STANDARDS.md`,
`00_governance/SCORING_FRAMEWORK.md`, and your workstream definition in `01_taxonomy/WORKSTREAMS.md`.

## Your outputs (write incrementally — append records as you finish them so work survives interruption)
1. `$ATLAS/02_discovery/<wsid>_opportunities.jsonl` — one JSON object per line (schema below).
2. `$ATLAS/02_discovery/<wsid>_sources.jsonl` — one source record per line (schema in EVIDENCE_STANDARDS.md).
3. `$ATLAS/02_discovery/<wsid>_summary.md` — ≤ 1,200 words: landscape of your workstream, the 5–8 strongest
   candidates and why, surprises, things that looked good but fail, evidence gaps, adjacent ideas for other streams.
4. Validate before finishing: `python3 $ATLAS/tools/validate_discovery.py <wsid>` and fix every error.

Use Python (`json.dumps`) or careful hand-written JSON — every line must parse. Use `ensure_ascii=False` is fine.

## How to research
- Use web search and web fetch (if WebSearch isn't loaded, load it with ToolSearch `select:WebSearch`).
- Prefer primary sources: statutes/agency sites (e.g., idfpr.illinois.gov, insurance.illinois.gov, fmcsa.dot.gov,
  sba.gov, sam.gov/usaspending.gov), Census (SUSB, Economic Census, CBP), BLS, public filings (10-K), FDD Item 19
  (via state FDD databases where public), official supplier/partner program pages, trade associations.
  Industry blogs and "best business ideas" lists are D-level at best — use only as leads.
- Budget roughly 40–90 searches/fetches. Spend most evidence effort on the ~12 most promising records; lighter
  records are fine if honestly labeled (evidence E) with `unanswered_questions` filled in.
- **Do not contact anyone, fill forms, create accounts, request quotes, or submit anything.** Read-only research.
- Don't bypass paywalls/logins. If a key source is inaccessible, note it in `limitations` of the summary.

## Distinctness
Each record must be a meaningfully distinct commercial mechanism, customer segment, product category, supply
chain, service model, or operating strategy. No padding with trivial variants (e.g., "cleaning offices" vs
"cleaning dental offices" only counts twice if economics/acquisition genuinely differ — say why).
Stay inside your workstream boundary; if you find a great idea outside it, list it in your summary under
"Cross-stream leads" rather than recording it.

## Opportunity record schema (all keys required; use null / "MISSING" when unknown — never invent)
```json
{
 "id": "WS03-001",
 "title": "Short descriptive name",
 "workstream": "WS03",
 "industry": "...", "subindustry": "...", "naics": "6-digit code or null",
 "mechanisms": ["brokerage_commission", "..."],
 "product_service": "Exactly what is sold",
 "target_customer": "Who buys (role + org type + size)",
 "purchase_motivation": "Why they pay (mandate, downtime cost, revenue, compliance...)",
 "spending_evidence": "Evidence buyers already spend on this (with [level, source_id])",
 "representative_operators": ["Company — note (size/revenue if known) [level, source]"],
 "revenue_mechanism": "How money is earned (price × volume, % commission, retainer...)",
 "typical_transaction_value": "e.g. '$1,200 per inspection; 2x/yr per site' [level]",
 "gross_margin_pct_low": 30, "gross_margin_pct_high": 45,
 "direct_costs": "Main direct costs",
 "contribution_profit_note": "Per-transaction or per-customer contribution after direct costs [level]",
 "validation_cost_usd": 500,
 "launch_capital_usd_low": 2000, "launch_capital_usd_high": 15000,
 "working_capital_note": "Payment timing, inventory, receivables, deposits",
 "time_to_first_revenue_months": 2,
 "time_to_profitability_months": 6,
 "sales_cycle": "...",
 "repeat_purchase": "none | occasional | recurring-contract | consumable-replenishment | ... + detail",
 "acquisition_channels": ["..."],
 "customer_accessibility": "...",
 "supplier_accessibility": "Confirmed / assumed / unknown + detail",
 "competitive_intensity": "low | moderate | high | extreme + detail",
 "entry_strategy": "Why a customer would choose a new company — specific wedge",
 "licenses": "Required licenses/registrations/bonds/insurance (Illinois + federal) [level, source]",
 "regulatory_barriers": "...",
 "operational_risks": "...", "financial_risks": "...",
 "geographic_constraints": "...",
 "founder_expertise": "What the founder must learn/acquire",
 "staffing": "Who must be hired and when",
 "automation_potential": "Specific tasks AI/software materially improves (and what stays human)",
 "delegation_potential": "...",
 "scalability": "...", "expansion": "Adjacencies / vertical integration paths",
 "yr3_operating_profit_usd_low": 60000, "yr3_operating_profit_usd_high": 250000,
 "plausible_milestone_ceiling": "Highest founder milestone plausible for a capable new entrant within ~5 yrs: '$10k/mo' | '$25k/mo' | '$250k/yr' | '$500k/yr' | '$1M/yr' | '$1M+/yr'",
 "roic_note": "...",
 "evidence_confidence": "A|B|C|D|E",
 "source_ids": ["WS03-S001"],
 "critical_assumptions": ["..."],
 "unanswered_questions": ["..."],
 "failure_modes": ["Why comparable businesses fail"],
 "scores": {"fcf":5,"roic":5,"access":5,"scale":5,"resilience":5,"entry":5,"delegation":5,"cash":5,"feasibility":5,"ai":5},
 "score_rationale": "One or two sentences per notable score",
 "gates": ["G7_FOUNDER_DEPENDENT:WARN"],
 "preliminary_verdict": "advance | hold | reject — one-sentence reason"
}
```
Controlled vocabulary for `mechanisms` (add new ones if needed, snake_case): buy_resell, wholesale_distribution,
authorized_reseller, manufacturer_rep, brokerage_commission, referral_fee, lead_generation, origination,
manufacturing, private_label, contract_manufacturing_broker, outsourced_service, recurring_service_contract,
inspection_testing, rental, leasing, subscription_replenishment, licensing, publishing, information_product,
training_certification, installation, repair_maintenance, refurbishment, supplier_aggregation,
customer_aggregation, inventory_availability, geographic_density, international_sourcing, procurement,
financing_own_capital, contingency_recovery, waste_to_value, compliance_workflow, information_asymmetry,
time_sensitive_fulfillment, marketplace_seller, route_business, staffing_placement, consulting, managed_service,
franchise, government_contracting, auction_liquidation, consignment.

## Score calibration reminder
Score for THIS founder starting from zero. Most records should have several scores in the 3–6 range. Reserve 8+
for criteria with evidence. Year-3 profit ranges must be for a capable new entrant, not the median incumbent.

## Final message to the orchestrator
Return ≤ 200 words: number of records, number of sources, your top 5 IDs with one line each, and the biggest
evidence gaps. Do not paste the records.
