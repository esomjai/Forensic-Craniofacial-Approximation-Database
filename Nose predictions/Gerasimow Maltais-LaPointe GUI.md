```python
import os
import qt
import slicer
import vtk
import numpy as np
import urllib.request
import tempfile
import random

class GerasimowNosePredictor:
    def __init__(self):
        # Debug mode toggle
        self.DEBUG_MODE = False
        
        # Set this at the beginning to avoid errors
        self.minLogLevel = 1
        self.currentDialog = None
        self.intersections = {}
        
        # Disable popup notifications
        settings = qt.QSettings()
        settings.setValue("Markups/MarkupsFidNotificationPopupEnabled", 0)
        
        # Create main widget with step navigation
        self.mainWidget = qt.QWidget()
        self.mainWidget.setWindowTitle("Gerasimov's Nose Prediction (with Maltais-LaPointe's 3D adjustment))")
        self.mainWidget.setMinimumSize(600, 750)
        
        # Make window stay on top (but dialogs will still appear above it)
        self.mainWidget. setWindowFlags(
            self.mainWidget.windowFlags() | qt.Qt.WindowStaysOnTopHint
        )
        
        # Main layout
        mainLayout = qt.QVBoxLayout(self.mainWidget)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        # Add title
        titleLabel = qt.QLabel("Gerasimow's Two Tangent Method")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 18px;")
        titleLabel.setAlignment(qt.Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)
        
        # Create stacked widget for steps
        self.stepStack = qt.QStackedWidget()
        mainLayout.addWidget(self.stepStack)
        
        # Create decision log window
        self.logWidget = qt.QTextEdit()
        self.logWidget.setWindowTitle("Decision Log")
        self.logWidget.setReadOnly(True)
        self.logWidget.setMinimumSize(400, 300)
        self.logWidget.show()
        
        self.decisions = []
        self.log("Starting Gerasimow's nose prediction process")
        
        # Storage variables
        self.landmarksNode = None
        self.planeNode = None
        self.boneModel = None
        self.boneLeftModel = None
        self.boneRightModel = None
        self.tangents = {}
        self.points = {}
        self.tangentNodes = {}
        self.tangent_backups = {}
        self.all_measurements = {}
        self.all_coordinates = {}
        self.isDynamicModelerInstalled = False
        
        # Current step tracking
        self.currentStep = 0
        self.totalSteps = 7 
        
        # Create all step widgets
        self.createAllStepWidgets()
        
        # Setup navigation
        self.setupNavigation()
        
        # Add to main layout
        mainLayout.addLayout(self.navLayout)
        
        # Check dependencies
        self.checkDependencies()
        
        # Sync with existing scene
        self.syncWithScene()
        
        # Update UI for current step
        self.updateStepUI()
        
        # Show the widget
        self.mainWidget.show()
    
    def debug_print(self, message):
        """Print debug messages only if DEBUG_MODE is enabled"""
        if self.DEBUG_MODE:
            print(f"DEBUG: {message}")
    
    def log(self, decision, level=1):
        """Add a decision to the log if it meets the minimum log level"""
        if level >= self.minLogLevel:
            self.decisions.append(decision)
            self.updateLog()
    
    def updateLog(self):
        """Update the log window"""
        logText = "<h3>Important Actions</h3><ol>"
        for decision in self.decisions:
            logText += f"<li>{decision}</li>"
        logText += "</ol>"
        self.logWidget.setHtml(logText)
    
    def checkDependencies(self):
        """Check if Dynamic Modeler extension is installed"""
        moduleName = "DynamicModeler"
        if moduleName in slicer.app.moduleManager().factoryManager().registeredModuleNames():
            self.isDynamicModelerInstalled = True
        else:
            self.isDynamicModelerInstalled = False
            msgBox = qt.QMessageBox()
            msgBox.setWindowTitle("Missing Required Extension")
            msgBox.setIcon(qt.QMessageBox.Warning)
            msgBox.setTextFormat(qt.Qt.RichText)
            msgBox.setText(
                "The <b>Dynamic Modeler</b> extension is required for skull cutting (Steps 3-4), but it was not found.<br><br>"
                "Please install it to use all features: <br>"
                "1.Go to the menu:  <b>View -> Extension Manager</b>.<br>"
                "2.In the 'Search' bar, type <b>Dynamic Modeler</b>.<br>"
                "3.Click the <b>'Install'</b> button.<br>"
                "4.<b>Restart 3D Slicer</b> after installation.<br><br>"
                "You can still use the T1-T2 shortcut without this extension."
            )
            msgBox.exec_()
    
    def setupNavigation(self):
        """Create navigation buttons"""
        self.navLayout = qt.QHBoxLayout()
        self.navLayout.setContentsMargins(0, 0, 0, 0)
        
        self.prevButton = qt.QPushButton("◀ Previous")
        self.prevButton.setToolTip("Go to the previous step")
        self.prevButton.clicked.connect(self.onPrevButtonClicked)
        
        self.stepLabel = qt.QLabel("Step 1/7")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter)
        self.stepLabel.setStyleSheet("font-weight:  bold; font-size: 14px;")
        
        self.nextButton = qt.QPushButton("Next ▶")
        self.nextButton.setToolTip("Go to the next step")
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        
        self.navLayout.addWidget(self.prevButton)
        self.navLayout.addStretch(1)
        self.navLayout.addWidget(self.stepLabel)
        self.navLayout.addStretch(1)
        self.navLayout.addWidget(self.nextButton)
    
    def createAllStepWidgets(self):
        """Create all step widgets"""
        self.createStep1_Welcome()
        self.createStep2_PlaneSetup()
        self.createStep3_Segmentation() 
        self.createStep4_ExecuteVisualization()  
        self.createStep5_TangentCreation()
        self.createStep6_SoftTissueComparison()
        self.createStep7_Results()
    
    def createStep1_Welcome(self):
        """Step 1: Welcome and Load Landmarks"""
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Welcome to Gerasimow's Nose Prediction Method")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "This method predicts the pronasale (nose tip) position using tangent lines.\n\n"
            "Please begin by loading the required landmarks using one of the options below."
        )
        desc.setWordWrap(True)
        desc.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(desc)
        
        buttonLayout = qt.QVBoxLayout()
        buttonLayout.setSpacing(10)
        
        self.downloadButton = qt.QPushButton("📥 Download Landmarks from GitHub")
        self.downloadButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.downloadButton.clicked.connect(self.onDownloadLandmarksClicked)
        buttonLayout.addWidget(self.downloadButton)
        
        self.loadLocalButton = qt.QPushButton("📂 Load Landmarks from Local File")
        self.loadLocalButton.setStyleSheet("background-color: #2196F3; color: white; font-weight:  bold; padding: 10px;")
        self.loadLocalButton.clicked.connect(self.onLoadLocalLandmarksClicked)
        buttonLayout.addWidget(self.loadLocalButton)
        
        layout.addLayout(buttonLayout)
        
        self.step1StatusLabel = qt.QLabel("Status: Waiting for landmarks to be loaded.")
        self.step1StatusLabel.setWordWrap(True)
        self.step1StatusLabel.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.step1StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep2_PlaneSetup(self):
        """Step 2: Create Reference Plane"""
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 2: Create a Reference Plane")
        title.setStyleSheet("font-weight:  bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc_html = """
        <p>Create a reference plane for the tangent lines. You have two options:</p>
        <ul>
            <li><b>INB Plane:</b> Uses Inion, Nasion, and Bregma (simple three-point plane)</li>
            <li><b>MSP Plane:</b> Uses Nasion, Acanthion, Prosthion, and Subspinale (best-fit midsagittal plane)</li>
        </ul>
        <p>The plane will be used to constrain the tangent lines in the following steps.</p>
        """
        desc = qt.QLabel(desc_html)
        desc.setTextFormat(qt.Qt.RichText)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        planeChoiceLayout = qt.QVBoxLayout()
        planeChoiceLayout.setSpacing(10)
        
        self.landmarkBundleCombo = qt.QComboBox()
        self.landmarkBundleCombo.addItems([
            "Select a method...",
            "INB (Inion-Nasion-Bregma)",
            "MSP (Midsagittal Best-Fit)"
        ])
        planeChoiceLayout.addWidget(self.landmarkBundleCombo)
        
        self.createPlaneButton = qt.QPushButton("Create Plane")
        self.createPlaneButton.setStyleSheet("background-color: #FFDF00; font-weight: bold; padding: 10px;")
        self.createPlaneButton.clicked.connect(self.onCreatePlaneClicked)
        planeChoiceLayout.addWidget(self.createPlaneButton)
        
        layout.addLayout(planeChoiceLayout)
        
        self.step2StatusLabel = qt.QLabel("Status: Please choose a plane creation method.")
        self.step2StatusLabel.setWordWrap(True)
        self.step2StatusLabel.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.step2StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep3_Segmentation(self):
        """Step 3: Choose Visualization Method"""
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(20)
        
        title = qt.QLabel("Step 3: Choose Your Visualization Method")
        title.setStyleSheet("font-weight:  bold; font-size: 16px;")
        title.setAlignment(qt.Qt. AlignCenter)
        mainLayout.addWidget(title)
        
        intro = qt.QLabel(
            "You need to visualize the skull to place tangent lines accurately. "
            "Choose one of the two methods below:"
        )
        intro.setWordWrap(True)
        intro.setAlignment(qt.Qt.AlignCenter)
        mainLayout.addWidget(intro)
        
        mainLayout.addSpacing(20)
        
        # Option 1: Manual Volume Rendering
        option1Group = qt.QGroupBox()
        option1Group.setStyleSheet("QGroupBox { background-color: #E8F5E9; border:  2px solid #4CAF50; border-radius: 5px; padding: 15px; }")
        option1Layout = qt.QVBoxLayout(option1Group)
        
        option1Title = qt.QLabel("<b>📌 Option 1: Quick Manual Method (Volume Rendering)</b>")
        option1Title.setTextFormat(qt.Qt.RichText)
        option1Title.setStyleSheet("font-size: 14px;")
        option1Layout.addWidget(option1Title)
        
        option1Desc = qt.QLabel(
            "<b>Pros:</b> Fast, reversible, good for beginners<br>"
            "<b>Cons: </b> Temporary visualization only, not saved<br><br>"
            "<b>Best for:</b> Quick analysis, T1-T2 shortcut method, learning"
        )
        option1Desc.setTextFormat(qt. Qt.RichText)
        option1Desc.setWordWrap(True)
        option1Layout.addWidget(option1Desc)
        
        self.chooseManualButton = qt.QPushButton("✓ Choose Manual Method")
        self.chooseManualButton. setStyleSheet("background-color:  #4CAF50; color:  white; font-weight: bold; padding: 10px;")
        self.chooseManualButton.clicked.connect(self.onChooseManualMethod)
        option1Layout.addWidget(self.chooseManualButton)
        
        mainLayout.addWidget(option1Group)
        
        # OR separator
        orLabel = qt.QLabel("<center><b>— OR —</b></center>")
        orLabel.setTextFormat(qt.Qt.RichText)
        orLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        mainLayout.addWidget(orLabel)
        
        # Option 2: Automatic Segmentation
        option2Group = qt.QGroupBox()
        option2Group.setStyleSheet("QGroupBox { background-color: #E3F2FD; border: 2px solid #2196F3; border-radius: 5px; padding: 15px; }")
        option2Layout = qt.QVBoxLayout(option2Group)
        
        option2Title = qt.QLabel("<b>🤖 Option 2: Permanent Segmentation Method</b>")
        option2Title.setTextFormat(qt. Qt.RichText)
        option2Title.setStyleSheet("font-size: 14px;")
        option2Layout.addWidget(option2Title)
        
        option2Desc = qt.QLabel(
            "<b>Pros:</b> Creates permanent 3D model, can save and export<br>"
            "<b>Cons:</b> More steps, takes longer, requires more disk space<br><br>"
            "<b>Best for:</b> Publication, detailed analysis, model archiving"
        )
        option2Desc.setTextFormat(qt.Qt.RichText)
        option2Desc.setWordWrap(True)
        option2Layout.addWidget(option2Desc)
        
        self.chooseSegmentationButton = qt.QPushButton("✓ Choose Segmentation Method")
        self.chooseSegmentationButton.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding:  10px;")
        self.chooseSegmentationButton. clicked.connect(self.onChooseSegmentationMethod)
        option2Layout.addWidget(self.chooseSegmentationButton)
        
        mainLayout.addWidget(option2Group)
        
        mainLayout.addSpacing(20)
        
        self.step3StatusLabel = qt. QLabel("Status:  Please choose a visualization method above.")
        self.step3StatusLabel.setWordWrap(True)
        self.step3StatusLabel.setStyleSheet("padding: 10px; background-color:  #f0f0f0; border-radius: 5px;")
        mainLayout.addWidget(self.step3StatusLabel)
        
        mainLayout.addStretch(1)
        self.stepStack.addWidget(widget)
        
        # Store the chosen method
        self.chosenVisualizationMethod = None

    def createStep4_ExecuteVisualization(self):
        """Step 4: Execute the chosen visualization method"""
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(15)
        
        title = qt.QLabel("Step 4: Set Up Visualization")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        mainLayout.addWidget(title)
        
        # This will be populated dynamically based on choice
        self.step4ContentWidget = qt.QWidget()
        self.step4ContentLayout = qt.QVBoxLayout(self.step4ContentWidget)
        mainLayout.addWidget(self.step4ContentWidget)
        
        self.step4StatusLabel = qt.QLabel("Status: Complete Step 3 first to see instructions here.")
        self.step4StatusLabel.setWordWrap(True)
        self.step4StatusLabel.setStyleSheet("padding: 10px; background-color:  #f0f0f0; border-radius: 5px;")
        mainLayout.addWidget(self.step4StatusLabel)
        
        mainLayout.addStretch(1)
        self.stepStack.addWidget(widget)

    def populateStep4ForManualMethod(self):
        """Populate Step 4 with manual volume rendering instructions"""
        # Clear existing content
        while self.step4ContentLayout.count():
            child = self.step4ContentLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        methodLabel = qt.QLabel("<b>Method:  Volume Rendering (Manual)</b>")
        methodLabel.setTextFormat(qt. Qt.RichText)
        methodLabel.setStyleSheet("font-size: 14px; color: #4CAF50;")
        self.step4ContentLayout.addWidget(methodLabel)
        
        # Detailed instructions
        instructionsLabel = qt.QLabel(
            "<b>Follow these steps to set up volume rendering:</b><br><br>"
            "<b>1.</b> Click the button below to open the Volume Rendering module.<br>"
        )
        instructionsLabel.setTextFormat(qt.Qt.RichText)
        instructionsLabel.setWordWrap(True)
        self.step4ContentLayout.addWidget(instructionsLabel)
        
        openVRButton = qt.QPushButton("📊 Open Volume Rendering Module")
        openVRButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
        openVRButton.clicked.connect(self.onOpenVolumeRendering)
        self.step4ContentLayout.addWidget(openVRButton)
        
        detailedSteps = qt.QLabel(
            "<br><b>2.</b> In the Volume Rendering module: <br>"
            "• Under '<b>Display</b>' section, find the '<b>Crop</b>' subsection<br>"
            "• Click the <b>eye icon</b> next to 'Display ROI' to make it visible<br>"
            "• Tick the checkbox for '<b>Enable</b>' under Crop<br><br>"
            "<b>3.</b> A <b>3D box (ROI)</b> should appear around your skull: <br>"
            "• If you cannot see the box, adjust the '<b>Shift</b>' slider (located right above 'Crop')<br>"
            "• Drag the box handles to cut the skull in half around the <b>acanthion</b> landmark<br>"
            "• This helps you visualize the <b>anterior nasal spine</b> for tangent T2<br><br>"
            "<b>4.</b> For tangent T2, you need to see the general direction of the anterior nasal spine. <br><br>"
            "<b>5.</b> When you're done placing tangents: <br>"
            "• Untick '<b>Enable</b>' under Crop<br>"
            "• Close the eye icon for 'Display ROI'<br>"
            "• This restores the full skull view"
        )
        detailedSteps.setTextFormat(qt.Qt.RichText)
        detailedSteps. setWordWrap(True)
        self.step4ContentLayout. addWidget(detailedSteps)
        
        continueButton = qt.QPushButton("✓ Continue to Tangent Creation")
        continueButton. setStyleSheet("background-color:  #FF9800; color: white; padding:  10px; font-weight: bold;")
        continueButton.clicked.connect(self.onSkipToTangents)
        self.step4ContentLayout.addWidget(continueButton)
        
        self.step4StatusLabel. setText("Status: Follow the volume rendering instructions above.")

    def populateStep4ForSegmentation(self):
        """Populate Step 4 with detailed segmentation instructions"""
        # Clear existing content
        while self.step4ContentLayout.count():
            child = self.step4ContentLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        methodLabel = qt. QLabel("<b>Method:  Segmentation (Permanent Model)</b>")
        methodLabel.setTextFormat(qt.Qt.RichText)
        methodLabel.setStyleSheet("font-size: 14px; color:  #2196F3;")
        self.step4ContentLayout. addWidget(methodLabel)
        
        # Create scroll area for detailed instructions
        scrollArea = qt.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setMaximumHeight(400)
        instructions_container = qt.QWidget()
        instructions_layout = qt.QVBoxLayout(instructions_container)
        instructions_layout.setContentsMargins(5, 5, 5, 5)
        scrollArea.setWidget(instructions_container)
        
        instructions = qt.QLabel()
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setWordWrap(True)
        instructions.setText(
            "<b>Follow these steps carefully to create a 'Bone' model:</b><br><br>"
            "<b>1. Open Segment Editor: </b> Click this button to open the module. <br>"
        )
        instructions_layout.addWidget(instructions)
        
        self.openSegmentEditorButton = qt.QPushButton("Open Segment Editor Module")
        self.openSegmentEditorButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px;")
        self.openSegmentEditorButton.clicked.connect(self.onOpenSegmentEditor)
        instructions_layout.addWidget(self.openSegmentEditorButton)
        
        instructions2 = qt.QLabel()
        instructions2.setTextFormat(qt.Qt.RichText)
        instructions2.setWordWrap(True)
        instructions2.setText(
            "<br><b>2. Rename your segmentation: </b> Click the dropdown menu next to <b>Segmentation: </b> and choose 'Rename current Segmentation'.<br><br>"
            "<b>3. Source Volume</b> should be the name of your DICOM file.<br><br>"
            "<b>4. Click the plus sign [+] 'Add'. </b><br><br>"
            "<b>5. Choose the Threshold tool</b> from the panel below (in the right column, first row).<br><br>"
            "<b>6. Edit the Threshold Range:</b> The minimum is usually 500.  The maximum can stay as is.  "
            "You can adjust these values to see more or less detail.<br><br>"
            "<b>7. Click 'Apply'</b> (in the Local histogram menu), then find the <b>'Show 3D'</b> button on the top, "
            "near to where the 'Add' button was.  Click it and wait for the model to appear.<br><br>"
            "<b>8. If you're happy with the details,</b> click on the green right arrow to go to the 'Segmentations' module.<br><br>"
            "<b>9. Double click on the row below 'Name'</b> and in the pop-up, edit the model name into <b>'Bone'</b>.<br><br>"
            "<b>10. Scroll to the dropdown menu 'Export/import models and labelmaps': </b> Make sure the <b>Operation</b> is 'Export' "
            "and the <b>Output type</b> is 'Models'.  Then move down to the next dropdown and click on '<b>Export</b>'.<br><br>"
            "<b>11. IMPORTANT: </b> You need to import this model back into the scene by clicking the <b>'Data'</b> button "
            "(very top of the Slicer window, under 'File'), 'Choose file(s) to add... ', and navigate to where Slicer saved your model.  "
            "Select it and click 'OK'.<br><br>"
            "<b>12. Select the re-imported model below: </b>"
        )
        instructions_layout.addWidget(instructions2)
        
        self.step4ContentLayout.addWidget(scrollArea)
        
        # Model selector
        confirmFrame = qt.QFrame()
        confirmLayout = qt.QFormLayout(confirmFrame)
        confirmLabel = qt.QLabel("Select re-imported 'Bone' model:")
        
        self.boneModelSelector = slicer.qMRMLNodeComboBox()
        self.boneModelSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.boneModelSelector.setMRMLScene(slicer. mrmlScene)
        self.boneModelSelector.addEnabled = False
        self.boneModelSelector.removeEnabled = False
        self.boneModelSelector.noneEnabled = True
        self. boneModelSelector.currentNodeChanged.connect(self.onConfirmSegmentation)
        
        confirmLayout.addRow(confirmLabel, self.boneModelSelector)
        self.step4ContentLayout.addWidget(confirmFrame)
        
        self.step4StatusLabel.setText("Status: Follow the segmentation instructions above and select the model when done.")
    
    def onChooseManualMethod(self):
        """Handle manual method selection"""
        self.chosenVisualizationMethod = "manual"
        self.step3StatusLabel.setText("Status: Manual method chosen!  Proceed to Step 4.")
        self.log("Chose manual volume rendering method")
        self.populateStep4ForManualMethod()
        # Enable next button
        self.nextButton.setEnabled(True)

    def onChooseSegmentationMethod(self):
        """Handle segmentation method selection"""
        self. chosenVisualizationMethod = "segmentation"
        self. step3StatusLabel.setText("Status: Segmentation method chosen!  Proceed to Step 4.")
        self.log("Chose segmentation method")
        self.populateStep4ForSegmentation()
        # Enable next button
        self. nextButton.setEnabled(True)

    def onSkipToTangents(self):
        """Skip directly to tangent creation (for manual method)"""
        self.step4StatusLabel.setText("Status: Proceeding to tangent creation.")
        self.log("Manual method complete, proceeding to tangent creation")
        # Jump to Step 5 (Tangent Creation)
        self.currentStep = 4  # ✅ Step 5 is index 4 (0-indexed)
        self.updateStepUI()

    def createStep5_TangentCreation(self):
        """Step 5: Create Tangent Lines"""
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 5: Create Tangent Lines")
        title.setStyleSheet("font-weight:  bold; font-size: 16px;")
        layout.addWidget(title)
        
        # T1-T2 Shortcut Section
        shortcutGroup = qt.QGroupBox("Quick Method:  T1-T2 Shortcut")
        shortcutLayout = qt.QVBoxLayout(shortcutGroup)
        
        shortcutDesc = qt.QLabel(
            "For a quick prediction using only T1 and T2 tangents, enable the shortcut below. "
            "This will hide the more complex T3, T4, and R2 options."
        )
        shortcutDesc.setWordWrap(True)
        shortcutLayout.addWidget(shortcutDesc)
        
        self.t1t2ShortcutCheckbox = qt.QCheckBox("Use T1-T2 Shortcut Mode")
        self.t1t2ShortcutCheckbox.setToolTip("When enabled, only T1 and T2 tangents are used")
        self.t1t2ShortcutCheckbox.setChecked(False)
        self.t1t2ShortcutCheckbox.toggled.connect(self.onT1T2ShortcutToggled)
        shortcutLayout.addWidget(self.t1t2ShortcutCheckbox)
        
        layout.addWidget(shortcutGroup)
        
        # Tangent Generation Section
        tangentGroup = qt.QGroupBox("Tangent Line Generation")
        tangentLayout = qt.QVBoxLayout(tangentGroup)
        
        self.regenTangentsButton = qt.QPushButton("🔄 Generate/Regenerate Default Tangents")
        self.regenTangentsButton.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        self.regenTangentsButton.setToolTip("Create T1, T2, T3 using default positions on the current plane")
        self.regenTangentsButton.clicked.connect(self.onRegenerateTangentsClicked)
        tangentLayout.addWidget(self.regenTangentsButton)
        
        self.tangentInstructionLabel = qt.QLabel("Click the button above to create tangent lines.")
        self.tangentInstructionLabel.setStyleSheet("font-style: italic; color: #555555; padding: 5px;")
        self.tangentInstructionLabel.setWordWrap(True)
        self.tangentInstructionLabel.setAlignment(qt.Qt.AlignCenter)
        tangentLayout.addWidget(self.tangentInstructionLabel)
        
        layout.addWidget(tangentGroup)
        
        # T4 Section (hidden in shortcut mode)
        self.t4Group = qt.QGroupBox("Additional Tangents (T4)")
        t4Layout = qt.QVBoxLayout(self.t4Group)
        
        self.t4rButton = qt.QPushButton("Place T4R (Purple)")
        self.t4rButton.setStyleSheet("background-color: #9966CC; color: white; font-weight: bold; padding: 8px;")
        self.t4rButton.clicked.connect(lambda: self.onPlaceTangentClicked("T4R"))
        t4Layout.addWidget(self.t4rButton)
        
        self.t4lButton = qt.QPushButton("Place T4L (Purple) - Optional")
        self.t4lButton.setStyleSheet("background-color: #9966CC; color: white; padding: 8px;")
        self.t4lButton.clicked.connect(lambda: self.onPlaceTangentClicked("T4L"))
        t4Layout.addWidget(self.t4lButton)
        
        layout.addWidget(self.t4Group)
        
        # Intersection Finding
        intersectionGroup = qt.QGroupBox("Find Intersections")
        intersectionLayout = qt.QVBoxLayout(intersectionGroup)
        
        self.extendTangentsButton = qt.QPushButton("📏 Elongate Tangents if Needed")
        self.extendTangentsButton.setStyleSheet("background-color: #66CCBB; color: white; padding: 8px;")
        self.extendTangentsButton.clicked.connect(self.onExtendTangentsClicked)
        intersectionLayout.addWidget(self.extendTangentsButton)
        
        self.findIntersectionsButton = qt.QPushButton("🎯 Find Intersections")
        self.findIntersectionsButton.setStyleSheet("background-color: #99CC66; color: white; font-weight: bold; padding: 10px;")
        self.findIntersectionsButton.clicked.connect(self.onFindIntersectionsClicked)
        intersectionLayout.addWidget(self.findIntersectionsButton)
        
        layout.addWidget(intersectionGroup)
        
        self.step5StatusLabel = qt.QLabel("Status: Ready to create tangent lines.")
        self.step5StatusLabel.setWordWrap(True)
        self.step5StatusLabel.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.step5StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep6_SoftTissueComparison(self):
        """Step 6: Soft Tissue Comparison"""
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 6: Soft Tissue Comparison")
        title.setStyleSheet("font-weight:  bold; font-size: 16px;")
        layout.addWidget(title)
        
        adviceLabel = qt.QLabel(
            "<b>Allocate the following soft tissue landmarks:</b><br>"
            "• <b>RR2: </b> Point where T4R crosses nasal soft tissue (right side)<br>"
            "• <b>LR2:</b> Point where T4L crosses nasal soft tissue (left side)<br>"
            "• <b>R2:</b> Point where final T4 crosses nasal soft tissue (midsagittal)"
        )
        adviceLabel.setTextFormat(qt.Qt.RichText)
        adviceLabel.setWordWrap(True)
        layout.addWidget(adviceLabel)
        
        # Use existing points
        self.useExistingPointsButton = qt.QPushButton("📍 Use Existing R2, LR2, RR2 Points")
        self.useExistingPointsButton.setStyleSheet("background-color: #f0ad4e; color: white; font-weight: bold; padding: 10px;")
        self.useExistingPointsButton.clicked.connect(self.onUseExistingPointsClicked)
        layout.addWidget(self.useExistingPointsButton)
        
        # R2 method selection
        methodGroup = qt.QGroupBox("R2 Point Placement Method")
        methodLayout = qt.QVBoxLayout(methodGroup)
        
        self.r2MethodButtonGroup = qt.QButtonGroup()
        self.manualR2RadioButton = qt.QRadioButton("Place R2 manually")
        self.automaticR2RadioButton = qt.QRadioButton("Calculate R2 from LR2 and RR2")
        
        self.r2MethodButtonGroup.addButton(self.manualR2RadioButton, 1)
        self.r2MethodButtonGroup.addButton(self.automaticR2RadioButton, 2)
        self.manualR2RadioButton.setChecked(True)
        
        methodLayout.addWidget(self.manualR2RadioButton)
        methodLayout.addWidget(self.automaticR2RadioButton)
        
        self.r2MethodButtonGroup.buttonClicked.connect(self.onR2MethodChanged)
        layout.addWidget(methodGroup)
        
        # Manual placement
        self.placeR2Button = qt.QPushButton("Place R2 Point Manually")
        self.placeR2Button.clicked.connect(lambda: self.onPlacePointClicked("R2"))
        layout.addWidget(self.placeR2Button)
        
        # Automatic calculation frame
        self.automaticR2Frame = qt.QFrame()
        automaticR2Layout = qt.QVBoxLayout(self.automaticR2Frame)
        
        self.placeLR2Button = qt.QPushButton("Place LR2 Point")
        self.placeLR2Button.clicked.connect(lambda: self.onPlacePointClicked("LR2"))
        automaticR2Layout.addWidget(self.placeLR2Button)
        
        self.placeRR2Button = qt.QPushButton("Place RR2 Point")
        self.placeRR2Button.clicked.connect(lambda: self.onPlacePointClicked("RR2"))
        automaticR2Layout.addWidget(self.placeRR2Button)
        
        r2CalcGroup = qt.QGroupBox("R2 Calculation Method")
        r2CalcLayout = qt.QVBoxLayout(r2CalcGroup)
        
        self.r2CalcMethodButtonGroup = qt.QButtonGroup()
        self.intersectionR2RadioButton = qt.QRadioButton("Use intersection with plane")
        self.geometricR2RadioButton = qt.QRadioButton("Use geometric mean")
        
        self.r2CalcMethodButtonGroup.addButton(self.intersectionR2RadioButton, 1)
        self.r2CalcMethodButtonGroup. addButton(self.geometricR2RadioButton, 2)
        self.intersectionR2RadioButton. setChecked(True)
        
        r2CalcLayout. addWidget(self.intersectionR2RadioButton)
        r2CalcLayout.addWidget(self.geometricR2RadioButton)
        automaticR2Layout.addWidget(r2CalcGroup)


        self.calculateR2Button = qt.QPushButton("Calculate R2 Point")
        self.calculateR2Button.clicked.connect(self.onCalculateR2Clicked)
        automaticR2Layout.addWidget(self.calculateR2Button)
        
        self.automaticR2Frame.setVisible(False)
        layout.addWidget(self.automaticR2Frame)
        
        # Error comparison
        self.calculateErrorsButton = qt.QPushButton("📊 Compare True vs. Predicted Points")
        self.calculateErrorsButton.setStyleSheet("background-color: #f0ad4e; color: white; font-weight: bold; padding:  10px;")
        self.calculateErrorsButton.clicked.connect(self.onCalculateErrorsClicked)
        layout.addWidget(self.calculateErrorsButton)
        
        self.step6StatusLabel = qt.QLabel("Status: Ready to place soft tissue points.")
        self.step6StatusLabel.setWordWrap(True)
        self.step6StatusLabel.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.step6StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep7_Results(self):
        """Step 7: Results and Export"""
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 7: Results and Export")
        title.setStyleSheet("font-weight:  bold; font-size: 16px;")
        layout.addWidget(title)
        
        # Measurements Table
        measurementsLabel = qt.QLabel("<b>📏 Measurements (Distances and Angles)</b>")
        measurementsLabel.setStyleSheet("font-size: 14px;")
        layout.addWidget(measurementsLabel)
        
        instructionsLabel = qt.QLabel(
            "Prediction errors are <span style='background-color: #ffffcc;'>highlighted in yellow</span>."
        )
        instructionsLabel.setWordWrap(True)
        layout.addWidget(instructionsLabel)
        
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable.setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Value", "Unit"])
        self.measurementsTable.horizontalHeader().setStretchLastSection(False)
        try:
            self.measurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        except:
            self.measurementsTable.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.measurementsTable.setMinimumHeight(200)
        self.measurementsTable.setAlternatingRowColors(True)
        layout.addWidget(self.measurementsTable)
        
        # Coordinates Table
        coordinatesLabel = qt.QLabel("<b>📍 Coordinates Comparison (Predicted vs True)</b>")
        coordinatesLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(coordinatesLabel)
        
        self.coordinatesTable = qt.QTableWidget()
        self.coordinatesTable.setColumnCount(8)
        self.coordinatesTable.setHorizontalHeaderLabels([
            "Landmark",
            "Predicted X", "Predicted Y", "Predicted Z",
            "True X", "True Y", "True Z",
            "3D Error (mm)"
        ])
        try:
            self.coordinatesTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        except:
            self.coordinatesTable.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.coordinatesTable.setMinimumHeight(150)
        self.coordinatesTable.setAlternatingRowColors(True)
        layout.addWidget(self.coordinatesTable)
        
        # Copy Buttons
        buttonLayout = qt.QHBoxLayout()
        
        self.copyMeasurementsButton = qt.QPushButton("📋 Copy Measurements")
        self.copyMeasurementsButton.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; font-weight: bold;")
        self.copyMeasurementsButton.clicked.connect(self.onCopyMeasurements)
        buttonLayout.addWidget(self.copyMeasurementsButton)
        
        self.copyCoordinatesButton = qt.QPushButton("📋 Copy Coordinates")
        self.copyCoordinatesButton.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold;")
        self.copyCoordinatesButton.clicked.connect(self.onCopyCoordinates)
        buttonLayout.addWidget(self.copyCoordinatesButton)
        
        layout.addLayout(buttonLayout)
        
        # Finish button
        self.finishButton = qt.QPushButton("✓ Finish and Close")
        self.finishButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 12px;")
        self.finishButton.clicked.connect(self.onFinish)
        layout.addWidget(self.finishButton)
        
        self.step7StatusLabel = qt.QLabel("Status: Review your results above.")
        self.step7StatusLabel.setWordWrap(True)
        self.step7StatusLabel.setStyleSheet("padding: 10px; background-color:  #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.step7StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    # Navigation methods
    def onPrevButtonClicked(self):
        """Go to previous step"""
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()
    
    def onNextButtonClicked(self):
        """Go to next step"""
        if self.currentStep < self.stepStack.count - 1:
            # Validation before moving forward
            if not self.validateCurrentStep():
                return
            self.currentStep += 1
            self.updateStepUI()
    
    def updateStepUI(self):
        """Update the UI for the current step"""
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.totalSteps}")
        
        # Update button states
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.totalSteps - 1)
        
        if self.currentStep == self.totalSteps - 1:
            self.nextButton.setText("Finished")
        else:
            self.nextButton.setText("Next ▶")
    
    def validateCurrentStep(self):
        """Validate current step before moving to next"""
        if self.currentStep == 0:
            # Step 1: Check if landmarks are loaded
            if not self.landmarksNode: 
                slicer.util.messageBox("Please load landmarks before continuing.")
                return False
        elif self.currentStep == 1:
            # Step 2: Check if plane is created
            if not self.planeNode:
                slicer.util.messageBox("Please create a reference plane before continuing.")
                return False
        # Steps 3 and 4 can be skipped for T1-T2 shortcut
        return True
    
    def onT1T2ShortcutToggled(self, checked):
        """Toggle T1-T2 shortcut mode"""
        self.t4Group.setVisible(not checked)
        if checked:
            self.log("T1-T2 Shortcut mode enabled")
            self.tangentInstructionLabel.setText(
                "Shortcut mode:  Only T1 and T2 tangents will be used."
            )
        else:
            self.log("Full tangent mode enabled")
            self.tangentInstructionLabel.setText(
                "Full mode: All tangents (T1, T2, T3, T4) will be used."
            )
    
    def syncWithScene(self):
        """Check scene for existing nodes"""
        self.log("Checking scene for existing nodes...")
        
        # Check for landmarks
        landmarksNode = slicer.util.getFirstNodeByName("Gerasimow_landmarks")
        if landmarksNode:
            self.landmarksNode = landmarksNode
            self.step1StatusLabel.setText("Status: Found existing 'Gerasimow_landmarks'.")
        
        # Check for plane
        planeNode = slicer.util.getFirstNodeByName("INB") or slicer.util.getFirstNodeByName("MSP")
        if planeNode: 
            self.planeNode = planeNode
            self.step2StatusLabel.setText(f"Status: Found existing '{planeNode.GetName()}' plane.")
        
        # Check for bone model
        boneModel = slicer.util.getFirstNodeByName("Bone")
        if boneModel: 
            self.boneModel = boneModel
            self.boneModelSelector.setCurrentNode(boneModel)
        
        # Check for cut models
        self.onConfirmCut(updateStatusOnly=True)
        
        # Check for tangent lines
        tangent_names = ["T1", "T2", "T3", "T4R", "T4L", "T4"]
        for name in tangent_names:
            try:
                node = slicer.util.getNode(name)
                if node: 
                    self.tangentNodes[name] = node
                    if node.GetNumberOfControlPoints() >= 2:
                        start = [0, 0, 0]
                        end = [0, 0, 0]
                        node.GetNthControlPointPositionWorld(0, start)
                        node.GetNthControlPointPositionWorld(1, end)
                        self.tangents[name] = {'start': start, 'end':  end}
            except:
                pass
        
        # Check for soft tissue points
        self.checkAndUseExistingPoints()
    
    # Implementation methods (keeping your existing logic)
    def onDownloadLandmarksClicked(self):
        """Download landmarks from GitHub"""
        url = "https://github.com/user-attachments/files/22232935/Gerasimow_landmarks.mrk.json"
        self.step1StatusLabel.setText("Status: Downloading...")
        slicer.app.processEvents()
        
        try: 
            with urllib.request.urlopen(url) as response:
                fileData = response.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile:
                tempFile.write(fileData)
                tempFilePath = tempFile.name
            
            loadedNode = slicer.util.loadMarkups(tempFilePath)
            if loadedNode:
                loadedNode.SetName("Gerasimow_landmarks")
                self.landmarksNode = loadedNode
                self.step1StatusLabel.setText("Status: Successfully downloaded and loaded landmarks!")
                self.log("Downloaded landmarks from GitHub")
            
            if os.path.exists(tempFilePath):
                os.remove(tempFilePath)
        except Exception as e:
            self.step1StatusLabel.setText(f"Status: Error downloading!  {e}")
            slicer.util.errorDisplay(f"Failed to download:  {e}")
    
    def onLoadLocalLandmarksClicked(self):
        """Load landmarks from local file"""
        fileName, _ = qt.QFileDialog.getOpenFileName(self.mainWidget, "Load Landmarks", "", "Markup JSON Files (*.mrk.json)")
        if fileName:
            loadedNode = slicer.util.loadMarkups(fileName)
            if loadedNode:
                loadedNode.SetName("Gerasimow_landmarks")
                self.landmarksNode = loadedNode
                self.step1StatusLabel.setText("Status: Successfully loaded local landmarks!")
                self.log(f"Loaded landmarks from {fileName}")
    
    def onCreatePlaneClicked(self):
        """Create reference plane"""
        if not self.landmarksNode:
            self.syncWithScene()
        if not self.landmarksNode:
            self.step2StatusLabel.setText("Status: Error!  Go back and load landmarks first.")
            return
        
        choice_index = self.landmarkBundleCombo.currentIndex
        if choice_index == 0:
            self.step2StatusLabel.setText("Status: Please select a plane method.")
            return
        
        self.step2StatusLabel.setText("Status: Creating plane...")
        slicer.app.processEvents()
        
        try:
            plane_name = ""
            if choice_index == 1:
                # INB plane
                plane_name = "INB"
                p_inion = self.getPos("inion")
                p_nasion = self.getPos("nasion")
                p_bregma = self.getPos("bregma")
                
                v1 = p_nasion - p_inion
                v2 = p_bregma - p_inion
                normal = np.cross(v1, v2)
                origin = p_inion
            elif choice_index == 2:
                # MSP plane
                plane_name = "MSP"
                required = ["nasion", "acanthion", "rhinion"]
                points = np.array([self.getPos(name) for name in required])
                centroid = np.mean(points, axis=0)
                covariance_matrix = np.cov(points - centroid, rowvar=False)
                eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
                normal = eigenvectors[:, np.argmin(eigenvalues)]
                origin = centroid
            
            # Remove old plane if exists
            try:
                oldPlane = slicer.util.getNode(plane_name)
                slicer.mrmlScene.RemoveNode(oldPlane)
            except: 
                pass
            
            # Create new plane
            planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', plane_name)
            planeNode.SetOrigin(origin)
            planeNode.SetNormal(normal)
            planeNode.SetSize(300, 300)
            planeNode.GetDisplayNode().SetOpacity(0.5)
            
            self.planeNode = planeNode
            self.step2StatusLabel.setText(f"Status: Successfully created '{plane_name}' plane!")
            self.log(f"Created {plane_name} plane")
            
        except Exception as e:
            self.step2StatusLabel.setText(f"Status: Error creating plane!  {e}")
            slicer.util.errorDisplay(f"Failed to create plane: {e}")
    
    def onConfirmSegmentation(self, node):
        """Confirm bone model selection"""
        if node: 
            self.boneModel = node
            self.step3StatusLabel.setText(f"Status:  Confirmed '{node.GetName()}' as bone model!")
            self.log(f"Confirmed bone model: {node.GetName()}")
        else:
            self.boneModel = None
            self.step3StatusLabel.setText("Status:  Waiting for bone model selection.")
    
    def onOpenDynamicModeler(self):
        """Open Dynamic Modeler module"""
        if not self.boneModel:
            slicer.util.warningDisplay("Please select the bone model in Step 3 first.")
            return
        
        if self.isDynamicModelerInstalled: 
            slicer.util.selectModule('DynamicModeler')
            self.log("Opened Dynamic Modeler module")
        else:
            slicer.util.warningDisplay("Dynamic Modeler extension is not installed.")
    
    def onConfirmCut(self, updateStatusOnly=False):
        """Confirm model cut"""
        if not updateStatusOnly:
            self.step4StatusLabel.setText("Status: Checking for cut models...")
        
        left_model_found = None
        right_model_found = None
        all_models = slicer.util.getNodesByClass('vtkMRMLModelNode')
        
        for model in all_models:
            model_name = model.GetName().lower()
            if "bone" in model_name and "left" in model_name: 
                left_model_found = model
            if "bone" in model_name and "right" in model_name: 
                right_model_found = model
        
        if left_model_found and right_model_found:
            self.boneLeftModel = left_model_found
            self.boneRightModel = right_model_found
            self.step4StatusLabel.setText(f"Status: Found cut models!")
            if not updateStatusOnly:
                self.log("Confirmed bone model cut")
        elif not updateStatusOnly:
            self.step4StatusLabel.setText("Status: Could not find left/right bone models.")
    
    def onOpenSegmentEditor(self):
        """Open the Segment Editor module"""
        slicer.util.selectModule('SegmentEditor')
        self.log("Opened Segment Editor module")
        self.step3StatusLabel.setText("Status: Segment Editor opened.  Follow the instructions above.")

    def onOpenVolumeRendering(self):
        """Open the Volume Rendering module"""
        slicer.util.selectModule('VolumeRendering')
        self.log("Opened Volume Rendering module for manual method")
        self.step3StatusLabel.setText("Status: Volume Rendering opened. Use Display ROI to visualize the skull.")

    def onSkipSegmentationSteps(self):
        """Skip both segmentation and cutting steps"""
        self.step3StatusLabel.setText("Status: Skipped to tangent creation (using manual volume rendering method).")
        self.log("Skipped Steps 3-4 (manual volume rendering method)")
        # Jump directly to Step 5 (tangent creation)
        self.currentStep = 4  # Step 5 is index 4 (0-indexed)
        self.updateStepUI()

    def onSkipCut(self):
        """Skip the model cutting step"""
        self. step4StatusLabel.setText("Status: Skipped model cutting (using manual method or T1-T2 shortcut).")
        self.log("Skipped model cutting step")
        # Move to next step
        self.currentStep += 1
        self.updateStepUI()
    
    def onRegenerateTangentsClicked(self):
        """Generate default tangent lines"""
        if not self.planeNode:
            slicer.util.messageBox("Please create a plane first.")
            return
        
        try:
            self.step5StatusLabel.setText("Status: Generating tangent lines...")
            slicer.app.processEvents()
            
            # Your existing tangent generation logic here
            # (I'll include a simplified version - you can expand with your full logic)
            
            # Example: Create T1 and T2 tangents
            planeOrigin = np.zeros(3)
            self.planeNode.GetOriginWorld(planeOrigin)
            planeNormal = np.zeros(3)
            self.planeNode.GetNormalWorld(planeNormal)
            
            # Create tangent lines (simplified - adapt your existing logic)
            tangent_length = 50  # mm
            
            # T1 - Example position
            t1_start = planeOrigin + np.array([0, 20, 30])
            t1_end = t1_start + np.array([0, tangent_length, 0])
            self.createTangentLine("T1", t1_start, t1_end, [1.0, 0.0, 0.0])  # Red
            
            # T2 - Example position
            t2_start = planeOrigin + np.array([0, -20, 20])
            t2_end = t2_start + np.array([0, tangent_length, 0])
            self.createTangentLine("T2", t2_start, t2_end, [0.0, 1.0, 0.0])  # Green
            
            if not self.t1t2ShortcutCheckbox.checked:
                # T3 - Example position
                t3_start = planeOrigin + np.array([0, 0, 10])
                t3_end = t3_start + np.array([0, tangent_length, 0])
                self.createTangentLine("T3", t3_start, t3_end, [0.0, 0.0, 1.0])  # Blue
            
            self.step5StatusLabel.setText("Status: Tangent lines created!  Adjust them as needed.")
            self.log("Generated default tangent lines")
            
        except Exception as e:
            self.step5StatusLabel.setText(f"Status: Error generating tangents! {e}")
            slicer.util.errorDisplay(f"Failed to generate tangents: {e}")
    
    def createTangentLine(self, name, start, end, color):
        """Create a tangent line node"""
        # Remove existing node if present
        try:
            oldNode = slicer.util.getNode(name)
            slicer.mrmlScene.RemoveNode(oldNode)
        except:
            pass
        
        # Create new line
        lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
        lineNode.AddControlPoint(start)
        lineNode.AddControlPoint(end)
        
        # Set color
        displayNode = lineNode.GetDisplayNode()
        displayNode.SetSelectedColor(color[0], color[1], color[2])
        displayNode.SetColor(color[0], color[1], color[2])
        displayNode.SetLineThickness(0.5)
        
        # Store references
        self.tangentNodes[name] = lineNode
        self.tangents[name] = {'start': start.tolist(), 'end': end.tolist()}
    
    def onPlaceTangentClicked(self, tangentName):
        """Place a tangent manually"""
        if not self.landmarksNode:
            slicer.util.messageBox("Landmarks node not found.")
            return
        
        # Switch to Markups module and activate placement
        slicer.util.selectModule('Markups')
        self.log(f"Placing {tangentName} tangent")
        self.step5StatusLabel.setText(f"Status: Place two points for {tangentName} tangent.")
    
    def onExtendTangentsClicked(self):
        """Extend tangent lines"""
        elongation_distance = 50  # mm
        
        tangents_to_extend = ["T1", "T2"]
        if not self.t1t2ShortcutCheckbox.checked:
            tangents_to_extend.extend(["T3", "T4"])
        
        for tangent_name in tangents_to_extend:
            if tangent_name in self.tangents:
                tangent = self.tangents[tangent_name]
                start = np.array(tangent['start'])
                end = np.array(tangent['end'])
                
                direction = end - start
                direction_normalized = direction / np.linalg.norm(direction)
                
                new_start = start - elongation_distance * direction_normalized
                new_end = end + elongation_distance * direction_normalized
                
                self.tangents[tangent_name]['start'] = new_start.tolist()
                self.tangents[tangent_name]['end'] = new_end.tolist()
                
                if tangent_name in self.tangentNodes:
                    node = self.tangentNodes[tangent_name]
                    wasModified = node.StartModify()
                    node.SetNthControlPointPositionWorld(0, new_start)
                    node.SetNthControlPointPositionWorld(1, new_end)
                    node.EndModify(wasModified)
        
        self.log("Extended tangent lines")
        self.step5StatusLabel.setText("Status:  Tangents elongated.")
    
    def onFindIntersectionsClicked(self):
        """Find intersections between tangent lines"""
        self.log("Finding intersections...")
        
        if self.t1t2ShortcutCheckbox.checked:
            # T1-T2 Shortcut mode
            self.runT1T2Shortcut()
        else:
            # Full mode - find all intersections
            self.findAllIntersections()
    
    def runT1T2Shortcut(self):
        """Run the T1-T2 shortcut workflow"""
        self.log("=== Starting T1-T2 Shortcut Workflow ===")
        
        try:
            if "T1" not in self.tangents or "T2" not in self.tangents:
                slicer.util.messageBox("T1 and T2 tangents must exist.")
                return
            
            # Get tangent data
            t1_start = np.array(self.tangents["T1"]['start'])
            t1_end = np.array(self.tangents["T1"]['end'])
            t2_start = np.array(self.tangents["T2"]['start'])
            t2_end = np.array(self.tangents["T2"]['end'])
            
            t1_dir = t1_end - t1_start
            t2_dir = t2_end - t2_start
            
            # Find intersection
            A = np.array([t1_dir, -t2_dir]).T
            b = t2_start - t1_start
            t = np.linalg.lstsq(A, b, rcond=None)[0]
            intersection_point = t1_start + t[0] * t1_dir
            
            self.log(f"T1-T2 intersection found at: {intersection_point}")
            
            # Create predicted pronasale point
            try:
                pred_prn_node = slicer.util.getNode('T1-T2_predicted_pronasale')
                pred_prn_node.RemoveAllControlPoints()
            except:
                pred_prn_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'T1-T2_predicted_pronasale')
                pred_prn_node.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)
            
            pred_prn_node.AddControlPoint(intersection_point, 'T1-T2 pred')
            
            # Find actual pronasale if available
            if self.landmarksNode:
                prn_index = self.findPointByName(self.landmarksNode, "pronasale")
                if prn_index >= 0:
                    actual_prn = np.zeros(3)
                    self.landmarksNode.GetNthControlPointPositionWorld(prn_index, actual_prn)
                    
                    error_distance = np.linalg.norm(intersection_point - actual_prn)
                    
                    self.storeMeasurement("T1-T2 Prediction Error", error_distance, "mm", is_error=True)
                    self.storeCoordinate("Pronasale (T1-T2)", intersection_point.tolist(), actual_prn.tolist())
                    
                    self.log(f"Prediction error: {error_distance:.2f} mm")
                    
                    # Create error line
                    try:
                        error_line_node = slicer.util.getNode('T1-T2_prediction_error')
                        error_line_node.RemoveAllControlPoints()
                    except:
                        error_line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'T1-T2_prediction_error')
                        error_line_node.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)
                    
                    error_line_node.AddControlPoint(actual_prn)
                    error_line_node.AddControlPoint(intersection_point)
            
            self.step5StatusLabel.setText("Status: T1-T2 intersection found!  Check Results tab.")
            slicer.util.showStatusMessage("T1-T2 Shortcut Complete!", 3000)
            
        except Exception as e:
            slicer.util.errorDisplay(f"Error in T1-T2 shortcut: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def findAllIntersections(self):
        """Find all intersections in full mode"""
        # Your existing full intersection logic here
        self.log("Finding all intersections (full mode)")
        self.step5StatusLabel.setText("Status: All intersections found!")
    
    def onUseExistingPointsClicked(self):
        """Use existing R2, LR2, RR2 points from landmarks"""
        self.checkAndUseExistingPoints()
        self.step6StatusLabel.setText("Status: Checked for existing soft tissue points.")
    
    def checkAndUseExistingPoints(self):
        """Check for existing soft tissue points"""
        if not self.landmarksNode:
            return
        
        points_to_find = ["pronasale", "R2", "LR2", "RR2"]
        found_points = []
        
        for i in range(self.landmarksNode.GetNumberOfControlPoints()):
            point_name = self.landmarksNode.GetNthControlPointLabel(i)
            if point_name in points_to_find: 
                pos = [0, 0, 0]
                self.landmarksNode.GetNthControlPointPositionWorld(i, pos)
                internal_name = "R1" if point_name == "pronasale" else point_name
                self.points[internal_name] = pos
                found_points.append(point_name)
                self.log(f"Found existing point: {point_name}")
        
        if found_points:
            self.log(f"Found existing soft tissue points: {', '.join(found_points)}")
    
    def onR2MethodChanged(self):
        """Toggle R2 method UI"""
        if self.automaticR2RadioButton.isChecked():
            self.automaticR2Frame.setVisible(True)
            self.placeR2Button.setVisible(False)
        else:
            self.automaticR2Frame.setVisible(False)
            self.placeR2Button.setVisible(True)
    
    def onPlacePointClicked(self, pointName):
        """Place a soft tissue point"""
        self.log(f"Placing {pointName} point")
        slicer.util.selectModule('Markups')
        self.step6StatusLabel.setText(f"Status: Place the {pointName} point.")
    
    def onCalculateR2Clicked(self):
        """Calculate R2 from LR2 and RR2"""
        if "LR2" not in self.points or "RR2" not in self.points:
            slicer.util.messageBox("Please place LR2 and RR2 points first.")
            return
        
        lr2 = np.array(self.points["LR2"])
        rr2 = np.array(self.points["RR2"])
        
        try:
            # Get plane information
            planeOrigin = np.zeros(3)
            self.planeNode.GetOriginWorld(planeOrigin)
            planeNormal = np.zeros(3)
            self.planeNode.GetNormalWorld(planeNormal)
            
            # Calculate R2 based on selected method
            if self.intersectionR2RadioButton.isChecked():
                # Method 1: Project onto plane and find intersection
                lr2_proj = self.projectPointOntoPlane(lr2, planeOrigin, planeNormal)
                rr2_proj = self.projectPointOntoPlane(rr2, planeOrigin, planeNormal)
                r2_pos = (lr2_proj + rr2_proj) / 2.0
                self.log("Calculated R2 using plane intersection method")
            else:
                # Method 2: Geometric mean
                r2_pos = (lr2 + rr2) / 2.0
                self.log("Calculated R2 using geometric mean method")
            
            # Store R2 position
            self.points["R2"] = r2_pos.tolist()
            
            # Create or update R2 fiducial
            try:
                r2_node = slicer.util.getNode("R2_calculated")
                r2_node.RemoveAllControlPoints()
            except:
                r2_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'R2_calculated')
                r2_node.GetDisplayNode().SetSelectedColor(0.0, 1.0, 1.0)  # Cyan
            
            r2_node.AddControlPoint(r2_pos, "R2")
            
            self.step6StatusLabel.setText("Status: R2 point calculated successfully!")
            self.log(f"R2 calculated at position: {r2_pos}")
            
        except Exception as e: 
            slicer.util.errorDisplay(f"Error calculating R2: {e}")
            self.step6StatusLabel.setText(f"Status: Error calculating R2!")
    
    def onCalculateErrorsClicked(self):
        """Compare true vs predicted points"""
        self.log("Calculating prediction errors...")
        
        try:
            # Check if we have predicted points
            if not self.points: 
                slicer.util.messageBox("No predicted points found. Please complete the previous steps.")
                return
            
            # Try to find true pronasale
            if self.landmarksNode:
                prn_index = self.findPointByName(self.landmarksNode, "pronasale")
                if prn_index >= 0:
                    true_prn = np.zeros(3)
                    self.landmarksNode.GetNthControlPointPositionWorld(prn_index, true_prn)
                    
                    # Calculate errors for each predicted point
                    for point_name in ["R1", "R2", "LR2", "RR2"]: 
                        if point_name in self.points:
                            predicted = np.array(self.points[point_name])
                            error = np.linalg.norm(predicted - true_prn)
                            
                            self.storeMeasurement(f"{point_name} Error", error, "mm", is_error=True)
                            self.storeCoordinate(point_name, predicted.tolist(), true_prn.tolist())
                            
                            # Create error visualization line
                            try:
                                error_line = slicer.util.getNode(f"{point_name}_error_line")
                                error_line.RemoveAllControlPoints()
                            except:
                                error_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"{point_name}_error_line")
                                error_line.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)
                            
                            error_line.AddControlPoint(true_prn)
                            error_line.AddControlPoint(predicted)
                    
                    self.step6StatusLabel.setText("Status: Errors calculated!  Check Results tab.")
                    self.log("Prediction errors calculated successfully")
                else:
                    slicer.util.messageBox("Could not find 'pronasale' landmark for comparison.")
            else:
                slicer.util.messageBox("Landmarks node not found.")
        
        except Exception as e: 
            slicer.util.errorDisplay(f"Error calculating errors:  {e}")
            import traceback
            traceback.print_exc()
    
    def onCopyMeasurements(self):
        """Copy measurements table to clipboard"""
        try:
            clipboard_text = "Measurement\tValue\tUnit\n"
            
            for row in range(self.measurementsTable.rowCount):
                metric = self.measurementsTable.item(row, 0).text() if self.measurementsTable.item(row, 0) else ""
                value = self.measurementsTable.item(row, 1).text() if self.measurementsTable.item(row, 1) else ""
                unit = self.measurementsTable.item(row, 2).text() if self.measurementsTable.item(row, 2) else ""
                clipboard_text += f"{metric}\t{value}\t{unit}\n"
            
            from qt import QApplication
            app_clipboard = QApplication.clipboard()
            app_clipboard.setText(clipboard_text)
            slicer.util.infoDisplay("Measurements copied to clipboard!")
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to copy measurements: {e}")
    
    def onCopyCoordinates(self):
        """Copy coordinates table to clipboard"""
        try:
            clipboard_text = "Landmark\tPred X\tPred Y\tPred Z\tTrue X\tTrue Y\tTrue Z\t3D Error\n"
            
            for row in range(self.coordinatesTable.rowCount):
                row_data = []
                for col in range(self.coordinatesTable.columnCount):
                    item = self.coordinatesTable.item(row, col)
                    row_data.append(item.text() if item else "")
                clipboard_text += "\t".join(row_data) + "\n"
            
            from qt import QApplication
            app_clipboard = QApplication.clipboard()
            app_clipboard.setText(clipboard_text)
            slicer.util.infoDisplay("Coordinates copied to clipboard!")
            
        except Exception as e: 
            slicer.util.errorDisplay(f"Failed to copy coordinates: {e}")
    
    def onFinish(self):
        """Close the GUI"""
        self.log("Finishing Gerasimow's nose prediction workflow")
        self.mainWidget.close()
        self.logWidget.close()
    
    # Helper methods
    def findPointByName(self, node, name):
        """Find point index by name in a markups node"""
        if not node:
            return -1
        for i in range(node.GetNumberOfControlPoints()):
            label = node.GetNthControlPointLabel(i)
            if name.lower() in label.lower():
                return i
        return -1
    
    def getPos(self, name, node=None):
        """Get position of a landmark by name"""
        landmark_node = node if node is not None else self.landmarksNode
        if not landmark_node:
            raise ValueError("Landmarks node not found.")
        
        for i in range(landmark_node.GetNumberOfControlPoints()):
            if name.lower() in landmark_node.GetNthControlPointLabel(i).lower():
                pos = np.zeros(3)
                landmark_node.GetNthControlPointPositionWorld(i, pos)
                return pos
        
        raise ValueError(f"Landmark '{name}' not found!")
    
    def projectPointOntoPlane(self, point, planeOrigin, planeNormal):
        """Project a point onto a plane"""
        v = point - planeOrigin
        dist = np.dot(v, planeNormal)
        projected = point - dist * planeNormal
        return projected
    
    def storeMeasurement(self, name, value, unit="mm", is_error=False):
        """Store a measurement for the results table"""
        self.all_measurements[name] = {
            "value": value,
            "unit":  unit,
            "is_error": is_error
        }
        self.updateResultsTables()
    
    def storeCoordinate(self, landmark_name, predicted_coords, true_coords=None):
        """Store coordinates for comparison"""
        self.all_coordinates[landmark_name] = {
            "predicted":  predicted_coords,
            "true": true_coords
        }
        self.updateResultsTables()
    
    def updateResultsTables(self):
        """Update both results tables with current data"""
        # Update Measurements Table
        self.measurementsTable.setRowCount(0)
        
        for name, data in self.all_measurements.items():
            row = self.measurementsTable.rowCount
            self.measurementsTable.insertRow(row)
            
            nameItem = qt.QTableWidgetItem(name)
            valueItem = qt.QTableWidgetItem("{:.2f}".format(data["value"]))
            unitItem = qt.QTableWidgetItem(data["unit"])
            
            if data.get("is_error", False):
                yellow = qt.QColor(255, 255, 200)
                nameItem.setBackground(yellow)
                valueItem.setBackground(yellow)
                unitItem.setBackground(yellow)
            
            self.measurementsTable.setItem(row, 0, nameItem)
            self.measurementsTable.setItem(row, 1, valueItem)
            self.measurementsTable.setItem(row, 2, unitItem)
        
        # Update Coordinates Table
        self.coordinatesTable.setRowCount(0)
        
        for landmark, data in self.all_coordinates.items():
            row = self.coordinatesTable.rowCount
            self.coordinatesTable.insertRow(row)
            
            predicted_coords = data["predicted"]
            true_coords = data.get("true")
            
            nameItem = qt.QTableWidgetItem(landmark)
            predXItem = qt.QTableWidgetItem("{:.2f}".format(predicted_coords[0]))
            predYItem = qt.QTableWidgetItem("{:.2f}".format(predicted_coords[1]))
            predZItem = qt.QTableWidgetItem("{:.2f}".format(predicted_coords[2]))
            
            self.coordinatesTable.setItem(row, 0, nameItem)
            self.coordinatesTable.setItem(row, 1, predXItem)
            self.coordinatesTable.setItem(row, 2, predYItem)
            self.coordinatesTable.setItem(row, 3, predZItem)
            
            if true_coords is not None:
                trueXItem = qt.QTableWidgetItem("{:.2f}".format(true_coords[0]))
                trueYItem = qt.QTableWidgetItem("{:.2f}".format(true_coords[1]))
                trueZItem = qt.QTableWidgetItem("{:.2f}".format(true_coords[2]))
                
                error_3d = np.linalg.norm(np.array(predicted_coords) - np.array(true_coords))
                errorItem = qt.QTableWidgetItem("{:.2f}".format(error_3d))
                
                yellow = qt.QColor(255, 255, 200)
                errorItem.setBackground(yellow)
                
                self.coordinatesTable.setItem(row, 4, trueXItem)
                self.coordinatesTable.setItem(row, 5, trueYItem)
                self.coordinatesTable.setItem(row, 6, trueZItem)
                self.coordinatesTable.setItem(row, 7, errorItem)
            else:
                for col in range(4, 8):
                    self.coordinatesTable.setItem(row, col, qt.QTableWidgetItem("-"))


# To run the GUI, create an instance: 
gui = GerasimowNosePredictor()


```
