# Cycle 1 — Response, part 2 (biology/CRO/quality; investor/IP)

| ID | Sev | Status | Response |
|---|---|---|---|
| QA-REG-01 | critical | fixed | PDF prints a per-specimen measurement-support table (status, reason, conditions), marks conditional values "(c)" and refused values "n/m", states the evidence stage, and lists analysis parameters; CSV has a `__support` column per endpoint. |
| CRO-01 | critical | fixed | Pilot template: agreement only for supported endpoints and total mineral; independent reference (histology, phantom subset, blinded manual consensus) agreed before unblinding; disagreements adjudicated against it. |
| INV-01 | critical | open (scheduled) | Gen-1 decks/report/workbook marked superseded in deliverables/README; rebuilt in the final-deliverables phase from current sources. |
| IP-01 | critical | assigned | Desktop stream: exclude GPL-only Qt modules (Virtual Keyboard etc.), bundle licence check, third-party notices, LGPL relinking instructions. |
| IP-06 | critical | accepted (founder decision) | Repository stays public by founder instruction; consequences recorded in docs/ip/IP_STRATEGY.md (addendum). No LICENSE file = all rights reserved by default; choosing a licence is a founder/counsel decision. |
| BIO-01 | high | disclosed | Day-0 condition text for resorbable materials (creeping substitution counted as graft) is now printed in reports. Method change needs real data. |
| BIO-02 | high | fixed | DBM new-bone endpoints not supported (advisor 1.2.1; test). |
| BIO-03 | high | open | Periosteal callus outside the segmental ROI: add an optional "callus envelope" ROI (cycle 2). |
| CRO-02 | high | fixed | Total mineral volume added to the default endpoint set. |
| CRO-03 | high | fixed | SOW clause for endpoints refused during or after analysis (reduced fee / change order / termination; no numeric value for refused endpoints). |
| CRO-04/05 | high | disclosed | Large-animal day-0 infeasibility and metal hardware: advisor refuses metals; day-0 mechanism documented as requiring a day-0 scan; positioning notes in FOUNDER_HANDOFF update (final phase). |
| CRO-06 | high | fixed | Analysis-parameter table (method, thresholds, graft share, advisor version) in the report. |
| QA-REG-02 | high | partial | Revision banners on URS/FS/IQ/OQ/PQ; full re-baseline to the desktop product scheduled with the documentation set. |
| QA-REG-03 | high | fixed | Grant drafts no longer state validation against physical phantoms. |
| QA-REG-05 | high | fixed | GLP package removed from SOW (quote already "not offered"). |
| QA-REG-06 | medium | fixed | 21 CFR 888.3045 (calcium salt) vs 888.3046 (with aminoglycoside) corrected. |
| QA-REG-08 | medium | fixed | Policy doc version synced to advisor 1.2.1. |
| QA-REG-12 | medium | open | Accuracy thresholds glossary (decision ±10%, experiment failure >20%, physical acceptance ±5%/±15%) — to add to ENDPOINT_DEFINITIONS. |
| QA-REG-13/14, BIO-04 | medium | fixed | Test count, market size, woven-bone range synchronised. |
| IP (dataset defaults) | high | fixed | `Case` defaults to commercial_use "unclear" (never commercial-eligible by default); tests updated; ATTRIBUTION.md lists CC-BY obligations. |
| IP (EULA vs LGPL) | high | fixed | IP strategy: EULA must permit reverse engineering of LGPL components. |
| IP (customer-data training) | high | fixed | Revenue model: fine-tuning on customer scans only with written opt-in; per-customer weights. |
| INV (automated reviews) | high | fixed | REVIEW_REGISTRY discloses that reviews are automated reviewer agents, not human experts. |
| Remaining INV market/finance findings | high/medium | open | Market sizing basis, grants-as-cash, 2027 revenue timing, licence-revenue share vs public source: for founder decision with the commercial model owner; listed in FOUNDER_HANDOFF (final phase). |
