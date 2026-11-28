# WS04-014 — Draft commercial materials: managed IT + HIPAA security compliance for independent dental and vet practices

> **DRAFT — not sent; requires founder review.** Nothing here has been sent, submitted, posted or used to contact anyone.
>
> **Placeholders:** [Founder Name], [Company Name], [phone], [email] and [website] are placeholders. Do not invent credentials, client names, testimonials or certifications.
>
> **Never say:**
> - "HIPAA certified". There is no official HIPAA certification.
> - "guaranteed compliance".
>
> **Fact-check before use.** Every factual claim below is cited to `06_playbooks/WS04-014_playbook.md` sources. Re-check them before use.
>
> **Vets are not HIPAA covered entities** [A, E-WS04014-S003]. Use the vet variants for vet hospitals.

---

## 1. Supplier / partner inquiry templates
**DRAFT — not sent; requires founder review.**

### 1a. Security-tool vendor (EDR/MDR, email security, DNS filtering, backup)
Subject: MSP programme terms for a new healthcare-focused MSP (small starting volume)

Hello [Vendor] partner team,

I am starting [Company Name], a managed IT provider for independent dental and veterinary practices in Chicago. I expect 3–10 client sites (30–120 endpoints) in the first year. Before choosing a stack, I would like to understand your terms:

1. Per-endpoint (or per-mailbox) MSP cost at 10, 50 and 150 endpoints. Is there a monthly minimum or commitment?
2. Monthly billing, or annual only? Can I add and remove endpoints mid-term?
3. Will you sign a Business Associate Agreement with an MSP acting as a subcontractor business associate? Please send your standard BAA.
4. Is the managed detection/SOC service included, and what is the escalation path to me after hours?
5. Data location, retention and immutability options (for backup products).
6. Trial or not-for-resale licences for a lab environment.
7. Any partner requirements: training, certifications or minimum revenue.

Thank you,
[Founder Name], [Company Name], [email]

### 1b. Backblaze (B2) — BAA route
Subject: B2 BAA for dental-practice backups administered by an MSP

Hello,

Your compliance page says Backblaze can provide a BAA to business customers who are HIPAA covered entities. I administer IT for dental practices. Two questions:

(1) Can a covered-entity dental practice hold its own B2 account, sign your BAA directly, and grant my firm administrative access?
(2) Alternatively, will Backblaze sign a subcontractor BAA with an MSP that is itself a business associate?

Please also confirm which B2 features (object lock, application keys) are covered.

[Founder Name], [Company Name]

### 1c. Insurance broker (tech E&O + cyber + GL)
Subject: Quote request — tech E&O + cyber + GL for a start-up MSP serving dental practices

Hello [Broker],

I am forming [Company Name], an Illinois LLC that will provide managed IT and HIPAA Security Rule documentation for independent dental and veterinary practices. Expected year-1 revenue is $25–80k, with 1 owner and 0 employees, rising to 1 technician in year 2. I will have administrative access to client networks through an RMM tool and will sign BAAs.

Please quote:
- tech E&O + cyber at $1M/$1M and $2M/$2M;
- GL at $1M/$2M;
- options for contractual liability under client BAAs.

What controls do underwriters require of me as an MSP? For example: MFA on RMM and all admin access, EDR on my own devices, backups, and an incident-response plan. Do any carriers exclude ransomware at client sites caused by an MSP's tools?

[Founder Name]

### 1d. Licensed low-voltage cabling contractor (Chicago)
Subject: Subcontract cabling for dental-office IT projects

Hello [Contractor],

I run IT projects for dental and vet offices on Chicago's North Side. I need a licensed low-voltage contractor for occasional jobs: 4–20 drops, rack/patch panel, Wi-Fi AP runs, sometimes a new-office build-out. Could you share:
- your City of Chicago licence type;
- typical per-drop pricing and minimum job size;
- lead time;
- permit handling;
- whether you work as a subcontractor with a certificate of insurance naming my company?

[Founder Name]

---

## 2. Customer discovery interview questionnaire
**DRAFT — not sent; requires founder review.**

**Purpose:** learn past behaviour and real spend. Do **not** pitch during the interview.
**Format:** 20–25 minutes with an office manager or owner.
**Ground rules:**
- Ask about the last time something happened, not about hypotheticals.
- Record exact numbers where offered. Never press for patient information.

**Opening:** "I'm researching how independent dental [vet] practices handle IT and security. Could I ask about how things work here today? I'm not selling anything in this conversation."

**A. Set-up (facts)**
1. How many people work here, and how many computers or workstations do you use day to day?
2. Which practice-management and imaging software do you use? Is it on a server in the office or in the cloud?
3. Who handles your IT today: someone on staff, an outside person or company, your equipment dealer, or "whoever is around"?

**B. Last incident (past behaviour)**
4. Tell me about the last time the computers or imaging stopped you from seeing patients. When was it? What happened next? How long until it was fixed?
5. Roughly what did that cost? (Lost appointments, overtime, the invoice.)
6. Who did you call first? Why them?

**C. Spend (past behaviour)**
7. What did you pay for IT support in the last 12 months? Was it a monthly fee, per-visit or hourly invoices, or both? (Ask for a range if exact figures are unknown.)
8. In the last 3 years, what larger IT purchases have you made (server, workstations, firewall, new office)? Who recommended and installed them?
9. Is there a contract with your current IT provider? When does it end? What notice does it need?

**D. Compliance and insurance (past behaviour)**
10. *(Dental)* When was your last HIPAA security risk analysis done, and by whom? Could you find the document if asked?
11. *(All)* Do you carry cyber insurance? Who completed the application, and who signed it?
12. *(All)* When the application asked about multi-factor authentication or backups, how did you decide what to answer?
13. *(All)* When was your backup last restored as a test, as opposed to just "running"?

**E. Buying process**
14. If you changed IT providers, who would decide? Who else would weigh in?
15. The last time you hired a vendor like this, how did you find and choose them?

**F. Close**
16. Is there anything about IT or security here that worries you that I haven't asked about?
17. May I follow up with a short summary of what I'm hearing from practices? Is there anyone else you think I should talk to?

**After each interview, log:**
- Workstation count, PM/imaging, server vs cloud.
- Current provider type and spend.
- Contract end date.
- Last risk-analysis date (dental).
- Cyber application signer.
- Last restore test.
- Decision-maker.
- Incident cost.

---

## 3. Outreach message variants
**DRAFT — not sent; requires founder review.**

### 3a. Email (to an office manager, where an email address is publicly listed)
Subject: Who signs your cyber-insurance security answers?

Hi [Name],

I'm [Founder Name], and I'm setting up [Company Name], a local IT and security service for independent dental practices on the North Side.

Many cyber-insurance applications now ask whether multi-factor authentication protects email, remote access, and every admin login to servers, firewalls and backups, including logins used by outside IT providers. Some forms ask whether the signer was helped by "the person in charge of IT security." Separately, HIPAA already requires a documented security risk analysis. OCR has been settling cases specifically over missing or inadequate ones, including with a small Illinois provider this year.

I offer a fixed-price review that checks each of those insurance questions and produces a written risk analysis and fix list. It is done on-site in about two visits. Would a 15-minute conversation next week be useful?

[Founder Name] · [Company Name] · [phone]

*(Vet version: replace the HIPAA sentence with "and to keep client and card data safe".)*

**Sources:**
- Travelers MFA supplement [B, E-WS04014-S007].
- 45 CFR 164.308 [A, E-WS04014-S020].
- OCR Risk Analysis Initiative / Illinois settlement [C, E-WS04014-S008, S009].

### 3b. Call opener (for a phone listed publicly as the practice number)
"Hi, this is [Founder Name] with [Company Name], a local IT service for dental offices near you. I'm not calling about patients. Is the office manager available for 30 seconds, or is there a better time?

*[If yes]* Thanks. Quick question: when you renewed your cyber insurance, who filled in the security questions about multi-factor authentication and backups? *[Listen.]*

The reason I ask: I do a fixed-price on-site check that walks through those exact questions and the HIPAA risk-analysis paperwork, then leaves you a written list. Would it be worth 15 minutes in person this week or next?"

*If the answer is "our IT guy handles it":* "Great. Do you know when your backup was last test-restored? If that's covered, I won't take your time." *(Then log the answer and move on.)*

### 3c. In-person (walk-in at the front desk; quiet times only, never in front of patients)
"Hi, I'm [Founder Name]. I run a small IT and security service for dental offices in [neighbourhood]. I know you're busy, so I'll leave this one page.

It describes a fixed-price check of the security questions cyber insurers ask, plus the HIPAA risk analysis, done on-site. Who would be the right person to look at it? Is there a good time for a 15-minute chat with them?"

*Leave:* the one-page offer sheet (§6) and a business card. *Log:* the practice, who you spoke with, any DSO branding, and the follow-up date.

---

## 4. Sales call script with qualification questions
**DRAFT — not sent; requires founder review.**

**Goal:** decide in 20–30 minutes whether a paid review or a monthly proposal makes sense. The founder should be willing to disqualify.

**1. Agenda (1 minute).** "I'd like to understand how IT runs here today. If it makes sense, I'll explain what I do and the price. If it doesn't fit, I'll say so."

**2. Qualification: ask and record.**
- *Fit:* number of workstations; server or cloud PM; imaging hardware; one location or more; DSO-affiliated or planning a sale?
- *Pain:* last outage and its cost; slow systems; unsupported Windows; backup restore last tested?
- *Compliance:* *(dental)* date of last risk analysis and where it is; *(all)* cyber-insurance carrier, renewal month, who signed the security answers.
- *Spend & contract:* last 12 months of IT spend; contract end date and notice.
- *Decision:* who signs (usually the owner), who influences (office manager), and the budget process.
- *Timing:* any trigger in the next 6 months (new office, equipment purchase, insurance renewal, associate buy-in, sale).

**Disqualify (politely):**
- DSO-managed IT.
- Planned sale within 6 months, unless the work is a buyer-side diligence project.
- Fewer than 3 workstations, unless the job is a stand-alone review.
- Outside the radius.
- Unwilling to adopt MFA.

**3. Present (5 minutes), only if qualified:**
- **Step 1: paid review.** Dental risk analysis + policy set, $1,500 ($750 introductory for the first five practices); or an insurance readiness check, $350. You keep the report whether or not you hire us.
- **Step 2, optional: monthly service.**
  - Dental: $60 per workstation per month, minimum $450, plus $100 for the HIPAA layer.
  - Vet: $55 per workstation plus $60 for the insurance-readiness layer.
  - Includes monitoring, patching, managed EDR, email and DNS security, tested backups, same-day on-site within the area, and vendor coordination.
  - Projects and hardware are quoted separately.
  - 12-month initial term, then month-to-month with 30 days' notice.
- **Be honest about comparison.** Remote dental IT firms publish lower list prices. Some publish $399/month, but with security tools as add-ons, and some publish per-workstation rates. What you pay extra for here is someone who shows up the same day and does the compliance work with you.

**4. Objections:**

| Objection | Response |
|---|---|
| "Too expensive vs. $399" | "Fair. Let's price the like-for-like: their base plus EDR and email security add-ons, and on-site visits beyond four a year. If it still comes out cheaper and you rarely need on-site help, they may be the better fit." |
| "Our IT guy handles it" | "Good. Two quick checks: when was the last test restore, and is MFA on every admin login, including his? If both are yes, you're in good shape." |
| "We did HIPAA training" | "Training is one piece. The risk analysis is a separate required document. Could you find yours if asked?" |

**5. Close.** Ask for the paid review with a 50% deposit and a signed BAA, *or* agree a follow-up date tied to the contract end or insurance renewal. Log the outcome in the KPI sheet the same day.

---

## 5. RFQ / quote templates
**DRAFT — not sent; requires founder review.**

### 5a. Supplier RFQ (security stack / backup / insurance), table to send or fill

| Item | Qty assumption | Unit | Price @10 / 50 / 150 | Minimum term | Monthly billing? | BAA signed? | Notes |
|---|---|---|---|---|---|---|---|
| Managed EDR/MDR | 11 endpoints per practice | endpoint/mo | | | | | SOC escalation path |
| Email security | 8 mailboxes per practice | mailbox/mo | | | | | |
| DNS filtering | 11 endpoints | endpoint/mo | | | | | |
| Cloud backup storage | 2–3 TB per practice | TB/mo | (B2 list $6.95) | | | | Immutability |
| Local backup appliance/NAS | 1 per practice | unit | | | | | Practice-owned? |
| RMM/PSA | 1–2 technicians | technician/mo | (Syncro list $179 annual) | | | n/a | AI pricing after Jan 2027 |
| Tech E&O + cyber + GL | — | annual premium | $1M / $2M options | | | n/a | MSP control requirements |

### 5b. Customer quote / order form (one page)
**[Company Name] — Quote #[ ] — valid 30 days — DRAFT**

- **Client:** [Practice legal name], [address]. **Decision-maker:** [Owner]. **Workstations:** [n]. **Servers:** [n]. **Locations:** 1.
- **Recurring:**
  - [n] workstations × $[60] = $[ ]
  - HIPAA layer (dental) $100 *or* insurance-readiness layer (vet) $60
  - **Monthly total $[ ]**, billed on the 1st in advance by ACH.
- **One-time:** onboarding/remediation (scoped list attached) $[1,000]; stand-alone risk analysis $[1,500]; hardware (itemised, at cost +[10–15]%) $[ ]; labour $[120]/hour beyond scope; cabling by a licensed low-voltage subcontractor at cost +[ ]%.
- **Not included:** M365 and software licences (pass-through, or billed by the vendor directly), practice-management/imaging software fees, after-hours project work, cabling.
- **Taxes:** applicable Illinois sales tax on hardware; any Chicago lease-transaction tax on cloud components *(treatment to be confirmed by tax counsel before use)*.
- **Terms:** 12-month initial term, then month-to-month (30 days' notice); a 50% deposit on projects; BAA (dental) or confidentiality/data-processing agreement (vet) signed before access; offboarding includes handover of documentation and admin credentials.
- **Signatures:** Client ____ Date ____ · [Company Name] ____ Date ____

---

## 6. One-page offer sheet (text)
**DRAFT — not sent; requires founder review.**

**[Company Name] — Local IT and security for independent dental practices** *(vet version: "...for independent veterinary hospitals")*

**When your computers stop, your chairs stop.** We keep your practice-management server, imaging and front desk running, and we come in person the same day when something breaks within [area].

**Start with a fixed-price review**
- **Dental Security Risk Analysis + Policy Set: $1,500** ($750 for our first five North Side practices). We walk your office, review systems and backups, and complete a documented HIPAA Security Rule risk analysis. You receive a prioritised fix list and policies adapted to your practice. The Security Rule requires a risk analysis today, not only under future rules.
- **Cyber-Insurance Readiness Check: $350.** We check each security control insurers typically ask about: multi-factor authentication on email, remote access and admin logins; backups; endpoint protection. You get a plain-English list of what is true now and what to fix before you sign.

**Then, if you want us: monthly managed IT**
- $60 per workstation per month, minimum $450, plus $100 for the HIPAA layer.
- Includes:
  - 24/7 monitoring and patching;
  - managed endpoint detection and response;
  - email and web filtering;
  - local and cloud backups with monthly test restores;
  - firewall and Wi-Fi management;
  - practice-management and imaging vendor coordination;
  - same-day on-site response in [area];
  - an annual risk-analysis refresh and staff security training.
- Hardware and projects are quoted separately. 12-month initial term, then month-to-month.

**What we will never do:**
- Hold your data or passwords hostage.
- Sell you a "certification".
- Hide add-ons.

[Founder Name] · [phone] · [email] · [website]

*Footnotes for founder (do not print):*
- Risk-analysis duty: 45 CFR 164.308 [A, E-WS04014-S020].
- Insurer control questions: [B, E-WS04014-S007].
- The free HHS SRA Tool exists [B, E-WS04014-S017]. Be ready to explain the value added: on-site review, remediation, documentation.

---

## 7. Pricing calculator specification
**DRAFT — not sent; requires founder review.**

**Inputs (per practice):**

| Group | Fields |
|---|---|
| Practice | Type (dental / vet / human-medical); workstations; servers; mailboxes; locations; backup data (TB) |
| On-site load | Imaging devices (sensors, pan/CBCT); distance from base (miles; flag >5) |
| Price list | Price per workstation (default dental $60, vet $55); minimum ($450); compliance layer (dental $100 / vet $60 / none) |
| One-time | Onboarding/remediation items (checklist with hours × $120); hardware lines (cost, markup %) |
| Tool costs | EDR $7/endpoint; email $3/mailbox; DNS $1.50/endpoint; backup $6.95/TB; compliance portal $15 |
| Labour | Expected technician hours/month (default 6 dental, 7 vet; override after time logs); loaded hourly cost ($37.40) |
| Tax | Chicago location flag (PPLTT treatment pending) |

**Outputs:**
- Monthly price.
- One-time total and deposit due.
- Monthly tool cost.
- Gross margin %.
- Contribution after technician time ($ and %).
- Contribution after allocated overhead (input: active practices; overhead/month default $2,470).
- Payback months on onboarding effort.
- A comparison line, "remote all-in equivalent", using published anchors (Siotek $399 + add-ons input; Darkhorse $49.93 × workstations) [B, E-WS04014-S004, S005].
- Warnings:
  - contribution after technician time <$250/month;
  - distance >5 miles;
  - price <$550;
  - hours >8.

---

## 8. Order-intake / onboarding checklist
**DRAFT — not sent; requires founder review.**

**Before any access**
- [ ] Signed quote/order form, MSA, and BAA (dental) or confidentiality/data-processing agreement (vet).
- [ ] ACH mandate on file; deposit received.
- [ ] Insurance bound and certificate available on request.
- [ ] Client contacts confirmed: owner, office manager, after-hours emergency contact.
- [ ] Current IT provider offboarding requested by the client (credentials, documentation); contract end date noted.

**Week 1 — discover & secure**
- [ ] Asset inventory: workstations, servers, network gear, imaging devices, printers, phones, cloud services.
- [ ] Network diagram and credential vault entries. Rotate shared and admin passwords.
- [ ] RMM agents deployed; EDR deployed; old antivirus removed.
- [ ] MFA enabled for email, remote access and **all admin accounts, including the MSP's own RMM and vault logins** (maps to the carrier questions [B, E-WS04014-S007]).
- [ ] Email security and DNS filtering on.

**Weeks 2–3 — backup & recovery**
- [ ] Local backup target installed (practice-owned hardware).
- [ ] Cloud backup configured (practice-owned B2 account with the practice's BAA, or a vendor that signs a subcontractor BAA); immutability on.
- [ ] **First full test restore of the PM database and imaging store completed and logged.** No monthly contract "go-live" before this.
- [ ] Written restore procedure and target time for critical systems.

**Weeks 3–4 — document & hand over**
- [ ] Patch baseline; unsupported OS list with a replacement quote.
- [ ] Firewall review and change log.
- [ ] *(Dental)* Risk-analysis kickoff or refresh scheduled; policy set adapted; training scheduled.
- [ ] *(All)* Cyber-insurance control checklist prepared for the next renewal.
- [ ] Welcome pack: how to open tickets, emergency number, SLA.
- [ ] 30-day check-in booked; first QBR date set.

**Exceptions to escalate:** no restorable backup found; signs of compromise; owner refuses MFA (document the refusal); end-of-life server holding ePHI.

---

## 9. Weekly KPI sheet specification
**DRAFT — not sent; requires founder review.**

**One row per week. Columns:**

| Group | Columns |
|---|---|
| Pipeline | Walk-ins; decision-maker conversations; interviews; referral-partner meetings; introductions received; proposals sent; paid reviews sold (count, $); monthly LOIs (count, price); monthly contracts signed (count, MRR) |
| Customer base | Active practices; MRR; churned practices (with reason: sale / DSO / switch / other); net adds |
| Delivery | Tickets opened; tickets per endpoint; on-site visits; technician hours per practice (rolling 4 weeks); first-response time (median); critical incidents; restore tests done vs due |
| Money | Cash balance; AR >15 days; deposits held; tool costs per practice; insurance and fixed overhead |
| Founder time | Hours selling; hours technical; hours admin |

**Derived indicators and thresholds:**

| Indicator | Threshold |
|---|---|
| Conversations per month | Target 12; alert <8 |
| Proposal → win | Target 25%; alert <15% |
| Average price per practice | Target $690; alert <$600 |
| Hours per practice | Target ≤6; alert >8 |
| Tickets per endpoint per month | Alert >1.5 |
| Restore-test completion | Must be 100% |
| Contribution after technician time per practice | Target ≥$300 |
| Months of cash runway | — |
| Hire-readiness flag | Practices ≥14 **and** ≥1 win/month for 3 months **and** founder technical hours >50/week |

**Gates shown on the sheet:**
- **Day 30 / 30 visits:** ≥3 paid engagements; ≥2 LOIs ≥$550.
- **Month 9:** ≥4 monthly practices.
- **Month 18:** ≥12 practices.
