# Unified Nose Multi-Method GUI (Single-Scene Workflow)

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
- Load landmark schema from `nose_master_landmarks.json`
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

## Landmark schema file
Use: `Nose predictions/nose_master_landmarks.json`

- Includes canonical landmark names + aliases
- Keeps line-guided landmarks at the end
- Supports robust cross-method naming recognition
