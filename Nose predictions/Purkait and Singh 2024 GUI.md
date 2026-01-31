``` python

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
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        self.stepStack = qt.QStackedWidget()
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
            
            url = "https://github.com/user-attachments/files/21217369/PS_hard_tissue.mrk.json"
            temp_file = os.path.join(tempfile.gettempdir(), "PS_hard_tissue.mrk.json")
            
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
                self.softTissueNode = slicer.util.getNode("PS_soft_tissue")
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
        widget = qt.QWidget()
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
        
        layout.addWidget(mspGroup)
        
        fhpGroup = qt.QGroupBox("Frankfurt Horizontal Plane (FHP)")
        fhpLayout = qt.QVBoxLayout(fhpGroup)
        
        fhpDesc = qt.QLabel("Please ensure you have created your FHP before proceeding.")
        fhpDesc.setWordWrap(True)
        fhpLayout.addWidget(fhpDesc)
        
        self.fhpSelector = slicer.qMRMLNodeComboBox()
        self.fhpSelector.nodeTypes = ["vtkMRMLMarkupsPlaneNode"]
        self.fhpSelector.setMRMLScene(slicer.mrmlScene)
        self.fhpSelector.noneEnabled = True
        self.fhpSelector.selectNodeUponCreation = True
        self.fhpSelector.currentNodeChanged.connect(self.onFHPSelected)
        
        fhpFormLayout = qt.QFormLayout()
        fhpFormLayout.addRow("FHP Plane:", self.fhpSelector)
        fhpLayout.addLayout(fhpFormLayout)
        
        layout.addWidget(fhpGroup)
        
        self.step2StatusLabel = qt.QLabel("Status: Please create MSP and select FHP.")
        self.step2StatusLabel.setWordWrap(True)
        layout.addWidget(self.step2StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep3_Measurements(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 3: Create Hard Tissue Measurements")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "This will create all guide lines and measurements needed for prediction.\n\n"
            "Please set the facial soft tissue thickness (FSTT) values for predictions:"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # ============= FSTT for sn' =============
        snGroup = qt.QGroupBox("FSTT for Subnasale (sn')")
        snLayout = qt.QVBoxLayout(snGroup)

        snExplanation = qt.QLabel(
            "The FSTT at subnasale (sn') is used to predict the soft tissue position from the hard tissue landmark 'subspinale (ss)'.\n"
            "Values: Male = 11.61±1.6mm (Purkait & Singh 2024), Female = 10.27±10.62mm (Purkait & Singh 2024), "
            "Not sex-specific = 13.5±3.5mm (Hona et al.2024)"
        )
        snExplanation.setWordWrap(True)
        snExplanation.setStyleSheet("font-style: italic; color: #555;")
        snLayout.addWidget(snExplanation)

        # Tickboxes for sn'
        snSexLayout = qt.QHBoxLayout()
        self.snMaleCheckbox = qt.QCheckBox("Male")
        self.snFemaleCheckbox = qt.QCheckBox("Female")
        self.snNonSexCheckbox = qt.QCheckBox("Not sex-specific")
        self.snMaleCheckbox.setChecked(True)
        self.snMaleCheckbox.toggled.connect(self.onSnSexChanged)
        self.snFemaleCheckbox.toggled.connect(self.onSnSexChanged)
        self.snNonSexCheckbox.toggled.connect(self.onSnSexChanged)
        snSexLayout.addWidget(self.snMaleCheckbox)
        snSexLayout.addWidget(self.snFemaleCheckbox)
        snSexLayout.addWidget(self.snNonSexCheckbox)
        snSexLayout.addStretch()
        snLayout.addLayout(snSexLayout)

        # Slider for sn' (Male)
        self.snMaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.snMaleSlider.setRange(0, 100)
        self.snMaleSlider.setValue(50)
        self.snMaleSlider.valueChanged.connect(self.onSnMaleSliderChanged)

        self.snMaleLabel = qt.QLabel("FSTT sn' (Male): 11.61 mm")
        self.snMaleLabel.setStyleSheet("font-weight: bold;")
        snLayout.addWidget(self.snMaleLabel)
        snLayout.addWidget(self.snMaleSlider)

        self.snMaleRangeLabel = qt.QLabel("Range: -SD (10.01 mm) ← Mean (11.61 mm) → +SD (13.21 mm) [Adjustable beyond limits]")
        self.snMaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        snLayout.addWidget(self.snMaleRangeLabel)

        # Slider for sn' (Female)
        self.snFemaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.snFemaleSlider.setRange(0, 100)
        self.snFemaleSlider.setValue(50)
        self.snFemaleSlider.valueChanged.connect(self.onSnFemaleSliderChanged)
        self.snFemaleSlider.setVisible(False)

        self.snFemaleLabel = qt.QLabel("FSTT sn' (Female): 10.27 mm")
        self.snFemaleLabel.setStyleSheet("font-weight: bold;")
        self.snFemaleLabel.setVisible(False)
        snLayout.addWidget(self.snFemaleLabel)
        snLayout.addWidget(self.snFemaleSlider)

        self.snFemaleRangeLabel = qt.QLabel("Range: -SD (-0.35 mm) ← Mean (10.27 mm) → +SD (20.89 mm) [Adjustable beyond limits]")
        self.snFemaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.snFemaleRangeLabel.setVisible(False)
        snLayout.addWidget(self.snFemaleRangeLabel)

        # Slider for sn' (Non-sex-specific)
        self.snNonSexSlider = qt.QSlider(qt.Qt.Horizontal)
        self.snNonSexSlider.setRange(0, 100)
        self.snNonSexSlider.setValue(50)
        self.snNonSexSlider.valueChanged.connect(self.onSnNonSexSliderChanged)
        self.snNonSexSlider.setVisible(False)

        self.snNonSexLabel = qt.QLabel("FSTT sn' (Non-sex-specific): 13.50 mm")
        self.snNonSexLabel.setStyleSheet("font-weight: bold;")
        self.snNonSexLabel.setVisible(False)
        snLayout.addWidget(self.snNonSexLabel)
        snLayout.addWidget(self.snNonSexSlider)

        self.snNonSexRangeLabel = qt.QLabel("Range: -SD (10.0 mm) ← Mean (13.5 mm) → +SD (17.0 mm) [Adjustable beyond limits]")
        self.snNonSexRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.snNonSexRangeLabel.setVisible(False)
        snLayout.addWidget(self.snNonSexRangeLabel)

        layout.addWidget(snGroup)

        # ============= FSTT for n' =============
        nGroup = qt.QGroupBox("FSTT for Nasion (n')")
        nLayout = qt.QVBoxLayout(nGroup)

        nExplanation = qt.QLabel(
            "The FSTT at nasion (n') is used to predict the soft tissue position from the hard tissue landmark 'nasion (n)'.\n"
            "Values: Male = 5.02±0.99mm (Purkait & Singh 2024), Female = 3.97±0.92mm (Purkait & Singh 2024), "
            "Not sex-specific = 6.0±1.5mm (Hona et al.2024)"
        )
        nExplanation.setWordWrap(True)
        nExplanation.setStyleSheet("font-style: italic; color: #555;")
        nLayout.addWidget(nExplanation)

        # Tickboxes for n'
        nSexLayout = qt.QHBoxLayout()
        self.nMaleCheckbox = qt.QCheckBox("Male")
        self.nFemaleCheckbox = qt.QCheckBox("Female")
        self.nNonSexCheckbox = qt.QCheckBox("Not sex-specific")
        self.nMaleCheckbox.setChecked(True)
        self.nMaleCheckbox.toggled.connect(self.onNSexChanged)
        self.nFemaleCheckbox.toggled.connect(self.onNSexChanged)
        self.nNonSexCheckbox.toggled.connect(self.onNSexChanged)
        nSexLayout.addWidget(self.nMaleCheckbox)
        nSexLayout.addWidget(self.nFemaleCheckbox)
        nSexLayout.addWidget(self.nNonSexCheckbox)
        nSexLayout.addStretch()
        nLayout.addLayout(nSexLayout)

        # Slider for n' (Male)
        self.nMaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.nMaleSlider.setRange(0, 100)
        self.nMaleSlider.setValue(50)
        self.nMaleSlider.valueChanged.connect(self.onNMaleSliderChanged)

        self.nMaleLabel = qt.QLabel("FSTT n' (Male): 5.02 mm")
        self.nMaleLabel.setStyleSheet("font-weight: bold;")
        nLayout.addWidget(self.nMaleLabel)
        nLayout.addWidget(self.nMaleSlider)

        self.nMaleRangeLabel = qt.QLabel("Range: -SD (4.03 mm) ← Mean (5.02 mm) → +SD (6.01 mm) [Adjustable beyond limits]")
        self.nMaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        nLayout.addWidget(self.nMaleRangeLabel)

        # Slider for n' (Female)
        self.nFemaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.nFemaleSlider.setRange(0, 100)
        self.nFemaleSlider.setValue(50)
        self.nFemaleSlider.valueChanged.connect(self.onNFemaleSliderChanged)
        self.nFemaleSlider.setVisible(False)

        self.nFemaleLabel = qt.QLabel("FSTT n' (Female): 3.97 mm")
        self.nFemaleLabel.setStyleSheet("font-weight: bold;")
        self.nFemaleLabel.setVisible(False)
        nLayout.addWidget(self.nFemaleLabel)
        nLayout.addWidget(self.nFemaleSlider)

        self.nFemaleRangeLabel = qt.QLabel("Range: -SD (3.05 mm) ← Mean (3.97 mm) → +SD (4.89 mm) [Adjustable beyond limits]")
        self.nFemaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.nFemaleRangeLabel.setVisible(False)
        nLayout.addWidget(self.nFemaleRangeLabel)

        # Slider for n' (Non-sex-specific)
        self.nNonSexSlider = qt.QSlider(qt.Qt.Horizontal)
        self.nNonSexSlider.setRange(0, 100)
        self.nNonSexSlider.setValue(50)
        self.nNonSexSlider.valueChanged.connect(self.onNNonSexSliderChanged)
        self.nNonSexSlider.setVisible(False)

        self.nNonSexLabel = qt.QLabel("FSTT n' (Non-sex-specific): 6.00 mm")
        self.nNonSexLabel.setStyleSheet("font-weight: bold;")
        self.nNonSexLabel.setVisible(False)
        nLayout.addWidget(self.nNonSexLabel)
        nLayout.addWidget(self.nNonSexSlider)

        self.nNonSexRangeLabel = qt.QLabel("Range: -SD (4.5 mm) ← Mean (6.0 mm) → +SD (7.5 mm) [Adjustable beyond limits]")
        self.nNonSexRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.nNonSexRangeLabel.setVisible(False)
        nLayout.addWidget(self.nNonSexRangeLabel)

        layout.addWidget(nGroup)

        # ============= CREATE BUTTON =============
        self.createMeasurementsButton = qt.QPushButton("Create All Measurements")
        self.createMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px; font-weight: bold;"
        )
        self.createMeasurementsButton.clicked.connect(self.onCreateMeasurements)
        layout.addWidget(self.createMeasurementsButton)
        
        self.step3StatusLabel = qt.QLabel("Status: Ready to create measurements.")
        self.step3StatusLabel.setWordWrap(True)
        layout.addWidget(self.step3StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep4_Prediction(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 4: Predict Pronasale and nasal tip")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "Select the biological sex and visualization options, then run the prediction.\n\n"
            "Note: If you used 'Not sex-specific' FSTT values in Step 3, you must choose which "
            "prediction equation (Male or Female) to use below, as there are no sex-neutral equations available."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        sexGroup = qt.QGroupBox("Prediction Equations to Use")
        sexLayout = qt.QVBoxLayout(sexGroup)
        
        sexButtonLayout = qt.QHBoxLayout()
        self.maleRadio = qt.QRadioButton("Male")
        self.femaleRadio = qt.QRadioButton("Female")
        self.bothRadio = qt.QRadioButton("Both (for comparison)")
        self.maleRadio.setChecked(True)
        
        sexButtonLayout.addWidget(self.maleRadio)
        sexButtonLayout.addWidget(self.femaleRadio)
        sexButtonLayout.addWidget(self.bothRadio)
        sexButtonLayout.addStretch()
        sexLayout.addLayout(sexButtonLayout)
        
        noteLabel = qt.QLabel(
            "<i>These equations are used to predict pronasale (prn) and nasal tip (nt) positions."
            "They are independent of the FSTT values chosen in Step 3.</i>"
        )
        noteLabel.setWordWrap(True)
        noteLabel.setStyleSheet("color: #666; font-size: 10pt;")
        sexLayout.addWidget(noteLabel)
        
        layout.addWidget(sexGroup)
        
        self.showLinesCheckbox = qt.QCheckBox("Show visualization lines")
        self.showLinesCheckbox.setChecked(True)
        layout.addWidget(self.showLinesCheckbox)
        
        self.predictButton = qt.QPushButton("Run Predictions (Pronasale & nasal tip)")
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
        self.additionalMeasurementsButton.clicked.connect(self.onCreateAdditionalMeasurements)
        layout.addWidget(self.additionalMeasurementsButton)
        
        self.calculateErrorButton = qt.QPushButton("📊 Calculate Prediction Errors")
        self.calculateErrorButton.setStyleSheet(
            "background-color: #9b59b6; color: white; padding: 8px; font-weight: bold;"
        )
        self.calculateErrorButton.clicked.connect(self.onCalculateErrors)
        layout.addWidget(self.calculateErrorButton)
        
        self.step5StatusLabel = qt.QLabel("Status: Optional step.")
        self.step5StatusLabel.setWordWrap(True)
        layout.addWidget(self.step5StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep6_Results(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)  # Increased spacing
        layout.setContentsMargins(10, 10, 10, 10)  # Add margins around the widget
        
        title = qt.QLabel("Step 6: Results & Export")
        title.setStyleSheet("font-weight: bold; font-size: 18px; margin-bottom: 10px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)

        # ========== PREDICTION PROVENANCE REPORT ==========
        provenanceLabel = qt.QLabel("<b>📊 Prediction Provenance Report (Regression Predictions Only)</b>")
        provenanceLabel.setStyleSheet("font-size: 14px; margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(provenanceLabel)
        
        provenanceDesc = qt.QLabel(
            "Shows pronasale (prn) and nasal tip (nt) predictions only. " +
            "FSTT predictions (sn', n') are in the measurements table below."
        )
        provenanceDesc.setWordWrap(True)
        provenanceDesc.setStyleSheet("margin-bottom: 10px; color: #666; padding: 5px; background-color: #f5f5f5; border-radius: 4px;")
        layout.addWidget(provenanceDesc)
        
        self.provenanceTable = qt.QTableWidget()
        self.provenanceTable.setColumnCount(9)  # Fixed: Changed from 11 to 9
        self.provenanceTable.setHorizontalHeaderLabels([
            "Prediction ID", 
            "Landmark",
            "Reg Eq",
            "Method Combo",
            "Pred X", "Pred Y", "Pred Z",
            "3D Error (mm)",
            "Error Status"
        ])
        
        # Set column width strategies
        header = self.provenanceTable.horizontalHeader()
        header.setSectionResizeMode(0, qt.QHeaderView.Interactive)  # ID - adjustable
        header.setSectionResizeMode(1, qt.QHeaderView.ResizeToContents)  # Landmark
        header.setSectionResizeMode(2, qt.QHeaderView.ResizeToContents)  # Reg Eq
        header.setSectionResizeMode(3, qt.QHeaderView.Interactive)  # Method Combo
        for col in range(4, 7):  # Coordinate columns
            header.setSectionResizeMode(col, qt.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, qt.QHeaderView.ResizeToContents)  # 3D Error
        header.setSectionResizeMode(8, qt.QHeaderView.ResizeToContents)  # Error Status
        
        # Set reasonable widths
        self.provenanceTable.setColumnWidth(0, 120)  # Prediction ID
        self.provenanceTable.setColumnWidth(1, 70)   # Landmark
        self.provenanceTable.setColumnWidth(2, 60)   # Reg Eq
        self.provenanceTable.setColumnWidth(3, 150)  # Method Combo (wider)
        for col in range(4, 7):  # Coordinate columns
            self.provenanceTable.setColumnWidth(col, 80)
        self.provenanceTable.setColumnWidth(7, 100)   # 3D Error
        self.provenanceTable.setColumnWidth(8, 90)   # Error Status
        
        self.provenanceTable.setMinimumHeight(200)
        self.provenanceTable.setMaximumHeight(300)  # Limit height
        self.provenanceTable.setAlternatingRowColors(True)
        self.provenanceTable.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        layout.addWidget(self.provenanceTable)
        
        # Add spacer between tables
        spacer1 = qt.QLabel()
        spacer1.setFixedHeight(15)
        layout.addWidget(spacer1)
        
        # ========== MEASUREMENTS TABLE ==========
        measurementsLabel = qt.QLabel("<b>📏 Key Measurements & Validation</b>")
        measurementsLabel.setStyleSheet("font-size: 14px; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(measurementsLabel)

        instructionsLabel = qt.QLabel(
            "<b>Methodology Note:</b> Bony sn = subspinale (ss) = orthodontic point A. " +
            "FSTT at sn' = distance from ss to sn'.<br>" +
            "<b>Highlighting:</b> Errors in <span style='background-color: #ffeaea;'>red</span>, " +
            "key measurements in <span style='background-color: #ffffcc;'>yellow</span>."
        )
        instructionsLabel.setWordWrap(True)
        instructionsLabel.setStyleSheet("margin-bottom: 10px; color: #666; padding: 5px; background-color: #f5f5f5; border-radius: 4px;")
        layout.addWidget(instructionsLabel)
        
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable.setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Value", "Unit"])
        
        # Set column widths
        measurementsHeader = self.measurementsTable.horizontalHeader()
        measurementsHeader.setSectionResizeMode(0, qt.QHeaderView.Stretch)  # Name stretches
        measurementsHeader.setSectionResizeMode(1, qt.QHeaderView.Fixed)    # Value fixed width
        measurementsHeader.setSectionResizeMode(2, qt.QHeaderView.Fixed)    # Unit fixed width
        
        self.measurementsTable.setColumnWidth(1, 100)  # Value column
        self.measurementsTable.setColumnWidth(2, 60)   # Unit column
        
        self.measurementsTable.setMinimumHeight(200)
        self.measurementsTable.setMaximumHeight(300)  # Limit height
        self.measurementsTable.setAlternatingRowColors(True)
        self.measurementsTable.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        layout.addWidget(self.measurementsTable)
        
        # Add spacer between tables
        spacer2 = qt.QLabel()
        spacer2.setFixedHeight(15)
        layout.addWidget(spacer2)
        
        # ========== COORDINATES TABLE ==========
        coordinatesLabel = qt.QLabel("<b>📍 Coordinates Comparison (Predicted vs True)</b>")
        coordinatesLabel.setStyleSheet("font-size: 14px; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(coordinatesLabel)
        
        coordDesc = qt.QLabel("3D positions in RAS coordinate system (Right, Anterior, Superior)")
        coordDesc.setWordWrap(True)
        coordDesc.setStyleSheet("margin-bottom: 10px; color: #666; padding: 5px; background-color: #f5f5f5; border-radius: 4px;")
        layout.addWidget(coordDesc)
        
        self.coordinatesTable = qt.QTableWidget()
        self.coordinatesTable.setColumnCount(8)
        self.coordinatesTable.setHorizontalHeaderLabels([
            "Landmark", 
            "Pred X", "Pred Y", "Pred Z",
            "True X", "True Y", "True Z",
            "3D Error"
        ])
        
        # Set column widths
        coordHeader = self.coordinatesTable.horizontalHeader()
        coordHeader.setSectionResizeMode(0, qt.QHeaderView.Interactive)  # Landmark - adjustable
        for col in range(1, 7):  # Coordinate columns
            coordHeader.setSectionResizeMode(col, qt.QHeaderView.Fixed)
        coordHeader.setSectionResizeMode(7, qt.QHeaderView.Fixed)  # 3D Error
        
        # Set reasonable widths
        self.coordinatesTable.setColumnWidth(0, 150)  # Landmark
        for col in range(1, 7):  # Coordinate columns (1-6)
            self.coordinatesTable.setColumnWidth(col, 80)
        self.coordinatesTable.setColumnWidth(7, 90)  # 3D Error
        
        self.coordinatesTable.setMinimumHeight(150)
        self.coordinatesTable.setMaximumHeight(250)  # Limit height
        self.coordinatesTable.setAlternatingRowColors(True)
        self.coordinatesTable.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        layout.addWidget(self.coordinatesTable)
        
        # ========== BUTTONS ==========
        buttonLayout = qt.QHBoxLayout()
        buttonLayout.setSpacing(10)  # Add spacing between buttons
        
        self.copyMeasurementsButton = qt.QPushButton("📋 Copy Measurements")
        self.copyMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px; font-weight: bold; min-width: 150px;"
        )
        self.copyMeasurementsButton.setToolTip("Copy measurements table to clipboard")
        self.copyMeasurementsButton.clicked.connect(self.onCopyMeasurements)
        buttonLayout.addWidget(self.copyMeasurementsButton)
        
        self.copyCoordinatesButton = qt.QPushButton("📋 Copy Coordinates")
        self.copyCoordinatesButton.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px; font-weight: bold; min-width: 150px;"
        )
        self.copyCoordinatesButton.setToolTip("Copy coordinates table to clipboard")
        self.copyCoordinatesButton.clicked.connect(self.onCopyCoordinates)
        buttonLayout.addWidget(self.copyCoordinatesButton)
        
        self.copyProvenanceButton = qt.QPushButton("📋 Copy Provenance")
        self.copyProvenanceButton.setStyleSheet(
            "background-color: #9b59b6; color: white; padding: 8px; font-weight: bold; min-width: 150px;"
        )
        self.copyProvenanceButton.setToolTip("Copy provenance table to clipboard")
        self.copyProvenanceButton.clicked.connect(self.onCopyProvenance)
        buttonLayout.addWidget(self.copyProvenanceButton)
        
        buttonLayout.addStretch(1)  # Push the finish button to the right
        
        self.finishButton = qt.QPushButton("Finish")
        self.finishButton.setStyleSheet("padding: 8px; min-width: 100px;")
        self.finishButton.clicked.connect(lambda: self.close())
        buttonLayout.addWidget(self.finishButton)
        
        layout.addLayout(buttonLayout)
        
        # Add a stretch at the end to push everything up
        layout.addStretch(1)
        
        self.step6StatusLabel = qt.QLabel("Status: Review results above.")
        self.step6StatusLabel.setWordWrap(True)
        self.step6StatusLabel.setStyleSheet("margin-top: 15px; color: #666; padding: 5px;")
        layout.addWidget(self.step6StatusLabel)
        
        # Make the widget scrollable
        scrollArea = qt.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widget)
        
        container = qt.QWidget()
        containerLayout = qt.QVBoxLayout(container)
        containerLayout.addWidget(scrollArea)
        
        self.stepStack.addWidget(container)


    # ==================== SLIDER HELPER METHODS ====================

    def onSnSexChanged(self):
        """Handle sn' sex checkbox changes"""
        maleChecked = self.snMaleCheckbox.isChecked()
        femaleChecked = self.snFemaleCheckbox.isChecked()
        nonSexChecked = self.snNonSexCheckbox.isChecked()
        
        # Show/hide male slider
        self.snMaleSlider.setVisible(maleChecked)
        self.snMaleLabel.setVisible(maleChecked)
        self.snMaleRangeLabel.setVisible(maleChecked)
        
        # Show/hide female slider
        self.snFemaleSlider.setVisible(femaleChecked)
        self.snFemaleLabel.setVisible(femaleChecked)
        self.snFemaleRangeLabel.setVisible(femaleChecked)
        
        # Show/hide non-sex-specific slider
        self.snNonSexSlider.setVisible(nonSexChecked)
        self.snNonSexLabel.setVisible(nonSexChecked)
        self.snNonSexRangeLabel.setVisible(nonSexChecked)

    def onNSexChanged(self):
        """Handle n' sex checkbox changes"""
        maleChecked = self.nMaleCheckbox.isChecked()
        femaleChecked = self.nFemaleCheckbox.isChecked()
        nonSexChecked = self.nNonSexCheckbox.isChecked()
        
        # Show/hide male slider
        self.nMaleSlider.setVisible(maleChecked)
        self.nMaleLabel.setVisible(maleChecked)
        self.nMaleRangeLabel.setVisible(maleChecked)
        
        # Show/hide female slider
        self.nFemaleSlider.setVisible(femaleChecked)
        self.nFemaleLabel.setVisible(femaleChecked)
        self.nFemaleRangeLabel.setVisible(femaleChecked)
        
        # Show/hide non-sex-specific slider
        self.nNonSexSlider.setVisible(nonSexChecked)
        self.nNonSexLabel.setVisible(nonSexChecked)
        self.nNonSexRangeLabel.setVisible(nonSexChecked)

    def onSnMaleSliderChanged(self, value):
        """Update sn' male FSTT value based on slider"""
        mean = 11.61
        sd = 1.6
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.snMaleLabel.setText("FSTT sn' (Male): {:.2f} mm".format(fstt_value))

    def onSnFemaleSliderChanged(self, value):
        """Update sn' female FSTT value based on slider"""
        mean = 10.27
        sd = 10.62
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.snFemaleLabel.setText("FSTT sn' (Female): {:.2f} mm".format(fstt_value))

    def onSnNonSexSliderChanged(self, value):
        """Update sn' non-sex-specific FSTT value based on slider"""
        mean = 13.5
        sd = 3.5
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.snNonSexLabel.setText("FSTT sn' (Non-sex-specific): {:.2f} mm".format(fstt_value))

    def onNMaleSliderChanged(self, value):
        """Update n' male FSTT value based on slider"""
        mean = 5.02
        sd = 0.99
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.nMaleLabel.setText("FSTT n' (Male): {:.2f} mm".format(fstt_value))

    def onNFemaleSliderChanged(self, value):
        """Update n' female FSTT value based on slider"""
        mean = 3.97
        sd = 0.92
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.nFemaleLabel.setText("FSTT n' (Female): {:.2f} mm".format(fstt_value))

    def onNNonSexSliderChanged(self, value):
        """Update n' non-sex-specific FSTT value based on slider"""
        mean = 6.0
        sd = 1.5
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.nNonSexLabel.setText("FSTT n' (Non-sex-specific): {:.2f} mm".format(fstt_value))

    def updateProvenanceTable(self):
        """Update the provenance report table - NOW ONLY SHOWS REGRESSION PREDICTIONS"""
        if not hasattr(self, 'lmrk_predictions') or not self.lmrk_predictions:
            return
        
        # Count rows: each prediction has prn and possibly nt
        row_count = 0
        for prediction in self.lmrk_predictions.values():
            row_count += 1  # prn
            if prediction['nt'] is not None:
                row_count += 1  # nt
        
        self.provenanceTable.setRowCount(row_count)
        
        row = 0
        # Add ONLY regression predictions (prn and nt)
        for pred_id, pred_data in sorted(self.lmrk_predictions.items()):
            # Add prn row
            self.addProvenanceRow(row, pred_id, 'prn', pred_data)
            row += 1
            
            # Add nt row if exists
            if pred_data['nt'] is not None:
                self.addProvenanceRow(row, pred_id, 'nt', pred_data)
                row += 1
        
        self.provenanceTable.resizeColumnsToContents()

    def getSnFSTTValue(self, method):
        """Get the FSTT value for sn' based on method"""
        if method == 'PS_M':
            mean = 11.61
            sd = 1.6
            slider_value = self.snMaleSlider.value   
            return mean + ((slider_value - 50) / 25.0) * sd
        elif method == 'PS_F':
            mean = 10.27
            sd = 10.62
            slider_value = self.snFemaleSlider.value   
            return mean + ((slider_value - 50) / 25.0) * sd
        elif method == 'Hona':
            mean = 13.5
            sd = 3.5
            slider_value = self.snNonSexSlider.value   
            return mean + ((slider_value - 50) / 25.0) * sd
        return None

    def getNFSTTValue(self, method):
        """Get the FSTT value for n' based on method"""
        if method == 'PS_M':
            mean = 5.02
            sd = 0.99
            slider_value = self.nMaleSlider.value   
            return mean + ((slider_value - 50) / 25.0) * sd
        elif method == 'PS_F':
            mean = 3.97
            sd = 0.92
            slider_value = self.nFemaleSlider.value   
            return mean + ((slider_value - 50) / 25.0) * sd
        elif method == 'Hona':
            mean = 6.0
            sd = 1.5
            slider_value = self.nNonSexSlider.value   
            return mean + ((slider_value - 50) / 25.0) * sd
        return None

    def getNFSTT(self):
        """Get all selected n' FSTT values as a dictionary {method: value}"""
        n_fstt_values = {}
        if self.nMaleCheckbox.isChecked():
            mean = 5.02
            sd = 0.99
            slider_value = self.nMaleSlider.value
            fstt_value = mean + ((slider_value - 50) / 25.0) * sd
            n_fstt_values['PS_M'] = fstt_value
        
        if self.nFemaleCheckbox.isChecked():
            mean = 3.97
            sd = 0.92
            slider_value = self.nFemaleSlider.value   
            fstt_value = mean + ((slider_value - 50) / 25.0) * sd
            n_fstt_values['PS_F'] = fstt_value
        
        if self.nNonSexCheckbox.isChecked():
            mean = 6.0
            sd = 1.5
            slider_value = self.nNonSexSlider.value   
            fstt_value = mean + ((slider_value - 50) / 25.0) * sd
            n_fstt_values['Hona'] = fstt_value
        
        return n_fstt_values

    def getSnFSTT(self):
        """Get all selected sn' FSTT values as a dictionary {method: value}"""
        sn_fstt_values = {}
        if self.snMaleCheckbox.isChecked():
            mean = 11.61
            sd = 1.6
            slider_value = self.snMaleSlider.value   
            fstt_value = mean + ((slider_value - 50) / 25.0) * sd
            sn_fstt_values['PS_M'] = fstt_value
        
        if self.snFemaleCheckbox.isChecked():
            mean = 10.27
            sd = 10.62
            slider_value = self.snFemaleSlider.value   
            fstt_value = mean + ((slider_value - 50) / 25.0) * sd
            sn_fstt_values['PS_F'] = fstt_value
        
        if self.snNonSexCheckbox.isChecked():
            mean = 13.5
            sd = 3.5
            slider_value = self.snNonSexSlider.value   
            fstt_value = mean + ((slider_value - 50) / 25.0) * sd
            sn_fstt_values['Hona'] = fstt_value
        
        return sn_fstt_values
    
    
    def addProvenanceRow(self, row, pred_id, landmark_type, pred_data):
        """Add a row to the provenance table - SIMPLIFIED VERSION"""
        # Prediction ID
        id_item = qt.QTableWidgetItem(pred_id)
        id_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.provenanceTable.setItem(row, 0, id_item)
        
        # Landmark type
        landmark_item = qt.QTableWidgetItem(landmark_type)
        landmark_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.provenanceTable.setItem(row, 1, landmark_item)
        
        # Regression Equation
        reg_item = qt.QTableWidgetItem(str(pred_data.get('regression_sex', 'N/A')))
        reg_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.provenanceTable.setItem(row, 2, reg_item)
        
        # Method Combination (sn_FSTT + n_FSTT)
        sn_method = pred_data.get('sn_FSTT_method', 'N/A')
        n_method = pred_data.get('n_FSTT_method', 'N/A')
        combo_item = qt.QTableWidgetItem(f"sn: {sn_method}, n': {n_method}")
        combo_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        self.provenanceTable.setItem(row, 3, combo_item)
        
        # Predicted Coordinates
        if landmark_type == 'prn':
            coords = pred_data.get('prn')
        else:  # nt
            coords = pred_data.get('nt')
        
        if coords is not None:
            for col, coord in enumerate([coords[0], coords[1], coords[2]]):
                coord_item = qt.QTableWidgetItem(f"{coord:.2f}")
                coord_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                self.provenanceTable.setItem(row, 4 + col, coord_item)
        else:
            for col in range(3):
                coord_item = qt.QTableWidgetItem("N/A")
                coord_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                self.provenanceTable.setItem(row, 4 + col, coord_item)
        
        # 3D Error
        error_item = qt.QTableWidgetItem()
        error_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        
        # Get true coordinates and calculate error
        if coords is not None and self.softTissueNode:
            true_coords = self.getTrueCoordinatesFromSoftTissue(landmark_type)
            if true_coords is not None:
                error_3d = np.linalg.norm(coords - true_coords)
                error_item.setText(f"{error_3d:.2f}")
                
                # Color code based on error magnitude
                if error_3d > 5.0:
                    error_item.setBackground(qt.QColor(255, 200, 200))
                    error_item.setForeground(qt.QColor(255, 0, 0))
                elif error_3d > 2.0:
                    error_item.setBackground(qt.QColor(255, 255, 200))
                    error_item.setForeground(qt.QColor(255, 140, 0))
                else:
                    error_item.setBackground(qt.QColor(200, 255, 200))
                    error_item.setForeground(qt.QColor(0, 128, 0))
            else:
                error_item.setText("N/A")
        else:
            error_item.setText("N/A")
        
        self.provenanceTable.setItem(row, 7, error_item)
        
        # Error Status
        status_item = qt.QTableWidgetItem()
        status_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        
        error_text = error_item.text()
        if error_text != "N/A":
            error_val = float(error_text)
            if error_val > 5.0:
                status_item.setText("High")
                status_item.setBackground(qt.QColor(255, 150, 150))
                status_item.setForeground(qt.QColor(255, 0, 0))
            elif error_val > 2.0:
                status_item.setText("Moderate")
                status_item.setBackground(qt.QColor(255, 255, 150))
                status_item.setForeground(qt.QColor(255, 140, 0))
            else:
                status_item.setText("Low")
                status_item.setBackground(qt.QColor(150, 255, 150))
                status_item.setForeground(qt.QColor(0, 128, 0))
        else:
            status_item.setText("N/A")
        
        self.provenanceTable.setItem(row, 8, status_item)
    
    def formatProvenanceRow(self, pred_id, landmark_type, pred_data):
        """Format a provenance row for export with True values and errors"""
        if landmark_type == 'prn':
            coords = pred_data.get('prn')
        else:
            coords = pred_data.get('nt')
        
        row = f"{pred_id}\t{landmark_type}\t"
        row += f"{pred_data.get('sn_FSTT_method', 'N/A')}\t"
        
        sn_value = pred_data.get('sn_fstt_value')
        row += f"{sn_value:.2f}\t" if sn_value is not None else "N/A\t"
        
        row += f"{pred_data.get('n_FSTT_method', 'N/A')}\t"
        
        n_value = pred_data.get('n_fstt_value')
        row += f"{n_value:.2f}\t" if n_value is not None else "N/A\t"
        
        row += f"{pred_data.get('regression_sex', 'N/A')}\t"
        
        # Predicted coordinates
        if coords is not None:
            row += f"{coords[0]:.2f}\t{coords[1]:.2f}\t{coords[2]:.2f}\t"
        else:
            row += "N/A\tN/A\tN/A\t"
        
        # True coordinates and error
        if coords is not None and self.softTissueNode:
            true_coords = self.getTrueCoordinatesFromSoftTissue(landmark_type)
            if true_coords is not None:
                error_3d = np.linalg.norm(coords - true_coords)
                row += f"{true_coords[0]:.2f}\t{true_coords[1]:.2f}\t{true_coords[2]:.2f}\t"
                row += f"{error_3d:.2f}\n"
            else:
                row += "N/A\tN/A\tN/A\tN/A\n"
        else:
            row += "N/A\tN/A\tN/A\tN/A\n"
        
        return row
    
    def onCopyProvenance(self):
        """Copy provenance table to clipboard - FIXED"""
        try:
            if self.provenanceTable.rowCount == 0:  # Fixed: property, not method
                slicer.util.warningDisplay("No provenance data available to copy.")
                return
            
            # Create tab-separated values (TSV) format
            export_text = "\t".join([
                "Prediction ID", "Landmark", "Reg Eq", "Method Combo",
                "Pred X", "Pred Y", "Pred Z", "3D Error (mm)", "Error Status"
            ]) + "\n"
            
            for row in range(self.provenanceTable.rowCount):  # Fixed: property, not method
                row_data = []
                for col in range(self.provenanceTable.columnCount):  # Fixed: property, not method
                    item = self.provenanceTable.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                export_text += "\t".join(row_data) + "\n"
            
            # Copy to clipboard
            qt.QApplication.clipboard().setText(export_text)
            
            self.step6StatusLabel.setText("Status: ✅ Provenance copied to clipboard!")
            slicer.util.showStatusMessage("Provenance table copied!", 3000)
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to copy provenance: {str(e)}")

    def findCircleIntersections(self, center1, radius1, center2, radius2):
        """
        Find intersection points of two circles in 3D space.
        For 3D, we need to constrain to the plane containing both centers and perpendicular to MSP.
        Returns the two intersection points (or one if circles are tangent, or None if no intersection)
        """
        d = np.linalg.norm(center2 - center1)
        
        # Check if circles intersect
        if d > radius1 + radius2:  # Circles too far apart
            print("Warning: Circles don't intersect (too far).Distance: {:.2f}, Sum of radii: {:.2f}".format(d, radius1 + radius2))
            return None
        if d < abs(radius1 - radius2):  # One circle inside the other
            print("Warning: One circle is inside the other")
            return None
        if d == 0 and radius1 == radius2:  # Same circle
            print("Warning: Circles are identical")
            return None
        
        # Calculate the intersection points
        # Point P on the line between centers
        a = (radius1**2 - radius2**2 + d**2) / (2 * d)
        h = np.sqrt(radius1**2 - a**2)
        
        # Direction from center1 to center2
        direction = (center2 - center1) / d
        
        # Point P (on line between centers)
        P = center1 + a * direction
        
        # We need a perpendicular direction to find the two intersection points
        # Get MSP normal to constrain the solution
        if self.mspNode:
            msp_origin, msp_normal = self.getPlaneData(self.mspNode)
            # Perpendicular direction in the plane perpendicular to line center1-center2
            # and considering MSP orientation
            perp = np.cross(direction, msp_normal)
            perp = perp / np.linalg.norm(perp)
        else:
            # Fallback: use arbitrary perpendicular
            if abs(direction[2]) < 0.9:
                perp = np.array([0, 0, 1])
            else:
                perp = np.array([1, 0, 0])
            perp = np.cross(direction, perp)
            perp = perp / np.linalg.norm(perp)
        
        # Two intersection points
        intersection1 = P + h * perp
        intersection2 = P - h * perp
        
        return intersection1, intersection2

    def selectBestNtIntersection(self, intersection1, intersection2, n_soft):
        """
        Select the best nt intersection point.
        Choose the one that is more INFERIOR (lower Z value in RAS) and more ANTERIOR (higher Y)
        The nasal tip should be below the nasion, not above it.
        """
        if intersection1 is None:
            return None
        
        if intersection2 is None:
            return intersection1
        
        # In RAS coordinates:
        # - Anterior is positive Y (we want this)
        # - Superior is positive Z (we want NEGATIVE/lower for inferior)
        
        # Primary criterion: Choose the more inferior point (lower Z = downward)
        # Secondary criterion: If similar Z, choose more anterior (higher Y)
        
        z_diff = abs(intersection1[2] - intersection2[2])
        
        if z_diff > 1.0:  # Significant Z difference (> 1mm)
            # Choose the LOWER point (more inferior/downward)
            if intersection1[2] < intersection2[2]:
                print("Selected intersection 1 (more inferior): Z={0:.2f}".format(intersection1[2]))
                return intersection1
            else:
                print("Selected intersection 2 (more inferior): Z={0:.2f}".format(intersection2[2]))
                return intersection2
        else:
            # Z values are similar, use anterior position as tiebreaker
            if intersection1[1] > intersection2[1]:  # Y coordinate (anterior)
                print("Selected intersection 1 (more anterior): Y={0:.2f}, Z={1:.2f}".format(intersection1[1], intersection1[2]))
                return intersection1
            else:
                print("Selected intersection 2 (more anterior): Y={0:.2f}, Z={1:.2f}".format(intersection2[1], intersection2[2]))
                return intersection2

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
            node = slicer.util.getFirstNodeByName(name)
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
                    self.softTissueSelector.setCurrentNode(node)
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
            print("No existing nodes detected. Please load or create landmarks.")
    
    # ==================== HELPER METHODS ====================
    
    def getPoint(self, node, index):
        point = [0, 0, 0]
        node.GetNthControlPointPosition(index, point)
        return np.array(point)
    
    def getPointByLabel(self, node, label):
        for i in range(node.GetNumberOfControlPoints()):
            if node.GetNthControlPointLabel(i) == label:
                return self.getPoint(node, i)
        raise ValueError("Point '{0}' not found".format(label))
    
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
            displayNode.SetColor(*color)
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
    
    def getTrueCoordinatesFromSoftTissue(self, landmark_name):
        """Extract true coordinates from PS_soft_tissue node based on landmark name"""
        if not self.softTissueNode:
            return None
        
        # Map of prediction names to true landmark names in PS_soft_tissue
        landmark_mapping = {
            # prn predictions
            'prn': 'prn',
            # nt predictions  
            'nt': 'nt',
            # sn' predictions
            'sn_pred': "sn'",
            # n' predictions
            "n'_pred": "n'",
            # Other soft tissue landmarks
            "n'": "n'",
            "sn'": "sn'",
            "rhi'": "rhi'",
            "alL": "alL",
            "alR": "alR",
            "nbL": "nbL",
            "nbR": "nbR"
        }
        
        # Try to find the true landmark
        for pred_key, true_key in landmark_mapping.items():
            if pred_key in landmark_name:
                try:
                    return self.getPointByLabel(self.softTissueNode, true_key)
                except ValueError:
                    continue
        
        # If not found by mapping, try direct lookup
        try:
            # Remove method suffixes to get base landmark name
            base_name = landmark_name
            for suffix in ['_PS_M', '_PS_F', '_Hona', '_male', '_female']:
                if suffix in base_name:
                    base_name = base_name.split(suffix)[0]
            
            # Try to get the point
            return self.getPointByLabel(self.softTissueNode, base_name)
        except ValueError:
            return None
    
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
            self.step1StatusLabel.setText("Status: ✅ Selected '{0}'.".format(node.GetName()))
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
            self.step5StatusLabel.setText("Status: ✅ Selected '{0}'.".format(node.GetName()))
            self.step5StatusLabel.setStyleSheet("color: green; font-weight: bold;")
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
            self.step2StatusLabel.setText("Status: MSP created. ⚠️ Please select FHP plane.")
            self.step2StatusLabel.setStyleSheet("color: orange; font-weight: bold;")
        elif self.fhpNode:
            self.step2StatusLabel.setText("Status: FHP selected.⚠️ Please create MSP.")
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
            self.mspNode.SetNormalWorld(normal)
            
            self.updateStep2Status()
            slicer.util.showStatusMessage("✅ MSP created successfully!", 3000)
            print("✅ MSP created from landmarks")
            
        except Exception as e:
            self.step2StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step2StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create MSP:  {0}".format(str(e)))
    
    def onCreateMeasurements(self):
        try:
            print("DEBUG: Starting onCreateMeasurements")
            
            if not all([self.hardTissueNode, self.mspNode, self.fhpNode]):
                raise ValueError("Please complete previous steps first.")
            
            print("DEBUG: Step 1 - Getting n_fstt_values")
            n_fstt_values = self.getNFSTT()
            print(f"DEBUG: n_fstt_values = {n_fstt_values}")
            
            print("DEBUG: Step 2 - Getting sn_fstt_values")
            sn_fstt_values = self.getSnFSTT()
            print(f"DEBUG: sn_fstt_values = {sn_fstt_values}")
            
            print("DEBUG: Step 3 - Setting status label")
            self.step3StatusLabel.setText("Status: Creating measurements...")
            slicer.app.processEvents()
            
            print("DEBUG: Step 4 - Getting plane data")
            msp_origin, msp_normal = self.getPlaneData(self.mspNode)
            fhp_origin, fhp_normal = self.getPlaneData(self.fhpNode)
            
            self.step3StatusLabel.setText("Status: Creating measurements...")
            slicer.app.processEvents()
            
            msp_origin, msp_normal = self.getPlaneData(self.mspNode)
            fhp_origin, fhp_normal = self.getPlaneData(self.fhpNode)
            
            line_direction = np.cross(msp_normal, fhp_normal)
            line_direction = line_direction / np.linalg.norm(line_direction)
            
            length = 70.0
            half_vec = 0.5 * length * line_direction
            fhp_start = msp_origin - half_vec
            fhp_end = msp_origin + half_vec
            
            self.createLine(fhp_start, fhp_end, 'FHP guide', [1.0, 1.0, 1.0], [1.0, 0.0, 0.0])
            
            guide_names = ['st n guide', 'st rhi guide', 'st sn guide']
            guide_colors = {
                'st n guide': ([1.0, 1.0, 1.0], [0.0, 1.0, 0.0]),
                'st rhi guide': ([1.0, 1.0, 1.0], [0.0, 0.0, 1.0]),
                'st sn guide': ([1.0, 1.0, 1.0], [1.0, 1.0, 0.0])
            }
            
            for i, name in enumerate(guide_names):
                landmark_pos = self.getPoint(self.hardTissueNode, i)
                start = landmark_pos - half_vec
                end = landmark_pos + half_vec
                self.createLine(start, end, name, *guide_colors[name])
            
            # ============= CREATE UNIFIED FSTT PREDICTION NODE =============
            # Create or clear FSTT_pred node BEFORE using it
            fstt_pred_node = slicer.util.getFirstNodeByName('FSTT_pred')
            if fstt_pred_node:
                slicer.mrmlScene.RemoveNode(fstt_pred_node)
            fstt_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'FSTT_pred')
            
            # Set display properties
            displayNode = fstt_pred_node.GetDisplayNode()
            if displayNode:
                displayNode.SetColor(0.0, 0.8, 0.0)  # Green
                displayNode.SetSelectedColor(1.0, 0.0, 0.0)
                displayNode.SetGlyphScale(1.8)
                displayNode.SetTextScale(3.0)
                displayNode.SetSliceProjection(True)
            
            # ============= PREDICT NASION (n') FOR ALL SELECTED METHODS =============
            n_fstt_values = self.getNFSTT()  # Returns dict with keys 'PS_M', 'PS_F', 'Hona'

            # Get the st n guide line
            st_n_guide = slicer.util.getNode('st n guide')
            n_guide_start = self.getPoint(st_n_guide, 0)
            n_guide_end = self.getPoint(st_n_guide, 1)

            # Compute the guide vector for direction
            n_guide_vec = n_guide_end - n_guide_start
            n_guide_unit_vec = n_guide_vec / np.linalg.norm(n_guide_vec)

            # Ensure the guide_unit_vec points anteriorly (positive Y in RAS)
            if n_guide_unit_vec[1] < 0:
                n_guide_unit_vec = -n_guide_unit_vec

            # Get nasion point (hard tissue)
            n_point = self.getPoint(self.hardTissueNode, 0)

            for method, n_thickness in n_fstt_values.items():
                # Predict n' by moving anteriorly from nasion
                pred_n_position = n_point + n_guide_unit_vec * n_thickness
                
                # Determine label based on method
                if method == 'PS_M':
                    label = "n'_pred_PS_M"
                elif method == 'PS_F':
                    label = "n'_pred_PS_F"
                else:  # Hona
                    label = "n'_pred_Hona"
                
                # Add to FSTT_pred node
                fstt_pred_node.AddControlPoint(pred_n_position.tolist(), label)
                
                # Store measurement and coordinate
                method_name = method
                self.storeMeasurement("Predicted n' FSTT ({0})".format(method_name), n_thickness, "mm")
                self.storeCoordinate("n' ({0})".format(label), pred_n_position)

            print("✅ Created n' predictions for methods: {0}".format(list(n_fstt_values.keys())))

            # ============= PREDICT SUBNASALE (sn') FOR ALL SELECTED METHODS =============
            # Get sn' FSTT values for all selected methods
            sn_fstt_values = self.getSnFSTT()  # Returns dict with keys 'PS_M', 'PS_F', 'Hona'

            # Get the st sn guide line and direction
            st_sn_guide = slicer.util.getNode('st sn guide')
            sn_guide_start = self.getPoint(st_sn_guide, 0)
            sn_guide_end = self.getPoint(st_sn_guide, 1)

            # Get hard tissue landmark (ss - subspinale)
            ss_point = self.getPoint(self.hardTissueNode, 2)

            # For each selected sn FSTT method, compute the predicted sn' position
            for method, sn_thickness in sn_fstt_values.items():
                # The predicted sn' should be ANTERIOR (positive Y) from the hard tissue point
                pred_sn_position = ss_point.copy()
                pred_sn_position[1] += sn_thickness  # Move anterior by FSTT value
                
                # Determine label based on method
                if method == 'PS_M':
                    label = "sn_pred_PS_M"
                elif method == 'PS_F':
                    label = "sn_pred_PS_F"
                else:  # Hona
                    label = "sn_pred_Hona"
                
                # Add to FSTT_pred node (already created above)
                fstt_pred_node.AddControlPoint(pred_sn_position.tolist(), label)
                
                # Store measurement and coordinate
                method_name = method
                self.storeMeasurement("Predicted sn' FSTT ({0})".format(method_name), sn_thickness, "mm")
                self.storeCoordinate("sn ({0})".format(label), pred_sn_position)

            print("✅ Created sn' predictions for methods: {0}".format(list(sn_fstt_values.keys())))
            
            # ============= CREATE OTHER MEASUREMENTS =============
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
            import traceback
            traceback.print_exc()  # This will print the full traceback
            self.step3StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step3StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create measurements: {0}".format(str(e)))
    
    def runSinglePrediction(self, regression_sex):
        """
        Predict pronasale and nasal tip for given regression sex
        Uses all available FSTT combinations from FSTT_pred node
        """
        # Get all FSTT predictions from the unified node
        fstt_pred_node = slicer.util.getFirstNodeByName('FSTT_pred')
        if not fstt_pred_node:
            raise ValueError("FSTT_pred node not found.Please run Step 3 first.")
        
        # Group FSTT predictions by type
        fstt_points = {
            'sn': {},
            'n_prime': {}
        }
        
        # Extract all points from FSTT_pred node
        for i in range(fstt_pred_node.GetNumberOfControlPoints()):
            label = fstt_pred_node.GetNthControlPointLabel(i)
            point = self.getPoint(fstt_pred_node, i)
            
            if 'sn_pred' in label:
                # Extract method name from label (e.g., "sn_pred_PS_M" -> "PS_M")
                method = label.replace('sn_pred_', '')
                fstt_points['sn'][method] = point
            elif "n'_pred" in label:
                # Extract method name from label (e.g., "n'_pred_PS_M" -> "PS_M")
                method = label.replace("n'_pred_", '')
                fstt_points['n_prime'][method] = point
        
        print("Found FSTT points: sn={0}, n'={1}".format(
            list(fstt_points['sn'].keys()), list(fstt_points['n_prime'].keys())
        ))
        
        # Get all combinations of sn and n' methods
        sn_methods = list(fstt_points['sn'].keys())
        n_methods = list(fstt_points['n_prime'].keys())
        
        if not sn_methods or not n_methods:
            raise ValueError("No FSTT predictions found.Please check Step 3.")
        
        # Create or clear unified lmrk_predictions node
        lmrk_pred_node = slicer.util.getFirstNodeByName('lmrk_predictions')
        if lmrk_pred_node:
            slicer.mrmlScene.RemoveNode(lmrk_pred_node)
        lmrk_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'lmrk_predictions')
        
        # Set display properties based on regression sex
        displayNode = lmrk_pred_node.GetDisplayNode()
        if displayNode:
            if regression_sex == 'male':
                displayNode.SetColor(0.0, 0.0, 0.8)  # Blue
                displayNode.SetSelectedColor(0.0, 0.0, 1.0)
            else:
                displayNode.SetColor(0.8, 0.0, 0.0)  # Red
                displayNode.SetSelectedColor(1.0, 0.0, 0.0)
            
            displayNode.SetGlyphScale(1.8)
            displayNode.SetTextScale(3.0)
            displayNode.SetGlyphType(1)
            displayNode.SetSliceProjection(True)
        
        # Run prediction for each combination
        for sn_method in sn_methods:
            for n_method in n_methods:
                # Create unique key for this combination
                combo_key = "{0}_{1}_{2}".format(sn_method, n_method, regression_sex)
                
                # Get FSTT points for this combination
                sn_point = fstt_points['sn'][sn_method]
                n_soft_point = fstt_points['n_prime'][n_method]
                
                # Run regression prediction with these measurements
                predicted_landmarks = self.runRegressionForCombo(
                    sn_point, n_soft_point, regression_sex, combo_key
                )
                
                # Add predictions to unified node
                if predicted_landmarks['prn'] is not None:
                    lmrk_pred_node.AddControlPoint(predicted_landmarks['prn'].tolist(), 
                                                "prn_{0}".format(combo_key))
                
                if predicted_landmarks['nt'] is not None:
                    lmrk_pred_node.AddControlPoint(predicted_landmarks['nt'].tolist(),
                                                "nt_{0}".format(combo_key))
                
                # Store in lmrk_predictions dictionary
                self.storeLandmarkPredictions(combo_key, predicted_landmarks, 
                                            sn_method, n_method, regression_sex)
                
                print("✅ Generated prediction: {0}".format(combo_key))
        
        print("✅ All predictions stored in 'lmrk_predictions' node")
        return lmrk_pred_node

    def runRegressionForCombo(self, sn_point, n_soft_point, regression_sex, combo_key):
        """Run regression prediction for a specific FSTT combination"""
        coefficients = {
            'male': {
                'prn_baseline': (19.544, 0.299),
                'bony_n_sn': (4.385, 0.988),
                'soft_n_nt': (31.76, 1.009)
            },
            'female': {
                'prn_baseline': (15.056, 0.622),
                'bony_n_sn': (7.673, 0.909),
                'soft_n_nt': (33.23, 0.768)
            },
        }
        
        if regression_sex not in coefficients:
            raise ValueError("Invalid regression sex: '{0}'".format(regression_sex))
        
        coeffs = coefficients[regression_sex]
        show_lines = self.showLinesCheckbox.isChecked()
        
        # Get required nodes
        baselineNode = slicer.util.getNode('baseline')
        rhiToBaselineNode = slicer.util.getNode('rhi to baseline')
        nToRhiNode = slicer.util.getNode('n to rhi')
        
        if not all([self.hardTissueNode, baselineNode, rhiToBaselineNode, self.mspNode]):
            raise ValueError("Required measurements not found.")
        
        msp_origin, msp_normal = self.getPlaneData(self.mspNode)
        ans_point = self.getPoint(self.hardTissueNode, 3)
        n_hard_point = self.getPoint(self.hardTissueNode, 0)
        
        baseline_start = self.getPoint(baselineNode, 0)
        baseline_end = self.getPoint(baselineNode, 1)
        baseline_vec = baseline_end - baseline_start
        baseline_unit = baseline_vec / np.linalg.norm(baseline_vec)
        
        perp_vec = np.cross(baseline_unit, msp_normal)
        perp_vec = perp_vec / np.linalg.norm(perp_vec)
        
        if perp_vec[1] < 0:
            perp_vec = -perp_vec
        
        # ========== PREDICT PRONASALE ==========
        if show_lines:
            ans_perp_length = 60.0
            ans_perp_start = ans_point - (ans_perp_length / 2.0) * perp_vec
            ans_perp_end = ans_point + (ans_perp_length / 2.0) * perp_vec
            self.createLine(ans_perp_start, ans_perp_end, 
                        "ANS_perp_{0}".format(combo_key), [0.0, 0.8, 0.8], [0.0, 1.0, 1.0])
        
        rhi_to_baseline_length = self.getLineLength(rhiToBaselineNode)
        intercept, coeff = coeffs['prn_baseline']
        pred_prn_distance = intercept + coeff * rhi_to_baseline_length
        pred_prn_point = ans_point + pred_prn_distance * perp_vec
        
        if show_lines:
            self.createLine(ans_point, pred_prn_point, 
                        "ANS_to_prn_{0}".format(combo_key), [0.8, 0.8, 0.0], [1.0, 0.7, 0.0])
        
        # ========== PREDICT nasal tip (nt) ==========
        if nToRhiNode:
            n_to_rhi_length = self.getLineLength(nToRhiNode)
        else:
            rhi_point = self.getPoint(self.hardTissueNode, 1)
            n_to_rhi_length = np.linalg.norm(rhi_point - n_hard_point)
        
        # Calculate baseline distance (n to ANS)
        baseline_length = np.linalg.norm(ans_point - n_hard_point)
        
        # Calculate radii
        intercept1, coeff1 = coeffs['bony_n_sn']
        radius1 = intercept1 + coeff1 * baseline_length
        
        intercept2, coeff2 = coeffs['soft_n_nt']
        radius2 = intercept2 + coeff2 * n_to_rhi_length
        
        # Find intersection of two circles
        intersections = self.findCircleIntersections(n_hard_point, radius1, n_soft_point, radius2)
        
        pred_nt_point = None
        if intersections:
            pred_nt_point = self.selectBestNtIntersection(intersections[0], intersections[1], n_soft_point)
            
            if pred_nt_point is not None:
                # Create visualization lines if requested
                if show_lines:
                    self.createLine(n_hard_point, pred_nt_point, 
                                "n_to_nt_{0}".format(combo_key), [1.0, 0.5, 0.0], [1.0, 0.3, 0.0])
                    self.createLine(n_soft_point, pred_nt_point, 
                                "n'_to_nt_{0}".format(combo_key), [0.5, 1.0, 0.0], [0.3, 1.0, 0.0])
        
        return {
            'prn': pred_prn_point,
            'nt': pred_nt_point
        }

    def storeLandmarkPredictions(self, combo_key, landmarks, sn_method, n_method, regression_sex):
        """Store landmark predictions in a structured dictionary"""
        if not hasattr(self, 'lmrk_predictions'):
            self.lmrk_predictions = {}
        
        self.lmrk_predictions[combo_key] = {
            'sn_FSTT_method': sn_method,
            'n_FSTT_method': n_method,
            'regression_sex': regression_sex,
            'prn': landmarks['prn'],
            'nt': landmarks['nt']
        }
        
        # Store coordinates for results table
        if landmarks['prn'] is not None:
            self.storeCoordinate("prn_{0}".format(combo_key), landmarks['prn'])
        
        if landmarks['nt'] is not None:
            self.storeCoordinate("nt_{0}".format(combo_key), landmarks['nt'])
        
        print("✅ Stored prediction: {0}".format(combo_key))

    def onRunPrediction(self):
        try:
            # Create unified lmrk_predictions node
            lmrk_pred_node = slicer.util.getFirstNodeByName('lmrk_predictions')
            if lmrk_pred_node:
                slicer.mrmlScene.RemoveNode(lmrk_pred_node)
            lmrk_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'lmrk_predictions')
            
            # Clear previous predictions
            if hasattr(self, 'lmrk_predictions'):
                self.lmrk_predictions = {}
            
            if self.bothRadio.isChecked():
                self.step4StatusLabel.setText("Status: Running predictions for both sexes...")
                slicer.app.processEvents()
                
                # Run predictions for male
                male_pred_node = self.runSinglePrediction("male")
                
                # Run predictions for female
                female_pred_node = self.runSinglePrediction("female")
                
                # Merge both into unified node
                self.mergePredictionNodes(lmrk_pred_node, male_pred_node, female_pred_node)
                
                self.step4StatusLabel.setText("Status: ✅ Predictions completed for both sexes!")
                self.step4StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            elif self.maleRadio.isChecked():
                self.step4StatusLabel.setText("Status: Running male prediction...")
                slicer.app.processEvents()
                self.runSinglePrediction("male")
                self.step4StatusLabel.setText("Status: ✅ Male prediction completed!")
                self.step4StatusLabel.setStyleSheet("color: green; font-weight: bold;")
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
            slicer.util.errorDisplay("Failed to predict: {0}".format(str(e)))

    def mergePredictionNodes(self, unified_node, male_node, female_node):
        """Merge male and female prediction nodes into unified node"""
        # Copy points from male node
        if male_node:
            for i in range(male_node.GetNumberOfControlPoints()):
                point = [0, 0, 0]
                male_node.GetNthControlPointPosition(i, point)
                label = male_node.GetNthControlPointLabel(i)
                unified_node.AddControlPoint(point, label)
        
        # Copy points from female node
        if female_node:
            for i in range(female_node.GetNumberOfControlPoints()):
                point = [0, 0, 0]
                female_node.GetNthControlPointPosition(i, point)
                label = female_node.GetNthControlPointLabel(i)
                unified_node.AddControlPoint(point, label)
        
        # Set unified display properties
        displayNode = unified_node.GetDisplayNode()
        if displayNode:
            displayNode.SetColor(0.5, 0.0, 0.5)  # Purple for combined
            displayNode.SetSelectedColor(1.0, 0.5, 0.0)
            displayNode.SetGlyphScale(1.8)
            displayNode.SetTextScale(3.0)
            displayNode.SetGlyphType(1)
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
                baseline_start = n_soft.copy()
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
            self.step5StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
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
            display_node.SetTextScale(3.0)
        return np.linalg.norm(point2 - point1)
    
    def createAngle(self, name, point1, apex, point2):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        angle_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsAngleNode", name)
        angle_node.AddControlPoint(point1.tolist())
        angle_node.AddControlPoint(apex.tolist())
        angle_node.AddControlPoint(point2.tolist())
        display_node = angle_node.GetDisplayNode()
        if display_node:
            display_node.SetTextScale(3.0)
        return angle_node.GetAngleDegrees()
    
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
        """Calculate errors between predictions and true landmarks from PS_soft_tissue"""
        try:
            if not self.softTissueNode:
                raise ValueError("Please load PS_soft_tissue landmarks first.")
            
            self.step5StatusLabel.setText("Status: Calculating errors...")
            slicer.app.processEvents()
            
            errors_summary = []
            
            # Calculate errors for all stored coordinates
            for landmark_name, coords in self.all_coordinates.items():
                pred_coords = coords["predicted"]
                true_coords = self.getTrueCoordinatesFromSoftTissue(landmark_name)
                
                if true_coords is not None:
                    error_3d = np.linalg.norm(pred_coords - true_coords)
                    
                    # Store the true coordinates
                    self.all_coordinates[landmark_name]["true"] = true_coords
                    
                    # Store error measurement
                    if "ERROR:" not in landmark_name:  # Avoid duplicate error entries
                        error_name = f"ERROR: {landmark_name}"
                        self.storeMeasurement(error_name, error_3d, "mm", is_summary=True)
                    
                    # Add to summary
                    errors_summary.append(f"{landmark_name}: {error_3d:.2f} mm")
                    
                    # Create visualization line
                    line_name = f"error_{landmark_name.replace(' ', '_').replace('/', '_')}"
                    self.createLine(pred_coords, true_coords, line_name, 
                                [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
            
            self.step5StatusLabel.setText("Status: ✅ Errors calculated!")
            self.step5StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            # Update all tables
            self.updateResultsTables()
            
            # Show summary
            if errors_summary:
                msg = qt.QMessageBox()
                msg.setIcon(qt.QMessageBox.Information)
                msg.setText("Prediction Errors Calculated")
                msg.setInformativeText("\n".join(errors_summary))
                msg.setWindowTitle("Validation Results")
                msg.exec_()
            else:
                slicer.util.messageBox("No errors could be calculated.Check that true landmarks exist in PS_soft_tissue.")
                
        except Exception as e:
            self.step5StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step5StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to calculate errors: {0}".format(str(e)))
        
    def updateResultsTables(self):
        self.updateMeasurementsTable()
        self.updateCoordinatesTable()
        self.updateProvenanceTable()
    
    def updateMeasurementsTable(self):
        """Update measurements table - EXCLUDES FSTT predictions, adds comparison measurements"""
        # Filter measurements to exclude FSTT predictions
        filtered_measurements = {}
        for name, data in self.all_measurements.items():
            # Skip FSTT prediction measurements
            if "Predicted sn' FSTT" in name or "Predicted n' FSTT" in name:
                continue
            # Skip FSTT coordinate predictions (sn_pred, n'_pred)
            if "sn_pred_" in name or "n'_pred_" in name:
                continue
            filtered_measurements[name] = data
        
        # Add comparison measurements if we have soft tissue data
        if self.softTissueNode and self.hardTissueNode:
            try:
                # Get required points
                n_hard = self.getPointByLabel(self.hardTissueNode, "n")
                
                # IMPORTANT: Use subspinale (ss) as the bony sn point
                # According to Purkait & Singh's methodology and anatomical literature
                # bony sn = subspinale (ss) = orthodontic point A
                try:
                    ss = self.getPointByLabel(self.hardTissueNode, "ss")
                    bony_sn_label = "ss"
                except ValueError:
                    try:
                        ss = self.getPointByLabel(self.hardTissueNode, "subspinale")
                        bony_sn_label = "subspinale"
                    except ValueError:
                        try:
                            ss = self.getPointByLabel(self.hardTissueNode, "point A")
                            bony_sn_label = "point A"
                        except ValueError:
                            # Try by index if labels fail
                            for i in range(self.hardTissueNode.GetNumberOfControlPoints()):
                                label = self.hardTissueNode.GetNthControlPointLabel(i)
                                if label in ["ss", "subspinale", "point A", "A"]:
                                    ss = self.getPoint(self.hardTissueNode, i)
                                    bony_sn_label = label
                                    break
                            else:
                                # Default to index 2 if available (standard order)
                                if self.hardTissueNode.GetNumberOfControlPoints() > 2:
                                    ss = self.getPoint(self.hardTissueNode, 2)
                                    bony_sn_label = "ss (index 2)"
                                else:
                                    ss = None
                
                # Get ANS point
                try:
                    ans = self.getPointByLabel(self.hardTissueNode, "ANS")
                except ValueError:
                    try:
                        ans = self.getPointByLabel(self.hardTissueNode, "ans")
                    except ValueError:
                        # Try by index 3 if available
                        if self.hardTissueNode.GetNumberOfControlPoints() > 3:
                            ans = self.getPoint(self.hardTissueNode, 3)
                        else:
                            ans = None
                
                # Get soft tissue points
                n_soft = self.getPointByLabel(self.softTissueNode, "n'")
                sn_soft = self.getPointByLabel(self.softTissueNode, "sn'")
                prn_soft = self.getPointByLabel(self.softTissueNode, "prn")
                nt_soft = self.getPointByLabel(self.softTissueNode, "nt")
                
                # 1. BONY N-SS DISTANCE (This is the "bony_n_sn" measurement in Purkait & Singh)
                if ss is not None:
                    bony_n_ss_distance = np.linalg.norm(ss - n_hard)
                    filtered_measurements["Bony n-ss (bony_n_sn)"] = {
                        "value": bony_n_ss_distance,
                        "unit": "mm",
                        "is_summary": True,
                        "note": f"Using {bony_sn_label} as bony sn point"
                    }
                    print(f"✅ Bony n-ss distance (bony_n_sn): {bony_n_ss_distance:.2f} mm (using {bony_sn_label})")
                
                # 2. SOFT N'-NT DISTANCE (True from soft tissue)
                n_nt_distance = np.linalg.norm(nt_soft - n_soft)
                filtered_measurements["Soft n'-nt (true)"] = {
                    "value": n_nt_distance,
                    "unit": "mm",
                    "is_summary": True
                }
                print(f"✅ Soft n'-nt distance (true): {n_nt_distance:.2f} mm")
                
                # 3. SOFT N'-SN' DISTANCE (True from soft tissue)
                n_sn_distance = np.linalg.norm(sn_soft - n_soft)
                filtered_measurements["Soft n'-sn' (true)"] = {
                    "value": n_sn_distance,
                    "unit": "mm",
                    "is_summary": True
                }
                print(f"✅ Soft n'-sn' distance (true): {n_sn_distance:.2f} mm")
                
                # 4. SOFT N'-PRN DISTANCE (True from soft tissue)
                n_prn_distance = np.linalg.norm(prn_soft - n_soft)
                filtered_measurements["Soft n'-prn (true)"] = {
                    "value": n_prn_distance,
                    "unit": "mm",
                    "is_summary": False
                }
                
                # 5. PRN BASELINE DISTANCE (Perpendicular from prn to n-ANS line)
                if ans is not None:
                    baseline_start = n_hard
                    baseline_end = ans
                    baseline_vec = baseline_end - baseline_start
                    baseline_unit = baseline_vec / np.linalg.norm(baseline_vec)
                    
                    # Vector from n_hard to prn_soft
                    prn_vec = prn_soft - baseline_start
                    
                    # Projection length
                    projection_length = np.dot(prn_vec, baseline_unit)
                    closest_point = baseline_start + projection_length * baseline_unit
                    
                    # Perpendicular distance
                    prn_baseline_distance = np.linalg.norm(prn_soft - closest_point)
                    filtered_measurements["prn baseline (true)"] = {
                        "value": prn_baseline_distance,
                        "unit": "mm",
                        "is_summary": True
                    }
                    print(f"✅ prn baseline distance (true): {prn_baseline_distance:.2f} mm")
                
                # 6. SOFT SS-SN' DISTANCE (FSTT at sn' - for validation)
                if ss is not None:
                    ss_sn_distance = np.linalg.norm(sn_soft - ss)
                    filtered_measurements["ss-sn' (FSTT sn')"] = {
                        "value": ss_sn_distance,
                        "unit": "mm",
                        "is_summary": True,
                        "note": "Actual FSTT at sn' (ss to sn')"
                    }
                    print(f"✅ Actual ss-sn' distance (FSTT sn'): {ss_sn_distance:.2f} mm")
                
                # 7. ADD PREDICTED VERSIONS AND ERRORS
                if hasattr(self, 'lmrk_predictions') and self.lmrk_predictions:
                    for pred_id, pred_data in sorted(self.lmrk_predictions.items()):
                        # Predicted n'-nt distance
                        if pred_data.get('nt') is not None:
                            pred_n_nt_distance = np.linalg.norm(pred_data['nt'] - n_soft)
                            filtered_measurements[f"n'-nt (pred) {pred_id}"] = {
                                "value": pred_n_nt_distance,
                                "unit": "mm",
                                "is_summary": True
                            }
                            
                            # Calculate error for predicted n'-nt
                            true_n_nt = n_nt_distance
                            pred_n_nt = pred_n_nt_distance
                            error_n_nt = abs(pred_n_nt - true_n_nt)
                            filtered_measurements[f"n'-nt Error {pred_id}"] = {
                                "value": error_n_nt,
                                "unit": "mm",
                                "is_summary": True,
                                "is_error": True
                            }
                            print(f"✅ n'-nt prediction {pred_id}: pred={pred_n_nt_distance:.2f}, error={error_n_nt:.2f}")
                        
                        # Predicted prn baseline distance
                        if pred_data.get('prn') is not None and ans is not None:
                            baseline_start = n_hard
                            baseline_end = ans
                            baseline_vec = baseline_end - baseline_start
                            baseline_unit = baseline_vec / np.linalg.norm(baseline_vec)
                            
                            pred_prn_vec = pred_data['prn'] - baseline_start
                            pred_projection_length = np.dot(pred_prn_vec, baseline_unit)
                            pred_closest_point = baseline_start + pred_projection_length * baseline_unit
                            pred_prn_baseline_distance = np.linalg.norm(pred_data['prn'] - pred_closest_point)
                            
                            filtered_measurements[f"prn baseline (pred) {pred_id}"] = {
                                "value": pred_prn_baseline_distance,
                                "unit": "mm",
                                "is_summary": True
                            }
                            
                            # Calculate error for predicted prn baseline
                            true_prn_baseline = prn_baseline_distance
                            pred_prn_baseline = pred_prn_baseline_distance
                            error_prn_baseline = abs(pred_prn_baseline - true_prn_baseline)
                            filtered_measurements[f"prn baseline Error {pred_id}"] = {
                                "value": error_prn_baseline,
                                "unit": "mm",
                                "is_summary": True,
                                "is_error": True
                            }
                            print(f"✅ prn baseline prediction {pred_id}: pred={pred_prn_baseline_distance:.2f}, error={error_prn_baseline:.2f}")
                
                # 8. BONY N-SS vs SOFT N'-SN' COMPARISON
                if ss is not None:
                    ratio_n = n_sn_distance / bony_n_ss_distance if bony_n_ss_distance > 0 else 0
                    filtered_measurements["n'-sn' / n-ss ratio"] = {
                        "value": ratio_n,
                        "unit": "ratio",
                        "is_summary": True,
                        "note": "Soft/bony nasal length ratio"
                    }
                    print(f"✅ n'-sn' / n-ss ratio: {ratio_n:.3f}")
                
            except Exception as e:
                print(f"Warning: Could not add comparison measurements: {e}")
                import traceback
                traceback.print_exc()
        
        # Set table row count
        self.measurementsTable.setRowCount(len(filtered_measurements))
        
        row = 0
        for name, data in sorted(filtered_measurements.items()):
            name_item = qt.QTableWidgetItem(name)
            name_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            # Add tooltip if there's a note
            if "note" in data:
                name_item.setToolTip(data["note"])
            
            value_item = qt.QTableWidgetItem("{0:.2f}".format(data["value"]))
            value_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            unit_item = qt.QTableWidgetItem(data["unit"])
            unit_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            # Highlight important measurements (comparisons and errors)
            if data.get("is_summary", False):
                if data.get("is_error", False):
                    # Red background for errors
                    error_color = qt.QColor(255, 220, 220)
                    name_item.setBackground(error_color)
                    value_item.setBackground(error_color)
                    unit_item.setBackground(error_color)
                    
                    font = qt.QFont()
                    font.setBold(True)
                    name_item.setFont(font)
                    value_item.setFont(font)
                    unit_item.setFont(font)
                else:
                    # Yellow background for important measurements
                    yellow = qt.QColor(255, 255, 200)
                    name_item.setBackground(yellow)
                    value_item.setBackground(yellow)
                    unit_item.setBackground(yellow)
                    
                    font = qt.QFont()
                    font.setBold(True)
                    name_item.setFont(font)
                    value_item.setFont(font)
                    unit_item.setFont(font)
            
            self.measurementsTable.setItem(row, 0, name_item)
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
            true_coords = coords.get("true", None)
            
            # Always show predicted coordinates
            for col, val in enumerate([pred_coords[0], pred_coords[1], pred_coords[2]]):
                item = qt.QTableWidgetItem("{0:.2f}".format(val))
                item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                self.coordinatesTable.setItem(row, col + 1, item)
            
            # Check if we have soft tissue node for True values
            if self.softTissueNode:
                # Extract landmark type from name to match with PS_soft_tissue
                true_coords = self.getTrueCoordinatesFromSoftTissue(landmark_name)
                
                if true_coords is not None:
                    for col, val in enumerate([true_coords[0], true_coords[1], true_coords[2]]):
                        item = qt.QTableWidgetItem("{0:.2f}".format(val))
                        item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                        item.setBackground(qt.QColor(220, 255, 220))  # Light green
                        self.coordinatesTable.setItem(row, col + 4, item)
                    
                    # Calculate and show 3D error
                    error_3d = np.linalg.norm(pred_coords - true_coords)
                    error_item = qt.QTableWidgetItem("{0:.2f}".format(error_3d))
                    error_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                    error_item.setBackground(qt.QColor(255, 220, 220))  # Light red
                    font = qt.QFont()
                    font.setBold(True)
                    error_item.setFont(font)
                    self.coordinatesTable.setItem(row, 7, error_item)
                    
                    # Also update the all_coordinates dictionary
                    self.all_coordinates[landmark_name]["true"] = true_coords
                else:
                    # True landmark not found in PS_soft_tissue
                    for col in range(4, 8):
                        item = qt.QTableWidgetItem("N/A")
                        item.setFlags(qt.Qt.ItemIsEnabled)
                        self.coordinatesTable.setItem(row, col, item)
            else:
                # No soft tissue node available
                for col in range(4, 8):
                    item = qt.QTableWidgetItem("N/A")
                    item.setFlags(qt.Qt.ItemIsEnabled)
                    self.coordinatesTable.setItem(row, col, item)
            
            row += 1
        
        self.coordinatesTable.resizeColumnsToContents()
    
    def onCopyMeasurements(self):
        try:
            if not self.all_measurements:
                slicer.util.warningDisplay("No measurements available to copy. Please run the prediction and measurements first.")
                return
            
            export_text = "Measurement\tValue\tUnit\n"
            
            for name, data in sorted(self.all_measurements.items()):
                value_str = "{0:.2f}".format(data["value"])
                export_text += "{0}\t{1}\t{2}\n".format(name, value_str, data["unit"])
            
            qt.QApplication.clipboard().setText(export_text)
            
            self.step6StatusLabel.setText("Status: ✅ Measurements copied to clipboard!  Ready to paste into Excel.")
            slicer.util.showStatusMessage("Measurements copied!", 3000)
            
        except Exception as e:
            slicer.util.errorDisplay("Failed to copy measurements: {0}".format(str(e)))
    
    def onCopyCoordinates(self):
        """Copy coordinates table to clipboard"""
        try: 
            if not self.all_coordinates:
                slicer.util.warningDisplay("No coordinates available to copy.Please run the prediction first.")
                return
            
            # Create tab-separated values (TSV) format with headers
            export_text = "Landmark\tPredicted X\tPredicted Y\tPredicted Z\tTrue X\tTrue Y\tTrue Z\t3D Error (mm)\n"
            
            for landmark_name, coords in sorted(self.all_coordinates.items()):
                pred = coords["predicted"]
                true_coords = coords.get("true", None)
                
                if true_coords is not None: 
                    # Calculate 3D error
                    error_3d = np.linalg.norm(pred - true_coords)
                    # Format each value separately to avoid format specifier issues
                    export_text += "{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6:.2f}\t{7:.2f}\n".format(
                        landmark_name,
                        float(pred[0]), float(pred[1]), float(pred[2]),
                        float(true_coords[0]), float(true_coords[1]), float(true_coords[2]),
                        float(error_3d)
                    )
                else:
                    # No true coordinates available
                    export_text += "{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\tN/A\tN/A\tN/A\tN/A\n".format(
                        landmark_name,
                        float(pred[0]), float(pred[1]), float(pred[2])
                    )
            
            # Copy to clipboard
            qt.QApplication.clipboard().setText(export_text)
            
            # Show success message
            self.step6StatusLabel.setText("Status: ✅ Coordinates copied to clipboard! Ready to paste into Excel.")
            slicer.util.showStatusMessage("Coordinates copied!", 3000)
            
        except Exception as e: 
            import traceback
            traceback.print_exc()
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
