# Stage C Protocol — Industry & Mechanism Investigations

Read first: `MANDATE_AND_FOUNDER_BRIEF.md`, `EVIDENCE_STANDARDS.md`, `SCORING_FRAMEWORK.md` (all in `00_governance/`).
Each assigned opportunity's Stage A record is in `09_databases/opportunities.jsonl` (look up by `id`); its sources
are in `09_databases/sources.jsonl`. Treat the Stage A record as a hypothesis to test, not a conclusion.

## For each assigned opportunity, investigate and write `04_industry_investigations/<ID>.md` (900–1,600 words)
1. **Verdict box (top):** advance to Stage D / hold / drop · revised evidence level · one-paragraph reason.
2. **Industry structure:** size from official/credible data (Census Economic Census/SUSB/CBP, BLS, trade
   association), firm counts and size distribution (fragmentation), growth, cyclicality, Illinois concentration.
3. **Value chain & mechanism:** who pays whom, where margin is captured, what the new entrant actually does.
4. **Operator economics:** ≥3 real operators with any disclosed numbers (10-K, FDD Item 19, acquisition
   announcements, credible interviews, business-for-sale listings labeled D). Separate incumbent economics from
   realistic new-entrant economics. State gross margin, operating margin, revenue/employee where findable.
5. **Small-start evidence:** any documented case of an operator that started small and grew (name, source).
6. **Competition:** national players, regional/local players near Illinois, PE roll-ups, platforms; their
   weaknesses; switching costs; what customers complain about (reviews = D).
7. **Customer purchasing behavior:** decision-maker, purchase frequency, typical spend, procurement process,
   contract terms, how they find vendors today.
8. **Failure evidence:** why businesses in this niche fail (bankruptcies, enforcement actions, closures,
   margin compression). Cite.
9. **Regulation (Illinois + federal), precise:** license names, issuing agency, fees, exams, bonds, insurance,
   time to obtain; whether a licensed employee/partner can satisfy it. Primary sources.
10. **Entry wedge test:** the specific reason a buyer would switch to a new firm, how it is delivered, what it
   costs; is it copyable?
11. **Economics sanity check:** recompute year-3 operating-profit range for a capable new entrant from drivers
   (customers × spend × margin − staff − overhead). Show the arithmetic.
12. **Revised scores** (all 10 criteria) with one-line justification for any change ≥2 from Stage A.

## Machine-readable outputs
- Append one line per opportunity to `03_screening/stage_updates/stageC_<batch>.jsonl`:
```json
{"id":"WS05-004","stage":"C","scores":{"fcf":..,"roic":..,"access":..,"scale":..,"resilience":..,"entry":..,"delegation":..,"cash":..,"feasibility":..,"ai":..},
 "evidence_confidence":"C","yr3_operating_profit_usd_low":..,"yr3_operating_profit_usd_high":..,"launch_capital_usd_low":..,
 "launch_capital_usd_high":..,"validation_cost_usd":..,"plausible_milestone_ceiling":"$500k/yr",
 "verdict":"advance|hold|drop — reason","note":"<=40 words on what changed"}
```
- New sources → `04_industry_investigations/sources_<batch>.jsonl` (schema in EVIDENCE_STANDARDS.md; IDs
  `C<batch>-S###`, `opportunity_ids` filled).
- Validate JSONL lines parse before finishing.

## Rules
Read-only research. No contact, forms, accounts, quotes, spending. Never fabricate; unknown = "MISSING".
Do not anchor on the Stage A author's enthusiasm; actively look for disconfirming evidence.
Final reply ≤200 words: per opportunity one line (ID, verdict, revised adj. view, the single most important fact).
