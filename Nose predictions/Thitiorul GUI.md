```python
import os
import qt
import slicer
import vtk
import numpy as np
import urllib.request
import tempfile
import json
from collections import OrderedDict

class ThitiorulGUI:
    def __init__(self):
        """Initialize the GUI with multi-run comparison and save/load state features."""
        
        self.mainWidget = qt.QWidget()
        self.mainWidget.setWindowFlags(self.mainWidget.windowFlags() | qt.Qt.WindowStaysOnTopHint)
        self.mainWidget.setWindowTitle("Thitiorul (2020) Nose Prediction Method")
        self.mainWidget.setMinimumSize(650, 800)
        
        scrollArea = qt.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollContent = qt.QWidget()
        mainLayout = qt.QVBoxLayout(scrollContent)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        titleLabel = qt.QLabel("Thitiorul et al. (2020) Method")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 16px;")
        titleLabel.setAlignment(qt.Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)
        
        self.prediction_runs = OrderedDict()
        self.colors = [[1, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0.5, 0], [0.5, 1, 0.5]]
        
        self.topLayout = mainLayout
        self.error_tolerance = 0.1

        self.populateAllSteps(350)

        scrollArea.setWidget(scrollContent)
        outerLayout = qt.QVBoxLayout(self.mainWidget)
        outerLayout.setContentsMargins(0, 0, 0, 0)
        outerLayout.addWidget(scrollArea)
        
        self.refNasionNode = None
        self.hardTissueNode = None
        self.softTissueNode = None
        self.mspPlaneNode = None
        self.xzPlaneNode = None
        self.transformNode = None
        self.transform_applied = False

        self.setGuiState(False)
        self.syncWithScene()
        self.mainWidget.show()

    def get_text_safe(self, widget):
        """Safely get text from a Qt widget, whether .text is a method or property."""
        if hasattr(widget, 'text'):
            if callable(widget.text):
                return widget.text()
            else:
                return str(widget.text)
        return ""

    def createStepGroupBox(self, title, parentLayout):
        groupBox = qt.QGroupBox(title)
        groupBox.setLayout(qt.QVBoxLayout())
        parentLayout.addWidget(groupBox)
        return groupBox

    def setGuiState(self, transform_done):
        self.transform_applied = transform_done
        boxes = [self.step2GroupBox, self.step3GroupBox, self.step4GroupBox, 
                 self.step5GroupBox, self.step6GroupBox, self.step7GroupBox]
        for box in boxes:
            box.setEnabled(transform_done)
        if not transform_done:
            slicer.util.showStatusMessage("Please complete Step 1 to unlock.", 3000)

    def populateAllSteps(self, buttonWidth):
        self.step1GroupBox = self.createStepGroupBox("Step 1: Set Up Coordinate System (Nasion as Origin)", self.topLayout)
        self.step2GroupBox = self.createStepGroupBox("Step 2: Load Hard Tissue Landmarks", self.topLayout)
        self.step3GroupBox = self.createStepGroupBox("Step 3: Create MSP and X-Z Plane", self.topLayout)
        self.step4GroupBox = self.createStepGroupBox("Step 4: Predict Soft Tissue", self.topLayout)
        self.step5GroupBox = self.createStepGroupBox("Step 5: Load True Soft Tissue (for validation)", self.topLayout)
        self.step6GroupBox = self.createStepGroupBox("Step 6: Calculate Errors", self.topLayout)
        self.step7GroupBox = self.createStepGroupBox("Step 7: View and Save Results", self.topLayout)
        
        # Step 1 Layout
        step1Layout = self.step1GroupBox.layout()
        step1InfoLabel = qt.QLabel(
            "<b>To begin, let's set nasion to (0,0,0). Follow these steps:</b><br><br>"
            "1. Click 'Download Reference Nasion'. A yellow point will appear.<br>"
            "2. In the 3D Slicer window, <b>move the yellow point</b> to mark the exact location of nasion on your scan.<br>"
            "3. When you are happy with the position, click 'Apply Transform'."
        )
        step1InfoLabel.setWordWrap(True)
        step1Layout.addWidget(step1InfoLabel)
        
        self.downloadRefNasionButton = qt.QPushButton("1. Download Reference Nasion")
        self.downloadRefNasionButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.downloadRefNasionButton.setFixedWidth(buttonWidth)
        self.downloadRefNasionButton.clicked.connect(self.onDownloadRefNasionClicked)
        step1Layout.addWidget(self.downloadRefNasionButton, 0, qt.Qt.AlignHCenter)
        
        self.applyTransformButton = qt.QPushButton("2. Apply Transform")
        self.applyTransformButton.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 8px;")
        self.applyTransformButton.setFixedWidth(buttonWidth)
        self.applyTransformButton.clicked.connect(self.onApplyTransformClicked)
        step1Layout.addWidget(self.applyTransformButton, 0, qt.Qt.AlignHCenter)

        # Step 2 Layout
        step2Layout = self.step2GroupBox.layout()
        self.hardTissueSelector = slicer.qMRMLNodeComboBox()
        self.hardTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.hardTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.hardTissueSelector.noneEnabled = True
        step2Layout.addWidget(self.hardTissueSelector)
        
        self.downloadHardButton = qt.QPushButton("Download Hard Tissue Landmarks")
        self.downloadHardButton.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        self.downloadHardButton.setFixedWidth(buttonWidth)
        self.downloadHardButton.clicked.connect(self.onDownloadHardLandmarksClicked)
        step2Layout.addWidget(self.downloadHardButton, 0, qt.Qt.AlignHCenter)
        
        self.createHardGuideLinesButton = qt.QPushButton("Create Guide Lines (optional)")
        self.createHardGuideLinesButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px;")
        self.createHardGuideLinesButton.setFixedWidth(buttonWidth)
        self.createHardGuideLinesButton.clicked.connect(self.onCreateHardGuideLinesClicked)
        step2Layout.addWidget(self.createHardGuideLinesButton, 0, qt.Qt.AlignHCenter)
        
        # Step 3 Layout
        step3Layout = self.step3GroupBox.layout()
        self.createPlanesButton = qt.QPushButton("Create MSP and X-Z Plane")
        self.createPlanesButton.setStyleSheet("background-color: #FFDF00; font-weight: bold; padding: 8px;")
        self.createPlanesButton.setFixedWidth(buttonWidth)
        self.createPlanesButton.clicked.connect(self.onCreatePlanesClicked)
        step3Layout.addWidget(self.createPlanesButton, 0, qt.Qt.AlignHCenter)
        
        self.visualizeAxesButton = qt.QPushButton("Visualize Axes (optional)")
        self.visualizeAxesButton.setFixedWidth(buttonWidth)
        self.visualizeAxesButton.clicked.connect(self.onVisualizeAxesClicked)
        step3Layout.addWidget(self.visualizeAxesButton, 0, qt.Qt.AlignHCenter)
        
        # Step 4 Layout
        layout4 = self.step4GroupBox.layout()
        info4Label = qt.QLabel("<b>Choose prediction method:</b>")
        layout4.addWidget(info4Label)

        explanationLabel = qt.QLabel(
            "<ul>"
            "<li><b>Mirror (as paper):</b> Strictly follows the published 2020 paper. It calculates coordinates from left-side points and mirrors them for the right side.</li>"
            "<li><b>Auto-replace missing:</b> Uses side-specific formulas but automatically substitutes a missing landmark (e.g., iof_R) with its contralateral counterpart (iof_L) to ensure the prediction can run.</li>"
            "<li><b>Side-specific:</b> Uses the separate, more accurate formulas for the right side, requiring all right-side landmarks to be present.</li>"
            "</ul>"
        )
        explanationLabel.setWordWrap(True)
        layout4.addWidget(explanationLabel)

        self.predictionMethodGroup = qt.QButtonGroup()

        self.mirrorRadio = qt.QRadioButton("Mirror (as paper)")
        self.mirrorRadio.setChecked(True)
        self.predictionMethodGroup.addButton(self.mirrorRadio, 1)

        self.autoReplaceRadio = qt.QRadioButton("Auto-replace missing")
        self.predictionMethodGroup.addButton(self.autoReplaceRadio, 2)

        self.sideSpecificRadio = qt.QRadioButton("Side-specific")
        self.predictionMethodGroup.addButton(self.sideSpecificRadio, 3)

        layout4.addWidget(self.mirrorRadio)
        layout4.addWidget(self.autoReplaceRadio)
        layout4.addWidget(self.sideSpecificRadio)

        self.predictButton = qt.QPushButton("Run Prediction")
        self.predictButton.setStyleSheet("background-color: #00BCD4; color: white; font-weight: bold; padding: 8px;")
        self.predictButton.setFixedWidth(buttonWidth)
        self.predictButton.clicked.connect(self.onPredictClicked)
        layout4.addWidget(self.predictButton, 0, qt.Qt.AlignHCenter)
        
        # Step 5 Layout
        layout5 = self.step5GroupBox.layout()
        self.softTissueSelector = slicer.qMRMLNodeComboBox()
        self.softTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.softTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.softTissueSelector.noneEnabled = True
        layout5.addWidget(self.softTissueSelector)
        
        self.downloadSoftButton = qt.QPushButton("Download True Soft Tissue Landmarks")
        self.downloadSoftButton.setStyleSheet("background-color: #8BC34A; color: white; font-weight: bold; padding: 8px;")
        self.downloadSoftButton.setFixedWidth(buttonWidth)
        self.downloadSoftButton.clicked.connect(self.onDownloadSoftLandmarksClicked)
        layout5.addWidget(self.downloadSoftButton, 0, qt.Qt.AlignHCenter)
        
        self.createSoftGuideLinesButton = qt.QPushButton("Create Soft Guide Lines (optional)")
        self.createSoftGuideLinesButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px;")
        self.createSoftGuideLinesButton.setFixedWidth(buttonWidth)
        self.createSoftGuideLinesButton.clicked.connect(self.onCreateSoftGuideLinesClicked)
        layout5.addWidget(self.createSoftGuideLinesButton, 0, qt.Qt.AlignHCenter)

        # Step 6 Layout
        layout6 = self.step6GroupBox.layout()
        self.calculateErrorsButton = qt.QPushButton("Calculate All Errors")
        self.calculateErrorsButton.setStyleSheet("background-color: #E91E63; color: white; font-weight: bold; padding: 8px;")
        self.calculateErrorsButton.setFixedWidth(buttonWidth)
        self.calculateErrorsButton.clicked.connect(self.onCalculateAllErrors)
        layout6.addWidget(self.calculateErrorsButton, 0, qt.Qt.AlignHCenter)

        # Step 7 Layout
        layout7 = self.step7GroupBox.layout()
        self.resultsTable = qt.QTableWidget()
        self.resultsTable.setColumnCount(1)
        self.resultsTable.setHorizontalHeaderLabels(["Landmark"])
        
        landmarks = ["se'", "npp'", "npa'", "pn'", "nd'", "sn'", 
                     "al'L", "als'L", "alp'L", "ali'L", 
                     "al'R", "als'R", "alp'R", "ali'R"]
        self.resultsTable.setRowCount(len(landmarks))
        for i, name in enumerate(landmarks):
            self.resultsTable.setItem(i, 0, qt.QTableWidgetItem(name))
        
        self.resultsTable.setMinimumHeight(300)
        layout7.addWidget(self.resultsTable)
        
        exportLayout = qt.QHBoxLayout()
        self.saveButton = qt.QPushButton("Save Summary to CSV")
        self.saveButton.setStyleSheet("background-color: #3f51b5; color: white; font-weight: bold; padding: 8px;")
        self.saveButton.clicked.connect(self.onSaveToCSV)
        self.copySummaryButton = qt.QPushButton("Copy Summary to Clipboard")
        self.copySummaryButton.clicked.connect(self.onCopySummaryToClipboard)
        exportLayout.addWidget(self.saveButton)
        exportLayout.addWidget(self.copySummaryButton)
        layout7.addLayout(exportLayout)
        
        self.showDetailedButton = qt.QPushButton("Show Detailed Results...")
        self.showDetailedButton.setStyleSheet("background-color: #795548; color: white; padding: 8px;")
        self.showDetailedButton.clicked.connect(self.onShowDetailedResultsClicked)
        layout7.addWidget(self.showDetailedButton)

        self.clearButton = qt.QPushButton("Clear All Predictions & Results")
        self.clearButton.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 8px;")
        self.clearButton.clicked.connect(self.onClearAll)
        layout7.addWidget(self.clearButton)
    
    def onCopyToClipboard(self, table_widget):
        clipboard = qt.QApplication.clipboard()
        if not clipboard:
            slicer.util.warningDisplay("Clipboard not available.")
            return
        
        text = ""
        headers = [table_widget.horizontalHeaderItem(i).text().replace("\n", " ") for i in range(table_widget.columnCount)]
        text += "\t".join(headers) + "\n"
        
        for row in range(table_widget.rowCount):
            row_data = [table_widget.item(row, col).text().replace("\n", " ") if table_widget.item(row, col) else "" for col in range(table_widget.columnCount)]
            text += "\t".join(row_data) + "\n"
            
        clipboard.setText(text)
        slicer.util.showStatusMessage("Table contents copied to clipboard.", 3000)

    def onCopySummaryToClipboard(self):
        self.onCopyToClipboard(self.resultsTable)

    def syncWithScene(self):
        try:
            self.transformNode = slicer.util.getNode("MoveToOrigin")
            self.setGuiState(True)
        except:
            self.setGuiState(False)
        
        for name, selector in [("Thitiorul_hard_tissue", self.hardTissueSelector), ("true_Thitiorul_soft_tissue", self.softTissueSelector)]:
            try:
                node = slicer.util.getNode(name)
                selector.setCurrentNode(node)
                if "hard" in name: self.hardTissueNode = node
                else: self.softTissueNode = node
            except: pass
        
        for method_name in ["mirror", "replace", "side"]:
            try:
                pred_node = slicer.util.getNode(f"Predicted_Thitiorul_{method_name}")
                if pred_node and method_name not in self.prediction_runs:
                    color_idx = len(self.prediction_runs) % len(self.colors)
                    self.prediction_runs[method_name] = {'node_id': pred_node.GetID(), 'color': self.colors[color_idx]}
                    pred_node.GetDisplayNode().SetSelectedColor(*self.colors[color_idx])
            except: pass
        
        if len(self.prediction_runs) > 0 and self.softTissueNode:
            self.onCalculateAllErrors()
        
    def onDownloadRefNasionClicked(self):
        node = self.download_and_load_markup(
            "https://github.com/user-attachments/files/20638483/reference_nasion.mrk.json",
            "reference_nasion", [1, 1, 0], 2.5)
        if node:
            self.refNasionNode = node
            node.GetDisplayNode().SetVisibility(True)
            self.show_popup("Reference Point Loaded", "A yellow point has been loaded.\nPlease move it to nasion, then click 'Apply Transform'.")

    def onDownloadHardLandmarksClicked(self):
        node = self.download_and_load_markup(
            "https://github.com/user-attachments/files/23696758/Thitiorul_hard_tissue.mrk.json",
            "Thitiorul_hard_tissue", [0, 1, 0], 1.5, harden=True)
        if node:
            self.hardTissueNode = node
            self.hardTissueSelector.setCurrentNode(node)

    def onDownloadSoftLandmarksClicked(self):
        node = self.download_and_load_markup(
            "https://github.com/user-attachments/files/23696755/true_Thitiorul_soft_tissue.mrk.json",
            "true_Thitiorul_soft_tissue", [0, 1, 1], 1.5, harden=True)
        if node:
            self.softTissueNode = node
            self.softTissueSelector.setCurrentNode(node)

    def download_and_load_markup(self, url, name, color, scale, harden=False):
        try:
            with urllib.request.urlopen(url) as response, tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json') as temp:
                temp.write(response.read())
                temp_filename = temp.name
            
            node = slicer.util.loadMarkups(temp_filename)
            node.SetName(name)
            os.unlink(temp_filename)
            
            display_node = node.GetDisplayNode()
            display_node.SetSelectedColor(*color)
            display_node.SetGlyphScale(scale)
            display_node.SetVisibility(True)
            
            if harden and self.transform_applied and self.transformNode:
                node.SetAndObserveTransformNodeID(self.transformNode.GetID())
                slicer.vtkSlicerTransformLogic().hardenTransform(node)
            return node
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to download {name}: {e}")
            return None

    def onApplyTransformClicked(self):
        try:
            if not self.refNasionNode: self.refNasionNode = slicer.util.getNode("reference_nasion")
            if not self.refNasionNode:
                slicer.util.warningDisplay("Reference Nasion point not found. Please download it first.")
                return

            n_coord = self.refNasionNode.GetNthControlPointPosition(0)
            if slicer.util.getNode("MoveToOrigin"): slicer.mrmlScene.RemoveNode(slicer.util.getNode("MoveToOrigin"))
            
            self.transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode", "MoveToOrigin")
            matrix = vtk.vtkMatrix4x4()
            matrix.SetElement(0, 3, -n_coord[0])
            matrix.SetElement(1, 3, -n_coord[1])
            matrix.SetElement(2, 3, -n_coord[2])
            self.transformNode.SetMatrixTransformToParent(matrix)
            
            for node_name in ["Thitiorul_hard_tissue", "true_Thitiorul_soft_tissue"]:
                try:
                    node = slicer.util.getNode(node_name)
                    if self.show_yes_no_popup(f"Existing '{node_name}' found!", "Apply transform to these landmarks?"):
                        node.SetAndObserveTransformNodeID(self.transformNode.GetID())
                        slicer.vtkSlicerTransformLogic().hardenTransform(node)
                except: pass
            
            for vol_node in slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode"):
                if self.show_yes_no_popup("Apply Transform to Volume?", f"Apply transform to volume node '{vol_node.GetName()}'?"):
                    vol_node.SetAndObserveTransformNodeID(self.transformNode.GetID())
            
            self.refNasionNode.GetDisplayNode().SetVisibility(False)
            self.setGuiState(True)
            slicer.util.infoDisplay("Transform applied! Other steps are now unlocked.")
        except Exception as e:
            slicer.util.errorDisplay(f"Could not apply transform: {e}")
    
    def onCreateHardGuideLinesClicked(self):
        node = self.hardTissueSelector.currentNode()
        if not node: slicer.util.warningDisplay("Please load or select hard tissue landmarks first!"); return
        self.create_line_by_name('for_nr', node, "n", "rhi")
        self.create_line_by_name('for_ss', node, "a", "pr")
        slicer.util.showStatusMessage("Hard tissue guide lines created!", 2000)
    
    def onCreateSoftGuideLinesClicked(self):
        node = self.softTissueSelector.currentNode()
        if not node: slicer.util.warningDisplay("Please load or select soft tissue landmarks first!"); return
        self.create_line_by_name('for_npp_and_npa', node, "n'", "pn'")
        self.create_line_by_name('for_nd', node, "pn'", "sn'")
        slicer.util.showStatusMessage("Soft tissue guide lines created!", 2000)
    
    def create_line_by_name(self, name, node, label1, label2):
        if slicer.util.getNode(name): slicer.mrmlScene.RemoveNode(slicer.util.getNode(name))
        p1_idx, p2_idx = self.findLandmarkByName(node, label1), self.findLandmarkByName(node, label2)
        if p1_idx != -1 and p2_idx != -1:
            line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
            line.AddControlPoint(node.GetNthControlPointPosition(p1_idx))
            line.AddControlPoint(node.GetNthControlPointPosition(p2_idx))
            line.GetDisplayNode().SetColor(0.0, 1.0, 0.0)
    
    def onVisualizeAxesClicked(self):
        try:
            if not all([self.mspPlaneNode, self.xzPlaneNode, self.hardTissueNode]):
                slicer.util.warningDisplay("Create planes first!"); return
            n_idx = self.findLandmarkByName(self.hardTissueNode, "n")
            if n_idx == -1: slicer.util.warningDisplay("Nasion 'n' not found!"); return
            
            n_coord = self.hardTissueNode.GetNthControlPointPosition(n_idx)
            y_axis, z_axis = np.array(self.mspPlaneNode.GetNormal()), np.array(self.xzPlaneNode.GetNormal())
            x_axis = np.cross(y_axis, z_axis)
            
            for axis_name, vector, color in [('X_axis', x_axis, [1,0,0]), ('Y_axis', y_axis, [0,1,0]), ('Z_axis', z_axis, [0,0,1])]:
                if slicer.util.getNode(axis_name): slicer.mrmlScene.RemoveNode(slicer.util.getNode(axis_name))
                axis_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', axis_name)
                axis_node.AddControlPoint(n_coord)
                axis_node.AddControlPoint(n_coord + vector / np.linalg.norm(vector) * 100)
                axis_node.GetDisplayNode().SetSelectedColor(color)
            slicer.util.showStatusMessage("Axes visualized!", 2000)
        except Exception as e: slicer.util.errorDisplay(f"Error visualizing axes: {e}")

    def onPredictClicked(self):
        method_id = self.predictionMethodGroup.checkedId()
        method_name = {1: "mirror", 2: "replace", 3: "side"}[method_id]
        
        if method_name in self.prediction_runs and not self.show_yes_no_popup("Overwrite?", f"Prediction '{method_name}' already exists. Overwrite?"):
            return
        
        self.hardTissueNode = self.hardTissueSelector.currentNode()
        if not self.hardTissueNode: slicer.util.warningDisplay("Load hard tissue landmarks first!"); return
        
        outputName = f"Predicted_Thitiorul_{method_name}"
        color = self.prediction_runs.get(method_name, {}).get('color', self.colors[len(self.prediction_runs) % len(self.colors)])
        
        prediction_node = self.runSoftTissueRegression(self.hardTissueNode, outputName, method_id, color)
        if prediction_node:
            self.prediction_runs[method_name] = {'node_id': prediction_node.GetID(), 'color': color}
            slicer.util.infoDisplay(f"Prediction '{method_name}' complete.")

    def runSoftTissueRegression(self, hardTissueNode, outputName, mode_id, color):
        try:
            get = lambda label, opposite=None: self.get_point_by_label(hardTissueNode, label, opposite, mode_id)
            ss, nr, pr, iof_L, ecm_L, zy_L = get("ss"), get("nr"), get("pr"), get("iof_L"), get("ecm_L"), get("zy_L")
            iof_R, ecm_R, zy_R = (iof_L, ecm_L, zy_L) if mode_id == 1 else (get("iof_R", "iof_L"), get("ecm_R", "ecm_L"), get("zy_R", "zy_L"))

            ss_y, ss_z = ss[1], abs(ss[2])
            nr_y, nr_z = nr[1], abs(nr[2])
            pr_y, pr_z = pr[1], abs(pr[2])
            iof_L_x, iof_L_y = abs(iof_L[0]), iof_L[1]
            ecm_L_y, ecm_L_z = ecm_L[1], abs(ecm_L[2])
            zy_L_x, zy_L_y, zy_L_z = abs(zy_L[0]), zy_L[1], abs(zy_L[2])
            iof_R_x, iof_R_y = abs(iof_R[0]), iof_R[1]

            se_y = -0.869 + 0.212*ss_y + 0.139*zy_L_z - 0.073*ecm_L_y; se_z = -1.198 - 1.159*nr_y + 0.691*nr_z - 0.208*iof_L_y
            npp_y = 3.182 + 0.271*ss_y + 0.423*nr_y - 0.098*ecm_L_y; npp_z = 5.345 - 0.607*nr_y + 0.840*nr_z
            npa_y = 0.587 + 0.739*ss_y + 0.109*pr_z + 0.242*zy_L_x; npa_z = 4.315 - 0.371*ss_y + 0.573*ss_z + 0.285*nr_z
            pn_y = -2.091 + 0.818*ss_y + 0.152*pr_z + 0.251*zy_L_x; pn_z = 2.095 - 0.288*ss_y + 0.456*ss_z + 0.250*pr_z
            nd_y = -2.040 + 0.865*ss_y + 0.120*pr_z + 0.241*zy_L_x; nd_z = 3.626 - 0.392*ss_y + 0.842*ss_z
            sn_y = -1.902 + 0.676*ss_y + 0.260*pr_y + 0.198*zy_L_x; sn_z = 6.455 - 0.269*ss_y + 0.551*ss_z + 0.277*pr_z
            
            alL_x = -(7.101+0.107*pr_y+0.316*iof_L_x-0.076*zy_L_y); alL_y=2.427-0.320*nr_z+0.733*ss_y+0.129*pr_z; alL_z=2.897-0.218*ss_y+0.464*ss_z+0.305*pr_z
            alsL_x=-(3.167+0.174*iof_L_x+0.097*zy_L_x); alsL_y=3.993+0.453*ss_y+0.270*pr_y+0.072*pr_z; alsL_z=3.827-0.466*ss_y+0.674*ss_z+0.257*iof_L_y
            alpL_x=-(7.885+0.060*pr_z+0.310*iof_L_x); alpL_y=4.199+0.398*ss_y+0.224*pr_y+0.247*iof_L_y; alpL_z=2.054-0.419*ss_y+0.433*ss_z+0.332*pr_z
            aliL_x=-(4.611+0.239*iof_L_x-0.070*zy_L_y); aliL_y=-0.890+0.476*pr_y+0.377*ss_y+0.089*zy_L_x; aliL_z=0.404+0.499*ss_y+0.312*pr_z-0.119*zy_L_y

            if mode_id == 1: # Mirror Mode
                alR_x,alR_y,alR_z, alsR_x,alsR_y,alsR_z, alpR_x,alpR_y,alpR_z, aliR_x,aliR_y,aliR_z = -alL_x,alL_y,alL_z, -alsL_x,alsL_y,alsL_z, -alpL_x,alpL_y,alpL_z, -aliL_x,aliL_y,aliL_z
            else: # Side-specific / Replace
                ecm_R_z, zy_R_y = abs(ecm_R[2]), zy_R[1]
                alR_x=8.967+0.125*pr_y+0.249*iof_R_x-0.079*zy_R_y; alR_y=0.338-0.264*nr_z+0.760*ss_y+0.151*pr_z; alR_z=2.778-0.223*ss_y+0.437*ss_z+0.325*pr_z
                alsR_x=3.244+0.225*iof_R_x+0.079*zy_L_x; alsR_y=-1.183+0.628*pr_y+0.151*ecm_R_z; alsR_z=3.864-0.499*ss_y+0.685*ss_z+0.350*iof_R_y
                alpR_x=12.069+0.045*pr_z+0.207*iof_R_x; alpR_y=6.126+0.626*ss_y+0.323*iof_R_y; alpR_z=2.578-0.404*ss_y+0.403*ss_z+0.350*pr_z
                aliR_x=6.729+0.100*pr_y+0.165*iof_R_x-0.062*zy_R_y; aliR_y=-2.325+0.504*pr_y+0.345*ss_y+0.112*zy_L_x; aliR_z=6.363-0.161*ss_y+0.468*ss_z+0.350*pr_z

            if slicer.util.getNode(outputName): slicer.mrmlScene.RemoveNode(slicer.util.getNode(outputName))
            result_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", outputName)
            landmarks = [("se'",[0,se_y,se_z]),("npp'",[0,npp_y,npp_z]),("npa'",[0,npa_y,npa_z]),("pn'",[0,pn_y,pn_z]),("nd'",[0,nd_y,nd_z]),("sn'",[0,sn_y,sn_z]),
                         ("al'L",[alL_x,alL_y,alL_z]),("als'L",[alsL_x,alsL_y,alsL_z]),("alp'L",[alpL_x,alpL_y,alpL_z]),("ali'L",[aliL_x,aliL_y,aliL_z]),
                         ("al'R",[alR_x,alR_y,alR_z]),("als'R",[alsR_x,alsR_y,alsR_z]),("alp'R",[alpR_x,alpR_y,alpR_z]),("ali'R",[aliR_x,aliR_y,aliR_z])]
            for i, (label, coords) in enumerate(landmarks):
                result_node.AddControlPoint([coords[0], coords[1], -coords[2]])
                result_node.SetNthControlPointLabel(i, label)
            result_node.GetDisplayNode().SetSelectedColor(*color)
            return result_node
        except ValueError as e:
            slicer.util.errorDisplay(f"Missing landmark for prediction: {e}")
            return None

    def onCalculateAllErrors(self):
        self.softTissueNode = self.softTissueSelector.currentNode()
        if not self.softTissueNode: slicer.util.warningDisplay("Load true soft tissue landmarks to calculate errors."); return

        self.resultsTable.setColumnCount(1 + len(self.prediction_runs))
        self.resultsTable.setHorizontalHeaderLabels(["Landmark"] + [f"Error ({name})" for name in self.prediction_runs.keys()])
        true_dict = {self.softTissueNode.GetNthControlPointLabel(i): np.array(self.softTissueNode.GetNthControlPointPosition(i)) for i in range(self.softTissueNode.GetNumberOfControlPoints())}
        
        for node in slicer.util.getNodesByClass('vtkMRMLMarkupsLineNode'):
            if "error_line" in node.GetName(): slicer.mrmlScene.RemoveNode(node)

        for col_idx, (method_name, run_data) in enumerate(self.prediction_runs.items()):
            pred_node = slicer.mrmlScene.GetNodeByID(run_data['node_id'])
            if not pred_node: continue
            pred_dict = {pred_node.GetNthControlPointLabel(i): np.array(pred_node.GetNthControlPointPosition(i)) for i in range(pred_node.GetNumberOfControlPoints())}
            
            for row_idx in range(self.resultsTable.rowCount):
                landmark = self.resultsTable.item(row_idx, 0).text()
                item = qt.QTableWidgetItem("N/A")
                if landmark in pred_dict and landmark in true_dict:
                    error = np.linalg.norm(pred_dict[landmark] - true_dict[landmark])
                    item = qt.QTableWidgetItem(f"{error:.2f}")
                    line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", f"error_line_{method_name}_{landmark}")
                    line.AddControlPoint(pred_dict[landmark]); line.AddControlPoint(true_dict[landmark])
                    line.GetDisplayNode().SetSelectedColor(*run_data['color']); line.GetDisplayNode().SetGlyphScale(0); line.GetDisplayNode().SetLineThickness(0.5)
                self.resultsTable.setItem(row_idx, col_idx + 1, item)

    def onClearAll(self, confirm=True):
        if confirm and not self.show_yes_no_popup("Confirm Clear", "Clear all predictions, error lines, and results?"): return
        for run_data in self.prediction_runs.values():
            if slicer.mrmlScene.GetNodeByID(run_data['node_id']): slicer.mrmlScene.RemoveNode(slicer.mrmlScene.GetNodeByID(run_data['node_id']))
        for node in [n for n in slicer.util.getNodesByClass('vtkMRMLMarkupsLineNode') if any(x in n.GetName() for x in ["error_line", "_axis", "for_"])]:
            slicer.mrmlScene.RemoveNode(node)
        self.prediction_runs.clear()
        self.resultsTable.setColumnCount(1)
        self.resultsTable.setHorizontalHeaderLabels(["Landmark"])
        for i in range(self.resultsTable.rowCount): self.resultsTable.setItem(i, 1, None)
    
    def onShowDetailedResultsClicked(self):
        self.detailedWidget = qt.QDialog(self.mainWidget)
        self.detailedWidget.setWindowTitle("Detailed Prediction Results")
        self.detailedWidget.setMinimumSize(1200, 700)
        layout = qt.QVBoxLayout(self.detailedWidget)
        table = qt.QTableWidget()
        
        headers = ["Method", "Landmark", "Pred X", "Pred Y", "Pred Z", "True X", "True Y", "True Z", "Error (mm)", "Error Direction", "Equation"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        if not self.softTissueSelector.currentNode():
            slicer.util.warningDisplay("Please select true soft tissue to show detailed results.")
            return

        formulas = {
            "se'": ["y = -0.869+0.212*ss_y+0.139*zy_L_z-0.073*ecm_L_y", "z = -1.198-1.159*nr_y+0.691*nr_z-0.208*iof_L_y"],
            "npp'": ["y = 3.182+0.271*ss_y+0.423*nr_y-0.098*ecm_L_y", "z = 5.345-0.607*nr_y+0.840*nr_z"],
            "npa'": ["y = 0.587+0.739*ss_y+0.109*pr_z+0.242*zy_L_x", "z = 4.315-0.371*ss_y+0.573*ss_z+0.285*nr_z"],
            "pn'": ["y = -2.091+0.818*ss_y+0.152*pr_z+0.251*zy_L_x", "z = 2.095-0.288*ss_y+0.456*ss_z+0.250*pr_z"],
            "nd'": ["y = -2.040+0.865*ss_y+0.120*pr_z+0.241*zy_L_x", "z = 3.626-0.392*ss_y+0.842*ss_z"],
            "sn'": ["y = -1.902+0.676*ss_y+0.260*pr_y+0.198*zy_L_x", "z = 6.455-0.269*ss_y+0.551*ss_z+0.277*pr_z"],
            "al'L": ["x=-(7.101+0.107*pr_y+0.316*iof_L_x-0.076*zy_L_y)","y=2.427-0.320*nr_z+0.733*ss_y+0.129*pr_z","z=2.897-0.218*ss_y+0.464*ss_z+0.305*pr_z"],
            "als'L": ["x=-(3.167+0.174*iof_L_x+0.097*zy_L_x)","y=3.993+0.453*ss_y+0.270*pr_y+0.072*pr_z","z=3.827-0.466*ss_y+0.674*ss_z+0.257*iof_L_y"],
            "alp'L": ["x=-(7.885+0.060*pr_z+0.310*iof_L_x)","y=4.199+0.398*ss_y+0.224*pr_y+0.247*iof_L_y","z=2.054-0.419*ss_y+0.433*ss_z+0.332*pr_z"],
            "ali'L": ["x=-(4.611+0.239*iof_L_x-0.070*zy_L_y)","y=-0.890+0.476*pr_y+0.377*ss_y+0.089*zy_L_x","z=0.404+0.499*ss_y+0.312*pr_z-0.119*zy_L_y"],
            "al'R": ["x=8.967+0.125*pr_y+0.249*iof_R_x-0.079*zy_R_y","y=0.338-0.264*nr_z+0.760*ss_y+0.151*pr_z","z=2.778-0.223*ss_y+0.437*ss_z+0.325*pr_z"],
            "als'R": ["x=3.244+0.225*iof_R_x+0.079*zy_L_x","y=-1.183+0.628*pr_y+0.151*ecm_R_z","z=3.864-0.499*ss_y+0.685*ss_z+0.350*iof_R_y"],
            "alp'R": ["x=12.069+0.045*pr_z+0.207*iof_R_x","y=6.126+0.626*ss_y+0.323*iof_R_y","z=2.578-0.404*ss_y+0.403*ss_z+0.350*pr_z"],
            "ali'R": ["x=6.729+0.100*pr_y+0.165*iof_R_x-0.062*zy_R_y","y=-2.325+0.504*pr_y+0.345*ss_y+0.112*zy_L_x","z=6.363-0.161*ss_y+0.468*ss_z+0.350*pr_z"]
        }
        
        true_dict = {self.softTissueSelector.currentNode().GetNthControlPointLabel(i): np.array(self.softTissueSelector.currentNode().GetNthControlPointPosition(i)) for i in range(self.softTissueSelector.currentNode().GetNumberOfControlPoints())}
        
        valid_row_count = sum(1 for run_data in self.prediction_runs.values() if slicer.mrmlScene.GetNodeByID(run_data['node_id']) for i in range(slicer.mrmlScene.GetNodeByID(run_data['node_id']).GetNumberOfControlPoints()) if slicer.mrmlScene.GetNodeByID(run_data['node_id']).GetNthControlPointLabel(i) in true_dict)
        table.setRowCount(valid_row_count)
        
        current_row = 0
        for method_name, run_data in self.prediction_runs.items():
            pred_node = slicer.mrmlScene.GetNodeByID(run_data['node_id'])
            if not pred_node: continue
            
            for i in range(pred_node.GetNumberOfControlPoints()):
                landmark = pred_node.GetNthControlPointLabel(i)
                if landmark not in true_dict: continue
                
                table.setItem(current_row, 0, qt.QTableWidgetItem(method_name))
                table.setItem(current_row, 1, qt.QTableWidgetItem(landmark))
                
                pred_pos = np.array(pred_node.GetNthControlPointPosition(i))
                true_pos = true_dict[landmark]
                error = np.linalg.norm(pred_pos - true_pos)
                
                for j, val in enumerate(list(pred_pos) + list(true_pos) + [error]): table.setItem(current_row, 2+j, qt.QTableWidgetItem(f"{val:.2f}"))
                table.setItem(current_row, 9, qt.QTableWidgetItem(self.get_error_direction_string(true_pos - pred_pos)))
                
                equation_str = "Not predicted"
                if method_name == "mirror" and "'R" in landmark:
                    equation_str = "Mirror from LEFT:\n" + "\n".join(formulas.get(landmark.replace("'R", "'L"), ["N/A"]))
                else:
                    equation_str = "\n".join(formulas.get(landmark, ["Not predicted"]))
                table.setItem(current_row, 10, qt.QTableWidgetItem(equation_str))
                current_row += 1

        table.resizeColumnsToContents(); table.resizeRowsToContents()
        layout.addWidget(table)

        explanationLabel = qt.QLabel(f"<b>Note:</b> The 'Error Direction' column uses a tolerance of <b>{self.error_tolerance} mm</b>. A prediction is 'Spot on' if the error for each coordinate (X, Y, Z) is less than this value.")
        explanationLabel.setWordWrap(True); explanationLabel.setStyleSheet("font-style: italic; margin-top: 10px;")
        layout.addWidget(explanationLabel)
        
        copy_button = qt.QPushButton("Copy Table to Clipboard")
        copy_button.clicked.connect(lambda: self.onCopyToClipboard(table))
        layout.addWidget(copy_button)
        
        self.detailedWidget.show()

    def get_error_direction_string(self, error_vector):
        x_err, y_err, z_err = error_vector
        tol = self.error_tolerance
        x_dir = "Overestimated X" if x_err < -tol else "Underestimated X" if x_err > tol else ""
        y_dir = "Overestimated Y" if y_err < -tol else "Underestimated Y" if y_err > tol else ""
        z_dir = "Overestimated Z" if z_err < -tol else "Underestimated Z" if z_err > tol else ""
        directions = [d for d in [x_dir, y_dir, z_dir] if d]
        return ", ".join(directions) if directions else "Spot on"

    def onSaveToCSV(self):
        result = qt.QFileDialog.getSaveFileName(self.mainWidget, "Save Summary", "thitiorul_summary.csv", "CSV Files (*.csv)")
        fileName = result[0] if isinstance(result, tuple) else result
        if not fileName: return
        self.onCopyToClipboard(self.resultsTable)
        try:
            with open(fileName, 'w') as f: f.write(qt.QApplication.clipboard().text())
            slicer.util.infoDisplay(f"Summary table saved to {fileName}")
        except Exception as e: slicer.util.errorDisplay(f"Could not save file: {e}")

    def show_popup(self, title, text):
        msgBox = qt.QMessageBox(self.mainWidget); msgBox.setWindowFlags(msgBox.windowFlags()|qt.Qt.WindowStaysOnTopHint)
        msgBox.setWindowTitle(title); msgBox.setText(text); msgBox.setIcon(qt.QMessageBox.Information); msgBox.setStandardButtons(qt.QMessageBox.Ok); msgBox.exec_()

    def show_yes_no_popup(self, title, text):
        return qt.QMessageBox.question(self.mainWidget, title, text, qt.QMessageBox.Yes | qt.QMessageBox.No) == qt.QMessageBox.Yes
        
    def findLandmarkByName(self, node, label):
        for i in range(node.GetNumberOfControlPoints()):
            if node.GetNthControlPointLabel(i) == label: return i
        return -1
        
    def get_point_by_label(self, node, label, use_opposite=None, mode_id=1):
        idx = self.findLandmarkByName(node, label)
        if idx != -1: return node.GetNthControlPointPosition(idx)
        if (mode_id == 2 or mode_id == 3) and use_opposite: # Only allow replace for specific modes
            idx_opp = self.findLandmarkByName(node, use_opposite)
            if idx_opp != -1: return node.GetNthControlPointPosition(idx_opp)
        raise ValueError(f"Landmark '{label}' not found.")

    def onCreatePlanesClicked(self):
        self.hardTissueNode = self.hardTissueSelector.currentNode()
        if not self.hardTissueNode: slicer.util.warningDisplay("Load hard tissue landmarks first!"); return
        midline_labels = ["n", "a", "pr", "ss", "rhi"]
        indices = [self.findLandmarkByName(self.hardTissueNode, name) for name in midline_labels]
        if -1 in indices: slicer.util.warningDisplay(f"Cannot create plane. Missing one of: {', '.join(midline_labels)}"); return
        
        points = np.array([self.hardTissueNode.GetNthControlPointPosition(i) for i in indices])
        centroid, _, Vt = np.mean(points, axis=0), *np.linalg.svd(points - np.mean(points, axis=0))
        self.mspPlaneNode = self.create_plane('MSP', centroid, Vt[2, :])
        self.xzPlaneNode = self.create_plane('X-Z plane', self.hardTissueNode.GetNthControlPointPosition(indices[0]), np.cross(Vt[2, :], [0, 0, 1]))
        slicer.util.showStatusMessage("Planes created!", 2000)

    def create_plane(self, name, origin, normal):
        if slicer.util.getNode(name): slicer.mrmlScene.RemoveNode(slicer.util.getNode(name))
        plane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', name)
        plane.SetOrigin(origin); plane.SetNormal(normal)
        return plane

try:
    if 'gui' in globals() and isinstance(globals().get('gui'), ThitiorulGUI):
        globals()['gui'].mainWidget.close()
    gui = ThitiorulGUI()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Failed to create GUI: {e}")

```
