# Data protection, audit trail and backups

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed. The controls described here are technical controls; they do not by themselves make a system
> compliant.

## Local-first, no telemetry

OsteoQuant Desktop runs entirely on your computer:

* It makes **no network connections**: no telemetry, crash reporting, analytics, update checks or licence server.
* Analysis runs in the same process as the user interface; there is no local server and no browser component.
* Licence files are verified offline against a public key built into the application.
* Data leave the computer only when you export them (CSV, PDF, screenshots, workflow-timing CSV) or copy the project
  folder yourself.

The older browser-based prototype (`osteoquant serve`) is optional and not needed by the desktop. If you use it, it
binds to 127.0.0.1 by default and warns when bound to another interface.

## What is stored where

| Location | Contents | Created by |
|---|---|---|
| **Project folder** (you choose it) | `osteoquant-project.json` (name, creation time, application version) | New project |
| | `osteoquant.db`: SQLite database with users (salted scrypt password hashes), roles, studies, groups, animals, timepoints, scans and their SHA-256, QC results, ROIs, segmentation versions, measurements, reviews and signatures, jobs, the import log and the **audit trail** | Every action |
| | `data/`: imported scans as chunked Zarr stores, label revisions, generated reports and figures | Import, analysis, editing, reports |
| | Workflow-timing events (only if enabled for the project) in `osteoquant.db` | *Tools > Record workflow timing* |
| **Settings folder** — Linux `~/.config/OsteoQuant`, Windows `%APPDATA%\OsteoQuant`, macOS `~/Library/Application Support/OsteoQuant` | `licence.oqlic` (if installed; or the path in `OSTEOQUANT_LICENCE_FILE`), `error.log` (tracebacks of unexpected errors; may contain file paths) | Licence installation; errors |
| **Operating-system settings store** (Qt settings, "OsteoQuant Desktop") | Recent project paths, theme | Application |
| Your export folders | Exported PDFs, CSVs, screenshots | You |

Imported scans are **copied** into the project; your original files are not modified. Patient or animal identifiers
in file names and metadata are copied too: de-identify scans before import if your data policy requires it, and use
blinded review mode to hide group, animal and file names on screen.

**Encryption.** The application does not encrypt project folders or the database. Use full-disk encryption (BitLocker,
FileVault, LUKS) and store projects on access-controlled drives.

## Users and access

* Each project has its own users; the creator is administrator. Roles: administrator, analyst, reviewer, viewer.
* Passwords: at least 10 characters with an upper-case letter and a digit, stored as salted scrypt hashes.
* Five failed sign-ins lock the account for 15 minutes.
* Signatures (approve, needs changes, reject) require password re-entry and a stated meaning; failed re-entries are
  audited. Authors cannot approve their own segmentations.
* Blinded review mode hides group names, animal IDs and file names everywhere for every role; blinded studies also
  hide group allocation from non-administrators.
* Anyone who can read the project folder can copy it. Access control on the folder is the operating system's job.

## Audit trail

The audit trail lives in `osteoquant.db`. Each event stores a sequence number, UTC timestamp, user, action, object
and details, plus `prev_hash` and `row_hash` = SHA-256(previous hash ‖ event fields).

* Rows are only inserted; SQLite triggers reject updates and deletes.
* Anyone who edits the file directly breaks the chain. **Audit trail > Verify chain** recomputes every hash and
  reports either an intact chain (with the event count and head hash) or the first altered event.
* Deleting the newest events and leaving a consistent shorter chain is detectable only if you have recorded an
  **anchor** (sequence number and head hash) elsewhere. Write down the event count and head hash shown after *Verify
  chain* at regular intervals (for example weekly, and when a report is approved) and keep it outside the project.
* Recorded events include sign-in, failed sign-in and sign-out; imports, duplicates and rejections; QC; scan views;
  analysis jobs (submitted, done, failed, cancelled); ROI definitions; every saved segmentation revision with the
  reason and per-class voxel changes; reviews, refused self-approvals and failed re-authentications; report
  generation, approval and export; CSV and screenshot exports; blinded-mode and workflow-timing switches; chain
  verifications and backups.

From a source install the same check runs on the command line:
`OQ_DB=/path/to/project/osteoquant.db osteoquant audit-verify`.

## Backups

The project folder is the unit of backup: the database and `data/` must be backed up **together**.

**Simple and safe:** close the project (or quit the application), then copy the whole project folder to the backup
target. Back up regularly and keep at least one copy on a different device or site.

**Consistent database copy while in use** (source install): `OQ_DB=/path/to/project/osteoquant.db osteoquant backup
/backup/osteoquant-YYYY-MM-DD.db` uses SQLite's online backup API, prints the SHA-256 of the copy and records a
`backup` event in the audit trail. Copy `data/` and `osteoquant-project.json` alongside it.

**Restore and check:**

1. Copy the backed-up folder to a new location (do not overwrite the damaged project until the restore is checked).
2. Open it with *File > Open project* and sign in.
3. *Audit trail > Verify chain*: it must report an intact chain, and the head hash must match your last anchor, or the
   chain must extend it.
4. Open a few scans and regenerate one report; compare with the archived report.

A draft backup-and-restore SOP for organisational use (schedules, manifests, restore tests) is in
`docs/quality/SOPs/SOP-006_backup_and_restore.md`. It is a draft and not in effect.

## Deleting data

Delete a project by deleting its folder (and its backups). Remove the per-user settings folder to remove the licence
file and error log. There is no remote copy to delete.

## Pilots and shared data

For pilot work with OsteoQuant, scans are exchanged only under a written data-processing agreement. By default your
scans are not used to train models; any adaptation to your material requires your written opt-in, and adapted
weights are kept for you alone.

See also: [LICENSING_AND_ADMIN.md](LICENSING_AND_ADMIN.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md) and the
security review `docs/security/SECURITY_REVIEW_GEN2.md`.
