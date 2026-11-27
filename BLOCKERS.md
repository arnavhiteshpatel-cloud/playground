# Blockers

| ID | Component | Blocker | Needs | Workaround in place |
|---|---|---|---|---|
| B-001 | Three-class validation on real graft data | No public micro-CT dataset with voxel labels for new bone vs residual graft vs host bone was known at start | Physical phantom scans (validation/PHANTOM_EXPERIMENT_PROTOCOL.md) or customer data under a DPA | Synthetic phantom benchmark; real-data experiments on bone-vs-background only |
| B-002 | GPU training (nnU-Net-scale) | Container has 4 CPUs, no GPU | Personal/company cloud GPU (not NCSA, for IP hygiene) | Small CPU U-Net; architecture swappable |
| B-003 | Physical density units | No calibration phantom scans available | HA phantom scanned with each protocol | Uncalibrated grey-value reporting (D-004) |
| B-004 | Bone H&E whole-slide data (IDR idr0096 MarrowQuant) | ftp.ebi.ac.uk HTTPS download fails at TLS through this environment's egress proxy (curl exit 35) | Download on the founder's Mac (browser or `curl` from a normal network), then run `experiments/exp_N_histology.py --wsi <file>` | Histology validated on NuInsSeg (real nuclei labels) + synthetic sections with known truth |
| B-005 | BONe dataset (Dryad 4j0zpc8qq, CC0, 44.6 GB) | Dryad file downloads return 401/403 without an API token | Founder: create a free Dryad account/API token or download `1R_1U_HF.zip` (2.0 GB) in a browser | Dog forelimb (SPROUT) used for real bone-vs-background experiments instead |
| B-006 | Labelled three-class real data (new bone / graft / host) | No public dataset found (dataset stream searched Zenodo, Dryad, Figshare, OSF, IDR, Dataverse, MorphoSource, TCIA) | Physical phantom experiment (validation/) or customer data under DPA | Synthetic benchmark + longitudinal design |
| B-007 | NIH grant drafts | NIH states it will not consider applications substantially written by AI as the applicants' original work | Founder must substantially rewrite the drafts in their own words before any NIH submission | Drafts provided only as scaffolding/checklists |
| B-008 | Federal SBIR/STTR eligibility | PI must be >50% employed by the company (NSF SBIR, NSF STTR, NIH SBIR); full-time student founder conflicts | Full-time co-founder PI, leave of absence, or NIH STTR with a UIUC faculty PI | Cozad / I-Corps / iVenture first |
