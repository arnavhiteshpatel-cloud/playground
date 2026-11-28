# WS04-014 — Stage F Adversarial Review (batch F4)

**Concept reviewed:** managed IT plus a HIPAA Security Rule compliance layer for independent dental practices on Chicago's North Side. The vet segment is secondary.

**Material reviewed:**
- Stage C memo and Stage D deep dive;
- Stage E playbook and materials;
- `08_financial_models/WS04-014_assumptions.json` and `_results.json`;
- the prospect CSV (35 rows) and the supplier CSV (11 rows);
- `sources_E_WS04-014.jsonl` and the cited C6/DD/WS04 records.

**Reviewer:** independent; I did not write any of this. **Access date:** 2026-11-28.

**Re-runs:** all made with `tools/fin_engine.py`. Scripts are in `/tmp/claude-0/atlas_scratch/F4/` (`base.py`, `ws04.py`, `ws04b.py`). The finalist's files were not modified. New sources are F4-S001…S006 and F4-S011 in `07_review/sources_F4.jsonl`.

---

## 1. Verdict: **SURVIVES WITH MAJOR REVISIONS**

The good points are real and I confirm them:
- It is still the cheapest finalist to test (under $400).
- Revenue is prepaid and recurring.
- The technical work fits the founder.
- The playbook is unusually candid about its conservative case.

But the base case rests on three inputs that independent evidence does not support:

1. **Price.** A $690/month blended price plus $1,000 onboarding assumes a premium over a remote dental specialist (Siotek). Siotek is *already marketing to Chicagoland* and says it coordinates on-site technicians in Chicago [D, F4-S002]. It charges $399 for about 10 workstations and **charges nothing for onboarding**, which per its pricing page includes "discovery, documentation, agent deployment, and risk assessment" [B, F4-S003].
2. **Technician cost.** The cost is based on the Illinois *help-desk* median ($59,860). The job described is a solo field engineer who runs servers, firewalls, EDR, backup and imaging chains. The comparable Chicago figure is the network-support median of $73,340 [C, F4-S004].
3. **Founder time.** Founder labour is free until 14 practices. That is a modelling convention, but it makes the "breakeven at 4.7 practices" a founder-job breakeven, not a business breakeven.

**Corrected base.** I changed only two inputs and kept every funnel rate as written (§4):
- technician cost $7,500/month loaded;
- ARPC $650, onboarding $500.

| Measure | Stage E base | Corrected base | Corrected base, technician hired at 18 practices instead of 14 |
|---|---|---|---|
| Year-3 operating profit | $64,047 | **$37,459** | $37,459 |
| Year-5 operating profit | $128,878 | **$94,859** | $111,741 |
| Peak funding with draw | $42,408 | **$69,661** | $38,761 |
| Peak funding with no draw | $21,831 | $23,403 | $23,403 |
| 10-year deployable | $386,875 | **$216,469** | $298,141 |

**Corrected conservative:** unchanged at about $12k in year 3. A founder who never hires reaches about **$57k in year 5**, which is a job.

**Bottom line:**
- This is a **$35–50k year-3 / $95–110k year-5 local company** with very low capital at risk. It is not a $64k / $129k one.
- It stays on the list because the test is cheap and decisive.
- The price ceiling, the free-onboarding competitor already in Chicago, and the liability tail together make it a weaker first holding-company asset than Stage E says.

---

## 2. Factual errors found

| # | Claim | What the source actually says | Correction |
|---|---|---|---|
| F1 | Technician cost of $37.40/h, $6,500/month loaded, from the "IL computer user support specialist median $59,860" [C6-S026] | The O*NET figure is verified: IL $59,860, Chicago $60,730. But it is the **help-desk** occupation. Chicago **computer network support specialists**: median $73,340, 75th percentile $88,550 [C, F4-S004]. A technician who covers 28 practices alone (firewalls, servers, EDR, imaging bridges, after-hours) is the second role. | The source is applied to the wrong occupation. Loaded cost should be **$7,500 base** (about $69k × 1.3) and $8,000 conservative. Effect alone: year 3 $64.0k → $46.2k (at $7,900). |
| F2 | "Siotek … HIPAA assessment only in a custom tier" (Stages C/D), so "compliance work that rivals sell only in custom tiers" justifies the premium | The pricing page today (verified) has Essentials "everything HIPAA-essential". Onboarding is "no charge" and includes a "risk assessment". The Larger Practice tier adds a "HIPAA risk assessment and remediation roadmap" [B, F4-S003]. Darkhorse includes "full HIPAA compliance" in both tiers [B, E-WS04014-S005, verified]. | The compliance layer is **not** a differentiator against the remote specialists; they bundle a version of it. The paid-wedge offer ($750–1,500) competes with free onboarding risk assessments, $499/yr software and the free HHS tool. |
| F3 | Siotek and Darkhorse are framed as "remote rivals" that the on-site SLA beats locally | Darkhorse lists no Chicago service area (verified). **Siotek has a Chicago landing page.** It claims Chicagoland coverage, Dentrix → Ascend migrations of Illinois practices, and coordinated on-site technicians in Chicago [D, F4-S002]. | The main price anchor is an *active local competitor* that also offers coordinated on-site work, not just a remote benchmark. Entry 4 → 3. |
| F4 | "Local providers listed in a Chicago dental-IT directory … market range $500–2,000/month" [D, DD-S019], used as an ARPC anchor | Verified page, but it is a `pages.dev` directory with no author. It says listings are not independently verified, yet also claims every provider "has been vetted", which is contradictory. | Keep at D/weak. It must not anchor the base price. |
| F5 | Tool cost: EDR at $7/endpoint as "MSP cost (retail $7–12)" | Siotek's guide gives $7–12 per workstation as the price the *practice* pays [D, E-WS04014-S006, verified]. MSP wholesale cost is MISSING. | Not an error against the model: wholesale is plausibly *below* $7. But the guide also prices HIPAA backup at $150–400/month, against the model's $13.90 B2 line (local NAS/BDR capex not in COGS). The two roughly offset. Gross margin 0.79 is acceptable as E. |
| F6 | The Chicago low-voltage licence rule [A, E-WS04014-S016] | I could not re-verify it (chicago.gov returned 403 today). | Not falsified; left as cited. |

**Citations that checked out exactly:**
- Siotek $399, add-ons and terms;
- Darkhorse $422/$749 at 15 workstations;
- Unified Agenda "Long-Term Actions", final action 07/2027;
- Insureon IT-consultant medians (E&O $75, cyber $128, GL $31);
- the Backblaze BAA only for covered entities;
- the Hunton note on the $103k Illinois OCR settlement;
- Syncro $129/$179, AI free through January 2027;
- O*NET $59,860.

---

## 3. Unsupported or over-stated claims

| Claim | Warranted level |
|---|---|
| "The defensible range for a local on-site provider is about $600–900" | **E.** The only local price evidence is the weak directory (D). With Siotek in Chicago at $399 + add-ons and free onboarding, $600–650 is the defensible newcomer base until LOIs prove more. |
| Proposal → win 25% and 12 qualified owner/office-manager conversations a month from walk-ins | **E**, and optimistic for an unknown vendor asking for admin rights to patient-data systems. The practices that can switch are those whose 12-month terms are expiring. Kept as base here to avoid stacking, but at 20% year 3 falls to about $4k (re-run). |
| "A T2 that converts to T1 is acquisition that pays for itself"; 10% of walk-ins buy a $750–1,500 risk analysis | **E.** The wedge faces free onboarding assessments, $499/yr software, and office managers who seldom buy from walk-ins. Keep it as the test; do not treat it as likely. |
| 6 technician hours per practice per month | **D/E, plausible as steady state.** Vendor-sourced benchmarks are 200–350 endpoints per technician, with no neutral standard [D, F4-S011]. The model's ~300 endpoints per technician sits inside that range. Onboarding months and imaging-heavy offices will run higher, and onboarding hours are not in the model. |
| Insurance $550/month | **D/E, reasonable** for $1M limits. MSP-specific premiums are MISSING: Insureon gives only tech-company averages [D, F4-S005], and broker guides give about $1–10k/yr for cyber. The *premium* is not the problem; uninsured *contractual* exposure under BAAs and indemnities is (§7). |
| Year-10 EV $645k at 3.5× | **D**, and it requires the base case to hold. On the corrected base, year-10 operating profit is about $136k, so EV is about $475k. |

---

## 4. Financial model audit

**Reproduction.** The engine reproduces Stage E exactly:
- conservative $12,175 / −$38,018 / $307,555;
- base $64,047 / $128,878 / $42,408 ($21,831 with no draw);
- optimistic $268,828.

**Top drivers.** Each was challenged; all are re-runs on base with only that driver changed.

| Driver | Stage E | Independent evidence | Proposed base / conservative | Year-3 effect alone |
|---|---|---|---|---|
| ARPC | $690 | Siotek $399 + EDR/email add-ons ≈ $500–600; active in Chicago; free onboarding [B, F4-S003; D, F4-S002] | **$650** / $540 | $64.0k → $47.3k (at $625) |
| Technician cost | $6,500/month | Chicago network-support median $73,340 [C, F4-S004] | **$7,500** / $8,000 | $64.0k → $46.2k (at $7,900) |
| Onboarding revenue | $1,000 | Siotek charges $0 [B, F4-S003] | **$500** / $300 | $64.0k → $60.5k |
| Proposal → win | 25% | No evidence (E). Newcomer trust barrier | Keep 25%; flag 20% as a live downside | $64.0k → $27.6k at 20% |
| Hours per practice | 6 | Benchmarks weak (D) | Keep 6; at 8 hours (founder 11, technician 21 practices), year 5 is $61k and peak $112k | Year 5 −$34k |

**Combined corrected base** (technician $7,500, ARPC $650, onboarding $500):

| | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|
| Operating profit | −$19.4k | $12.4k | **$37.5k** | $105.0k | $94.9k |

- Breakeven in month 11.
- First $5k/month in month 34; first $10k/month in month 43.
- Cumulative payback in month 50.
- Peak funding $69.7k with the $4k draw, $23.4k without.
- 10-year deployable $216k.

**Hiring at 18 practices instead of 14** reduces peak funding to $38.8k and raises year 5 to $111.7k. I recommend this as a model change. It is the single most valuable operating rule in this plan.

**Working capital.** Negative working capital (prepaid) is correct and is the business's best feature.
- One caution: hardware projects at 50% deposit with assumed net-30 distributor terms. A new account will likely pay by card or prepay (the playbook notes this as MISSING).
- The exposure is small (about $4–8k).

**Founder draw logic.**
- The base case cannot carry the $4k/month stipend until about month 17.
- On the corrected base, monthly retained cash is negative in most months from 20 to 31. Cumulative retained cash bottoms at −$69.7k in month 31, and about $46k of that is the stipend itself (peak $69.7k with the draw against $23.4k without). The founder is in effect funding his or her own salary.
- A tech-background founder's market salary is likely above $48k a year (E), so the opportunity cost is large through year 3.

---

## 5. Customer acquisition challenge

**What incumbents' sales motions look like:**
- **Siotek:** a Chicago landing page, published flat pricing, free switching, and messages about migrating Dentrix to Ascend [F4-S002, F4-S003].
- **Henry Schein One / TechCentral:** sells IT to the installed Dentrix base and offers "Omnicore", a monthly hardware-plus-setup-plus-lifecycle bundle aimed at new offices and practice acquisitions [B, F4-S006]. Those are exactly the "triggered" buyers the playbook targets through brokers and dealers.
- **Equipment-dealer service reps:** the playbook's channel #2, but they work for distributors that sell competing IT.

**What the first 10 customers really require.** Ten owner-dentists must hand an unknown person domain-admin rights to their patient-data systems. In practice that needs:
- (a) insurance certificates and a signed BAA before any access;
- (b) at least one local reference, which the founder does not have at client #1;
- (c) a switching moment: an outage, a contract end, a new office or a practice purchase;
- (d) a price no more than about 10–15% above Siotek's all-in.

At 12 conversations a month, 35% to proposal and 25% to win, the base produces about 1 win a month. My judgement (E) is that the first three clients take 4–6 months, not the modelled 2–3. Wins come mostly via referral partners (practice brokers, dental CPAs, independent equipment technicians), not walk-ins.

**Recommended early-warning metric:** referral-sourced proposals as a share of all proposals by month 4. If walk-ins produce under 1 proposal per 10 visits, the base funnel is already falsified.

---

## 6. Supplier and partner accessibility challenge

**Most likely to refuse or impose terms:**
1. **Cyber/E&O carriers.** They can decline a zero-history MSP with healthcare clients, or require strict controls on the RMM (MFA, privileged-access management, EDR on the MSP's own devices). Premium is likely obtainable, but exclusions matter: contractual liability, ransomware originating from the MSP's tools.
2. **EDR/MDR and email-security MSP programmes.** Minimum commitments and annual terms are MISSING. Some vendors also require distributor accounts.
3. **Backup with a BAA.** Backblaze signs only with covered entities (verified), so practice-owned accounts are needed. That is workable but clumsy.
4. **Dental equipment dealers.** Henry Schein and Patterson both sell IT, so their reps are channel competitors, not neutral referrers.

**Easy to access:** Syncro, B2, the HHS SRA Tool, M365 retail.

---

## 7. Legal and regulatory challenge

1. **Business-associate liability is the real tail risk, and it is under-weighted.**
   - The 2019 PerCSoft/DDS Safe incident encrypted files at about **400 dental practices** through one service provider [C, F4-S001].
   - An MSP's RMM is a single point of compromise for every client. The model has no scenario in which all clients are hit at once.
   - BAAs typically require indemnification and breach-cost reimbursement. A $1M tech E&O + cyber limit can be exhausted by one multi-practice event.
   - **Required before launch:** an attorney-drafted MSA with a limitation-of-liability cap tied to fees, carve-outs negotiated, and an insurer confirming that contractual liability under BAAs is covered.
2. **Chicago PPLTT (15%)** on any taxable component of the managed fee could add up to 15% to a Chicago client's bill. Remote competitors may not collect it. The playbook flags this correctly; it needs tax counsel *before* pricing.
3. **Illinois PIPA and BIPA** were not re-verified (ILGA unavailable). Treat as open.
4. **The "insurance MFA attestation readiness check" (offer b).** The founder must not complete or sign a client's insurance application. The materials say this implicitly; it should be explicit, because a misrepresentation claim like the cited Travelers rescission case [C, E-WS04014-S019] could pull the MSP in.

---

## 8. Competitive response

- **Siotek** can simply add Chicago on-site partners or a local technician. Its free onboarding already neutralises the $1,000 fee.
- **Henry Schein One** bundles IT into software and hardware relationships. Cloud migration (Dentrix Ascend, which Siotek also sells) steadily removes the server work that justifies on-site premiums.
- **Local one-person "dental IT guys"** compete on relationship and price.

**Underestimated incumbent advantage:** the *references*. An owner-dentist's switching decision is risk-averse; "who else do you look after?" is the question a newcomer cannot answer for months.

---

## 9. Founder execution and delegation realism

- **Can the founder personally deliver MSP-grade security?**
  - A tech/research background can learn RMM, EDR, M365 hardening and backup in weeks. Dental imaging chains (sensors, bridges, pan/CBCT) and practice-management server quirks take longer.
  - The larger gap is **operational security of the MSP itself**: privileged-access hygiene, RMM lock-down, incident response. One mistake there harms every client.
  - Plausible, but it requires a disciplined first 90 days, ideally with a paid mentor or a vendor-run SOC (MDR) doing 24/7 detection.
- **Solo SLA.** A same-day on-site promise from one person is not credible beyond about 8–10 clients without the backup-technician arrangement. The playbook recognises this.
- **Delegation.** Technician roles are standard. But L3 engineering and security judgement stay with the founder until the senior-engineer hire at 70 practices, which is beyond year 5 in base. Delegation 7 → 6.

---

## 10. Pre-mortem

| # | Most plausible failure | Early indicator | Cheapest preventive test |
|---|---|---|---|
| 1 | **Price collapse to parity.** Owners compare against Siotek's $399 plus free onboarding. LOIs come in at $500–550, and the business becomes a founder job at about $40–55k a year. | Two or more of the first five proposals countered with a Siotek quote | Experiment 4 (price test), with Siotek's page shown side by side; walk away below $600 |
| 2 | **A client incident with contractual liability beyond the policy**, for example ransomware via an unhardened RMM or a missed restore | Any client without a verified restore after 30 days; RMM without phishing-resistant MFA | Insurer and attorney review of the MSA/BAA *before* the first monthly contract; MDR vendor for the 24/7 SOC |
| 3 | **Slow trust formation.** Fewer than 4 clients by month 9; the founder draws a stipend the business cannot fund. | Walk-ins yield <1 proposal per 10 visits | Run the 5 referral-partner conversations first (experiment 1). If none offers an introduction, stop before spending on insurance. |

---

## 11. Corrected scores

| Criterion | Stage E | **F4** | Reason |
|---|---|---|---|
| fcf | 4 | **3** | Corrected base year 3 $37k, year 5 $95–112k |
| roic | 7 | **5** | Peak funding $39–70k with draw; year-3 return on that is about 55–95% |
| access | 5 | **4** | A trust wall on admin access to patient-data systems; 12-month terms; no references |
| scale | 5 | **4** | Pod economics thinner at the corrected price and technician cost |
| resilience | 7 | **6** | Essential recurring demand, but cloud practice management and DSO drift erode the on-site premium |
| entry | 4 | **3** | Siotek is active in Chicago with free onboarding and bundled HIPAA; Henry Schein One bundles |
| delegation | 7 | **6** | L3 and security judgement stay with the founder through year 5 |
| cash | 8 | **8** | Prepaid recurring revenue, confirmed |
| feasibility | 8 | **7** | Business-associate liability tail, PPLTT uncertainty, insurer controls |
| ai | 5 | **5** | — |

- **Raw composite:** 4.63. Evidence D (k = 0.70) gives an **evidence-adjusted score of 4.74** (Stage E: 5.48).
- **Gates:** G4 borderline. Corrected base year 5 is $95–112k, so it reaches $100k only with density-based hiring. G7: WARN until the first technician hire.

**Bottom line.** WS04-014 remains the cheapest, lowest-capital finalist, with genuinely prepaid recurring revenue. That is why it survives.

But its Stage E base assumed a local price premium that the strongest specialist competitor is already contesting in Chicago, with free onboarding and bundled HIPAA items. It also costed a field engineer at help-desk wages. Corrected, it is roughly a $37k year-3 / $95–110k year-5 business that the founder carries as technician-salesperson for about two years. It has a contractual-liability tail that a single RMM compromise could realise.

**Recommended revisions:**
- re-base ARPC at $650 and technician cost at $7,500;
- hire at 18 practices, not 14;
- get insurer and attorney sign-off on BAA liability *before* the first monthly contract;
- make the referral-partner test the first kill gate.

**Preserved disagreement.** If experiment 4 produces two or more LOIs at $690+ and experiment 1 yields real introductions, the Stage E base (~$64k year 3) is defensible. The author's case for a local on-site premium is not unreasonable; it is simply unproven, and the nearest competitor now argues the opposite.
