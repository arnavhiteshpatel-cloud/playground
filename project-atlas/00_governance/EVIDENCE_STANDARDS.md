# Evidence Standards

## Evidence hierarchy (apply to every consequential claim)
| Level | Meaning | Examples |
|---|---|---|
| **A** | Direct commercial evidence | Verified completed transactions; audited financials (10-K); official procurement awards (USASpending, state award notices); official regulatory records (statutes, agency rules, license fee schedules) |
| **B** | Strong commercial documentation | Official supplier price lists; published partner/commission schedules; official product catalogs; documented purchasing requirements (RFPs); credible company financial disclosures (S-1, investor decks of public cos, FDD Item 19) |
| **C** | Supporting industry evidence | Credible industry surveys (trade associations, IBISWorld/RMA summaries if public), trade publications, government statistics (Census SUSB/Economic Census, BLS), well-supported market research |
| **D** | Indirect evidence / proxies | Reviews, forum anecdotes, job postings, traffic data, marketplace listing counts, "how much do X make" blog posts, BizBuySell asking prices/listed cash flow |
| **E** | Assumptions / hypotheses | Analyst (our) estimates, unverified conversion rates, hypothetical pricing, modeled profitability, assumed customer interest |

Rules:
- Never present D or E as verified fact. Label the level inline: e.g. "gross margin 35–45% [C, WS03-S014]".
- An opportunity's overall `evidence_confidence` = the level supporting its **economics** (margin, ticket size,
  profit potential), not its best-supported trivia.
- Business-for-sale listings (BizBuySell etc.) show *asking* prices and seller-claimed cash flow = **D**. Useful as
  proxies for small-operator earnings, never as fact.
- FDD Item 19 financial performance representations = **B** (franchisor-disclosed, often median/mean of units).
- Public-company margins describe mature incumbents. Mark them as "incumbent economics" and estimate new-entrant
  economics separately (usually lower margin, higher CAC, no scale purchasing).
- Where sources disagree, keep both numbers and note the discrepancy. Never silently pick the attractive one.
- Prices, commissions, regulations and programs are time-sensitive: record publication date and access date.
- Quote at most ~25 words of any source; otherwise paraphrase.

## Source record (JSONL, one per line)
```json
{"source_id":"WS03-S001","url":"https://...","organization":"...","title":"...","publication_date":"2025-06 or null",
 "access_date":"2026-11-28","claim":"what this source supports","evidence_level":"A|B|C|D|E",
 "excerpt":"<=25-word quote or paraphrase","limitations":"...","opportunity_ids":["WS03-004"]}
```

## Analytical failure checklist (check before finalizing any record)
Do not confuse: revenue/profit; gross profit/FCF; asking prices/completed transactions; advertised/realized
commissions; market size/obtainable demand; supplier existence/supplier accessibility; customer
identification/customer interest; interest/sales; traffic/revenue; popularity/quality; public-co
profitability/new-entrant profitability; tech capability/commercial demand; AI automation/zero human labor;
low startup cost/low overall risk; historical/guaranteed future.

## Prohibited
Fabricated numbers, fabricated quotes, fabricated customer interest, fabricated sources or URLs. If a fact cannot
be found, write null or "MISSING" and list it under `unanswered_questions`.
