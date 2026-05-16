import json
import re
import csv
import numpy as np
import qt
import slicer


SCHEMA_JSON = r'''
{
  "schemaVersion": "1.0.0",
  "source": "User-provided landmark table image and existing method GUI docs in this repository",
  "sourceImageUrl": "https://github.com/user-attachments/assets/36959dcc-ba75-40fd-86d9-518b8efb5da0",
  "scope": {
    "includedMethods": [
      "Threefold_ANS",
      "Stephan_2003",
      "Rynn_2010_necessary_only",
      "Tedeschi_Oliveira_2016",
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
  "landmarksRequiringGuidingLines": ["HT-5", "HT-24", "ST-4", "ST-17", "ST-18", "ST-19"],
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
    {"id":"HT-5","canonicalName":"Subspinale","tissueType":"hard","aka":["subspinale","ss","point A"],"requiresGuidingLine":true},
    {"id":"HT-24","canonicalName":"Nasal Suture Depth Point","tissueType":"hard","aka":["nr"],"requiresGuidingLine":true},
    {"id":"ST-4","canonicalName":"Selion / Sellion","tissueType":"soft","aka":["S","se'"],"requiresGuidingLine":true},
    {"id":"ST-17","canonicalName":"n-prn Posterior","tissueType":"soft","aka":["npp'"],"requiresGuidingLine":true},
    {"id":"ST-18","canonicalName":"n-prn Anterior","tissueType":"soft","aka":["npa'"],"requiresGuidingLine":true},
    {"id":"ST-19","canonicalName":"Nasal Drop","tissueType":"soft","aka":["nd'"],"requiresGuidingLine":true}
  ]
}
'''


def _normalize_label(label):
    if label is None:
        return ""
    s = str(label).lower().strip()
    s = s.replace("left", "_l").replace("right", "_r")
    s = s.replace("’", "'").replace("`", "'")
    s = re.sub(r"[^a-z0-9_]+", "", s)
    s = s.replace("__", "_")
    return s


def _unit(v):
    n = np.linalg.norm(v)
    return (v / n) if n > 1e-8 else np.array([1.0, 0.0, 0.0])


class UnifiedNoseMasterGUI(qt.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Unified Nose MASTER GUI")
        self.setMinimumSize(980, 760)

        self.schema = json.loads(SCHEMA_JSON)
        self.mapping = {}
        self.predictions = []
        self.errorRows = []
        self.methodNodes = {}

        self._buildAliasIndex()
        self._buildUI()

    def _buildAliasIndex(self):
        self.aliasToLandmarkIdsExact = {}
        self.aliasToLandmarkIdsNormalized = {}
        self.landmarkById = {lm["id"]: lm for lm in self.schema["landmarks"]}
        for lm in self.schema["landmarks"]:
            values = [lm["canonicalName"]] + lm.get("aka", [])
            for v in values:
                self.aliasToLandmarkIdsExact.setdefault(str(v), []).append(lm["id"])
                self.aliasToLandmarkIdsNormalized.setdefault(_normalize_label(v), []).append(lm["id"])

    def _buildUI(self):
        root = qt.QVBoxLayout(self)

        title = qt.QLabel("Unified Nose Multi-Method MASTER GUI (Copy-Paste Script)")
        title.setStyleSheet("font-weight:bold; font-size:16px;")
        root.addWidget(title)

        # Inputs
        inputsBox = qt.QGroupBox("Stage 1: Inputs and Alias Recognition")
        inputsLayout = qt.QFormLayout(inputsBox)

        self.hardSelector = slicer.qMRMLNodeComboBox()
        self.hardSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.hardSelector.noneEnabled = True
        self.hardSelector.addEnabled = False
        self.hardSelector.removeEnabled = False
        self.hardSelector.setMRMLScene(slicer.mrmlScene)

        self.softSelector = slicer.qMRMLNodeComboBox()
        self.softSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.softSelector.noneEnabled = True
        self.softSelector.addEnabled = False
        self.softSelector.removeEnabled = False
        self.softSelector.setMRMLScene(slicer.mrmlScene)

        self.mapBtn = qt.QPushButton("Auto-map Landmarks")
        self.mapBtn.clicked.connect(self.autoMap)

        inputsLayout.addRow("Hard tissue node:", self.hardSelector)
        inputsLayout.addRow("True soft tissue node (optional):", self.softSelector)
        inputsLayout.addRow(self.mapBtn)
        root.addWidget(inputsBox)

        # Mapping table
        self.mappingTable = qt.QTableWidget(0, 4)
        self.mappingTable.setHorizontalHeaderLabels(["ID", "Canonical", "Matched Label", "Status"])
        self.mappingTable.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.mappingTable)

        # Stage 2/3 controls
        opsBox = qt.QGroupBox("Stage 2/3: Guided Helpers and Reference Geometry")
        opsLayout = qt.QHBoxLayout(opsBox)
        self.guidesBtn = qt.QPushButton("Create Guiding Helpers")
        self.guidesBtn.clicked.connect(self.createGuidingHelpers)
        self.geomBtn = qt.QPushButton("Build INB/MSP/FHP Geometry")
        self.geomBtn.clicked.connect(self.buildReferenceGeometry)
        opsLayout.addWidget(self.guidesBtn)
        opsLayout.addWidget(self.geomBtn)
        root.addWidget(opsBox)

        # Stage 4 controls
        methodsBox = qt.QGroupBox("Stage 4: Method Selection and Prediction")
        methodsLayout = qt.QVBoxLayout(methodsBox)

        self.methodChecks = {}
        grid = qt.QGridLayout()
        for i, m in enumerate(self.schema["scope"]["includedMethods"]):
            c = qt.QCheckBox(m)
            c.setChecked(True)
            self.methodChecks[m] = c
            grid.addWidget(c, i // 2, i % 2)
        methodsLayout.addLayout(grid)

        form = qt.QFormLayout()
        self.sexCombo = qt.QComboBox(); self.sexCombo.addItems(["Female", "Male"])
        self.ancestryEdit = qt.QLineEdit(); self.ancestryEdit.placeholderText = "Optional"
        form.addRow("Sex:", self.sexCombo)
        form.addRow("Ancestry:", self.ancestryEdit)
        methodsLayout.addLayout(form)

        self.runBtn = qt.QPushButton("Run Selected Methods")
        self.runBtn.setStyleSheet("background-color:#28a745;color:white;font-weight:bold;padding:6px;")
        self.runBtn.clicked.connect(self.runSelectedMethods)
        methodsLayout.addWidget(self.runBtn)
        root.addWidget(methodsBox)

        # Stage 5/6 controls
        resultsOpsBox = qt.QGroupBox("Stage 5/6: Error + Export")
        resultsOpsLayout = qt.QHBoxLayout(resultsOpsBox)
        self.errorBtn = qt.QPushButton("Compute Errors")
        self.errorBtn.clicked.connect(self.computeErrors)
        self.copyBtn = qt.QPushButton("Copy Results (TSV)")
        self.copyBtn.clicked.connect(self.copyResults)
        self.exportBtn = qt.QPushButton("Export CSV")
        self.exportBtn.clicked.connect(self.exportCSV)
        resultsOpsLayout.addWidget(self.errorBtn)
        resultsOpsLayout.addWidget(self.copyBtn)
        resultsOpsLayout.addWidget(self.exportBtn)
        root.addWidget(resultsOpsBox)

        self.resultsTable = qt.QTableWidget(0, 8)
        self.resultsTable.setHorizontalHeaderLabels([
            "Method", "Landmark", "Pred_R", "Pred_A", "Pred_S",
            "Error(mm)", "TrueLabel", "Status"
        ])
        self.resultsTable.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.resultsTable)

        self.summaryLabel = qt.QLabel("Summary: (no errors yet)")
        root.addWidget(self.summaryLabel)

        self.status = qt.QLabel("Ready")
        root.addWidget(self.status)

    def _collectNodeLabels(self, node):
        labels = []
        if not node:
            return labels
        for i in range(node.GetNumberOfControlPoints()):
            labels.append((i, node.GetNthControlPointLabel(i)))
        return labels

    def autoMap(self):
        self.mapping = {}
        hard = self.hardSelector.currentNode()
        soft = self.softSelector.currentNode()

        hardLabels = self._collectNodeLabels(hard)
        softLabels = self._collectNodeLabels(soft)

        hardNorm = {}
        softNorm = {}
        for idx, lbl in hardLabels:
            hardNorm.setdefault(_normalize_label(lbl), []).append((idx, lbl))
        for idx, lbl in softLabels:
            softNorm.setdefault(_normalize_label(lbl), []).append((idx, lbl))

        rows = []
        for lm in self.schema["landmarks"]:
            tissue = lm["tissueType"]
            labelPool = hardLabels if tissue == "hard" else softLabels
            normPool = hardNorm if tissue == "hard" else softNorm
            node = hard if tissue == "hard" else soft

            if not node:
                rows.append((lm["id"], lm["canonicalName"], "", "Missing Node"))
                self.mapping[lm["id"]] = {"status": "missing", "node": None, "index": None, "label": None}
                continue

            targetLabels = [lm["canonicalName"]] + lm.get("aka", [])

            # 1) Exact canonical/alias
            exact = []
            for i, lbl in labelPool:
                if lbl in targetLabels:
                    exact.append((i, lbl))
            if len(exact) == 1:
                i, lbl = exact[0]
                rows.append((lm["id"], lm["canonicalName"], lbl, "Matched"))
                self.mapping[lm["id"]] = {"status": "matched", "node": node, "index": i, "label": lbl}
                continue
            if len(exact) > 1:
                rows.append((lm["id"], lm["canonicalName"], ", ".join([x[1] for x in exact]), "Ambiguous"))
                self.mapping[lm["id"]] = {"status": "ambiguous", "node": node, "index": None, "label": None}
                continue

            # 2) Normalized alias
            candidates = []
            for t in targetLabels:
                candidates.extend(normPool.get(_normalize_label(t), []))
            uniq = {(i, lbl) for i, lbl in candidates}
            candidates = list(uniq)

            if len(candidates) == 1:
                i, lbl = candidates[0]
                rows.append((lm["id"], lm["canonicalName"], lbl, "Matched"))
                self.mapping[lm["id"]] = {"status": "matched", "node": node, "index": i, "label": lbl}
            elif len(candidates) > 1:
                rows.append((lm["id"], lm["canonicalName"], ", ".join([x[1] for x in candidates]), "Ambiguous"))
                self.mapping[lm["id"]] = {"status": "ambiguous", "node": node, "index": None, "label": None}
            else:
                rows.append((lm["id"], lm["canonicalName"], "", "Missing"))
                self.mapping[lm["id"]] = {"status": "missing", "node": node, "index": None, "label": None}

        self._fillTable(self.mappingTable, rows)
        self.status.setText("Mapping complete")

    def _getPoint(self, landmark_id):
        m = self.mapping.get(landmark_id)
        if not m or m.get("status") != "matched":
            return None
        p = np.zeros(3)
        m["node"].GetNthControlPointPositionWorld(m["index"], p)
        return p

    def createGuidingHelpers(self):
        if not self.mapping:
            self.autoMap()

        created = 0
        for lm_id in self.schema.get("landmarksRequiringGuidingLines", []):
            p = self._getPoint(lm_id)
            if p is None:
                continue
            n = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", f"guide_{lm_id}")
            n.AddControlPoint(p - np.array([5.0, 0.0, 0.0]))
            n.AddControlPoint(p + np.array([5.0, 0.0, 0.0]))
            dn = n.GetDisplayNode() or (n.CreateDefaultDisplayNodes() or n.GetDisplayNode())
            if dn:
                dn.SetSelectedColor(1.0, 1.0, 0.0)
            created += 1

        self.status.setText(f"Created {created} guiding helper line(s)")

    def buildReferenceGeometry(self):
        if not self.mapping:
            self.autoMap()

        # INB plane
        p_inion = self._getPoint("HT-2")
        p_nasion = self._getPoint("HT-1")
        p_bregma = self._getPoint("HT-3")
        if p_inion is not None and p_nasion is not None and p_bregma is not None:
            v1 = p_nasion - p_inion
            v2 = p_bregma - p_inion
            normal = _unit(np.cross(v1, v2))
            inb = slicer.util.getFirstNodeByName("INB") or slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "INB")
            inb.SetOrigin(p_inion)
            inb.SetNormal(normal)
            inb.SetSize(300, 300)

        # MSP plane (best-fit over available hard midsagittal points)
        msp_ids = ["HT-1", "HT-4", "HT-5", "HT-6", "HT-7"]
        pts = [self._getPoint(i) for i in msp_ids]
        pts = [p for p in pts if p is not None]
        if len(pts) >= 3:
            arr = np.array(pts)
            center = arr.mean(axis=0)
            cov = np.cov((arr - center).T)
            _, eigvec = np.linalg.eigh(cov)
            normal = _unit(eigvec[:, 0])
            msp = slicer.util.getFirstNodeByName("MSP") or slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "MSP")
            msp.SetOrigin(center)
            msp.SetNormal(normal)
            msp.SetSize(300, 300)

        # Approximate FHP from orbitale L/R + midpoint(nasion,prosthion)
        p_orL = self._getPoint("HT-8")
        p_orR = self._getPoint("HT-9")
        p_pr = self._getPoint("HT-4")
        if p_orL is not None and p_orR is not None and p_nasion is not None and p_pr is not None:
            porion_proxy = (p_nasion + p_pr) / 2.0
            v1 = p_orR - p_orL
            v2 = porion_proxy - p_orL
            normal = _unit(np.cross(v1, v2))
            fhp = slicer.util.getFirstNodeByName("FHP") or slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "FHP")
            fhp.SetOrigin((p_orL + p_orR + porion_proxy) / 3.0)
            fhp.SetNormal(normal)
            fhp.SetSize(300, 300)

        self.status.setText("Reference geometry updated (INB/MSP/FHP where possible)")

    def _predict_method_points(self, method):
        # Shared anchors
        p_nas = self._getPoint("HT-1")
        p_rhi = self._getPoint("HT-6")
        p_aca = self._getPoint("HT-7")
        p_al_l = self._getPoint("HT-12")
        p_al_r = self._getPoint("HT-13")

        if p_nas is None or p_rhi is None or p_aca is None:
            return None

        axis_forward = _unit(p_rhi - p_aca)
        axis_superior = _unit(p_nas - p_aca)
        axis_lateral = _unit(np.cross(axis_superior, axis_forward))

        # Method-specific forward multipliers (scaffold hooks)
        k = {
            "Threefold_ANS": 0.70,
            "Stephan_2003": 0.66,
            "Rynn_2010_necessary_only": 0.64,
            "Tedeschi_Oliveira_2016": 0.62,
            "Ridel_2018": 0.68,
            "Ryu_2020": 0.65,
            "Thitiorul_2020": 0.63,
            "Purkait_Singh_2024": 0.67,
        }.get(method, 0.65)

        span = np.linalg.norm(p_rhi - p_aca)
        pronasale = p_rhi + axis_forward * (k * span) + axis_superior * (0.08 * span)
        subnasale = p_aca + axis_forward * (0.15 * span)

        al_l = (p_al_l + axis_lateral * (0.06 * span)) if p_al_l is not None else (subnasale + axis_lateral * (0.20 * span))
        al_r = (p_al_r - axis_lateral * (0.06 * span)) if p_al_r is not None else (subnasale - axis_lateral * (0.20 * span))

        return {
            "Pronasale": pronasale,
            "Subnasale": subnasale,
            "Alare_L": al_l,
            "Alare_R": al_r,
        }

    def runSelectedMethods(self):
        if not self.mapping:
            self.autoMap()

        self.predictions = []
        self.errorRows = []
        self.methodNodes = {}

        selected = [m for m, c in self.methodChecks.items() if c.isChecked()]
        if not selected:
            slicer.util.warningDisplay("Please select at least one method.")
            return

        for method in selected:
            pts = self._predict_method_points(method)
            if pts is None:
                self.predictions.append({
                    "method": method, "landmark": "-", "point": None,
                    "status": "Missing prerequisites (need Nasion/Rhinion/Acanthion)"
                })
                continue

            node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", f"Pred_{method}")
            for name, p in pts.items():
                idx = node.AddControlPoint(p)
                node.SetNthControlPointLabel(idx, f"Pred_{method}_{name}")
                self.predictions.append({"method": method, "landmark": name, "point": p, "status": "Predicted"})
            self.methodNodes[method] = node

        self.refreshResultsTable()
        self.status.setText(f"Ran {len(selected)} method(s)")

    def _truePointByPredLandmark(self, predLandmark):
        lookup = {
            "Pronasale": "ST-3",
            "Subnasale": "ST-2",
            "Alare_L": "ST-9",
            "Alare_R": "ST-10",
        }
        lid = lookup.get(predLandmark)
        if not lid:
            return None, None
        m = self.mapping.get(lid)
        if not m or m.get("status") != "matched":
            return None, None
        p = np.zeros(3)
        m["node"].GetNthControlPointPositionWorld(m["index"], p)
        return p, m.get("label")

    def computeErrors(self):
        if not self.predictions:
            slicer.util.warningDisplay("Run selected methods first.")
            return

        self.errorRows = []
        errs = []
        for row in self.predictions:
            if row.get("point") is None:
                continue
            trueP, trueLabel = self._truePointByPredLandmark(row["landmark"])
            if trueP is None:
                self.errorRows.append((row["method"], row["landmark"], None, "", "No true landmark"))
                continue

            d = float(np.linalg.norm(row["point"] - trueP))
            errs.append(d)
            self.errorRows.append((row["method"], row["landmark"], d, trueLabel, "OK"))

            line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", f"error_{row['method']}_{row['landmark']}")
            line.AddControlPoint(row["point"])
            line.AddControlPoint(trueP)

        if errs:
            arr = np.array(errs, dtype=float)
            self.summaryLabel.setText(
                f"Summary: mean={arr.mean():.2f} mm | median={np.median(arr):.2f} mm | sd={arr.std(ddof=0):.2f} mm | min={arr.min():.2f} mm | max={arr.max():.2f} mm"
            )
        else:
            self.summaryLabel.setText("Summary: no comparable true soft-tissue landmarks found")

        self.refreshResultsTable()
        self.status.setText("Error computation complete")

    def refreshResultsTable(self):
        errorIndex = {(m, l): (e, tl, st) for (m, l, e, tl, st) in self.errorRows}
        rows = []
        for p in self.predictions:
            method = p["method"]
            landmark = p["landmark"]
            point = p.get("point")
            if point is None:
                rows.append((method, landmark, "", "", "", "", "", p.get("status", "")))
                continue
            err, trueLabel, eStatus = errorIndex.get((method, landmark), (None, "", ""))
            rows.append((
                method,
                landmark,
                f"{point[0]:.2f}",
                f"{point[1]:.2f}",
                f"{point[2]:.2f}",
                (f"{err:.2f}" if err is not None else ""),
                trueLabel,
                eStatus or p.get("status", "")
            ))
        self._fillTable(self.resultsTable, rows)

    def _fillTable(self, table, rows):
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                table.setItem(r, c, qt.QTableWidgetItem(str(val)))
        table.resizeColumnsToContents()

    def _tableToTSV(self, table):
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount)]
        lines = ["\t".join(headers)]
        for r in range(table.rowCount):
            vals = []
            for c in range(table.columnCount):
                item = table.item(r, c)
                vals.append(item.text() if item else "")
            lines.append("\t".join(vals))
        return "\n".join(lines)

    def copyResults(self):
        text = self._tableToTSV(self.resultsTable)
        qt.QApplication.clipboard().setText(text)
        slicer.util.infoDisplay("Results copied to clipboard.")

    def exportCSV(self):
        path = qt.QFileDialog.getSaveFileName(self, "Export Results CSV", "nose_master_results.csv", "CSV (*.csv)")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            headers = [self.resultsTable.horizontalHeaderItem(i).text() for i in range(self.resultsTable.columnCount)]
            writer.writerow(headers)
            for r in range(self.resultsTable.rowCount):
                row = []
                for c in range(self.resultsTable.columnCount):
                    item = self.resultsTable.item(r, c)
                    row.append(item.text() if item else "")
                writer.writerow(row)
        slicer.util.infoDisplay(f"CSV exported: {path}")


# Launch helper (safe re-run)
def launch_unified_nose_master_gui():
    for w in qt.QApplication.topLevelWidgets():
        if w.objectName == "UnifiedNoseMasterGUI":
            w.close()
    gui = UnifiedNoseMasterGUI()
    gui.setObjectName("UnifiedNoseMasterGUI")
    gui.show()
    return gui


# Auto-launch on paste
_unified_nose_master_gui_instance = launch_unified_nose_master_gui()
