# OsteoQuant Revenue Model (v2, 2026-11-27)

**Status: every price, volume and conversion rate in this file is a hypothesis [HYP] or an analyst assumption [AE].**
OsteoQuant is pre-revenue and unincorporated. It has no customers, no interviews, no pilots and no letters of intent. The revenue figures below show what the hypotheses imply. They are not forecasts.

Evidence labels follow `PROSPECTS.md`: [V] verified primary source, [RF] reported fact, [AE] assumption, [INF] inference, [HYP] hypothesis to test, [UNR] unresolved.

| Artefact | What it holds |
|---|---|
| `FINANCIAL_MODEL.xlsx` | Formula-driven model. Sheets: Inputs, P&L Bootstrapped, P&L Venture, Unit economics, Market check, Sensitivity |
| `build_financial_model.py` | Rebuilds the workbook and both JSON files. It checks that no formula references itself, then recalculates the workbook in LibreOffice and checks it against a Python copy of the same model (last run: 1,221 formulas, no self-references, max relative difference 4×10⁻¹⁵) |
| `financial_model_outputs.json` | Per structure and scenario: revenue by offering, volumes, gross margin, EBITDA, cash with and without grants, equity requirement |
| `revenue_model_sensitivity.json` | One-way and two-way sensitivity, plus the break-even study price |
| `PRICING_VALIDATION_PLAN.md` | How each price hypothesis gets tested, with the decision thresholds |

---

## 1. Offerings and price hypotheses

The product is an **offline desktop application**. Scans stay on the analyst's or customer's machine, and the application separates new bone, residual graft and host bone, reports morphometry, registers later time points to a day-0 scan, abstains when a measurement is not supported, and writes an audit trail and a study report. Around it sit three services. The price ranges were set by the founder as hypotheses to test.

| # | Offering | Unit and scope [AE] | Price range [HYP] | Base value in model | Likely buyer [INF] | What it is *not* |
|---|---|---|---|---|---|---|
| O1 | **Paid pilot** | 10–20 retrospective scans from a completed study; blinded comparison with the customer's own analysis (`templates/PILOT_PROPOSAL.md`) | $2,500–5,000 | $3,500 | Manufacturer R&D, CRO study director | Not a validation of the customer's material |
| O2 | **Non-GLP study analysis** | ≤40 scans, ≤2 time points, one defect model; reviewed three-class segmentation, morphometry, report | $8,000–15,000 per study | $11,000 | SME orthobiologic and dental manufacturers | Not GLP. Not for regulatory submission without the customer's own QA review |
| O3 | **Material characterisation** | Can new bone and this graft material be told apart at the customer's scanner settings? Covers the known-truth phantom and simulator assessment, a scan-protocol recommendation and a day-0 protocol design | $5,000–15,000 | $9,000 | Manufacturers before a study, CROs designing one | Not a claim that separation will work. The answer may be "not separable by micro-CT alone" |
| O4 | **Academic desktop licence** | One lab or core per year, local install, updates, email support | $4,000–10,000 per year | $6,000 | NIH-funded bone-repair labs, micro-CT cores | Not a fee-for-service licence for third parties |
| O5 | **Enterprise desktop licence** | One organisation per year, multi-seat, onboarding, a validation-evidence pack (documents what was tested, not a GLP validation) | $30,000–75,000 per year | $45,000 | Preclinical CROs, high-volume manufacturers | No GLP validation, no Part 11 compliance, no claim of regulatory acceptance |

**What changed from v1 (playbook prices in `MARKET_MODEL_INPUTS.md` §5 and `SCIENTIFIC_EVIDENCE.md` §6):**
- The **$25K GLP-study offering is removed.** It cannot be sold until a validation report and a Quality Agreement exist.
- The $40K CRO licence becomes the **$30–75K enterprise licence**. The $4K academic licence becomes **$4–10K**.
- **Paid pilot** and **material characterisation** are new.
- Cloud compute (previously $120–250 per study) falls to **~$0** because analysis runs locally.
- Customer counts are no longer typed in. They are **derived from a funnel** (§4), so the sensitivity analysis can show which conversion assumption matters most.

### 1a. Published price anchors (verified only)
| Anchor | Published figure | Source (accessed 2026-11-27) | How to use it |
|---|---|---|---|
| Hospital for Special Surgery micro-CT core: analysis performed by the core | **$200/h corporate**, $100/h academic non-NIH, $75/h NIH-funded; $25/h self-analysis on the core workstation | https://www.hss.edu/research/core-facilities/micro-computed-tomography-core [V] (the page carries no effective date for the fee schedule) | The base study price ($11K) equals **55 h** of core analysis at the published corporate rate. The $8–15K range equals **40–75 h**. This is one core's hourly rate, not a market average |
| Beckman Microscopy Suite, Versa 630 instrument time | $40.00–79.02/h, by user category | https://microscopy.beckman.illinois.edu/equipment/fees [V], effective 2021-08-01, "subject to change", via `validation/BILL_OF_MATERIALS.csv` | Pass-through cost of scanner time in material characterisation (O3). This is instrument time, not analysis |
| Dragonfly (Comet) academic licence | Free for individuals at degree-granting institutions; excludes fee-for-service and industry collaboration | `docs/research/COMPETITOR_INTELLIGENCE.md` [V] | A free substitute for academic **software** sets a hard ceiling on O4 unless the graft-specific value is clear |
| Scanco analysis service, Dragonfly commercial licence | Not published ("priced by estimate" / by quote) | `docs/research/COMPETITOR_INTELLIGENCE.md` [V] | **Do not use as an anchor.** No figure exists to cite |

---

## 2. Unit economics

### 2a. Analyst hours per non-GLP study (assumption; replace with timestamps from the first pilot)
| Step | Low | Base (2027) | High | Basis |
|---|---|---|---|---|
| Data intake, checksums, format and calibration QC | 2 | 4 | 8 | [AE] |
| Defect ROI placement and review (20–40 scans) | 5 | 8 | 10 | [AE] automatic ROI with manual check, ~15 min per scan |
| Material-specific adaptation (label 1–3 scans, fine-tune) | 6 | 10 | 16 | [AE] experiment R8: 1–3 labelled scans lift held-out graft Dice from 0.84 to 0.86–0.91 (synthetic) | **Requires the customer's written opt-in** for training on their scans (default: no training on customer data — `templates/DPA_ISSUES_CHECKLIST.md`); the adapted weights are kept per customer and are not used for other customers or the general model.
| Segmentation review and correction | 5 | 15 | 20 | [AE] spot-review of flagged and uncertain regions at 15–30 min per scan |
| Morphometry, group statistics | 4 | 6 | 8 | [AE] |
| Report assembly and QA read | 6 | 9 | 12 | [AE] |
| Client calls, protocol approval, revisions | 4 | 8 | 10 | [AE] |
| **Total** | **32** | **60** | **84+** | Model: Conservative 90 → 55 h, Base 60 → 32 h, Optimistic 45 → 22 h over 2027–2031 (learning curve [AE]) |

**Stress test (not in the scenarios).** `SCIENTIFIC_EVIDENCE.md` §5 assumes a reviewer needs 20 s per slice. If every slice of a 300–600-slice defect ROI [AE] had to be reviewed, review alone would take 1.7–3.3 h per scan, or 50–100 h for 30 scans. Replacing the 15 h of spot-review in the Base column gives about 95–145 h per study, which costs $5.7–8.7K at $60/h plus data handling. Under those conditions an $8K study earns between +28% and −9% contribution margin, and an $11K study earns 21–48%. **Measuring real review time is the first job of the pilot.**

### 2b. Delivery cost and contribution per unit (Bootstrapped; `Unit economics` sheet)
Delivery cost = analyst hours × loaded rate ($65 / $60 / $55 per hour [AE]) + data handling ($75 / $40 / $25: encrypted drives, shipping, backup [AE]) + scanner pass-through for O3 ($1,500 / $1,000 / $500 [AE]). **Compute ≈ $0**, because the application runs on local hardware.

| Offering | Scenario | Price | Delivery cost (2027) | Contribution (2027) | Margin (2027) | Margin (2031) |
|---|---|---|---|---|---|---|
| Paid pilot | Cons / Base / Opt | $2,500 / $3,500 / $5,000 | $2,350 / $1,540 / $850 | $150 / $1,960 / $4,150 | 6% / 56% / 83% | same |
| Non-GLP study | Cons / Base / Opt | $8,000 / $11,000 / $15,000 | $5,925 / $3,640 / $2,500 | $2,075 / $7,360 / $12,500 | 26% / 67% / 83% | 54% / 82% / 92% |
| Material characterisation | Cons / Base / Opt | $5,000 / $9,000 / $15,000 | $5,475 / $3,440 / $2,175 | **−$475** / $5,560 / $12,825 | **−10%** / 62% / 85% | same |
| Academic licence (yr) | Cons / Base / Opt | $4,000 / $6,000 / $10,000 | $1,040 / $600 / $330 (support h) | $2,960 / $5,400 / $9,670 | 74% / 90% / 97% | same |
| Enterprise licence (yr) | Cons / Base / Opt | $30,000 / $45,000 / $75,000 | $7,800 / $4,800 / $2,750 | $22,200 / $40,200 / $72,250 | 74% / 89% / 96% | same |

**Reading:**
1. At the bottom of its range ($5K), material characterisation **loses money** under conservative cost assumptions (60 h plus $1.5K of scanner time). Either set a floor of about $7.5K or limit the scope to customer-supplied scans.
2. A pilot at $2.5K roughly breaks even. Treat it as a sales cost that filters for serious buyers, not as a profit line.
3. Licences carry high margins only if support stays within 6–16 h per academic and 50–120 h per enterprise licence per year [AE]. That has not been measured.

---

## 3. Structures
- **Bootstrapped:** a founder-led services-plus-licence business. Analyst time is paid as cost of goods sold at the loaded rate (this includes the founder's own analysis hours). Salaries cover only non-delivery work and grow from $0–24K to $48–150K.
- **Venture:** the same prices and conversion rates, with a funded team (salaries $150–250K in 2027, rising to $1.0–1.5M in 2031), more conversations, and hypothetical expansion modules (osseointegration, spine fusion, histology registration) at 5–40% of core revenue from 2029. Those modules are **not built**. Money buys more conversations; it does **not** buy higher conversion rates, so the rates are deliberately left the same.

## 4. Conversion funnel assumptions
No published conversion benchmark for this niche was verified, so every rate is founder-set and has to be measured. The decision thresholds that would confirm or replace each one are in `PRICING_VALIDATION_PLAN.md` §7.

| Input | Cons / Base / Opt (Bootstrapped) | Rationale |
|---|---|---|
| Qualified industry conversations per year (distinct buying units) | 12–25 / 20–35 / 25–50 | [AE] Founder capacity alongside full-time study. Capped by ~200 US-visible industry buying units: 41 bone-void-filler and 24 dental applicants active in 2023–26, 117 spine applicants and 10–25 CROs (`MARKET_MODEL_INPUTS.md` §1b, §2). For scale, NSF I-Corps Teams expects ≥100 customer and partner interviews over its curriculum ([V] NSF 25-549, accessed 2026-11-27); those are learning interviews, not qualified buyers |
| Conversation → paid pilot | 8% / 15% / 22% | [HYP] A paid pilot requires the customer to share retrospective scans. Confidentiality and sponsor consent are the expected blockers (`INTERVIEW_CODING_SCHEME.md` §6) |
| Paid pilot → recurring study customer | 25% / 40% / 50% | [HYP] Conditional on the pilot meeting its pre-specified agreement criteria |
| Study-customer retention per year | 60% / 75% / 85% | [HYP] Manufacturers' study cadence is lumpy: about one clearance per active firm every 1–2 years [INF from §1a counts] |
| Studies per active customer per year | 1.0 / 1.5 / 1.8 | [AE] `MARKET_MODEL_INPUTS.md` §4 (bone-void-filler firms 0.5 / 1.5 / 3) |
| New customers' first-year studies | 50% of a full year | [AE] Timing convention |
| Material characterisations per paid pilot | 20% / 40% / 50% | [HYP] Sold where the pilot shows graft and new bone overlapping in density |
| Academic evaluations per year | 2–8 / 4–18 / 6–25 | [AE] Against 45–49 organisations with NIH micro-CT bone-repair projects (lower bound, `MARKET_MODEL_INPUTS.md` §3) |
| Evaluation → academic licence | 20% / 35% / 45% | [HYP] Free general-purpose tools exist (Dragonfly academic, BoneJ) |
| Academic retention | 70% / 80% / 85% | [HYP] Tied to grant cycles |
| New enterprise licences per year | 0,0,0,0,1 / 0,0,1,0,1 / 0,0,1,1,1 | [HYP] Long CRO procurement and vendor qualification (`INTERVIEW_GUIDE.md` §8) |
| Enterprise retention | 80% / 85% / 90% | [HYP] |
| Grants (Bootstrapped) | $0 / $325K / $345K | [HYP] One NSF or NIH Phase I (up to $305K NSF [V]) plus small student awards. **Conditional:** PI eligibility for a full-time student is unresolved (`grants/NSF_vs_NIH_ELIGIBILITY.md`) |

## 5. Scenarios (hypothetical; 2027–2031)

### 5a. Total revenue, $ (`financial_model_outputs.json`)
| Structure / scenario | 2027 | 2028 | 2029 | 2030 | 2031 | Gross margin 2031 |
|---|---|---|---|---|---|---|
| Bootstrapped: Conservative | 5,920 | 12,672 | 19,435 | 24,844 | 58,494 | 63% |
| **Bootstrapped: Base** | **39,600** | **85,170** | **177,028** | **210,610** | **287,555** | **84%** |
| Bootstrapped: Optimistic | 132,875 | 309,462 | 566,608 | 822,731 | 1,051,934 | 93% |
| Venture: Conservative | 10,400 | 21,360 | 64,080 | 105,223 | 143,113 | 66% |
| Venture: Base | 59,400 | 172,755 | 299,452 | 501,410 | 706,242 | 82% |
| Venture: Optimistic | 193,225 | 515,532 | 968,290 | 1,663,602 | 2,431,719 | 89% |

### 5b. Cash, $
| Structure / scenario | Cumulative cash 2031, with grants | Without grants | Equity needed (max deficit), with grants | Without grants |
|---|---|---|---|---|
| Bootstrapped: Conservative | −251,661 | −251,661 | 251,661 | 251,661 |
| Bootstrapped: Base | 382,331 | 57,331 | 0 | 60,076 |
| Bootstrapped: Optimistic | 2,138,148 | 1,793,148 | 0 | 0 |
| Venture: Conservative | −3,820,595 | −4,125,595 | 3,820,595 | 4,125,595 |
| Venture: Base | −2,384,831 | −3,959,831 | 2,384,831 | 3,959,831 |
| Venture: Optimistic | 283,433 | −1,311,567 | 839,059 | 1,420,266 |

### 5c. What drives Bootstrapped Base in 2031
- **Volumes:** 5.2 paid pilots, 7.4 studies, 2.1 characterisations, 15.2 academic licences and 1.7 enterprise licences (fractional values are expected values).
- **Revenue mix:** studies $81.6K (28%), academic licences $91.2K (32%), enterprise licences $77.5K (27%), pilots $18.4K, characterisations $18.9K. **Licences make up 59% of 2031 revenue**, so the desktop product, not the service, carries the Base case.
- **Capacity:** 0.5 delivery FTE. The founder alone could deliver the Base case; the Optimistic case needs about 0.8 FTE.

### 5d. Market check (`Market check` sheet)
Recomputed at the Base price hypotheses ($11K per study, $6K academic licence), the serviceable pool is:

| | Pool low | mid | high |
|---|---|---|---|
| Industry per-study pool | $0.52M | $1.26M | $2.40M |
| Academic licences | $0.29M | $0.60M | $1.50M |
| **Total** | **$0.81M** | **$1.86M** | **$3.90M** |

The pool excludes material characterisation. Enterprise licences are left out because they overlap the industry rows. Counts are [V]; per-organisation volumes are [AE].

Modelled 2031 revenue as a share of the **mid** total pool:

| Structure | Conservative | Base | Optimistic |
|---|---|---|---|
| Bootstrapped | 3% | 15% | 56% |
| Venture | 8% | 38% | 130% |

The Bootstrapped Optimistic and both Venture Base and Optimistic exceed what US graft-defect work alone can plausibly supply, so they **require** non-US sponsors, higher study volumes than assumed, or expansion modules. This repeats the v1 conclusion: graft-defect analysis alone supports a founder-scale business, not a venture-scale one.

## 6. Sensitivity (Bootstrapped Base; `Sensitivity` sheet, `revenue_model_sensitivity.json`)
Base outputs: 2031 revenue **$287,555**; cumulative 2027–31 EBITDA **$57,331**, with no grants counted. Each row moves one input to its Conservative and Optimistic value while every other input stays at Base.

| Input (low → high) | 2031 revenue low / high | Swing | Cum. EBITDA low / high |
|---|---|---|---|
| Conversation → paid pilot (8% → 22%) | 232,081 / 343,029 | 110,948 | −76,173 / 190,835 |
| Academic licence price ($4K → $10K) | 257,165 / 348,336 | 91,170 | −20,609 / 213,210 |
| Academic evaluations per year | 240,710 / 328,101 | 87,390 | −43,726 / 153,169 |
| Industry conversations per year | 252,279 / 333,404 | 81,125 | −26,303 / 145,712 |
| Enterprise licence price ($30K → $75K) | 261,718 / 339,230 | 77,512 | 3,744 / 164,506 |
| New enterprise licences | 255,043 / 325,805 | 70,762 | −46,083 / 131,701 |
| Evaluation → academic licence (20% → 45%) | 248,482 / 313,604 | 65,122 | −32,856 / 117,456 |
| Study price ($8K → $15K) | 265,301 / 317,227 | 51,926 | −8,207 / 144,715 |
| Pilot → study customer (25% → 50%) | 256,956 / 307,955 | 50,999 | −13,469 / 104,531 |
| Studies per customer (1.0 → 1.8) | 260,356 / 303,875 | 43,519 | −5,603 / 95,091 |
| Study-customer retention (60% → 85%) | 265,528 / 306,345 | 40,817 | 18,354 / 88,534 |
| Characterisation price ($5K → $15K) | 279,155 / 300,155 | 21,000 | 20,131 / 113,131 |
| Characterisation attach (20% → 50%) | 278,105 / 292,280 | 14,175 | 31,477 / 70,258 |
| Pilot price ($2.5K → $5K) | 282,305 / 295,430 | 13,125 | 34,081 / 92,206 |
| Analyst hours per study | no revenue effect | 0 | 23,915 / 72,283 |
| Loaded analyst rate ($65 → $55) | no revenue effect | 0 | 44,968 / 69,694 |

**Two-way grid** (2031 revenue): study price × pilot-to-customer rate.

| Study price | 25% | 40% | 50% |
|---|---|---|---|
| $8K | 243,048 | 265,301 | 280,137 |
| $11K | 256,956 | 287,555 | 307,955 |
| $15K | 275,501 | 317,227 | 345,045 |

**Break-even study price.** With everything else at Base and no grants, cumulative cash reaches zero by 2031 at a study price of **$8,376**, inside the hypothesis range. In the Venture structure the equivalent figure is **$115,887**: no plausible study price funds the venture cost base.

**What the sensitivity says [INF]:**
1. The two inputs that most often decide whether Base makes or loses money are the **share of conversations that become paid pilots** and **academic willingness to pay** (price and conversion). Both are untested.
2. The study price matters less than expected. Study volume in Base is small (7 per year by 2031), so the price per study moves revenue less than the funnel does.
3. Analyst hours do not change revenue. They change cash by up to $48K over five years at these volumes, but the stress test in §2a shows they could erase the margin on low-priced studies.

## 7. Evidence needed to move each hypothesis to "validated"
"Validated" means the stated evidence exists in `interview_log_template.csv` rows or signed documents, not that the hypothesis was discussed. Thresholds and methods are detailed in `PRICING_VALIDATION_PLAN.md`.

| Hypothesis | Status now | Evidence that validates it | Evidence that rejects or revises it |
|---|---|---|---|
| H1. Paid pilot at $2.5–5K | [HYP] | ≥3 signed paid pilots at ≥$2.5K from the first 10 pilot offers | 0 of the first 5 offers accepted: test a free pilot that converts to a paid study instead |
| H2. Non-GLP study at $8–15K | [HYP] | ≥8 industry Van Westendorp responses whose acceptable range overlaps $8–15K; ≥40% of decision-makers say yes at ≥$8K on the price ladder; then ≥1 paid study at ≥$8K | Median "too expensive" price below $8K, or analysis costs under 5% of the study budget |
| H3. Material characterisation at $5–15K | [HYP] | ≥2 manufacturers code the graft-separation pain (P-GRAFT) at severity ≥4 and say yes at ≥$5K on the ladder; ≥1 paid characterisation | Fewer than 20% of manufacturers see density overlap as a problem |
| H4. Academic licence at $4–10K/yr | [HYP] | ≥6 lab or core interviews with a named budget line (grant or recharge) and a median "expensive but would consider" price ≥$4K; ≥1 paid licence after evaluation | ≥50% say free tools (Dragonfly academic, BoneJ) are enough: switch to per-scan core recharge |
| H5. Enterprise licence at $30–75K/yr | [HYP] | ≥2 CROs confirm ≥10 qualifying studies per year **and** say yes at ≥$30K on the ladder; a procurement path is identified | CROs report in-house deep-learning pipelines, or a pull rate (C-PULL) below 1 in 3 |
| H6. Funnel rates (§4) | [HYP] | Measured from the first 20 qualified conversations, logged in `interview_log_template.csv` | Recalibrate the model inputs and rerun the build script |
| H7. Analyst hours (§2a) | [AE] | Audit-trail timestamps from ≥2 pilots | If above 100 h per study, set the study price floor at 2× measured cost |
| H8. Studies per customer per year | [AE] | ≥8 manufacturer interviews giving counts from their own records ([V] in the coding scheme) | Median below 1 study per year: per-study services cannot carry the business (`MARKET_MODEL_INPUTS.md` §5) |

## 8. Reproduce
```
python business/build_financial_model.py    # workbook + financial_model_outputs.json + revenue_model_sensitivity.json
python business/segment_prospects.py        # prospect_segments.csv
```
To change an assumption, edit `P` in `build_financial_model.py` (or the yellow cells in the workbook, though only the build script regenerates the JSON). Then rerun. The script stops with an error if a formula references itself or if LibreOffice's recalculation disagrees with the Python copy of the model.
