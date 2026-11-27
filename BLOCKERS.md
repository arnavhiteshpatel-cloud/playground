# Blockers

| ID | Component | Blocker | Needs | Workaround in place |
|---|---|---|---|---|
| B-001 | Three-class validation on real graft data | No public micro-CT dataset with voxel labels for new bone vs residual graft vs host bone was known at start | Physical phantom scans (validation/PHANTOM_EXPERIMENT_PROTOCOL.md) or customer data under a DPA | Synthetic phantom benchmark; real-data experiments on bone-vs-background only |
| B-002 | GPU training (nnU-Net-scale) | Container has 4 CPUs, no GPU | Personal/company cloud GPU (not NCSA, for IP hygiene) | Small CPU U-Net; architecture swappable |
| B-003 | Physical density units | No calibration phantom scans available | HA phantom scanned with each protocol | Uncalibrated grey-value reporting (D-004) |
