# Retrospective Pilot Proposal: DefectFill Report (TEMPLATE)

> Template. No pilot has been run, and no performance claims are made. Prices are hypotheses [HYP]. Needs legal review before use.
>
> **Do not send before:** M0 (an entity exists; OTM determination received; insurance; counsel-reviewed NDA, SOW and
> DPA — `investor/FUNDING_STRATEGY.md` §3) **and** Gate 1 (`RELEASE_READINESS.md`). A paid pilot (Option B) also needs
> Gate 2. None of these is met today. Whether any evaluation on customer data may be offered, paid or free, is founder
> decision #18 (`FOUNDER_DECISIONS.md`).

**Prepared for:** [Organization]  **Date:** [ ]  **Valid until:** [ ]

## 1. Purpose
Compare OsteoQuant's DefectFill workflow (automated ROI and three-class segmentation, followed by human review) against the customer's existing analysis on **20–30 retrospective micro-CT scans** from a completed bone-defect study. The aim is to find out whether it saves analyst time while agreeing closely with the customer's own results.

## 2. Offer [HYP]
- **Option A (free) — suspended** until founder decision #18 is made; if reinstated, it carries the same M0, DPA and Gate 1 preconditions as Option B: no fee in exchange for (i) a 45-minute debrief interview and (ii) permission to report **anonymized, aggregate** agreement statistics. Publication requires the customer's prior written approval.
- **Option B (paid pilot):** $[2,500–5,000] [HYP; see `business/REVENUE_MODEL.md`], with no publication rights and full confidentiality. Credited against a follow-on study if one is ordered within [90] days.

## 3. Data requested
- 20–30 reconstructed scans: at least 2 groups (e.g. graft vs empty defect), ideally ≥2 graft types or time points.
- The customer's existing results for the same scans: ROI definition, BV/TV within ROI, residual-graft volume where available, the analysis software and version, and the analyst time spent, actual or estimated.
- Optional: histology/histomorphometry for a subset (≥8 samples) as an external reference.
- Must contain no personal data. Strip sponsor identities if needed.

## 4. Pre-specified endpoints (fixed before unblinding)
| Endpoint | Method | Pre-specified success criterion [HYP] |
|---|---|---|
| Agreement, defect BV/TV | ICC(2,1), two-way random effects, absolute agreement, single measure (Koo & Li 2016 interpretation) | ICC ≥ 0.90 and lower 95% CI ≥ 0.75 |
| Agreement, residual graft volume fraction (only where the advisor marks it supported) | ICC(2,1) vs independent reference where available, else vs customer | ICC ≥ 0.85; if not supported: advisor rationale reported instead |
| Agreement, total mineral volume in defect (only where the advisor marks it supported) | ICC(2,1) on the supported scans; and, if the locked analysis records the value for refused scans, over all scans, labelled as a pilot comparison only | ICC ≥ 0.90 on the supported scans; the all-scan figure is reported descriptively |
| Coverage | Number and share of scans on which the advisor supported each endpoint (residual graft, new bone, total mineral), and the share with no volume endpoint supported | Reported next to every agreement statistic; no success criterion |
| Bias and limits of agreement | Bland–Altman: mean difference, 95% LoA, check for proportional bias (regression of difference on mean) | |bias| ≤ 2 percentage points BV/TV; LoA judged acceptable by the customer's study director *before* unblinding |
| Segmentation overlap (if customer masks available) | Dice coefficient per class | Median Dice ≥ 0.80 for bone, ≥ 0.75 for graft |
| Analyst time saved | Time-stamped hands-on minutes per scan (OsteoQuant reviewer) vs customer-reported minutes | ≥ 50% reduction in hands-on time |
| Turnaround | Data Acceptance → report | [founder decision #14; same figure as the quote and SOW] business days for 30 scans |
| Reviewer correction rate | % of scans needing manual correction; median edited volume | Reported descriptively |

**Interpreting disagreement (cycle-1 review CRO-01).** Agreement with the customer's own analysis is *not* proof
that either method is right: for grafts whose intensity overlaps new bone, threshold workflows are themselves biased
(OsteoQuant Experiments C/C2/S1). The pilot therefore (i) uses agreement only for endpoints OsteoQuant's advisor marks
**supported** and for total mineral volume; (ii) for graft/new-bone endpoints the advisor marks *conditional* or
*not supported*, reports the advisor's reasoning instead of an agreement verdict; and (iii) where possible adds an
**independent reference** agreed before unblinding — histomorphometry on matched sections, a physical-phantom subset
scanned with the study protocol, or a blinded consensus of two analysts using manual delineation. Disagreements are
adjudicated against that reference, not against either party's analysis.

**Coverage and selection effect (cycle-3 review C3-BIZ-02).** Agreement computed only on the scans the advisor
supports describes those scans, not the study: it is a conditional, selected estimate and can look better than
agreement over the whole study would. Coverage is therefore always reported with it. Total mineral is **not** an
always-available endpoint: in the pre-registered held-out simulation S1H3 (SYNTHETIC), new-bone volume was never
supported, total mineral volume supported in 10% of held-out specimens (sharp imaging only), and no volume endpoint
supported for 58% of held-out specimens. A pilot may return few or no supported volume endpoints; that is a valid
outcome, and the debrief explains the reasons per scan.

Statistical notes: n = 20–30 gives a wide CI on the ICC. With n = 25 and a true ICC of 0.90, the 95% CI is roughly ±0.08 [AE]. Report the CI and do not over-claim. Analyse group-wise results as a secondary check (do both methods reach the same group conclusion?).

## 5. Blinding and procedure
1. The customer sends scans **without** their results. OsteoQuant analyses blind to group and to the customer's values.
2. OsteoQuant locks its results with a hash and a timestamp in the audit log, then receives the customer's results.
3. The agreement analysis is run with a pre-registered script. Results go to the customer first.

## 6. Timeline
Week 0: agreements signed (NDA/DPA) → Week 1: data transfer and protocol (ROI, class definitions) → Weeks 2–4: analysis → Week 5: agreement report and debrief.

## 7. What the customer receives
A pilot DefectFill Report for each scan (watermarked "Pilot – not for regulatory use"), an agreement report (ICC, Bland–Altman plots, Dice, time comparison) and a debrief.

## 8. What happens after
There is no obligation. If the pre-specified criteria are met, OsteoQuant may offer a paid SOW at pilot-informed pricing. If the criteria are not met, the results are still shared so both sides learn.

## 9. Agreements needed
Mutual NDA; DPA (or a confirmation that no personal data is involved); data-transfer method; publication/anonymization consent (Option A); IP terms (customer keeps its data and results; OsteoQuant keeps its software and improvements, and **does not train on customer data without explicit written opt-in**).
