# Commercial Terms Requiring Legal Review

> Issue list for an attorney (e.g. a university entrepreneurship legal clinic or startup counsel) **before** any contract, quote or pilot agreement is signed. This is not legal advice. Items are ordered by urgency.

## 0. Blocking prerequisites
1. **Entity formation:** OsteoQuant is not incorporated. Choose an entity type and state, and settle founder equity and IP assignment into the entity. Do not sign customer agreements personally.
2. **University IP and policy [UNR]:** Determine whether the University of Illinois has rights in software, models or know-how developed with university resources, funding, facilities, coursework or employment (including RA/TA roles). Engage the university's technology-transfer office early. Also check conflict-of-interest rules if university labs become customers or collaborators.
3. **Third-party code and model licences:** Audit open-source licences (GPL/AGPL obligations in a hosted service, model-weight licences, dataset licences such as non-commercial training data).
4. **Training-data rights:** Confirm that every image used to train or validate models may be used commercially.

## 1. Master services / terms of service
- Service description and the "research use only; not a medical device; no diagnostic use" positioning [INF: preclinical animal analysis is generally outside device regulation. Confirm.]
- Warranties: performance to the SOW, disclaimer of fitness for regulatory acceptance, and an accurate statement of validation status
- **Limitation of liability:** cap (e.g. fees paid in the prior 12 months), exclusion of consequential damages, carve-outs (confidentiality, data breach, IP indemnity) [HYP to be set by counsel]
- Indemnities: IP infringement (by Provider); customer data rights (by Customer)
- Term, termination for convenience/cause, and refunds for undelivered work
- Governing law and venue; dispute resolution
- Assignment / change of control (relevant if acquired)
- Non-solicitation, publicity and logo-use restrictions (no customer names or logos without written consent)

## 2. Intellectual property
- Customer owns its data and the results/report. Provider owns software, algorithms and improvements
- **Model training on customer data:** default prohibited. Any opt-in needs explicit terms on de-identification, ownership of the trained model, revocation and confidentiality survival
- Feedback licence (suggestions for product improvement)
- Joint publications: authorship, review periods, patent-filing holds
- Algorithm-licensing deals (PRICING_EXPERIMENT M8): field of use, exclusivity, royalties, sublicensing, audit rights, IP warranties (dependent on the university IP outcome)

## 3. Pricing and payment terms [HYP]
- Fixed-fee vs T&M, change orders, out-of-scope rates
- Prepayment/deposit, late fees, taxes (sales tax on SaaS/services varies by state; check nexus)
- Pilot terms: free pilot with no implied commitment; discount-claw-back clauses (avoid unless counsel advises)
- Subscription: auto-renewal and notice (some states regulate auto-renewal), price-change notice, seat definitions
- CRO enterprise licence: internal-use vs resale/white-label rights, sponsor pass-through, branding of reports

## 4. Data and quality schedules
- DPA / data-handling schedule (see `DPA_ISSUES_CHECKLIST.md`)
- Quality Agreement for GLP-supporting work (see `QUALITY_AGREEMENT_ISSUES.md`)
- Record retention and the escrow/transfer plan if the business ceases

## 5. Regulatory and compliance positioning
- Wording of any claims about GLP, Part 11, validation or accuracy. No claims until the evidence exists (avoid misleading-advertising risk)
- Export controls: likely low risk for image-analysis software, but confirm classification if selling abroad [UNR]
- Anti-kickback/sunshine rules: generally not applicable to preclinical vendors, but confirm before paying referral fees to CROs or physicians [UNR]
- Antitrust: no price coordination with partner vendors or CROs beyond a legitimate reseller agreement

## 6. Insurance
- Professional liability / E&O, cyber liability, general liability, and the limits customers' vendor-qualification processes typically ask for

## 7. Vendor-partnership agreements
- Reseller/referral terms, revenue share, MFN clauses, exclusivity, co-marketing approvals, support split, end-of-partnership data and customer transition
