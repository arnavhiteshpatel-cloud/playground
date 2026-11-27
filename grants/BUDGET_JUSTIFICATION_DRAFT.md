# Budget Justification: Phase I-Scale DRAFT (illustrative)

**Prepared:** 2026-11-27. **All figures are planning assumptions [HYP] unless marked [V].** Replace them with quotes, offer letters and institutional rates before submission. Arithmetic was checked with a script (rounded to the nearest dollar).

## Verified caps and rules

| Item | Value | Label |
|---|---|---|
| NSF Phase I max | "up to $305,000", "6-18 months", inclusive of indirect costs, the small business fee, TABA and optional I-Corps funding (per NSF 26-511 wording) | [V] |
| NSF voluntary cost share | "Inclusion of voluntary committed cost sharing is prohibited." | [V] |
| NSF indirect | "NSF may give preference to institutions with lower indirect cost rates." | [V] |
| NIH Phase I (NIBIB/NIAMS) | "SBA Guideline" = **$335,937** total (as of Oct 16, 2026; above requires a waiver) | [V] |
| NIH Phase I period | "normally may not exceed 6 months" | [V] |
| NIH SBIR work split | Phase I ≥67% by the SBC | [V] |
| NIH STTR work split | SBC ≥40%, RI ≥30% | [V] |
| NSF STTR split | ≥30% of budget to the RI; SBC ≥40% | [V] |
| Small-business fee | Up to 7% of total costs (customary) | [CC] confirm in the NOFO |
| TABA (Technical and Business Assistance) | Up to $6,500 for Phase I (customary). At NIH, whether it is inside or outside the guideline is [UNR] | [CC] |
| Company indirect rate | No negotiated rate. 30% of company direct is assumed. Confirm allowable approaches (e.g., NIH guidance for SBCs without a negotiated rate) | [UNR] |
| UIUC F&A rate (subaward) | 58.7% MTDC is assumed for illustration only | [UNR] confirm with UIUC Sponsored Programs |
| Beckman Versa hourly rate | $110/h is assumed. The fee page lists categories but no figures were retrievable | [UNR] |

---

## Scenario A: NSF SBIR Phase I (12 months; founder or hired PI ≥51% employed)

| Category | Basis (assumption) | Amount ($) |
|---|---|---|
| **A. Senior personnel:** PI | $75,000/yr × 75% effort × 12 mo. **[HYP]** salary; the PI must be >50% *employed* by the company [V], and effort ≥1 month per 6 months [V] | 56,250 |
| **B. Other personnel:** ML/imaging engineer | $100,000/yr × 50% × 12 mo **[HYP]** | 50,000 |
| **C. Fringe** | 25% of salaries **[HYP]** (payroll taxes + benefits) | 26,563 |
| **D. Equipment** | None ≥$5,000 | 0 |
| **E. Travel** | 1 domestic conference (e.g., ORS Annual Meeting) for validation dissemination **[HYP]** | 2,500 |
| **G1. Materials & supplies** | Phantom matrices, mineral surrogates, graft granules (several materials), fabrication consumables **[HYP]**: 9,000. Workstation <$5k: 4,500 | 13,500 |
| **G2. Publication / dissemination** | Open benchmark hosting, data repository | 1,500 |
| **G3. Consultant services** | Faculty MSK/imaging advisor 40 h × $150/h: 6,000. Expert micro-CT readers 3 × 35 specimens × 1.5 h × $75/h: 11,813 (time per specimen is itself a [PENDING RESULT]) | 17,813 |
| **G4. Computer services** | Cloud GPU training and inference | 10,000 |
| **G5. Facility fees** | Beckman Zeiss Xradia 630 Versa, 120 instrument-hours × $110/h **[UNR rate]** | 13,200 |
| **G6. Other** | Software licenses, QMS / document control tooling | 3,000 |
| **Total direct** | | **194,326** |
| **Indirect** | 30% of direct **[HYP; UNR]** | 58,298 |
| **Subtotal** | | 252,624 |
| **Fee** | 7% **[CC]** | 17,684 |
| **TABA** | **[CC]** | 6,500 |
| **Grand total** | Under the $305,000 cap; ~$28k headroom for optional I-Corps funding or rate corrections | **276,807** |

## Scenario B: NIH STTR Phase I (faculty PD/PI at UIUC; 12 months **if** NIBIB allows. Otherwise compress to 6 months and scale.)

| Category | Basis (assumption) | Amount ($) |
|---|---|---|
| Company personnel | Company PD/PI or lead: $75,000 × 75%: 56,250. Engineer $100,000 × 50%: 50,000 | 106,250 |
| Fringe | 25% | 26,563 |
| Consultants | Expert readers (as above) | 11,813 |
| Compute / workstation / software / travel | 7,000 + 4,500 + 2,500 + 2,500 | 16,500 |
| **Company direct** | | **161,126** |
| Company indirect | 30% **[HYP; UNR]** | 48,338 |
| **Subaward: UIUC (research institution)** | Faculty PD/PI ≥10% effort [V rule] (salary + fringe), graduate/staff support for phantom fabrication and scanning, Beckman instrument time at the internal rate, phantom materials. Direct 60,000 **[HYP]** | 60,000 |
| Subaward F&A | 58.7% **[UNR]** | 35,220 |
| Subtotal | | 304,684 |
| Fee | 7% **[CC]** | 21,328 |
| TABA | **[CC/UNR placement]** | 6,500 |
| **Grand total** | Under the $335,937 guideline | **332,512** |

**Work-split check:**
- RI share of total cost before fee: 31.3%, which meets ≥30% [V rule].
- SBC share: 68.7%, which meets ≥40%.
- NIH measures the split by research effort; confirm the computation method [UNR].

---

## Justification narrative (template text; edit assumptions)

- **Personnel:** The PI leads all aims and devotes [X]% effort, with primary employment at [company] for the full award [V rule]. The engineer implements the forward-model simulation, model training, uncertainty calibration and the audit module.
- **Consultants:**
  - The faculty advisor provides bone-biology and study-design guidance.
  - Expert readers perform blinded manual analyses for Aim 3. Hourly rates reflect [market/academic] rates [HYP].
  - Letters of commitment are required (see LETTER_OF_SUPPORT_TEMPLATES.md).
- **Facility fees:** The Beckman Institute Microscopy Suite charges usage rates "determined through analysis by Government Costing, University of Illinois" [V]. Rate categories include internal, internal with F&A and external-with-F&A for businesses under a working contract [V]. **The company will likely pay the external rate unless the work is run through an STTR subaward** [INF]. Hours are [N phantoms × voxel sizes × repeats × hours/scan], plus training.
- **Materials:** Phantom materials are itemized by material, lot and supplier quote [PLACEHOLDER].
- **Compute:** GPU-hours estimate = [experiments × hours] × [$/GPU-hour quote] [PLACEHOLDER].
- **Travel:** Present validation results to the orthopaedic research community (ORS).
- **No animal costs:** Phase I uses phantoms and existing de-identified scans only [INF].

## Assumptions to replace (checklist)
- [ ] Salaries per offer letters or market data; PI employment documentation
- [ ] Fringe rate (payroll provider quote)
- [ ] Company indirect approach (NSF/NIH guidance; accountant)
- [ ] Beckman Versa rates (external and internal) and training fees: written quote
- [ ] UIUC subaward budget and F&A from Sponsored Programs (STTR)
- [ ] Reader count, time per specimen and rate (signed letters)
- [ ] Material quotes; cloud compute quote
- [ ] Fee and TABA rules in the final NOFO
