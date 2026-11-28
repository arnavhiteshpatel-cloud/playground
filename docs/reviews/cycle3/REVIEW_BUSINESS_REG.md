# Review cycle 3: business, regulatory, IP/licensing and customer-facing science

**Date:** 2026-11-28.
**Commit reviewed:** `b55c459` (branch `claude/osteoquant-autonomous-dev-ujqgkl`). The review started at `6d87b5a`
with uncommitted changes to the decks and founder documents; those were committed as `67fc862` and `b55c459` during
the review, and the deck and founder text below is from those versions. Other work streams were still changing code
files (`osteoquant/desktop/services.py`, `osteoquant/api/bundle.py` and others) while this review ran.

> This review was produced by an automated reviewer agent, not by a qualified human expert. Nothing here is legal,
> tax or investment advice.

**Perspectives:**
- CRO operations buyer;
- quality and regulatory reviewer (GLP / 21 CFR 58 / Part 11 awareness);
- seed investor doing due diligence;
- IP/licensing counsel perspective (not legal advice);
- bone-biology check of customer-facing science statements.

**Scope:**
- the cycle-2 response in `docs/reviews/cycle2/REVIEW_BUSINESS_REG.md`;
- `website/` (9 pages and screenshots), `docs/user/`, `docs/quality/` (including the engineering dossier and SOPs), `docs/ip/`;
- `business/` (model, JSON outputs, templates, pricing and interview material), `investor/` (one-pager, funding strategy, the three `.pptx` decks), `grants/`, `validation/`;
- founder material: `founder/` (OPERATING_MANUAL, DEMO_SCRIPT, LEARNING_CURRICULUM), `FOUNDER_EXECUTIVE_SUMMARY.md`, `FOUNDER_DECISIONS.md`, `BLOCKERS.md`, `RELEASE_READINESS.md`, `ATTRIBUTION.md`, `deliverables/README.md`;
- the new sample reports `reports_samples/DefectFill_SAMPLE4_gen2_synthetic_betatcp.pdf` and `_SAMPLE5_gen2_synthetic_ha.pdf`;
- `deliverables/OsteoQuant_Gen2_Technical_Report.pdf`, `publications/`, `web/landing/`, `.github/workflows/`, `packaging/`.

**Method.** Read-only, apart from writing this file. Checks run:
- `python3 scripts/check_claims.py`: it passes. Its rule lists were then applied to a wider set of files.
- Deck text extracted with python-pptx; PDF text with pypdfium2; HTML pages reduced to text.
- `experiments/results/exp_S1H3_heldout.json` read per row to get endpoint coverage. Other result files read to compare quoted numbers: S1b, S1c, L4, F2, B.
- `scripts/material_support_table.py` run (advisor 1.4.2). `assess_support()` probed with blur values.
- `business/financial_model_outputs.json` checked against the decks, the one-pager and REVENUE_MODEL. Its SHA-256 prefix matches the `3fdeacbfa499` printed in the decks.
- `packaging/check_bundle_licences.py` run on the built Linux folder: it passes. `build-info.json` and the executable's timestamps compared with the git history.
- `git log` (push times), `git ls-files`, the CI workflow triggers, and the model-registry attribution fields.

**Severity:**
- **Critical:** a false or compliance-flavoured claim that a customer or investor would rely on.
- **High:** misleads a buyer or investor on a material point, contradicts the project's own gates, or creates a live legal or IP exposure.
- **Medium:** a weakness to fix before outreach or diligence.
- **Low:** hygiene.

## Verdict

The cycle-2 remediation is largely real.
- The rebuilt decks are honest and every figure in them traces to a file. They state the failures, the coverage cost,
  the absence of physical data and the automated nature of the reviews.
- The website quotes only the standard S1H3 phrase.
- The financial model now treats cash without grants as the lead case.
- Every quality document carries a DRAFT / not-executed banner.
- No GLP validation, Part 11 compliance or regulatory-acceptance claim was found anywhere. Simulated data are
  labelled SYNTHETIC wherever they appear, and no Gate 3 claim exists.

**No Critical finding.** What remains are three kinds of problem.
1. **Science-to-sales gap.** The final held-out result changes what the product can sell, and the commercial
   material has not caught up:
   - the per-material table still shows HA new bone as "supported";
   - several documents promise total mineral as a fallback;
   - the financial model assumes deliverable studies.

   Yet in S1H3, 126 of 216 specimens (58%) had *no* volume endpoint supported (C3-BIZ-01, -02).
2. **Stale or contradictory facts in places the checker does not look:**
   - the investor one-pager (advisor 1.3.3, "validation in progress");
   - the "multi-Otsu is the default" user documents;
   - a packaged build that predates the advisor it is said to ship;
   - inconsistent test and coverage figures, and date errors (C3-BIZ-03, -04, -05, -09, -10).
3. **Process and IP exposure:**
   - free evaluations on customer data are offered before Gate 1 and before M0;
   - new inventive work kept being pushed to the public repository after the documents set "before the next push"
     as the deadline for founder decision #2;
   - the IP documents overstate the loss of foreign rights (C3-BIZ-06, -07, -08).

---

## (a) Verification of the cycle-2 dispositions

Status key:
- **Agree**: the response is accurate and the fix is present.
- **Partly agree**: the fix is present, but a residual issue remains that the response did not state.
- **Disagree**: the disposition is not supported by the current files.

### C2-BIZ-01 … 24

| ID | Response | Cycle-3 verdict | Evidence |
|---|---|---|---|
| C2-BIZ-01 | Fixed | **Partly agree** | Verified:<br>• website, `docs/user/` and `docs/quality/` cite 1.4.2, or 1.4.1 only next to S1H3;<br>• the tables come from `scripts/material_support_table.py`;<br>• the 1.3.x/1.4.x rules are documented (science page, rules list).<br>Residuals:<br>• `investor/ONE_PAGE_OVERVIEW.md:17` still says "advisor 1.3.3", and the Gen-2 technical report table says "advisor 1.3.3". The version check does not cover `investor/`, `validation/`, `founder/` or `deliverables/` (C3-BIZ-04, -11, -17).<br>• The generated table runs the advisor without the blur and rim inputs, so it shows HA new bone as supported, which no held-out run ever did (C3-BIZ-01). |
| C2-BIZ-02 | Fixed | **Partly agree** | Verified:<br>• no S1/S1b/S1c numbers on the website or in `docs/user/`;<br>• the S1H3 phrase is checked against the file, with its `preregistered` and `advisor_version` guard;<br>• L3 is checked.<br>Residuals:<br>• `deliverables/OsteoQuant_Gen2_Technical_Report.pdf` p.3 still presents the in-sample S1b/S1c arms as "Advisor validation (SYNTHETIC)" (C3-BIZ-11).<br>• The `EXPERIMENT_REGISTRY.md:44` S1 row still reads "advisor pre-1.1.0". A correcting entry was added below it, but the row itself was not changed. |
| C2-BIZ-03 | Fixed (by removal) | **Agree**, with a new residual | The "54/54" card is gone, and the S1H3 phrase now carries coverage per endpoint. It still omits the specimen-level fact that matters commercially: 58% of held-out specimens had no endpoint supported (C3-BIZ-02). |
| C2-BIZ-04 | Fixed | **Agree** | SAMPLE4 and SAMPLE5 print "Weeks 4 (timepoint 'Week 4' (28 days))" and "8 (… 56 days)" with advisor 1.4.2 in the analysis-parameters table. |
| C2-BIZ-05 | Fixed | **Agree** | Both new samples carry the "SYNTHETIC DATA — computational phantoms…" banner, "Data class synthetic", and "SYNTHETIC DATA" in every page header. |
| C2-BIZ-06 | Fixed / Partial | **Agree** | Verified in SAMPLE5:<br>• "CI not shown, n=2" and "(n=1 of 3)";<br>• "—" for missing values; all 8 endpoints printed in two chunks;<br>• applied thresholds and the RUO footer printed;<br>• "Customer approver" role.<br>As the response says, the acquisition table is effectively empty (only `imported_with=desktop wizard`). Further residuals are in C3-BIZ-16. |
| C2-BIZ-07 | Fixed | **Partly agree** | The new samples exist, and `deliverables/README.md` marks SAMPLE1–3 superseded. Residuals:<br>• the old PDFs still sit in `reports_samples/` with nothing in the files themselves marking them superseded;<br>• the new samples were generated with `watermark=None`, so they lack the evaluation watermark that the site says every unlicensed report carries;<br>• their recorded git commit is wrong (C3-BIZ-16). |
| C2-BIZ-08 | Partial | **Agree** | `check_bundle_licences.py` passes on `packaging/dist/OsteoQuant/` (re-run by this review). The archive has not been rebuilt (B-016). New point: the built folder itself predates advisor 1.3.1–1.4.2 and the desktop cycle-2 remediation (C3-BIZ-05). |
| C2-BIZ-09 | Founder (#12) | **Agree** (founder), plus a residual | The counsel question is recorded as #12. The written offer added to the notices says "we will provide…" but names no offeror or address, and no entity exists (C3-BIZ-15). |
| C2-BIZ-10 | Fixed | **Agree** | `docs/security/SBOM.csv` has 143 rows, including PySide6, VTK and PyInstaller, and `sbom.cdx.json` exists. `IP_PROVENANCE.md:26` and IP_STRATEGY §2 state LGPL-3 Qt with dynamic linking. Note that the SBOM describes the stale build (C3-BIZ-05). |
| C2-BIZ-11 | Fixed | **Disagree** | The retired phrases are gone, but the one-pager is again stale on the central result:<br>• "measurement-support advisor 1.3.3" (`:17`);<br>• "Validation of the advisor under version 1.3.3 is in progress" (`:26-27`), although S1H3 (1.4.1) is complete and 1.4.2 ships;<br>• "556 tests" against the decks' "485 test functions";<br>• a "next 90 days" sequence that puts the phantom study before Cozad.<br>See C3-BIZ-04. |
| C2-BIZ-12 | Fixed / Founder (#8) | **Agree** | The JSON shows no 2027 revenue in the Conservative scenarios and 2027 Base revenue of $7,800 (0.8 pilots). Grants are restricted; the lead case has no grants (max deficit $96,126; with grants if awarded, $44,700). FUNDING_STRATEGY §6 has the four added risks. New residuals: the model has no coverage or refusal term (C3-BIZ-02), and M0 and the Gate 2 prerequisites are inconsistent (C3-BIZ-09). |
| C2-BIZ-13 | Fixed / Founder (#13) | **Partly agree** | REVENUE_MODEL §1 and the services page are corrected. But the interview script read **verbatim** to prospects still says "It can register later scans to a day-0 scan" (`business/INTERVIEW_GUIDE.md:84`; C3-BIZ-13). |
| C2-BIZ-14 | Fixed | **Partly agree** | The banned-phrase check exists and passes on its globs. Outward-facing files outside those globs still carry retired wording:<br>• "Audit-ready process prototype" (`web/landing/index.html:51`);<br>• "after independent review" (`publications/MANUSCRIPT_1_separability.md:65`, `MANUSCRIPT_3…:19`, `EXPERIMENT_REGISTRY.md:6`, which the website links as the source of every number).<br>See C3-BIZ-12 and -17. |
| C2-BIZ-15 | Fixed | **Agree** | No banned phrase in `grants/`. One low residual: the NSF pitch's competition statement (C3-BIZ-22). |
| C2-BIZ-16 | Fixed (statement) | **Agree** for the website | The science-page caption carries the caveat "tracking values the simulation has not yet achieved". The decks' day-0 column ("conditional") carries only "fragile under granule motion". The 200 µm policy tolerance is unchanged. |
| C2-BIZ-17 | Fixed (disclosure) | **Agree** | "Biological limits" is on the science page (callus, calcified cartilage, ectopic bone, autograft/allograft). The report limitations print the calcified-cartilage and ectopic-bone lines (seen in SAMPLE4 and SAMPLE5). |
| C2-BIZ-18 | Fixed | **Partly agree** | The table and advisor are correct: allograft, autograft and DBM are refused with day-0. But `docs/user/QUICK_START.md:88` and `FAQ.md:27` still list allograft, autograft (and DBM) as refused "without a day-0 scan", which implies a day-0 scan would help (C3-BIZ-19). |
| C2-BIZ-19 | Partial | **Agree** (still open) | `website/assets/img/08_report_preview.png` (22:11, 27 Nov) still shows "—" instead of "n/m", has no total-mineral volume column, and puts an unassigned "None" group in the table. |
| C2-BIZ-20 | Fixed | **Partly agree** | `docs/reviews/` is excluded and the checker passes. But the reason given for not scanning `.pptx` ("decks not regenerated") no longer holds: the decks were rebuilt on 28 Nov and are still unscanned, as are PDFs and `scripts/build_gen2_report.py` (C3-BIZ-17). |
| C2-BIZ-21 | Fixed | **Agree** | `ATTRIBUTION.md` and `legal.html` carry creators, titles and inline changes. The three SPROUT-derived registry entries carry a DOI, SPDX ID, creators and attribution text. The new `unet_dr2_mineral_s0` entry is synthetic-only. |
| C2-BIZ-22 | Fixed / Founder (#1, #2) | **Partly agree** | IP_STRATEGY was rewritten, INVENTION_REGISTER §0 says PUBLIC, and the bar date is in FOUNDER_HANDOFF and B-015. Residuals:<br>• advisor 1.4.0–1.4.2 (new mechanisms) were pushed publicly on 28 Nov, after decision #2 was set as "Now, before the next push", and the register still says everything was disclosed on 27 Nov (C3-BIZ-07);<br>• "foreign rights likely lost" and "Japan and Korea require absolute novelty" are overstated (C3-BIZ-08). |
| C2-BIZ-23 | Partial / Founder (#6, #7) | **Agree** | The footer reads "© 2026 [founder name] (no company exists yet…) … Unpublished draft". About and Contact still carry placeholders. |
| C2-BIZ-24 | Fixed | **Disagree** | The paid-engagement line is present (`index.html:181`, `services.html:145`). But replacing paid pilots with "free retrospective evaluations under a mutual NDA" leaves every risk the cycle-2 finding raised:<br>• custody of confidential sponsor scans by an individual, with no entity, insurance or DPA;<br>• university-ownership questions.<br>It also offers evaluation on customer data before Gate 1, the gate that defines when "a scientist can evaluate on their own data" (C3-BIZ-06). |

### Cycle-1 items the cycle-2 response left Partial or Founder (re-checked)

| ID | Response | Cycle-3 verdict | Evidence |
|---|---|---|---|
| INV-01 / INV-02 | Partial / Founder (#8) | **Agree** | The decks are rebuilt (built 28 Nov; advisor 1.4.2; model hash matches). None of the cycle-1 hard-coded claims remain. Slide 19 of the investor deck requires founder approval before external use. |
| IP-06 | Partial / Founder (#2) | **Partly agree** | See C2-BIZ-22. Still no `LICENSE` file. |
| BIO-04 | Partial | **Agree** | The site states that the early range is defined but not applied. The "≈1075" anchor remains in a code comment (`separability.py`). |
| CRO-04/05 | Fixed / Founder (#13) | **Agree** | "What we do not sell" lists metal hardware, osseointegration/BIC, day-0 including large-animal designs, and physical-phantom characterisation. |
| CRO-06 | Partial | **Agree** | Thresholds are printed. The acquisition table records nothing beyond the import route. |
| CRO-09/10 | Founder (#14) | **Agree** | The SOW, quote and pilot proposal carry one placeholder that points to #14. |
| INV-07 | Founder (#2) | **Agree** | Still open. The no-licence revenue figure ($114,174) is reported. |
| IP-02/03 | Partial / Founder (#12) | **Agree** | The notices are complete in the built folder. The built folder (and so its notices and SBOM) predates the commit `0aae793` that removes the web stack from the desktop bundle, so whether server packages remain in a future build is untested. |
| IP-07/13/15 | Founder (#3) | **Agree** (still tracked) | `PATENT_LANDSCAPE.md`, `patents.csv`, `prospects.csv`, the runtime logs (with the demo password "Demo-Password-2026") and `FOUNDER_HANDOFF.md:99` (a named faculty member with an email address) are all tracked. See C3-BIZ-23 for files #3 does not name. |
| IP-12 | Fixed (site) / Founder (#5, #7) | **Disagree** (as C2-BIZ-24) | See C3-BIZ-06. |

---

## (b) New findings

### C3-BIZ-01 · High · The per-material table shows new bone as "supported" where every held-out run refused it
**Perspective:** CRO buyer; bone biology.

**Location:**
- generator: `scripts/material_support_table.py:47`;
- customer-facing copies: `website/science.html:143` ("Sintered HA: Supported / Supported / Supported"), `docs/user/MATERIALS_AND_SUPPORT.md:43`;
- decks: investor slide 7, commercial-pilot slide 6, research slide 4 ("Single scan, any timepoint: HA … at low noise");
- founder material: `FOUNDER_EXECUTIVE_SUMMARY.md:34` ("graft and new bone can be separated only for dense calcium phosphates…"), `founder/DEMO_SCRIPT.md:56`.

**Evidence:**
- The generator calls `assess_support(mid, noise_rel, voxel_um, graft_prior, healing_weeks)` and passes no `blur_sigma_vox`, `rim_fraction_new` or `rim_fraction_mineral`, so the 1.4.x scan-measured blur and ambiguous-rim rules never fire. Those rules are what refuse new bone in practice.
- Probing HA at blur 0.75–2.5 voxels without rim inputs still returns supported for all three endpoints.
- In S1H3, new-bone volume was supported in **0 of 216** specimens, including the HA-like 3000 mgHA/cm³ arm at PSF 15 µm.
- The HA sample report produced by the same advisor (`DefectFill_SAMPLE5_gen2_synthetic_ha.pdf`, pp. 6–8) refuses new bone in **6 of 6** specimens ("13–22% of the would-be new bone is a one-voxel rim…") and total mineral in 3 of 6.
- The science page hedges ("the … blur and rim checks can still refuse a scan"). The decks and founder documents do not.

A buyer with an HA or BCP study is told to expect new-bone numbers that the product, on the project's own evidence, does not produce.

**Fix:**
- Split the table into graft and new-bone columns.
- Run the generator with the rim fractions and blur measured on a representative synthetic scan (or with the S1H3 imaging conditions).
- Add a fixed row note: "New-bone volume: never supported in the held-out simulation (S1H3), for any material."
- Rephrase "graft and new bone can be separated" as "residual graft can be supported".

### C3-BIZ-02 · High · The "total mineral is still reported" fallback held for 10% of held-out specimens; 58% got no endpoint at all
**Perspective:** Seed investor; CRO buyer.

**Location:**
- `founder/LEARNING_CURRICULUM.md:120` (model answer: "…and always give total mineral");
- `docs/user/QUICK_START.md:88-89` ("Total mineral volume is usually still reported");
- decks, the "Total mineral is the robust endpoint" text block;
- `business/templates/PILOT_PROPOSAL.md:25,35`: total mineral is an always-available agreement endpoint, and agreement is computed only on advisor-supported specimens;
- `business/REVENUE_MODEL.md` §2, §4 and `build_financial_model.py`: no feasibility or refusal term;
- O3 on the services page ("Can new bone and your graft be told apart…").

**Evidence:**
- From the rows of `exp_S1H3_heldout.json`:
  - 126 of 216 specimens (58%) had residual graft, new bone **and** total mineral all refused;
  - total mineral was supported only at PSF 15 µm (22 of 72 specimens there; 0 at 35 or 50 µm);
  - residual graft was supported in 0/54 at 1350 mgHA/cm³ and 8/54 at 1900.
- The standard phrase is accurate per endpoint but never states the per-specimen outcome. A sponsor buying an $8–15K non-GLP study, or a CRO on a $30–75K licence, would most often receive a report with no graft-related volume.
- The model's pilot-to-customer rate (40% Base) and characterisation attach rate (40%) assume deliverable results.
- In the pilot plan, ICC computed only on the specimens the advisor selects is a conditional, selection-biased estimate unless coverage is reported alongside it.
- The O3 answer for new bone is predictable today ("no").

**Fix:**
- Add one checked clause to the standard phrase, e.g. "no volume endpoint supported in 58% of specimens", and a CLAIMS entry for it.
- Replace "always" and "usually" with what was measured.
- Add to the model a feasibility-pass rate (studies that pass the SOW §7 pre-contract gate) and a refused-endpoint fee reduction, and run a sensitivity case.
- In PILOT_PROPOSAL, require reporting of coverage and of agreement over all specimens for total mineral, and state the selection effect.
- Reconsider whether O3 and O2 should be sold before stage B data exist (founder, see (c)).

### C3-BIZ-03 · High · Six customer documents name the wrong default segmentation method; under that method every tissue endpoint is refused
**Perspective:** CRO buyer; quality.

**Location:**
- `website/index.html:68` ("The default method is a classical, material-aware multi-Otsu split");
- `website/product.html:198`;
- `docs/user/QUICK_START.md:69` ("Segmentation: Multi-Otsu (classical) is the default");
- `docs/user/GLOSSARY.md:45`, `docs/user/INSTALLATION.md:46`, `docs/user/SCIENTIFIC_METHODS.md:34`.

**Evidence:**
- The code default is `advisor_threshold` (`osteoquant/desktop/services.py:481`, `osteoquant/pipeline.py:27`), and so are both sample reports.
- `science.html:121` and `MATERIALS_AND_SUPPORT.md:14` correctly say that support applies only to the advisor's threshold method, and that "with multi-Otsu … tissue endpoints are reported as not supported".
- A pilot user who follows the Quick Start and selects multi-Otsu, believing it to be the default, will get every tissue endpoint refused and conclude the product does not work.

**Fix:**
- Correct the six statements to "advisor threshold (default); multi-Otsu available but tissue endpoints not supported".
- Add an anchor to `check_claims.py` that compares the documented default with `ANALYSIS_DEFAULTS["segmentation"]`.

### C3-BIZ-04 · High · The investor one-pager is stale on the central result and the advisor version
**Perspective:** Seed investor.

**Location:** `investor/ONE_PAGE_OVERVIEW.md`:
- `:17` "measurement-support advisor 1.3.3";
- `:26-27` "Validation of the advisor under version 1.3.3 is in progress";
- `:18` "556 tests";
- `:50-51` "→ physical phantom study … → Cozad (Feb 2)".

**Evidence:**
- S1H3 (advisor 1.4.1) completed on 28 Nov and 1.4.2 ships, but the one-pager (last changed `c2b14f8`, 00:07 on 28 Nov) predates both.
- The decks built the same day quote S1H3, 1.4.2 and "485 test functions". An investor holding the one-pager and the deck sees two different products.
- The checker cannot catch this, because `VERSION_GLOBS` covers only `website/`, `docs/user/` and `docs/quality/`.

**Fix:**
- Generate the one-pager from the same data dictionary as `build_decks.py`, including the S1H3 phrase.
- Add `investor/`, `validation/`, `founder/`, `FOUNDER_*.md` and `deliverables/README.md` to `VERSION_GLOBS`.

### C3-BIZ-05 · High · "Shipped advisor 1.4.2" and "the Linux build passes its packaged self-test" describe two different code states
**Perspective:** Quality and regulatory; seed investor.

**Location:**
- `RELEASE_READINESS.md:13` (`[x] Desktop build Linux (local) … packaged self-test exit 0`);
- decks: slide 1 subtitle ("shipped measurement-support advisor 1.4.2"), slide 2 and slide 4 (investor);
- `website/product.html:179` ("packaged self-test passed (8 of 8 steps)");
- `FOUNDER_EXECUTIVE_SUMMARY.md:10-15`.

**Evidence:**
- `packaging/dist/OsteoQuant/OsteoQuant` was written at 22:16 UTC on 27 Nov and `build-info.json` at 22:18.
- At that time `separability.py` was at 1.3.0 (`24fc0c5`, 22:12).
- Advisor 1.3.1–1.4.2, method binding and the whole desktop cycle-2 remediation (`6658fd2`, 00:05 on 28 Nov) came later.
- The only self-tested package therefore contains neither the advisor nor the desktop fixes that the decks and the website describe as shipped.
- The SBOM (C2-BIZ-10) also describes this older build.

**Fix:**
- Untick the RELEASE_READINESS item until the bundle is rebuilt (B-016).
- Have `build.py` write `git_commit`, a dirty flag and `ADVISOR_VERSION` into `build-info.json`.
- Have the decks print "advisor in the last packaged build: X".
- Add a check that fails when `build-info.json`'s advisor differs from `ADVISOR_VERSION` while any document says "shipped".

### C3-BIZ-06 · High · Free evaluations on customer scans are offered before Gate 1 and before M0
**Perspective:** CRO buyer; quality; counsel perspective (not legal advice).

**Location:**
- `website/index.html:181`, `website/services.html:145` ("we can discuss free retrospective evaluations under a mutual NDA");
- commercial-pilot deck slide 9 ("Until incorporation and IP clearance: free retrospective evaluation under NDA only"; "analysed on a local, encrypted machine");
- `founder/DEMO_SCRIPT.md:40` (the 9:15 ask).

**Evidence:**
- RELEASE_READINESS defines Gate 1 as an "installable build that a scientist can evaluate on their own data"; it is not met. Gate 2, for pilots, needs counsel-reviewed SOW/DPA templates and real-data validation; also not met.
- FUNDING_STRATEGY §4: "Do not … sign … before M0". Without an entity, the founder signs the NDA personally and holds confidential sponsor scans personally, with no insurance (#16) and no DPA. The OTM determination is pending, which matters because customer data and university ownership interact.
- The application does not encrypt project folders (`docs/user/DATA_PROTECTION.md:36`). The "encrypted machine" promise depends on an undocumented operational control.
- Charging nothing does not remove any of these exposures.

**Fix:**
- Remove the free-evaluation offer until M0 and Gate 1, or make it a founder decision (see (c)) with an NDA/DPA reviewed by counsel or the clinic and a written data-handling procedure (encrypted disk, access log, deletion certificate).
- State the current gate status next to every pilot call to action.

### C3-BIZ-07 · High · New inventive work kept being pushed publicly after the documents said to stop; the invention register does not record it
**Perspective:** IP counsel perspective (not legal advice); seed investor.

**Location:**
- `FOUNDER_DECISIONS.md:24` (#2, "Now, before the next push");
- `FOUNDER_EXECUTIVE_SUMMARY.md:73` ("Stop pushing new inventive work publicly until decision #2 is made");
- `founder/OPERATING_MANUAL.md:144`;
- against: the `docs/ip/IP_STRATEGY.md` Addendum ("founder decided to keep it public and push all work"), `docs/ip/INVENTION_REGISTER.md:11,13` (15 commits, all dated 2026-11-27; everything publicly disclosed as of 2026-11-27; single bar date 2027-11-27), and IP_STRATEGY §1.1 and §5.4 ("Record the push date of every new inventive change").

**Evidence:**
- `FOUNDER_DECISIONS.md` was created in `c2b14f8` (00:07 on 28 Nov). After that, these were pushed to the public origin (the branch is level with `origin`):
  - advisor 1.4.0 (`a22da5a`, 00:25: scan-measured blur, a blur-aware graft partial-volume model, propagation of graft error into new bone, the ambiguous graft rim);
  - 1.4.1 (`7a3ae70`, the blur-scaled rim);
  - 1.4.2 (`cfad464`, method binding).
- These are the mechanisms that made S1H3 safe, arguably the most valuable embodiments. They are absent from the register, and their US one-year date is 2027-11-28, not 2027-11-27.
- The three founder-facing documents contradict each other: "push everything" is recorded as decided, the question is open and urgent, and the founder is told to stop.

**Fix:**
- Reconcile the documents with one recorded standing instruction from the founder that the development process follows.
- Until #2 is decided, keep new inventive work on a non-public branch or private remote.
- Add INV entries for the 1.4.x mechanisms with their push dates and commits.
- Replace "single bar date" with a per-invention table of push dates.

### C3-BIZ-08 · Medium · The IP documents' statements about the consequences of a public repository are incomplete (not legal advice)
**Perspective:** IP counsel perspective.

**Location:** `docs/ip/IP_STRATEGY.md:24-25`, `:42`, `:84`, `:138`; `docs/ip/INVENTION_REGISTER.md:13`; FOUNDER_DECISIONS #1–#3.

**Evidence:** These points are for counsel to confirm.
- (a) Grace periods. "The EPO, China, Japan and Korea generally require absolute novelty" is not accurate for Japan and Korea:
  - both provide a 12-month grace period for the applicant's own disclosures (Japan Patent Act Art. 30, with a declaration and proof of the disclosure; Korean Patent Act Art. 30);
  - Canada and Australia do as well.

  "Foreign rights are likely already lost" therefore overstates the position. A PCT or national filing by 2027-11-27 might preserve some non-European rights, and the option is missing from decision #1.
- (b) GitHub's terms let other users view and fork a public repository. The "all rights reserved by default" note omits this.
- (c) "Licence revenue has no practical enforcement basis" conflates several separate things: copyright that may still be enforceable once ownership is settled; the missing EULA and entity; the open OTM determination; and a licence check that anyone can remove from the public source.
- (d) The public INVENTION_REGISTER and IP_STRATEGY contain the founder's own novelty assessments, e.g. "weak novelty vs Schulte 2011, Wehrle 2019, US9036899B2". They are as discoverable as the FTO triage that decision #3 already covers.

**Fix:** Correct §3 and §1.1. Add "PCT or national filings in grace-period jurisdictions by 2027-11-27" as an option under #1. Separate the legal and practical points in (c). Add the two IP documents to the scope of #3.

### C3-BIZ-09 · Medium · Date and gate errors in founder and investor material
**Perspective:** Seed investor.

**Location:**
- `FOUNDER_DECISIONS.md:14` ("2 Feb 2027 | Cozad pitch"), `FOUNDER_EXECUTIVE_SUMMARY.md:67,81`, investor deck slide 18 key dates;
- against `grants/COZAD_APPLICATION_PACKAGE.md:7,149-151` (2 Feb is the registration deadline; finals in April).
- `business/PRICING_VALIDATION_PLAN.md:116`, investor deck slides 15 and 19, `investor/ONE_PAGE_OVERVIEW.md:50-53`;
- `investor/FUNDING_STRATEGY.md:68` (M0) against `:37` and `business/REVENUE_MODEL.md:90`;
- investor deck slide 18 milestone 2 against `RELEASE_READINESS.md` Gate 2.

**Evidence:**
- **Cozad date.** The pitch date is misread; the registration deadline is taken for the pitch.
- **25 Feb gate.** The combined gate (around 25 Feb 2027) requires "a separable path in the phantom study". The phantom protocol is not approved and needs 14 signed imaging-scientist decisions, the OTM determination and a Beckman agreement. M2 is "Spring 2027" (Feb–Apr), so the gate cannot be evaluated on that date.
- **M0.** It is defined two ways: "OTM determination *requested*; entity decision" (§3) versus "entity, OTM/IP clearance, insurance, counsel-reviewed NDA/SOW/DPA" (§2a and the model).
- **Gate 2.** The paid-pilot milestone lists entity, OTM and contracts but not the Gate 2 prerequisites that RELEASE_READINESS sets for a paid pilot (real-data validation for one task, closed human review). Slide 18 itself says human expert review is "required before a pilot-ready release (Gate 2)".

**Fix:**
- Rename the date "Cozad registration deadline" and add the finals date.
- Move the combined gate to after the phantom read-out, or split it into a price gate (Feb) and a separability gate (spring).
- Use one definition of M0.
- Make Gate 2 a stated prerequisite of M3 and of the model's paid-pilot start.

### C3-BIZ-10 · Medium · Test-count and coverage figures conflict across investor and quality documents
**Perspective:** Seed investor; quality.

**Location:**

| Figure | Locations |
|---|---|
| 372 test functions | `docs/user/RELEASE_NOTES_GEN2.md:98` |
| 439–457 test items | `docs/quality/ENGINEERING_VALIDATION_DOSSIER.md:23` |
| 485 test functions | decks |
| ≈555 / 556 tests | `BASELINE_COMPARISON.md:22`; one-pager `:18`; Gen-2 report |
| 62% coverage | dossier `:25` (from `coverage_baseline.txt`) |
| ≈88% coverage | `RELEASE_READINESS.md:17`; `FOUNDER_EXECUTIVE_SUMMARY.md:18` |
| 91% coverage | decks and Gen-2 report, from `docs/qa/coverage_final.txt` of 27 Nov 22:48, whose header records "1 failed" |
| coverage "unknown" | B14 in the same Gen-2 report |

**Evidence:** The decks' 91% is above the 90% Gate 1 coverage threshold that RELEASE_READINESS says is *not* met at ≈88%. A diligence reader will find all of these. The dossier also mixes 27 Nov metrics with a 28 Nov software baseline, and its file name says "VALIDATION" while its title says "Verification".

**Fix:**
- Have CI write one metrics file (tests collected, passed, coverage, commit, date) that every document and deck reads.
- Drop the stale `coverage_final.txt` figure.
- Rename the dossier file to `ENGINEERING_VERIFICATION_DOSSIER.md`.

### C3-BIZ-11 · Medium · The Gen-2 technical report presents in-sample runs as validation; the deliverables index is stale
**Perspective:** Seed investor; quality.

**Location:** `deliverables/OsteoQuant_Gen2_Technical_Report.pdf` (built at `33d085c`), pp. 2–3, 10; `deliverables/README.md` rows 1 and 11 and the "Also" line.

**Evidence:**
- The report's capability table says "Identifiability decided before reporting (advisor 1.3.3)".
- Its "Advisor validation (SYNTHETIC)" row cites the S1b/S1c arms ("every failing measurement refused … in all S1b/S1c arms"). Those are in-sample development runs (now 1.4.2 re-runs), which the project's own rule says are development checks, and which the website explicitly does not quote.
- Transfer results read "pending" throughout. Coverage is 91% on p.3 and "unknown" on p.10.
- The README still lists the Gen-1 `OsteoQuant_Technical_and_Commercial_Report.pdf` as deliverable 1, does not list the Gen-2 report, and points readers to `web/landing/index.html`.

**Fix:**
- Rebuild the report after the S1H3 standard phrase and current metrics are fixed, with no S1b/S1c "validation" row and no "pending" placeholders.
- Update the README.
- Add `scripts/build_gen2_report.py` to `SCAN_GLOBS`, and scan PDF text in CI.

### C3-BIZ-12 · Medium · Outward-facing files outside the checker's scope repeat retired claims
**Perspective:** Seed investor; quality.

**Location:**
- `web/landing/index.html:43`, `:49`, `:51`;
- `publications/MANUSCRIPT_1_separability.md:65` and its abstract conclusion (lines 12–25);
- `publications/MANUSCRIPT_3_adaptation_uncertainty.md:19`;
- `EXPERIMENT_REGISTRY.md:6`;
- `FOUNDER_HANDOFF.md:8`, `:77`.

**Evidence:**
- The Gen-1 landing page still says "Audit-ready process prototype", "benefit of a day-0 baseline scan" and "Talk to us about a pilot".
- Both manuscripts say results were "corrected after independent review", though the reviews were automated agents.
- Manuscript 1 concludes "a day-0 baseline scan is the most robust strategy", which L3 contradicts (0.535 at 50 µm).
- `EXPERIMENT_REGISTRY.md`, which the science page links as the registry "with every number", says "corrected after an independent review".
- FOUNDER_HANDOFF repeats "independent review" and "audit-ready per-study reports".

**Fix:**
- Delete or mark `web/landing/` superseded.
- Rewrite the manuscripts' review statement ("internal automated review") and the day-0 conclusion (cite L3).
- Fix the registry header.
- Add `publications/`, `web/`, `founder/`, `validation/` and the root ledgers linked from the site to `FACING_GLOBS`.

### C3-BIZ-13 · Medium · The interview script read verbatim to prospects claims day-0 registration
**Perspective:** CRO buyer.

**Location:** `business/INTERVIEW_GUIDE.md:84` (§9 concept description, "Read this description verbatim").

**Evidence:** The script says "It can register later scans to a day-0 scan … labels new bone, residual graft and host bone".
- There is no desktop day-0 workflow, and day-0 analysis is "not sold" (services page).
- The FTO question (#15) is open.
- New bone was never supported in held-out simulation.

This is the one artefact guaranteed to reach every interviewee. C2-BIZ-13 is therefore only partly fixed.

**Fix:** Rewrite the description from the services page's wording. Add `INTERVIEW_GUIDE.md` to a day-0 claim check (e.g. ban "register later scans" outside history lines).

### C3-BIZ-14 · Medium · Pricing cards outside the stated hypothesis ranges, and offers before incorporation
**Perspective:** Seed investor; counsel perspective.

**Location:** `business/PRICING_EXPERIMENT.md:18-24` (card set), `:36`, `:64`.

**Evidence:** The interview cards anchor prices that the stated hypotheses do not contain:

| Card | Card price | Stated hypothesis |
|---|---|---|
| M6 full analysis service | $8–20K per study | $8–15K |
| M4 industry subscription | $15–30K per year | enterprise $30–75K |
| M1 per-scan | $150–600 | no hypothesis exists |
| M8 algorithm licence | $25–100K up-front + royalty | no hypothesis exists |

Phase 2 (weeks 6–16) sends "real written proposals" with "one coherent, genuine offer that OsteoQuant would honour", but sets no entity precondition. The follow-up draft (`outreach_drafts/06…:26-30`) does set that precondition.

**Fix:**
- Align the card anchors with the five hypotheses, or add the new ones to REVENUE_MODEL §1 as explicit [HYP] rows.
- Add "only after M0 (entity exists)" to Phase 2.

### C3-BIZ-15 · Medium · Distribution and source-offer controls are weaker than the documents say
**Perspective:** Licensing counsel perspective (not legal advice).

**Location:**
- `.github/workflows/desktop-release.yml:11-25`, `:122-131`;
- `founder/OPERATING_MANUAL.md:129` and `docs/desktop/PACKAGING.md:16` ("never publishes"), against `BLOCKERS.md` B-013;
- `packaging/bundle_inventory.py:302` and `THIRD_PARTY_NOTICES.txt:118-127`.

**Evidence:**
- (a) **PR-triggered builds.** Any pull request that touches `osteoquant/desktop/`, `osteoquant/licensing/` or `packaging/` triggers the desktop build. If the build passes, it uploads unsigned archives as artifacts that any signed-in user can download from a public repository. That is a distribution, which B-013 reserves to the founder.
  - The Windows and macOS inventories have never run. `bundle_inventory.py` would probably fail on unmapped DLLs (fail-safe), but that is untested.
- (b) **No named offeror.** The LGPL-2.1 written offer reads "On written request within three years … we will provide the corresponding source". It names no offeror, address or contact, and no entity exists to make the offer.
- (c) **ICU text.** The ICU licence text is copied from the build host's Debian ICU package, not from the ICU version inside the wheel.

**Fix:**
- Remove the `pull_request` trigger or make artifact upload conditional on manual dispatch, and correct "never publishes".
- Name the offeror and a contact address in the notice (founder decision; see (c)), or ship the source archives with the build.
- Take the ICU text from the matching ICU source release.

### C3-BIZ-16 · Medium · The sample reports' provenance and gating do not meet the project's own traceability rules
**Perspective:** Quality (GLP awareness); CRO buyer.

**Location:** `reports_samples/DefectFill_SAMPLE4_gen2_synthetic_betatcp.pdf` and `_SAMPLE5_gen2_synthetic_ha.pdf` §1, §6, §9; `scripts/make_gen2_sample_reports.py:70`; `pyproject.toml:3`.

**Evidence:**
- **Wrong commit.** Both reports print `git_commit d1fd78c…`, but the generator script does not exist at `d1fd78c`; it was first committed in `91abd5f`. The reports were made from an uncommitted working tree, and nothing in them says so.
- **Static version.** `software_version` is 0.1.0, the same as the Gen-1 samples, after about 80 commits of changes.
- **No watermark.** Both were generated with `watermark=None`, so they lack the "EVALUATION COPY" watermark that the website (`services.html:99`, `product.html:158`) says every unlicensed report carries.
- **Inconsistent gating in SAMPLE5:**
  - every specimen is QC "review";
  - dense HA phantoms are flagged "possible metal/hardware";
  - 5 of 6 ROIs are "not yet accepted";
  - yet residual-graft fractions are reported, while Tb.Th is refused on the grounds of the unaccepted ROI.

**Fix:**
- Record the commit and a dirty flag, and refuse to stamp a clean commit on a dirty tree.
- Version releases.
- Generate samples with the evaluation watermark, or state on page 1 why they carry none.
- Accept the demo ROIs before generating the samples, or explain the "review" verdicts in the deliverables README.

### C3-BIZ-17 · Medium · The claims checker is too narrow for what it is described as guaranteeing
**Perspective:** Quality; seed investor.

**Location:** `scripts/check_claims.py`. The about page (`website/about.html:73`) says "A claims checker compares numbers in the documents with the result files".

**Evidence:** Gaps found by applying its rules more widely:
1. **Unscanned file types and generators.** It does not scan `.pptx` or PDF text, and `scripts/build_gen2_report.py` is not in `SCAN_GLOBS`.
2. **Narrow version scope.** `VERSION_GLOBS` misses `investor/` (C3-BIZ-04), `validation/` (`VALIDATION_PROGRAM.md:9`: "S1/S1b/S1c are being re-run with advisor 1.3.0"), `founder/` and `deliverables/`.
3. **Narrow banned-phrase scope.** `FACING_GLOBS` misses `publications/`, `web/` and the root ledgers the site links (C3-BIZ-12).
4. **Paraphrases go unchecked.** Only exact anchors are checked:
   - investor deck slide 2, "Final S1H3 (advisor 1.4.1): every failure refused on every endpoint", breaks the rule that advisor validation is quoted only as the standard phrase;
   - the Gen-2 report's "residual graft was supported in 37%…" is likewise unchecked.
5. **Unchecked load-bearing numbers.** Not checked: test counts and coverage (C3-BIZ-10); market size ($0.81M / $1.86M / $3.90M); the five price ranges; "0 interviews"; "38 competitors"; "869 MiB"; the build's advisor version (C3-BIZ-05); the documented default method (C3-BIZ-03); experiment status ("running" against "Queued", C3-BIZ-21).
6. **Whole-line exemptions.** `ALLOW_LINE` exempts any line containing "do not", "not sold" or "banned", and `VERSION_ALLOW` any line containing "since", "before" or "until". None is exploited today, but both are wide.
7. **Missing banned phrases.** The list lacks positive "compliant", "GLP-validated", "Part 11 compliant", "has been validated" (e.g. `SCIENTIFIC_METHODS.md:324`, "The advisor has been validated only in simulation"), "proven" and "human expert review" used as a claim.

**Fix:** Close items 1–7. Match exemptions on a span around the hit, not the whole line. Make a deck-text dump from `build_decks.py` part of the scanned set.

### C3-BIZ-18 · Medium · Refusal reasons advise sponsors to add a day-0 scan
**Perspective:** Bone biology; CRO buyer (3Rs).

**Location:** `osteoquant/advisor/separability.py:595` ("Report total mineral; add a day-0 scan or histology to separate graft from new bone"), printed in every SAMPLE4 refusal; `docs/user/TROUBLESHOOTING.md:48` ("plan a day-0 scan or histology").

**Evidence:**
- A day-0 scan means an extra in vivo imaging session, with anaesthesia, for every animal.
- The project does not offer day-0 analysis, has no desktop workflow and has an FTO question open (#15). In simulation, day-0 fails with tens of µm of granule motion (L3).
- For remodelling grafts the advisor refuses day-0 anyway.

A study director could change a protocol on the strength of a report line that the product cannot follow through on.

**Fix:**
- Change the text to "Report total mineral; separating graft from new bone needs histology (a day-0 scan is a research option this software does not support)".
- Never suggest day-0 for autograft, allograft or DBM.

### C3-BIZ-19 · Low · Quick Start and FAQ imply that day-0 rescues bone-derived grafts
**Perspective:** Bone biology.

**Location:** `docs/user/QUICK_START.md:88`; `docs/user/FAQ.md:26-27`.

**Evidence:** "…allograft, autograft and DBBM without a day-0 scan" (and DBM in the FAQ). Advisor 1.3.3+ never supports allograft, autograft or DBM, with or without day-0. Only DBBM may receive day-0 support.

**Fix:** List the bone-derived grafts separately as "refused by any mechanism (use histology)".

### C3-BIZ-20 · Low · Stale website and validation-programme content
**Perspective:** CRO buyer; seed investor.

**Location:**
- `website/validation.html:196-213`;
- `website/assets/img/08_report_preview.png`;
- `website/about.html:105`;
- `validation/VALIDATION_PROGRAM.md:9` (the source of the validation page).

**Evidence:**
- **Scorecard.** The site says "The current build has not yet been scored against these targets", with B4 "not measured", B5 "not built then" and B10 "50% fail". `BENCHMARK_SCORECARD.md` now holds current values: B4 n=80, bias +0.1%; B5 met in S1H3; B10 16/16.
- **Screenshot.** It still shows "—" instead of "n/m" (C2-BIZ-19).
- **About page.** It lists "a day-0 study design for difficult materials" as a focus, while the services page lists it under "not sold".
- **Validation programme.** Stage A says "S1/S1b/S1c are being re-run with advisor 1.3.0" and "L3 is being re-run", and names the in-sample S1/S1b/S1c as the exit criteria instead of S1H3.

**Fix:** Regenerate these from `BENCHMARK_SCORECARD.md` and the registry, and update stage A.

### C3-BIZ-21 · Low · Experiments described as "running" are queued
**Perspective:** Seed investor.

**Location:** investor deck slide 11 and research deck slide 8 ("S2v2 parts b, c; S3 … running", "U1 … running"); `FOUNDER_EXECUTIVE_SUMMARY.md` §2 ("S2b/c, S3, U1, O2 are still running").

**Evidence:** `EXPERIMENT_REGISTRY.md:54` lists U1 as "Queued". `exp_U1.log` is empty. `QUEUE4.log` and the process list show only `exp_S2_sim2real.py b` running.

**Fix:** Print the registry status (running / queued) per experiment.

### C3-BIZ-22 · Low · The NSF pitch's competition paragraph contradicts the project's own competitor matrix
**Perspective:** Seed investor; grant reviewer.

**Location:** `grants/NSF_PROJECT_PITCH_DRAFT.md`, section 3 ("general micro-CT software … and open-source tools, all built around thresholding and manual ROI work").

**Evidence:** Investor deck slide 14 and `docs/research/COMPETITOR_MATRIX.md` say that learned segmentation is commodity: Dragonfly ships SAM and 3D deep learning, and Amira/Avizo with BONe offers trainable multi-material deep learning.

**Fix:** Use the matrix's wording: deep learning is available, and graft-aware abstention was not found.

### C3-BIZ-23 · Low · Personal data in the public repository beyond what decision #3 names
**Perspective:** Counsel perspective (privacy; not legal advice).

**Location:** `outreach/collaborators.csv` (about 20 named academics with email addresses, phone numbers and "proposed project" notes, including one personal Gmail address); `outreach/OUTREACH_EMAILS.md`.

**Evidence:**
- Both files are tracked. The contacts carry source URLs, so they do not look fabricated, but they are published with outreach intentions and without consent.
- FOUNDER_DECISIONS #3 names `COLLABORATORS.md` and `prospects.csv` but not these two files.
- The CSV is malformed: rows have 23–30 fields against a 23-column header.

**Fix:** Add both files to #3. Fix the CSV quoting.

---

## (c) Founder-only decisions missing from `FOUNDER_DECISIONS.md`

None of this is legal, tax or investment advice.

| # | Decision | Why it is founder-only and time-sensitive | Related |
|---|---|---|---|
| c1 | **A standing instruction to the development process on pushing**: whether new inventive work may go to the public `origin` before decision #2 is made, and where it goes otherwise (private remote or branch). | The documents contradict each other, and pushes of new mechanisms continued on 28 Nov. Each push starts a new one-year US clock. | C3-BIZ-07 |
| c2 | **Whether to offer any evaluation on customer data before M0 and Gate 1**, and if so under which NDA/DPA, who holds the data, on what machine, and with what insurance. | It is currently written into the website, the pilot deck and the demo script as an offer. #7 mentions it only as context. | C3-BIZ-06 |
| c3 | **Non-US filings in grace-period jurisdictions** (PCT or national filings in Japan, Korea, Canada and Australia) by 2027-11-27, as an option alongside the US provisional. | This changes the value of decision #1. Japan requires a disclosure declaration at filing. | C3-BIZ-08 |
| c4 | **Positioning after S1H3**: whether to sell non-GLP study analysis and material characterisation before stage B data, or to lead with "residual graft and total mineral where supported, plus a feasibility check"; and whether the financial model should carry a feasibility-pass rate and a refused-endpoint fee reduction. | It decides what the website, decks and interview script may promise. #13 covers only the characterisation price floor. | C3-BIZ-01, -02 |
| c5 | **Whether to allow the desktop-build workflow to run on pull requests** (public artifacts) and when to dispatch it. | B-013 calls this a distribution decision, but it is not in FOUNDER_DECISIONS, and the PR trigger bypasses it. | C3-BIZ-15 |
| c6 | **Who makes the LGPL-2.1 written source offer** (name, address, a three-year commitment), or whether to ship the source archives instead. | The offer in the notices has no offeror. This is needed before any distribution. | C3-BIZ-15, #12 |
| c7 | **Manuscripts**: whether and when to submit; authorship; the disclosure of AI assistance under each journal's policy; and the IP check before submission (IP_STRATEGY D-IP-7). | #10 covers grant applications only. The manuscripts contain stale conclusions. | C3-BIZ-12 |
| c8 | **Budget and recruitment of human expert reviewers** (imaging scientist, bone biologist, biostatistician, quality, counsel). | This is a Gate 2 prerequisite, and the deck says "Cost: not yet estimated in any project file". | C3-BIZ-09 |
| c9 | **Release and version policy**: tagged releases, semantic versions, and a rule that "shipped" refers to a rebuilt, self-tested bundle. | It determines what customers and investors may be told about the product state. | C3-BIZ-05, -16 |
| c10 | **Extend #3** to `outreach/collaborators.csv`, `outreach/OUTREACH_EMAILS.md`, `docs/ip/INVENTION_REGISTER.md` and `docs/ip/IP_STRATEGY.md` (self-assessed novelty weaknesses). | They are public now. | C3-BIZ-08, -23 |

---

## Summary

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 7 | C3-BIZ-01, -02, -03, -04, -05, -06, -07 |
| Medium | 11 | C3-BIZ-08, -09, -10, -11, -12, -13, -14, -15, -16, -17, -18 |
| Low | 5 | C3-BIZ-19, -20, -21, -22, -23 |
| **Total** | **23** | |

**Cycle-2 dispositions:**
- I disagree with **C2-BIZ-11** (the one-pager is stale again) and **C2-BIZ-24** (free evaluations keep the risk; see also IP-12).
- I partly agree with C2-BIZ-01, -02, -07, -13, -14, -18, -20 and -22.
- I agree with the rest.

**Checks that passed:**
- no GLP, Part 11 or regulatory-acceptance claim;
- no Gate 3 claim;
- no statement that anything was purchased, sent, submitted, signed or incorporated;
- no fabricated contact found (contacts carry source URLs);
- the deck prices match the five hypotheses;
- the financial figures in the decks, the one-pager and REVENUE_MODEL match `financial_model_outputs.json`;
- licensing code ships only a published test key, and `PRODUCTION_KEYS` is empty;
- every quality document is marked DRAFT and not executed or approved;
- the only AI mention in the decks is the team slide's red-flag disclosure, not branding.
