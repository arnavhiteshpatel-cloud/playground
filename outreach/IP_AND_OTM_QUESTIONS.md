# IP, OTM and Landuyt IP Clinic: Questions to Ask Before Collaborating

Prepared 2026-11-27. This is **not legal advice**. It is a prepared question list so the founder can get authoritative answers from the right offices. Evidence labels are as defined in `COLLABORATORS.md`.

## Offices and verified contacts

| Office | What it does | Contact (as shown on official page) |
|---|---|---|
| **UIUC Office of Technology Management (OTM)** | Makes University IP ownership determinations under Statutes Art. XII and General Rules Art. III **[V/CC]**. Receives invention, software and app disclosures, and assigns a technology manager. Advises disclosing roughly 8–12 weeks before publication **[V]**. | Ceramics Building 319, 105 S Goodwin Ave, Urbana IL 61801. 217-333-7862. otm@illinois.edu **[V]** ([page](https://otm.illinois.edu/researchers-innovators/transferring-research-beyond-academia)) |
| **Landuyt Center for Entrepreneurship: Intellectual Property Clinic** | A joint program with the College of Law. Law students prepare patent (Patent Track) and trademark (Trademark Track) filings for student entrepreneurs. **Offered only in the Spring semester.** Students pay USPTO filing fees **[V]**. Eligibility and application steps are not stated on the page **[UNR]**. | 351 Coordinated Science Lab, MC-228, 1308 W. Main St, Urbana IL 61801. 217-244-3124. landuyt@illinois.edu **[V]** ([page](https://landuyt.illinois.edu/programs/ipclinic)) |
| **Division of Research Safety (DRS)** | Biosafety and IBC registration, x-ray safety training, chemical waste | 217-333-2755. drs@illinois.edu. IBC: ibc@illinois.edu **[RF]** (search summary of DRS pages; confirm) |

### What policy says, as far as verified

- Copyrightable works a student creates using resources "over and above those usually and customarily provided" are owned by the student, with University internal-use rights. Customarily provided resources include office space, dorm rooms, library facilities and ordinary computer/network access. **[RF]**, from search summaries of University policy pages; read General Rules Art. III directly.
- When a student creates IP using University facilities, equipment or funds, standard University ownership rules apply. Students must report the project or invention to OTM to receive an ownership determination, and the University "in many cases" waives and assigns IP back **[RF]**.
- **[INF]** A micro-CT session at Beckman, billed to a faculty CFOP at the internal rate, likely counts as using University equipment and funds. Data stored on the ITG "CTData" server is on University infrastructure. Either could bring results within University ownership rules unless OTM determines otherwise in writing.

---

## A. Questions for OTM (ask for written answers)

### Status and ownership of what already exists
1. I am a UIUC undergraduate developing OsteoQuant, a software pipeline and synthetic-phantom benchmark, on my own time and equipment, with no University lab data, no faculty-lab resources, and no sponsored funding. **Should I file a software disclosure now to get an ownership determination**, so that the starting position is documented?
2. Which resources I used count as "usually and customarily provided"? Specifically: personal laptop; campus Wi-Fi; University software licenses such as MATLAB or campus cloud; library access; course knowledge.
3. Does any of my **prior research employment or volunteer work** in UIUC labs (orthopedic imaging, fracture detection, regenerative medicine) create University or sponsor claims? This includes any invention-assignment or confidentiality terms I signed, and ideas or code from that work. What should I do to ring-fence it?
4. If I took a course or independent study related to imaging or ML, does coursework create ownership issues? Is there a course exception?

### The planned physical phantom experiment
5. If I pay for Beckman Versa 630 time **myself** at the external rate, or through a future company under a facility usage agreement, and use butcher-sourced tissue and my own materials, will the resulting data and any improvements be mine or my company's?
6. If a faculty member sponsors access (internal rate on their CFOP), what ownership and conflict-of-interest consequences follow? Is there a standard **facility-use or sponsored-access agreement** that preserves founder ownership?
7. Scan data defaults to the Beckman ITG "CTData" network drive **[V]**. Does storage on University servers affect ownership? May I export immediately to my own storage?
8. Can the **Beckman "external with F&A" rate** ("businesses with a working contract" **[V]**) be used by a not-yet-incorporated founder? Or must I incorporate first? Who signs the contract?

### Collaborations
9. If I talk with UIUC faculty (Kersh, Wagoner Johnson, Harley) for **non-confidential advice only**, does that create any University claim? Is a simple written acknowledgement recommended?
10. If a faculty member later contributes ideas, data, or student labour, what agreement should come first: an NDA, a sponsored research agreement, a material/data transfer agreement or a collaboration agreement? How long do these typically take?
11. What is the process for licensing a University-owned dataset or model to a student startup, if one is ever needed?
12. For external collaborators (UCLA, CSU, WashU, Midwestern), which agreements route through OTM? Data-use agreements? Is there anything I may not do as an individual?
13. Publication: if I submit a benchmark paper or preprint, what should be disclosed first to preserve patent options, given the 8–12 week guidance **[V]**? Note that a U.S. one-year grace period exists, but many foreign jurisdictions require absolute novelty **[RF]**.

### Open-source and third-party code
14. OsteoQuant may use open-source libraries and possibly third-party models such as BONe (CC BY paper; Dryad model files whose license is unconfirmed **[UNR]**). Does OTM review open-source license compatibility for student projects, or should I get outside counsel?

### Startup path
15. What are the University's standard startup terms, such as equity or royalties, if any University-owned IP is ever licensed? Are there student-founder programs I should know about?

---

## B. Questions for the Landuyt Center / IP Clinic

1. **Eligibility:** must the startup be incorporated? Must the founder be an engineering student? Is an OTM ownership determination required before Clinic intake? *(The Clinic page does not say **[UNR]**; a 2019 article described referrals from the Technology Entrepreneur Center **[RF]**.)*
2. **Timing:** when does intake for the next Spring cycle open? What is the deadline?
3. **Patentability:** is software for *audited, multi-material segmentation of micro-CT* likely patent-eligible in the U.S. after *Alice*, or are trade secret, copyright and trademark more realistic? What do I need to document now: invention notebook, dated commits, a provisional?
4. **Provisional application:** is a provisional worth filing before the first publication or benchmark preprint? What would it cost in USPTO fees at micro-entity status? Note that students pay filing fees **[V]**.
5. **Trademark:** is "OsteoQuant" clear to use? Should I run a knockout search before outreach materials circulate widely?
6. **Agreements:** templates for a mutual NDA, an advisor agreement (with founder-friendly IP assignment) and a data-use agreement. Can the Clinic review these, or should I go to another resource?
7. **Collaborator inventorship:** if an advisor suggests an idea during a non-confidential meeting, how should that be handled for inventorship?
8. **Entity formation:** when to incorporate (for the Beckman contract rate and for IP assignment), and which other campus resources help with formation.

---

## C. Things to do now (low cost, protective)

1. Keep a **dated development log**: what was built, when, and on which equipment. Git history counts.
2. Write a one-page **"independence statement"** listing what OsteoQuant does *not* use: university lab data, lab equipment, sponsored funds, or confidential information from prior labs.
3. **Do not** start the physical phantom on a faculty CFOP or a University balance or drill until OTM has answered A5–A8.
4. Keep first emails **non-confidential** (see `OUTREACH_EMAILS.md`). No algorithm specifics.
5. Before using any third-party model or dataset, record its license and source in a `THIRD_PARTY.md` (to be created later in the codebase, not here).
