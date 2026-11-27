# OsteoQuant Security Review

Scope: `osteoquant/` (API, study store, audit log, job runner, I/O, report), `web/static/`, `scripts/`. Review date 2026-11-27.
Method: manual code review plus benign local reproductions. All reproductions ran against local `Store` objects or local functions; no external hosts were contacted. The script is `/tmp/claude-0/-home-user/b184cf39-87b0-5bba-b79b-9f478d2dc224/scratchpad/review/poc_integrity.py`. The existing test suite passes (42 passed). No existing file was modified.

For the code-execution, file-read and resource-exhaustion findings (S-01 to S-04, S-09), the evidence given is the code path. Working exploit payloads were deliberately not built.

Severity scale: critical, high, medium, low, info.

---

## Findings

### S-01 — Arbitrary server file read through detached-header volume formats (critical)
- **Location:** `osteoquant/io/readers.py:412` (`nrrd.read`), `osteoquant/io/readers.py:447` (`sitk.ReadImage`); reached from the upload path `osteoquant/api/app.py:302-328`.
- **Description:**
  - The upload filter accepts `.nhdr` and `.mhd` names (`readers.py:68-72`).
  - pynrrd follows a `data file:` field. It accepts absolute paths unchanged and joins relative paths onto the header directory (checked in the installed `nrrd.reader.read_data`).
  - MetaImage `ElementDataFile` behaves the same way in SimpleITK.
  - Any analyst can therefore upload a small header whose voxel payload is any file readable by the server process. This includes `osteoquant.db`, which holds password hashes, session hashes and every tenant's data, and also other organisations' stores under `data/org*/`.
  - The bytes are then stored as the "image" and can be viewed through `/api/scans/{id}/slice`.
  - `file_sha256` covers only the header file, so provenance does not reveal the problem.
- **Evidence:** code path only. `read_nrrd` and `read_itk` never inspect `data file` or `ElementDataFile`, and `upload()` passes the user file straight to `read_volume`.
- **Fix:**
  - Reject detached headers at upload: refuse `.nhdr`/`.mhd`, or parse the header and require that the data-file field is absent, or is a bare filename inside the upload temp directory.
  - After resolving, require `Path(datafile).resolve()` to lie under the upload temp directory.
  - Run ingestion in a sandboxed worker with no access to the DB or the data directory.

### S-02 — Unsafe deserialization of model files named in the user-supplied analysis config (critical)
- **Location:**
  - `osteoquant/pipeline.py:72-74`: `rf:<path>` leads to `joblib.load(path)`.
  - `osteoquant/pipeline.py:80-83` and `osteoquant/ml/train.py:219-223`: `unet:<name>` leads to `load_model`. This uses `Path(name)` directly if it exists, or else `MODEL_DIR / f"{name}.pt"`, which allows `../`. It loads with `torch.load(..., weights_only=False)`.
  - `osteoquant/api/app.py:178-180,400-404`: `AnalyzeIn.config: dict` is forwarded without validation.
- **Description:**
  - Any user with `run` permission (analyst or admin) chooses `config.segmentation`. Pickle-based loading of an attacker-chosen path is code execution in the server process if a suitable file exists anywhere readable. Examples are shared mounts, other tenants' writable areas, temp files, and `/proc/self/fd/*` of in-flight uploads.
  - The `expected_model_sha256` check (`pipeline.py:86`) runs *after* deserialization, so it gives no protection.
  - The docstring (`pipeline.py:9`) claims "locked U-Net from models/registry.json (sha256 verified)". `load_model` never consults the registry.
  - The job-failure message is stored and returned by `/api/jobs/{id}` (`jobs.py:80-83`). Exception text from loading arbitrary paths, such as not-found versus unpickling errors, therefore also acts as a file-existence and content oracle.
- **Fix:**
  - Validate `config` against a strict schema.
  - Allow only `multiotsu`, `ctan_style`, and model *names* that are present in `registry.json`.
  - Verify the SHA-256 of the file **before** loading.
  - Use `torch.load(weights_only=True)` and store metadata separately (JSON card).
  - Remove `rf:` from the API surface entirely, or use a non-pickle format such as skops or ONNX.
  - Apply the same `weights_only=True` change to `train.py:137` (`init_from`).

### S-03 — Archive extraction: no ratio limit for TAR/TGZ, whole-member reads into memory, and limits larger than the upload cap (high)
- **Location:** `osteoquant/io/safe_archive.py:15-16, 52, 86-88`; `osteoquant/api/app.py:30, 319-323`.
- **Description:**
  - The ZIP branch checks a per-member ratio of 200, but only for members over 1 MB. The TAR branch (including `.tgz` and `.tar.gz`) has no compression-ratio check at all.
  - The TAR branch reads each member fully into memory (`dst.write(f.read())`), with each member up to 40 GB, so a small gzip-compressed tar can exhaust RAM.
  - `MAX_TOTAL_BYTES` (40 GB) is five times the 8 GB upload cap, so ZIP can still amplify roughly 200× up to 40 GB of disk per request.
  - `tarfile.getmembers()` on a gzip stream decompresses the whole stream before any limit is applied.
- **Evidence:** code inspection. No payload was built.
- **Fix:**
  - Stream TAR members in chunks while counting bytes, as the ZIP branch already does.
  - Enforce a global ratio of total uncompressed bytes to archive bytes.
  - Set `max_total` relative to the upload size and free disk space, for example ≤ 4× upload and ≤ 20 GB.
  - Refuse compressed tar, or decompress with a byte budget.

### S-04 — ReportLab markup injection in the PDF report (high)
- **Location:** `osteoquant/report/defectfill.py:143` (`Paragraph(str(c), SM)` for every table cell), `:157` (`Paragraph(bundle["title"], H1)`), `:182`, `:254`, `:315`.
- **Description:**
  - ReportLab `Paragraph` interprets an XML-like mini-markup that includes `<img src=...>` and `<a href=...>`.
  - User-controlled strings are inserted unescaped: study name, species, graft materials, group names, timepoint labels, reviewer meaning, user full names and source names.
  - Consequences:
    - Malformed markup makes report jobs fail (denial of service).
    - `<a href>` injects links into a document that is presented as a signed report.
    - `<img src=...>` makes the server read a local file path into the PDF. Report figures for every organisation sit at predictable paths (`data/org{N}/reports/fig/scan{S}_seg{G}.png`, `bundle.py:61`), so this is a cross-tenant image-disclosure path.
- **Fix:** pass every untrusted string through `xml.sax.saxutils.escape` (or `reportlab.lib.utils.escapeOnce`) before building a `Paragraph`, or use plain table strings. Also store figures outside any path a renderer could reach.

### S-05 — Cross-tenant IDOR: specimen `group_id` not validated, leaks other organisations' group names (high)
- **Location:** `osteoquant/study/db.py:268-274` (`add_specimen`), `:283-291` (`specimens` LEFT JOIN `groups_`), `osteoquant/api/app.py:129-133, 266-268`.
- **Description:** `group_id` is inserted without checking that the group belongs to the same study or organisation. The specimen listing then joins on the global `groups_.id`, so the caller receives the other tenant's group name (often the treatment arm) and `blind_code`. Group ids are sequential integers and easy to enumerate. Reports built from such specimens (`bundle.py:68`) carry the foreign name as well.
- **Reproduction (poc_integrity.py, check 3):** org B's analyst adds specimen `X1` with org A's `group_id`, and `specimens(B, sb)` returns `['Secret treatment arm']`.
- **Fix:**
  - Validate `group_id IN (SELECT id FROM groups_ WHERE study_id=?)` in `add_specimen`.
  - Join with `g.study_id = s.study_id`.
  - Likewise validate `specimen_id` and `timepoint_id` against the study in `register_scan` (`db.py:294-313`), which currently accepts any integer.

### S-06 — Blinding bypass through stored reports (high)
- **Location:** `osteoquant/api/app.py:89-103` (`job_report` renders with the *submitting* user's view), `:488-499` (`get_report` checks only `read` and org).
- **Description:** If a user with `unblind` (admin) generates a report for a blinded study, the PDF and CSV contain real group names (`bundle.py:35-36,68` via `store.specimens`). Any analyst, reviewer or viewer in the organisation can then download it by report id, defeating SOP-009 blinding. Report ids are sequential.
- **Fix:**
  - Record the blinding state used at render time in the `reports` row.
  - Refuse download of unblinded renders for users without `unblind` while the study is blinded.
  - Preferably always render blinded and add the key only in a separately controlled artefact.

### S-07 — Study export exposes the whole organisation's audit trail to analysts (medium)
- **Location:** `osteoquant/study/db.py:423-431` (`"audit": self.audit.events(org_id=..., limit=100000)`), `osteoquant/api/app.py:289-291`.
- **Description:**
  - `/api/audit` is restricted to reviewer and admin roles (`app.py:514-518`), but `/api/studies/{sid}/export` needs only `export`, which analysts have. It returns every audit event of the organisation, not just this study.
  - The events include failed-login reasons, usernames, all job parameters, and job-failure tracebacks with server paths (`jobs.py:80-83`).
- **Fix:** filter the export's audit records to objects that belong to the study, and apply the same role rule as `/api/audit`. Remove tracebacks from audit details (log them server-side instead).

### S-08 — Review and e-signature integrity: unbound object ids, pre-approval, self-review, stale approvals (medium)
- **Location:** `osteoquant/study/db.py:404-415`, `osteoquant/api/app.py:474-481`, `osteoquant/api/bundle.py:48-50`.
- **Description:**
  - `review()` never checks that `object_id` exists or belongs to the reviewer's organisation. It does not bind the signature to content (`labels_sha256`), and it does not stop an admin (who has both `write` and `review`) approving a segmentation they edited.
  - Segmentation ids are SQLite `INTEGER PRIMARY KEY` without `AUTOINCREMENT`, so:
    - a reviewer can approve id N+1 before it exists, and
    - after `delete_study_data` removes the highest rows, new segmentations reuse the ids and inherit old approvals.
  - `bundle_from_store` treats *any* earlier `approved` as reviewed, even if a later `rejected` exists, so a report can show the green "REVIEWED" banner for content no one signed.
- **Reproduction (check 4):** `review(revA, "segmentation", 999, "approved", …)` succeeds although segmentation 999 does not exist.
- **Fix:**
  - Validate existence and organisation of the object.
  - Store `labels_sha256` (or the report's PDF hash) in the review row and compare it at report time.
  - Use the latest decision.
  - Forbid `reviewer_id == created_by`.
  - Use `AUTOINCREMENT` (or UUIDs) for signed objects.

### S-09 — Account lockout: permanent, unauthenticated denial of service; races; username timing oracle (medium)
- **Location:** `osteoquant/study/db.py:166-181`.
- **Description:**
  - **Permanent lockout:** five bad passwords from anyone lock any account, admins included, permanently. `failed_logins` resets only on a successful login, which is now impossible, and there is no unlock path in the API or CLI.
  - **Race:** check-then-increment is not atomic. Parallel requests (FastAPI threadpool) each pass the `failed_logins >= 5` test before any increment, so more than five guesses are possible.
  - **Timing oracle:** unknown users return without running scrypt, while known users incur the roughly 50 ms scrypt cost, so usernames can be enumerated by response time.
  - **Re-authentication path:** re-auth at `/api/reviews` (`app.py:476-480`) has no counter, so a stolen session allows unlimited password guessing.
- **Fix:**
  - Use time-based lockout (exponential back-off) plus an admin unlock command.
  - Make the increment atomic (`UPDATE … SET failed_logins=failed_logins+1 WHERE id=? RETURNING failed_logins`).
  - Run a dummy scrypt for unknown users.
  - Count review re-auth failures toward the same lockout.

### S-10 — Audit log: concurrency forks the chain, shared SQLite connection misused across threads (medium)
- **Location:** `osteoquant/audit/log.py:61-69` (read last hash, then insert, with no transaction), `osteoquant/study/db.py:107` (`check_same_thread=False`, `isolation_level=None`, one connection shared by request threads and job workers).
- **Description:**
  - Concurrent `record()` calls read the same `prev_hash`, so the chain forks. `verify_chain` then reports tampering although nothing was tampered with, which destroys the evidential value of the control.
  - The same shared connection raised `sqlite3.InterfaceError: bad parameter or other API misuse` under load. With that misuse, `cursor.lastrowid` across threads is also unreliable for the ids returned to callers.
- **Reproduction (check 1):** 8 threads × 200 `record()` calls gives `{'ok': False, 'first_bad_seq': 3, 'reason': 'prev_hash mismatch …'}` plus InterfaceError exceptions.
- **Fix:**
  - Use one connection per thread (or a pool).
  - Wrap read-prev plus insert in `BEGIN IMMEDIATE … COMMIT`, or compute `prev_hash` inside an `INSERT … SELECT` under a process lock.

### S-11 — Audit log: what `verify_chain` cannot detect (medium)
- **Location:** `osteoquant/audit/log.py:72-92`, `osteoquant/cli.py:241-246`.
- **Description:**
  - The chain is an **unkeyed** SHA-256. Anyone with write access to the DB file can drop the triggers, edit any row, and recompute every later hash, and `verify_chain` returns `ok`.
  - Tail truncation is undetectable unless an external anchor exists. `anchor()` and `verify_anchor()` exist but nothing exports, schedules or checks an anchor (no CLI command, endpoint or backup step), and the module docstring (lines 6-8) overstates the protection.
  - Deleting the entire table also verifies as `ok` with `n: 0`.
  - `/api/audit/verify` verifies all tenants' events and returns the global count and head to any viewer, which is minor cross-tenant metadata.
- **Reproduction (check 2):** drop `audit_no_delete`, delete rows with seq > 6, re-open, and `verify_chain()` returns `{'ok': True, 'n': 6, …}`.
- **Fix:**
  - Key the chain with HMAC, using a key held outside the DB.
  - Periodically write signed anchors to write-once storage, and include the anchor in every backup and report.
  - Add an `audit-anchor` CLI and verify against the last anchor.
  - Scope `/api/audit/verify` output per organisation.

### S-12 — Activity missing from the audit trail (low)
- **Location:** various.
- **Description:** The following are not audited:
  - data views: `/slice`, `/mesh`, `/scans/{id}`, `/results`, `/users`;
  - direct `UPDATE`s of `segmentations.labels_key`, `scans.status`, `scans.store_path` and `reports` (`app.py:79, 85, 336, 100`);
  - edit operations beyond the first 200 (`app.py:459`, only `ops[:200]` stored);
  - overwriting the unversioned `labels/roi_current` layer (`app.py:81`).
- **Fix:** audit read access to image data and results, log full edit payload hashes, and version `roi_current`.

### S-13 — Data deletion is incomplete (medium)
- **Location:** `osteoquant/study/db.py:433-446`.
- **Description:** `delete_study_data` removes zarr stores and some rows, but leaves behind:
  - report PDF and CSV files and `reports` rows, which remain downloadable via `/api/reports/{rid}/…`;
  - figure PNGs (`reports/fig/`);
  - `jobs.params`/`result`, `reviews` and `analysis_configs`;
  - audit details containing animal ids and source filenames;
  - previous backups.

  There is also no API endpoint to delete, so the documented retention policy cannot be exercised by an admin through the application.
- **Fix:** delete or crypto-shred every artefact, list them in a deletion certificate, and document that backups expire on their own schedule.

### S-14 — Backups cover only the SQLite file (low)
- **Location:** `osteoquant/study/db.py:134-141`.
- **Description:** `backup()` copies the DB only. Scan zarr stores, label layers, reports and figures under `data_dir` are not included, so a restore yields rows whose `store_path` targets are missing. There is no restore or verify command, and `dest` overwrites without checks.
- **Fix:** back up `data_dir` with a manifest of hashes, add `restore` and `verify-backup`, and include the audit anchor.

### S-15 — Unbounded compute in `/mesh`, `/edits` and `/analyze` (low–medium)
- **Location:** `osteoquant/api/app.py:385-398` (any `read` user; `step=1` runs marching cubes on the full volume and returns all vertices as JSON), `:417-471` (5000 ops, each `ndi.label` on a plane, full-volume load), `:400-404` (unbounded queued jobs per user).
- **Fix:** cap voxel count and vertex count, set a per-user rate limit and job quota, and cache meshes.

### S-16 — Error messages leak internals (low)
- **Location:** `osteoquant/api/app.py:202-208` (`KeyError` and `ValueError` messages returned verbatim), `jobs.py:80` (job message).
- **Fix:** return generic messages and log details server-side.

### S-17 — Stale privileges in background jobs (low)
- **Location:** `osteoquant/study/jobs.py:149-157, 165-170`.
- **Description:** The user dict captured at submission is used for the whole job, so deactivation or a role change does not stop it. `requeue_interrupted` re-runs jobs as the original user without re-checking `active`.
- **Fix:** re-load the user and check `active` when the job starts.

### S-18 — Hard-coded demo admin password (low)
- **Location:** `scripts/demo_seed.py:27` (`DEMO_PW = "Demo-Password-2026"` for `demo_admin`).
- **Fix:** generate a random password per seed and refuse to seed a DB that is used with `serve --host` other than localhost.

### S-19 — CSV formula injection in the report CSV (low)
- **Location:** `osteoquant/report/defectfill.py:94-104`.
- **Description:** Group names and timepoint labels are free text, so a value starting with `=`, `+`, `-` or `@` is executed by spreadsheet software.
- **Fix:** prefix such cells with `'`.

### S-20 — Session handling details (low/info)
- **Location:** `osteoquant/study/db.py:166-193`, `web/static/app.js:4,39`.
- **Description:**
  - There is an 8 h absolute lifetime but no idle timeout.
  - Expired sessions are never purged.
  - Deactivating a user does not delete their sessions (blocked only at lookup).
  - The token is kept in `sessionStorage`, which any XSS can read.
  - There is no CSP or security headers.
- **Fix:** add an idle timeout, a purge job, session deletion on deactivation, and CSP / `X-Content-Type-Options` / `frame-ancestors` headers.

### S-21 — Upload filename edge case (info)
- **Location:** `osteoquant/api/app.py:302-306`.
- **Description:** A filename of `..` survives sanitisation (dots are allowed), so `dest` becomes the parent `uploads/` directory. `open(..., "wb")` then fails with a 500 error. It is not writable outside the directory.
- **Fix:** reject names consisting only of dots.

---

## Areas checked with no issue found
- **SQL injection:** all queries are parameterised. The only f-string SQL (`db.py:442,444`) interpolates fixed table names from literals.
- **Slice and mesh `layer` parameters** (`app.py:370,389`): regex-restricted to `image` or `labels/[A-Za-z0-9_]+`, so no path traversal into the zarr store or filesystem.
- **ZIP/TAR path traversal and links** in `safe_archive.py`: `..`, absolute paths, drive letters, symlinks, hardlinks and devices are rejected, and the resolved target is checked against `dest`. Only the resource limits are weak (S-03).
- **Report download path** (`app.py:497`): the path comes from the DB, not from the request. `kind` is allow-listed.
- **Password storage:** scrypt (n=2^14, r=8) with a per-user salt and constant-time compare. Session tokens are 256-bit and stored hashed.
- **RBAC on create/read endpoints:** project, study, group, timepoint, scan, ROI, edit, job and report endpoints all reach `require(...)` with an organisation check through `store.study`/`store.scan`/`runner.get`. The exceptions are those listed above (S-05, S-06, S-07, S-08).
- **XSS in the web client:** every `innerHTML` interpolation of server strings in `app.js` and `viewer.js` goes through `esc()`. The unescaped values are numeric ids, server-generated keys (`labels_key`, `kind`) and hashes.
- **CSRF:** not applicable. Authentication uses an `Authorization` header and no cookies.
- **Regex DoS:** all patterns are simple and anchored.
- **Static file serving:** only `web/static` is mounted. The vendor JS is local, with no remote script origins.

## Summary (≤300 words)
Twenty-one security findings.

**Critical (2)**
- S-01: detached NRRD/MetaImage headers let any analyst read arbitrary server files, including the shared SQLite DB with every tenant's data.
- S-02: the analysis config chooses a model path that is loaded with pickle/joblib or `torch.load(weights_only=False)`, with the hash check run after loading. This is code execution and a file oracle for any analyst.

**High (4)**
- S-03: TAR decompression and memory exhaustion with no ratio limit; 40 GB limits.
- S-04: ReportLab markup injection, including server-side `<img>` file inclusion into PDFs.
- S-05: cross-tenant `group_id` IDOR that leaks other organisations' group names (reproduced).
- S-06: blinding bypass by downloading admin-generated reports.

**Medium (6)**
- S-07: study export exposes the full organisation audit trail to analysts.
- S-08: e-signatures not bound to existing objects or content; pre-approval reproduced; id reuse; self-review; stale approvals.
- S-09: permanent unauthenticated lockout DoS, lockout race and username timing oracle.
- S-10: concurrent audit writes fork the hash chain and misuse the shared SQLite connection (reproduced).
- S-11: an unkeyed chain without exported anchors cannot detect rewrite or tail truncation (reproduced).
- S-13: deletion leaves reports, figures, jobs, reviews and audit PII.

**Low (8)**
- S-12: unaudited reads and updates.
- S-14: backups omit image data.
- S-15: unbounded mesh, edit and job compute (rated low–medium).
- S-16: verbose errors.
- S-17: stale job privileges.
- S-18: hard-coded demo password.
- S-19: CSV formula injection.
- S-20: session hygiene and missing security headers.

**Info (1)**
- S-21: `..` upload filename.

**Priority:** fix S-01 and S-02 before any multi-user or networked use. Then fix S-04, S-05, S-06 and S-10.
