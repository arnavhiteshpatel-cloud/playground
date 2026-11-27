# Science Knowledge Base: Index

Start here for anything about bone biology, graft materials, micro-CT physics, standards or public datasets.

| What | Where |
|---|---|
| Consolidated knowledge base: healing timelines by model, graft materials, micro-CT physics, Bouxsein and Dempster standards, published graft-vs-bone methods with accuracies, FDA guidance, and product implications | `docs/science/KNOWLEDGE_BASE.md` |
| Verified references (80 entries; each has a Crossref-resolved DOI or an official URL and a `verification` field: 14 full-text, 51 abstract, 15 metadata-only) | `docs/science/references.bib` |
| Machine-readable materials (16 classes, each with an `advisor_profile`) and the workflow for an unsupported material | `osteoquant/knowledge/materials.json`; load with `osteoquant.knowledge.load_materials()` and check with `validate_materials()` |
| Dataset discovery, round 2 (sources searched, ranked candidates, downloads) | `docs/research/DATASET_DISCOVERY_R2.md`, `docs/research/datasets_r2.csv` |
| Leakage-free split plan per dataset | `docs/research/SPLIT_PLAN.md` |
| Round-1 dataset survey | `docs/research/DATASET_REGISTRY.md` |
| Earlier detailed notes (background; superseded where they conflict with KNOWLEDGE_BASE.md) | `docs/science/BONE_BIOLOGY_AND_GRAFTS.md`, `MICROCT_IMAGING_SCIENCE.md`, `MORPHOMETRY_STANDARDS.md`, `SEPARABILITY_ANALYSIS.md`, `REFERENCES.md` |
| Provenance of downloaded data (SHA-256 and licence text per folder) | `data/raw/<source>_<id>/PROVENANCE.json` and `LICENSE.txt` |

## Key conclusions

- **Bone-derived grafts.** Never report new bone from intensity alone for autograft, allograft, DBBM or DBM. In 111 DBB-grafted human biopsies, µCT and histology did not correlate in grafted bone. Use total mineralised volume, day-0 registration, or histology.
- **Materials that read in the bone band** are calcium sulfate, polymer–ceramic composites and Mg alloys. Intensity is rated `poor` for all three.
- **β-TCP and BCP** separate well only while the granules are intact. The timepoint must be an input.
- **Thresholds for glasses, CaSO4 and Mg are tied to the scan protocol.** Their contrast against bone changes with kVp and filtration, so a threshold must not be transferred between protocols.
- **No openly downloadable voxel-labelled graft vs new-bone dataset exists.** Labelled Mg-implant SRµCT data exist, but only on request from the authors.
