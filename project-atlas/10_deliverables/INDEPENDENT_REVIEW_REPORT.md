# Project Atlas — Independent Review Report

**Date:** 2026-11-28 · **Scope:** the 11 finalists challenged at Stage F: SYN-006, WS16-006, SYN-004, SYN-001, WS05-007, WS18-003, WS04-014, WS13-014, WS12-012, WS12-014, WS18-035.
**Compiled from:** `07_review/<ID>_review.md` (11 files), `07_review/CROSS_MODEL_AUDIT.md`, `07_review/sources_F1…F6.jsonl`, `03_screening/calibration.md`, `03_screening/screening_dispositions.csv`, `03_screening/scores.csv`, `03_screening/stage_updates/*.jsonl`, `09_databases/opportunities.jsonl` (stage history) and `tools/score.py` (composite formula). Nothing here is new research; figures are quoted from those files, and computed items (rank orders, counts) are flagged.

**In one paragraph.** Every finalist weakened under review. All 11 evidence-adjusted scores fell between Stage E and Stage F, and the year-3 base operating profit fell for all 11. Three finalists were judged to **fail** as a first company: WS16-006, WS12-012 and WS18-035. WS18-003 fails as a primary candidate. The other seven **survive with major revisions**, but only as cheap tests. Once the cross-model audit charges for the founder's own unpaid delivery labour, **no finalist reaches $100k/yr of harmonized year-5 operating profit**. The best are WS12-012 at $87k, WS12-014 at $84k, SYN-004 at $57k and WS04-014 at $55k (`CROSS_MODEL_AUDIT.md` §5).

---

## 1. How review worked

### 1.1 Stage B: blind re-scoring of all 630 Stage A records

- **Method.** A second scorer re-scored each record blind (`03_screening/blind_packets/` → `blind_scores/`).
- **Stage B composite.** For each criterion, the mean of the original and blind scores (`score_basis = "mean(original, blind)"`). It is weighted by the v1 weights and shrunk toward 5 by evidence level: adj = 5 + (raw − 5) × k, with k = A 1.0, B 0.95, C 0.85, D 0.70, E 0.55 (`tools/score.py`).
- **Calibration result** (`03_screening/calibration.md`):
  - Authors scored higher than blind reviewers on **every** criterion.
  - The largest gaps were AI leverage (mean 4.15 vs 3.41; mean |diff| 0.81), free cash flow (3.58 vs 2.90; 0.70) and ROIC (5.46 vs 5.02).
  - Gaps above 2 points were rare (≤1% per criterion): the bias was systematic, not erratic.
  - Inflation by workstream ran from +0.17 (WS12) to +0.70 (WS02). The single largest disagreement was WS08-021 at +1.72.
- **Limitation.** The three bundles (SYN-001, SYN-004, SYN-006) were **not** blind-scored. Their Stage B entries are bundle-hypothesis scores with evidence E.

### 1.2 Stages C and D: skeptical memos and deep dives

Each survivor was re-scored with an explicit evidence level (`stageC_C1…C9`, `stageD_DA…DI`). Stage D already cut WS05-007 (fcf 5→4, roic 7→6) and classed WS13-014, WS16-006, WS18-003 and WS18-035 as "reserve". SYN-004 carried a G2_LICENSE WARN through C and passed G2 at D.

### 1.3 Stage E: standardized playbooks and models

- Each finalist got a playbook, a materials file, a sources file and an `08_financial_models` model built on `tools/fin_engine.py`.
- **Standard rules:** a $4,000/month owner draw from month 13, 30% tax, and a start-capital injection equal to base peak funding.
- The audit confirmed all three rules were **followed in all 11** (`CROSS_MODEL_AUDIT.md` §1).

### 1.4 Stage F: adversarial reviewers who wrote nothing they reviewed

- **Six batches.** F1: SYN-006, WS16-006. F2: SYN-004, SYN-001. F3: WS05-007, WS18-003. F4: WS04-014, WS13-014. F5: WS12-012, WS12-014. F6: WS18-035 plus the cross-model audit.
- **Independence.** Every review begins "Reviewer: independent; I did not write any of this."
- **Common protocol:** reproduce the filed model exactly with the engine (every review reports an exact match); challenge the top five drivers against independent evidence; re-run with overrides only, never modifying finalist files (F6 checked md5 sums); re-open cited sources; then write a pre-mortem and corrected scores.
- **New evidence.** 72 new source records: F1 9, F2 26, F3 12, F4 14, F5 7, F6 4 (`07_review/sources_F*.jsonl`).
  - F2-S026 documents access failures: ilga.gov returned 503 or TLS errors on all hosts; Justia, FindLaw, LegiScan and BillTrack50 returned Cloudflare challenges.

### 1.5 Cross-model audit (F6)

- **Harmonized "skeptic" rules H1–H9** were applied to every base scenario as overrides, changing a driver only when the model is more favourable: H1 ≤15 founder conversations/month; H2 conversion ≤8%; H3 ramp ≥6 months; H4 churn ≥1.5%/month; H5 ≤1.0 referral per 100 active; H6 rep output ≤ founder output; H7 franchise-median job volume; H8 growth ≤5%, ROIC ≤60%, EV ≤3.0× (2.38× sensitivity); H9 ARPC growth ≤3%.
- **Founder-Delivery Charge (FDC):** 12 × the loaded monthly cost of the delivery role the founder performs, charged unless a manager on payroll replaces it. Code: `07_review/cross_model_audit.py`; no model file was written.

### 1.6 Citation spot-checks

| Review | Citations opened | Outcome |
|---|---|---|
| WS12-012 | **14** (stated) | 11 verified, 1 partly wrong (TR page lacks the 11% statistic), 1 unverifiable (Accounting Today 29%), 1 incomplete (treaty PE qualifier omitted) |
| WS18-003 | **12** (stated; 13 rows in §12) | 2 returned 403 (Junk Peddler fact sheet, HomeGuide Chicago). 2 mis-applied: College Hunks all-franchise CPL instead of the junk-only column; an Insureon $268 auto median that is not a box-truck figure |
| WS05-007 | **11** (stated; 12 rows in §12) | 1 could not be opened: the HomeAdvisor price source C2-S020, which is the model's #1 driver. 1 partly contradicted: 6 City-licensed pest firms, not ~15 |
| WS12-014 | **11** (stated) | All substantively verified; "the errors are in interpretation" |
| WS18-035 | **11** (stated) | 1 misattribution ($173/$66 is Elevarus, not Searchlight). DDM products.json returned 403 |
| WS13-014 | 13 (enumerated by me from the review) | 1 anchor not at its cited URL (half-day $300–600, C3-S028). 1 URL now redirects (DF-S031). 1 misquote (umbrella $2M vs $5M). 1 page returned 403 (Field Environmental) |
| WS04-014 | 11 (enumerated) | 1 applied to the wrong occupation (help-desk wage). 1 returned 403 (chicago.gov low-voltage rule) |
| SYN-006 | 10 (enumerated) | 2 A-level labels the sources do not carry (225 ILCS 450/8.05; IDOL FAQ 17). 1 vendor blog presented as market data |
| SYN-001 | ~10 (enumerated, mostly re-queries) | FMCSA data reproduced exactly. CCJ page returned 403 |
| SYN-004 | ~10 (enumerated) | Statute read via a mirror. PJM report internally inconsistent (1,105.6 vs 1,200.3 MW) |
| WS16-006 | ~8 (enumerated) | 1 derived figure presented as disclosed (4imprint "81%"). 1 garment match unconfirmed |

**Totals.**
- **59 citations are explicitly counted** in five reviews. About 120 including my enumeration of the other six.
- **At least 10 cited sources could not be opened** (403s, a redirect, unrendered pages, ilga.gov 503).
- The factual-error tables in §2 of the reviews hold **64 rows**. About 10 of those confirm or strengthen the claim (e.g. WS05-007 #3–4, SYN-001 F4, SYN-006 F4, SYN-004 F1). That leaves **roughly 54 substantive corrections**.

---

## 2. Major errors discovered (per finalist)

Effects are base-case operating profit before owner pay, from the reviewers' engine re-runs.

**SYN-006: construction back office** (`SYN-006_review.md`)

| Claim | What the evidence showed | Correction | Y3 / Y5 effect |
|---|---|---|---|
| ARPC $1,000 [D] | Wishup offers a dedicated construction bookkeeper incl. WIP from $999 [D, C5-S035]. The $500–1,800 "list ranges" are a vendor's own blog [C5-S009] | $950 / $800 | $94,734 → $76,822 / $181,482 → $150,093 alone |
| 15 clients per bookkeeper, $5,800 bookkeeper, $600 reviewer | Chicago clerk mean $53,560 [C, F1-S001]; no reviewer rate under ~$150/h (E) | 13; $6,200; $1,000 | All four together: **$49,662 / $82,563** |
| "No licence … for preparing certified payroll [A]" | 225 ILCS 450/8.05 covers accounting only and is silent on CP | Downgraded to E; counsel item | None on profit; removes a false A |
| Western National "No C.P.A." program supports surety-grade product [B] | Capped at $1.5M single and aggregate; effective Oct 2016 [E-SYN006-S005] | The product feeds the CPA; it is not the surety's document | Channel order changed |

**WS16-006: workwear distributor** (`WS16-006_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| GM 30% "C", anchored on 4imprint 31.5% | The playbook's own desk test: 25% tee, 5–10% hoodie, 17% cap and −12% ANSI tee at parity | 27% / 25% (E) | GM 26/24 alone: $52,056 / $89,243 |
| 4imprint keeps "~81%" of orders from existing customers | Derived figure (838k of 1,040k); order mix ≠ account retention | Churn 3%/month | — |
| ARPC $650 | Bottom-up $5–7k/yr at 100% wallet share | $600 | Corrected base **$47,301 / $86,175**; peak with draw $98,336 |

**SYN-004: energy cost management** (`SYN-004_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| Fees start 4 months after a lead | ENGIE pays only once the new contract flows [B, F2-S005]; expiries can be up to 18 months out | Sales cycle 10 months | $98,323 → $62,267 alone |
| 6% DR partner share in ARPC $850 | GridBeyond advertised 100% revenue share plus a floor [D, F2-S010] | ARPC $800, DR ≈ 0 | $90,022 alone |
| Statute "could not be read" | 16-115C(b) exclusion read verbatim via mirror [A, F2-S001] | Exemption upgraded to statutory | Feasibility holds |
| Code of conduct binds only licensees | 16-115C(a-5) applies to "All third-party sales representatives" | Add a utility non-affiliation disclosure | — |
| Combined (cycle 10, 7 leads, 20% win, $800) | | | **$33,486 / $105,728**; peak with draw $122.0k |

**SYN-001: carrier compliance hub** (`SYN-001_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| Attach of 5/14/21/25/28% applied to all clients via `arpc_annual_growth_pct` 9% | The path is attach *by tenure*; the engine credits month-40 joiners with year-4 attach | Cohort attach ≈11% (Y3), ≈13% (Y5) | $48.3k → $37.1k / $177.5k → $113.9k |
| 50% sub-producer split on new and renewal business | Published splits 30–90%; hosts keep expirations [D, F2-S017; C, F2-S018] | 40% blended | **$33.5k / $102.1k**; peak ~$95k |
| Month-12 gate "≥3 insured accounts" | The model gives 10.9 clients × 5% ≈ 0.5 | Reconcile gate and model | — |

**WS05-007: commercial pest control** (`WS05-007_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| Restaurant $125/month ($105 blended) [D, C2-S020] | A 2021 consumer guide recorded as a "search-summary paraphrase", now unopenable. GorillaDesk lows $30–160 [D, F3-S005]; public bids $30–180 [A] | $92 blended (commercial ≈$108) | ×0.75 alone → Y3 $33.5k |
| Rentokil 80.7% retention as B-level restaurant churn | That figure is total NA retention; Commercial "needs more focus" | 2.2%/month; level E | — |
| Implicit greenfield demand | Only 112 licences citywide, 20 in the SW cluster, cited for having no licensed PCO in 12 months [A, F3-S001] | Displacement sale | Win 25% → 21% |
| Combined, technician hired at 140 accounts | | | **$42,875 / $80,218**; peak $78,709 (hiring at 110: Y5 $28,895) |

**WS18-003: junk removal** (`WS18-003_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| Plateau ~106 jobs, $545k, "between" the Junk King median $436k and 1-800-GOT-JUNK | The Junk King median covers all 166 branded units; third quartile $355k [B, F3-S009] | ~80 jobs at $390 | — |
| Ticket $430 [B] | Chicago aggregator ≈$246 [D]; branded national $399–443 | $390 | — |
| Auto ~$600–900; Insureon $268 floor | Box-truck medians: auto $909, WC $673 [D, F3-S010] | Overhead ×1.10 | — |
| Combined, single-zone | | | **$34,878 / $49,383**; multi-zone Y5 −$11,282; peak with no draw $135,934 |

**WS04-014: dental/vet MSP** (`WS04-014_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| Technician $6,500 from IL help-desk median $59,860 | Chicago network support median $73,340 [C, F4-S004] | $7,500 | $64.0k → $46.2k (at $7,900) |
| Siotek offers HIPAA "only in a custom tier"; remote rival | Siotek: HIPAA bundled, free onboarding incl. risk assessment [B, F4-S003], and a Chicago page with on-site coordination [D, F4-S002] | ARPC $650; onboarding $500 | — |
| Combined | | | **$37,459 / $94,859**; peak $69,661; hiring at 18 practices: Y5 $111,741 |

**WS13-014: utility locating / GPR** (`WS13-014_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| Half-day $300–600 [C3-S028] | The page gives only "~$1,000–$3,000 per day"; no half-day figure [D, F4-S010] | ARPC $750 → $700; anchor unsourced | $106k → $79k alone |
| W.E. O'Neil umbrella "$2M" | $5M for Concrete, Electrical, Plumbing, HVAC; 5-year completed-ops [B, F4-S009] | Insurance $1,000/month | — |
| Combined (with repeat 30%, technician $8,700) | | | **$49,869 / $86,098**; peak $110,459 ($145,622 at DSO 60) |

**WS12-012: Philippine accounting staff** (`WS12-012_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| GM 31% labelled C | $1,100 salary sits at the bottom of the $1,463 / $1,500–1,900 bands. Bench, backfill and separation pay are omitted | 27% (E) | Alone: $13,603 / $269,860 |
| ARPC 1.25 × $2,300; 1.2 wins/month | Compliant market $1,963–2,100; partners unreachable Feb–Apr | 1.2 × $2,250; 0.77 wins | Combined **$57,548 / $78,364**; 10-yr deployable $1.26M → $37k |
| Thomson Reuters as D; "only 11% use no automation" | 1040 GA notice is B; the 11% is not on the page | Re-level; drop the statistic | AI threat stronger |

**WS12-014: controls recruiting desk** (`WS12-014_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| ~$195k per producer by year 3 is "optimistic for a newcomer" | PageGroup £148.9k is a blended mature fee earner with brand and database [B] | Optimistic case, not base | — |
| 30% conversation → agreement | The playbook's own pass gate is 5/30 = 16.7% | 22%; fill 20% → 15%; ramp 15 months | **$80,698 / $114,468** (from $170,012 / $259,002) |

**WS18-035: garage doors** (`WS18-035_review.md`)

| Claim | Evidence | Correction | Effect |
|---|---|---|---|
| ~133 jobs × $575 calibrated to Precision $858k / Access year-3 $1.02M [B] | Precision earns $1,213 per job → ~59 jobs; Access had 7 units, average age 1.88, median $389,856 [B, C8-S019, DF-S001] | 58.9 jobs (D/E) | Y3 **+$25k** (fewer loss-making hires) |
| Launch suburbs ≈ Precision's smallest band | Precision counts *detached* homes: 89,152, below the band [C, F6-S002] | Bottom of band | — |
| Opener "≥$870" | Raynor Chicago: opener installed $250–600 [D, F6-S001] | Ticket $545 | −$26k alone |
| 65% book × 85% paid | ServiceTitan small-shop median booking 30% [D, F6-S003] | 55%; CAC $137 | −$36k alone |
| Combined | | | **$51k / $70k**; after founder-technician charge −$22k; peak $110k |

---

## 3. Unsupported or over-stated claims

| Finalist | Claim | Stated | Warranted (reviewer) |
|---|---|---|---|
| SYN-006 | Surety demand for an *outside non-CPA* WIP preparer | B | **E** (B only for demand that a WIP exists) |
| SYN-006 | Surety producers as the #1 channel | — | **E, with contrary priors** |
| SYN-006 | IDOL third-party filing "contemplated" | A | **D/E** inference |
| WS16-006 | Newcomer GM 30% | C | **E**, with B evidence pointing lower |
| SYN-004 | Suppliers will pay an unlicensed exempt-only broker | — | **MISSING**; E with a negative prior |
| SYN-001 | 50% split on new and renewal, founder-owned book | — | **E** |
| WS05-007 | Restaurant $125; blended $105 | D | **D-, unverifiable** |
| WS18-003 | 30% B2B jobs at near-zero CAC | E | **E, internally inconsistent** (the repeat driver yields ~6 per 100) |
| WS18-003 | Economics overall | B | **C** (B only for branded units) |
| WS04-014 | Local on-site range $600–900 | — | **E**; $600–650 defensible |
| WS13-014 | ARPC $750 | — | **E**; GSA rates are federal ceilings |
| WS12-012 | "CAS is less targeted by agentic tools" | — | **E**; QuickBooks agent targets reconciliation |
| WS12-014 | Founder can run a credible PLC/SCADA screen after 2 hours' study | — | **E**; entry 4 → 3 |
| WS18-035 | Revenue density "near $1M within three years" | B | B for Access's few units only, **not** for an independent |
| WS18-035 | Margin after parts 60% | C | **E**; needs an unconfirmed dealer account |

The cross-model audit adds a portfolio-level finding:
- 54 of the 66 long-term driver fields across the 11 models are E, D or D/E;
- 9 are mixed with an E component;
- only 3 are clean C/B (`CROSS_MODEL_AUDIT.md` §1).

---

## 4. Revised financial assumptions

| Finalist | Driver | Stage E | Reviewer | Source / level |
|---|---|---|---|---|
| SYN-006 | ARPC | $1,000 | $950 (cons. $800) | C5-S035, C5-S009 [D] |
| SYN-006 | Clients per bookkeeper | 15 | 13 (11) | Census DB-S036 [C]; E |
| SYN-006 | Bookkeeper loaded cost | $5,800 | $6,200 ($7,000) | F1-S001, F1-S002 [C] |
| SYN-006 | External reviewer | $600/month | $1,000 ($1,500) | MISSING; E |
| WS16-006 | GM recurring / first order | 30% / 28% | 27% / 25% | Playbook §3.1 desk test [B prices, E] |
| WS16-006 | Churn; ARPC; DSO | 2.5%; $650; 40 | 3%; $600; 45 | E; F1-S007 [C] |
| SYN-004 | Sales cycle | 4 months | 10 | F2-S005 [B]; E |
| SYN-004 | Leads/month; win | 10; 22% | 7; 20% | F2-S005 [B]; E |
| SYN-004 | ARPC | $850 | $800 | F2-S010 [D] |
| SYN-001 | Book-average attach, Y3 / Y5 | 21% / 28% | ~11% / ~13% | Cohort recalculation (engine series) |
| SYN-001 | Sub-producer split | 50% | 40% | F2-S017 [D], F2-S018 [C] |
| SYN-001 | Churn | 1.5% | 1.5–1.8% | F2-S024 [C-general] |
| WS05-007 | ARPC | $105 | $92 | F3-S005 [D], C2-S017 [A] |
| WS05-007 | Win; churn; set-up fee; start delay | 0.25; 1.8%; $200; 3 months | 0.21; 2.2%; $150; 4 months | F3-S001 [A], F3-S003 [A]; E |
| WS18-003 | Ticket | $430 | $390 | E-WS18003-S021 [D], F3-S009 [B] |
| WS18-003 | Leads (plateau) | 245 (~106 jobs) | 185 (~80 jobs) | F3-S008, F3-S009 [B] |
| WS18-003 | CAC; GM; overhead | $65; 0.64; ×1.0 | $80; 0.62; ×1.10 | F3-S011, F3-S010 [D] |
| WS04-014 | Technician cost | $6,500 | $7,500 ($8,000) | F4-S004 [C] |
| WS04-014 | ARPC; onboarding | $690; $1,000 | $650; $500 | F4-S003 [B], F4-S002 [D] |
| WS04-014 | Technician hire trigger | 14 practices | 18 (recommended) | Re-run |
| WS13-014 | ARPC | $750 | $700 ($550) | F4-S010, F4-S014 [D] |
| WS13-014 | First job → account; technician; insurance | 35%; $8,300; $750 | 30%; $8,700; $1,000 | DF-S033 [C], F4-S009 [B] |
| WS12-012 | GM | 31% | 27% | S020 [D], DG-S012 [D], E-WS12012-S013 [A] |
| WS12-012 | ARPC; funnel | $2,875; 12 × 40% × 25% | $2,700; 10 × 35% × 22% | B/D anchors; E |
| WS12-014 | Conversion; fill; ramp; cycle | 30%; 20%; 12; 4 | 22%; 15%; 15; 5 | Playbook gate; PageGroup [B]; E |
| WS12-014 | Repeat revenue; churn | $670; 5% | $520; 5.5% | E |
| WS18-035 | Plateau jobs/month | ~133 | 58.9 (cons. 45) | DF-S001, DF-S002, C8-S019 [B] |
| WS18-035 | Ticket; CAC per paid job; GM | $575; $105; 60% | $545; $137; 58% | F6-S001, F6-S003 [D] |
| All recurring | Founder conversations | 9–45 | ≤15 (H1) | F6-S004 [D] |
| All recurring | Conversion | 0.10 template in 4 models | ≤0.08 (H2) | E |
| All | EV multiple; year-6 growth | 2.0–3.5×; 4–10% | ≤3.0× (2.38×); ≤5% | E-WS05007-S007 [D]; Rollins [A] |

---

## 5. Contradictory evidence and preserved disagreements

Each review records where the author and reviewer still disagree. Both views are kept because the deciding fact can only be measured.

| Finalist | Author's view | Reviewer's view | Why both are kept / what settles it |
|---|---|---|---|
| SYN-006 | fcf 5; ceiling $250k; 15 clients per bookkeeper | fcf 4; ceiling ~$150k; 13 | Census (~$130k receipts per employee) shows staffing "not unrealistically lean", recorded in the author's favour. Settled by ≤10 h per client and median ARPC ≥$950 |
| WS16-006 | Base GM 30% | Fails at 27% | The reviewer disagrees with his own verdict: if V1 shows contractors pay 15–35% above 4imprint, the ~$65–78k Y3 base returns. Cost: $0 |
| SYN-004 | Y3 $98k; roic 6; access 4 | Y3 ~$33k; roic 5; access 3 | Both agree it is "not a strong first holding-company asset". Settled by V1 (supplier acceptance) and V3 (expiry statistics) |
| SYN-001 | Y5 $178k; feasibility 6; entry 4 | Y5 ~$102k; 5; 3 | Agrees with the author's ranking caution. Settled by a host term sheet and ≥3 quote authorities in 10 renewals |
| WS05-007 | Evidence C | Evidence D (top driver D-) | Explicitly preserved. Settled by E1 measuring the median price (≥$90 to proceed) |
| WS18-003 | Evidence B | Evidence C | B holds for branded units only. Settled by experiment 2 (B2B reorders within 60 days) |
| WS04-014 | Local on-site premium justifies $690 | $650 until proven | "Not unreasonable; simply unproven". Two or more LOIs at $690+ would restore the ~$64k Y3 |
| WS13-014 | Y3 $106k | Y3 ~$50k | "I cannot show that it is wrong, only that it is unevidenced". Needs measured ARPC ≥$750 and monthly rebooking |
| WS12-012 | Base defensible | Fails | Revisit if V3 shows asks ≤$1,100 and V1–V2 show ≥$2,300 prepaid |
| WS12-014 | Base funnel | Stage E base = optimistic | Top-quartile output (5.21 vs 1.38 placements [D, F5-S007]) would justify the filed base |
| WS18-035 | "Conditional, low priority" | Fails (classification only) | Agrees "on almost every fact". Reopen the B2B variant if paid spring-pair medians are ≥$375 |
| Cross-model | — | Precision CY2024 implies ~166 jobs/month [B, C8-S020] | Kept as a disagreeing figure against the H7 median of 58.9 |

**A disagreement within the review itself.**
- The Stage F **scorecard** composites and the F6 **harmonized-model** composite rank the finalists differently (§8):
  - SYN-001 is #2 by Stage F evidence-adjusted score but #8 on the harmonized model;
  - WS05-007 is #3 against #11;
  - WS12-012, rated "fails" by F5, is #2 harmonized.
- The scorecard weighs qualitative criteria; the harmonized composite ranks only profit, cash and capital. Neither is "the decision".

---

## 6. Competitive weaknesses; legal and regulatory concerns

### 6.1 Competitive weaknesses found

- **SYN-006:** offshore firms advertise WIP (Wishup $999). Construction payroll platforms (Payroll4Construction [D, F1-S005]; Miter [D, F1-S006]) generate CP reports; **neither was named in the playbook**.
- **WS16-006:** 65% of end-buyers buy promo through e-commerce [C, F1-S007]; AGC members get exclusive Cintas discounts [C, F1-S008]; 4imprint publishes the price ceiling.
- **SYN-004:** ENGIE "may also from time to time make contact with Customer outside the presence of Broker", and the customer designates between brokers [B, F2-S005]. Incumbents give the PLC-alert wedge away free.
- **SYN-001:** OOIDA and Simplex already bundle; GEICO writes 8.4% direct; the founder gets "one shot a year per client".
- **WS05-007:** local independents speak customers' languages and can price at $50–80.
- **WS18-003:** 10 licensed 1-800-GOT-JUNK trucks, $79 single-item marketplaces, and dumpster rental as a substitute for full-load cleanouts.
- **WS04-014:** Siotek is in Chicago with free onboarding; Henry Schein One's Omnicore targets the same triggered buyers [B, F4-S006].
- **WS13-014:** GPRS plus at least four coring firms with in-house GPR [D, F4-S013]. "Our coring sub scans for free" is "the most likely incumbent response".
- **WS12-012:** QX (SOC 2 Type II, 500+ firms, $2,500); clients insource to their own EOR [C, S029]; Black Ore pitches against offshoring.
- **WS12-014:** in-house TA uses LinkedIn Hiring Assistant [B]; top firms place 54.4% of hires from their own CRM, and a newcomer starts at 0%.
- **WS18-035:** the "honest pricing" wedge is legally required in Chicago [A, E-WS18035-S004] and already claimed by Precision and Raynor.

### 6.2 Legal and regulatory concerns (wording verified in the review files)

- **SYN-004: licence exemption.**
  - 220 ILCS 5/16-115C(b), read via an unofficial mirror, excludes "any person or entity that is attempting to procure on behalf of or sell retail electric service to a third party that has aggregate billing demand of all of its affiliated electric service accounts in Illinois of greater than 1,500 kW" [A via mirror, F2-S001]. 83 Ill. Adm. Code 454.30(b)(5) is unchanged since 35 Ill. Reg. 17602 [A, F2-S003].
  - **Gap:** 16-115C was also amended by **P.A. 102-958 (HB 4973, eff. 2023-01-01)**, whose content "could not be read (ilga.gov returned 503)" [D, F2-S002]. The playbook asked only about 2025–26 amendments.
  - Also open: the meaning of "affiliated"; the 16-115C(a-5) non-affiliation disclosure; agency agreements under Texas law with a class-action waiver.
- **SYN-001: likely illegal inducement.**
  - The "20% off when we also place your liability" offer appears in the playbook (line 237) and materials (lines 179, 229).
  - 215 ILCS 5/151 bars "any paid employment or contract for services of any kind or any other valuable consideration or inducement to or for insurance... not specified in the policy" [A via mirror, F2-S019].
  - Value-added-services bills appear unenacted (SB 3466; HB 2766 re-referred to Rules) [D, F2-S020].
  - Also: under §500-80, the founder's LLC "almost certainly needs an IDOI business-entity licence" if it receives the split [A via mirror, F2-S021].
  - Gate: G3 WARN, not FAIL, "because the discount is removable".
- **WS12-012: Philippine corporate officers.**
  - The Revised Corporation Code requires "a resident treasurer and a Filipino citizen-resident corporate secretary" [A, F5-S001]. "The founder cannot run the entity alone from Illinois." The nominee cost is not itemised.
  - Also missed: DO 174 labour-only-contracting exposure for client-directed seats [C, F5-S002/S003].
  - Also: the treaty Art. 5(2)(j) qualifier "(for the same or a connected project)"; and the Form 5471 $10,000 penalty (IRC §6038(b), not re-fetched).
- **WS12-014: Private Employment Agency Act exclusion.**
  - 225 ILCS 515/1.1 is verified, "with its 'never charged … résumé … other personal service' proviso".
  - "'Indirectly' charging a fee, or 'any other personal service' (résumé polishing, interview coaching sold to candidates, or a candidate-paid 'career' product later), voids it [A]." The exclusion is "an operating discipline, not a one-time fact".
  - Feasibility 9 stands.
- **SYN-006: SB1344 third-party filer liability.**
  - SB1344 adds civil penalties of $1,000 / $2,000 per missed month on the employer and on "any officer, employee, or agent … whose duty … is to file" [C, C5-S019 verified].
  - An engagement letter making the firm responsible for timely submission makes it that agent. E&O "probably excludes the fines themselves".
  - Debarment comes from 820 ILCS 130/11a, not SB1344 (Stage C/D conflation).
  - Also unaddressed: Illinois PIPA (815 ILCS 530) for worker SSNs; Class A misdemeanour exposure for wilful false certification (820 ILCS 130/5).
- **WS05-007: pest-bait reclassification proposal.**
  - EPA's November 2022 proposed interim decisions would make "all second-generation anticoagulant rodenticides, strychnine and zinc phosphide restricted-use pesticides", and first-generation anticoagulants, bromethalin and cholecalciferol in packages over 1 lb. The EPA page "still shows this as proposed, not final" [A, F3-S004].
  - Illinois requires restricted-use subcategory exams [A, F3-S002]. A general-use-only CT "could not use the professional rodent baits this business runs on".
  - The 830.270 one-hour supervision rule also caps delegation.
- **Others:** WS04-014's business-associate contractual liability (PerCSoft/DDS Safe hit ~400 dental practices [C, F4-S001]); WS13-014's GC indemnity and $5M umbrella; WS16-006's SanMar "continuing and irrevocable" personal guaranty [B, DH-S024].

---

## 7. Operational risks surfaced

- **Founder hours as the business.**
  - SYN-006: ~200 h/month in months 10–24; the founder keeps ~12 clients through year 5.
  - SYN-001: ~95 h servicing plus ~90 h selling a month.
  - WS05-007: ~140 accounts plus selling "fills a 55–60 h week".
  - WS18-035: 60 jobs/month plus selling. At 45 jobs of founder capacity, the reviewer base is −$41k in year 3.
- **Hiring valleys and thin hired units:** a WS05-007 technician hired at 110 accounts sinks Y5 to $28,895; a WS13-014 technician earns $3,200/month at full fill; a WS18-035 technician ≈ +$0.9k/month; a WS16-006 rep at 45% of GP leaves the firm ~15% of sales; a WS18-003 ops manager needs ~$600k of revenue.
- **Capital beyond the $100k backing** (harmonized peak with draw): SYN-001 $139k, WS18-003 $204k, WS05-007 $206k. WS18-035 reaches $110k under reviewer drivers, and SYN-004 $122k under F2 drivers.
- **Working capital:** WS16-006 carries ~$82k of unsecured contractor AR in year 3; WS12-012 accrues ≈$40k of 13th-month pay at 40 seats, payable 24 December [A].
- **Seasonality:** WS13-014's Dec–Feb 811 hit tickets run ~30% below Apr–Oct [A, F4-S008], so a January pilot runs in the trough; WS12-012's CPA partners are unreachable Feb–Apr, so the first buying window is May–June 2027.
- **Single-point compromise:** in WS04-014 one RMM compromise could hit every client.
- **Gatekeepers and supply:** IDPH exam seats (10 per session, no 2027 dates [A, F3-S003]); SSC sells "ONLY … to professional garage door dealers"; ENGIE asks for "broker/agent licenses and/or state approval documents" [B, F2-S004]; SWANCC Glenview closes 10 AM–2 PM [B, F3-S007].
- **Competence:** WS13-014 plans 2 days' training against GPRS's 4 weeks + 80 h + 4 weeks [D]. SYN-006's surety-grade WIP judgment "takes most practitioners years".
- **Liability events:** a SYN-006 misclassification triggers back wages, a 20% IDOL penalty and SB1344 penalties. WS12-014 should budget one collections action in 24 months.

---

## 8. Corrected rankings

**Method.** These are evidence-adjusted v1 composites for the 11 finalists. Rank is among the 11, computed by me.
- **Stage B** is from `screening_dispositions.csv`. Bundles carry non-blind bundle scores.
- **Stages C–F** are computed from `stage_history` with `tools/score.py`'s formula. My computations reproduce every Stage E and F composite the reviewers quote; for example SYN-006 E 5.65, WS16-006 E 5.20, SYN-004 E 5.06.
- **Harmonized** is the four-rank composite in `CROSS_MODEL_AUDIT.md` §4.

| ID ("=" = exact tie) | B adj (rank) | C | D | E | F | Change E→F | Harmonized model rank (orig → harm) |
|---|---|---|---|---|---|---|---|
| SYN-006 | 5.46 E (6) | 5.65 (2) | 5.65 (1) | 5.65 (1) | **5.20 (1)** | −0.45 | 2 → **3** |
| SYN-001 | 5.42 E (8) | 5.61 (3) | 5.29 (8=) | 5.26 (4=) | **4.87 (2)** | −0.39 | 4 → **8** |
| WS05-007 | 6.33 C (1) | 5.85 (1) | 5.57 (3) | 5.47 (3) | **4.84 (3)** | −0.63 | 9 → **11** |
| WS04-014 | 5.66 E (2) | 5.51 (5) | 5.51 (5) | 5.48 (2) | **4.74 (4)** | −0.74 | 7 → **5** |
| WS12-014 | 5.23 C (10) | 5.38 (7) | 5.38 (7) | 5.17 (7) | **4.65 (5)** | −0.52 | 1 → **1** |
| WS13-014 | 5.60 D (3) | 5.20 (11) | 5.19 (11) | 5.26 (4=) | **4.57 (6)** | −0.69 | 6 → **9** |
| WS12-012 | 5.52 E (5) | 5.49 (6) | 5.62 (2) | 5.00 (9) | **4.53 (7)** | −0.47 | 3 → **2** |
| SYN-004 | 5.11 E (11) | 5.32 (10) | 5.56 (4) | 5.06 (8) | **4.50 (8)** | −0.56 | 8 → **4** |
| WS16-006 | 5.42 C (9) | 5.33 (8=) | 5.20 (10) | 5.20 (6) | **4.42 (9)** | −0.78 | 5 → **6** |
| WS18-035 | 5.45 E (7) | 5.53 (4) | 5.29 (8=) | 4.71 (11) | **4.29 (10)** | −0.42 | 11 → **7** |
| WS18-003 | 5.57 B (4) | 5.33 (8=) | 5.46 (6) | 4.83 (10) | **4.12 (11)** | −0.71 | 10 → **10** |

**How the scores moved.**
- **Every composite fell at Stage F**, by 0.39 (SYN-001) to 0.78 (WS16-006). The largest falls were in fcf, roic, access, entry and delegation. The mean Stage F score is ~4.6, against ~5.5 at Stage B.
- **WS05-007** was #1 at Stages B and C. It ends #3 on the scorecard and last on the harmonized model: its $105 ticket was unverifiable, and capping founder conversations at 15 (from 45) alone takes Y5 to $38k.
- **WS13-014** swung from #3 (B) to #11 (C, D) to #4= (E). The audit calls its rank "not robust": it moves from #5 to #9 on H1 alone.
- **WS12-014** is #1 in **every** harmonization variant, including the original. Its Stage E drivers "were already benchmark-capped". Its Y5 after FDC ($84k) ties WS12-012 ($87k), and its robustness depends on H5.
- **SYN-004 and WS04-014** *rise* under harmonization (8→4, 7→5), partly through deferred hiring; read them after FDC ($57k, $55k).
- **Data-integrity note.** `03_screening/scores.csv` and `opportunities.jsonl` still carry WS18-035 at its *Stage E* revision (raw 4.59 / adj 4.713). The F6 update (`stageF_F6.jsonl`: raw 3.99, adj 4.29) was not merged. The table above uses the F6 figures.

---

## 9. Cross-cutting lessons

1. **Founder unpaid delivery labour was embedded in profit.**
   - In 10 of 11 models, operating profit includes the founder performing a $4.8–6.9k/month delivery role. Only WS18-003 pays a manager to replace it.
   - Capacity-triggered hiring makes lower demand look more profitable: WS18-035 +70% Y5, WS04-014 +11%, SYN-004 +15% under the skeptic set.
   - After the FDC, no finalist clears $100k harmonized. Report "Y5 op after FDC" beside raw profit.
2. **Funnel drivers came from template defaults.**
   - Four models (SYN-001, WS05-007, WS16-006, WS12-012) use exactly 0.40 × 0.25 = 0.10, the engine's defaults, labelled E.
   - Founder volumes ranged from 9 to 45 conversations a month, against a full-time SDR median of 10 meetings [D, F6-S004].
   - Capping both cuts Y5 by 55–77% for five models.
3. **Optimism stacked.** Each driver looked defensible alone; together they were not:
   - SYN-006: four drivers each worth $5–18k of Y3 cut Y3 by 48%.
   - SYN-001: three rules each take Y5 to ~$91–99k; jointly to $48k.
   - WS12-012 assumed the newcomer "wins on price, cost and volume at the same time".
4. **Real prices lowered the economics in 10 of 11.**
   - Every finalist except WS12-014 had its price or margin cut once a real comparator was found: Wishup $999, Siotek $399, Raynor, Chicago aggregator tickets, the 4imprint desk test, the compliant offshore market, GridBeyond's 100% pass-through, the cohort-correct insurance attach.
   - WS12-014's fee was verified and kept ("Fee rate is not the vulnerability… Volume is"). It fell on its funnel instead.
   - All 11 composites and all 11 Y3 base figures fell. Y5 rose only for WS18-035, through fewer loss-making hires.
5. **Incumbent benchmarks were applied to a newcomer.** 4imprint's GM, Rentokil's total retention, a mature PageGroup fee earner, Junk King's all-unit median and Access's year-3 average all describe scale or branded firms. Precision's revenue was converted at half its own ticket. Calibrate in units (jobs, placements, seats) at a newcomer quantile.
6. **Evidence labels drifted upward.** Some A labels rest on sources that do not say the claim (SYN-006 F1, F2). Some B labels describe a different population (WS18-035 volume; WS18-003 economics). Some C labels are really E (WS12-012 and WS16-006 GM).
7. **Long-term drivers sat above their anchors.** Year-6 growth was 8–10% against Rollins residential at 5.0% [A]. One 2.38× sold-comps source supports EV multiples from 2.0× to 3.0×.
8. **Validation gates contradicted the models.** SYN-001's month-12 gate is 6× the model's expectation; WS12-014's pass gate implies 16.7% conversion against the model's 30%.
9. **Step-function artefacts mislead year-3 comparisons.** Y3 rose under lower demand in SYN-006, WS12-012, SYN-001, WS12-014 and WS13-014, because hires were deferred. Judge on Y5, after FDC.
10. **Statute access is an evidence ceiling.** With ilga.gov unreachable, statute text came from mirrors ("A-text with C-currency"). Every legal conclusion still needs official text and counsel.

---

## 10. Unresolved questions that only real-world validation can answer

**Cross-cutting.**
- Founder conversations per month while delivering, and their conversion (every recurring rank depends on H1/H2).
- Realised prices from signed contracts, not published bands.
- Real distributor, dealer and insurer quotes (SanMar/S&S, SSC/Clopay, E&O penalty and contractual-liability wording, a $5M umbrella).
- Counsel on official statute text (P.A. 102-958; §151; §500-80; DO 174; 225 ILCS 441).

**Per finalist** (tests named in the reviews):

| ID | Question | Test / threshold |
|---|---|---|
| SYN-006 | Is CP preparation regulated? Does E&O cover SB1344 penalties? Can an outside preparer use the client's IDOL log-in? Real hours per client? | Counsel plus an E&O quote before the first CP job; ≥5 clients at a median ≥$950; ≤10 h per client; ≥2 paid health checks from cold outreach |
| WS16-006 | Do Chicago contractors pay ≥1.15× 4imprint? | V1 incumbent-invoice benchmark ($0) plus V2 net quotes; V5 reorder check before any hire |
| SYN-004 | Will ARES onboard an exempt-only broker? What is the expiry distribution? Will customers pay a flat fee? | V1 (2 of 3 ARES in writing within 45 days) in parallel with a customer-paid offer; V3 (≥30% of expiries ≤12 months); no draw until 5 paying accounts |
| SYN-001 | Host split, expiration ownership and non-solicit terms; quote authority at renewal | V1 (≥2 written term sheets out of 12); V4 on the first 6 renewals; §151 counsel opinion before any materials |
| WS05-007 | Neighbourhood price and switching rate; is NW a better cluster? Will the RUP rule be finalised? | E1 (≤$150) plus ≥10 NW interviews; median ≥$90 and ≥25% switching; E4 ≥6 accounts at ≥$100; restricted-use exam in year 1 |
| WS18-003 | Do B2B accounts reorder? Private gate rates and insurance cost? | Experiment 2 scored on reorders within 60 days; insurance ≤$15k/yr and disposal ≤$100/ton |
| WS04-014 | Price against Siotek; referral-partner introductions; insurer cover of BAA liability | Experiment 4 (walk away below $600); experiment 1 as first kill gate; attorney and insurer sign-off before the first contract |
| WS13-014 | Chicago price, visit frequency, trust for post-tensioned work, insurability | E1 ($0–200): median ≥$600 plus dated bookings before a $9–10k pilot; E2 written insurance terms; pilot in March–April, not the winter trough |
| WS12-012 | Qualified salary asks; prepaid acceptance; DO 174 and resident-officer answers | V3 ($99) ≤$1,100; V1–V2 ≥$2,300 prepaid; counsel before month 6; no entity before ≥8 renewed seats |
| WS12-014 | Can a newcomer convert ≥5 of 30 conversations and reach final rounds? Does the founder tolerate cold calling? | Test 3 ($0–270); final rounds by month 4; abandon if cold calling is disliked after 60 days; month-24 boutique-or-harvest decision |
| WS18-035 | Paid spring-pair medians and opener prices; dealer access; LSA booking rate | V1 desk benchmark ($0): stop if spring pair <$325; V3 supplier questions; V5 LSA test only after V1 and V2 pass |

**Bottom line.**
- The reviews do not show any finalist to be bad. They show that none is yet **proven**, and that each one's Stage E base case sat at the favourable end of nearly every uncertain driver.
- The strongest claim the evidence supports is the audit's: two staffing-type models (WS12-014, WS12-012) and two recurring B2B services (SYN-004, WS04-014) are "the least sensitive to cross-model optimism".
- Most finalists can be tested for $0–$3k, so the right next step is to run those tests in the order given above. Committing to any one business now would be premature.
