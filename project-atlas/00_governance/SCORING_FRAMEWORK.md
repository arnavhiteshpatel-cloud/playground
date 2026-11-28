# Scoring Framework (v1.0 — provisional weights from founder; revisions logged in DECISION_LOG.md)

Score every opportunity **as it would be executed by THIS founder** (Illinois, no licenses, tech/research
background, ≤$100k conditional capital, willing to sell and work hard, starting from zero, no acquisition) —
not as an abstract industry. Integer scores 1–10. 5 = mediocre/typical small business. Be harsh: most
opportunities should land 3–6 on most criteria. A 9–10 needs evidence.

| Key | Criterion | Weight |
|---|---|---|
| `fcf` | Sustainable free cash flow & owner wealth creation | 18% |
| `roic` | Return on invested capital & capital efficiency | 15% |
| `access` | Customer accessibility & acquisition feasibility (for an unknown new entrant) | 12% |
| `scale` | Scalability & reinvestment runway | 12% |
| `resilience` | Durable demand & business resilience (recession, tech change, regulation) | 10% |
| `entry` | Competitive entry & developing defensibility | 10% |
| `delegation` | Ability to delegate operations/management | 8% |
| `cash` | Cash conversion & working capital | 5% |
| `feasibility` | Regulatory & practical feasibility for this founder | 5% |
| `ai` | AI-enabled operational efficiency (real, durable, affordable post-Dec-2026) | 5% |

## Anchors
**fcf** — realistic year-3 to year-5 annual owner FCF (after market-rate pay for non-founder staff, before founder
salary) for a capable new entrant in base case:
1 = <$25k · 3 = ~$50–75k · 5 = ~$100–150k · 7 = ~$250–400k · 9 = ~$750k+ · 10 = $1M+ with multiple comparable
small-start operators documented.

**roic** — annual operating profit ÷ total capital the owner must put at risk to get there:
1 = <10% · 3 = ~25% · 5 = ~75% · 7 = ~200% · 9 = >500% (asset-light, customer-funded) · 10 = near-infinite and proven.

**access** — can a newcomer reach and win paying buyers?
1 = buyers unreachable/locked in long contracts, needs years of track record · 3 = long cycles, credibility walls,
heavy RFP/qualification · 5 = reachable through standard B2B outreach, moderate cycle (1–3 mo) · 7 = many buyers
with frequent need, identifiable via public data, short cycle, referrals common · 9–10 = buyers actively searching
for providers and switching is easy and frequent.

**scale** — can retained earnings be redeployed at good returns for years?
1 = capped at owner's hours · 3 = local niche, ceiling ~$1–2M revenue · 5 = regional expansion, moderate ceiling ·
7 = multi-region / multi-line, many reinvestment slots · 9–10 = large runway, repeatable units, adjacencies.

**resilience** — 1 = fad, discretionary, single-platform-dependent, or highly cyclical with recession collapse ·
5 = typical B2B demand, moderately cyclical · 8 = mandated/essential recurring demand (code-required, consumable,
regulatory) · 10 = counter-cyclical or mandated and growing.

**entry** — 1 = commodity with entrenched scale players and no wedge · 3 = crowded, weak wedge · 5 = credible wedge
(service, speed, niche focus) but easily copied · 7 = clear wedge plus accumulating moat (contracts, density,
relationships, certification) · 9–10 = structural opening (incumbents exiting, new mandate, underserved segment)
plus compounding defensibility.

**delegation** — 1 = requires founder's license/personality forever · 5 = delegable with 2–3 yrs of systemization ·
8 = standard roles with established labor market, SOP-friendly · 10 = already commonly run by managers/absentee owners.

**cash** — 1 = large inventory, 60–120-day receivables, long negative cash cycle · 5 = typical net-30 B2B ·
8 = paid at/before service, low inventory · 10 = customer prepays/deposits, negative cash conversion cycle.

**feasibility** — 1 = requires license/credential the founder cannot obtain in ~12 months (attorney, CPA, MD, PE)
or heavy enforcement risk · 4 = license obtainable in 3–12 months or needs licensed partner · 7 = light
registration/bond/insurance · 10 = no special requirements.

**ai** — 1 = AI irrelevant · 5 = meaningful back-office savings (quotes, admin, prospecting) · 8 = AI materially
lowers unit cost vs. incumbents in a durable way at ordinary API prices · 10 = AI enables a cost structure
incumbents cannot match and remains cheap post-Dec-2026. Never let `ai` compensate for weak economics.

## Gates (flags — recorded in `gates`; any FAIL removes from the shortlist unless explicitly overridden in DECISION_LOG)
- `G1_CAPITAL` FAIL if >$100k must be at risk before first revenue.
- `G2_LICENSE` FAIL if it requires a credential the founder cannot obtain within ~12 months and cannot legally
  work around with a licensed partner/employee.
- `G3_LEGAL_ETHICS` FAIL if structurally predatory, deceptive, or high enforcement risk (e.g., MCA stacking,
  debt-settlement upfront fees, lead-selling that violates TCPA, unlicensed practice).
- `G4_CEILING` WARN if no credible path to ≥$100k/yr operating profit.
- `G5_VENTURE` WARN if success fundamentally requires venture-scale technology or funding.
- `G6_ACQUISITION` FAIL if the only realistic entry is buying an existing business.
- `G7_FOUNDER_DEPENDENT` WARN if structurally capped at the founder's personal hours.

## Composite scores (computed by `tools/score.py`)
- `raw_score` = Σ weight × score (1–10 scale).
- `evidence_adjusted_score` = 5 + (raw_score − 5) × k, shrinking toward the prior mean when evidence is weak:
  k = 1.00 (A), 0.95 (B), 0.85 (C), 0.70 (D), 0.55 (E).
  Rationale: a weakly evidenced 8 should not outrank a strongly evidenced 7.
- Alternative rankings re-weight the same criterion scores (see `tools/score.py` RANKING_PROFILES).
- Original (v1.0) and revised scores are both retained in every dataset.

## Anti-gaming rules (from the founder)
- A large hypothetical market cannot compensate for inaccessible customers.
- Automation potential cannot compensate for weak commercial economics.
- High advertised margins cannot compensate for extreme financial or regulatory risk.
- Rankings are inputs to judgment, not the decision. Final choices are argued in prose with evidence.
