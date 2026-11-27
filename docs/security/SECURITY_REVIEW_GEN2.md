# OsteoQuant Security Review — Generation 2

Scope: re-review of `osteoquant/study/db.py`, `audit/log.py`, `io/safe_archive.py`, `io/readers.py`
(`check_safe_input` and the readers it guards), `ml/train.py` (`load_model`), `ml/runtime.py` (ONNX
loader), `api/app.py`. Also covers the open low items from Gen 1 (S-15, S-16, S-20, S-21 in
`SECURITY_REVIEW.md` / `REVIEW_RESPONSE.md`). Review date: 2026-11-27.

**Method:**
- Manual code review.
- Benign local proofs of concept: marker files only, run in a scratch directory; no external hosts.
- A mutation fuzzer over every reader (7 formats, truncation, byte flips, planted large integers), run in
  subprocesses with a 3 GB address-space limit and a 30 s timeout.
- `bandit` 1.9.4 and `pip-audit` 2.10.1.
- Every fix has a regression test in `tests/`.
- Cross-references to QA defect IDs are in `docs/qa/DEFECTS_FOUND.md`.

Severity scale: critical, high, medium, low, info.

## Summary

| ID | Sev | Title | Status | Regression test |
|---|---|---|---|---|
| G2-01 | critical (conditional) | Code execution via a pickle codec in an uploaded Zarr store | **Fixed** (allow-list) + dependency floor recommended | `test_zarr_pickle_codec_rejected_before_decoding`, `test_zip_with_pickle_zarr_rejected_by_api` |
| G2-02 | medium | Memory exhaustion from header-declared dimensions (Zarr fill value, NIfTI, NRRD, TIFF, DICOM, TXM) | **Fixed** | `test_huge_*_fail_fast` (6 tests) |
| G2-03 | medium | Password brute force through the e-signature re-authentication endpoint | **Fixed** | `test_review_endpoint_cannot_bruteforce_password`, `test_reauthentication_counts_towards_lockout` |
| G2-04 | medium | Zip-bomb bypass with many small members (per-member ratio test applies only above 1 MB) | **Fixed** | `test_zip_many_small_members_aggregate_ratio` |
| G2-05 | low | Upload validation checked only the sub-folder chosen for reading, not the whole extracted ZIP | **Fixed** | `test_zip_with_pickle_zarr_rejected_by_api` |
| G2-06 | low | OME-TIFF companion-file references (`UUID FileName`, `MetadataFile`) outside the upload | **Fixed** | `test_ome_tiff_external_reference_rejected` |
| G2-07 | low | Library exceptions from malformed uploads and archives became HTTP 500 with stack-derived text | **Fixed** (`CorruptInput` / `UnsafeArchive`) | `test_truncation_never_crashes`, `test_random_byte_mutations_never_crash`, `test_corrupt_member_data_reported_as_unsafe_archive`, `test_corrupt_zip_and_malformed_volumes_are_400` |
| G2-08 | medium (integrity) | Zarr store chunks missing or modified were read silently as fill value; the recorded hash was not verified | **Fixed** | `test_zarr_integrity_detects_deleted_chunk` |
| G2-09 | low | `check_password` raised on a corrupt stored hash | **Fixed** | `test_malformed_password_hash_never_raises` |
| G2-10 | low | `set_scan_qc` / `save_measurement` lacked a `write` permission check (defence in depth) | **Fixed** | `test_writes_require_write_permission` |
| G2-11 | low | Audit anchor of an empty log never verifies; timestamp from two clock reads | **Fixed** | `test_anchor_from_empty_log_verifies`, `test_timestamp_is_one_instant` |
| G2-12 | low | Symbolic links inside uploaded folders followed by readers | **Fixed** (rejected in `safe` mode) | `test_symlinks_rejected_in_uploads`, `test_preexisting_symlink_in_destination_cannot_be_followed` |
| G2-13 | low | ONNX loader TOCTOU: hashes the file, then reopens the path | **Assigned to lead** (`ml/runtime.py`, QA-023) | — |
| G2-14 | low | Dependency floors allow vulnerable versions (`torch>=2.2`, numcodecs < 0.17.1) | **Assigned to lead** (QA-024); CI installs `torch>=2.6` | — |
| G2-15 | low | Model registry write uses `fcntl` (fails on Windows; not a vulnerability, but locking is the integrity control for the registry) | **Assigned to lead** (QA-022) | `test_update_registry_works_without_fcntl` (xfail strict) |
| G2-16 | low | `/api/audit/verify` reveals the global event count and head hash to any `read` user (cross-tenant metadata) | Open (accepted for single-lab local deployment) | — |
| G2-17 | low | Upload parsing runs synchronously inside the async request handler (blocks the event loop; DoS by a `write` user) | Open | — |
| G2-18 | low | scrypt cost N = 2^14 is below the current OWASP recommendation (2^17) | Open (needs rehash-on-login) | — |
| G2-19 | info | bandit B314 (`xml.etree` on untrusted OME-XML) | Mitigated: expat 2.9.0 amplification limit; safe-mode check rejects entity bombs in < 0.2 s | `test_ome_xml_entity_expansion_rejected_quickly` |
| G2-20 | info | bandit B608 (f-string SQL in `delete_study_data`) | False positive: table names are literals | — |

Gen-1 open items:

| Item | Status |
|---|---|
| S-15 (unbounded compute) | Unchanged: still partially mitigated. |
| S-16 (verbose errors) | **Partially fixed** (G2-07): parser and archive errors now give one controlled message. Job failure messages are still shown to same-org users. |
| S-20 (session hygiene) | **Partially fixed**: deactivation deletes the user's sessions; expired sessions are purged at login; CSP, `X-Frame-Options`, `X-Content-Type-Options` and `Referrer-Policy` headers are set. Still open: idle timeout and token rotation. Test: `test_deactivation_deletes_sessions_and_login_purges_expired`, `test_security_headers_present`. |
| S-21 (dot filenames) | **Fixed**. Test: `test_dot_filenames_do_not_500`. |

No new high-severity issue was found in the installed environment. G2-01 is critical only where the
installed zarr/numcodecs combination still decodes pickle. The allow-list closes it in every
environment.

---

## Findings

### G2-01 — Code execution through a pickle codec in an uploaded Zarr store (critical, conditional)
- **Location:** `api/app.py` upload → `read_volume(src, safe=True)` → `io/readers.read_zarr` → `zarr.open_group(...)["image"][...]`.
- **Path:** The upload endpoint accepts a ZIP. It extracts the ZIP and reads the folder with the most files. `detect_format` classifies a folder containing `.zgroup` or `zarr.json` as Zarr. `check_safe_input` then looked only at detached headers.
- **Exploit:** A Zarr v2 array whose `.zarray` declares `compressor: {"id": "pickle"}` (or the pickle filter, or the v3 `numcodecs.pickle` codec) makes numcodecs call `pickle.loads` on the chunk bytes.
- **Evidence (benign marker PoC, scratch directory):**
  - zarr 3.0.8 with numcodecs 0.15.1, 0.16.0, 0.16.1, 0.16.3 or 0.17.0: the payload ran and created the marker file. The decode then failed with a `TypeError`.
  - numcodecs 0.17.1 raises `UnsafeDecodeError`.
  - zarr 3.4.2 refuses the dtype/object-codec combination.
  - `pyproject.toml` declares only `zarr>=3.0`, so a fresh install can resolve to a vulnerable pair.
- **Fix:**
  - `check_safe_input` parses every `.zarray`, `.zmetadata`, `.zgroup` and `zarr.json` in the upload, including consolidated metadata and nested sharding codecs.
  - It accepts only an allow-list of compression and filter codecs (`blosc`, `zstd`, `zlib`, `gzip`, `bz2`, `lzma`, `lz4`, `delta`, `fixedscaleoffset`, `quantize`, `bitround`, `shuffle`, `packbits`, `bytes`, `transpose`, `crc32c`, `sharding_indexed`) and plain numeric/bool dtypes.
  - The API now runs the check over the whole extracted tree (G2-05).
- **Also recommended (lead, pyproject):** `numcodecs>=0.17.1`.
- **Tests:** `tests/test_io_destructive.py::test_zarr_pickle_codec_rejected_before_decoding[v2,v3]` asserts that no marker file is created. `::test_zarr_object_dtype_and_consolidated_metadata_rejected`, `::test_upload_zip_with_zarr_payload_rejected_end_to_end`, `tests/test_security_gen2.py::test_zip_with_pickle_zarr_rejected_by_api` and `tests/test_io_metadata.py::test_zarr_metadata_rejections` cover the other paths.

### G2-02 — Memory exhaustion from header-declared dimensions (medium)
- **Location:** every reader in `io/readers.py`.
- **Evidence:** run under a 3 GB `RLIMIT_AS`, in subprocesses.
  - A 2 KB Zarr store with shape 1100³ uint16 and `fill_value=7` allocated and filled 2.48 GB. Without the limit it would push a 16 GB server into the OOM killer.
  - NIfTI (`.nii`, `.nii.gz`) with dims 30000³ raised `MemoryError` from `np.asanyarray(img.dataobj)`.
  - Zarr with 30000³ raised `MemoryError` (49 TiB).
  - Uncompressed TIFF, NPY and DICOM failed late with mmap/pixel-size errors.
- **Fix:**
  - `_check_alloc` computes the size of the *selected* region (`zrange`/`step`) from header metadata before any allocation. It raises `VolumeTooLarge` (a `ValueError`, so HTTP 400) above `OQ_MAX_READ_BYTES`, which defaults to 75 % of physical RAM.
  - A `MemoryError` that still occurs is converted to `VolumeTooLarge`.
- **Tests:** `test_huge_nifti_dims_fail_fast`, `test_huge_nrrd_sizes_fail_fast[raw,gzip]`, `test_huge_zarr_shape_fail_fast` (a bounded sub-range is still readable), `test_huge_tiff_dims_fail_fast`, `test_huge_dicom_rows_cols_fail_fast` (series and multi-frame), `test_huge_txm_declared_size_fail_fast`, `test_huge_npy_header`. API: `test_corrupt_zip_and_malformed_volumes_are_400`.

### G2-03 — Password brute force through e-signature re-authentication (medium)
- **Location:** `api/app.py` `POST /api/reviews`.
- **Problem:** The password was checked with `check_password`, with no failure accounting. Anyone holding a session token could guess the user's password without limit (about 30 guesses/s with scrypt), bypassing the login lockout added for S-09. The recovered password then allows signing as that user after the token expires.
- **Fix:** `Store.reauthenticate(user, password)` shares the login lockout state (5 failures → 15-minute lock), runs the same scrypt cost while locked, and audits `auth.reauth_failed`. The API uses it.
- **Tests:** `test_security_gen2.py::test_review_endpoint_cannot_bruteforce_password`, `::test_reauthentication_counts_towards_lockout`, `::test_reauthentication_inactive_user`.

### G2-04 — Zip bomb with many small members (medium)
- **Location:** `io/safe_archive.py`.
- **Problem:** The per-member ratio check applies only to members larger than 1 MB. 16 000 members of 1 MB zeros (about 16 MB compressed) stay under the 16 GB total limit and fill the disk.
- **Fix:**
  - A whole-archive ratio limit of 200:1 applies once more than 64 MB would be extracted.
  - Encrypted members, special-file modes and colliding or duplicate member paths are rejected.
  - Corrupt member data is reported as `UnsafeArchive`.
- **Tests:** `test_safe_archive.py` (29 tests). Highlights:
  - `test_zip_many_small_members_aggregate_ratio`
  - `test_zip_encrypted_member_rejected`
  - `test_zip_collisions_rejected_cleanly`
  - `test_corrupt_member_data_reported_as_unsafe_archive`
  - `test_preexisting_symlink_in_destination_cannot_be_followed[zip,tar]`
  - traversal variants (`..`, absolute, drive letters, backslashes, empty name)

### G2-05 — Upload validation scope (low)
- **Problem:** After extracting a ZIP, the API ran `check_safe_input` only on the sub-folder it would read. That is enough for the reader itself, but hostile metadata elsewhere in the tree was never examined, for example consolidated Zarr metadata one level up.
- **Fix:** `check_safe_input(ex)` runs on the whole extraction folder.

### G2-06 — OME-TIFF external references (low)
- **Problem:** tifffile resolves `TiffData/UUID@FileName` with `os.path.join(dirname, FileName)`, so an absolute name escapes the folder. It also opens `BinaryOnly@MetadataFile`.
- **Mitigating factor:** tifffile checks that the UUID matches, which requires knowing the target file's UUID.
- **Fix:** In safe mode only bare file names are allowed: no separators, `..`, drive or URL colons.
- **Test:** `test_ome_tiff_external_reference_rejected`.

### G2-07 — Library exceptions surfaced as HTTP 500 (low; closes part of S-16)
- **Evidence:** The fuzzer outcome classes before the fix were `zlib.error`, `nrrd.errors.NRRDError`, `nibabel...ImageFileError`, `HeaderDataError`, tifffile `RuntimeError`, `NotImplementedError`, `tokenize.TokenError`, `IndexError` and `KeyError`.
- **Fix:**
  - `read_volume` wraps reader errors as `CorruptInput("Could not read <fmt> input <name>: <Type>: <msg>")`.
  - `safe_extract` wraps `BadZipFile`, `zlib.error`, `TarError`, `EOFError`, `RuntimeError` and `NotImplementedError`.

### G2-08 — Silent data substitution in the internal Zarr store (medium, integrity)
- **Problem:** A missing or modified chunk file is returned as the fill value (zeros). `content_sha256` was stored at write time but never compared at read time. An analysis could therefore run on corrupted data with intact provenance.
- **Fix:** A full read with `do_hash=True` (the `read_volume` default, used by the API job handlers) verifies the hash and raises `CorruptInput` on a mismatch. Previews pass `do_hash=False` or a sub-range.
- **Test:** `test_zarr_integrity_detects_deleted_chunk`.

### G2-09 to G2-12
These are the low hardening items in the summary table. Each has a fix and the regression test named
there.

### G2-13 — ONNX TOCTOU (low, assigned to lead)
- **Location:** `ml/runtime.OnnxSegmenter.__init__`.
- **Problem:** It hashes `path.read_bytes()` and then calls `InferenceSession(str(path))`. A local writer could swap the file between the check and the load.
- **Mitigating factors:** ONNX graphs cannot execute arbitrary Python, and the `onnx:` route is not reachable from the web API schema.
- **Fix:** Pass the verified `bytes` to `InferenceSession`.

### G2-14 — Dependency floors (low, assigned to lead)
- **`torch`:** `torch>=2.2` allows versions affected by CVE-2025-32434 (bypass of `torch.load(weights_only=True)`, fixed in 2.6.0).
  - The registry hash check in `load_model` means a hostile checkpoint would also need a matching registry entry, so practical risk is limited to someone with write access to `models/`.
  - Installed here: torch 2.15.0.
- **`zarr`:** see G2-01.
- **`pip-audit` on the declared dependency closure** (resolved to the latest versions): **no known vulnerabilities**.
- **`pip-audit` on this container's environment:** 53 advisories in 8 packages, none of them OsteoQuant runtime dependencies:

  | Package | Advisories |
  |---|---|
  | pypdf | 25 |
  | pip | 12 |
  | setuptools | 5 |
  | soupsieve | 4 |
  | httplib2 | 2 |
  | oauthlib | 2 |
  | opentelemetry-api | 2 |
  | wheel | 1 |

  pypdf is used only by the desktop tests. The CI `audit` job checks the declared runtime dependencies.

### Re-review of the Gen-1 critical fixes (no new issue)
- **`load_model`:**
  - The name is regex-validated (`^[A-Za-z0-9_-]{1,64}$`).
  - The file is read once. The SHA-256 of *those bytes* is compared with `models/registry.json`, and the same bytes are deserialised with `torch.load(weights_only=True)`, so there is no TOCTOU.
  - A hash-matching checkpoint containing a pickled callable is still refused, and no marker file is created (`test_load_model_refuses_pickled_code_even_if_registered`). The registry cannot vouch for code.
  - Tampering with any single byte is refused (`test_load_model_verifies_hash_before_deserialising`).
- **`check_safe_input` (S-01):**
  - Rejected: `.mhd`, `.nhdr`, `.raw` and `.mha`, and NRRD files with `data file`/`datafile` in any case or spacing.
  - The new symlink, Zarr and OME checks are listed above.
  - `.npy` uses `np.load(mmap_mode="r")` with `allow_pickle=False`; object arrays are refused (tested).
- **Audit chain:**
  - Property test: for any random row and any of the 9 columns set to any other value, `verify_chain` reports a failure at that row or the next (`test_any_single_field_tamper_is_detected`).
  - Deletion of a non-tail row and reordering are detected.
  - Tail truncation is detected only with an exported anchor; this documented limitation is tested.
  - 4 concurrent writers × 15 events produce one valid chain.
- **SQL:** all queries are parameterised. Table names in f-strings are literals (G2-20).

## Tooling results
- **bandit** (`-r osteoquant -x osteoquant/desktop`):

  | Severity | Count | Tests | Assessment |
  |---|---|---|---|
  | High | 0 | — | — |
  | Medium | 4 | B314 ×2 (see G2-19), B608 ×2 (false positive, G2-20) | — |
  | Low | 16 | B110 try/except/pass ×3, B404/B603/B607 (fixed `git` subprocess in `api/bundle.py`), B405/B406 (xml imports) | Accepted |

- **pip-audit:** see G2-14.
- **Fuzzing:** 7 formats × (11 truncation points + 30 mutations) with no hang and no unhandled exception type after the fixes. Plus 7 hostile huge-dimension cases, the TXM structure faults, and the Zarr/OME/symlink hostile uploads.
