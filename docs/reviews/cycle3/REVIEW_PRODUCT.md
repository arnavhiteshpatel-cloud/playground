# OsteoQuant: product review, cycle 3

This review was produced by an automated reviewer agent, not by a qualified human expert.

| | |
|---|---|
| **Date** | 2026-11-28 |
| **Commit reviewed** | `b55c459` (HEAD at the time of writing). The review started at `4b28a5a`. While it ran, `07c4e22` and `67fc862` changed `ci.yml`, `pyproject.toml`, `io/readers.py`, `report/defectfill.py` and some tests. Findings are stated against `b55c459`. Line numbers refer to that commit. |
| **Perspectives** | software architect; security engineer; QA / test engineer; desktop UX for a micro-CT analyst and a study director |
| **Scope** | (1) the Response section of `docs/reviews/cycle2/REVIEW_PRODUCT.md` (C2-PRD-01…21); (2) changes since cycle 2: method binding and the new `advisor_threshold` default, report group statistics, signed validation records, the ONNX runtime and registry lock, job handlers, licensing, packaging and CI; (3) test quality; (4) UX |

## Method

- **Code reading** of these areas:
  - `pipeline.py`, `advisor/integration.py`;
  - `desktop/{services,support,dialogs,main_window,project,report_integrity,jobs}.py`;
  - `study/{db,handlers}.py`, `audit/log.py`, `api/bundle.py`, `api/app.py` (configuration model only), `cli.py`;
  - `report/defectfill.py`;
  - `ml/{validation_records,runtime,train,core}.py`;
  - `licensing/{core,keys}.py`, `tools/make_test_licence.py`;
  - `packaging/{build.py,check_bundle_licences.py,bundle_inventory.py,osteoquant_desktop.spec}`, `docs/desktop/PACKAGING.md`, `.github/workflows/{ci,desktop-release}.yml`;
  - user documentation where it describes defaults.
- **Probes.** Six throw-away scripts, run outside the repository, each under 25 s of CPU.
  - Each probe used a temporary project, `OQ_MODEL_DIR` pointing to an empty temporary folder (so `models/` was never read or written), and temporary `HOME` / `XDG_CONFIG_HOME`.
  - Each probe calls the same public service functions the desktop UI calls. The Evidence fields below describe each probe precisely enough to repeat it.
- **Tests run:**
  - `pytest tests/desktop/test_cycle2_fixes.py`: **22 passed** in 52 s.
  - Single-function checks of `report.defectfill.group_stats` / `write_csv`, using the bundle from `tests/test_report_bounds.py::_supported_bundle`.
  - The full suite was not run (CPU budget).
- **Headless UI** (`QT_QPA_PLATFORM=offscreen`):
  - setup: demo project from `desktop.demo.build_demo_project`, `MainWindow` signed in as the demo analyst, one scan given a record in the format of the previous release (see C3-PRD-01);
  - screenshots in `docs/reviews/cycle3/screens/` (`c3_01` … `c3_05`).
- **Not done:** no PyInstaller build, no training, no Windows or macOS run. The macOS licence-check gap was shown with a synthetic folder layout.

## Severity scale

- **Critical**: wrong numbers presented as supported or validated in normal use with no special access, or remote compromise. Blocks any release.
- **High**: can mislead a sign-off, mis-attribute data, or defeat a stated control. Needs either an upgrade path or local access that every user of the application has.
- **Medium**: a control works only partly; or data, attribution or evidence can be degraded under realistic use; or a CI/packaging gap lets such regressions ship.
- **Low**: hardening, hygiene, clarity.

## (a) Verification of the cycle-2 dispositions

"Agree" means that the stated disposition matches what the code and tests show at `b55c459`.

| ID | Response disposition | Cycle-3 verdict | Agree? | Evidence |
|---|---|---|---|---|
| C2-PRD-01 | fixed | **verified** | yes | <ul><li>Specimens are joined by `(scan_id, segmentation_id)` and an unmatched specimen stops the report (`desktop/services.py:988-1000`).</li><li>One read transaction: `Store.snapshot()` (`study/db.py:181-183`).</li><li>`latest_measurements` has `ORDER BY`.</li><li>The UI refuses to generate a report while analysis, save or import jobs run (`main_window.py:1064-1068`).</li><li>`test_c2_01_*` pass.</li><li>Caveat: the snapshot test's `sleep(0.3)` can pass vacuously under load (C3-PRD-19).</li></ul> |
| C2-PRD-02 | fixed | **verified** | yes | <ul><li>`test_c2_02_*` passes. Dialogs in their own event loop are rejected, other windows are hidden, and the input filter blocks clicks and keys.</li><li>Not verifiable headless: native OS file dialogs on Windows/macOS while locked.</li></ul> |
| C2-PRD-03 | fixed | **verified** | yes | <ul><li>`test_c2_03_*` pass: forced blinding for roles without `unblind`, locked toggle, re-authenticated `study.unblind`.</li></ul> |
| C2-PRD-04 | fixed | **partially fixed** | **no** | <ul><li>Fixed: a naive edit of the bundle, or of the bundle plus the database hash, is refused (test).</li><li>Not fixed: `report_integrity.generate_event` (`:24-29`) takes the *latest* `report.generate` event, because `audit.events` orders by `seq DESC`. Appending a forged event with the new hash defeats the check.</li><li>Probe 4: TV edited to 999.999, DB hash updated, matching event appended with `AuditLog.record`. `verify_chain().ok` is True and `render_signed_report` produced a signed copy containing 999.999.</li><li>See C3-PRD-03.</li></ul> |
| C2-PRD-05 | fixed | **verified** (same file-level caveat as C2-PRD-04) | yes | <ul><li>Approval re-hashes the PDF; `review_status` is stored in the database; a missing bundle fails closed (`test_c2_04_05_*`, `test_c2_05_*`).</li><li>The PDF hash is compared with the same appendable `report.generate` event.</li></ul> |
| C2-PRD-06 | fixed | **verified, with caveats** | yes | <ul><li>One approval per person, and authors are excluded (test).</li><li>Caveat 1: authorship is read from the plain `segmentations.created_by` / `rois.created_by` columns (`report_integrity.py:89-112`), which are not bound to the chain.</li><li>Caveat 2: an administrator can still sign as "Customer approver" (`services.py:769-770`). The cycle-2 suggestion to restrict that role was not adopted, and this is not stated.</li></ul> |
| C2-PRD-07 | fixed | **verified** | yes | <ul><li>`test_c2_07_*` pass; `require_user()` re-validates before every service call.</li></ul> |
| C2-PRD-08 | fixed | **verified** | yes | <ul><li>`test_c2_08_*` passes.</li><li>The forced change runs only in the interactive sign-in (`main_window.py:644`). The programmatic `open_project(folder, user, pw)` path skips it, but only tests and screenshots use that path.</li></ul> |
| C2-PRD-09 | fixed | **partially fixed** | **no** | <ul><li>Fixed: a role edited in the database alone is detected (test).</li><li>Not fixed: `audited_user_state` (`db.py:262-279`) does not check who recorded a `user.role_change`, so a self-recorded event is accepted.</li><li>Probe 3: `UPDATE users SET role='admin'`, then `AuditLog(con).record('user.role_change', ana, org, 'user', ana, {...new_role:'admin'})`. Afterwards: `login('ana')` returns True, role `admin`, `can('manage_users')` and `can('unblind')` are True, `verify_chain().ok` is True, `user_record_problem` returns None.</li><li>See C3-PRD-03.</li></ul> |
| C2-PRD-10 | fixed | **verified for revision, import and report** | yes | <ul><li>`test_c2_10_*` (3 tests) pass.</li><li>The analysis path (`study/handlers.py:job_analyze`), which the finding did not name, still writes rows before data (C3-PRD-16).</li></ul> |
| C2-PRD-11 | fixed | **verified** | yes | <ul><li>`test_c2_11_*` passes: 3 writers including a second connection, contiguous versions.</li><li>Per-scan job serialisation was not added; it is not needed for version integrity.</li></ul> |
| C2-PRD-12 | fixed | **verified for missing or unknown advisor output** | yes | <ul><li>`test_c2_12_*` passes.</li><li>A *recognised but stale* status (written before method binding, or by an older advisor) is still trusted (C3-PRD-01).</li></ul> |
| C2-PRD-13 | open (library) | **partially fixed; disposition text is stale** | **no** | <ul><li>Commit `c94f505` (before the response commit `6658fd2`) made records Ed25519-signed, so "open" is out of date.</li><li>The new control can be bypassed without any signature (C3-PRD-02).</li><li>Test-key-signed records are accepted (C3-PRD-05).</li><li>A record is bound to the wrong artefact hash for ONNX (C3-PRD-06).</li><li>A corrupt file still raises out of `pipeline.analyze` (C3-PRD-15).</li></ul> |
| C2-PRD-14 | fixed (except event order) | **verified** | yes | <ul><li>Test passes: no `scan*_seg*.png` is written, and the blinded CSV has no file hash.</li><li>The import-order leak via chain order remains, as declared.</li></ul> |
| C2-PRD-15 | fixed | **verified** | yes | <ul><li>`test_c2_15_*` passes.</li></ul> |
| C2-PRD-16 | fixed | **verified** | yes | <ul><li>The test re-verifies every CSV row from the file.</li><li>The `audit.export` hash lives in the same appendable chain (C3-PRD-03).</li></ul> |
| C2-PRD-17 | fixed | **verified** | yes | <ul><li>`test_c2_17_*` passes: a typed reason is required, and acceptance by the creator is refused.</li></ul> |
| C2-PRD-18 | fixed | **verified** | yes | <ul><li>Test passes; code at `licensing/core.py:186-189, 232-242, 261-269`.</li></ul> |
| C2-PRD-19 | open (Low) | **still open** | yes | <ul><li>`LicenceStatus.has` has no caller (`grep "\.has("`).</li><li>There is no `issued > today` check (`core.py:199-215`) and no persisted last-seen date.</li></ul> |
| C2-PRD-20 | open (Low) | **still open** | yes | <ul><li>`probe_source` / `_write_store` (`services.py:168-224, 287`) never call `check_safe_input`.</li></ul> |
| C2-PRD-21 | open (Low) | **fixed after the response** | yes (was open) | <ul><li>`67fc862` removed both stale Windows skips (`tests/test_ml_phantom.py:47`).</li></ul> |
| UX-07 (cycle-1, "fixed") | fixed | **partially fixed** | **no** | <ul><li>Depends on C2-PRD-04 (see above).</li></ul> |
| D-6 (dossier) | open (library) | **partially fixed** | **no** | <ul><li>As for C2-PRD-13.</li></ul> |
| ARC-01…06 (cycle-2 "partially fixed") | *no disposition in the response* | **mixed** | n/a | <ul><li>ARC-01: verified remediated. `models/registry.json` gives `unet_synth_ft_dog_k1/k3` parent `unet_noctx_s0` and provenance including `synthetic`.</li><li>ARC-03: still open. `save_model` replaces an existing name (`ml/train.py:200`, `:217`).</li><li>ARC-06: still open. The ONNX output channel count is never checked (`pipeline.py:103-108`).</li><li>ARC-02, 04, 05: not re-checked.</li></ul> |

## (b) New findings

### C3-PRD-01: Stored support decisions are trusted at read time, so pre-binding multi-Otsu results stay "supported"

- **Severity:** High.
- **Perspective:** architect, UX.
- **Location:**
  - `pipeline.py:196, 205-225`: binding happens only inside `analyze`;
  - `advisor/integration.py:174-176`: `measurement_support()` returns the stored statuses;
  - `desktop/support.py:64-92`;
  - `api/bundle.py:118-121`;
  - `osteoquant/__init__.py` (`__version__ = "0.1.0"`, unchanged across the behaviour change).

**Evidence.**
- `bind_support_to_method` runs once, when an analysis is computed. Every reader trusts the stored `measurement_support.endpoints[*].status`: the Results view, the Review detail, `_enforce_support`, the report bundle and the CSV.
- The previous release defaulted to multi-Otsu (`git show 1fab377:osteoquant/desktop/services.py:445`, `"segmentation": "multiotsu"`).
- Every project analysed with it therefore holds advisor statuses that were never bound to the method. Those statuses keep showing as before after the upgrade.
- There is no migration or re-check, and stored records cannot be told apart:
  - the software version is still `0.1.0`;
  - `method_binding` is not written for `advisor_threshold` results either (`pipeline.py:213-214` returns early).

Probe 1:
1. HA phantom 40×56×56, 4 weeks.
2. `analyze_scan(... segmentation="advisor_threshold")` and `(... "multiotsu")`. Result: binding works for new runs (multi-Otsu → every tissue endpoint `not_supported`).
3. The multi-Otsu measurement row was then rewritten in the previous release's form: same advisor output, `segmentation.method = "multiotsu"`, no `method_binding`.

Observed:
```
--- multiotsu record as stored by the previous release: method=multiotsu binding=None
   advisor statuses: {'total_mineral_volume': 'supported', 'mineral_fraction_of_defect': 'supported',
                      'residual_graft_volume': 'supported', 'graft_fraction_of_defect': 'supported', ...}
   desktop residual_graft_fraction  value=11.874 status=flagged   reasons=[QC verdict 'review' ...]   <- no method reason
   desktop mineralized_fraction     value=34.64  status=flagged
   report bundle: method multiotsu | mineralized_fraction 0.3464 | support {'mineral_fraction_of_defect': 'supported', ...}
```

The headless run reproduces this in the UI:
- `c3_02`: R02 has Method "Multi-Otsu (classical)" and Mineralised 32.3 %.
- The report and CSV give R02 `multiotsu … 0.323 supported`, and R02 enters the Treatment group mean.

The vendor's own release notes say advisor 1.3.3 and 1.4.0 "supported some measurements that failed" (`docs/user/RELEASE_NOTES_GEN2.md:130`). Records from those versions are also still shown as supported.

**Fix.**
1. Make support a pure function evaluated at read time, from stored facts: method, `advisor_version`, a new `support_rules_version`, and the validation record. Apply it in `support.measurement_support`, in `_enforce_support` and in `bundle_from_store`.
2. Treat any record that is not bound under the current rules as **not assessed**, with the reason "analysed with an earlier rule set or a non-validated method; re-analyse". Offer *Re-analyse affected scans* when a project is opened.
3. Always write `method_binding`, including for `advisor_threshold`.
4. Bump `__version__` on behaviour changes and record the rules version in every measurement and report.
5. Add an upgrade test that loads a pre-binding fixture project.

### C3-PRD-02: Validation-record signature bypassed by an unsigned file (string match on the reason)

- **Severity:** High.
- **Perspective:** security.
- **Location:**
  - `pipeline.py:215`: `validated = "qualifying validation record" in str(seg_info.get("validation_record", ""))`;
  - `ml/validation_records.py:79-80`: the error message embeds the unsigned `key_id`.

**Evidence.** The binding decides "validated" by searching the human-readable reason for a phrase, not by using the boolean that `validated_for` returns. `load_records` echoes the attacker-controlled `key_id` into its `RuntimeError` message, and `validated_for` returns that message as the reason.

Probe 2:
- Setup: a tiny 4-class ONNX network (1×1×1 Conv) registered in a temporary `OQ_MODEL_DIR`; `material="ha"`, 4 weeks.
- The forged file is an unsigned `validation_records.json`:
  ```json
  {"format":"oq-validation-records-1","key_id":"qualifying validation record","payload":"{}","signature":"AA=="}
  ```

Observed:
```
--- ONNX model, no validation_records.json
   graft endpoint statuses: {'residual_graft_volume': 'not_supported', 'graft_fraction_of_defect': 'not_supported'}
--- ONNX model, unsigned records file with key_id='qualifying validation record'
   validation_record: 'validation records signed with an untrusted key (qualifying validation record)'
   graft endpoint statuses: {'residual_graft_volume': 'supported', 'graft_fraction_of_defect': 'supported'}
   reported residual graft fraction: 0.110
```

Anyone who can place a file in the models folder can make an unvalidated learned model's graft volume show as supported. That covers a user-writable one-folder install, an administrator, or a support bundle. The supported number then flows into a signed report.

**Fix.**
- Carry the boolean: set `info["validation_ok"] = ok` and make `bind_support_to_method` use only that.
- Never put unsigned envelope fields in messages; report "untrusted key", not the key id.
- Add a test with a hostile `key_id`.

### C3-PRD-03: The audit chain can be extended by anyone with write access, so the cycle-2 integrity fixes can be bypassed by any user

- **Severity:** High.
- **Perspective:** security.
- **Location:**
  - `audit/log.py:1-9, 47-80`: unkeyed SHA-256 chain; INSERT is allowed;
  - `study/db.py:262-291`: `audited_user_state` ignores the actor;
  - `desktop/report_integrity.py:24-29, 115-123`: latest event wins;
  - `audit/log.py:105-113`: `anchor()` exists but the desktop never stores one.

**Evidence.**
- The application runs as the user, so every user necessarily has write access to `osteoquant.db`.
- The chain stops edits and deletions, but a correctly hashed *append* is indistinguishable from a real event. The module docstring ("Anyone who bypasses the triggers … breaks the chain") does not hold for appends.
- Probe 3 (role escalation, C2-PRD-09) and probe 4 (forged signed copy, C2-PRD-04) are described in section (a). Both end with `verify_chain().ok == True`.
- The same technique also defeats three more controls, all of which read appendable or unbound state:
  - the signature-role cross-check (`audited_signature_roles`);
  - the `audit.export` hash;
  - the report-author exclusion (C2-PRD-06, which reads `created_by`).

**Fix.** A local file cannot defend itself, so:
1. **Anchor externally and automatically.** Write the chain head (seq + hash) outside the project folder at every sign-off and every export: the per-user config dir plus a printed field in every PDF. Verify against the last anchor at project open.
2. **Bind authority.** Accept `user.role_change`, `user.activate` and `user.deactivate` only when the actor was an administrator in the audited state at that sequence number and differs from the subject. Accept a `report.generate` event only from the report's recorded creator, and only one per report.
3. **Sign security events** with a per-user key derived from the password (or kept in the OS keystore), so that forging an administrator's event requires that administrator's password.
4. **State the residual limitation** in `docs/user/DATA_PROTECTION.md` (OS folder ACLs, read-only reviewer shares).

### C3-PRD-04: Hand-edited label revisions inherit the measurement support of the automatic result

- **Severity:** Medium.
- **Perspective:** architect, UX.
- **Location:**
  - `desktop/services.py:717-724`: support is carried over to edited labels;
  - `desktop/services.py:736`: `method=base["method"]` is stored for a `corrected` version.

**Evidence.**
- Support is validated for the advisor threshold's *labels* (S1b/S1c/S1H*). A revision may repaint any number of voxels, yet it keeps the base version's endpoint statuses, and its segmentation row still says `advisor_threshold`.
- Probe 1(c): background in a 12-slice slab of the defect was painted as graft. Graft voxels went from 3 427 to 29 335.
  - `residual_graft_fraction` went from 11.85 % to **35.95 %**, and its status stayed the same.
  - The only reasons shown are the QC "review" and ROI-acceptance reasons. After a second person accepted the ROI, only the QC reason remained.
  - No reason mentions the manual edit, and `method_binding` is absent.

**Fix.**
- Store the method of a revision as `corrected:<base method>`.
- Mark advisor-dependent endpoints of a corrected version *flagged* at least, with the reason "manually edited labels: outside the validated method". Make *not supported* a policy option.
- Show the edit volume next to the endpoint in Results and in the report.

### C3-PRD-05: Validation records trust the licence test key, and test-signed evidence is not labelled

- **Severity:** Medium.
- **Perspective:** security.
- **Location:**
  - `ml/validation_records.py:78-81`: `_is_test` is ignored;
  - `licensing/core.py:137-144`;
  - `licensing/keys.py`: the test seed is published;
  - `docs/user/LICENSING_AND_ADMIN.md:75-83`: tells users to set `OSTEOQUANT_ACCEPT_TEST_LICENCES=1`.

**Evidence.**
- Probe 2(3) signed a record (`in_vivo`, n=12, `evidence_location="forged with the public test seed"`) with the published test key and set the variable. Result:
  - `validated_for → (True, 'qualifying validation record: in_vivo, n=12, …')`;
  - the ONNX model's graft endpoints became `supported`.
- A licence signed with the test key is watermarked "TEST LICENCE", but nothing marks test-signed *evidence*.
- One key set signs two different things, licences and scientific evidence. The format string is not inside the signed bytes, so there is no domain separation.
- Records carry no sequence number or expiry, so an older signed file can be restored after a record is withdrawn (rollback).
- `PACKAGING.md:207` suggests generating the production key with the *test* tool (`--keygen`), which writes an unencrypted `test_private.pem`.

**Fix.**
- Use a separate `EVIDENCE_KEYS` trust store with no test key in production builds, or reject `_is_test` records unless an explicit developer flag is set, and label the resulting support "TEST EVIDENCE".
- Put `format`, `purpose` and a monotonically increasing `sequence` inside the signed payload. Persist the highest sequence seen and refuse lower ones.
- Provide a production key-generation procedure that writes an encrypted key.

### C3-PRD-06: An ONNX model's validation record is bound to the PyTorch checkpoint hash, not to the bytes that run

- **Severity:** Medium.
- **Perspective:** security, architect.
- **Location:** `pipeline.py:100-101, 185` (`model_sha256 = reg.get("sha256")` on the ONNX path); `ml/runtime.py:55-62`.

**Evidence.**
- `OnnxSegmenter` verifies the ONNX bytes against the unsigned registry's `onnx_sha256`. `validated_for` is then called with the registry's `sha256`, which is the `.pt` hash.
- Probe 2(4): a different ONNX network (it labels nearly everything as graft) replaced `tiny.onnx`, and only `onnx_sha256` was updated. Result: the record still qualified, and the reported graft fraction went from **0.110 to 0.897**, still "supported".
- The same happens legitimately: `export_onnx` re-exports update `onnx_sha256` and inherit the record.

**Fix.**
- Validate the deployed artefact: put `onnx_sha256` (and `onnx_int8_sha256`) into `ValidationRecord`, and pass the hash of the bytes actually loaded.
- Longer term, sign the registry entries (provenance, licence tag, hashes) with the evidence key, so the synthetic chip and the licence tag cannot be edited either.

### C3-PRD-07: The report library computes group statistics and the CSV from refused values whenever the bundle contains them; a new test claims the opposite

- **Severity:** Medium.
- **Perspective:** QA, architect.
- **Location:**
  - `report/defectfill.py:148`: `row[key] = bounded_describe([_get(s["metrics"], key) …])`;
  - `report/defectfill.py:161-166`: comparisons;
  - `report/defectfill.py:209-223`: `write_csv`;
  - `tests/test_report_bounds.py:147-163`.

**Evidence.**
- `group_stats` and `write_csv` ignore `measurement_support`: they drop only values that are `None` or non-finite. Only the per-specimen PDF table consults the status (`_fmt_support`).
- The new test `test_report_prints_refused_values_as_not_measured_with_reasons` builds a bundle whose refused new-bone values are numbers, and asserts that "no refused new-bone value leaks into the PDF". It checks individual values only. Re-running `group_stats` and `build_pdf` on the test's own bundle gives:
  ```
  Ctrl new_bone_volume mean (refused values): 7.2665 n= 3     -> "7.267" printed in PDF: True
  Tx   new_bone_volume mean (refused values): 7.5666 n= 3     -> "7.567" printed in PDF: True
  comparisons on refused endpoint: new_bone_volume_mm3 p=0.00195, new_bone_fraction p=0.00195
  CSV row: ...,pass,7.2137,0.9017,... ,not_supported,...   (refused raw value next to its status)
  ```
- The desktop path is safe today, because `reported_metrics` and `_enforce_support` null the values first. The renderer itself gives no guarantee, though. Any caller that passes raw metrics would publish group means and p-values of refused endpoints: the web API's `job_report`, sample-report scripts, or future code.

**Fix.**
- Make `build_pdf` / `group_stats` / `write_csv` enforce the rule themselves: a value whose endpoint status is `not_supported` (or absent, when the bundle declares support) is treated as `None` everywhere.
- Extend the test to assert that no group mean, CI or p-value is computed for a refused endpoint, and that the CSV cell is empty.

### C3-PRD-08: Exports contradict the application: values the Results view flags are "supported" in the CSV and plain numbers in the PDF

- **Severity:** Medium.
- **Perspective:** UX, QA.
- **Location:** `report/defectfill.py:190-200` (`_support` uses only the advisor status), `:209-223`; `desktop/services.py:964-985` (`_enforce_support` only nulls NOT_SUPPORTED / NOT_ASSESSED).

**Evidence.**
- In the headless run every scan is "⚠ flagged" in Results, with QC verdict "review" and automatic ROI awaiting acceptance (`c3_02`, `c3_03`).
- The generated CSV says `class_volumes.mineralized_fraction__support = supported` for all five specimens.
- The PDF prints plain numbers without "(c)". The ROI acceptance state appears nowhere in the report.
- A reader of the CSV, which is the file a study director's statistician uses, cannot see the caution the analyst saw.

**Fix.**
- Export the *desktop* status (supported / flagged / not supported / not assessed), with its reasons, in the CSV, and mark flagged values in the PDF (for example "‡").
- Add a "ROI" column (automatic accepted / manual accepted / awaiting) to report section 6.

### C3-PRD-09: CI does not block desktop or licensing regressions caused by library changes

- **Severity:** Medium.
- **Perspective:** QA.
- **Location:**
  - `.github/workflows/ci.yml:82, 87`: `--ignore=tests/desktop`;
  - `.github/workflows/ci.yml:93-98`: desktop tests with `continue-on-error: true`;
  - `.github/workflows/desktop-release.yml:20-25`: PR path filter.

**Evidence.**
- The regression tests for C2-PRD-01, 04, 05, 09, 11, 12 and 16, and all licensing tests, live in `tests/desktop/`. `tests/desktop/test_licensing.py` is the only licensing test file.
- In `ci.yml` those tests never block.
- `desktop-release.yml` runs them blocking only for PRs that touch `osteoquant/desktop/**`, `licensing/**`, `packaging/**` or `tests/desktop/**`.
- The code those tests protect lives largely elsewhere: `study/db.py`, `audit/log.py`, `api/bundle.py`, `pipeline.py`, `advisor/**`, `report/**`, `ml/validation_records.py`. A change there that breaks a desktop control merges green.
- Coverage gates exclude the desktop. The 95 % gate does not include `advisor`, `pipeline`, `report`, `licensing` or `ml/validation_records`.
- `RELEASE_READINESS.md:16` confirms that desktop tests ran for the first time in run 59, as a non-blocking step.
- At the start of this review (`4b28a5a`) the 3.11 jobs could not install (`numcodecs 0.17.1` requires Python ≥ 3.12; checked with `importlib.metadata`), and `cryptography` was not a core dependency although the core pipeline imports it. Both were fixed in `07c4e22`.

**Fix.**
- Make the desktop and licensing tests blocking in `ci.yml` on at least one OS.
- Move `test_licensing.py` and the non-GUI parts of `test_cycle2_fixes.py` to `tests/`.
- Remove the path filter, or extend it to every module the tests import.
- Add the support-critical modules to the 95 % gate.

### C3-PRD-10: The release pipeline works in practice only on Linux, and the macOS Qt licence check passes vacuously

- **Severity:** Medium.
- **Perspective:** QA, licensing.
- **Location:**
  - `packaging/check_bundle_licences.py:46-48, 61-73`;
  - `packaging/osteoquant_desktop.spec:42-44`;
  - `packaging/bundle_inventory.py:161-168, 204-209`;
  - `packaging/build.py:141-142`.

**Evidence.**
- **macOS:**
  - Qt ships as `QtCharts.framework/Versions/A/QtCharts`, a binary with no suffix and no "6" in the name. The checker considers only `.so/.dylib/.dll/.pyd` files whose names contain `Qt6`.
  - The spec filter also matches `"Qt6Charts"`, `"Qt6Graphs"`, `"Qt6Coap"`, `"Qt6Mqtt"` by the "Qt6" name, which misses `QtCharts.framework`.
  - Synthetic layout test: `QtCore`, `QtCharts` and `QtVirtualKeyboard` frameworks plus `PySide6/QtCharts.abi3.so` gave `Qt modules: (empty)` and `LICENCE CHECK PASSED … exit=0`.
  - Nothing asserts that at least `Core` was found.
- **Windows:**
  - Top-level `python313.dll`, `VCRUNTIME140.dll` and the stdlib `_ssl.pyd` etc. reach the `else` branch, where owners come only from `dpkg` on Linux. They become UNMAPPED.
  - The PSF licence is looked up in `…\Lib\LICENSE.txt`, but on Windows it sits one level up.
  - So `build.py:141-142` exits before the licence check, by construction.
  - `bundle_inventory.py`'s docstring and `BLOCKERS.md` B-013 admit that Windows and macOS were never built, yet the workflow and `PACKAGING.md:150-151` say "the CI build runs the same check on each platform".

**Fix.**
- Match Qt modules by framework (`Qt(\w+)\.framework`) and by PySide module (`PySide6/Qt(\w+)\.(abi3\.so|pyd)`), and fail when no `Core` module is found.
- Add platform owners for Windows/macOS (Python runtime, MSVC redistributable, OpenSSL).
- Run a dry inventory on Windows and macOS runners before claiming parity.

### C3-PRD-11: Release workflow: PR builds can use the signing secrets, and on a public repository they publish application archives

- **Severity:** Medium (latent: no secrets are configured yet).
- **Perspective:** security, licensing.
- **Location:** `.github/workflows/desktop-release.yml:20-25, 49-50, 82-120, 122-131`; `BLOCKERS.md` B-013.

**Evidence.**
- `pull_request` runs from branches of the same repository receive repository secrets.
- The job first builds with the PR's own `packaging/`, `tests/` and `osteoquant/` code, then signs `packaging/dist/OsteoQuant/*.exe` (and the `.app`) with the company certificate, on the same runner.
- A malicious or compromised branch can therefore get its own binary Authenticode-signed or notarised. It can also leave a process behind that reads the `.pfx` / `.p12` written to `RUNNER_TEMP`.
- The header says the workflow "never publishes a release". On a public repository, though, every PR-triggered run uploads `OsteoQuant-desktop-*` archives that any GitHub user can download for 14 days (B-013 says so). These archives:
  - are distributed copies, with the LGPL source-offer obligations that implies;
  - are packed under the same conditions as the archive `BLOCKERS.md` B-016 marks "do not distribute".

**Fix.**
- Sign only on `push: tags` or `workflow_dispatch` from a protected branch, inside a GitHub *environment* with required reviewers.
- Never sign in a `pull_request` run.
- For PR runs, upload only test results and the licence report, not archives, or make the repository private.

### C3-PRD-12: The analysis dialog overstates validation and does not make clear what carries support

- **Severity:** Medium.
- **Perspective:** UX (analyst, study director).
- **Location:** `desktop/dialogs.py:175-193`; `desktop/services.py:542` ("Advisor threshold (measurement-support validated)" in the Method column); `scripts/check_claims.py:26-28` (scans documents only, not application strings).

**Evidence** (`c3_01`):
- The combo box reads "Advisor threshold (validated with measurement su…" (truncated). The user's own documentation says "**Validation (simulation only)** … evidence of internal safety, not of accuracy on real scans" (`MATERIALS_AND_SUPPORT.md:12`), and the report says "computational (stage A) — no physical or in-vivo validation".
- Only the multi-Otsu item says "no measurement support". The U-Net items ("U-Net unet_noctx_s0 (locked model) — SYNTHETIC-TRAINED") do not say that tissue endpoints will be refused.
- The dialog has no line stating that only the advisor threshold carries support.
- *Graft material* defaults to "Unspecified", which refuses every graft and new-bone endpoint. It does not pre-fill from the study's "Graft material(s)" ("beta-TCP" in the demo).
- The Method column repeats "measurement-support validated" on every row (`c3_02`).

**Fix.**
- Label the option "Advisor threshold — the only method with measurement support (validated in simulation)", with a tooltip.
- Add "(no measurement support)" to every other method, including the U-Net items.
- Pre-select the material from the study, and warn when it is unspecified.
- Run the claims checker over UI strings in `osteoquant/desktop/*.py`.

### C3-PRD-13: The entry points disagree about the default method, and the web API cannot select the validated one

- **Severity:** Medium.
- **Perspective:** architect.
- **Location:** `cli.py:36` (`--seg` default `multiotsu`); `api/app.py:133` (`segmentation` default `multiotsu`, pattern `^(multiotsu|ctan_style|unet:…)$`, and `extra: forbid` with no `material` or `healing_weeks` field).

**Evidence.**
- The pipeline and the desktop default to `advisor_threshold`. The CLI and the web API default to multi-Otsu.
- The API schema rejects `advisor_threshold`, `onnx:` and `material`. Every API analysis therefore has all tissue endpoints refused, with no way to obtain the validated method.

**Fix.**
- Make one shared defaults object the source for the CLI, the API and the desktop.
- Allow `advisor_threshold`, `onnx:<name>`, `material` and `healing_weeks` in `AnalyzeConfig`.
- Add a test asserting that all three entry points agree.

### C3-PRD-14: Test gaps on the new critical paths: plausible mutations survive

- **Severity:** Medium.
- **Perspective:** QA.
- **Location:** `tests/test_advisor.py:322-330`, `:230-245`; `tests/test_report_bounds.py:94-108` (cycle-2 version); `tests/desktop/` (no default-method test).

**Evidence** (reasoned; no mutation tool was run):

| Change to the code | Test that should catch it | Survives? |
|---|---|---|
| `validated = "qualifying" in …` (broader), or exploiting the reason text (C3-PRD-02) | `test_pipeline_binds_support_to_method` never passes a `validation_record` | survives |
| Delete `support["method_binding"] = …` | none | survives |
| Remove the `tissue_mineral_density` exemption | none | survives |
| Swap the first two `AnalysisDialog.seg` items, or change `ANALYSIS_DEFAULTS["segmentation"]` | none asserts the default | survives |
| `valid = comps` (Holm over every test, including NaN p) | `test_group_stats_ignore_refused_values_and_uncomputable_tests` has one finite comparison and no NaN-p case | survives |
| `"holm"` → `"bonferroni"` | same test (m = 1) | survives |
| `n_specimens < 8` → `< 1`, or drop the p95-error check in `ValidationRecord.qualifies` | no record with n < 8 or p95 > 0.15 | survives |
| Display layer re-binds nothing for old records (C3-PRD-01) | no upgrade fixture | survives |

A probe confirmed the NaN-p path works today (`p=nan → p_holm None`), but no test pins it.

**Fix.** Add tests for each row above. For report statistics, assert the exact adjusted p-values for 3+ comparisons including one with NaN p. Add a pre-binding fixture project.

### C3-PRD-15: A corrupt `validation_records.json` aborts every learned-model analysis

- **Severity:** Low.
- **Perspective:** robustness.
- **Location:** `ml/validation_records.py:75` (`json.loads(p.read_text())` outside the `RuntimeError` handling), `:110-111`, `:117` (`ValidationRecord(**d)`).

**Evidence.** Probe 2(2): file content `{not json` gave `validated_for raised JSONDecodeError`, which propagates out of `pipeline.analyze` for any `onnx:` or `unet:` analysis with a material set. Non-UTF-8 bytes would raise `UnicodeDecodeError`. A signed record with an unexpected key raises `TypeError` (the second half of C2-PRD-13).

**Fix.** Make `validated_for` total: any exception gives `(False, "validation records unreadable: …")`, plus a test.

### C3-PRD-16: Analysis outputs are not written transactionally (the C2-PRD-10 pattern remains in `job_analyze`)

- **Severity:** Low.
- **Perspective:** robustness.
- **Location:** `study/handlers.py:54-69`.

**Evidence.**
- The order of writes is: ROI row, segmentation row, labels, `roi_current`, `roi_v{v}`, measurement. There is no transaction and no cleanup.
- Probe 6 made the second `write_labels_zarr` call raise `OSError(28, "No space left on device")`. Result:
  - segmentation versions `[(1,'seg_v1'), (2,'seg_v2')]`;
  - measurements `{1: 1, 2: 0}`;
  - scan status `analyzed`.
- The viewer then opens v2, while Results and reports still use v1's numbers.

**Fix.** Apply the C2-PRD-10 pattern: write data under unique keys first, insert the ROI, segmentation and measurement rows in one transaction last, and remove the arrays on failure.

### C3-PRD-17: Report readability for a study director

- **Severity:** Low.
- **Perspective:** UX.
- **Location:** `report/defectfill.py:72-90, 320-345, 360, 364, 482-510`; `desktop/services.py:984` (labels mixed into `measurement_support`).

**Evidence** (`c3_04_report_page1/3/6`, demo report):
- The group summary shows "—" for endpoints refused for every animal, with no count or reason ("not measured, 0 of 2" would be clear).
- The support table has **51 "not measured" rows for 5 specimens**, repeating the same long reasons. One example: "physics model (NIST, assumed porosity) gives 1.12 vs knowledge base 1.41: profile uncertain".
- The table mixes advisor endpoint ids ("new bone thickness") with desktop labels ("Tb.Th (new bone)") for the same quantity.
- The overlay figures still colour new bone and graft separately for specimens where that split was refused (page 3).
- The comparison note says "Holm-adjusted across all comparisons" but adjusts only the computable ones.
- Comparisons that could not be computed are silently omitted, and at most 30 are shown with no notice.
- An animal with one refused and one measured scan contributes the measured scan's value without disclosure (probe: n = 1, mean 2.0).
- The audit excerpt shows user *ids* ("1") instead of names.

**Fix.**
- Use "n/m (0 of N)" in group cells.
- Group the support table per endpoint, with specimen lists and one plain-language reason; put the technical detail in an appendix.
- Use one endpoint vocabulary.
- Grey out, or merge to "mineral", the classes whose split was refused, and caption it.
- Correct the Holm wording, list omitted comparisons and say when the table is truncated.
- Disclose partial per-animal pooling.
- Show user names in the audit excerpt.

### C3-PRD-18: Customer documentation still says multi-Otsu is the default

- **Severity:** Low.
- **Perspective:** UX.
- **Location:** `docs/desktop/USER_GUIDE.md:165`, `docs/user/QUICK_START.md:69`, `docs/user/GLOSSARY.md:45`, `docs/user/INSTALLATION.md:46`, `docs/user/SCIENTIFIC_METHODS.md:34`. The last contradicts `SCIENTIFIC_METHODS.md:169` in the same file.

**Evidence.** `grep -n -i "multi-otsu" docs/...` (lines above). Also, `MATERIALS_AND_SUPPORT.md:14` says other methods refuse "graft and new-bone endpoints", but the code also refuses total mineral (`pipeline.py:216-224`). No document tells users that results from earlier versions need re-analysis (C3-PRD-01).

**Fix.** Update the five places. Add an upgrade note: "results analysed before advisor 1.4.2 / with multi-Otsu are not supported; re-analyse".

### C3-PRD-19: Timing-dependent tests can pass vacuously or flake

- **Severity:** Low.
- **Perspective:** QA.
- **Location:** `tests/desktop/test_cycle2_fixes.py:118-135`; `tests/desktop/test_viewer_ux.py:165`.

**Evidence.**
- The snapshot test asserts `not done.is_set()` after `time.sleep(0.3)`. If the writer thread is scheduled late (a loaded runner), the test passes even when `snapshot()` does not block.
- `assert time.time() - t0 < 4.5` is a wall-clock upper bound on a GUI action.

**Fix.**
- Have the writer signal "about to write" with an Event before the assertion, then assert it is blocked; or use a deterministic lock probe.
- Replace wall-clock bounds with event-based waits.

### C3-PRD-20: No memory pre-flight for analysis; cancellation only between stages

- **Severity:** Low (code reading; not executed, because of the CPU budget).
- **Perspective:** robustness.
- **Location:** `study/handlers.py:22-29, 51`; `desktop/jobs.py:112-115` (2 workers); `pipeline.py:136-198` (6 progress points).

**Evidence.**
- Import and QC are memory-bounded (slab import, decimated QC), but `job_analyze` loads the whole volume, and two analyses can run at once.
- On Linux, overcommit means a too-large analysis is usually killed by the OOM killer rather than raising `MemoryError`. The friendly message in `messages.py:28` never appears, and unsaved edits are lost.
- *Cancel* takes effect only at the next pipeline stage. Thickness metrics on a large volume can run for minutes.

**Fix.**
- Estimate peak memory (about 6–8 × the volume in float32) before submitting, refuse or queue when `psutil.virtual_memory().available` is insufficient, and serialise large jobs.
- Pass `ctx.check` into long loops such as local thickness.

### C3-PRD-21: No guard against older application versions opening newer projects; opening a project mutates it before sign-in

- **Severity:** Low.
- **Perspective:** architect, security.
- **Location:** `study/db.py:141-147`; `desktop/project.py:69-79`.

**Evidence.**
- `migrate()` applies newer migrations but never refuses a database whose `schema_version` is above `SCHEMA_VERSION`.
- An older build therefore opens a cycle-2/3 project and silently ignores newer controls such as `must_change_password`, bundle integrity records and forced blinding.
- `Project.__init__` runs `DESKTOP_SCHEMA` and `ALTER TABLE` before anyone signs in, so merely browsing a project folder modifies it.

**Fix.**
- Store a `min_app_version` in the database and the marker, and refuse (read-only at most) when the application is older.
- Defer schema changes until after a successful administrator sign-in, or record them in the audit trail.

### C3-PRD-22: Registry lock fallback breaks mutual exclusion; locked model names can still be overwritten

- **Severity:** Low.
- **Perspective:** architect.
- **Location:** `ml/train.py:249-258` (mkdir fallback); `ml/train.py:200, 217` (ARC-03).

**Evidence.**
- After 60 s of waiting, every waiter removes `.registry.lock.d` on every retry. `t0` is never reset, so two writers can hold the "lock" at once, and a concurrent `rmdir` raises `FileNotFoundError`.
- The fallback is reached only when neither `fcntl` nor `msvcrt` is importable, which is rare.
- `save_model` still overwrites `models/<name>.pt` and replaces the registry entry for an existing name, dropping `onnx_sha256`. This contradicts "locked model version".

**Fix.**
- Break a stale lock only once, atomically (rename the lock directory with a PID or timestamp check), and reset `t0`.
- Refuse `save_model` for an existing name unless `overwrite=True` is passed explicitly and audited.

## (c) Usability narrative (headless run)

- **Analysis dialog (`c3_01`).** The analyst who opens *Analyse* sees "Advisor threshold (validated with measurement su…" pre-selected. Nothing in the dialog body says that this is the only method whose numbers can be reported. Material is "Unspecified", although the study was created as beta-TCP. An analyst in a hurry would run with no material and get graft and new-bone "not measured" for every scan; the bottom note explains why only in general terms. The time-since-implantation control is clear.
- **Results (`c3_02`, `c3_03`).**
  - Strengths:
    - The ⚠ / ✖ status column, "not measured" cells and the per-endpoint reasons in the detail pane are understandable, and each endpoint carries its own reason.
    - The footer legend ("'not measured': no number is shown because the endpoint is not supported…") is good.
  - Weaknesses:
    - At 1500 px the endpoint columns start off-screen. The wide Method column ("Advisor threshold (measurement-support validated)", repeated per row) pushes them right.
    - The detail pane repeats the same QC sentence under every endpoint, so the single advisor reason per endpoint is hard to find.
    - The R02 row carries a result in the previous release's format (multi-Otsu). Its "Mineralised 32.3" looks exactly like the advisor-threshold rows, and no reason mentions the method (C3-PRD-01).
    - "auto · not reviewed" and "auto · awaiting acceptance" still sit side by side without explanation (cycle-2 note, unchanged).
- **Report (`c3_04_*`).**
  - Strengths:
    - The banners (synthetic, unreviewed, research use, evaluation watermark) are unambiguous.
    - Per-specimen "n/m" is clear.
    - The analysis-parameter table usefully lists method, thresholds, weeks and advisor version per specimen. It is the only place a careful study director could notice that R02 used `multiotsu`.
  - Weaknesses:
    - Group cells show "—" for refused endpoints.
    - The support section runs to 51 repetitive rows.
    - The figures colour a new-bone/graft split that the report says cannot be measured (C3-PRD-17).
    - The CSV calls every value "supported" although the application showed them as flagged (C3-PRD-08).
- **Reports tab (`c3_05`).** The separation-of-duties message under a disabled *Approve…* ("You generated this report…") is clear. The job title "Defect-fill report (study 1)" is fine.

## Summary

- **Critical:** 0.
- **High:** 3.
  - C3-PRD-01: stale stored support is trusted, so old multi-Otsu and old-advisor results stay "supported".
  - C3-PRD-02: an unsigned file defeats the validation-record signature.
  - C3-PRD-03: the audit chain can be extended, so the C2-PRD-04 and C2-PRD-09 fixes can be bypassed by any user.
- **Medium:** 11 (C3-PRD-04 … 14).
- **Low:** 8 (C3-PRD-15 … 22).
- **Total new findings:** 22.
- **Cycle-2 dispositions** (21 findings plus the affected cycle-1 rows):
  - Agree: 18. Of these, 14 are verified fixed (C2-PRD-01, 02, 03, 05, 07, 08, 10, 11, 12, 14, 15, 16, 17, 18), 1 is verified with caveats (C2-PRD-06), 2 are confirmed still open (C2-PRD-19, 20), and C2-PRD-21 was open at the time of the response and is now fixed (`67fc862`).
  - Disagree: C2-PRD-04 and C2-PRD-09 ("fixed", but only partially fixed: they can be bypassed by appending to the chain); C2-PRD-13 ("open (library)", stale: it was signed in `c94f505` and the signature can be bypassed); and consequently UX-07 and D-6.
  - ARC-01…06 received no disposition. ARC-01 is remediated; ARC-03 and ARC-06 remain open.
- **No claimed fix has regressed.** All 22 cycle-2 regression tests pass.
