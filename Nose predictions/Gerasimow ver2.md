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
        # Set this at the beginning to avoid errors
        self.minLogLevel = 1
        self.currentDialog = None
        self.intersections = {}  # Store intersections for error analysis
        
                
        # This is a more aggressive approach if needed:
        settings = qt.QSettings()
        settings.setValue("Markups/MarkupsFidNotificationPopupEnabled", 0)
        
        # Create main widget with scrollable area for better usability
        self.mainWidget = qt.QWidget()
        self.mainWidget.setWindowTitle("Gerasimow's Nose Prediction")
        self.mainWidget.setMinimumSize(550, 700)  # Narrower width, adequate height
        
        # Create scrollable area to handle different screen sizes
        scrollArea = qt.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollContent = qt.QWidget()
        mainLayout = qt.QVBoxLayout(scrollContent)
        mainLayout.setContentsMargins(10, 10, 10, 10)  # Less padding
        mainLayout.setSpacing(8)  # Reduced spacing between elements
        



        # Create decision log window - SIMPLIFIED
        self.logWidget = qt.QTextEdit()
        self.logWidget.setWindowTitle("Decision Log")
        self.logWidget.setReadOnly(True)
        self.logWidget.setMinimumSize(400, 300)  # Smaller size
        self.logWidget.show()
        
        self.decisions = []
        self.log("Starting Gerasimow's nose prediction process")
        
        # Add title and description - centered
        titleLabel = qt.QLabel("Gerasimow's Two Tangent Method")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 16px;")
        titleLabel.setAlignment(qt.Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)
        
        descriptionLabel = qt.QLabel("This method predicts the pronasale position using tangent lines.")
        descriptionLabel.setAlignment(qt.Qt.AlignCenter)
        mainLayout.addWidget(descriptionLabel)
        
        # Fixed width for most buttons
        buttonWidth = 250
        
        # STEP 1: LANDMARK SELECTION
        step1GroupBox = qt.QGroupBox("Step 1: Load Landmarks")
        step1Layout = qt.QVBoxLayout(step1GroupBox)
        step1Layout.setContentsMargins(8, 10, 8, 10)
        step1Layout.setSpacing(8)
        
        # Landmarks selector with label
        selectorLabel = qt.QLabel("Landmarks Node:")
        step1Layout.addWidget(selectorLabel)
        
        self.markupsSelector = slicer.qMRMLNodeComboBox()
        self.markupsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.markupsSelector.selectNodeUponCreation = True
        self.markupsSelector.noneEnabled = True
        self.markupsSelector.addEnabled = False
        self.markupsSelector.removeEnabled = False
        self.markupsSelector.setMRMLScene(slicer.mrmlScene)
        self.markupsSelector.setToolTip("Select the landmarks node")
        step1Layout.addWidget(self.markupsSelector)
        
        # GitHub download button - centered, fixed width
        self.downloadButton = qt.QPushButton("Download Landmarks from GitHub")
        self.downloadButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.downloadButton.setFixedWidth(buttonWidth)
        self.downloadButton.clicked.connect(self.onDownloadLandmarksClicked)
        step1Layout.addWidget(self.downloadButton, 0, qt.Qt.AlignHCenter)
        
        # Local file load button - centered, fixed width
        self.loadLocalButton = qt.QPushButton("Load Landmarks from Local File")
        self.loadLocalButton.setFixedWidth(buttonWidth)
        self.loadLocalButton.clicked.connect(self.onLoadLocalLandmarksClicked)
        step1Layout.addWidget(self.loadLocalButton, 0, qt.Qt.AlignHCenter)
        
        # Landmark bundle selection
        bundleLabel = qt.QLabel("Select landmark bundle for plane creation:")
        step1Layout.addWidget(bundleLabel)
        
        self.landmarkBundleCombo = qt.QComboBox()
        self.landmarkBundleCombo.addItem("Inion, Bregma, Nasion bundle (INB)")
        self.landmarkBundleCombo.addItem("Nasion, Acanthion, Rhinion bundle (MSP)")
        step1Layout.addWidget(self.landmarkBundleCombo)
        # Add a checkbox for T1-T2 shortcut mode
        self.t1t2ShortcutCheckbox = qt.QCheckBox("Use T1-T2 Shortcut (hides T3, T4, R2 options)")
        self.t1t2ShortcutCheckbox.setToolTip("When enabled, only T1 and T2 tangents are used for a quick pronasale prediction")
        self.t1t2ShortcutCheckbox.setChecked(False)
        self.t1t2ShortcutCheckbox.toggled.connect(self. onT1T2ShortcutToggled)
        step1Layout.addWidget(self.t1t2ShortcutCheckbox)
        
        # Create plane button - centered, fixed width
        self.createPlaneButton = qt.QPushButton("Create Plane from Landmarks")
        self.createPlaneButton.setStyleSheet("background-color: #FFDF00; font-weight: bold; padding: 8px;")
        self.createPlaneButton.setFixedWidth(buttonWidth)
        self.createPlaneButton.clicked.connect(self.onCreatePlaneClicked)
        step1Layout.addWidget(self.createPlaneButton, 0, qt.Qt.AlignHCenter)
        
        mainLayout.addWidget(step1GroupBox)
        
        # STEP 2: TANGENT CREATION
        step2GroupBox = qt.QGroupBox("Step 2: Create Tangent Lines")
        step2Layout = qt.QVBoxLayout(step2GroupBox)
        step2Layout.setContentsMargins(8, 10, 8, 10)
        step2Layout.setSpacing(8)
        
        
        # Tangent definitions - will be updated based on mode
        self.tangentsInfoLabel = qt. QLabel()
        self.updateTangentInfoText()  # Set initial text
        self.tangentsInfoLabel.setWordWrap(True)
        step2Layout.addWidget(self.tangentsInfoLabel)
        
        # VERTICAL TANGENT BUTTONS - each on its own line
        tangentControlFrame = qt.QFrame()
        tangentLayout = qt.QVBoxLayout(tangentControlFrame)
        tangentLayout.setSpacing(10)  # More space between buttons

        # --- NEW BUTTON: Regenerate Default Tangents ---
        self.regenTangentsButton = qt.QPushButton("Regenerate Default Tangents")
        self.regenTangentsButton.setStyleSheet("background-color: #E0E0E0; font-weight: bold; padding: 8px;")
        self.regenTangentsButton.setFixedWidth(buttonWidth)
        self.regenTangentsButton.setToolTip("Recreate T1, T2, T3 using default positions on the current plane.")
        self.regenTangentsButton.clicked.connect(self.onRegenerateTangentsClicked)
        tangentLayout.addWidget(self.regenTangentsButton, 0, qt.Qt.AlignHCenter)

        # Our new "message board" for instructions
        self.tangentInstructionLabel = qt.QLabel("...")
        self.tangentInstructionLabel.setStyleSheet("font-style: italic; color: #555555;")
        self.tangentInstructionLabel.setWordWrap(True)
        self.tangentInstructionLabel.setAlignment(qt.Qt.AlignCenter)
        self.tangentInstructionLabel.setVisible(False) # Hide it until we need it
        tangentLayout.addWidget(self.tangentInstructionLabel)

           
        # T4R Button - Purple
        self.t4rButton = qt.QPushButton("Place T4R (Purple)")
        self.t4rButton.setStyleSheet("background-color: #9966CC; font-weight: bold; padding: 8px;")
        self.t4rButton.setFixedWidth(buttonWidth)
        self.t4rButton.clicked.connect(lambda: self.onPlaceTangentClicked("T4R"))
        tangentLayout.addWidget(self.t4rButton, 0, qt.Qt.AlignHCenter)
        
        step2Layout.addWidget(tangentControlFrame)
        
        
        # T4L options in a better layout
        self.t4lOptionsGroup = qt.QGroupBox("Optional: T4L for Bilateral Analysis")
        t4lLayout = qt.QVBoxLayout(self.t4lOptionsGroup)
        t4lLayout.setContentsMargins(8, 8, 8, 8)
        t4lLayout.setSpacing(8)
        
        # T4L button - centered
        self.t4lButton = qt.QPushButton("Place T4L (Purple)")
        self.t4lButton.setStyleSheet("background-color: #9966CC; font-weight: bold; padding: 8px;")
        self.t4lButton.setFixedWidth(buttonWidth)
        self.t4lButton.clicked.connect(lambda: self.onPlaceTangentClicked("T4L"))
        t4lLayout.addWidget(self.t4lButton, 0, qt.Qt.AlignHCenter)
        
        # Remove T4L
        self.removeT4LButton = qt.QPushButton("Remove T4L")
        self.removeT4LButton.setToolTip("Click to remove the T4L tangent from the scene")
        self.removeT4LButton.setStyleSheet("background-color: #D9534F; color: white;") # A red-ish color
        self.removeT4LButton.setFixedWidth(buttonWidth)
        self.removeT4LButton.clicked.connect(lambda: self.removeTangent("T4L"))
        t4lLayout.addWidget(self.removeT4LButton, 0, qt.Qt.AlignHCenter)


        
        step2Layout.addWidget(self.t4lOptionsGroup)
        mainLayout.addWidget(step2GroupBox)
        
    

        # T4 calculation method section
        t4CalcGroupBox = qt.QGroupBox("T4 Calculation Method (when using T4L)")
        t4CalcLayout = qt.QVBoxLayout(t4CalcGroupBox)
        self.geometricMeanRadioButton = qt.QRadioButton("Geometric Mean")
        self.mutualAreaRadioButton = qt.QRadioButton("Mutual Intersection Area")
        self.geometricMeanRadioButton.setChecked(True)
        t4CalcLayout.addWidget(self.geometricMeanRadioButton)
        t4CalcLayout.addWidget(self.mutualAreaRadioButton)
        t4lLayout.addWidget(t4CalcGroupBox) # Add the box here

        self.createT4Button = qt.QPushButton("Create T4 Line from Tangents")
        self.createT4Button.setStyleSheet("background-color: #CC66AA; font-weight: bold; padding: 8px;")
        self.createT4Button.setFixedWidth(buttonWidth)
        self.createT4Button.clicked.connect(self.onCreateT4Clicked)
        t4lLayout.addWidget(self.createT4Button, 0, qt.Qt.AlignHCenter)

        # Extend Tangents Button - The one and only!
        self.extendTangentsButton = qt.QPushButton("Elongate Tangents if Needed")
        self.extendTangentsButton.setStyleSheet("background-color: #66CCBB; font-weight: bold; padding: 8px;")
        self.extendTangentsButton.setFixedWidth(buttonWidth)
        self.extendTangentsButton.clicked.connect(self.onExtendTangentsClicked)
        t4lLayout.addWidget(self.extendTangentsButton, 0, qt.Qt.AlignHCenter)

        self.resetExtensionsButton = qt.QPushButton("Reset All Extensions")
        self.resetExtensionsButton.setStyleSheet("background-color: #f0ad4e; font-weight: bold; padding: 8px;") # Orange color
        self.resetExtensionsButton.setFixedWidth(buttonWidth)
        self.resetExtensionsButton.setToolTip("Restores tangents to their size before they were elongated.")
        self.resetExtensionsButton.clicked.connect(self.onResetExtensionsClicked)
        t4lLayout.addWidget(self.resetExtensionsButton, 0, qt.Qt.AlignHCenter)

        # Find Intersections Button
        self.findIntersectionsButton = qt.QPushButton("Find Intersections")
        self.findIntersectionsButton.setStyleSheet("background-color: #99CC66; font-weight: bold; padding: 8px;")
        self.findIntersectionsButton.setFixedWidth(buttonWidth)
        self.findIntersectionsButton.clicked.connect(self.onFindIntersectionsClicked)
        t4lLayout.addWidget(self.findIntersectionsButton, 0, qt.Qt.AlignHCenter)

       
                
        mainLayout.addWidget(step2GroupBox)

        # STEP 3: Soft Tissue Comparison
        self.step3GroupBox = qt.QGroupBox("Step 3: Soft Tissue Comparison")
        step3Layout = qt.QVBoxLayout(self.step3GroupBox)
        step3Layout.setContentsMargins(8, 10, 8, 10)
        step3Layout.setSpacing(8)
    
        adviceLabel = qt.QLabel(
            "<b>Please ensure you have allocated the following soft tissue landmarks:</b><br>"
            "• <b>RR2:</b> The point where the T4R line crosses the nasal soft tissue on the right.<br>"
            "• <b>LR2:</b> The point where the T4L line crosses the nasal soft tissue on the left.<br>"
            "• <b>R2:</b> (If only T4R was used) The point where the final T4 line crosses the nasal soft tissue on the midsagittal plane."
        )
        adviceLabel.setWordWrap(True) # Make sure the text wraps nicely
        step3Layout.addWidget(adviceLabel) # Add it to the Step 3 layout
        
        self.elongateNasalFloorButton = qt.QPushButton("Elongate Nasal Floor Tangents (T4R/L)")
        self.elongateNasalFloorButton.setStyleSheet("background-color: #66CCBB; font-weight: bold; padding: 8px;") # A nice teal color
        self.elongateNasalFloorButton.setFixedWidth(buttonWidth)
        self.elongateNasalFloorButton.setToolTip("Extends T4R and T4L anteriorly to help find soft tissue points.")
        self.elongateNasalFloorButton.clicked.connect(self.onElongateNasalFloorTangentsClicked)
        step3Layout.addWidget(self.elongateNasalFloorButton, 0, qt.Qt.AlignHCenter)
        
        # Use existing points button - centered
        self.useExistingPointsButton = qt.QPushButton("Use Existing R2, LR2, RR2 Points")
        self.useExistingPointsButton.setStyleSheet("background-color: #f0ad4e; font-weight: bold; padding: 8px;")
        self.useExistingPointsButton.setFixedWidth(buttonWidth)
        self.useExistingPointsButton.clicked.connect(self.onUseExistingPointsClicked)
        self.useExistingPointsButton.setToolTip("Use pre-existing points from the landmarks file if available")
        step3Layout.addWidget(self.useExistingPointsButton, 0, qt.Qt.AlignHCenter)
        
        # R2 method selection
        methodLabel = qt.QLabel("Choose method for R2 point placement:")
        methodLabel.setAlignment(qt.Qt.AlignCenter)
        step3Layout.addWidget(methodLabel)
        
        # Radio buttons
        radioFrame = qt.QFrame()
        radioLayout = qt.QVBoxLayout(radioFrame)
        radioLayout.setSpacing(4)
        
        self.r2MethodButtonGroup = qt.QButtonGroup()
        self.manualR2RadioButton = qt.QRadioButton("Place R2 manually")
        self.automaticR2RadioButton = qt.QRadioButton("Calculate from LR2 and RR2")
        
        self.r2MethodButtonGroup.addButton(self.manualR2RadioButton, 1)
        self.r2MethodButtonGroup.addButton(self.automaticR2RadioButton, 2)
        self.manualR2RadioButton.setChecked(True)
        
        radioLayout.addWidget(self.manualR2RadioButton, 0, qt.Qt.AlignHCenter)
        radioLayout.addWidget(self.automaticR2RadioButton, 0, qt.Qt.AlignHCenter)
        step3Layout.addWidget(radioFrame)
        
        # Manual R2 placement - centered
        self.placeR2Button = qt.QPushButton("Place R2 Point")
        self.placeR2Button.setFixedWidth(buttonWidth)
        self.placeR2Button.clicked.connect(lambda: self.onPlacePointClicked("R2"))
        step3Layout.addWidget(self.placeR2Button, 0, qt.Qt.AlignHCenter)
        
        # Automatic R2 calculation frame
        self.automaticR2Frame = qt.QFrame()
        automaticR2Layout = qt.QVBoxLayout(self.automaticR2Frame)
        automaticR2Layout.setSpacing(8)
        
        # LR2 and RR2 buttons - vertical placement
        self.placeLR2Button = qt.QPushButton("Place LR2 Point")
        self.placeLR2Button.setFixedWidth(buttonWidth)
        self.placeLR2Button.clicked.connect(lambda: self.onPlacePointClicked("LR2"))
        automaticR2Layout.addWidget(self.placeLR2Button, 0, qt.Qt.AlignHCenter)
        
        self.placeRR2Button = qt.QPushButton("Place RR2 Point")
        self.placeRR2Button.setFixedWidth(buttonWidth)
        self.placeRR2Button.clicked.connect(lambda: self.onPlacePointClicked("RR2"))
        automaticR2Layout.addWidget(self.placeRR2Button, 0, qt.Qt.AlignHCenter)
        
        # R2 calculation method
        r2CalcLabel = qt.QLabel("R2 calculation method:")
        r2CalcLabel.setAlignment(qt.Qt.AlignCenter)
        automaticR2Layout.addWidget(r2CalcLabel)
        
        r2RadioFrame = qt.QFrame()
        r2RadioLayout = qt.QVBoxLayout(r2RadioFrame)
        r2RadioLayout.setSpacing(4)
        
        self.r2CalcMethodButtonGroup = qt.QButtonGroup()
        self.intersectionR2RadioButton = qt.QRadioButton("Use intersection with plane")
        self.geometricR2RadioButton = qt.QRadioButton("Use geometric mean")
        
        self.r2CalcMethodButtonGroup.addButton(self.intersectionR2RadioButton, 1)
        self.r2CalcMethodButtonGroup.addButton(self.geometricR2RadioButton, 2)
        self.intersectionR2RadioButton.setChecked(True)
        
        r2RadioLayout.addWidget(self.intersectionR2RadioButton, 0, qt.Qt.AlignHCenter)
        r2RadioLayout.addWidget(self.geometricR2RadioButton, 0, qt.Qt.AlignHCenter)
        automaticR2Layout.addWidget(r2RadioFrame)
        
        # Calculate R2 button
        self.calculateR2Button = qt.QPushButton("Calculate R2 Point")
        self.calculateR2Button.setFixedWidth(buttonWidth)
        self.calculateR2Button.clicked.connect(self.onCalculateR2Clicked)
        automaticR2Layout.addWidget(self.calculateR2Button, 0, qt.Qt.AlignHCenter)
        
        self.automaticR2Frame.setVisible(False)
        step3Layout.addWidget(self.automaticR2Frame)
        
        self.r2MethodButtonGroup.buttonClicked.connect(self.onR2MethodChanged)
        
        self.calculateErrorsButton = qt.QPushButton("Compare True vs. Predicted Points")
        self.calculateErrorsButton.setToolTip("Draws lines to show the distance between true and predicted points")
        self.calculateErrorsButton.setStyleSheet("background-color: #f0ad4e; font-weight: bold; padding: 8px;")
        self.calculateErrorsButton.setFixedWidth(300)
        self.calculateErrorsButton.clicked.connect(self.onCalculateErrorsClicked)
        step3Layout.addWidget(self.calculateErrorsButton, 0, qt.Qt.AlignHCenter)



        mainLayout.addWidget(self.step3GroupBox)
        
        # RESULTS SECTION
        resultsGroupBox = qt.QGroupBox("Results & Export")
        resultsLayout = qt.QVBoxLayout(resultsGroupBox)
        resultsLayout.setContentsMargins(8, 10, 8, 10)
        resultsLayout.setSpacing(8)

        # Measurements Table
        measurementsLabel = qt.QLabel("<b>📏 Measurements (Distances & Angles)</b>")
        measurementsLabel. setStyleSheet("font-size:  14px;")
        resultsLayout.addWidget(measurementsLabel)

        instructionsLabel = qt.QLabel(
            "Prediction errors are <span style='background-color: #ffffcc;'>highlighted in yellow</span>."
        )
        instructionsLabel.setWordWrap(True)
        resultsLayout.addWidget(instructionsLabel)

        self.measurementsTable = qt. QTableWidget()
        self.measurementsTable.setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Value", "Unit"])
        self.measurementsTable.horizontalHeader().setStretchLastSection(False)
        try:
            self.measurementsTable.horizontalHeader().setSectionResizeMode(0, qt. QHeaderView.Stretch)
        except:
            self.measurementsTable.horizontalHeader().setResizeMode(0, qt. QHeaderView.Stretch)
        self.measurementsTable.setMinimumHeight(200)
        self.measurementsTable.setAlternatingRowColors(True)
        resultsLayout.addWidget(self.measurementsTable)

        # Coordinates Table
        coordinatesLabel = qt.QLabel("<b>📍 Coordinates Comparison (Predicted vs True)</b>")
        coordinatesLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        resultsLayout.addWidget(coordinatesLabel)

        coordDesc = qt.QLabel("3D positions in RAS coordinate system (Right, Anterior, Superior)")
        coordDesc.setWordWrap(True)
        resultsLayout.addWidget(coordDesc)

        self.coordinatesTable = qt.QTableWidget()
        self.coordinatesTable.setColumnCount(8)
        self.coordinatesTable.setHorizontalHeaderLabels([
            "Landmark", 
            "Predicted X", "Predicted Y", "Predicted Z",
            "True X", "True Y", "True Z",
            "3D Error (mm)"
        ])
        try:
            self.coordinatesTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView. Stretch)
        except:
            self.coordinatesTable.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.coordinatesTable.setMinimumHeight(150)
        self.coordinatesTable.setAlternatingRowColors(True)
        resultsLayout.addWidget(self. coordinatesTable)

        # Copy Buttons
        buttonLayout = qt.QHBoxLayout()

        self.copyMeasurementsButton = qt. QPushButton("📋 Copy Measurements")
        self.copyMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color:  white; padding: 8px; font-weight: bold;"
        )
        self.copyMeasurementsButton.setToolTip("Copy measurements table to clipboard (TSV format)")
        self.copyMeasurementsButton.clicked.connect(self.onCopyMeasurements)
        buttonLayout.addWidget(self.copyMeasurementsButton)

        self.copyCoordinatesButton = qt.QPushButton("📋 Copy Coordinates")
        self.copyCoordinatesButton.setStyleSheet(
            "background-color: #3498db; color: white; padding:  8px; font-weight:  bold;"
        )
        self.copyCoordinatesButton.setToolTip("Copy coordinates table to clipboard (TSV format)")
        self.copyCoordinatesButton.clicked.connect(self.onCopyCoordinates)
        buttonLayout.addWidget(self.copyCoordinatesButton)

        resultsLayout.addLayout(buttonLayout)

        mainLayout.addWidget(resultsGroupBox)

        # Complete the scroll area setup
        scrollArea.setWidget(scrollContent)
        outerLayout = qt.QVBoxLayout(self.mainWidget)
        outerLayout.setContentsMargins(0, 0, 0, 0)
        outerLayout.addWidget(scrollArea)
        
        # Store state
        self.tangents = {}
        self.points = {}
        self.tangentNodes = {}
        self.tangent_backups = {}
        self.planeNode = None
        self.landmarksNode = None
        self.all_measurements = {}
        self.all_coordinates = {}


        # Run our new "smart inventory" check!
        self.syncWithScene()
        
        # Show the widget
        self.mainWidget.show()
        
        
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



    def onCreateT4Clicked(self):
        """Creates the final T4 tangent line, making sure to remember it."""
        self.log("'Create T4 Line' button clicked.")

        # --- Safety Checks ---
        if self.planeNode is None:
            slicer.util.messageBox("Please create a plane first using Step 1.")
            return

        if "T4R" not in self.tangents:
            slicer.util.messageBox("Please place the T4R tangent first using Step 2.")
            return

        try:
            # --- Get Plane Information ---
            planeNormal = np.zeros(3)
            self.planeNode.GetNormalWorld(planeNormal)
            planeOrigin = np.zeros(3)
            self.planeNode.GetOriginWorld(planeOrigin)

            # --- Calculate T4 start and end points ---
            t4_start_point, t4_end_point = None, None
            use_bilateral = "T4L" in self.tangents

            if use_bilateral:
                self.log("Calculating T4 using bilateral method (T4R and T4L).")
                t4r_start_proj = self.projectPointOntoPlane(self.tangents["T4R"]['start'], planeOrigin, planeNormal)
                t4r_end_proj = self.projectPointOntoPlane(self.tangents["T4R"]['end'], planeOrigin, planeNormal)
                t4l_start_proj = self.projectPointOntoPlane(self.tangents["T4L"]['start'], planeOrigin, planeNormal)
                t4l_end_proj = self.projectPointOntoPlane(self.tangents["T4L"]['end'], planeOrigin, planeNormal)

                t4_start_point = (t4r_start_proj + t4l_start_proj) / 2.0
                t4_end_point = (t4r_end_proj + t4l_end_proj) / 2.0
            else:
                self.log("Calculating T4 using unilateral method (T4R only).")
                t4_start_point = self.projectPointOntoPlane(self.tangents["T4R"]['start'], planeOrigin, planeNormal)
                t4_end_point = self.projectPointOntoPlane(self.tangents["T4R"]['end'], planeOrigin, planeNormal)

            # --- THIS IS THE FIX ---
            # We tell the "Store Manager" to write down the T4 line on its clipboard.
            self.tangents["T4"] = {'start': t4_start_point, 'end': t4_end_point}
            self.log("Stored final T4 line data in memory.")
            # --- END OF FIX ---

            # --- Visualize the Final T4 Line ---
            # This part just draws the line on the screen.
            self.createTangentLine("T4", t4_start_point, t4_end_point, [0.6, 0.4, 0.8]) # Purple
            slicer.util.showStatusMessage("Final T4 tangent created successfully!", 3000)

        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred while creating T4: {e}")
            import traceback
            traceback.print_exc()
            
    def checkAndUseExistingPoints(self):
        """
        Checks the loaded landmarks node for important points like R2, LR2, RR2, and pronasale,
        and stores them in the script's memory.
        """
        if not self.landmarksNode:
            self.log("Cannot check for existing points, no landmarks node is loaded.", 2)
            return
        
        # These are the special points we are looking for.
        points_to_find = ["pronasale", "R2", "LR2", "RR2"]
        found_points = []
        
        self.log(f"Searching for {points_to_find} in '{self.landmarksNode.GetName()}'...")
        
        # Loop through all the points in the loaded landmark file.
        for i in range(self.landmarksNode.GetNumberOfControlPoints()):
            point_name = self.landmarksNode.GetNthControlPointLabel(i)
            
            # Check if the point's name is one of the ones we're looking for.
            if point_name in points_to_find:
                pos = [0, 0, 0]
                self.landmarksNode.GetNthControlPointPositionWorld(i, pos)
                
                # Use "R1" as the internal name for "pronasale" for consistency.
                internal_name = "R1" if point_name == "pronasale" else point_name
                
                # Store the point's position in our script's memory ("the clipboard").
                self.points[internal_name] = pos
                found_points.append(point_name)
                self.log(f"Found and stored '{point_name}' at position {pos}.")

        if found_points:
            self.log(f"Finished search. Found existing points: {', '.join(found_points)}", 1)
            # We can show a popup, but for now, the log is enough.
            # slicer.util.showStatusMessage(f"Automatically used existing points: {', '.join(found_points)}", 4000)
        else:
            self.log("Finished search. No pre-existing soft tissue points found.")

    def syncWithScene(self):
        """
        Checks the Slicer scene for existing nodes using a more robust method
        that doesn't stop if a node is not found.
        """
        self.log("Checking scene for existing nodes...")
        found_nodes = []

        # A helper function to safely find a node
        def safeGetNode(name):
            try:
                return slicer.util.getNode(name)
            except slicer.util.MRMLNodeNotFoundException:
                return None # Return nothing if not found, instead of crashing

        # 1. Check for the main Landmarks Node
        landmarksNode = safeGetNode("Gerasimow_landmarks")
        if landmarksNode:
            self.landmarksNode = landmarksNode
            self.markupsSelector.setCurrentNode(landmarksNode)
            found_nodes.append("Landmarks File")

        # 2. Check for the Plane (INB or MSP)
        planeNode = safeGetNode("INB") or safeGetNode("MSP")
        if planeNode:
            self.planeNode = planeNode
            found_nodes.append(f"Plane ({planeNode.GetName()})")

        # 3. Check for Tangent Lines
        tangent_names = ["T1", "T2", "T3", "T4R", "T4L", "T4_Tangent"]
        for name in tangent_names:
            node = safeGetNode(name)
            if node:
                # Store the node so we can interact with it
                self.tangentNodes[name] = node
                # Also store its position data
                if node.GetNumberOfControlPoints() >= 2:
                    start = [0,0,0]
                    end = [0,0,0]
                    node.GetNthControlPointPositionWorld(0, start)
                    node.GetNthControlPointPositionWorld(1, end)
                    self.tangents[name] = {'start': start, 'end': end}
                found_nodes.append(f"Tangent ({name})")

        if found_nodes:
            self.log(f"Found existing items: {', '.join(found_nodes)}")
        else:
            self.log("No existing items found. Starting fresh.")

    def createT4FromGeometricMean(self, planeNormal):
        """Create T4 using geometric mean of T4R and T4L vectors"""
        # Get directional vectors for T4R and T4L
        t4r = self.tangents["T4R"]
        t4l = self.tangents["T4L"]
        
        # Extract start and end points for both tangents
        t4r_start = np.array(t4r['start']) if isinstance(t4r, dict) else np.array(t4r.GetPoint1())
        t4r_end = np.array(t4r['end']) if isinstance(t4r, dict) else np.array(t4r.GetPoint2())
        t4l_start = np.array(t4l['start']) if isinstance(t4l, dict) else np.array(t4l.GetPoint1())
        t4l_end = np.array(t4l['end']) if isinstance(t4l, dict) else np.array(t4l.GetPoint2())
        
        # Calculate vectors
        t4r_vector = t4r_end - t4r_start
        t4l_vector = t4l_end - t4l_start
        
        # Calculate geometric mean (normalize vectors and average them)
        t4r_norm = t4r_vector / np.linalg.norm(t4r_vector)
        t4l_norm = t4l_vector / np.linalg.norm(t4l_vector)
        t4_vector = (t4r_norm + t4l_norm) / 2.0
        t4_vector = t4_vector / np.linalg.norm(t4_vector)
        
        # Create T4 tangent using the calculated direction
        t4_origin = (t4r_start + t4l_start) / 2.0
        
        # Project vector to plane
        t4_vector = self.projectVectorOntoPlane(t4_vector, planeNormal)
        t4_vector = t4_vector / np.linalg.norm(t4_vector)
        
        # Project origin to plane
        planeOrigin = np.zeros(3)
        self.planeNode.GetOrigin(planeOrigin)
        t4_origin = self.projectPointOntoPlane(t4_origin, planeOrigin, planeNormal)
        
        # Create the new tangent
        tangent = vtk.vtkLineSource()
        tangent.SetPoint1(t4_origin)
        tangent.SetPoint2(t4_origin + 30 * t4_vector)  # 30mm length
        self.tangents["T4"] = tangent
        self.log("Created T4 using geometric mean of T4R and T4L, constrained to MSP/INB plane")

    def createT4FromT4R(self, planeNormal):
        """Create T4 based on T4R but constrained to the plane"""
        # Get T4R
        t4r = self.tangents["T4R"]
        
        # Extract start and end points
        t4r_start = np.array(t4r['start']) if isinstance(t4r, dict) else np.array(t4r.GetPoint1())
        t4r_end = np.array(t4r['end']) if isinstance(t4r, dict) else np.array(t4r.GetPoint2())
        
        # Calculate vector
        t4r_vector = t4r_end - t4r_start
        
        # Project the vector onto the plane
        t4_vector = self.projectVectorOntoPlane(t4r_vector, planeNormal)
        
        # Normalize the projected vector
        t4_vector = t4_vector / np.linalg.norm(t4_vector)
        
        # Project the origin point onto the plane
        planeOrigin = np.zeros(3)
        self.planeNode.GetOrigin(planeOrigin)
        t4_origin = self.projectPointOntoPlane(t4r_start, planeOrigin, planeNormal)
        
        # Create the T4 tangent
        tangent = vtk.vtkLineSource()
        tangent.SetPoint1(t4_origin)
        tangent.SetPoint2(t4_origin + 30.0 * t4_vector)  # 30mm length
        self.tangents["T4"] = tangent
        
        self.log("Created T4 from T4R, constrained to MSP/INB plane")

    def createT4FromIntersectionArea(self, planeNormal):
        """Create T4 using the mutual intersection area of T4R and T4L"""
        # Simplified implementation for beginners
        self.log("Using intersection area method to create T4")
        # For now, just use geometric mean as a fallback
        self.createT4FromGeometricMean(planeNormal) 
    

    def projectPointOntoPlane(self, point, planeOrigin, planeNormal):
        """Project a point onto a plane"""
        # Vector from plane origin to point
        v = point - planeOrigin
        
        # Calculate distance from point to plane
        dist = np.dot(v, planeNormal)
        
        # Project point onto plane
        projected = point - dist * planeNormal
        return projected       
    
    def projectVectorOntoPlane(self, vector, planeNormal):
            """Project a vector onto a plane with the given normal"""
            # Normalize plane normal
            normal = planeNormal / np.linalg.norm(planeNormal)
            
            # Calculate projection
            projection = vector - np.dot(vector, normal) * normal
            return projection
        
        
    def createT4FromT4R(self, planeNormal):
        """Create T4 based on T4R but constrained to the plane"""
        # Get T4R
        t4r = self.tangents["T4R"]
        
        # Extract start and end points
        t4r_start = np.array(t4r['start']) if isinstance(t4r, dict) else np.array(t4r.GetPoint1())
        t4r_end = np.array(t4r['end']) if isinstance(t4r, dict) else np.array(t4r.GetPoint2())
        
        # Calculate vector
        t4r_vector = t4r_end - t4r_start
        
        # Project the vector onto the plane
        t4_vector = self.projectVectorOntoPlane(t4r_vector, planeNormal)
        
        # Normalize the projected vector
        t4_vector = t4_vector / np.linalg.norm(t4_vector)
        
        # Project the origin point onto the plane
        planeOrigin = np.zeros(3)
        self.planeNode.GetOrigin(planeOrigin)
        t4_origin = self.projectPointOntoPlane(t4r_start, planeOrigin, planeNormal)
        
        # Create the T4 tangent
        tangent = vtk.vtkLineSource()
        tangent.SetPoint1(t4_origin)
        tangent.SetPoint2(t4_origin + 30.0 * t4_vector)  # 30mm length
        self.tangents["T4"] = tangent
        
        self.log("Created T4 from T4R, constrained to MSP/INB plane")

    def projectPointOntoPlane(self, point, planeOrigin, planeNormal):
        """Project a point onto a plane"""
        # Vector from plane origin to point
        v = point - planeOrigin
        
        # Calculate distance from point to plane
        dist = np.dot(v, planeNormal)
        
        # Project point onto plane
        projected = point - dist * planeNormal
        return projected

    def visualizeT4Tangent(self):
        """Create a visual representation of the T4 tangent as a line"""
        if "T4" in self.tangents:
            # Remove any existing T4 node
            if "T4" in self.tangentNodes:
                slicer.mrmlScene.RemoveNode(self.tangentNodes["T4"])
                
            # Get the points from the tangent
            tangent = self.tangents["T4"]
            point1 = tangent.GetPoint1()
            point2 = tangent.GetPoint2()
            
            # Create a markup line node (this is the proper way to represent lines)
            lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "T4_Tangent")
            
            # Add the two points to define the line
            lineNode.AddControlPoint(point1)
            lineNode.AddControlPoint(point2)
            
            # Style the line
            lineNode.GetDisplayNode().SetSelectedColor(0.6, 0.4, 0.8)  # Purple color
            lineNode.GetDisplayNode().SetLineWidth(3)
            lineNode.SetLocked(True)  # Prevent accidental movement
            
            # Store the node reference
            self.tangentNodes["T4"] = lineNode
            
            self.log("Created T4 line tangent")

    def onT1T2ShortcutClicked(self):
        """Run the complete T1-T2 shortcut workflow"""
        self.log("=== Starting T1-T2 Shortcut Workflow ===")
        
        try:
            # 1. Check prerequisites
            if not self.planeNode:
                slicer.util.messageBox("Please create a plane first (Step 1).")
                return
            
            if "T1" not in self.tangents or "T2" not in self. tangents:
                slicer.util.messageBox("Please ensure T1 and T2 tangents exist and are positioned correctly.")
                return
            
            # 2. Elongate T1 and T2 until they're long enough to intersect
            self. log("Elongating T1 and T2 tangents...")
            elongation_distance = 100  # mm
            for tangent_name in ["T1", "T2"]:
                tangent = self.tangents[tangent_name]
                start = np.array(tangent['start'])
                end = np. array(tangent['end'])
                
                # Calculate direction and elongate
                direction = end - start
                direction_normalized = direction / np.linalg.norm(direction)
                new_start = start - elongation_distance * direction_normalized
                new_end = end + elongation_distance * direction_normalized
                
                # Update tangent data
                self.tangents[tangent_name]['start'] = new_start. tolist()
                self.tangents[tangent_name]['end'] = new_end.tolist()
                
                # Update visualization
                if tangent_name in self.tangentNodes:
                    node = self.tangentNodes[tangent_name]
                    wasModified = node.StartModify()
                    node.SetNthControlPointPositionWorld(0, new_start)
                    node. SetNthControlPointPositionWorld(1, new_end)
                    node.EndModify(wasModified)
            
            self.log("T1 and T2 elongated")
            
            # 3. Find intersection point
            self.log("Finding T1-T2 intersection...")
            t1_start = np. array(self.tangents["T1"]['start'])
            t1_end = np.array(self.tangents["T1"]['end'])
            t2_start = np.array(self. tangents["T2"]['start'])
            t2_end = np.array(self.tangents["T2"]['end'])
            
            t1_dir = t1_end - t1_start
            t2_dir = t2_end - t2_start
            
            # Solve for intersection
            A = np. array([t1_dir, -t2_dir]).T
            b = t2_start - t1_start
            t = np.linalg.lstsq(A, b, rcond=None)[0]
            intersection_point = t1_start + t[0] * t1_dir
            
            self.log(f"Intersection found at: {intersection_point}")
            
            # 4. Create predicted pronasale point
            pred_prn_node = None
            try: 
                pred_prn_node = slicer.util.getNode('T1-T2_predicted_pronasale')
                pred_prn_node.RemoveAllControlPoints()
            except:
                pred_prn_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'T1-T2_predicted_pronasale')
                pred_prn_node.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)  # Orange
            
            pred_prn_node.AddControlPoint(intersection_point, 'T1-T2 pred')
            
            # 5. Find actual pronasale from landmarks
            if not self.landmarksNode:
                slicer. util.messageBox("Landmarks node not found. Cannot compare to actual pronasale.")
                return
            
            prn_index = self.findPointByName(self. landmarksNode, "pronasale")
            if prn_index < 0:
                slicer.util.messageBox("Could not find 'pronasale' in landmarks.  Cannot calculate error.")
                return
            
            actual_prn = np.zeros(3)
            self.landmarksNode.GetNthControlPointPositionWorld(prn_index, actual_prn)
            
            # 6. Calculate error
            error_distance = np.linalg. norm(intersection_point - actual_prn)
            # Store in results tables
            self.storeMeasurement("T1-T2 Prediction Error", error_distance, "mm", is_error=True)
            self.storeCoordinate("Pronasale (T1-T2)", intersection_point.tolist(), actual_prn.tolist())
            self.log(f"Prediction error: {error_distance:.2f} mm")
            
            # 7. Create error visualization line
            error_line_node = None
            try:
                error_line_node = slicer. util.getNode('T1-T2_prediction_error')
                error_line_node.RemoveAllControlPoints()
            except:
                error_line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'T1-T2_prediction_error')
                error_line_node.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                error_line_node.GetDisplayNode().SetColor(1.0, 0.0, 0.0)
            
            error_line_node.AddControlPoint(actual_prn)
            error_line_node.AddControlPoint(intersection_point)
            
            # 8. Show results in a copy-pasteable format
            result_text = (
                f"T1-T2 Shortcut Results\n"
                f"{'='*50}\n\n"
                f"Predicted Pronasale:\n"
                f"  X: {intersection_point[0]:.2f} mm\n"
                f"  Y: {intersection_point[1]:.2f} mm\n"
                f"  Z: {intersection_point[2]:.2f} mm\n\n"
                f"Actual Pronasale:\n"
                f"  X: {actual_prn[0]:.2f} mm\n"
                f"  Y: {actual_prn[1]:.2f} mm\n"
                f"  Z: {actual_prn[2]:.2f} mm\n\n"
                f"Prediction Error: {error_distance:.2f} mm\n"
                f"{'='*50}\n\n"
                f"CSV Format (for spreadsheet):\n"
                f"Metric,X,Y,Z,Total_Error\n"
                f"Predicted,{intersection_point[0]:.2f},{intersection_point[1]:.2f},{intersection_point[2]:.2f},-\n"
                f"Actual,{actual_prn[0]:.2f},{actual_prn[1]:.2f},{actual_prn[2]:.2f},-\n"
                f"Error,-,-,-,{error_distance:.2f}\n"
            )

            # Create a dialog with copy-pasteable text
            resultsDialog = qt.QDialog(self. mainWidget)
            resultsDialog.setWindowTitle("T1-T2 Prediction Results")
            resultsDialog.setMinimumWidth(500)
            resultsLayout = qt.QVBoxLayout(resultsDialog)

            # Add title label
            titleLabel = qt.QLabel("<h3>T1-T2 Shortcut Complete! </h3>")
            titleLabel.setAlignment(qt.Qt.AlignCenter)
            resultsLayout.addWidget(titleLabel)

            # Add text edit with results (read-only but selectable)
            resultsTextEdit = qt.QTextEdit()
            resultsTextEdit.setPlainText(result_text)
            resultsTextEdit.setReadOnly(True)
            resultsTextEdit.setMinimumHeight(300)
            resultsLayout.addWidget(resultsTextEdit)

            # Add info label
            infoLabel = qt. QLabel("You can select and copy the text above.  A red error line has been added to the 3D view.")
            infoLabel.setWordWrap(True)
            infoLabel.setStyleSheet("color: #666; font-style: italic;")
            resultsLayout.addWidget(infoLabel)

            # Add close button
            closeButton = qt.QPushButton("Close")
            closeButton.clicked.connect(resultsDialog.accept)
            resultsLayout.addWidget(closeButton)

            resultsDialog.exec_()

            self.log(f"=== T1-T2 Shortcut Complete.  Error: {error_distance:.2f} mm ===")
            
            
        except Exception as e: 
            slicer.util. errorDisplay(f"Error in T1-T2 shortcut:  {str(e)}")
            import traceback
            traceback. print_exc()

    def storeMeasurement(self, name, value, unit="mm", is_error=False):
        """Store a measurement for the results table"""
        self.all_measurements[name] = {
            "value":  value,
            "unit": unit,
            "is_error":  is_error
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
            row = self.measurementsTable.rowCount()
            self.measurementsTable.insertRow(row)
            
            nameItem = qt. QTableWidgetItem(name)
            valueItem = qt.QTableWidgetItem("{:. 2f}".format(data["value"]))
            unitItem = qt.QTableWidgetItem(data["unit"])
            
            # Highlight error measurements in yellow
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
            row = self.coordinatesTable.rowCount()
            self.coordinatesTable.insertRow(row)
            
            pred = data["predicted"]
            true = data.get("true")
            
            nameItem = qt. QTableWidgetItem(landmark)
            predXItem = qt. QTableWidgetItem("{:.2f}".format(pred[0]))
            predYItem = qt.QTableWidgetItem("{:. 2f}".format(pred[1]))
            predZItem = qt.QTableWidgetItem("{:.2f}".format(pred[2]))
            
            self.coordinatesTable.setItem(row, 0, nameItem)
            self.coordinatesTable. setItem(row, 1, predXItem)
            self.coordinatesTable.setItem(row, 2, predYItem)
            self.coordinatesTable. setItem(row, 3, predZItem)
            
            if true is not None:
                trueXItem = qt.QTableWidgetItem("{:.2f}".format(true[0]))
                trueYItem = qt.QTableWidgetItem("{:. 2f}".format(true[1]))
                trueZItem = qt.QTableWidgetItem("{:.2f}".format(true[2]))
                
                error_3d = np.linalg.norm(np.array(pred) - np.array(true))
                errorItem = qt.QTableWidgetItem("{:. 2f}".format(error_3d))
                
                # Highlight error in yellow
                yellow = qt.QColor(255, 255, 200)
                errorItem.setBackground(yellow)
                
                self.coordinatesTable.setItem(row, 4, trueXItem)
                self.coordinatesTable.setItem(row, 5, trueYItem)
                self.coordinatesTable.setItem(row, 6, trueZItem)
                self.coordinatesTable.setItem(row, 7, errorItem)
            else:
                for col in range(4, 8):
                    self. coordinatesTable.setItem(row, col, qt.QTableWidgetItem("-"))

    def onCopyMeasurements(self):
        """Copy measurements table to clipboard in TSV format"""
        text = "Measurement\tValue\tUnit\n"
        
        for name, data in self. all_measurements.items():
            text += "{}\t{:.2f}\t{}\n".format(name, data["value"], data["unit"])
        
        clipboard = qt.QApplication.clipboard()
        clipboard.setText(text)
        slicer.util. showStatusMessage("📋 Measurements copied to clipboard!", 2000)

    def onCopyCoordinates(self):
        """Copy coordinates table to clipboard in TSV format"""
        text = "Landmark\tPredicted X\tPredicted Y\tPredicted Z\tTrue X\tTrue Y\tTrue Z\t3D Error (mm)\n"
        
        for landmark, data in self.all_coordinates.items():
            pred = data["predicted"]
            true = data.get("true")
            
            line = "{}\t{:.2f}\t{:.2f}\t{:.2f}\t". format(landmark, pred[0], pred[1], pred[2])
            
            if true is not None: 
                error_3d = np.linalg.norm(np.array(pred) - np.array(true))
                line += "{:. 2f}\t{:.2f}\t{:.2f}\t{:.2f}\n".format(true[0], true[1], true[2], error_3d)
            else:
                line += "-\t-\t-\t-\n"
            
            text += line
        
        clipboard = qt.QApplication.clipboard()
        clipboard.setText(text)
        slicer.util.showStatusMessage("📋 Coordinates copied to clipboard!", 2000)
    
    def onT4LUsedToggled(self, checked):
            """Handle when user toggles the T4L checkbox"""
            # Update T4L button visibility
            if hasattr(self, 't4lButton'):
                self.t4lButton.setEnabled(checked)
            
            # Update radio buttons for T4 calculation method
            if hasattr(self, 'geometricMeanRadioButton'):
                self.geometricMeanRadioButton.setEnabled(checked)
                self.mutualAreaRadioButton.setEnabled(checked)
            
            # Show guidance to the user
            if checked:
                self.log("T4L enabled - bilateral method will be used")
                self.showGuidanceDialog(
                    "Bilateral method (T4R and T4L) enabled.\n\n"
                    "You'll need to place both right and left nasal floor tangents."
                    "The final T4 will be calculated as a combination of both."
                )
            else:
                self.log("T4L disabled - unilateral method will be used")
                # If we've already created T4L, ask if they want to remove it
                if "T4L" in self.tangentNodes:
                    self.showConfirmationDialog(
                        "Would you like to remove the existing T4L tangent?",
                        lambda: self.removeTangent("T4L")
                    )    
                    
    def showConfirmationDialog(self, message, yesAction):
            """Show a Yes/No confirmation dialog"""
            dialog = qt.QMessageBox(self.mainWidget)
            dialog.setText(message)
            dialog.setWindowTitle("Confirmation")
            yesButton = dialog.addButton("Yes", qt.QMessageBox.YesRole)
            dialog.addButton("No", qt.QMessageBox.NoRole)
            
            dialog.exec_()
            
            if dialog.clickedButton() == yesButton:
                yesAction()

    def removeTangent(self, tangentName):
            """Remove a tangent line from the scene"""
            if tangentName in self.tangentNodes:
                # Remove node from scene
                slicer.mrmlScene.RemoveNode(self.tangentNodes[tangentName])
                # Remove from our dictionaries
                del self.tangentNodes[tangentName]
                if tangentName in self.tangents:
                    del self.tangents[tangentName]
                self.log(f"Removed {tangentName} tangent")

    
    def calculateSceneBounds(self):
            """Calculate the bounds of the scene for tangent extension"""
            # Default bounds
            bounds = [-100, 100, -100, 100, -100, 100]
            
            # Try to get better bounds from visible nodes
            modelNodes = slicer.util.getNodesByClass('vtkMRMLModelNode')
            markupsNodes = slicer.util.getNodesByClass('vtkMRMLMarkupsNode')
            
            allNodes = list(modelNodes) + list(markupsNodes)
            if allNodes:
                # Start with first node's bounds
                firstBounds = [0, 0, 0, 0, 0, 0]
                allNodes[0].GetRASBounds(firstBounds)
                bounds = list(firstBounds)
                
                # Update with all other nodes
                for node in allNodes[1:]:
                    nodeBounds = [0, 0, 0, 0, 0, 0]
                    node.GetRASBounds(nodeBounds)
                    bounds[0] = min(bounds[0], nodeBounds[0])
                    bounds[1] = max(bounds[1], nodeBounds[1])
                    bounds[2] = min(bounds[2], nodeBounds[2])
                    bounds[3] = max(bounds[3], nodeBounds[3])
                    bounds[4] = min(bounds[4], nodeBounds[4])
                    bounds[5] = max(bounds[5], nodeBounds[5])
            
            return bounds


    def extendTangent(self, tangentName, extensionLength):
            """Extend a tangent line while preserving direction"""
            try:
                # Get the tangent data
                tangent = self.tangents[tangentName]
                
                # Handle different tangent storage formats
                if isinstance(tangent, dict):
                    start = np.array(tangent['start'])
                    end = np.array(tangent['end'])
                else:  # vtkLineSource
                    start = np.array(tangent.GetPoint1())
                    end = np.array(tangent.GetPoint2())
                
                # Calculate direction vector
                direction = end - start
                direction = direction / np.linalg.norm(direction)
                
                # Extend in both directions
                newStart = start - direction * extensionLength
                newEnd = end + direction * extensionLength
                
                # Update tangent
                if isinstance(tangent, dict):
                    self.tangents[tangentName]['start'] = newStart.tolist()
                    self.tangents[tangentName]['end'] = newEnd.tolist()
                    self.tangents[tangentName]['vector'] = (newEnd - newStart).tolist()
                else:  # vtkLineSource
                    tangent.SetPoint1(newStart)
                    tangent.SetPoint2(newEnd)
                
                self.log(f"Extended {tangentName} tangent")
            except Exception as e:
                self.log(f"Error extending {tangentName}: {str(e)}", 2)


    def updateTangentVisualization(self, tangentName):
        """Update the visualization of a tangent after extension, preventing warnings."""
        if tangentName in self.tangents and tangentName in self.tangentNodes:
            node = self.tangentNodes[tangentName]
            tangent_data = self.tangents[tangentName]

            if isinstance(node, slicer.vtkMRMLMarkupsLineNode):
                try:
                    # --- THE FIX ---
                    # 1. Get the "tracking number" when we start.
                    wasModified = node.StartModify()

                    start_point = tangent_data.get('start')
                    end_point = tangent_data.get('end')

                    if start_point and end_point:
                        node.SetNthControlPointPositionWorld(0, start_point)
                        node.SetNthControlPointPositionWorld(1, end_point)

                finally:
                    # 2. Give the "tracking number" back when we finish.
                    node.EndModify(wasModified)

                self.log(f"Updated visualization for {tangentName} tangent")    
    

    def showGuidanceDialog(self, message, nextAction=None):
            """Show a guidance dialog that doesn't block the application"""
            # Close any existing dialog first
            if hasattr(self, 'currentDialog') and self.currentDialog and self.currentDialog.isVisible():
                self.currentDialog.close()
                
            dialog = qt.QDialog(self.mainWidget)
            dialog.setWindowTitle("Placement Guidance")
            layout = qt.QVBoxLayout(dialog)
            
            # Add message
            label = qt.QLabel(message)
            label.setWordWrap(True)
            layout.addWidget(label)
            
            # Add Next button
            nextButton = qt.QPushButton("Next")
            nextButton.clicked.connect(lambda: dialog.accept())
            layout.addWidget(nextButton)
            
            # Make it stay on top but NOT modal
            dialog.setWindowFlags(qt.Qt.Tool | qt.Qt.WindowStaysOnTopHint)
            dialog.setMinimumWidth(400)
            
            # Run non-modally so it doesn't block the application
            dialog.setModal(False)
            dialog.show()
            
            # Store a reference to keep it alive
            self.currentDialog = dialog
            
            # If next action provided, connect it to button
            if nextAction:
                nextButton.clicked.connect(nextAction)
        
    def onT1T2ShortcutToggled(self, checked):
        """Handle when T1-T2 shortcut mode is toggled"""
        self. log(f"T1-T2 Shortcut mode: {'ENABLED' if checked else 'DISABLED'}")
        
        # Update the tangent info text
        self. updateTangentInfoText()
        
        # Hide/show T3, T4, and R2 related controls
        if hasattr(self, 't4rButton'):
            self.t4rButton.setVisible(not checked)
        if hasattr(self, 't4lButton'):
            self.t4lButton.setVisible(not checked)
        if hasattr(self, 't4lOptionsGroup'):
            self.t4lOptionsGroup. setVisible(not checked)
        if hasattr(self, 'step3GroupBox'):
            self.step3GroupBox.setVisible(not checked)
        
        # Show/hide the shortcut button
        if checked: 
            if not hasattr(self, 't1t2ShortcutButton'):
                # Create the shortcut button dynamically
                self.t1t2ShortcutButton = qt.QPushButton("Run T1-T2 Prediction & Compare to Pronasale")
                self.t1t2ShortcutButton.setStyleSheet("background-color: #FF6B35; color: white; font-weight: bold; padding: 10px;")
                self.t1t2ShortcutButton.setFixedWidth(350)
                self.t1t2ShortcutButton.clicked.connect(self.onT1T2ShortcutClicked)
                
                # Add to Step 2 layout (after the tangent controls)
                # We need to find step2GroupBox and add to its layout
                for widget in self.mainWidget.findChildren(qt.QGroupBox):
                    if widget.title == "Step 2: Create Tangent Lines":
                        layout = widget.layout()
                        layout.addWidget(self.t1t2ShortcutButton, 0, qt.Qt.AlignHCenter)
                        break
            
            self.t1t2ShortcutButton.setVisible(True)
        else:
            if hasattr(self, 't1t2ShortcutButton'):
                self.t1t2ShortcutButton.setVisible(False)

    def updateTangentInfoText(self):
        """Update the tangent info text based on current mode"""
        if hasattr(self, 't1t2ShortcutCheckbox') and self.t1t2ShortcutCheckbox.isChecked():
            text = (
                "<b>Tangent Definitions (T1-T2 Shortcut Mode):</b><br>"
                "• T1 (Yellow): Follows the last third of the nasal bone<br>"
                "• T2 (Green): Follows the direction of the anterior nasal spine"
            )
        else:
            text = (
                "<b>Tangent Definitions: </b><br>"
                "• T1 (Yellow): Follows the last third of the nasal bone<br>"
                "• T2 (Green): Follows the direction of the anterior nasal spine<br>"
                "• T3 (Lilac): Follows the last 1-2 mm of the nasal bone<br>"
                "• T4 (Purple): Follows the direction of the nasal floor"
            )
        
        if hasattr(self, 'tangentsInfoLabel'):
            self.tangentsInfoLabel.setText(text)
    
    def onDownloadLandmarksClicked(self):
            """Download landmarks from GitHub"""
            try:
                # Try primary URL first
                primaryUrl = "https://github.com/user-attachments/files/22232935/Gerasimow_landmarks.mrk.json"
                
                # Let user choose a URL if needed
                urlToUse = primaryUrl
                try:
                    response = urllib.request.urlopen(urlToUse)
                except:
                    urlToUse = qt.QInputDialog.getText(self.mainWidget, "Enter URL", 
                        "Primary URL not working. Please enter the URL to your landmarks file:",
                        qt.QLineEdit.Normal, "")[0]
                    if not urlToUse:
                        return
                        
                # Download from selected URL
                self.log(f"Downloading landmarks from {urlToUse}...")
                
                # Download the JSON file
                response = urllib.request.urlopen(urlToUse)
                jsonData = response.read().decode('utf-8')
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json') as temp:
                    temp.write(jsonData.encode('utf-8'))
                    tempFilename = temp.name
                
                # Load the markups file
                success = slicer.util.loadMarkups(tempFilename)
                if success:
                    # Get the loaded node
                    landmarksNode = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')[-1]
                    landmarksNode.SetName("Gerasimow_landmarks")
                    
                    self.landmarksNode = landmarksNode
                    self.markupsSelector.setCurrentNode(landmarksNode)
                    self.log(f"Successfully loaded {landmarksNode.GetNumberOfControlPoints()} landmarks from GitHub")
                    
                    # Automatically read the memo and find the important points.
                    self.checkAndUseExistingPoints()

                    # Show landmarks in 3D view
                    landmarksNode.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green color
                    landmarksNode.GetDisplayNode().SetVisibility(True)
                    landmarksNode.GetDisplayNode().SetPointLabelsVisibility(True)
                    
                    # Message to inform the user
                    self.showGuidanceDialog(f"Landmarks downloaded successfully!\n{landmarksNode.GetNumberOfControlPoints()} points loaded.")
                    
                    # Check for existing pronasale, R2, LR2, RR2 points
                    self.checkAndUseExistingPoints()
                    
                    # Preselect landmark bundle based on loaded landmarks
                    self.autoSelectLandmarkBundle()
                else:
                    slicer.util.errorDisplay("Failed to load landmarks file")
                
                # Clean up the temporary file
                os.unlink(tempFilename)
                
            except Exception as e:
                slicer.util.errorDisplay(f"Error downloading landmarks: {str(e)}")
        
    def onLoadLocalLandmarksClicked(self):
            """Load landmarks from local file"""
            try:
                fileName = qt.QFileDialog.getOpenFileName(self.mainWidget, "Load Landmarks", "", "JSON Files (*.json);;All Files (*.*)")
                
                if fileName:
                    # Load the markups file
                    success = slicer.util.loadMarkups(fileName)
                    if success:
                        # Get the loaded node
                        landmarksNode = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')[-1]
                        self.landmarksNode = landmarksNode
                        self.markupsSelector.setCurrentNode(landmarksNode)
                        self.log(f"Successfully loaded landmarks from {fileName}")
                        
                        # Show landmarks in 3D view
                        landmarksNode.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green color
                        landmarksNode.GetDisplayNode().SetVisibility(True)
                        landmarksNode.GetDisplayNode().SetPointLabelsVisibility(True)
                        
                        # Check for existing points
                        self.checkAndUseExistingPoints()
                        
                        # Preselect landmark bundle based on loaded landmarks
                        self.autoSelectLandmarkBundle()
                    else:
                        slicer.util.errorDisplay("Failed to load landmarks file")
                        
            except Exception as e:
                slicer.util.errorDisplay(f"Error loading landmarks: {str(e)}")


            
    def onUseExistingPointsClicked(self):
            """Use existing R2, LR2, RR2 points from landmarks file"""
            if not self.landmarksNode:
                slicer.util.errorDisplay("No landmarks loaded. Please load landmarks first.")
                return
            
            self.checkAndUseExistingPoints()
            
            # Visualize the points that were found
            for name, pos in self.points.items():
                if name in ["R2", "LR2", "RR2"]:
                    pointNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", f"{name}_Used")
                    pointNode.SetMarkupLabelFormat(name)
                    pointNode.AddControlPoint(pos)
        
    def autoSelectLandmarkBundle(self):
            """Auto-select the landmark bundle based on loaded landmarks"""
            if not self.landmarksNode:
                return
                
            # Check which landmarks are present
            hasInion = self.findPointByName(self.landmarksNode, "inion") >= 0
            hasBregma = self.findPointByName(self.landmarksNode, "bregma") >= 0
            
            # Select the appropriate bundle
            if hasInion and hasBregma:
                self.landmarkBundleCombo.setCurrentIndex(0)  # INB bundle
                self.log("Auto-selected INB landmark bundle based on loaded landmarks")
            else:
                self.landmarkBundleCombo.setCurrentIndex(1)  # MSP bundle
                self.log("Auto-selected MSP landmark bundle based on loaded landmarks")
        
    def onCreatePlaneClicked(self):
            """Handle create plane button click"""

            if self.planeNode is not None:
                self.log("A plane already exists. Skipping creation.")
                slicer.util.messageBox("A plane (INB or MSP) already exists in the scene. Using that one.")
                return # Stop the function here
    
            markupsNode = self.markupsSelector.currentNode()
            
            if not markupsNode:
                slicer.util.errorDisplay("Please select a landmarks node first")
                return
            
            bundle = self.landmarkBundleCombo.currentIndex
            
            try:
                # Get the landmarks based on the selected bundle
                if bundle == 0:
                    landmarkNames = ["nasion", "inion", "bregma"]
                    planeName = "INB"
                else:
                    landmarkNames = ["nasion", "acanthion", "rhinion"]
                    planeName = "MSP"
                    
                # Find the landmark points by name
                points = []
                for name in landmarkNames:
                    pointIndex = self.findPointByName(markupsNode, name)
                    
                    if pointIndex < 0:
                        slicer.util.errorDisplay(f"Could not find landmark '{name}' in the selected node")
                        return
                    
                    pos = [0, 0, 0]
                    markupsNode.GetNthControlPointPosition(pointIndex, pos)
                    points.append(np.array(pos))
                
                # Make sure we have exactly 3 points
                if len(points) != 3:
                    slicer.util.errorDisplay("Exactly 3 landmarks are required to create a plane")
                    return
                
                # Calculate the normal of the plane defined by the three points
                v1 = points[1] - points[0]  # Vector from point1 to point2
                v2 = points[2] - points[0]  # Vector from point1 to point3
                planeNormal = np.cross(v1, v2)
                planeNormal = planeNormal / np.linalg.norm(planeNormal)  # Normalize the normal vector
                
                # Create a new plane node
                planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', planeName)
                
                # Calculate the centroid (average of the three points)
                centroid = (points[0] + points[1] + points[2]) / 3.0

                # Set the origin of the new plane to the centroid
                planeNode.SetOrigin(centroid)
                                
                # Set the normal of the new plane
                planeNode.SetNormal(planeNormal)
                
                # Make plane visible and adjust appearance
                planeNode.GetDisplayNode().SetOpacity(0.7)
                planeNode.GetDisplayNode().SetColor(0.7, 0.3, 0.3)  # Reddish color for visibility
                planeNode.GetDisplayNode().SetVisibility(True) # This is the correct tool for the job!
                
                self.planeNode = planeNode
                self.log(f"Created {planeName} plane from landmarks")
                
                # NEW: Automatically create default tangent lines on the plane
                self.createDefaultTangents(planeNode)
                
                # Exit placement mode
                interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
                interactionNode.SetCurrentInteractionMode(interactionNode.ViewTransform)
                
            except Exception as e:
                slicer.util.errorDisplay(f"Error creating plane: {str(e)}")
        
    def findPointByName(self, markupsNode, name):
            """A better way to find points, ignoring case and extra spaces."""
            searchName = name.lower().strip() # Makes search "lr2"
            for i in range(markupsNode.GetNumberOfControlPoints()):
                label = markupsNode.GetNthControlPointLabel(i).lower().strip() # Makes label "lr2"
                if label == searchName:
                    self.log(f"Found exact match for '{name}' at index {i}")
                    return i
            self.log(f"Could not find a point named '{name}'")
            return -1

    def setPlaneConstraint(self, lineNode, planeNode):
            """Set plane constraint with better compatibility"""
            try:
                # For newer Slicer versions
                lineNode.SetPlaneConstraintEnabled(True)
                lineNode.SetPlaneConstraintPlane(planeNode)
                return True
            except:
                # For older Slicer versions
                try:
                    # Get plane parameters
                    normal = [0, 0, 0]
                    origin = [0, 0, 0]
                    planeNode.GetNormal(normal)
                    planeNode.GetOrigin(origin)
                    
                    # Project points to plane
                    for i in range(lineNode.GetNumberOfControlPoints()):
                        pos = lineNode.GetNthControlPointPosition(i)
                        vec = np.array(pos) - np.array(origin)
                        dist = np.dot(vec, normal)
                        newPos = np.array(pos) - dist * np.array(normal)
                        lineNode.SetNthControlPointPosition(i, newPos[0], newPos[1], newPos[2])
                    
                    # Add observer to keep future points on plane
                    def keep_on_plane(caller, event):
                        try:
                            for i in range(caller.GetNumberOfControlPoints()):
                                pos = caller.GetNthControlPointPosition(i)
                                vec = np.array(pos) - np.array(origin)
                                dist = np.dot(vec, normal)
                                if abs(dist) > 0.001:  # Only update if not already on plane
                                    newPos = np.array(pos) - dist * np.array(normal)
                                    caller.SetNthControlPointPosition(i, newPos[0], newPos[1], newPos[2])
                        except:
                            pass  # Ignore errors during updates
                    
                    # Add the observer
                    lineNode.AddObserver(lineNode.PointModifiedEvent, keep_on_plane)
                    return True
                except:
                    return False

    def resetInteractionMode(self):
                """Reset the interaction mode to prevent unwanted line creation"""
                interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
                interactionNode.SetCurrentInteractionMode(interactionNode.ViewTransform)
        
    def createDefaultTangents(self, planeNode):
        """Create default tangent lines on the plane that users can then adjust"""
        self.log("Creating default tangent lines on the plane")
        
        # Get plane parameters
        normal = [0, 0, 0]
        origin = [0, 0, 0]
        planeNode.GetNormal(normal)
        planeNode.GetOrigin(origin)
        
        # Create a coordinate system on the plane
        z_axis = np.array(normal)
        # Pick any vector not parallel to z_axis
        temp = np.array([1, 0, 0]) if abs(z_axis[0]) < 0.9 else np.array([0, 1, 0])
        x_axis = np.cross(temp, z_axis)
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = np.cross(z_axis, x_axis)
        y_axis = y_axis / np.linalg.norm(y_axis)
        
        # Check if shortcut mode is enabled
        shortcut_mode = hasattr(self, 't1t2ShortcutCheckbox') and self.t1t2ShortcutCheckbox.isChecked()
        
        # Create T1 (positioned in the center of the plane)
        t1_center = np.array(origin)
        t1_start = t1_center - 15 * x_axis
        t1_end = t1_center + 15 * x_axis
        self.createTangentLine("T1", t1_start, t1_end, [1.0, 1.0, 0.0])  # Yellow
        
        # Create T2 (offset from T1)
        t2_center = t1_center + 20 * y_axis
        t2_start = t2_center - 15 * x_axis
        t2_end = t2_center + 15 * x_axis
        self.createTangentLine("T2", t2_start, t2_end, [0.0, 1.0, 0.0])  # Green
        
        # Only create T3 if NOT in shortcut mode
        if not shortcut_mode:
            # Create T3 (offset from T2)
            t3_center = t2_center + 20 * y_axis
            t3_start = t3_center - 15 * x_axis
            t3_end = t3_center + 15 * x_axis
            self.createTangentLine("T3", t3_start, t3_end, [0.8, 0.6, 1.0])  # Lilac
        
        # Show guidance based on mode
        if shortcut_mode: 
            self.showGuidanceDialog(
                "Default tangent lines (T1 and T2) have been created on the plane.\n\n"
                "Please adjust them to the correct positions:\n"
                "• T1 (Yellow): Last third of the nasal bone\n"
                "• T2 (Green): Direction of anterior nasal spine\n\n"
                "Click on the lines to select them, then drag the control points to adjust.\n"
                "When ready, click 'Run T1-T2 Prediction & Compare to Pronasale'."
            )
        else:
            self.showGuidanceDialog(
                "Default tangent lines have been created on the plane.\n\n"
                "Please adjust them to the correct positions:\n"
                "• T1 (Yellow): Last third of the nasal bone\n"
                "• T2 (Green): Direction of anterior nasal spine\n"
                "• T3 (Lilac): Last 1-2 mm of the nasal bone\n\n"
                "Click on the lines to select them, then drag the control points to adjust."
            )
            
    def onRegenerateTangentsClicked(self):
            """Regenerate T1, T2, T3 using default logic on the current plane."""
            if not self.planeNode:
                slicer.util.messageBox("Please create a plane first in Step 1.")
                return

            # Remove existing T1, T2, T3 tangent nodes if they exist
            for tangent in ["T1", "T2", "T3"]:
                if tangent in self.tangentNodes:
                    slicer.mrmlScene.RemoveNode(self.tangentNodes[tangent])
                    del self.tangentNodes[tangent]
                    if tangent in self.tangents:
                        del self.tangents[tangent]
                    self.log(f"Removed {tangent} tangent for regeneration.")

            # Recreate default tangents
            self.createDefaultTangents(self.planeNode)
            slicer.util.showStatusMessage("Default tangents regenerated!", 3000)
    

    def createTangentLine(self, tangentName, startPoint, endPoint, color):
        """Create a tangent line with specified start and end points"""
        # 1. Create the line node in the scene
        lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", tangentName)
        
        # 2. Add the start and end points
        lineNode.AddControlPoint(startPoint)
        lineNode.AddControlPoint(endPoint)
        
        # 3. Set the color
        lineNode.GetDisplayNode().SetSelectedColor(color)
        lineNode.GetDisplayNode().SetColor(color)
        
        # 4. Store the node and its initial position data in our dictionaries
        self.tangentNodes[tangentName] = lineNode
        self.tangents[tangentName] = {
            'start': startPoint.tolist() if isinstance(startPoint, np.ndarray) else startPoint,
            'end': endPoint.tolist() if isinstance(endPoint, np.ndarray) else endPoint,
            'vector': (np.array(endPoint) - np.array(startPoint)).tolist()
        }
        
        # 5. Define a helper function that will run whenever the user moves the line
        def update_tangent_data(caller, event):
            """This function keeps our dictionary in sync with user edits in the GUI."""
            if caller.GetNumberOfControlPoints() >= 2:
                start = [0, 0, 0]
                end = [0, 0, 0]
                # Get the line's NEW position from the GUI
                caller.GetNthControlPointPositionWorld(0, start)
                caller.GetNthControlPointPositionWorld(1, end)
                # Update our dictionary with the new position
                self.tangents[tangentName] = {
                    'start': start,
                    'end': end,
                    'vector': (np.array(end) - np.array(start)).tolist()
                }
                self.log(f"User manually updated {tangentName} position.")

        # 6. Tell the line node to run our helper function every time it's moved
        lineNode.AddObserver(lineNode.PointModifiedEvent, update_tangent_data)

        # 7. Constrain to plane if needed
        if tangentName in ["T1", "T2", "T3"] and self.planeNode:
            self.setPlaneConstraint(lineNode, self.planeNode)
        
        self.log(f"Created {tangentName} tangent line")
        return lineNode

    
    def selectTangentForAdjustment(self, tangentName):
            """Select a tangent for the user to adjust"""
            if tangentName not in self.tangentNodes:
                self.showGuidanceDialog(f"Tangent {tangentName} doesn't exist yet. Create the MSP/INB plane first.")
                return
                
            # Select the tangent in the scene
            selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
            selectionNode.SetReferenceActivePlaceNodeID(self.tangentNodes[tangentName].GetID())
            
            # Exit placement mode (to allow adjustment)
            interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
            interactionNode.SetCurrentInteractionMode(interactionNode.ViewTransform)
            
            # Show guidance for this tangent
            if tangentName == "T1":
                instruction = "Adjust T1 (Yellow): Should follow the last third of the nasal bone"
            elif tangentName == "T2":
                instruction = "Adjust T2 (Green): Should follow the direction of the anterior nasal spine"
            elif tangentName == "T3":
                instruction = "Adjust T3 (Lilac): Should follow the last 1-2 mm of the nasal bone"
            else:
                instruction = f"Adjust {tangentName} tangent to the correct position"
            
            self.showGuidanceDialog(instruction) 

    def constrainPointToPlane(self, lineNode, planeNormal, planeOrigin):
            """Constrain a point to a plane when moved"""
            for i in range(lineNode.GetNumberOfControlPoints()):
                pos = lineNode.GetNthControlPointPosition(i)
                
                # Project point onto plane
                vec = np.array(pos) - np.array(planeOrigin)
                dist = np.dot(vec, planeNormal)
                projectedPos = np.array(pos) - dist * np.array(planeNormal)
                
                # Update point position without triggering another event
                lineNode.RemoveObservers(lineNode.PointModifiedEvent)
                lineNode.SetNthControlPointPosition(i, projectedPos[0], projectedPos[1], projectedPos[2])
                lineNode.AddObserver(lineNode.PointModifiedEvent, 
                                lambda caller, event: self.constrainPointToPlane(
                                    caller, planeNormal, planeOrigin))

    def onPlaceTangentClicked(self, tangentName):
        """Handle placing a tangent with instructions inside the GUI."""
        if tangentName in self.tangentNodes:
            self.log(f"Tangent {tangentName} already exists.")
            slicer.util.messageBox(f"The tangent '{tangentName}' already exists. If you want to re-place it, please delete it from the Data module first.")
            return

        try:
            # Create a line node
            lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", tangentName)

            # --- This part is mostly the same ---
            if tangentName == "T1":
                color = [1.0, 1.0, 0.0] # Yellow
                instruction = "Place T1 (Yellow): Draw a line following the last third of the nasal bone."
            elif tangentName == "T2":
                color = [0.0, 1.0, 0.0] # Green
                instruction = "Place T2 (Green): Draw a line following the direction of the anterior nasal spine."
            elif tangentName == "T3":
                color = [0.8, 0.6, 1.0] # Lilac
                instruction = "Place T3 (Lilac): Draw a line following the last 1-2 mm of the nasal bone."
            elif tangentName == "T4R":
                color = [0.6, 0.4, 0.8] # Purple
                instruction = "Place T4R (Purple): Draw a line following the direction of the nasal floor on the right side."
            elif tangentName == "T4L":
                color = [0.6, 0.4, 0.8] # Purple
                instruction = "Place T4L (Purple): Draw a line following the direction of the nasal floor on the left side."
            else:
                color = [1.0, 1.0, 1.0]
                instruction = f"Place {tangentName} tangent."

            lineNode.GetDisplayNode().SetSelectedColor(color)
            lineNode.GetDisplayNode().SetColor(color)

            # Instead of a pop-up, we show the message on our "message board"
            self.tangentInstructionLabel.setText(instruction)
            self.tangentInstructionLabel.setVisible(True)
        
            # Start placement mode
            selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
            selectionNode.SetReferenceActivePlaceNodeID(lineNode.GetID())
            selectionNode.SetActivePlaceNodeClassName("vtkMRMLMarkupsLineNode")

            interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
            interactionNode.SetCurrentInteractionMode(interactionNode.Place)

            # Store the node and set up observers
            self.tangentNodes[tangentName] = lineNode
            lineNode.AddObserver(lineNode.PointPositionDefinedEvent,
                                lambda caller, event: self.onTangentComplete(tangentName, caller))
            self.log(f"Starting placement of {tangentName} tangent")

        except Exception as e:
            slicer.util.errorDisplay(f"Error placing tangent: {str(e)}")    
        

    def onInteractionModeChanged(self, tangentName):
            """Monitor when user exits placement mode and offer to return"""
            interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
            if interactionNode.GetCurrentInteractionMode() != interactionNode.Place:
                # If placement was cancelled, ask if user wants to continue
                if tangentName in self.tangentNodes and self.tangentNodes[tangentName].GetNumberOfControlPoints() < 2:
                    self.showGuidanceDialog(
                        f"Placement of {tangentName} was interrupted.\nWould you like to continue?", 
                        lambda: self.resumeTangentPlacement(tangentName)
                    )
        
    def resumeTangentPlacement(self, tangentName):
            """Resume placement of a tangent"""
            if tangentName in self.tangentNodes:
                lineNode = self.tangentNodes[tangentName]
                
                # Make sure we have the right node selected
                selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
                selectionNode.SetReferenceActivePlaceNodeID(lineNode.GetID())
                selectionNode.SetActivePlaceNodeClassName("vtkMRMLMarkupsLineNode")
                
                # Return to placement mode
                interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
                interactionNode.SetCurrentInteractionMode(interactionNode.Place)
                
                # Show guidance again
                self.showGuidanceDialog(f"Continuing placement of {tangentName}...")
        
    def onTangentComplete(self, tangentName, lineNode):
            """Handle when a tangent placement is complete"""
            if lineNode.GetNumberOfControlPoints() >= 2:
                # (The code to store the tangent info stays the same)
                startPoint = lineNode.GetNthControlPointPosition(0)
                endPoint = lineNode.GetNthControlPointPosition(1)
                self.tangents[tangentName] = {
                    'start': startPoint,
                    'end': endPoint,
                    'vector': (np.array(endPoint) - np.array(startPoint)).tolist()
                }
                self.log(f"Placed {tangentName} tangent")
                self.resetInteractionMode()

                # --- NEW, SMARTER LOGIC ---
                nextTangent = None
                message = ""

                # Check if T4L has already been placed
                t4l_exists = "T4L" in self.tangents or "T4L" in self.tangentNodes

                if tangentName == "T1":
                    nextTangent = "T2"
                    message = "T1 placed! Ready to place T2?"
                elif tangentName == "T2":
                    nextTangent = "T3"
                    message = "T2 placed! Ready to place T3?"
                elif tangentName == "T3":
                    nextTangent = "T4R"
                    message = "T3 placed! Ready to place T4R?"
                elif tangentName == "T4R" and not t4l_exists:
                    # We just placed T4R and T4L isn't there, so ask to place it.
                    nextTangent = "T4L"
                    message = "T4R placed! Would you like to place T4L for bilateral analysis?"
                else:
                    # This runs after placing T4L, or after T4R if T4L already exists.
                    # No popup, just a quiet message at the bottom of the screen.
                    slicer.util.showStatusMessage(f"{tangentName} placed successfully!", 3000)
                    message = "" # This ensures no popup will appear

                if message and nextTangent:
                    self.showNextTangentDialog(message, nextTangent)
                        
                      
    def showNextTangentDialog(self, message, nextTangent=None):
            """Show a dialog with Yes/No buttons for continuing to next tangent"""
            if not nextTangent:
                # If no next tangent, just show a simple message
                dialog = qt.QMessageBox(self.mainWidget)
                dialog.setText(message)
                dialog.setWindowTitle("Tangent Placement Complete")
                dialog.addButton(qt.QMessageBox.Ok)
                dialog.exec_()
                return
                
            # Create custom dialog with Yes/No buttons
            dialog = qt.QMessageBox(self.mainWidget)
            dialog.setText(message)
            dialog.setWindowTitle("Continue to Next Tangent?")
            yesButton = dialog.addButton("Yes, place next tangent", qt.QMessageBox.YesRole)
            dialog.addButton("No, I'll place it later", qt.QMessageBox.NoRole)
            
            dialog.exec_()
            
            # If user clicked Yes, place the next tangent
            if dialog.clickedButton() == yesButton and nextTangent:
                # Small delay to make sure everything is reset
                qt.QTimer.singleShot(100, lambda: self.onPlaceTangentClicked(nextTangent))

   
    def extendTangent(self, tangentName, extensionLength):
        """
        Extend a tangent line *intelligently* by 50mm in the anterior direction,
        regardless of how the user has drawn the line.
        """
        try:
            tangent_data = self.tangents[tangentName]
            
            p1 = np.array(tangent_data['start'])
            p2 = np.array(tangent_data['end'])
            
            # --- THE CORRECTED LOGIC ---
            # In 3D Slicer's standard RAS coordinate system:
            # - The Y-axis runs from Posterior (-) to Anterior (+).
            # - Therefore, the point with the LARGER Y-value is the more "anterior" point.
            
            # 1. Let's identify which point is anterior and which is posterior.
            #    THIS IS THE ONE-CHARACTER FIX: We change '<' to '>'
            if p1[1] > p2[1]:
                anterior_point = p1
                posterior_point = p2
            else:
                anterior_point = p2
                posterior_point = p1
                
            # 2. Calculate the direction vector *always* pointing from posterior to anterior.
            direction = anterior_point - posterior_point
            # Normalize the vector to have a length of 1, so we can scale it accurately.
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            
            # 3. Calculate the new anterior point by extending it forward.
            new_anterior_point = anterior_point + direction * extensionLength
            
            # 4. Update our data with the new, correct points.
            # The posterior point stays the same, and the anterior point is the new extended one.
            self.tangents[tangentName]['start'] = posterior_point.tolist()
            self.tangents[tangentName]['end'] = new_anterior_point.tolist()
            self.tangents[tangentName]['vector'] = (new_anterior_point - posterior_point).tolist()
            
            self.log(f"Correctly extended {tangentName} anteriorly by {extensionLength}mm.")

        except Exception as e:
            self.log(f"Error extending {tangentName}: {e}", 2)
 

    def onExtendTangentsClicked(self):
        """Extends tangents by a fixed amount and backs up their original state."""
        self.log("'Elongate Tangents' button clicked.")
        
        extensionLength = 50

        try:
            tangents_to_extend = ["T1", "T2", "T3"]
            if "T4" in self.tangents:
                tangents_to_extend.append("T4")
            elif "T4R" in self.tangents:
                tangents_to_extend.append("T4R")

            for name in tangents_to_extend:
                if name not in self.tangent_backups:
                    self.tangent_backups[name] = self.tangents[name].copy()
                    self.log(f"Backed up original position for {name}.")

            # Extend each tangent
            for name in tangents_to_extend:
                if name in self.tangents:
                    self.extendTangent(name, extensionLength)
                    self.updateTangentVisualization(name)
                else:
                    self.log(f"Skipping extension for {name} as it does not exist.", 2)

            self.log(f"Extended tangents by {extensionLength}mm.")
            slicer.util.showStatusMessage(f"Tangents extended by {extensionLength}mm!", 3000)

        except Exception as e:
            self.log(f"Error in onExtendTangentsClicked: {e}", 2)
            slicer.util.errorDisplay(f"Error extending tangents: {e}")

    

    def onResetExtensionsClicked(self):
        """Restores all tangents to their state before elongation."""
        self.log("'Reset Extensions' button clicked.")

        if not self.tangent_backups:
            slicer.util.showStatusMessage("Tangents have not been extended yet.", 3000)
            return

        try:
            # Go through our backup dictionary
            for name, backup_data in self.tangent_backups.items():
                if name in self.tangents and name in self.tangentNodes:
                    # Restore the data in our main dictionary from the backup
                    self.tangents[name] = backup_data.copy()
                    # Update the line in the 3D scene to match the backup
                    self.updateTangentVisualization(name)
            
            self.log("Successfully reset all tangent extensions.")
            slicer.util.showStatusMessage("All tangent extensions have been reset.", 4000)
            
            # Optional: Clear the backup so you can't reset again until you extend again
            self.tangent_backups = {}

        except Exception as e:
            self.log(f"Error resetting tangent extensions: {e}", 2)
            slicer.util.errorDisplay(f"Could not reset extensions: {e}")

   
    def onElongateNasalFloorTangentsClicked(self):
        """Extends only the T4R and T4L tangents anteriorly."""
        self.log("'Elongate Nasal Floor Tangents' button clicked.")
        
        extensionLength = 50
        tangents_to_extend = []

        # Check if T4R exists and needs to be extended
        if "T4R" in self.tangents:
            tangents_to_extend.append("T4R")
        
        # Check if T4L exists and needs to be extended
        if "T4L" in self.tangents:
            tangents_to_extend.append("T4L")

        if not tangents_to_extend:
            slicer.util.messageBox("Please create the T4R and/or T4L tangents in Step 2 before elongating them.")
            return

        try:
            # Backup the positions before extending, if not already backed up
            for name in tangents_to_extend:
                if name not in self.tangent_backups:
                    self.tangent_backups[name] = self.tangents[name].copy()
                    self.log(f"Backed up original position for {name}.")

            # Extend each tangent and update its look in the 3D scene
            for name in tangents_to_extend:
                self.extendTangent(name, extensionLength)
                self.updateTangentVisualization(name)

            self.log(f"Extended nasal floor tangents by {extensionLength}mm.")
            slicer.util.showStatusMessage(f"Nasal floor tangents extended by {extensionLength}mm!", 3000)

        except Exception as e:
            self.log(f"Error in onElongateNasalFloorTangentsClicked: {e}", 2)
            slicer.util.errorDisplay(f"Error elongating nasal floor tangents: {e}")

    def onR2MethodChanged(self, button):
            """Handle R2 method selection"""
            isManual = button == self.manualR2RadioButton
            self.placeR2Button.setVisible(isManual)
            self.automaticR2Frame.setVisible(not isManual)
            self.log(f"Switched to {'manual' if isManual else 'automatic'} R2 placement")
        


    def onPlacePointClicked(self, pointName):
        """Handles placing a point *directly into the main landmarks file*."""
        self.log(f"Starting placement for '{pointName}' point.")

        # --- Safety Check: Make sure the main landmarks file exists ---
        if not self.landmarksNode:
            slicer.util.errorDisplay("Please load the 'Gerasimow_landmarks' file first in Step 1.")
            return

    
        
        # We are putting the main landmarks node into "placement mode"
        slicer.app.applicationLogic().GetInteractionNode().SetCurrentInteractionMode(slicer.vtkMRMLInteractionNode.Place)
        slicer.app.applicationLogic().GetSelectionNode().SetActivePlaceNodeID(self.landmarksNode.GetID())

        # Set up an observer to run a function ONCE the user has clicked to place the point.
        # We will tell that function to name the new point correctly.
        self.pointPlacementObserver = self.landmarksNode.AddObserver(slicer.vtkMRMLMarkupsNode.PointAddedEvent, 
                                                                    lambda caller, event: self.onPointPlaced(pointName, caller))
        
        # Show guidance to the user
        pointDescriptions = {
            "R2": "Place R2: Where the T4 line crosses the soft tissue on the midsagittal plane.",
            "LR2": "Place LR2: Where the T4L line crosses the soft tissue on the left.",
            "RR2": "Place RR2: Where the T4R line crosses the soft tissue on the right."
        }
        if pointName in pointDescriptions:
            self.showGuidanceDialog(pointDescriptions[pointName])



    def onPointPlaced(self, pointName, landmarksNode):
        """This function runs right after the user places a new point."""
        
        # --- The new point is the LAST one in the list ---
        numberOfPoints = landmarksNode.GetNumberOfControlPoints()
        if numberOfPoints == 0:
            return # Should not happen, but a good safety check
        
        # The point we just added is the last one.
        newPointIndex = numberOfPoints - 1
        
        # --- Set the name of the point we just added ---
        landmarksNode.SetNthControlPointLabel(newPointIndex, pointName)
        
        # Get its position and store it in our internal dictionary
        position = [0, 0, 0]
        landmarksNode.GetNthControlPointPositionWorld(newPointIndex, position)
        self.points[pointName] = position
        
        self.log(f"Placed '{pointName}' point at index {newPointIndex} in the main landmarks file.")
        
    
        # We must remove the observer so it doesn't run again accidentally.
        landmarksNode.RemoveObserver(self.pointPlacementObserver)
        self.pointPlacementObserver = None # Clear it
        
        slicer.app.applicationLogic().GetInteractionNode().SetCurrentInteractionMode(slicer.vtkMRMLInteractionNode.ViewTransform)
        
        slicer.util.showStatusMessage(f"'{pointName}' placed successfully!", 3000)
        

    def onCalculateR2Clicked(self):
        """Calculates R2 and moves the existing point in the main landmarks file."""
        self. log("'Calculate R2' button clicked.")

        # --- Safety Checks ---
        if "LR2" not in self.points or "RR2" not in self.points:
            slicer.util.errorDisplay("Please place both LR2 and RR2 points first.")
            return

        landmarksNode = self.landmarksNode
        if not landmarksNode:
            slicer.util.errorDisplay("Could not find the 'Gerasimow_landmarks' node. Please load it first.")
            return

        try:
            lr2 = np.array(self.points["LR2"])
            rr2 = np. array(self.points["RR2"])
            r2_position = None
            methodName = ""

            # Calculation Logic 
            if self.intersectionR2RadioButton.isChecked() and self.planeNode:
                planeNormal, planeOrigin = np.zeros(3), np.zeros(3)
                self.planeNode.GetNormalWorld(planeNormal)
                self.planeNode. GetOriginWorld(planeOrigin)
                r2_position = self.calculateIntersection(lr2, rr2, planeOrigin, planeNormal)
                methodName = "intersection with plane"
            else: 
                r2_position = (lr2 + rr2) / 2.0
                methodName = "geometric mean"
            
            # Find the R2 point in the main landmarks file
            r2_index = self.findPointByName(landmarksNode, "R2")

            if r2_index != -1:
                # If we found it, move it to the new position
                landmarksNode.SetNthControlPointPositionWorld(r2_index, r2_position)
                self.log(f"Moved existing 'R2' point using {methodName}.")
                slicer.util.showStatusMessage("Moved existing R2 point successfully!", 4000)
            else:
                # If it doesn't exist, add it to the main landmarks file
                landmarksNode.AddControlPoint(r2_position, "R2")
                self.log(f"Created new 'R2' point in landmarks file using {methodName}.")
                slicer.util.showStatusMessage("Created new R2 point successfully!", 4000)

            # Update our internal dictionary
            self.points["R2"] = r2_position. tolist()

        except Exception as e:
            slicer.util.errorDisplay(f"Error calculating R2: {e}")
            import traceback
            traceback.print_exc()



    def calculateIntersection(self, p1, p2, planePoint, planeNormal):
            """Calculate the intersection of a line with a plane"""
            # Line direction
            lineDirection = p2 - p1
            lineDirection = lineDirection / np.linalg.norm(lineDirection)
            
            # Calculate the intersection parameter
            d = np.dot(np.array(planeNormal), np.array(planePoint) - p1) / np.dot(np.array(planeNormal), lineDirection)
            
            # Calculate the intersection point
            intersection = p1 + d * lineDirection
            
            return intersection
        

    def onFindIntersectionsClicked(self):
            """Calculates intersections using your proven logic."""
            self.log("'Find Intersections' button clicked.")

            # A helper function from your snippet
            def find_intersection_point(p1, v1, p2, v2):
                # Solves for the intersection of two lines in 3D space
                A = np.array([v1, -v2]).T
                b = np.array(p2) - np.array(p1)
                try:
                    t = np.linalg.lstsq(A, b, rcond=None)[0]
                    intersection = p1 + t[0] * v1
                    return intersection
                except np.linalg.LinAlgError:
                    self.log("Could not find intersection; lines may be parallel.", 2)
                    return None

            try:
                # Check if we have the required tangents
                required = ["T1", "T2", "T3", "T4"]
                for name in required:
                    if name not in self.tangents:
                        slicer.util.messageBox(f"Missing required tangent: {name}. Please create it first.")
                        return

                # Get tangent vectors from our stored data
                t1_start, t1_end = self.tangents["T1"]['start'], self.tangents["T1"]['end']
                t2_start, t2_end = self.tangents["T2"]['start'], self.tangents["T2"]['end']
                t3_start, t3_end = self.tangents["T3"]['start'], self.tangents["T3"]['end']
                t4_start, t4_end = self.tangents["T4"]['start'], self.tangents["T4"]['end']

                t1_dir = np.array(t1_end) - np.array(t1_start)
                t2_dir = np.array(t2_end) - np.array(t2_start)
                t3_dir = np.array(t3_end) - np.array(t3_start)
                t4_dir = np.array(t4_end) - np.array(t4_start)

                # Find intersections
                self.intersections = {}
                self.intersections["T1-T2"] = find_intersection_point(t1_start, t1_dir, t2_start, t2_dir)
                self.intersections["T1-T4"] = find_intersection_point(t1_start, t1_dir, t4_start, t4_dir)
                self.intersections["T3-T2"] = find_intersection_point(t3_start, t3_dir, t2_start, t2_dir)
                self.intersections["T3-T4"] = find_intersection_point(t3_start, t3_dir, t4_start, t4_dir)

                # Create a new markups node for the predictions
                prediction_points = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'prediction points')
                for name, point in self.intersections.items():
                    if point is not None:
                        prediction_points.AddControlPoint(point, f"pred {name}")
                
                self.log(f"Created 'prediction points' node with {len(self.intersections)} points.")
                slicer.util.showStatusMessage("Intersection points created successfully!", 4000)
                
                # Store intersections in results
                for name, point in self.intersections.items():
                    if point is not None:
                        self.storeCoordinate(f"Intersection {name}", point.tolist())    

            except Exception as e:
                slicer.util.errorDisplay(f"An error occurred while finding intersections: {e}")
                
    def onCalculateErrorsClicked(self):
        """
        Creates lines between the true landmarks (pronasale, R2) and the
        predicted intersection points, using the logic you provided.
        """
        self.log("'Compare Points' button clicked.")

        # --- Safety Checks: Make sure everything we need exists ---
        try: 
            landmarks_node = slicer.util.getNode("Gerasimow_landmarks")
            prediction_node = slicer.util.getNode("prediction points")

            if not landmarks_node or not prediction_node:
                slicer.util.messageBox("Could not find 'Gerasimow_landmarks' or 'prediction points' nodes. Please run previous steps first.")
                return

            # A more robust way to find points: by their name!
            prn_index = self.findPointByName(landmarks_node, "pronasale")
            r2_index = self.findPointByName(landmarks_node, "R2")

            if prn_index == -1 or r2_index == -1:
                slicer.util.messageBox("Could not find 'pronasale' or 'R2' in the 'Gerasimow_landmarks' file. Please ensure they are named correctly.")
                return
            
            if prediction_node.GetNumberOfControlPoints() < 4:
                slicer.util.messageBox("Not enough points found in 'prediction points'. Please run 'Find Intersections' again.")
                return

        except Exception as e:
            slicer.util.errorDisplay(f"Setup failed: {e}")
            return

        # --- Main Logic: Create the lines ---
        try:
            # This is a helper function based on your snippet
            def create_line(point1_idx, point2_idx, line_name, color, node1, node2):
                p1, p2 = [0,0,0], [0,0,0]
                node1.GetNthControlPointPositionWorld(point1_idx, p1)
                node2.GetNthControlPointPositionWorld(point2_idx, p2)
                
                line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', line_name)
                line_node.AddControlPoint(p1)
                line_node.AddControlPoint(p2)
                
                # Set the color
                line_node.GetDisplayNode().SetSelectedColor(color)
                line_node.GetDisplayNode().SetColor(color)
                line_node.SetLocked(True)

            # Define the colors you chose
            prn_color = (128/255, 0/255, 32/255)  # Maroon
            r2_color = (255/255, 69/255, 0/255)   # Orange-Red

            # Create lines from 'pronasale' to each of the 4 prediction points
            create_line(prn_index, 0, 'prn_T1-T2_error', prn_color, landmarks_node, prediction_node)
            create_line(prn_index, 1, 'prn_T1-T4_error', prn_color, landmarks_node, prediction_node)
            create_line(prn_index, 2, 'prn_T3-T2_error', prn_color, landmarks_node, prediction_node)
            create_line(prn_index, 3, 'prn_T3-T4_error', prn_color, landmarks_node, prediction_node)

            # Create lines from 'R2' to each of the 4 prediction points
            create_line(r2_index, 0, 'R2_T1-T2_error', r2_color, landmarks_node, prediction_node)
            create_line(r2_index, 1, 'R2_T1-T4_error', r2_color, landmarks_node, prediction_node)
            create_line(r2_index, 2, 'R2_T3-T2_error', r2_color, landmarks_node, prediction_node)
            create_line(r2_index, 3, 'R2_T3-T4_error', r2_color, landmarks_node, prediction_node)

            slicer.util. showStatusMessage("Error comparison lines created successfully!", 4000)
            self.log("Successfully created all error comparison lines.")

            # Store all prediction errors in the results tables
            prn_pos = [0,0,0]
            r2_pos = [0,0,0]
            landmarks_node.GetNthControlPointPositionWorld(prn_index, prn_pos)
            landmarks_node.GetNthControlPointPositionWorld(r2_index, r2_pos)

            # Store pronasale errors
            for i, name in enumerate(["T1-T2", "T1-T4", "T3-T2", "T3-T4"]):
                pred_pos = [0,0,0]
                prediction_node.GetNthControlPointPositionWorld(i, pred_pos)
                error = np.linalg. norm(np.array(pred_pos) - np.array(prn_pos))
                self.storeMeasurement(f"prn {name} error", error, "mm", is_error=True)
                self.storeCoordinate(f"Pronasale ({name})", pred_pos, prn_pos)

            # Store R2 errors  
            for i, name in enumerate(["T1-T2", "T1-T4", "T3-T2", "T3-T4"]):
                pred_pos = [0,0,0]
                prediction_node. GetNthControlPointPositionWorld(i, pred_pos)
                error = np.linalg.norm(np.array(pred_pos) - np.array(r2_pos))
                self.storeMeasurement(f"R2 {name} error", error, "mm", is_error=True)
                self.storeCoordinate(f"R2 ({name})", pred_pos, r2_pos)
        
        except Exception as e: 
            slicer.util.errorDisplay(f"An error occurred while creating the error lines: {e}")
            import traceback
            traceback.print_exc()

    
        
    def calculateT4FromT4RandT4L(self, t4r, t4l, method):
            """Calculate T4 from T4R and T4L using the specified method"""
            if method == 'mutual':
                # Find midpoint between projected T4R and T4L
                t4rStart = np.array(t4r['projectedStart'])
                t4rEnd = np.array(t4r['projectedEnd'])
                t4lStart = np.array(t4l['projectedStart'])
                t4lEnd = np.array(t4l['projectedEnd'])
                
                # Use the midpoint of the start and end points
                start = (t4rStart + t4lStart) / 2
                end = (t4rEnd + t4lEnd) / 2
                
                return {
                    'projectedStart': start.tolist(),
                    'projectedEnd': end.tolist()
                }
            else:  # geometric mean
                # Calculate the geometric mean of the vectors
                t4rStart = np.array(t4r['projectedStart'])
                t4rEnd = np.array(t4r['projectedEnd'])
                t4lStart = np.array(t4l['projectedStart'])
                t4lEnd = np.array(t4l['projectedEnd'])
                
                # Calculate vectors
                t4rVector = t4rEnd - t4rStart
                t4lVector = t4lEnd - t4lStart
                
                # Normalize vectors
                t4rVector = t4rVector / np.linalg.norm(t4rVector)
                t4lVector = t4lVector / np.linalg.norm(t4lVector)
                
                # Calculate the mean vector (simplified approach)
                meanVector = (t4rVector + t4lVector) / 2
                meanVector = meanVector / np.linalg.norm(meanVector)
                
                # Use the midpoint of the start points
                start = (t4rStart + t4lStart) / 2
                
                # Calculate the end point using the mean vector
                length = (np.linalg.norm(t4rEnd - t4rStart) + np.linalg.norm(t4lEnd - t4lStart)) / 2
                end = start + meanVector * length
                
                return {
                    'projectedStart': start.tolist(),
                    'projectedEnd': end.tolist()
                }
        
    def calculateIntersections(self, tangents):
            """Calculate intersections between tangent lines"""
            intersections = {}
            
            # Define the pairs to calculate
            pairs = [
                ('T1', 'T2'),
                ('T1', 'T4'),
                ('T3', 'T2'),
                ('T3', 'T4')
            ]
            
            for t1_name, t2_name in pairs:
                if t1_name in tangents and t2_name in tangents:
                    try:
                        # Get the projected tangent lines
                        t1 = tangents[t1_name]
                        t2 = tangents[t2_name]
                        
                        # Calculate the closest points between the two lines in 2D (on the plane)
                        p1, p2 = self.closestPointsBetweenLines(
                            np.array(t1['projectedStart']), 
                            np.array(t1['projectedEnd']), 
                            np.array(t2['projectedStart']), 
                            np.array(t2['projectedEnd'])
                        )
                        
                        # Use the midpoint as the intersection
                        intersection = (p1 + p2) / 2
                        
                        # Store the intersection
                        intersections[f"{t1_name}-{t2_name}"] = intersection.tolist()
                        
                    except Exception as e:
                        self.log(f"Error calculating intersection {t1_name}-{t2_name}: {str(e)}")
            
            return intersections
        
    def closestPointsBetweenLines(self, p1, p2, p3, p4):
            """Find the closest points between two lines"""
            # Direction vectors
            d1 = p2 - p1
            d2 = p4 - p3
            
            # Normalize
            n1 = d1 / np.linalg.norm(d1)
            n2 = d2 / np.linalg.norm(d2)
            
            # Cross product of direction vectors
            cross = np.cross(n1, n2)
            
            # If lines are parallel, just use the start points
            if np.linalg.norm(cross) < 1e-10:
                return p1, p3
            
            # Calculate the closest points
            a = p3 - p1
            
            n1n1 = np.dot(n1, n1)
            n2n2 = np.dot(n2, n2)
            n1n2 = np.dot(n1, n2)
            n1a = np.dot(n1, a)
            n2a = np.dot(n2, a)
            
            # Solve for the parameters t1 and t2
            det = n1n1 * n2n2 - n1n2 * n1n2
            
            # If determinant is too small, lines are nearly parallel
            if abs(det) < 1e-10:
                # Project the start point of line 2 onto line 1
                t1 = np.dot(p3 - p1, n1)
                c1 = p1 + t1 * n1
                
                # Project the start point of line 1 onto line 2
                t2 = np.dot(p1 - p3, n2)
                c2 = p3 + t2 * n2
                
                # Use midpoint of these projections
                return c1, c2
            
            t1 = (n1n2 * n2a - n2n2 * n1a) / det
            t2 = (n1n1 * n2a - n1n2 * n1a) / det
            
            # Calculate the closest points
            c1 = p1 + t1 * n1
            c2 = p3 + t2 * n2
            
            return c1, c2
        
    def calculatePronasale(self, intersections):
            """Calculate the pronasale (R1) point from the intersections"""
            # According to Gerasimow's method, we use a combination of intersections
            points = []
            weights = []
            
            # Add each intersection with its weight
            if 'T1-T2' in intersections:
                points.append(np.array(intersections['T1-T2']))
                weights.append(0.3)
                
            if 'T1-T4' in intersections:
                points.append(np.array(intersections['T1-T4']))
                weights.append(0.3)
                
            if 'T3-T2' in intersections:
                points.append(np.array(intersections['T3-T2']))
                weights.append(0.2)
                
            if 'T3-T4' in intersections:
                points.append(np.array(intersections['T3-T4']))
                weights.append(0.2)
            
            # If we have at least one intersection
            if points:
                # Normalize weights
                total_weight = sum(weights)
                weights = [w / total_weight for w in weights]
                
                # Calculate weighted average
                pronasale = np.zeros(3)
                for point, weight in zip(points, weights):
                    pronasale += weight * point
                    
                return pronasale.tolist()
            
            return [0, 0, 0]
        
    def displayResults(self, intersections, pronasale):
            """Display the results in the results text area"""
            resultText = "<h3>Intersection Results</h3>"
            resultText += "<table border='1' cellpadding='5'>"
            resultText += "<tr><th>Intersection</th><th>Coordinates (x,y,z)</th></tr>"
            
            for name, coords in intersections.items():
                resultText += f"<tr><td>{name}</td><td>{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}</td></tr>"
            
            resultText += "</table>"
            
            resultText += "<h3>Calculated Points</h3>"
            resultText += "<ul>"
            
            if "R2" in self.points:
                r2 = self.points["R2"]
                method = "Manually placed" if self.manualR2RadioButton.isChecked() else "Calculated"
                resultText += f"<li>R2: [{r2[0]:.2f}, {r2[1]:.2f}, {r2[2]:.2f}] ({method})</li>"
            
            resultText += f"<li>Pronasale (R1): [{pronasale[0]:.2f}, {pronasale[1]:.2f}, {pronasale[2]:.2f}]</li>"
            resultText += "</ul>"
            

            self.log("Processing complete - results calculated")

# ADD THESE LINES AT THE VERY END OF THE FILE (after the last method)
print("About to create Gerasimow Nose Predictor GUI...")
gerasimowPredictor = GerasimowNosePredictor()
print("GUI created successfully!")
print(f"Main widget exists: {gerasimowPredictor.mainWidget is not None}")
print(f"Main widget is visible: {gerasimowPredictor.mainWidget.isVisible()}")


```
