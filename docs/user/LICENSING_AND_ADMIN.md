# Licensing and administration

> **Status.** Research product: not validated on real graft materials; not a medical device; no GLP/Part 11
> compliance claimed. **No production licence can be issued yet:** only a published test key exists.

Implementation: `osteoquant/licensing/` (`core.py`, `keys.py`). Design decision: ADR-G2-06 in
[ARCHITECTURE_DECISIONS.md](../../ARCHITECTURE_DECISIONS.md). Key handling for builders:
[docs/desktop/PACKAGING.md](../desktop/PACKAGING.md#licence-signing-key-production).

## Evaluation mode

Without a valid licence, OsteoQuant Desktop runs in **evaluation mode**:

* every function works (import, viewer, editing, analysis, review, reports, batch);
* every report carries the watermark **"EVALUATION COPY - NOT FOR STUDY DECISIONS"**;
* the start page, status bar and *Help > Licence* show "Evaluation mode".

An expired licence, a licence bound to another machine, a tampered file or a file signed by an unknown key all fall
back to evaluation mode, with the reason shown in *Help > Licence*. The application never stops working because of a
licence problem.

## Licence files

A licence is a small JSON file with the extension `.oqlic`:

```json
{
  "format": "osteoquant-licence/1",
  "key_id": "<id of the signing key>",
  "payload": "<canonical JSON string>",
  "signature": "<base64 Ed25519 signature over the exact payload bytes>"
}
```

The payload contains `licence_id`, `licensee`, `edition` (`academic`, `commercial` or `evaluation`), `features`,
`issued`, `expiry` (a date, or `null` for perpetual), `machine` (optional fingerprint), `product`
(`osteoquant-desktop`) and `test`.

Verification is **offline**: the signature is checked against public keys built into the application
(`osteoquant/licensing/keys.py`). The private signing key never ships with the application. A licence is valid only
if the signature matches, the key is trusted, the product matches, the edition is known, the issue date is present,
it has not expired and, if machine-bound, the fingerprint matches.

**Editions and watermarks**

| Licence state | Report watermark |
|---|---|
| None, expired, invalid, or edition `evaluation` | EVALUATION COPY - NOT FOR STUDY DECISIONS |
| Valid but signed with the test key or marked `test` | TEST LICENCE - NOT A VALID PRODUCT LICENCE |
| Valid `academic` or `commercial` licence signed with a production key | none |

**Features.** The payload lists feature flags (`import`, `viewer`, `edit`, `analyze`, `review`, `report`, `batch`).
They are verified and displayed; the current desktop build does not switch functions off by feature.

## Installing a licence

1. *Help > Licence...* shows the current state, edition, licensee, licence ID, expiry, features, signing key, report
   watermark, licence file and this computer's **machine fingerprint**.
2. For a machine-bound licence, send the fingerprint to the licensor. The fingerprint is a hash of host name, primary
   network adapter address, operating system and CPU architecture. It is a deterrent, not copy protection: changing the
   host name or network adapter changes it.
3. *Install licence file...* checks the file offline. If valid, it is copied to the per-user location: Linux
   `~/.config/OsteoQuant/licence.oqlic`, Windows `%APPDATA%\OsteoQuant\licence.oqlic`, macOS
   `~/Library/Application Support/OsteoQuant/licence.oqlic`. An invalid file is not installed; the reason is shown.

Administrators can point the application at a licence elsewhere with the environment variable
`OSTEOQUANT_LICENCE_FILE=/path/to/licence.oqlic`.

## Test keys only

* `PRODUCTION_KEYS` in `keys.py` is **empty**. No production signing key has been generated; generating it and keeping
  the private half offline (hardware token or encrypted offline storage) is a founder action.
* `TEST_KEYS` contains one key (`oq-test-1`) whose private half is derived from a seed **published** in
  `tools/make_test_licence.py`. Anyone can sign with it, so test licences prove nothing.
* Test licences are accepted only when explicitly allowed: environment variable `OSTEOQUANT_ACCEPT_TEST_LICENCES=1`,
  unit tests or CI. Otherwise they are rejected with "signed with the public TEST key". When accepted, they are always
  labelled TEST LICENCE and watermark reports accordingly.

Creating a test licence (for evaluation of the licensing flow only):

```bash
python tools/make_test_licence.py --licensee "Test Lab" --edition academic --days 365 -o test.oqlic
OSTEOQUANT_ACCEPT_TEST_LICENCES=1 osteoquant-desktop      # then Help > Licence > Install licence file...
```

Options: `--edition {academic,commercial,evaluation}`, `--days N` (0 = perpetual), `--features a,b,...`,
`--bind-this-machine`, `--keygen DIR` (fresh random **test** keypair), `--key PEM --key-id ID`. Never use this tool to
issue licences to anyone.

**When production keys exist** (procedure in PACKAGING.md): the 32-byte Ed25519 public key is added to
`PRODUCTION_KEYS` under a new key ID (for example `oq-prod-2027-01`) and a new build is released; licences are signed
with `"test": false`; keys rotate by adding a new ID and keeping old IDs until their licences expire.

## Adding users

Authors cannot approve their own segmentations, so review needs at least a second account. **The desktop application
has no user-management screen yet.** Until it has one, an administrator can add users from a source install, with the
application closed:

```python
from osteoquant.desktop.project import Project

p = Project("/path/to/project")
assert p.login("admin_username", "admin password")
p.store.create_user(p.user["org_id"], "rreviewer", "Choose-A-Pass-1", "reviewer", "R. Reviewer", actor=p.user)
p.close()
```

Roles: `admin`, `analyst`, `reviewer`, `viewer`. The new password must meet the policy (≥10 characters, an upper-case
letter and a digit). The creation is recorded in the audit trail under the administrator. Give each person their own
account; never share accounts.

## Other administration

| Task | How |
|---|---|
| Check an installation | `osteoquant-desktop-console --selftest` (exit code 0 = all 8 steps passed) |
| Version | `osteoquant-desktop-console --version`, or *Help > About* |
| Verify a project's audit trail | *Audit trail > Verify chain* (reviewers and administrators) |
| Back up a project | Close it and copy the folder; see [DATA_PROTECTION.md](DATA_PROTECTION.md#backups) |
| Third-party licences | *Help > About > Third-party licences*, and `THIRD_PARTY_LICENSES/` in the install folder |
| Workflow timing | *Tools > Record workflow timing for this project* (off by default; stored only in the project) |
| Memory limits for large data | Environment variables `OQ_SLAB_IMPORT_BYTES`, `OQ_QC_FULL_RES_BYTES`, `OQ_3D_SURFACE_VOXELS`, `OQ_3D_VOLUME_VOXELS`, `OQ_OBLIQUE_VOXELS` (see [docs/desktop/ARCHITECTURE.md](../desktop/ARCHITECTURE.md#performance-and-memory)) |
