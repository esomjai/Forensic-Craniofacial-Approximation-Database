
```
python

import numpy as np
import slicer
import qt
import vtk
import urllib.request
import tempfile
import os

class PurkaitSinghGUI(qt.QWidget):
    """
    Complete GUI for Purkait and Singh (2024) Nasal Prediction Method
    With separate Measurements and Coordinates tables + Smart Auto-Detection
    """
    
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Purkait & Singh (2024) Method")
        self.setObjectName("PurkaitSinghGUI")
        
        # Normal window behavior - allows pop-ups to work correctly
        self.setWindowFlags(qt.Qt.Window)
        
        # Initialize all variables
        self.hardTissueNode = None
        self.softTissueNode = None
        self.mspNode = None
        self.fhpNode = None
        self.pred_FSTT_sn = None
        self.all_measurements = {}
        self.all_coordinates = {}
        
        # Setup UI
        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setSpacing(10)
        
        self.stepStack = qt. QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        self.createAllStepWidgets()
        self.setupNavigation()
        
        # Initialize step counter FIRST
        self.currentStep = 0
        
        # Then do auto-detection
        self.syncWithScene()
        self.showDetectionSummary()
        
        # Finally update UI
        self.updateStepUI()
        
    def createAllStepWidgets(self):
        self.createStep1_Welcome()
        self.createStep2_PlaneSetup()
        self.createStep3_Measurements()
        self.createStep4_Prediction()
        self.createStep5_Validation()
        self.createStep6_Results()
    
    def setupNavigation(self):
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        navLayout.setContentsMargins(0, 0, 0, 0)
        
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.clicked.connect(self.onPrevButtonClicked)
        
        self.stepLabel = qt.QLabel("Step 1/6")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter)
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.nextButton = qt.QPushButton("Next")
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        
        navLayout.addWidget(self.prevButton)
        navLayout.addStretch(1)
        navLayout.addWidget(self.stepLabel)
        navLayout.addStretch(1)
        navLayout.addWidget(self.nextButton)
        
        self.mainLayout.addWidget(navWidget)
    
    def createStep1_Welcome(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Welcome to Purkait & Singh (2024) Method")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "This tool will guide you through the nasal prediction workflow.\n\n"
            "You can download example landmarks or select your own."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        downloadGroup = qt.QGroupBox("Download Example Landmarks")
        downloadLayout = qt.QVBoxLayout(downloadGroup)
        
        downloadDesc = qt.QLabel(
            "Click below to download example landmark files from the GitHub repository.\n"
            "These will be automatically loaded into 3D Slicer."
        )
        downloadDesc.setWordWrap(True)
        downloadLayout.addWidget(downloadDesc)
        
        self.downloadHardButton = qt.QPushButton("⬇️ Download Hard Tissue Landmarks")
        self.downloadHardButton.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px; font-weight: bold;"
        )
        self.downloadHardButton.clicked.connect(self.onDownloadHardTissue)
        downloadLayout.addWidget(self.downloadHardButton)
        
        self.downloadSoftButton = qt.QPushButton("⬇️ Download Soft Tissue Landmarks")
        self.downloadSoftButton.setStyleSheet(
            "background-color: #9b59b6; color: white; padding: 8px; font-weight: bold;"
        )
        self.downloadSoftButton.clicked.connect(self.onDownloadSoftTissue)
        downloadLayout.addWidget(self.downloadSoftButton)
        
        self.downloadStatusLabel = qt.QLabel("")
        self.downloadStatusLabel.setWordWrap(True)
        downloadLayout.addWidget(self.downloadStatusLabel)
        
        layout.addWidget(downloadGroup)
        
        selectionGroup = qt.QGroupBox("Or Select Existing Landmarks")
        selectionLayout = qt.QVBoxLayout(selectionGroup)
        
        self.hardTissueSelector = slicer.qMRMLNodeComboBox()
        self.hardTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.hardTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.hardTissueSelector.noneEnabled = True
        self.hardTissueSelector.addEnabled = False
        self.hardTissueSelector.removeEnabled = False
        self.hardTissueSelector.selectNodeUponCreation = True
        self.hardTissueSelector.currentNodeChanged.connect(self.onHardTissueSelected)
        
        formLayout = qt.QFormLayout()
        formLayout.addRow("Hard Tissue Landmarks:", self.hardTissueSelector)
        selectionLayout.addLayout(formLayout)
        
        layout.addWidget(selectionGroup)
        
        self.step1StatusLabel = qt.QLabel("Status: Download landmarks or select 'PS_hard_tissue' node.")
        self.step1StatusLabel.setWordWrap(True)
        layout.addWidget(self.step1StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def onDownloadHardTissue(self):
        try:
            self.downloadStatusLabel.setText("⏳ Downloading hard tissue landmarks...")
            slicer.app.processEvents()
            
            url = "https://github.com/user-attachments/files/21217369/PS_hard_tissue.mrk. json"
            temp_file = os.path.join(tempfile. gettempdir(), "PS_hard_tissue.mrk.json")
            
            urllib.request.urlretrieve(url, temp_file)
            success = slicer.util.loadMarkups(temp_file)
            
            if success:
                self.hardTissueNode = slicer.util.getNode("PS_hard_tissue")
                self.hardTissueSelector.setCurrentNode(self.hardTissueNode)
                
                self.downloadStatusLabel.setText("✅ Hard tissue landmarks downloaded and loaded successfully!")
                self.step1StatusLabel.setText("Status: ✅ Hard tissue landmarks ready!")
                self.step1StatusLabel.setStyleSheet("color: green; font-weight: bold;")
                slicer.util.showStatusMessage("Hard tissue landmarks loaded!", 3000)
            else:
                raise Exception("Failed to load file")
                
        except Exception as e:
            self.downloadStatusLabel.setText("❌ Error:  {0}".format(str(e)))
            slicer.util.errorDisplay("Failed to download hard tissue landmarks: {0}".format(str(e)))
    
    def onDownloadSoftTissue(self):
        try:
            self.downloadStatusLabel.setText("⏳ Downloading soft tissue landmarks...")
            slicer.app.processEvents()
            
            url = "https://github.com/user-attachments/files/21217705/PS_soft_tissue.mrk.json"
            temp_file = os.path.join(tempfile.gettempdir(), "PS_soft_tissue.mrk.json")
            
            urllib.request.urlretrieve(url, temp_file)
            success = slicer.util.loadMarkups(temp_file)
            
            if success: 
                self.softTissueNode = slicer.util. getNode("PS_soft_tissue")
                if hasattr(self, 'softTissueSelector'):
                    self.softTissueSelector.setCurrentNode(self.softTissueNode)
                
                self.downloadStatusLabel.setText("✅ Soft tissue landmarks downloaded and loaded successfully!")
                slicer.util.showStatusMessage("Soft tissue landmarks loaded!", 3000)
            else:
                raise Exception("Failed to load file")
                
        except Exception as e:
            self.downloadStatusLabel.setText("❌ Error: {0}".format(str(e)))
            slicer.util.errorDisplay("Failed to download soft tissue landmarks: {0}".format(str(e)))
    
    def createStep2_PlaneSetup(self):
        widget = qt. QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 2: Setup Reference Planes")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        mspGroup = qt.QGroupBox("Midsagittal Plane (MSP)")
        mspLayout = qt.QVBoxLayout(mspGroup)
        
        mspDesc = qt.QLabel("Create MSP using best-fit through:  nasion, rhinion, subspinale, and ANS.")
        mspDesc.setWordWrap(True)
        mspLayout.addWidget(mspDesc)
        
        self.createMSPButton = qt.QPushButton("Create MSP from Landmarks")
        self.createMSPButton.clicked.connect(self.onCreateMSP)
        mspLayout.addWidget(self.createMSPButton)
        
        layout. addWidget(mspGroup)
        
        fhpGroup = qt.QGroupBox("Frankfurt Horizontal Plane (FHP)")
        fhpLayout = qt.QVBoxLayout(fhpGroup)
        
        fhpDesc = qt.QLabel("Please ensure you have created your FHP before proceeding.")
        fhpDesc.setWordWrap(True)
        fhpLayout.addWidget(fhpDesc)
        
        self.fhpSelector = slicer.qMRMLNodeComboBox()
        self.fhpSelector.nodeTypes = ["vtkMRMLMarkupsPlaneNode"]
        self.fhpSelector.setMRMLScene(slicer. mrmlScene)
        self.fhpSelector.noneEnabled = True
        self.fhpSelector.selectNodeUponCreation = True
        self.fhpSelector. currentNodeChanged.connect(self.onFHPSelected)
        
        fhpFormLayout = qt.QFormLayout()
        fhpFormLayout. addRow("FHP Plane:", self.fhpSelector)
        fhpLayout.addLayout(fhpFormLayout)
        
        layout. addWidget(fhpGroup)
        
        self.step2StatusLabel = qt.QLabel("Status: Please create MSP and select FHP.")
        self.step2StatusLabel.setWordWrap(True)
        layout.addWidget(self.step2StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep3_Measurements(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt. QLabel("Step 3: Create Hard Tissue Measurements")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "This will create all guide lines and measurements needed for prediction.\n\n"
            "Please set the facial soft tissue thickness (FSTT) for subnasale prediction:"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        fsttForm = qt.QFormLayout()
        self.fsttSpinBox = qt.QDoubleSpinBox()
        self.fsttSpinBox.setRange(0.01, 30.0)
        self.fsttSpinBox.setValue(13.50)
        self.fsttSpinBox.setDecimals(2)
        self.fsttSpinBox. setSingleStep(0.1)
        self.fsttSpinBox.setSuffix(" mm")
        fsttForm.addRow("FSTT for sn':", self.fsttSpinBox)
        layout.addLayout(fsttForm)
        
        self.createMeasurementsButton = qt. QPushButton("Create All Measurements")
        self.createMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px; font-weight: bold;"
        )
        self.createMeasurementsButton.clicked.connect(self.onCreateMeasurements)
        layout.addWidget(self.createMeasurementsButton)
        
        self.step3StatusLabel = qt.QLabel("Status: Ready to create measurements.")
        self.step3StatusLabel.setWordWrap(True)
        layout.addWidget(self.step3StatusLabel)
        
        layout. addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep4_Prediction(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt. QLabel("Step 4: Predict Pronasale")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt. QLabel("Select the biological sex and visualization options, then run the prediction.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        sexGroup = qt.QGroupBox("Biological Sex")
        sexLayout = qt.QHBoxLayout(sexGroup)
        
        self.maleRadio = qt.QRadioButton("Male")
        self.femaleRadio = qt. QRadioButton("Female")
        self.bothRadio = qt.QRadioButton("Both (for comparison)")
        self.maleRadio.setChecked(True)
        
        sexLayout.addWidget(self.maleRadio)
        sexLayout.addWidget(self.femaleRadio)
        sexLayout.addWidget(self.bothRadio)
        sexLayout.addStretch()
        
        layout.addWidget(sexGroup)
        
        self.showLinesCheckbox = qt.QCheckBox("Show visualization lines")
        self.showLinesCheckbox.setChecked(True)
        layout.addWidget(self.showLinesCheckbox)
        
        self.predictButton = qt.QPushButton("Run Pronasale Prediction")
        self.predictButton.setStyleSheet(
            "background-color: #e74c3c; color: white; padding: 10px; font-weight: bold;"
        )
        self.predictButton.clicked.connect(self.onRunPrediction)
        layout.addWidget(self.predictButton)
        
        self.step4StatusLabel = qt.QLabel("Status: Ready to predict.")
        self.step4StatusLabel.setWordWrap(True)
        layout.addWidget(self.step4StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep5_Validation(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 5: Validation & Additional Measurements (Optional)")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "If you have ground truth soft tissue landmarks, you can calculate prediction errors "
            "and create additional measurements from the paper."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        self.softTissueSelector = slicer.qMRMLNodeComboBox()
        self.softTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.softTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.softTissueSelector.noneEnabled = True
        self.softTissueSelector.selectNodeUponCreation = True
        self.softTissueSelector.currentNodeChanged.connect(self.onSoftTissueSelected)
        
        formLayout = qt.QFormLayout()
        formLayout.addRow("Soft Tissue Landmarks:", self.softTissueSelector)
        layout.addLayout(formLayout)
        
        self.additionalMeasurementsButton = qt.QPushButton("📏 Create All Additional Measurements")
        self.additionalMeasurementsButton.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px; font-weight: bold;"
        )
        self.additionalMeasurementsButton. clicked.connect(self.onCreateAdditionalMeasurements)
        layout.addWidget(self.additionalMeasurementsButton)
        
        self.calculateErrorButton = qt.QPushButton("📊 Calculate Prediction Errors")
        self.calculateErrorButton.setStyleSheet(
            "background-color: #9b59b6; color: white; padding: 8px; font-weight: bold;"
        )
        self.calculateErrorButton. clicked.connect(self.onCalculateErrors)
        layout.addWidget(self.calculateErrorButton)
        
        self.step5StatusLabel = qt.QLabel("Status: Optional step.")
        self.step5StatusLabel.setWordWrap(True)
        layout.addWidget(self.step5StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep6_Results(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 6: Results & Export")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        measurementsLabel = qt.QLabel("<b>📏 Measurements (Distances & Angles)</b>")
        measurementsLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(measurementsLabel)
        
        instructionsLabel = qt.QLabel(
            "Prediction errors are <span style='background-color: #ffffcc;'>highlighted in yellow</span>."
        )
        instructionsLabel.setWordWrap(True)
        layout.addWidget(instructionsLabel)
        
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable. setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Value", "Unit"])
        self.measurementsTable.horizontalHeader().setStretchLastSection(False)
        self.measurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView. Stretch)
        self.measurementsTable.setMinimumHeight(250)
        self.measurementsTable.setAlternatingRowColors(True)
        layout.addWidget(self.measurementsTable)
        
        coordinatesLabel = qt.QLabel("<b>📍 Coordinates Comparison (Predicted vs True)</b>")
        coordinatesLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(coordinatesLabel)
        
        coordDesc = qt.QLabel("3D positions in space (RAS coordinate system:  Right, Anterior, Superior)")
        coordDesc.setWordWrap(True)
        layout.addWidget(coordDesc)
        
        self.coordinatesTable = qt.QTableWidget()
        self.coordinatesTable.setColumnCount(8)
        self.coordinatesTable.setHorizontalHeaderLabels([
            "Landmark", 
            "Predicted X", "Predicted Y", "Predicted Z",
            "True X", "True Y", "True Z",
            "3D Error (mm)"
        ])
        self.coordinatesTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self.coordinatesTable. setMinimumHeight(150)
        self.coordinatesTable.setAlternatingRowColors(True)
        layout.addWidget(self.coordinatesTable)
        
        buttonLayout = qt.QHBoxLayout()
        
        self.copyMeasurementsButton = qt. QPushButton("📋 Copy Measurements")
        self.copyMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px; font-weight: bold;"
        )
        self.copyMeasurementsButton.setToolTip("Copy measurements table to clipboard")
        self.copyMeasurementsButton.clicked.connect(self.onCopyMeasurements)
        buttonLayout.addWidget(self.copyMeasurementsButton)
        
        self.copyCoordinatesButton = qt.QPushButton("📋 Copy Coordinates")
        self.copyCoordinatesButton.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px; font-weight: bold;"
        )
        self.copyCoordinatesButton. setToolTip("Copy coordinates table to clipboard")
        self.copyCoordinatesButton.clicked.connect(self.onCopyCoordinates)
        buttonLayout.addWidget(self.copyCoordinatesButton)
        
        self.finishButton = qt.QPushButton("Finish")
        self.finishButton.clicked.connect(lambda: self.close())
        buttonLayout.addWidget(self.finishButton)
        
        layout.addLayout(buttonLayout)
        
        self.step6StatusLabel = qt.QLabel("Status: Review results above.")
        self.step6StatusLabel.setWordWrap(True)
        layout.addWidget(self.step6StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    # ==================== ENHANCED:  SMART AUTO-DETECTION ====================
    
    def syncWithScene(self):
        """ENHANCED: Smart auto-detection with multiple name variations"""
        # Hard tissue detection
        possible_hard_names = ["PS_hard_tissue", "hard_tissue", "Hard_tissue", "hard", "Hard Tissue", "HardTissue"]
        for name in possible_hard_names: 
            node = slicer.util.getFirstNodeByName(name)
            if node:
                self.hardTissueNode = node
                self.hardTissueSelector.setCurrentNode(node)
                print("✅ Auto-detected hard tissue:  '{0}'".format(name))
                break
        
        # MSP detection
        possible_msp_names = ["MSP", "msp", "Midsagittal", "midsagittal", "Mid-Sagittal", "mid-sagittal"]
        for name in possible_msp_names: 
            node = slicer. util.getFirstNodeByName(name)
            if node: 
                self.mspNode = node
                print("✅ Auto-detected MSP: '{0}'".format(name))
                break
        
        # FHP detection - ENHANCED with more variations
        possible_fhp_names = ["FHP", "fhp", "Frankfurt", "frankfurt", "Frankfort", "frankfort", "FH", "fh", "Frankfurt Horizontal", "frankfurt horizontal"]
        for name in possible_fhp_names:
            node = slicer.util.getFirstNodeByName(name)
            if node: 
                self.fhpNode = node
                self.fhpSelector.setCurrentNode(node)
                print("✅ Auto-detected FHP: '{0}'".format(name))
                break
        
        # Soft tissue detection
        possible_soft_names = ["PS_soft_tissue", "soft_tissue", "Soft_tissue", "soft", "Soft Tissue", "SoftTissue"]
        for name in possible_soft_names: 
            node = slicer.util.getFirstNodeByName(name)
            if node:
                self.softTissueNode = node
                if hasattr(self, 'softTissueSelector'):
                    self.softTissueSelector. setCurrentNode(node)
                print("✅ Auto-detected soft tissue: '{0}'".format(name))
                break
    
    def showDetectionSummary(self):
        """Show a summary of what was auto-detected"""
        detected = []
        
        if self.hardTissueNode:
            detected.append("✅ Hard tissue landmarks")
        if self.mspNode:
            detected.append("✅ MSP plane")
        if self.fhpNode:
            detected.append("✅ FHP plane")
        if self.softTissueNode:
            detected.append("✅ Soft tissue landmarks")
        
        if detected: 
            summary = "Auto-detected nodes:\n" + "\n".join(detected)
            print("\n" + "="*50)
            print(summary)
            print("="*50 + "\n")
            slicer.util.showStatusMessage("Auto-detection complete! Check Python console for details.", 3000)
            
            # Update status labels
            if self.hardTissueNode:
                self.step1StatusLabel.setText("Status: ✅ Hard tissue detected!")
                self.step1StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            if self.currentStep == 1:
                self.updateStep2Status()
        else:
            print("No existing nodes detected.  Please load or create landmarks.")
    
    # ==================== HELPER METHODS ====================
    
    def getPoint(self, node, index):
        point = [0, 0, 0]
        node.GetNthControlPointPosition(index, point)
        return np.array(point)
    
    def getPointByLabel(self, node, label):
        for i in range(node.GetNumberOfControlPoints()):
            if node. GetNthControlPointLabel(i) == label:
                return self.getPoint(node, i)
        raise ValueError("Point '{0}' not found". format(label))
    
    def getPlaneData(self, planeNode):
        if 'Plane' in planeNode.GetClassName():
            origin = [0, 0, 0]
            normal = [0, 0, 0]
            planeNode.GetOrigin(origin)
            planeNode.GetNormal(normal)
            return np.array(origin), np.array(normal)
        else:
            raise ValueError("Node is not a plane")
    
    def createLine(self, p1, p2, name, color=[1.0, 1.0, 1.0], selected_color=[1.0, 0.5, 0.0], thickness=0.25):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
        lineNode.AddControlPoint(p1.tolist())
        lineNode.AddControlPoint(p2.tolist())
        
        displayNode = lineNode.GetDisplayNode()
        if displayNode:
            displayNode. SetColor(*color)
            displayNode.SetSelectedColor(*selected_color)
            displayNode.SetLineThickness(thickness)
            displayNode.SetGlyphScale(1.8)
        
        return lineNode
    
    def getLineLength(self, lineNode):
        start = [0, 0, 0]
        end = [0, 0, 0]
        lineNode.GetNthControlPointPosition(0, start)
        lineNode.GetNthControlPointPosition(1, end)
        return np.linalg.norm(np.array(end) - np.array(start))
    
    def storeMeasurement(self, name, value, unit="mm", is_summary=False):
        self.all_measurements[name] = {
            "value": value,
            "unit": unit,
            "is_summary": is_summary
        }
    
    def storeCoordinate(self, landmark_name, predicted_coords, true_coords=None):
        self.all_coordinates[landmark_name] = {
            "predicted":  predicted_coords,
            "true": true_coords
        }
    
    def onHardTissueSelected(self, node):
        if node: 
            self.hardTissueNode = node
            self.step1StatusLabel.setText("Status: ✅ Selected '{0}'. ".format(node.GetName()))
            self.step1StatusLabel.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.hardTissueNode = None
            self.step1StatusLabel.setText("Status: Download landmarks or select 'PS_hard_tissue' node.")
            self.step1StatusLabel.setStyleSheet("")
    
    def onFHPSelected(self, node):
        """ENHANCED: Smart FHP selection with status updates"""
        if node: 
            self.fhpNode = node
            print("✅ FHP selected: '{0}'".format(node.GetName()))
            self.updateStep2Status()
            
            # Check if both planes are ready
            if self.mspNode: 
                slicer.util.showStatusMessage("✅ Both planes ready!  You can proceed to Step 3.", 3000)
        else:
            self.fhpNode = None
            self.updateStep2Status()
    
    def onSoftTissueSelected(self, node):
        if node:
            self.softTissueNode = node
            self.step5StatusLabel.setText("Status: ✅ Selected '{0}'.". format(node.GetName()))
            self.step5StatusLabel. setStyleSheet("color: green; font-weight: bold;")
        else:
            self.softTissueNode = None
            self.step5StatusLabel.setText("Status: Optional step.")
            self.step5StatusLabel.setStyleSheet("")
    
    def updateStep2Status(self):
        """ENHANCED: Color-coded status messages"""
        if self.mspNode and self.fhpNode:
            self.step2StatusLabel.setText("Status: ✅ MSP and FHP ready!  Click 'Next' to continue.")
            self.step2StatusLabel.setStyleSheet("color: green; font-weight: bold;")
        elif self.mspNode:
            self.step2StatusLabel.setText("Status: MSP created.  ⚠️ Please select FHP plane.")
            self.step2StatusLabel.setStyleSheet("color: orange; font-weight: bold;")
        elif self.fhpNode:
            self.step2StatusLabel.setText("Status: FHP selected. ⚠️ Please create MSP.")
            self.step2StatusLabel.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.step2StatusLabel.setText("Status: ❌ Please create MSP and select FHP.")
            self.step2StatusLabel.setStyleSheet("color: red; font-weight:  bold;")
    
    def onCreateMSP(self):
        try:
            if not self.hardTissueNode:
                raise ValueError("Please select hard tissue landmarks first.")
            
            self.step2StatusLabel.setText("Status: Creating MSP...")
            self.step2StatusLabel.setStyleSheet("color: blue;")
            slicer.app.processEvents()
            
            points = []
            for i in range(4):
                points.append(self.getPoint(self.hardTissueNode, i))
            points = np.array(points)
            
            centroid = np.mean(points, axis=0)
            pts_centered = points - centroid
            U, S, Vt = np.linalg.svd(pts_centered)
            normal = Vt[2, :]
            
            existing = slicer.util.getFirstNodeByName('MSP')
            if existing: 
                slicer.mrmlScene.RemoveNode(existing)
            
            self.mspNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'MSP')
            self.mspNode.SetOriginWorld(centroid)
            self.mspNode. SetNormalWorld(normal)
            
            self.updateStep2Status()
            slicer.util.showStatusMessage("✅ MSP created successfully!", 3000)
            print("✅ MSP created from landmarks")
            
        except Exception as e:
            self.step2StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step2StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create MSP:  {0}".format(str(e)))
    
    def onCreateMeasurements(self):
        try:
            if not all([self.hardTissueNode, self.mspNode, self.fhpNode]):
                raise ValueError("Please complete previous steps first.")
            
            self.step3StatusLabel.setText("Status: Creating measurements...")
            slicer.app.processEvents()
            
            msp_origin, msp_normal = self.getPlaneData(self.mspNode)
            fhp_origin, fhp_normal = self.getPlaneData(self.fhpNode)
            
            line_direction = np.cross(msp_normal, fhp_normal)
            line_direction = line_direction / np.linalg. norm(line_direction)
            
            length = 70.0
            half_vec = 0.5 * length * line_direction
            fhp_start = msp_origin - half_vec
            fhp_end = msp_origin + half_vec
            
            self.createLine(fhp_start, fhp_end, 'FHP guide', [1.0, 1.0, 1.0], [1.0, 0.0, 0.0])
            
            guide_names = ['st n guide', 'st rhi guide', 'st sn guide']
            guide_colors = {
                'st n guide': ([1.0, 1.0, 1.0], [0.0, 1.0, 0.0]),
                'st rhi guide':  ([1.0, 1.0, 1.0], [0.0, 0.0, 1.0]),
                'st sn guide': ([1.0, 1.0, 1.0], [1.0, 1.0, 0.0])
            }
            
            for i, name in enumerate(guide_names):
                landmark_pos = self.getPoint(self.hardTissueNode, i)
                start = landmark_pos - half_vec
                end = landmark_pos + half_vec
                self.createLine(start, end, name, *guide_colors[name])
            
            pred_FSTT_sn = slicer.util.getFirstNodeByName('pred_FSTT_sn')
            if pred_FSTT_sn:
                slicer.mrmlScene.RemoveNode(pred_FSTT_sn)
            self.pred_FSTT_sn = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pred_FSTT_sn')
            
            sn_thickness = self.fsttSpinBox.value
            
            st_sn_guide = slicer.util.getNode('st sn guide')
            sn_guide_start = self.getPoint(st_sn_guide, 0)
            sn_guide_end = self.getPoint(st_sn_guide, 1)
            
            guide_vec = sn_guide_end - sn_guide_start
            guide_unit_vec = guide_vec / np. linalg.norm(guide_vec)
            guide_unit_vec = -guide_unit_vec
            
            ss_point = self.getPoint(self.hardTissueNode, 2)
            pred_sn_position = ss_point + guide_unit_vec * sn_thickness
            
            self.pred_FSTT_sn.AddControlPoint(pred_sn_position.tolist(), "sn'_FSTT")
            
            displayNode = self.pred_FSTT_sn.GetDisplayNode()
            if displayNode: 
                displayNode.SetColor(0.0, 0.8, 0.0)
                displayNode.SetSelectedColor(1.0, 0.0, 0.0)
                displayNode.SetGlyphScale(1.8)
                displayNode.SetTextScale(3.0)
                displayNode.SetSliceProjection(True)
            
            n_point = self.getPoint(self.hardTissueNode, 0)
            self.createLine(n_point, pred_sn_position, 'n to sn FSTT', [1.0, 1.0, 1.0], [0.5, 0.5, 0.0])
            
            n_to_sn_dist = np.linalg.norm(pred_sn_position - n_point)
            self.storeMeasurement("n to sn FSTT", n_to_sn_dist)
            
            ab_start = self.getPoint(self.hardTissueNode, 4)
            ab_end = self.getPoint(self.hardTissueNode, 5)
            ab_line = self.createLine(ab_start, ab_end, 'AB', [1.0, 1.0, 1.0], [1.0, 0.0, 1.0])
            self.storeMeasurement("AB", self.getLineLength(ab_line))
            
            cd_start = self.getPoint(self.hardTissueNode, 6)
            cd_end = self.getPoint(self.hardTissueNode, 7)
            cd_line = self.createLine(cd_start, cd_end, 'CD', [1.0, 1.0, 1.0], [0.0, 1.0, 1.0])
            self.storeMeasurement("CD", self.getLineLength(cd_line))
            
            baseline_start = self.getPoint(self.hardTissueNode, 0)
            baseline_end = self.getPoint(self.hardTissueNode, 3)
            baseline_line = self.createLine(baseline_start, baseline_end, 'baseline', [1.0, 1.0, 1.0], [1.0, 0.5, 0.0])
            self.storeMeasurement("baseline", self.getLineLength(baseline_line))
            
            n_to_rhi_start = self.getPoint(self.hardTissueNode, 0)
            n_to_rhi_end = self.getPoint(self.hardTissueNode, 1)
            n_to_rhi_line = self.createLine(n_to_rhi_start, n_to_rhi_end, 'n to rhi', [1.0, 1.0, 1.0], [0.5, 0.0, 0.5])
            self.storeMeasurement("n to rhi", self.getLineLength(n_to_rhi_line))
            
            rhi_point = self.getPoint(self.hardTissueNode, 1)
            baseline_vec = baseline_end - baseline_start
            line_unit_vec = baseline_vec / np.linalg.norm(baseline_vec)
            
            v = rhi_point - baseline_start
            proj_length = np.dot(v, line_unit_vec)
            closest_point = baseline_start + proj_length * line_unit_vec
            
            rhi_to_baseline_line = self.createLine(rhi_point, closest_point, 'rhi to baseline', [1.0, 1.0, 1.0], [0.7, 0.3, 0.3])
            self.storeMeasurement("rhi to baseline", self.getLineLength(rhi_to_baseline_line))
            
            self.step3StatusLabel.setText("Status: ✅ All measurements created successfully!")
            self.step3StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            slicer.util.showStatusMessage("Measurements created!", 3000)
            
            self.updateResultsTables()
            
        except Exception as e:
            self.step3StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step3StatusLabel. setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create measurements: {0}".format(str(e)))
    
    def onRunPrediction(self):
        try:
            if self.bothRadio.isChecked():
                self.step4StatusLabel.setText("Status: Running predictions for both sexes...")
                slicer. app.processEvents()
                self.runSinglePrediction("male")
                self.runSinglePrediction("female")
                self.step4StatusLabel.setText("Status: ✅ Predictions completed for both sexes!")
                self.step4StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            elif self.maleRadio.isChecked():
                self.step4StatusLabel.setText("Status: Running male prediction...")
                slicer. app.processEvents()
                self.runSinglePrediction("male")
                self.step4StatusLabel.setText("Status: ✅ Male prediction completed!")
                self.step4StatusLabel. setStyleSheet("color: green; font-weight: bold;")
            else:
                self.step4StatusLabel.setText("Status: Running female prediction...")
                slicer.app.processEvents()
                self.runSinglePrediction("female")
                self.step4StatusLabel.setText("Status: ✅ Female prediction completed!")
                self.step4StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            slicer.util.showStatusMessage("Prediction complete!", 3000)
            self.updateResultsTables()
            
        except Exception as e:
            self.step4StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step4StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer. util.errorDisplay("Failed to predict: {0}".format(str(e)))
    
    def runSinglePrediction(self, sex):
        coefficients = {
            'male': {'prn_baseline': (19.544, 0.299)},
            'female': {'prn_baseline': (15.056, 0.622)}
        }
        
        coeffs = coefficients[sex]
        show_lines = self.showLinesCheckbox.isChecked()
        
        baselineNode = slicer.util. getNode('baseline')
        rhiToBaselineNode = slicer. util.getNode('rhi to baseline')
        
        if not all([self.hardTissueNode, baselineNode, rhiToBaselineNode, self.mspNode]):
            raise ValueError("Required measurements not found.  Please run Step 3 first.")
        
        pred_node_name = 'pred_soft_tissue_{0}'.format(sex)
        pred_node = slicer.util.getFirstNodeByName(pred_node_name)
        if pred_node:
            while pred_node. GetNumberOfControlPoints() > 0:
                pred_node.RemoveNthControlPoint(0)
        else:
            pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', pred_node_name)
        
        msp_origin, msp_normal = self.getPlaneData(self.mspNode)
        ans_point = self.getPoint(self.hardTissueNode, 3)
        
        baseline_start = self.getPoint(baselineNode, 0)
        baseline_end = self.getPoint(baselineNode, 1)
        baseline_vec = baseline_end - baseline_start
        baseline_unit = baseline_vec / np.linalg.norm(baseline_vec)
        
        perp_vec = np.cross(baseline_unit, msp_normal)
        perp_vec = perp_vec / np.linalg.norm(perp_vec)
        
        if perp_vec[1] < 0:
            perp_vec = -perp_vec
        
        if show_lines:
            ans_perp_length = 60.0
            ans_perp_start = ans_point - (ans_perp_length / 2.0) * perp_vec
            ans_perp_end = ans_point + (ans_perp_length / 2.0) * perp_vec
            self.createLine(ans_perp_start, ans_perp_end, "ANS perpendicular_{0}".format(sex), [0.0, 0.8, 0.8], [0.0, 1.0, 1.0])
        
        rhi_to_baseline_length = self.getLineLength(rhiToBaselineNode)
        intercept, coeff = coeffs['prn_baseline']
        pred_prn_distance = intercept + coeff * rhi_to_baseline_length
        pred_prn_point = ans_point + pred_prn_distance * perp_vec
        
        if show_lines:
            self.createLine(ans_point, pred_prn_point, "ANS to pred_prn_{0}".format(sex), [0.8, 0.8, 0.0], [1.0, 0.7, 0.0])
        
        pred_node.AddControlPoint(pred_prn_point.tolist(), "pred_prn_{0}". format(sex))
        pred_node.SetNthControlPointDescription(0, "Predicted pronasale ({0})".format(sex))
        
        self.storeMeasurement("Predicted Pronasale Distance ({0})".format(sex), pred_prn_distance, "mm")
        self.storeCoordinate("Pronasale ({0})".format(sex), pred_prn_point)
        
        displayNode = pred_node.GetDisplayNode()
        if displayNode: 
            if sex == "male":
                displayNode.SetColor(0.0, 0.0, 0.8)
                displayNode. SetSelectedColor(0.0, 0.0, 1.0)
            else:
                displayNode.SetColor(0.0, 0.8, 0.0)
                displayNode. SetSelectedColor(0.0, 1.0, 0.0)
            
            displayNode.SetGlyphScale(1.8)
            displayNode.SetTextScale(3.0)
            displayNode. SetGlyphType(1)
            displayNode.SetSliceProjection(True)
    
    def onCreateAdditionalMeasurements(self):
        try:
            if not self.softTissueNode:
                raise ValueError("Please select soft tissue landmarks first (PS_soft_tissue).")
            
            if not self.hardTissueNode:
                raise ValueError("Hard tissue landmarks not found.")
            
            self.step5StatusLabel.setText("Status: Creating additional measurements...")
            slicer.app.processEvents()
            
            baselineNode = slicer.util.getFirstNodeByName("baseline")
            if baselineNode:
                baseline_start = np.zeros(3)
                baseline_end = np.zeros(3)
                baselineNode.GetNthControlPointPosition(0, baseline_start)
                baselineNode.GetNthControlPointPosition(1, baseline_end)
                baseline_dir = (baseline_end - baseline_start)
                baseline_dir = baseline_dir / np.linalg.norm(baseline_dir)
            else:
                n_soft = self.getPointByLabel(self.softTissueNode, "n'")
                baseline_dir = np.array([1.0, 0.0, 0.0])
                baseline_start = n_soft. copy()
                baseline_end = n_soft + baseline_dir * 100.0
                baselineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "baseline")
                baselineNode.AddControlPoint(baseline_start.tolist())
                baselineNode.AddControlPoint(baseline_end.tolist())
            
            n_hard = self.getPointByLabel(self.hardTissueNode, "n")
            n_soft = self.getPointByLabel(self.softTissueNode, "n'")
            nn_dist = self.createMeasurementLine("n-n'", n_hard, n_soft)
            self.storeMeasurement("n-n'", nn_dist)
            
            rhi_hard = self.getPointByLabel(self.hardTissueNode, "rhi")
            rhi_soft = self.getPointByLabel(self.softTissueNode, "rhi'")
            rhi_dist = self.createMeasurementLine("rhi-rhi'", rhi_hard, rhi_soft)
            self.storeMeasurement("rhi-rhi'", rhi_dist)
            
            sn = self.getPointByLabel(self.softTissueNode, "sn'")
            
            alL = self.getPointByLabel(self.softTissueNode, "X1(alL)")
            alR = self.getPointByLabel(self.softTissueNode, "X2(alR)")
            al_dist = self.createMeasurementLine("al-al", alL, alR)
            self.storeMeasurement("al-al", al_dist)
            
            nbL = self.getPointByLabel(self.softTissueNode, "Y1(nbL)")
            nbR = self.getPointByLabel(self.softTissueNode, "Y2(nbR)")
            nb_dist = self.createMeasurementLine("nb-nb", nbL, nbR)
            self.storeMeasurement("nb-nb", nb_dist)
            
            P, Q, xy_dist = self.shortestDistanceBetweenLines(alL, alR, nbL, nbR)
            self.createMeasurementLine("X-Y", P, Q)
            self.storeMeasurement("X-Y", xy_dist)
            
            nt = self.getPointByLabel(self.softTissueNode, "nt")
            n_nt_dist = self.createMeasurementLine("soft n-nt", n_soft, nt)
            self.storeMeasurement("soft n-nt", n_nt_dist)
            
            prn = self.getPointByLabel(self.softTissueNode, "prn")
            prn_proj = baseline_start + np.dot(prn - baseline_start, baseline_dir) * baseline_dir
            prn_perp_dist = self.createMeasurementLine("prn perp baseline", prn, prn_proj)
            self.storeMeasurement("prn perp baseline", prn_perp_dist)
            
            rhi_prn_sn_angle = self.createAngle("soft rhi'-prn-sn'", rhi_soft, prn, sn)
            self.storeMeasurement("soft rhi'-prn-sn'", rhi_prn_sn_angle, "degrees")
            
            prn_sn_nt_angle = self.createAngle("prn-sn'-nt", prn, sn, nt)
            self.storeMeasurement("prn-sn'-nt", prn_sn_nt_angle, "degrees")
            
            al_prn_al_angle = self.createAngle("al-prn-al", alL, prn, alR)
            self.storeMeasurement("al-prn-al", al_prn_al_angle, "degrees")
            
            self.step5StatusLabel.setText("Status: ✅ All additional measurements created successfully!")
            self.step5StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            slicer.util.showStatusMessage("Additional measurements complete!", 3000)
            
            self.updateResultsTables()
            
        except Exception as e:
            self.step5StatusLabel.setText("Status: ❌ Error - {0}". format(str(e)))
            self.step5StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create additional measurements: {0}".format(str(e)))
    
    def createMeasurementLine(self, name, point1, point2):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
        line_node.AddControlPoint(point1.tolist())
        line_node.AddControlPoint(point2.tolist())
        display_node = line_node.GetDisplayNode()
        if display_node:
            display_node. SetTextScale(3.0)
        return np.linalg.norm(point2 - point1)
    
    def createAngle(self, name, point1, apex, point2):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        angle_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsAngleNode", name)
        angle_node.AddControlPoint(point1.tolist())
        angle_node.AddControlPoint(apex.tolist())
        angle_node.AddControlPoint(point2.tolist())
        display_node = angle_node. GetDisplayNode()
        if display_node:
            display_node.SetTextScale(3.0)
        return angle_node. GetAngleDegrees()
    
    def shortestDistanceBetweenLines(self, p1, p2, q1, q2):
        v = p2 - p1
        u = q2 - q1
        w0 = p1 - q1
        
        a = np.dot(v, v)
        b = np.dot(v, u)
        c = np.dot(u, u)
        d = np.dot(v, w0)
        e = np.dot(u, w0)
        
        denom = a * c - b * b
        
        if abs(denom) < 1e-6:
            t = np.dot(v, w0) / a if a > 0 else 0
            t = max(0, min(1, t))
            closest_on_line1 = p1 + t * v
            s = 0.5
            closest_on_line2 = q1 + s * u
            distance = np.linalg.norm(closest_on_line2 - closest_on_line1)
            return closest_on_line1.astype(float), closest_on_line2.astype(float), distance
        
        s = (b * e - c * d) / denom
        t = (a * e - b * d) / denom
        
        s = max(0, min(1, s))
        t = max(0, min(1, t))
        
        P = p1 + s * v
        Q = q1 + t * u
        distance = np.linalg.norm(P - Q)
        
        return P.astype(float), Q.astype(float), distance
    
    def onCalculateErrors(self):
        try:
            if not self.softTissueNode:
                raise ValueError("Please select soft tissue landmarks first.")
            
            self.step5StatusLabel.setText("Status: Calculating errors...")
            slicer.app.processEvents()
            
            pred_male = slicer.util.getFirstNodeByName('pred_soft_tissue_male')
            pred_female = slicer.util.getFirstNodeByName('pred_soft_tissue_female')
            
            if not pred_male and not pred_female:
                raise ValueError("No predictions found. Please run Step 4 first.")
            
            errors = []
            true_prn = self.getPointByLabel(self.softTissueNode, "prn")
            
            if pred_male:
                pred_prn_male = self.getPointByLabel(pred_male, "pred_prn_male")
                self.createLine(pred_prn_male, true_prn, "error_prn_male", [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
                error_dist = np.linalg.norm(pred_prn_male - true_prn)
                errors.append("Male pronasale error: {0:.2f} mm".format(error_dist))
                self.storeMeasurement("ERROR:  Pronasale (male)", error_dist, "mm", is_summary=True)
                
                if "Pronasale (male)" in self.all_coordinates:
                    self.all_coordinates["Pronasale (male)"]["true"] = true_prn
            
            if pred_female: 
                pred_prn_female = self.getPointByLabel(pred_female, "pred_prn_female")
                self.createLine(pred_prn_female, true_prn, "error_prn_female", [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
                error_dist = np.linalg.norm(pred_prn_female - true_prn)
                errors.append("Female pronasale error: {0:.2f} mm".format(error_dist))
                self.storeMeasurement("ERROR:  Pronasale (female)", error_dist, "mm", is_summary=True)
                
                if "Pronasale (female)" in self.all_coordinates:
                    self.all_coordinates["Pronasale (female)"]["true"] = true_prn
            
            if self.pred_FSTT_sn: 
                try:
                    pred_sn_fstt = self.getPointByLabel(self.pred_FSTT_sn, "sn'_FSTT")
                    true_sn = self.getPointByLabel(self.softTissueNode, "sn'")
                    self.createLine(pred_sn_fstt, true_sn, "error_FSTT_sn", [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
                    error_dist = np.linalg.norm(pred_sn_fstt - true_sn)
                    errors.append("FSTT sn' error: {0:.2f} mm".format(error_dist))
                    self.storeMeasurement("ERROR: FSTT sn'", error_dist, "mm", is_summary=True)
                    self.storeCoordinate("Subnasale (FSTT)", pred_sn_fstt, true_sn)
                except: 
                    pass
            
            self.step5StatusLabel.setText("Status: ✅ Errors calculated!")
            self.step5StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            self.updateResultsTables()
            
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Information)
            msg.setText("Prediction Errors Calculated")
            msg.setInformativeText("\n".join(errors))
            msg.setWindowTitle("Validation Results")
            msg.exec_()
            
        except Exception as e:
            self.step5StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step5StatusLabel. setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to calculate errors: {0}".format(str(e)))
    
    def updateResultsTables(self):
        self.updateMeasurementsTable()
        self.updateCoordinatesTable()
    
    def updateMeasurementsTable(self):
        self.measurementsTable.setRowCount(len(self.all_measurements))
        
        row = 0
        for name, data in sorted(self.all_measurements.items()):
            name_item = qt.QTableWidgetItem(name)
            name_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            value_item = qt.QTableWidgetItem("{0:.2f}".format(data["value"]))
            value_item.setFlags(qt.Qt. ItemIsEnabled | qt.Qt. ItemIsSelectable)
            
            unit_item = qt.QTableWidgetItem(data["unit"])
            unit_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            if data. get("is_summary", False):
                yellow = qt.QColor(255, 255, 200)
                name_item.setBackground(yellow)
                value_item.setBackground(yellow)
                unit_item.setBackground(yellow)
                
                font = qt.QFont()
                font.setBold(True)
                name_item.setFont(font)
                value_item.setFont(font)
                unit_item. setFont(font)
            
            self.measurementsTable. setItem(row, 0, name_item)
            self.measurementsTable.setItem(row, 1, value_item)
            self.measurementsTable.setItem(row, 2, unit_item)
            
            row += 1
        
        self.measurementsTable.resizeColumnsToContents()
    
    def updateCoordinatesTable(self):
        self.coordinatesTable.setRowCount(len(self.all_coordinates))
        
        row = 0
        for landmark_name, coords in sorted(self.all_coordinates.items()):
            name_item = qt.QTableWidgetItem(landmark_name)
            name_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            self.coordinatesTable.setItem(row, 0, name_item)
            
            pred_coords = coords["predicted"]
            true_coords = coords. get("true", None)
            
            for col, val in enumerate([pred_coords[0], pred_coords[1], pred_coords[2]]):
                item = qt.QTableWidgetItem("{0:.2f}".format(val))
                item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                self.coordinatesTable.setItem(row, col + 1, item)
            
            if true_coords is not None:
                for col, val in enumerate([true_coords[0], true_coords[1], true_coords[2]]):
                    item = qt.QTableWidgetItem("{0:.2f}".format(val))
                    item.setFlags(qt. Qt.ItemIsEnabled | qt. Qt.ItemIsSelectable)
                    item.setBackground(qt.QColor(220, 255, 220))
                    self.coordinatesTable.setItem(row, col + 4, item)
                
                error_3d = np.linalg.norm(pred_coords - true_coords)
                error_item = qt.QTableWidgetItem("{0:.2f}".format(error_3d))
                error_item.setFlags(qt. Qt.ItemIsEnabled | qt. Qt.ItemIsSelectable)
                error_item.setBackground(qt. QColor(255, 220, 220))
                font = qt.QFont()
                font.setBold(True)
                error_item.setFont(font)
                self.coordinatesTable.setItem(row, 7, error_item)
            else:
                for col in range(4, 8):
                    item = qt.QTableWidgetItem("N/A")
                    item. setFlags(qt.Qt.ItemIsEnabled)
                    self.coordinatesTable.setItem(row, col, item)
            
            row += 1
        
        self.coordinatesTable.resizeColumnsToContents()
    
    def onCopyMeasurements(self):
        try:
            if not self.all_measurements:
                slicer.util.warningDisplay("No measurements available to copy.  Please run the prediction and measurements first.")
                return
            
            export_text = "Measurement\tValue\tUnit\n"
            
            for name, data in sorted(self.all_measurements.items()):
                value_str = "{0:.2f}".format(data["value"])
                export_text += "{0}\t{1}\t{2}\n". format(name, value_str, data["unit"])
            
            qt.QApplication.clipboard().setText(export_text)
            
            self.step6StatusLabel.setText("Status: ✅ Measurements copied to clipboard!  Ready to paste into Excel.")
            slicer.util.showStatusMessage("Measurements copied!", 3000)
            
        except Exception as e:
            slicer.util.errorDisplay("Failed to copy measurements: {0}".format(str(e)))
    
    def onCopyCoordinates(self):
        """Copy coordinates table to clipboard"""
        try: 
            if not self. all_coordinates:
                slicer.util.warningDisplay("No coordinates available to copy. Please run the prediction first.")
                return
            
            # Create tab-separated values (TSV) format with headers
            export_text = "Landmark\tPredicted X\tPredicted Y\tPredicted Z\tTrue X\tTrue Y\tTrue Z\t3D Error (mm)\n"
            
            for landmark_name, coords in sorted(self. all_coordinates.items()):
                pred = coords["predicted"]
                true_coords = coords.get("true", None)
                
                if true_coords is not None: 
                    # Calculate 3D error
                    error_3d = np.linalg.norm(pred - true_coords)
                    # ✅ FIXED - NO SPACES in any format specifiers
                    export_text += "{0}\t{1:. 2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6:.2f}\t{7:.2f}\n".format(
                        landmark_name,
                        pred[0], pred[1], pred[2],
                        true_coords[0], true_coords[1], true_coords[2],
                        error_3d
                    )
                else:
                    # ✅ FIXED - NO SPACES here either
                    export_text += "{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\tN/A\tN/A\tN/A\tN/A\n".format(
                        landmark_name,
                        pred[0], pred[1], pred[2]
                    )
            
            # Copy to clipboard
            qt.QApplication.clipboard().setText(export_text)
            
            # Show success message
            self.step6StatusLabel.setText("Status: ✅ Coordinates copied to clipboard! Ready to paste into Excel.")
            slicer.util.showStatusMessage("Coordinates copied!", 3000)
            
        except Exception as e: 
            slicer.util.errorDisplay("Failed to copy coordinates: {0}".format(str(e)))
    
    def onPrevButtonClicked(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()
    
    def onNextButtonClicked(self):
        if self.currentStep < self.stepStack.count - 1:
            self.currentStep += 1
            self.updateStepUI()
    
    def updateStepUI(self):
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText("Step {0}/{1}".format(self.currentStep + 1, self.stepStack.count))
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)

# Create and show the widget
widget = PurkaitSinghGUI()
widget.show()
```
