# Specific Aims (NIH-style, one page): DRAFT SCAFFOLD

> **Use notes (not part of the page):**
> - Target: NIH STTR/SBIR Phase I (R41/R43) to NIBIB (primary) or NIAMS (secondary). The limit is 1 page [V].
> - The NSF version of this content lives in NSF_PROJECT_PITCH_DRAFT.md.
> - Every **[PENDING RESULT: …]** must be replaced with real data or removed. Never submit a placeholder as a claim.
> - **NIH NOT-OD-25-132 [V]:** NIH will not consider applications "substantially developed by AI" to be original ideas of applicants. This scaffold must be rewritten in the team's own words and with the team's own reasoning before any submission.
> - NIH Phase I is "normally" 6 months [V]. Three aims may be too many for 6 months. Options: (i) keep Aims 1–2 in Phase I and move Aim 3 to Phase II; or (ii) request a longer period/budget with justification (some ICs allow it [INF; confirm with the NIBIB PO]).

---

**OsteoQuant: Toward ground-truth-validated, material-aware quantification of bone regeneration in preclinical micro-CT**

Bone-graft substitutes and orthobiologics are evaluated in animal defect models largely by micro-CT. The central question in these studies is how much **new bone** formed, how much **graft remains**, and how both relate to the **host bone**. Many graft materials (calcium phosphates, bioactive glasses, allograft and xenograft) have X-ray attenuation that overlaps mineralized tissue. Standard practice therefore relies on global thresholds and manual contouring. This approach (i) cannot reliably separate residual graft from new bone, (ii) varies across operators, scanners and voxel sizes, and (iii) leaves no audit trail that a sponsor, CRO or reviewer can inspect [INF from domain knowledge; cite literature: **[CITATIONS NEEDED: reviews on micro-CT of bone grafts; threshold sensitivity; reporting guidelines, e.g., Bouxsein et al. 2010 JBMR]**]. No public benchmark with physical ground truth currently quantifies *when* graft and new bone are separable as a function of material and voxel size [HYP: confirm with a literature search].

**Our long-term goal** is a validated, auditable software standard for 3-class (new bone / residual graft / host bone) micro-CT analysis that preclinical teams can adopt and that regulators and journals can trust. **The objective of this Phase I** is to establish physical ground truth, build a material-aware segmentation model that reports its own uncertainty, and test whether it matches expert analysis at a fraction of the time. **Our central hypothesis** is that combining physics-based phantom calibration, material-specific priors and calibrated uncertainty will yield graft/new-bone separation that is reproducible across voxel sizes and agrees with expert consensus. The rationale comes from our synthetic-phantom benchmark: **[PENDING RESULT: synthetic-phantom benchmark — separability metric (e.g., Dice/volume error) vs. contrast-to-noise and voxel size; currently being computed]**.

**Aim 1. Build a physical-phantom ground-truth benchmark of graft vs. new-bone separability across materials and voxel sizes.** We will fabricate phantoms with known volumes and spatial layouts of [PLACEHOLDER: N] clinically used graft materials and bone-mimicking mineral references. We will scan them on the Beckman Institute Zeiss Xradia 630 Versa at [PLACEHOLDER: voxel sizes, e.g., 3 levels] and [PLACEHOLDER: kV/filter settings]. *Deliverable:* a public benchmark with a separability map (error vs. material × voxel size × noise). *Success criterion (pre-specified target, not a result):* volume error for each class within [PLACEHOLDER: ±X%] at the voxel sizes typically used in rodent studies. **[PENDING RESULT: phantom fabrication feasibility and first scans]**

**Aim 2. Develop material-aware 3-class segmentation with calibrated uncertainty and low-label adaptation.** We will train models on synthetic data generated from the Aim 1 forward model and adapt them to new materials or scanners using ≤[PLACEHOLDER: k] annotated slices (semi-supervised / domain adaptation). Voxel-wise uncertainty will be calibrated (expected calibration error) and propagated to morphometric outputs (BV/TV of new bone, residual graft fraction) as confidence intervals. *Success criteria (targets):* Dice ≥[PLACEHOLDER] vs. phantom truth; uncertainty coverage of 95% intervals within [PLACEHOLDER] of nominal. **[PENDING RESULT: baseline vs. threshold method on synthetic phantoms]**

**Aim 3. Validate retrospectively against expert manual analysis.** Using [PLACEHOLDER: N specimens] of existing de-identified preclinical micro-CT scans from [PLACEHOLDER: collaborating lab(s) — data-use agreement pending], we will compare OsteoQuant against ≥[PLACEHOLDER: 2–3] blinded expert analysts. We will measure analyst time per specimen, agreement (ICC(2,1) with 95% CI) and Bland–Altman bias and limits of agreement for new-bone volume and residual-graft volume. *Success criteria (targets):* lower 95% CI of ICC ≥[PLACEHOLDER, e.g., 0.75]; ≥[PLACEHOLDER]% reduction in analyst time; inter-expert variability reported as the reference ceiling. **[PENDING RESULT: none yet — no retrospective data obtained]**

**Expected outcomes and impact.** Phase I will deliver:
- the first (to our knowledge [verify]) physical ground-truth benchmark for graft/new-bone separability;
- a validated 3-class pipeline with uncertainty-aware morphometry;
- audited reports that make each number traceable.

These outcomes will reduce analysis time and inter-operator variability in orthobiologic development, and may reduce the number of animals needed by tightening measurement error [HYP]. Phase II will extend to multi-site, multi-scanner validation and production software for CROs and orthobiologic developers.
