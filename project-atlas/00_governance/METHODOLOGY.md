# Research Methodology

## Design principles
1. **Breadth before depth, evidence before enthusiasm.** No sector is favored at the start. Research effort is
   allocated progressively to opportunities that earn it through evidence.
2. **Founder-specific scoring.** Every opportunity is judged as THIS founder would execute it: Illinois, from
   scratch, no licenses, ≤$100k conditional capital (not a budget), heavy AI access only until 2026-12-05.
3. **Owner cash is the objective function.** Free cash flow, ROIC, cash conversion and delegability dominate;
   revenue and TAM are secondary.
4. **Shrink weak evidence.** Composite scores are pulled toward the mean in proportion to evidence weakness
   (see SCORING_FRAMEWORK.md) so speculative ideas cannot outrank well-evidenced ones on modeled potential alone.
5. **Independence.** Discovery agents work in separate workstreams; a blind re-scoring pass (scores hidden)
   corrects cross-agent calibration drift; adversarial reviewers who did not write a playbook challenge it.
6. **Everything persists.** All outputs are files (JSONL for machines, Markdown for humans, XLSX for models), so
   work survives context resets. See README.md "How to resume".

## Funnel (targets are allocations, not quotas)
| Stage | Target | Method | Output location |
|---|---|---|---|
| A — Broad discovery | 300–500 distinct opportunities | 18 parallel workstream agents with web research | `02_discovery/` |
| B — Structured screening | ~100–150 | Merge/dedupe → gates → composite + blind re-score → document rejections | `03_screening/` |
| C — Industry investigations | ~50–75 | Industry/mechanism/competition memos, operator economics, failure research | `04_industry_investigations/` |
| D — Commercial deep dives | ~25–35 | Named operators, suppliers, prospects, transaction examples, regulation, prelim model | `05_deep_dives/` |
| E — Finalist playbooks | ~10–15 | Standalone playbooks + driver-based financial workbooks | `06_playbooks/`, `08_financial_models/` |
| F — Adversarial review | all finalists | Independent reviewers: facts, sources, math, CAC, suppliers, legality, pre-mortem | `07_review/` |
| G — Refined shortlist | ~5 | Comparative analysis, sensitivity of rankings to weights | `10_deliverables/` |
| H — Recommendation | 1 primary + 2 alternatives | Executive decision memo + handoff | `10_deliverables/` |

## Workstreams
Discovery: WS01–WS18 (see `01_taxonomy/WORKSTREAMS.md`). Cross-cutting teams are run as later-stage agents:
supplier & partner discovery, customer acquisition research, financial modeling, regulatory research,
competitive intelligence, AI operational leverage, capital allocation & wealth compounding, adversarial review,
final synthesis.

## Screening logic (Stage B)
1. Validate and merge all discovery records into `09_databases/opportunities.jsonl` (canonical IDs preserved).
2. Detect near-duplicates across workstreams; keep the better-evidenced record, link the other as `duplicate_of`.
3. Apply gates (G1–G7). FAIL gates are excluded from advancement unless overridden in DECISION_LOG.md.
4. Blind re-score: independent agents re-score every record from its descriptive fields with original scores
   hidden. Final Stage-B criterion score = mean of original and blind scores; disagreements >2 points flagged.
5. Composite = weighted score; evidence-adjusted composite = shrinkage by evidence level.
6. Advance by evidence-adjusted composite, plus a diversity floor (no more than ~25% of Stage C from one
   workstream) and a "wildcard" allowance for high-upside, low-evidence ideas whose key unknowns are cheap to
   resolve. Every non-advanced record keeps a recorded reason.

## Financial modeling standard
Driver-based (customers/transactions/reps/capacity → revenue), monthly for 24 months, annual to year 5, capital
accumulation to year 10; conservative/base/optimistic; explicit editable assumptions; formulas preserved in XLSX;
revenue → gross profit → contribution → operating profit → taxes → capex → working capital → FCF → owner comp →
distributions/retained earnings; maximum cumulative cash deficit; sensitivity tables; stress tests.

## Known structural limitations of desk research
- No direct supplier/customer contact is authorized, so supplier accessibility and customer interest can only be
  "documented" (published programs, published criteria) or "assumed" — never "confirmed".
- Private-company financials are mostly unavailable; small-operator economics rely on FDD Item 19, public comps,
  Census aggregates, and business-for-sale listings (D-level).
- Some sources (paywalled market research, SEC EDGAR bulk access without a contact UA) may be inaccessible.
All limitations are logged in `RESEARCH_LIMITATIONS.md`.
