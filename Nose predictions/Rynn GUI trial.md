```python

# =============================================================================

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import json

# --- Main GUI Class ---
class RynnMethodGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Rynn (2010) Method"); self.setObjectName("RynnMethodGUI")
        self.mainLayout = qt.QVBoxLayout(self); self.mainLayout.setSpacing(10)
        self.stepStack = qt.QStackedWidget(); self.mainLayout.addWidget(self.stepStack)
        self.activeProfilePlaneName = "INB" 
        self.createAllStepWidgets()
        self.setupNavigation()
        self.currentStep = 0; self.updateStepUI()

    def createAllStepWidgets(self):
        self.createStep1_Welcome()
        self.createStep2_LandmarkSetup()
        self.createStep3_PlaneSetup()
        self.createStep4_Scaffolding()
        self.createStep5_PronasaleAnterior()
        self.createStep6_PronasaleVertical()
        self.createStep7_pFHP()
        self.createStep8_SoftTissueSN()
        self.createStep9_NasionPrediction()

    def setupNavigation(self):
        navWidget = qt.QWidget(); navLayout = qt.QHBoxLayout(navWidget); navLayout.setContentsMargins(0, 0, 0, 0)
        self.prevButton = qt.QPushButton("Previous"); self.prevButton.clicked.connect(self.onPrevButtonClicked)
        self.stepLabel = qt.QLabel(f"Step 1/{self.stepStack.count}")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter); self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.nextButton = qt.QPushButton("Next"); self.nextButton.clicked.connect(self.onNextButtonClicked)
        navLayout.addWidget(self.prevButton); navLayout.addStretch(1); navLayout.addWidget(self.stepLabel); navLayout.addStretch(1); navLayout.addWidget(self.nextButton)
        self.mainLayout.addWidget(navWidget)

    # --- Step UI Creation (with tables) ---
    def createStep1_Welcome(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15); title = qt.QLabel("Welcome to the Rynn (2010) Method GUI"); title.setStyleSheet("font-weight: bold; font-size: 18px;"); title.setAlignment(qt.Qt.AlignCenter); layout.addWidget(title)
        desc = qt.QLabel("This tool provides a guided workflow for the Rynn nasal prediction method.\n\nClick 'Next' to begin."); desc.setWordWrap(True); desc.setAlignment(qt.Qt.AlignCenter); layout.addWidget(desc); layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep2_LandmarkSetup(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15); title = qt.QLabel("Step 2: Load and Place Landmarks"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        self.downloadHardButton = qt.QPushButton("1. Download Hard Tissue Landmarks"); self.downloadHardButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;"); self.downloadHardButton.clicked.connect(self.onDownloadHardLandmarks); layout.addWidget(self.downloadHardButton)
        noteLabel = qt.QLabel(); noteLabel.setTextFormat(qt.Qt.RichText); noteLabel.setWordWrap(True); noteLabel.setText("<b>2. Place the required hard tissue landmarks on your model.</b>"); layout.addWidget(noteLabel)
        self.landmarkTable = qt.QTableWidget(7, 1); self.landmarkTable.setHorizontalHeaderLabels(["Required Hard Tissue Landmarks"]); landmarks = ["nasion", "inion (if visible)", "bregma (if visible)", "prosthion", "subspinale", "rhinion", "acanthion"]
        for i, landmark in enumerate(landmarks): self.landmarkTable.setItem(i, 0, qt.QTableWidgetItem(landmark))
        self.landmarkTable.horizontalHeader().setStretchLastSection(True); self.landmarkTable.verticalHeader().setVisible(False); self.landmarkTable.setEditTriggers(qt.QAbstractItemView.NoEditTriggers); self.landmarkTable.setFixedHeight(self.landmarkTable.verticalHeader().defaultSectionSize * self.landmarkTable.rowCount + self.landmarkTable.horizontalHeader().height); layout.addWidget(self.landmarkTable)
        selectorLayout = qt.QFormLayout(); self.landmarksSelector = slicer.qMRMLNodeComboBox(); self.landmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]; self.landmarksSelector.setMRMLScene(slicer.mrmlScene); self.landmarksSelector.addEnabled = True; self.landmarksSelector.removeEnabled = False; self.landmarksSelector.noneEnabled = True; selectorLayout.addRow("<b>3. Select Landmark Node:</b>", self.landmarksSelector); layout.addLayout(selectorLayout)
        self.step2StatusLabel = qt.QLabel("Status: Waiting for user."); self.step2StatusLabel.setWordWrap(True); layout.addWidget(self.step2StatusLabel); layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep3_PlaneSetup(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15); title = qt.QLabel("Step 3: Create Reference Planes"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        desc = qt.QLabel("Choose a method to define the primary profile plane (INB or MSP)."); desc.setWordWrap(True); layout.addWidget(desc)
        planeChoiceLayout = qt.QFormLayout(); self.planeChoiceComboBox = qt.QComboBox(); self.planeChoiceComboBox.addItems(["Select a method...", "INB (Inion-Nasion-Bregma)", "MSP (Midsagittal Best-Fit)"]); planeChoiceLayout.addRow("Profile Plane Method:", self.planeChoiceComboBox); layout.addLayout(planeChoiceLayout)
        self.createPlanesButton = qt.QPushButton("Create All Reference Planes"); self.createPlanesButton.clicked.connect(self.onCreatePlanes); layout.addWidget(self.createPlanesButton)
        self.step3StatusLabel = qt.QLabel("Status: Please choose a plane creation method."); self.step3StatusLabel.setWordWrap(True); layout.addWidget(self.step3StatusLabel); layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep4_Scaffolding(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15); title = qt.QLabel("Step 4: Create Geometric Scaffolding"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        axesGroup = qt.QGroupBox("1. Coordinate Axes"); axesLayout = qt.QVBoxLayout(axesGroup); self.createAxesButton = qt.QPushButton("Create X, Y, Z Axes"); self.createAxesButton.clicked.connect(self.onCreateAxes); axesLayout.addWidget(self.createAxesButton); layout.addWidget(axesGroup)
        networkGroup = qt.QGroupBox("2. Reference Network"); networkLayout = qt.QVBoxLayout(networkGroup); self.createNetworkButton = qt.QPushButton("Create Network Lines 1, 2, 3"); self.createNetworkButton.clicked.connect(self.onCreateNetwork); networkLayout.addWidget(self.createNetworkButton); layout.addWidget(networkGroup)
        self.step4StatusLabel = qt.QLabel("Status: Waiting for user."); self.step4StatusLabel.setWordWrap(True); layout.addWidget(self.step4StatusLabel); layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep5_PronasaleAnterior(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15); title = qt.QLabel("Step 5: Predict Pronasale Anterior (PA)"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        description_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%"><tr> <th>Literature</th> <th>Ancestry</th> <th>Biological Sex</th> <th>Full Equation</th> </tr><tr> <td>Rynn et al. 2010</td> <td>ANY</td> <td>All</td> <td>pred Rynn PA = 0.83 &times; Y &minus; 3.5</td> </tr><tr> <td>Sarilita et al. 2018</td> <td>Indonesian</td> <td>Males</td> <td>pred Sarilita M PA = 0.57 &times; Y + 2.33</td> </tr><tr> <td>Bulut et al. 2019</td> <td>Turkish</td> <td>Females</td> <td>pred Bulut F PA = 2.711 + 0.681 &times; Y</td> </tr><tr> <td>Bulut et al. 2019</td> <td>Turkish</td> <td>Males</td> <td>pred Bulut M PA = &minus;0.481 + 0.776 &times; Y</td> </tr></table>"""; layout.addWidget(qt.QLabel(description_html))
        self.pa_equations = ["pred Rynn PA", "pred Sarilita M PA", "pred Bulut F PA", "pred Bulut M PA"]; self.pa_checkbox_list = []
        for eq in self.pa_equations: checkbox = qt.QCheckBox(eq); layout.addWidget(checkbox); self.pa_checkbox_list.append(checkbox)
        calculate_button = qt.QPushButton("Calculate Pronasale Anterior"); calculate_button.clicked.connect(self.onCalculatePA); layout.addWidget(calculate_button)
        self.step5StatusLabel = qt.QLabel("Status: Waiting for user."); layout.addWidget(self.step5StatusLabel); layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep6_PronasaleVertical(self):
        widget = qt.QWidget(); self.step6_layout = qt.QVBoxLayout(widget); self.step6_layout.setSpacing(15); title = qt.QLabel("Step 6: Predict Pronasale Vertical (PV)"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); self.step6_layout.addWidget(title)
        self.step6_dynamic_content_widget = qt.QWidget(); self.step6_layout.addWidget(self.step6_dynamic_content_widget); self.step6_layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep7_pFHP(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15); title = qt.QLabel("Step 7: Predict pFHP"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        description_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%"><tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr><tr><td>Rynn et al. 2010</td><td>ANY</td><td>All</td><td>pred Rynn pFHP = 0.93 &times; Y &minus; 6</td></tr><tr><td>Sarilita et al. 2018</td><td>Indonesian</td><td>Males</td><td>pred Sarilita M pFHP = 0.58 &times; Y + 4.55</td></tr><tr><td>Bulut et al. 2019</td><td>Turkish</td><td>Females</td><td>pred Bulut F pFHP = 1.161 + 0.775 &times; Y</td></tr><tr><td>Bulut et al. 2019</td><td>Turkish</td><td>Males</td><td>pred Bulut M pFHP = 0.518 + 0.777 &times; Y</td></tr></table>"""; layout.addWidget(qt.QLabel(description_html))
        self.pfhp_equations = ["pred Rynn pFHP", "pred Sarilita M pFHP", "pred Bulut F pFHP", "pred Bulut M pFHP"]; self.pfhp_checkbox_list = []
        for eq in self.pfhp_equations: checkbox = qt.QCheckBox(eq); layout.addWidget(checkbox); self.pfhp_checkbox_list.append(checkbox)
        calculate_button = qt.QPushButton("Calculate pFHP"); calculate_button.clicked.connect(self.onCalculatePFHP); layout.addWidget(calculate_button)
        self.step7StatusLabel = qt.QLabel("Status: Waiting for user."); layout.addWidget(self.step7StatusLabel); layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep8_SoftTissueSN(self):
        widget = qt.QWidget(); self.step8_layout = qt.QVBoxLayout(widget); self.step8_layout.setSpacing(15); title = qt.QLabel("Step 8: Predict Soft Tissue sn (ND Intersection)"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); self.step8_layout.addWidget(title)
        self.step8_dynamic_content_widget = qt.QWidget(); self.step8_layout.addWidget(self.step8_dynamic_content_widget); self.step8_layout.addStretch(1); self.stepStack.addWidget(widget)
    def createStep9_NasionPrediction(self):
        widget = qt.QWidget(); self.step9_layout = qt.QVBoxLayout(widget); self.step9_layout.setSpacing(15); title = qt.QLabel("Step 9: Predict Nasion (n')"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); self.step9_layout.addWidget(title)
        self.step9_dynamic_content_widget = qt.QWidget(); self.step9_layout.addWidget(self.step9_dynamic_content_widget); self.step9_layout.addStretch(1); self.stepStack.addWidget(widget)

    # --- UI Refresh Methods ---
    def refreshStep6UI(self):
        if self.step6_dynamic_content_widget: self.step6_dynamic_content_widget.deleteLater()
        self.step6_dynamic_content_widget = qt.QWidget(); layout = qt.QVBoxLayout(self.step6_dynamic_content_widget)
        pa_group = qt.QGroupBox("1. Select PA Line(s) to Use"); pa_layout = qt.QVBoxLayout(pa_group)
        self.pv_pa_lines = [node for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") if node.GetName().endswith("PA")]; self.pv_pa_checkboxes = []
        if not self.pv_pa_lines: pa_layout.addWidget(qt.QLabel("No PA lines found. Please complete Step 5."))
        else:
            for node in self.pv_pa_lines: checkbox = qt.QCheckBox(node.GetName()); pa_layout.addWidget(checkbox); self.pv_pa_checkboxes.append(checkbox)
        layout.addWidget(pa_group)
        pv_group = qt.QGroupBox("2. Select PV Equation(s)"); pv_layout = qt.QVBoxLayout(pv_group)
        description_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%"><tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr><tr><td>Rynn et al. 2010</td><td>ANY</td><td>All</td><td>pred Rynn PV = 0.9 &times; X &minus; 2</td></tr><tr><td>Sarilita et al. 2018</td><td>Indonesian</td><td>Males</td><td>pred Sarilita M PV = 0.88 &times; X + 0.68</td></tr><tr><td>Bulut et al. 2019</td><td>Turkish</td><td>Females</td><td>pred Bulut F PV = 5.501 + 0.779 &times; X</td></tr><tr><td>Bulut et al. 2019</td><td>Turkish</td><td>Males</td><td>pred Bulut M PV = &minus;3.53 + 0.954 &times; X</td></tr></table>"""; pv_layout.addWidget(qt.QLabel(description_html))
        self.pv_equations = ["pred Rynn PV", "pred Sarilita M PV", "pred Bulut F PV", "pred Bulut M PV"]; self.pv_checkbox_list = []
        for eq in self.pv_equations: checkbox = qt.QCheckBox(eq); pv_layout.addWidget(checkbox); self.pv_checkbox_list.append(checkbox)
        layout.addWidget(pv_group)
        calculate_button = qt.QPushButton("Calculate Pronasale Vertical"); calculate_button.clicked.connect(self.onCalculatePV); layout.addWidget(calculate_button)
        self.step6StatusLabel = qt.QLabel("Status: Waiting for user."); layout.addWidget(self.step6StatusLabel)
        self.step6_layout.insertWidget(1, self.step6_dynamic_content_widget)
    def refreshStep8UI(self):
        if self.step8_dynamic_content_widget: self.step8_dynamic_content_widget.deleteLater()
        self.step8_dynamic_content_widget = qt.QWidget(); layout = qt.QVBoxLayout(self.step8_dynamic_content_widget)
        pred_node = slicer.util.getFirstNodeByName("Rynn_soft_tissue_pred"); self.sn_points_data = []
        if pred_node:
            for i in range(pred_node.GetNumberOfControlPoints()):
                label = pred_node.GetNthControlPointLabel(i)
                if label.endswith("_pronasale_pred"):
                    self.sn_points_data.append((label, i))
        group1 = qt.QGroupBox("1. Choose pronasale pred point"); l1 = qt.QVBoxLayout(group1)
        self.sn_point_buttons = qt.QButtonGroup(self)
        if not self.sn_points_data: l1.addWidget(qt.QLabel("No 'pronasale_pred' points found."))
        else:
            for i, (label, idx) in enumerate(self.sn_points_data): radio = qt.QRadioButton(label); l1.addWidget(radio); self.sn_point_buttons.addButton(radio, i)
        layout.addWidget(group1)
        group2 = qt.QGroupBox("2. Choose ND radius equation"); l2 = qt.QVBoxLayout(group2)
        table_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%"><tr><th>Lit.</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr><tr><td>Rynn</td><td>ANY</td><td>F</td><td>0.5*Y + 1.5</td></tr><tr><td>Rynn</td><td>ANY</td><td>M</td><td>0.4*Y + 5</td></tr><tr><td>Sarilita</td><td>Indo.</td><td>M</td><td>0.22*Z + 4.02</td></tr><tr><td>Sarilita</td><td>Indo.</td><td>F</td><td>0.29*Y + 6.24</td></tr><tr><td>Bulut</td><td>Turkish</td><td>F</td><td>5.169 + 0.423*Y</td></tr><tr><td>Bulut</td><td>Turkish</td><td>M</td><td>6.587 + 0.386*Y</td></tr></table>"""; l2.addWidget(qt.QLabel(table_html))
        self.sn_equations = ["pred Rynn F ND", "pred Rynn M ND", "pred Sarilita M ND", "pred Sarilita F ND", "pred Bulut F ND", "pred Bulut M ND"]; self.sn_equation_buttons = qt.QButtonGroup(self)
        for i, eq in enumerate(self.sn_equations): radio = qt.QRadioButton(eq); l2.addWidget(radio); self.sn_equation_buttons.addButton(radio, i)
        layout.addWidget(group2)
        group3 = qt.QGroupBox("3. Choose pFHP line to intersect with"); l3 = qt.QVBoxLayout(group3)
        self.sn_lines = [node for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") if "pFHP" in node.GetName()]
        self.sn_line_buttons = qt.QButtonGroup(self)
        if not self.sn_lines: l3.addWidget(qt.QLabel("No pFHP lines found."))
        else:
            for i, line in enumerate(self.sn_lines): radio = qt.QRadioButton(line.GetName()); l3.addWidget(radio); self.sn_line_buttons.addButton(radio, i)
        layout.addWidget(group3)
        calculate_button = qt.QPushButton("Create ND Circle and Find Intersection"); calculate_button.clicked.connect(self.onCalculateSN); layout.addWidget(calculate_button)
        self.step8StatusLabel = qt.QLabel("Status: Waiting for user."); layout.addWidget(self.step8StatusLabel)
        self.step8_layout.insertWidget(1, self.step8_dynamic_content_widget)
    def refreshStep9UI(self):
        if self.step9_dynamic_content_widget: self.step9_dynamic_content_widget.deleteLater()
        self.step9_dynamic_content_widget = qt.QWidget(); layout = qt.QVBoxLayout(self.step9_dynamic_content_widget)
        pred_node = slicer.util.getFirstNodeByName("Rynn_soft_tissue_pred")
        group1 = qt.QGroupBox("1. Choose NH circle center ('sn_pred')"); l1 = qt.QVBoxLayout(group1)
        self.nh_center_points_data = [(pred_node.GetNthControlPointLabel(i), i) for i in range(pred_node.GetNumberOfControlPoints()) if pred_node.GetNthControlPointLabel(i).endswith("_sn_pred")] if pred_node else []
        self.nh_center_buttons = qt.QButtonGroup(self)
        if not self.nh_center_points_data: l1.addWidget(qt.QLabel("No 'sn_pred' points found. Please complete Step 8."))
        else:
            for i, (label, idx) in enumerate(self.nh_center_points_data): radio = qt.QRadioButton(label); self.nh_center_buttons.addButton(radio, i); l1.addWidget(radio)
        layout.addWidget(group1)
        group2 = qt.QGroupBox("2. Choose NH equation"); l2 = qt.QVBoxLayout(group2)
        nh_table_html = """<table border="1" cellspacing="0" cellpadding="3"><tr><th>Lit.</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr><tr><td>Rynn</td><td>European</td><td>M</td><td>pred Rynn EA M NH = 0.78*Z + 9.5</td></tr><tr><td>Rynn</td><td>European</td><td>F</td><td>pred Rynn EA F NH = 0.63*Z + 17</td></tr><tr><td>Sarilita</td><td>Indonesian</td><td>M</td><td>pred Sarilita M NH = 0.79*Z + 3.74</td></tr><tr><td>Sarilita</td><td>Indonesian</td><td>F</td><td>pred Sarilita F NH = 0.69*X + 12.36</td></tr><tr><td>Bulut</td><td>Turkish</td><td>F</td><td>pred Bulut F NH = 15.047 + 0.687*Z</td></tr><tr><td>Bulut</td><td>Turkish</td><td>M</td><td>pred Bulut M NH = 9.858 + 0.784*Z</td></tr></table>"""; l2.addWidget(qt.QLabel(nh_table_html))
        self.nh_equations = ["pred Rynn EA M NH", "pred Rynn EA F NH", "pred Sarilita M NH", "pred Sarilita F NH", "pred Bulut F NH", "pred Bulut M NH"]; self.nh_eq_buttons = qt.QButtonGroup(self)
        for i, eq in enumerate(self.nh_equations): radio = qt.QRadioButton(eq); self.nh_eq_buttons.addButton(radio, i); l2.addWidget(radio)
        layout.addWidget(group2)
        group3 = qt.QGroupBox("3. Choose NL circle center ('pronasale_pred')"); l3 = qt.QVBoxLayout(group3)
        self.nl_center_points_data = [(pred_node.GetNthControlPointLabel(i), i) for i in range(pred_node.GetNumberOfControlPoints()) if pred_node.GetNthControlPointLabel(i).endswith("_pronasale_pred")] if pred_node else []
        self.nl_center_buttons = qt.QButtonGroup(self)
        if not self.nl_center_points_data: l3.addWidget(qt.QLabel("No 'pronasale_pred' points found."))
        else:
            for i, (label, idx) in enumerate(self.nl_center_points_data): radio = qt.QRadioButton(label); self.nl_center_buttons.addButton(radio, i); l3.addWidget(radio)
        layout.addWidget(group3)
        group4 = qt.QGroupBox("4. Choose NL equation"); l4 = qt.QVBoxLayout(group4)
        nl_table_html = """<table border="1" cellspacing="0" cellpadding="3"><tr><th>Lit.</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr><tr><td>Rynn</td><td>European</td><td>All</td><td>pred Rynn EA NL = 0.74*Z + 3.5</td></tr><tr><td>Bulut</td><td>Turkish</td><td>F</td><td>pred Sarilita F NL = 6.624 + 0.71*Z</td></tr><tr><td>Bulut</td><td>Turkish</td><td>M</td><td>pred Sarilita M NL = 0.764 + 0.807*Z</td></tr><tr><td>Sarilita</td><td>Indonesian</td><td>M</td><td>pred Bulut M NL = 0.66*X + 7.77</td></tr></table>"""; l4.addWidget(qt.QLabel(nl_table_html))
        self.nl_equations = ["pred Rynn EA NL", "pred Sarilita F NL", "pred Sarilita M NL", "pred Bulut M NL"]; self.nl_eq_buttons = qt.QButtonGroup(self)
        for i, eq in enumerate(self.nl_equations): radio = qt.QRadioButton(eq); self.nl_eq_buttons.addButton(radio, i); l4.addWidget(radio)
        layout.addWidget(group4)
        calculate_button = qt.QPushButton("Draw Circles and Predict n'"); calculate_button.clicked.connect(self.onCalculateNasion); layout.addWidget(calculate_button)
        self.step9StatusLabel = qt.QLabel("Status: Waiting for user."); layout.addWidget(self.step9StatusLabel)
        self.step9_layout.insertWidget(1, self.step9_dynamic_content_widget)

    # --- Navigation and UI Update ---
    def onPrevButtonClicked(self):
        if self.currentStep > 0: self.currentStep -= 1; self.updateStepUI()
    def onNextButtonClicked(self):
        if self.currentStep < self.stepStack.count - 1: self.currentStep += 1; self.updateStepUI()
    def updateStepUI(self):
        self.stepStack.setCurrentIndex(self.currentStep); self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0); self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)
        self.autoSelectRynnNode() # THIS IS THE FIX
        if self.currentStep == 5: self.refreshStep6UI()
        if self.currentStep == 7: self.refreshStep8UI()
        if self.currentStep == 8: self.refreshStep9UI()

    # --- Helper Functions ---
    def autoSelectRynnNode(self):
        # THIS IS THE FIX: The auto-select function is restored
        if self.landmarksSelector.currentNode() is None:
            nodes = slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode")
            for node in nodes:
                name = node.GetName().lower()
                if "rynn" in name and "hard" in name:
                    self.landmarksSelector.setCurrentNode(node)
                    self.step2StatusLabel.setText(f"Status: Automatically selected '{node.GetName()}'.")
                    break

    def get_landmark_positions(self, node, required_landmarks):
        positions = {};
        for i in range(node.GetNumberOfControlPoints()): positions[node.GetNthControlPointLabel(i).lower()] = np.array(node.GetNthControlPointPositionWorld(i))
        for name in required_landmarks:
            if name.lower().split(" ")[0] not in positions and "(if visible)" not in name: raise ValueError(f"Required landmark '{name}' not found.")
        return positions
    
    def create_point_list_circle(self, center, radius, plane_normal, name, color):
        collection = slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
        for i in range(collection.GetNumberOfItems()):
            node = collection.GetItemAsObject(i)
            if node.GetName() == name: slicer.mrmlScene.RemoveNode(node); break
        point_list_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", name)
        display_node = point_list_node.GetDisplayNode()
        if display_node:
            display_node.SetSelectedColor(color); display_node.SetColor(color)
            display_node.SetGlyphScale(1.5); display_node.SetTextScale(0.0)
        u = np.cross([0,0,1], plane_normal)
        if np.linalg.norm(u) < 1e-6: u = np.array([1,0,0])
        u /= np.linalg.norm(u); v = np.cross(plane_normal, u)
        for i in range(36):
            angle = i * np.pi / 18.0
            point_on_circle = center + radius * (np.cos(angle) * u + np.sin(angle) * v)
            point_list_node.AddControlPoint(point_on_circle)
        slicer.app.processEvents()

    # --- Calculation Logic ---
    def onDownloadHardLandmarks(self):
        self.step2StatusLabel.setText("Status: Downloading..."); url = "https://github.com/user-attachments/files/22989769/Rynn_hard_tissue.mrk.json"; nodeName = "Rynn_hard_tissue"
        try:
            with urllib.request.urlopen(url) as response:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile:
                    tempFile.write(response.read()); tempFilePath = tempFile.name
            loadedNode = slicer.util.loadMarkups(tempFilePath); os.remove(tempFilePath)
            if loadedNode: loadedNode.SetName(nodeName); self.landmarksSelector.setCurrentNode(loadedNode); self.step2StatusLabel.setText("Status: Landmarks loaded.")
            else: raise IOError("Failed to load landmarks.")
        except Exception as e: self.step2StatusLabel.setText(f"Status: Error! {e}")

    def onCreatePlanes(self):
        self.step3StatusLabel.setText("Status: Processing..."); slicer.app.processEvents()
        try:
            landmarksNode = self.landmarksSelector.currentNode();
            if not landmarksNode: raise ValueError("Please select landmark node.")
            choice_index = self.planeChoiceComboBox.currentIndex;
            if choice_index == 0: raise ValueError("Please select a plane creation method.")
            def create_plane(name, o, n, c):
                p = slicer.util.getFirstNodeByName(name) or slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', name)
                p.SetOrigin(o); p.SetNormal(n); p.SetSize(300,300); d = p.GetDisplayNode() or p.CreateDefaultDisplayNodes() and p.GetDisplayNode(); d.SetSelectedColor(c); return p
            if choice_index == 1:
                self.activeProfilePlaneName = "INB"; pos = self.get_landmark_positions(landmarksNode, ["inion", "nasion", "bregma"])
                v1=pos['nasion']-pos['inion']; v2=pos['bregma']-pos['inion']; n=np.cross(v1,v2)/np.linalg.norm(np.cross(v1,v2)); p_plane=create_plane('INB',pos['inion'],n,(1,0,0))
            elif choice_index == 2:
                self.activeProfilePlaneName = "MSP"; pos = self.get_landmark_positions(landmarksNode, ["nasion", "acanthion", "prosthion", "subspinale"])
                pts=np.array(list(pos.values())); cen=np.mean(pts,axis=0); cov=np.cov(pts-cen,rowvar=False); _,eigv=np.linalg.eigh(cov); n=eigv[:,np.argmin(_)]; p_plane=create_plane('MSP',cen,n,(1,0.5,0))
            pos_np = self.get_landmark_positions(landmarksNode, ["nasion", "prosthion"]); n_p=np.array(p_plane.GetNormal()); v_np=pos_np['nasion']-pos_np['prosthion']
            npp_n=np.cross(n_p,v_np)/np.linalg.norm(np.cross(n_p,v_np)); create_plane('NPP',pos_np['prosthion'],npp_n,(0,1,0))
            ptp_n=np.cross(n_p,npp_n)/np.linalg.norm(np.cross(n_p,npp_n)); create_plane('PTP',pos_np['nasion'],ptp_n,(0,0,1))
            self.step3StatusLabel.setText("Status: Planes created.")
        except Exception as e: self.step3StatusLabel.setText(f"Status: Error! {e}")

    def onCreateAxes(self):
        self.step4StatusLabel.setText("Status: Creating axes..."); slicer.app.processEvents()
        try:
            lm_node = self.landmarksSelector.currentNode();
            if not lm_node: raise ValueError("Landmark node not found.")
            def create_line(name, p1, p2, c):
                old = slicer.util.getFirstNodeByName(name);
                if old: slicer.mrmlScene.RemoveNode(old)
                ln=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode',name); ln.AddControlPoint(p1); ln.AddControlPoint(p2)
                # THIS IS THE FIX: Set the color correctly
                disp = ln.GetDisplayNode(); disp.SetColor(c); disp.SetSelectedColor(c)
            pos=self.get_landmark_positions(lm_node,["nasion","acanthion","rhinion","subspinale"])
            create_line('nas-aca X',pos['nasion'],pos['acanthion'],(1,0,0)) # Red
            create_line('rhi-subs Y',pos['rhinion'],pos['subspinale'],(0,1,0)) # Green
            create_line('nas-subs Z',pos['nasion'],pos['subspinale'],(0,0,1)) # Blue
            self.step4StatusLabel.setText("Status: Axes created.")
        except Exception as e: self.step4StatusLabel.setText(f"Status: Error! {e}")

    def onCreateNetwork(self):
        self.step4StatusLabel.setText("Status: Creating network..."); slicer.app.processEvents()
        try:
            lm_node = self.landmarksSelector.currentNode()
            if not lm_node:
                raise ValueError("Landmark node not found.")
            npp = slicer.util.getNode("NPP")
            ptp = slicer.util.getNode("PTP")
            if not all([npp, ptp]):
                raise ValueError("Required planes (NPP, PTP) not found.")
            def create_line(name, start, direction, color=(1,0.5,0)):
                old = slicer.util.getFirstNodeByName(name)
                if old:
                    slicer.mrmlScene.RemoveNode(old)
                ln = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
                # Ensure display node exists and set color
                if not ln.GetDisplayNode():
                    ln.CreateDefaultDisplayNodes()
                disp = ln.GetDisplayNode()
                disp.SetSelectedColor(color)
                disp.SetColor(color)
                dirv = np.array(direction, dtype=float)
                norm = np.linalg.norm(dirv)
                if norm < 1e-8:
                    raise ValueError(f"Direction for line '{name}' is zero-length")
                dirv /= norm
                start = np.array(start, dtype=float)
                ln.AddControlPoint((start - dirv * 100).tolist())
                ln.AddControlPoint((start + dirv * 100).tolist())

            # get landmarks we need
            pos = self.get_landmark_positions(lm_node, ["nasion", "subspinale"])
            nasion_pos = pos['nasion']
            subspinale_pos = pos['subspinale']

            npp_n = np.array(npp.GetNormal(), dtype=float)
            ptp_n = np.array(ptp.GetNormal(), dtype=float)

            # Prefer a dedicated FHP plane if present (older working versions used an FHP-derived direction)
            fhp = slicer.util.getNode("FHP")
            if fhp:
                fhp_n = np.array(fhp.GetNormal(), dtype=float)
                # choose a reference axis that's not parallel to fhp_n
                ref = np.array([1.0, 0.0, 0.0])
                if abs(np.dot(np.abs(fhp_n), np.abs(ref))) > 0.999:
                    ref = np.array([0.0, 1.0, 0.0])
                fhp_dir = np.cross(fhp_n, ref)
                if np.linalg.norm(fhp_dir) < 1e-8:
                    # fallback to cross(NPP, PTP)
                    fhp_dir = np.cross(npp_n, ptp_n)
            else:
                # fallback: direction defined by cross(NPP, PTP)
                fhp_dir = np.cross(npp_n, ptp_n)

            # normalize fallback direction
            if np.linalg.norm(fhp_dir) < 1e-8:
                raise ValueError("Computed direction for line 3 is too small (degenerate). Check planes.")
            fhp_dir = fhp_dir / np.linalg.norm(fhp_dir)

            # create lines (with explicit colours for axes)
            create_line("1", nasion_pos, npp_n, color=(1,0,0))        # X (red)
            create_line("2", nasion_pos, ptp_n, color=(0,1,0))        # Y (green)
            create_line("3", subspinale_pos, fhp_dir, color=(1,0.5,0))# network line 3 (orange)

            self.step4StatusLabel.setText("Status: Network lines created.")
        except Exception as e:
            self.step4StatusLabel.setText(f"Status: Error! {e}")

    def onCalculatePA(self):
        self.step5StatusLabel.setText("Status: Calculating..."); slicer.app.processEvents()
        chosen = [cb.text for cb in self.pa_checkbox_list if cb.isChecked()]
        if not chosen: self.step5StatusLabel.setText("Status: No equation selected!"); return
        try:
            y,l1,lm=slicer.util.getNode("rhi-subs Y"),slicer.util.getNode("1"),self.landmarksSelector.currentNode(); p1,p2=np.zeros(3),np.zeros(3)
            y.GetNthControlPointPositionWorld(0,p1); y.GetNthControlPointPositionWorld(1,p2); Y=np.linalg.norm(p2-p1)
            start=self.get_landmark_positions(lm,["nasion"])["nasion"]; l1.GetNthControlPointPositionWorld(0,p1); l1.GetNthControlPointPositionWorld(1,p2)
            direction=-(p2-p1)/np.linalg.norm(p2-p1)
            for eq in chosen:
                length={"pred Rynn PA":.83*Y-3.5,"pred Sarilita M PA":.57*Y+2.33,"pred Bulut F PA":2.711+.681*Y,"pred Bulut M PA":-.481+.776*Y}.get(eq)
                if length is None: continue
                old = slicer.util.getFirstNodeByName(eq);
                if old: slicer.mrmlScene.RemoveNode(old)
                ln=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode",eq); ln.AddControlPoint(start); ln.AddControlPoint(start+direction*length)
            self.step5StatusLabel.setText(f"Status: Created {len(chosen)} line(s).")
        except Exception as e: self.step5StatusLabel.setText(f"Status: Error! {e}")

    def onCalculatePV(self):
        self.step6StatusLabel.setText("Status: Calculating..."); slicer.app.processEvents()
        pa_cb_text = [cb.text for cb in self.pv_pa_checkboxes if cb.isChecked()]
        pv_eqs = [cb.text for cb in self.pv_checkbox_list if cb.isChecked()]
        if not pa_cb_text or not pv_eqs: self.step6StatusLabel.setText("Status: Please select at least one PA line and PV equation."); return
        try:
            x,l2=slicer.util.getNode("nas-aca X"),slicer.util.getNode("2"); p1,p2=np.zeros(3),np.zeros(3)
            x.GetNthControlPointPositionWorld(0,p1); x.GetNthControlPointPositionWorld(1,p2); X=np.linalg.norm(p2-p1)
            l2.GetNthControlPointPositionWorld(0,p1); l2.GetNthControlPointPositionWorld(1,p2); dir2=(p2-p1)/np.linalg.norm(p2-p1)
            if dir2[2] > 0: dir2 = -dir2
            pred_node=slicer.util.getFirstNodeByName("Rynn_soft_tissue_pred") or slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode","Rynn_soft_tissue_pred")
            for pa_name in pa_cb_text:
                pa_node = slicer.util.getNode(pa_name); pa_end=np.zeros(3); pa_node.GetNthControlPointPositionWorld(1,pa_end)
                for pv_eq in pv_eqs:
                    pv_len={"pred Rynn PV":.9*X-2,"pred Sarilita M PV":.88*X+.68,"pred Bulut F PV":5.501+.779*X,"pred Bulut M PV":-3.53+.954*X}.get(pv_eq)
                    if pv_len is None: continue
                    pa_abbrev = pa_name.replace("pred ", "").replace(" ", "")
                    pv_abbrev = pv_eq.replace("pred ", "").replace(" ", "")
                    final_label = f"{pa_abbrev}_{pv_abbrev}_pronasale_pred"
                    pred_node.AddControlPoint(pa_end+dir2*pv_len, final_label)
            self.step6StatusLabel.setText("Status: Points created.")
        except Exception as e: self.step6StatusLabel.setText(f"Status: Error! {e}")

    def onCalculatePFHP(self):
        self.step7StatusLabel.setText("Status: Calculating..."); slicer.app.processEvents()
        chosen = [cb.text for cb in self.pfhp_checkbox_list if cb.isChecked()]
        if not chosen: self.step7StatusLabel.setText("Status: No equation selected!"); return
        try:
            lm,l3,y=self.landmarksSelector.currentNode(),slicer.util.getNode("3"),slicer.util.getNode("rhi-subs Y")
            start=self.get_landmark_positions(lm,["subspinale"])["subspinale"]; p1,p2=np.zeros(3),np.zeros(3)
            l3.GetNthControlPointPositionWorld(0,p1); l3.GetNthControlPointPositionWorld(1,p2); direction=-(p2-p1)/np.linalg.norm(p2-p1)
            y.GetNthControlPointPositionWorld(0,p1); y.GetNthControlPointPositionWorld(1,p2); Y=np.linalg.norm(p2-p1)
            for eq in chosen:
                length={"pred Rynn pFHP":.93*Y-6,"pred Sarilita M pFHP":.58*Y+4.55,"pred Bulut F pFHP":1.161+.775*Y,"pred Bulut M pFHP":.518+.777*Y}.get(eq)
                if length is None: continue
                old = slicer.util.getFirstNodeByName(eq);
                if old: slicer.mrmlScene.RemoveNode(old)
                ln=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode",eq); ln.AddControlPoint(start); ln.AddControlPoint(start+direction*length)
            self.step7StatusLabel.setText(f"Status: Created {len(chosen)} line(s).")
        except Exception as e: self.step7StatusLabel.setText(f"Status: Error! {e}")

    def onCalculateSN(self):
        self.step8StatusLabel.setText("Status: Calculating..."); slicer.app.processEvents()
        center_choice_id = self.sn_point_buttons.checkedId(); eq_choice_id = self.sn_equation_buttons.checkedId(); line_choice_id = self.sn_line_buttons.checkedId()
        if -1 in [center_choice_id, eq_choice_id, line_choice_id]: self.step8StatusLabel.setText("Status: Please make a selection in all sections."); return
        try:
            label, center_idx = self.sn_points_data[center_choice_id]; equation = self.sn_equations[eq_choice_id]; line_node = self.sn_lines[line_choice_id]
            pred_node=slicer.util.getNode("Rynn_soft_tissue_pred"); center=np.zeros(3); pred_node.GetNthControlPointPositionWorld(center_idx,center); center_label=pred_node.GetNthControlPointLabel(center_idx)
            y,z,plane=slicer.util.getNode("rhi-subs Y"),slicer.util.getNode("nas-subs Z"),slicer.util.getNode(self.activeProfilePlaneName); p1,p2=np.zeros(3),np.zeros(3)
            y.GetNthControlPointPositionWorld(0,p1); y.GetNthControlPointPositionWorld(1,p2); y_len=np.linalg.norm(p2-p1); z_len=0
            if z: z.GetNthControlPointPositionWorld(0,p1); z.GetNthControlPointPositionWorld(1,p2); z_len=np.linalg.norm(p2-p1)
            radius={"pred Rynn F ND":.5*y_len+1.5,"pred Rynn M ND":.4*y_len+5,"pred Sarilita M ND":.22*z_len+4.02,"pred Sarilita F ND":.29*y_len+6.24,"pred Bulut F ND":5.169+.423*y_len,"pred Bulut M ND":6.587+.386*y_len}.get(equation)
            plane_n=np.array(plane.GetNormal()); self.create_point_list_circle(center,radius,plane_n,"ND_Circle_Points",(0.2,0.8,0.2))
            lp0,lp1=np.zeros(3),np.zeros(3); line_node.GetNthControlPointPositionWorld(0,lp0); line_node.GetNthControlPointPositionWorld(1,lp1)
            u=np.cross([0,0,1],plane_n); u/=np.linalg.norm(u); v=np.cross(plane_n,u)
            def to_plane(pt): return np.array([np.dot(pt-center,u),np.dot(pt-center,v)])
            p0_plane,p1_plane=to_plane(lp0),to_plane(lp1); dp=p1_plane-p0_plane; a=np.dot(dp,dp); b=2*np.dot(p0_plane,dp); c=np.dot(p0_plane,p0_plane)-radius**2; disc=b**2-4*a*c
            if disc<0: raise ValueError("No intersection.")
            final_pt=None
            for t in [(-b+np.sqrt(disc))/(2*a),(-b-np.sqrt(disc))/(2*a)]:
                if 0<=t<=1: final_pt=lp0+t*(lp1-lp0); break
            if final_pt is None: raise ValueError("Intersection outside segment.")
            pronasale_abbrev = center_label.replace("_pronasale_pred", "")
            nd_abbrev = equation.replace("pred ", "").replace(" ", "")
            final_label = f"{pronasale_abbrev}_{nd_abbrev}_sn_pred"
            pred_node.AddControlPoint(final_pt,final_label)
            self.step8StatusLabel.setText(f"Status: Point '{final_label}' created.")
        except Exception as e: self.step8StatusLabel.setText(f"Status: Error! {e}")

    def onCalculateNasion(self):
        self.step9StatusLabel.setText("Status: Calculating..."); slicer.app.processEvents()
        nh_c_id,nh_eq_id,nl_c_id,nl_eq_id = self.nh_center_buttons.checkedId(),self.nh_eq_buttons.checkedId(),self.nl_center_buttons.checkedId(),self.nl_eq_buttons.checkedId()
        if -1 in [nh_c_id,nh_eq_id,nl_c_id,nl_eq_id]: self.step9StatusLabel.setText("Status: Please make all four selections."); return
        try:
            pred_node=slicer.util.getNode("Rynn_soft_tissue_pred"); _,nh_c_idx=self.nh_center_points_data[nh_c_id]; nh_eq=self.nh_equations[nh_eq_id]; _,nl_c_idx=self.nl_center_points_data[nl_c_id]; nl_eq=self.nl_equations[nl_eq_id]
            nh_c,nl_c=np.zeros(3),np.zeros(3); pred_node.GetNthControlPointPositionWorld(nh_c_idx,nh_c); pred_node.GetNthControlPointPositionWorld(nl_c_idx,nl_c)
            nh_l,nl_l=pred_node.GetNthControlPointLabel(nh_c_idx),pred_node.GetNthControlPointLabel(nl_c_idx)
            def get_len(n): node=slicer.util.getNode(n); p0,p1=np.zeros(3),np.zeros(3); node.GetNthControlPointPositionWorld(0,p0); node.GetNthControlPointPositionWorld(1,p1); return np.linalg.norm(p1-p0)
            x,z=get_len("nas-aca X"),get_len("nas-subs Z")
            nh_r={"pred Rynn EA M NH":.78*z+9.5,"pred Rynn EA F NH":.63*z+17,"pred Sarilita M NH":.79*z+3.74,"pred Sarilita F NH":.69*x+12.36,"pred Bulut F NH":15.047+.687*z,"pred Bulut M NH":9.858+.784*z}[nh_eq]
            nl_r={"pred Rynn EA NL":.74*z+3.5,"pred Sarilita F NL":6.624+.71*z,"pred Sarilita M NL":.764+.807*z,"pred Bulut M NL":.66*x+7.77}[nl_eq]
            plane=slicer.util.getNode(self.activeProfilePlaneName); plane_n=np.array(plane.GetNormal())
            self.create_point_list_circle(nh_c,nh_r,plane_n,"NH_Circle_Points",(1,0,0)); self.create_point_list_circle(nl_c,nl_r,plane_n,"NL_Circle_Points",(0,0,1))
            c1,r1,c2,r2=nh_c,nh_r,nl_c,nl_r; d_v=c1-c2; d=np.linalg.norm(d_v)
            if d>r1+r2 or d<abs(r1-r2) or d==0: raise ValueError("Circles do not intersect.")
            a=(r1**2-r2**2+d**2)/(2*d); h=np.sqrt(max(0,r1**2-a**2)); p2=c1+a*(c2-c1)/d; v=np.cross(d_v,plane_n); v/=np.linalg.norm(v); inters=[p2+h*v,p2-h*v]
            l1=slicer.util.getNode("1"); l1p0,l1p1=np.zeros(3),np.zeros(3); l1.GetNthControlPointPositionWorld(0,l1p0); l1.GetNthControlPointPositionWorld(1,l1p1)
            def dist_to_line(pt,p0,p1): vec=p1-p0; plen=np.linalg.norm(vec); proj=np.dot(pt-p0,vec)/plen; proj=np.clip(proj,0,plen); return np.linalg.norm(pt-(p0+proj*(vec/plen)))
            closest=min(inters,key=lambda pt:dist_to_line(pt,l1p0,l1p1))
            pred_node.AddControlPoint(closest,f"n' pred (from NH:{nh_l} and NL:{nl_l})")
            self.step9StatusLabel.setText("Status: Point created.")
        except Exception as e: self.step9StatusLabel.setText(f"Status: Error! {e}")

# --- Entry Point ---
try:
    old_gui = slicer.util.mainWindow().findChild(qt.QWidget, "RynnMethodGUI")
    if old_gui: old_gui.close()
except: pass
rynnGui = RynnMethodGUI()
rynnGui.show()
```
