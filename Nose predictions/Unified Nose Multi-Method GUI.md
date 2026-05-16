# Unified Nose Multi-Method GUI (Single-Scene Workflow) — Final Consolidated Version

This file is the complete final deliverable in one place.

## Scope
This unified GUI combines most nose approximation workflows into one scene in 3D Slicer.

### Included methods
- Threefold ANS (Krogman & Iscan)
- Stephan et al. (2003)
- Rynn et al. (2010) **(necessary components only)**
- Tedeschi-Oliviera (2016)
- Ridel et al. (2018)
- Ryu et al. (2020)
- Thitiorul et al. (2020)
- Purkait & Singh (2024)

### Excluded methods
- Gerasimov - Maltais-Lapointe (Two Tangent)
- Prokopec & Ubelaker (Aesthetic Method)

---

## Unified GUI design

### Stage 1 — Inputs and Alias Recognition
- Select hard tissue landmark node
- Optional: select true soft tissue landmark node (for error analysis)
- Load landmark schema from the embedded JSON below
- Auto-map labels by alias (case-insensitive, punctuation-insensitive)
- Show mapping table with status:
  - Matched
  - Ambiguous
  - Missing

### Stage 2 — Guided Placement Helpers
- Create helper guide lines for landmarks that need line-based placement
- Toggle guide-line visibility
- Lock/unlock guided endpoints

### Stage 3 — Reference Geometry
- Build reference planes/axes used across methods:
  - MSP (best-fit option)
  - INB (optional alternative where needed)
  - FHP (if selected)
  - Supporting transverse/coronal/sagittal planes required by method equations

### Stage 4 — Method Selection and Prediction
- Method checklist with per-method enable/disable
- Global controls for demographics when relevant (sex/ancestry where required by equations)
- One-click **Run Selected Methods**
- Create predicted landmarks in per-method nodes:
  - `Pred_<Method>_<Landmark>`

### Stage 5 — Error Measurement
If true soft tissue landmarks are available:
- Compute point-to-point 3D Euclidean errors by method and landmark
- Compute summary metrics:
  - Mean error
  - Median error
  - SD
  - Min/Max
- Create optional error lines (`error_<Method>_<Landmark>`)

### Stage 6 — Results and Export
- Results table (rows = landmarks, columns = methods + summary)
- Missing-data indicators when method-specific prerequisites are absent
- Copy to clipboard
- Export CSV/TSV
- Save scene state and method settings

---

## Alias recognition rules
- Normalize labels before matching:
  - lowercase
  - trim spaces
  - remove punctuation and apostrophe variants
  - normalize left/right suffix forms (`_L`, `L`, `Left` etc.)
- Match order:
  1. Exact canonical name
  2. Exact alias in JSON
  3. Normalized alias
  4. Left/right fallback with side inference
- If multiple matches remain, mark as ambiguous and require user confirmation.

---

## Necessary-only components from Rynn method
To keep scope aligned with your request, include only components needed for shared prediction/error workflows:
- Core reference setup (plane/axis support used by downstream equations)
- Essential base measurements reused by prediction pipelines
- Omit optional advanced projection-network-only branches when not needed for selected methods

---

## Output contract
For each selected method:
- Predicted landmark coordinates
- Intermediate measurement values used by equations
- Per-landmark error (if true soft tissue present)

Global outputs:
- Combined prediction table
- Combined error table
- Scene nodes grouped by method

---

## Master landmark JSON (canonical names + aliases)

> Landmarks that require additional guiding lines are intentionally placed at the end.

```json
{
  "schemaVersion": "1.0.0",
  "source": "User-provided landmark table image and existing method GUI docs in this repository",
  "scope": {
    "includedMethods": [
      "Threefold_ANS",
      "Stephan_2003",
      "Rynn_2010_necessary_only",
      "Tedeschi_Oliviera_2016",
      "Ridel_2018",
      "Ryu_2020",
      "Thitiorul_2020",
      "Purkait_Singh_2024"
    ],
    "excludedMethods": [
      "Gerasimov_Maltais_Lapointe",
      "Prokopec_Ubelaker"
    ]
  },
  "normalizationRules": {
    "caseInsensitive": true,
    "stripPunctuation": true,
    "stripWhitespace": true,
    "leftRightNormalization": true
  },
  "landmarks": [
    {"id":"HT-1","canonicalName":"Nasion","tissueType":"hard","aka":["nasion","N","n"]},
    {"id":"HT-2","canonicalName":"Inion","tissueType":"hard","aka":["inion"]},
    {"id":"HT-3","canonicalName":"Bregma","tissueType":"hard","aka":["bregma"]},
    {"id":"HT-4","canonicalName":"Prosthion","tissueType":"hard","aka":["prosthion","pr"]},
    {"id":"HT-6","canonicalName":"Rhinion","tissueType":"hard","aka":["rhinion","R","rhi"]},
    {"id":"HT-7","canonicalName":"Acanthion / Anterior Nasal Spine","tissueType":"hard","aka":["acanthion","AC","ANS","ns","a"]},
    {"id":"HT-8","canonicalName":"Orbitale Left","tissueType":"hard","aka":["O_L"]},
    {"id":"HT-9","canonicalName":"Orbitale Right","tissueType":"hard","aka":["O_R"]},
    {"id":"HT-10","canonicalName":"Inferior Nasal Concha Left","tissueType":"hard","aka":["IC_L"]},
    {"id":"HT-11","canonicalName":"Inferior Nasal Concha Right","tissueType":"hard","aka":["IC_R"]},
    {"id":"HT-12","canonicalName":"Hard Tissue Alare Left (Most Lateral Nasal/Piriform)","tissueType":"hard","aka":["A_L","alL","B (PA_L)"]},
    {"id":"HT-13","canonicalName":"Hard Tissue Alare Right (Most Lateral Nasal/Piriform)","tissueType":"hard","aka":["A_R","alR","A (PA_R)"]},
    {"id":"HT-14","canonicalName":"Left Posterior Piriform Aperture Border","tissueType":"hard","aka":["NAG_L"]},
    {"id":"HT-15","canonicalName":"Right Posterior Piriform Aperture Border","tissueType":"hard","aka":["NAG_R"]},
    {"id":"HT-16","canonicalName":"Left Nasal Aperture Inferior / Lowest Bony Pyriform","tissueType":"hard","aka":["NAI_L","LL","D (PAB_L)"]},
    {"id":"HT-17","canonicalName":"Right Nasal Aperture Inferior / Lowest Bony Pyriform","tissueType":"hard","aka":["NAI_R","RL","C (PAB_R)"]},
    {"id":"HT-18","canonicalName":"Left Zygion","tissueType":"hard","aka":["zy_L"]},
    {"id":"HT-19","canonicalName":"Right Zygion","tissueType":"hard","aka":["zy_R"]},
    {"id":"HT-20","canonicalName":"Left Ectomolare","tissueType":"hard","aka":["ecm_L"]},
    {"id":"HT-21","canonicalName":"Right Ectomolare","tissueType":"hard","aka":["ecm_R"]},
    {"id":"HT-22","canonicalName":"Left Infraorbital Foramen","tissueType":"hard","aka":["iof_L"]},
    {"id":"HT-23","canonicalName":"Right Infraorbital Foramen","tissueType":"hard","aka":["iof_R"]},
    {"id":"HT-25","canonicalName":"Vomer-Maxillary Junction","tissueType":"hard","aka":["VMJ"]},

    {"id":"ST-1","canonicalName":"Soft Tissue Nasion","tissueType":"soft","aka":["soft nasion","n'","soft tissue nasion"]},
    {"id":"ST-2","canonicalName":"Subnasale","tissueType":"soft","aka":["subnasale","SN","sn'"]},
    {"id":"ST-3","canonicalName":"Pronasale","tissueType":"soft","aka":["pronasale","PN","prn","pn'"]},
    {"id":"ST-5","canonicalName":"Left Alar Groove / Curvature Superior","tissueType":"soft","aka":["ACS_L","als'L"]},
    {"id":"ST-6","canonicalName":"Right Alar Groove / Curvature Superior","tissueType":"soft","aka":["ACS_R","als'R"]},
    {"id":"ST-7","canonicalName":"Left Alar Groove / Curvature Posterior","tissueType":"soft","aka":["ACP_L","alp'L"]},
    {"id":"ST-8","canonicalName":"Right Alar Groove / Curvature Posterior","tissueType":"soft","aka":["ACP_R","alp'R"]},
    {"id":"ST-9","canonicalName":"Left Alare (Soft Tissue)","tissueType":"soft","aka":["NA_L","X1(alL)","al'L"]},
    {"id":"ST-10","canonicalName":"Right Alare (Soft Tissue)","tissueType":"soft","aka":["NA_R","X2(alR)","al'R"]},
    {"id":"ST-11","canonicalName":"Left Alar Groove / Curvature Inferior","tissueType":"soft","aka":["ACI_L","ali'L"]},
    {"id":"ST-12","canonicalName":"Right Alar Groove / Curvature Inferior","tissueType":"soft","aka":["ACI_R","ali'R"]},
    {"id":"ST-13","canonicalName":"Soft Tissue Rhinion","tissueType":"soft","aka":["rhi'"]},
    {"id":"ST-14","canonicalName":"Nasal Tip Inferior","tissueType":"soft","aka":["nt"]},
    {"id":"ST-15","canonicalName":"Left Nasal Base Attachment","tissueType":"soft","aka":["Y1(nbL)"]},
    {"id":"ST-16","canonicalName":"Right Nasal Base Attachment","tissueType":"soft","aka":["Y2(nbR)"]},

    {"id":"HT-5","canonicalName":"Subspinale","tissueType":"hard","aka":["subspinale","ss","point A"],"requiresGuidingLine":true,"guidingLine":"Programmed helper line for point placement"},
    {"id":"HT-24","canonicalName":"Nasal Suture Depth Point","tissueType":"hard","aka":["nr"],"requiresGuidingLine":true,"guidingLine":"Programmed helper line for point placement"},
    {"id":"ST-4","canonicalName":"Selion / Sellion","tissueType":"soft","aka":["S","se'"],"requiresGuidingLine":true,"guidingLine":"Programmed helper line for point placement"},
    {"id":"ST-17","canonicalName":"n-prn Posterior","tissueType":"soft","aka":["npp'"],"requiresGuidingLine":true,"guidingLine":"Programmed helper line for point placement"},
    {"id":"ST-18","canonicalName":"n-prn Anterior","tissueType":"soft","aka":["npa'"],"requiresGuidingLine":true,"guidingLine":"Programmed helper line for point placement"},
    {"id":"ST-19","canonicalName":"Nasal Drop","tissueType":"soft","aka":["nd'"],"requiresGuidingLine":true,"guidingLine":"Programmed helper line for point placement"}
  ]
}
```
