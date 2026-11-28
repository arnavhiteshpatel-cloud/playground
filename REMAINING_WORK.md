# Prioritised Remaining-Work Checklist (end of Generation 2, 28 November 2026)

Priority: **P0** = needed before any outreach, pilot or distribution; **P1** = before a first paid study or Gate 2;
**P2** = before GLP-adjacent use or scale. Owner: **F** = founder; **C** = collaborator or advisor; **E** = engineering;
**X** = external professional. Nothing below has been started on the founder's behalf: no email sent, nothing bought,
signed, submitted or distributed. Decision numbers refer to `FOUNDER_DECISIONS.md`.

| # | Pri | Item | Owner | Needs | Done when |
|---|---|---|---|---|---|
| 1 | P0 | IP questions with counsel: public disclosures of 27–28 Nov start US and grace-period clocks; non-US filings; licence of the repository; whether new inventive work stays public (#1, #2, #17, #19) | F+X | counsel | written decisions with dates |
| 2 | P0 | OTM ownership determination (lab history, appointments, resources used) (#4) | F | `outreach/IP_AND_OTM_QUESTIONS.md` | written determination |
| 3 | P0 | Personal data in the public repository (named academics, contact details) and whether to rewrite history (#3) | F | — | files kept or removed; history decision recorded |
| 4 | P0 | Positioning after S1H3/S1H4: the shipped advisor supports almost nothing on the application's material paths (residual graft only for HA; nothing with Unspecified). Decide whether to lead with material characterisation and feasibility checks (#20) | F | `EXPERIMENT_REGISTRY.md` S1H4 | positioning recorded; website, decks and pricing aligned |
| 5 | P0 | Ten discovery conversations by segment (`business/INTERVIEW_GUIDE.md`; drafts in `outreach/`, unsent) | F | outreach approval | ≥10 coded interviews; price-gate input (around 25 Feb 2027) |
| 6 | P0 | Physical phantom study, stage B (`validation/`): imaging scientist signs the protocol decisions; materials per BOM; scanner access | F+C | approval, collaborator, budget | first real graft/new-bone separability data |
| 7 | P0 | Human expert review of the advisor rules and statistics (imaging scientist, bone biologist, biostatistician) (#24) | F+X | budget or volunteers | written reviews; responses recorded |
| 8 | P1 | Windows and macOS builds: decide on running the `desktop-build` workflow (public, unsigned artefacts) (#21); then test on own machines | F | decision | builds pass their self-tests on both OS |
| 9 | P1 | LGPL-2.1 written source offer: name the offeror once incorporated, or ship source archives with each build (#22); counsel on the EULA | F+X | entity, counsel | notice names an offeror; B-016 closed |
| 10 | P1 | Advisor 1.4.4 (one version, then a new pre-registered held-out test S1H5): blur treated as unmeasured at high noise (DF-041, B1-blur); upper bound on the graft share in the new-bone budget (C3-SCI-17); enforce `compatible_with` for measured references (C3-SCI-07); species/kinetics for the ≤4-week rule (C2-SCI-11) | E | — | S1H6 registered before running, with ≥36 structures carrying support per claimed endpoint (S1H5 showed this is feasible for HA residual graft) and conditions where failures occur, so refusal is exercised too |
| 11 | P1 | ML campaign completion: S2 parts b/c, S3, U1, O2 (running on CPU at the end of Generation 2) and their registry rows | E | CPU time | registry, scorecard (B2, B3, B6, B7, B11) and handoff §3a filled from result files |
| 12 | P1 | Retrospective pilot on partner scans only after incorporation, a DPA and Gate 1 (#18) | F | partner, DPA | agreed protocol; no customer data before then |
| 13 | P1 | Study tables inside the audit hash chain, or per-row content hashes in audit details (dossier D-3) | E | — | direct database edits detectable |
| 14 | P1 | Traceability gaps: 54 verified / 42 partial / 33 gap FS rows (`docs/quality/traceability_matrix.csv`) | E | — | no GAP rows for URS items in the pilot scope |
| 15 | P1 | Remaining low review items: report appendix for technical refusal reasons; second-instance detection; desktop backup/label export; SAP object; offline test with the network blocked; ONNX output-channel check (ARC-06); Windows/macOS owner mapping in the bundle inventory (C3-PRD-10) | E | — | each closed with a test or recorded as accepted |
| 16 | P1 | Timed reviewer study to replace assumed effort constants (Experiment M) | F+C | 2–3 analysts | measured hands-on time |
| 17 | P1 | Grant and manuscript drafts rewritten in the founder's own words; AI-assistance disclosure per venue (#23) | F | — | drafts rewritten; submission decisions recorded |
| 18 | P1 | Cozad: registration deadline 2 Feb 2027; finals in April (date not confirmed) | F | #4 first | registered or declined |
| 19 | P2 | Release and version policy: tagged releases, semantic versions, "shipped" only for a rebuilt, self-tested bundle whose `build-info.json` records commit and advisor version (#25) | F+E | — | first tagged release |
| 20 | P2 | IQ/OQ execution on a locked release with a quality consultant | X | budget | executed protocols |
| 21 | P2 | Multi-scanner benchmark with collaborators; cross-scanner checks of the advisor's material profiles | C | data-sharing agreements | multi-site data |
| 22 | P2 | Histology integration (nuclei model or QuPath export); fix Macenko normalisation | E | — | nuclei F1 ≥0.6 on a held-out set |

Generation-1 items that are done or superseded: security review findings S-01…S-21 (fixed, `docs/security/REVIEW_RESPONSE.md`);
the Generation-2 security review (`docs/security/SECURITY_REVIEW_GEN2.md`); three review cycles across twelve
perspectives (automated reviewer agents, `REVIEW_REGISTRY.md`); the 90-day single gate (replaced by a price gate and a
later evidence gate, `business/PRICING_VALIDATION_PLAN.md`); PostgreSQL/HTTPS deployment (the product is now an
offline desktop application).
