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
        
        # Tangent definitions
        tangentsInfoLabel = qt.QLabel(
            "<b>Tangent Definitions:</b><br>"
            "• T1 (Yellow): Follows the last third of the nasal bone<br>"
            "• T2 (Green): Follows the direction of the anterior nasal spine<br>"
            "• T3 (Lilac): Follows the last 1-2 mm of the nasal bone<br>"
            "• T4 (Purple): Follows the direction of the nasal floor"
        )
        tangentsInfoLabel.setWordWrap(True)
        step2Layout.addWidget(tangentsInfoLabel)
        
        # VERTICAL TANGENT BUTTONS - each on its own line
        tangentControlFrame = qt.QFrame()
        tangentLayout = qt.QVBoxLayout(tangentControlFrame)
        tangentLayout.setSpacing(10)  # More space between buttons
        
           
        # T4R Button - Purple
        self.t4rButton = qt.QPushButton("Place T4R (Purple)")
        self.t4rButton.setStyleSheet("background-color: #9966CC; font-weight: bold; padding: 8px;")
        self.t4rButton.setFixedWidth(buttonWidth)
        self.t4rButton.clicked.connect(lambda: self.onPlaceTangentClicked("T4R"))
        tangentLayout.addWidget(self.t4rButton, 0, qt.Qt.AlignHCenter)
        
        step2Layout.addWidget(tangentControlFrame)
        
        
        # T4L options in a better layout
        t4lOptionsGroup = qt.QGroupBox("Optional: T4L for Bilateral Analysis")
        t4lLayout = qt.QVBoxLayout(t4lOptionsGroup)
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


        
        step2Layout.addWidget(t4lOptionsGroup)
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


        # Find Intersections Button
        self.findIntersectionsButton = qt.QPushButton("Find Intersections")
        self.findIntersectionsButton.setStyleSheet("background-color: #99CC66; font-weight: bold; padding: 8px;")
        self.findIntersectionsButton.setFixedWidth(buttonWidth)
        self.findIntersectionsButton.clicked.connect(self.onFindIntersectionsClicked)
        t4lLayout.addWidget(self.findIntersectionsButton, 0, qt.Qt.AlignHCenter)

       
                
        mainLayout.addWidget(step2GroupBox)

        # STEP 3: Soft Tissue Comparison
        step3GroupBox = qt.QGroupBox("Step 3: Soft Tissue Comparison")
        step3Layout = qt.QVBoxLayout(step3GroupBox) # <-- First, we create the layout...
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



        mainLayout.addWidget(step3GroupBox)

        # Complete the scroll area setup
        scrollArea.setWidget(scrollContent)
        outerLayout = qt.QVBoxLayout(self.mainWidget)
        outerLayout.setContentsMargins(0, 0, 0, 0)
        outerLayout.addWidget(scrollArea)
        
        # Store state
        self.tangents = {}
        self.points = {}
        self.tangentNodes = {}
        self.planeNode = None
        self.landmarksNode = None

        # Store state
        self.tangents = {}
        self.points = {}
        self.tangentNodes = {}
        self.planeNode = None
        self.landmarksNode = None

        # Run our new "smart inventory" check!
        self.syncWithScene()
        
        # Show the widget
        self.mainWidget.show()
        
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
        """Creates the final T4 tangent line on the plane."""
        self.log("'Create T4 Line' button clicked.")

        # --- Safety Checks ---
        if self.planeNode is None:
            slicer.util.messageBox("Please create a plane first using Step 1.")
            return

        if "T4R" not in self.tangents:
            slicer.util.messageBox("Please place the T4R tangent first using Step 2.")
            return

        # Check if we should use the bilateral method (T4L exists)
        use_bilateral = "T4L" in self.tangents

        try:
            # --- Get Plane Information ---
            planeNormal = np.zeros(3)
            self.planeNode.GetNormalWorld(planeNormal)
            planeOrigin = np.zeros(3)
            self.planeNode.GetOriginWorld(planeOrigin)

            # --- Calculate T4 ---
            t4_start_point, t4_end_point = None, None

            if use_bilateral:
                self.log("Calculating T4 using bilateral method (T4R and T4L).")
                # Project both T4R and T4L to the plane
                t4r_start_proj = self.projectPointOntoPlane(self.tangents["T4R"]['start'], planeOrigin, planeNormal)
                t4r_end_proj = self.projectPointOntoPlane(self.tangents["T4R"]['end'], planeOrigin, planeNormal)
                t4l_start_proj = self.projectPointOntoPlane(self.tangents["T4L"]['start'], planeOrigin, planeNormal)
                t4l_end_proj = self.projectPointOntoPlane(self.tangents["T4L"]['end'], planeOrigin, planeNormal)

                # Average the start and end points to get the final T4
                t4_start_point = (t4r_start_proj + t4l_start_proj) / 2.0
                t4_end_point = (t4r_end_proj + t4l_end_proj) / 2.0
            else:
                self.log("Calculating T4 using unilateral method (T4R only).")
                # Just project T4R onto the plane
                t4_start_point = self.projectPointOntoPlane(self.tangents["T4R"]['start'], planeOrigin, planeNormal)
                t4_end_point = self.projectPointOntoPlane(self.tangents["T4R"]['end'], planeOrigin, planeNormal)

            # --- Visualize the Final T4 Line ---
            self.createTangentLine("T4", t4_start_point, t4_end_point, [0.6, 0.4, 0.8]) # Purple
            slicer.util.showStatusMessage("Final T4 tangent created successfully!", 3000)

        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred while creating T4: {e}")
            import traceback
            traceback.print_exc()



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
            """Update the visualization of a tangent after extension"""
            if tangentName in self.tangents and tangentName in self.tangentNodes:
                # Get the tangent
                tangent = self.tangents[tangentName]
                
                # Get the node
                node = self.tangentNodes[tangentName]
                
                # Update visualization based on node type
                if isinstance(node, slicer.vtkMRMLMarkupsLineNode):
                    # For markup lines
                    if isinstance(tangent, dict):
                        node.SetNthControlPointPosition(0, tangent['start'])
                        node.SetNthControlPointPosition(1, tangent['end'])
                    else:  # vtkLineSource
                        node.SetNthControlPointPosition(0, tangent.GetPoint1())
                        node.SetNthControlPointPosition(1, tangent.GetPoint2())
                else:
                    # For model nodes or other types
                    if isinstance(tangent, vtk.vtkLineSource):
                        node.SetPolyDataConnection(tangent.GetOutputPort())
                    
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
        
    def onDownloadLandmarksClicked(self):
            """Download landmarks from GitHub"""
            try:
                # Try primary URL first
                primaryUrl = "https://github.com/user-attachments/files/22078845/Gerasimow_landmarks.mrk.json"
                
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
        
    def checkAndUseExistingPoints(self):
            """Check for and use existing pronasale, R2, LR2, RR2 points"""
            if not self.landmarksNode:
                return
            
            pointsToCheck = ["pronasale", "R2", "LR2", "RR2"]
            foundPoints = []
            
            for name in pointsToCheck:
                idx = self.findPointByName(self.landmarksNode, name)
                if idx >= 0:
                    pos = [0, 0, 0]
                    self.landmarksNode.GetNthControlPointPosition(idx, pos)
                    
                    # Map pronasale to R1 in our internal dict
                    internalName = "R1" if name == "pronasale" else name
                    self.points[internalName] = pos
                    foundPoints.append(name)
            
            if foundPoints:
                self.log(f"Found existing points in landmarks: {', '.join(foundPoints)}")
                self.showGuidanceDialog(f"Found existing points: {', '.join(foundPoints)}\nThese will be used automatically.")
        
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
                
                # Set the origin of the new plane to the first point
                planeNode.SetOrigin(points[0])
                
                # Set the normal of the new plane
                planeNode.SetNormal(planeNormal)
                
                # Make plane visible and adjust appearance
                planeNode.GetDisplayNode().SetOpacity(0.7)
                planeNode.GetDisplayNode().SetColor(0.7, 0.3, 0.3)  # Reddish color for visibility
                
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
            
            # Create T3 (offset from T2)
            t3_center = t2_center + 20 * y_axis
            t3_start = t3_center - 15 * x_axis
            t3_end = t3_center + 15 * x_axis
            self.createTangentLine("T3", t3_start, t3_end, [0.8, 0.6, 1.0])  # Lilac
            
            # Show guidance to the user
            self.showGuidanceDialog(
                "Default tangent lines have been created on the plane.\n\n"
                "Please adjust them to the correct positions:\n"
                "• T1 (Yellow): Last third of the nasal bone\n"
                "• T2 (Green): Direction of anterior nasal spine\n"
                "• T3 (Lilac): Last 1-2 mm of the nasal bone\n\n"
                "Click on the lines to select them, then drag the control points to adjust."
            )

    def createTangentLine(self, tangentName, startPoint, endPoint, color):
            """Create a tangent line with specified start and end points"""
            # Create a line node
            lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", tangentName)
            
            # Add exactly 2 control points (start and end)
            lineNode.AddControlPoint(startPoint)
            lineNode.AddControlPoint(endPoint)
            
            # Set the color
            lineNode.GetDisplayNode().SetSelectedColor(color)
            lineNode.GetDisplayNode().SetColor(color)
            
            # Store the tangent info
            self.tangents[tangentName] = {
                'start': startPoint.tolist() if isinstance(startPoint, np.ndarray) else startPoint,
                'end': endPoint.tolist() if isinstance(endPoint, np.ndarray) else endPoint,
                'vector': (np.array(endPoint) - np.array(startPoint)).tolist()
            }
            
            # Store the node
            self.tangentNodes[tangentName] = lineNode
            
            # If T1, T2, T3, constrain to plane
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
            """Handle placing a tangent with guidance"""
            if tangentName in self.tangentNodes:
                self.log(f"Tangent {tangentName} already exists.")
                slicer.util.messageBox(f"The tangent '{tangentName}' already exists. If you want to re-place it, please delete it from the Data module first.")
                return # Stop the function here
            try:
                # Create a line node
                lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", tangentName)
                
                # Set color and instruction based on tangent name
                if tangentName == "T1":
                    color = [1.0, 1.0, 0.0]  # Yellow
                    instruction = "Place T1 (Yellow): Draw a line following the last third of the nasal bone"
                elif tangentName == "T2":
                    color = [0.0, 1.0, 0.0]  # Green
                    instruction = "Place T2 (Green): Draw a line following the direction of the anterior nasal spine"
                elif tangentName == "T3":
                    color = [0.8, 0.6, 1.0]  # Lilac
                    instruction = "Place T3 (Lilac): Draw a line following the last 1-2 mm of the nasal bone"
                elif tangentName == "T4R":
                    color = [0.6, 0.4, 0.8]  # Purple
                    instruction = "Place T4R (Purple): Draw a line following the direction of the nasal floor on the right side"
                elif tangentName == "T4L":
                    color = [0.6, 0.4, 0.8]  # Purple
                    instruction = "Place T4L (Purple): Draw a line following the direction of the nasal floor on the left side"
                else:
                    color = [1.0, 1.0, 1.0]  # White
                    instruction = f"Place {tangentName} tangent"
                
                lineNode.GetDisplayNode().SetSelectedColor(color)
                lineNode.GetDisplayNode().SetColor(color)
                
                # Constrain T1, T2, and T3 to the plane
                if tangentName in ["T1", "T2", "T3"]:
                    if self.planeNode:
                        self.setPlaneConstraint(lineNode, self.planeNode)
                
                # Show tangent-specific instruction with Next button
                self.showGuidanceDialog(instruction)
                
                # Start placement mode
                selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
                selectionNode.SetReferenceActivePlaceNodeID(lineNode.GetID())
                selectionNode.SetActivePlaceNodeClassName("vtkMRMLMarkupsLineNode")
                
                interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
                interactionNode.SetCurrentInteractionMode(interactionNode.Place)
                
                # Store the node
                self.tangentNodes[tangentName] = lineNode
                
                # Set up observer for when the line is complete
                lineNode.AddObserver(lineNode.PointPositionDefinedEvent, 
                                    lambda caller, event: self.onTangentComplete(tangentName, caller))
                
                self.log(f"Starting placement of {tangentName} tangent")
                
                # Add observer to monitor when user exits placement mode
                interactionNode.AddObserver(
                    interactionNode.InteractionModeChangedEvent,
                    lambda caller, event: self.onInteractionModeChanged(tangentName)
                )
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

    def onExtendTangentsClicked(self):
            """Extend all tangents including T4 to ensure intersection"""
            self.log("Extending tangents to ensure intersection")
            
            try:
                # Check which tangents exist
                tangentNames = list(self.tangents.keys())
                self.log(f"Found tangents: {', '.join(tangentNames)}")
                
                # Make sure we have the required tangents
                requiredTangents = ["T1", "T2", "T3"]
                for name in requiredTangents:
                    if name not in self.tangents:
                        slicer.util.messageBox(f"Missing tangent {name}! Create it first.")
                        return
                        
                # Include T4 if it exists
                if "T4" in self.tangents:
                    requiredTangents.append("T4")
                    self.log("Including T4 in tangent extension")
                elif "T4R" in self.tangents:
                    # Use T4R if T4 doesn't exist yet
                    self.tangents["T4"] = self.tangents["T4R"]
                    requiredTangents.append("T4")
                    self.log("Using T4R as T4 for tangent extension")
                
                # Calculate bounding box to determine extension distance
                bounds = self.calculateSceneBounds()
                maxDimension = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])
                extensionLength = maxDimension * 2
                
                # Extend each tangent
                for name in requiredTangents:
                    self.extendTangent(name, extensionLength)
                        
                # Visualize the extended tangents
                for name in requiredTangents:
                    self.updateTangentVisualization(name)
                        
                self.log("Tangents extended successfully")
                slicer.util.showStatusMessage("Tangents extended!", 2000)
                    
            except Exception as e:
                slicer.util.errorDisplay(f"Error extending tangents: {str(e)}")
        
    def onR2MethodChanged(self, button):
            """Handle R2 method selection"""
            isManual = button == self.manualR2RadioButton
            self.placeR2Button.setVisible(isManual)
            self.automaticR2Frame.setVisible(not isManual)
            self.log(f"Switched to {'manual' if isManual else 'automatic'} R2 placement")
        
    def onPlacePointClicked(self, pointName):
            """Handle place point button click"""
            self.log(f"Placing {pointName} point")
            
            # Create a fiducial node for the point
            pointNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", pointName)
            pointNode.SetMarkupLabelFormat(pointName)
            
            # Updated point descriptions with correct definitions
            pointDescriptions = {
                "R2": "Place at the point where the nasal spine line (T4) crosses the surface of the nasal soft tissue on the midsagittal plane (use if only one side was used for T4)",
                "LR2": "Place at the point where the nasal spine line (T2) crosses the surface of the nasal soft tissue on the left",
                "RR2": "Place at the point where the nasal spine line (T2) crosses the surface of the nasal soft tissue on the right"
            }
            
            # Start placement mode
            selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
            selectionNode.SetReferenceActivePlaceNodeID(pointNode.GetID())
            selectionNode.SetActivePlaceNodeClassName("vtkMRMLMarkupsFiducialNode")
            
            interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
            interactionNode.SetCurrentInteractionMode(interactionNode.Place)
            
            # Set up observer for when the point is placed
            pointNode.AddObserver(pointNode.PointPositionDefinedEvent, 
                            lambda caller, event: self.onPointPlaced(pointName, caller))
            
            # Show guidance with updated description
            if pointName in pointDescriptions:
                self.showGuidanceDialog(pointDescriptions[pointName])
        
    def onPointPlaced(self, pointName, node):
            """Handle when a point is placed"""
            if node.GetNumberOfControlPoints() > 0:
                position = [0, 0, 0]
                node.GetNthControlPointPosition(0, position)
                
                # Store the point
                self.points[pointName] = position
                
                self.log(f"Placed {pointName} point at {position}")
                
                # Stop placement mode
                interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
                interactionNode.SetCurrentInteractionMode(interactionNode.ViewTransform)
                
                # If automatic R2 calculation, suggest next step
                if pointName == "LR2" and "RR2" not in self.points:
                    self.showGuidanceDialog("Now place the RR2 point where the nasal spine line (T2) crosses the surface on the right", 
                                        lambda: self.onPlacePointClicked("RR2"))
                elif pointName == "RR2" and "LR2" in self.points:
                    self.showGuidanceDialog("Now you can calculate R2 from LR2 and RR2", 
                                        lambda: self.onCalculateR2Clicked())
        
    def onCalculateR2Clicked(self):
            """Handle calculate R2 button click with options for intersection or geometric mean"""
            if "LR2" not in self.points or "RR2" not in self.points:
                slicer.util.errorDisplay("Please place both LR2 and RR2 points first.")
                return
            
            try:
                lr2 = np.array(self.points["LR2"])
                rr2 = np.array(self.points["RR2"])
                
                # Check which method to use
                useIntersection = self.intersectionR2RadioButton.isChecked()
                
                if useIntersection and self.planeNode:
                    # Calculate R2 as the intersection of the LR2-RR2 line with the plane
                    planeNormal = [0, 0, 0]
                    self.planeNode.GetNormal(planeNormal)
                    
                    planeOrigin = [0, 0, 0]
                    self.planeNode.GetOrigin(planeOrigin)
                    
                    r2 = self.calculateIntersection(lr2, rr2, planeOrigin, planeNormal)
                    methodName = "intersection with plane"
                else:
                    # Calculate R2 as the geometric mean of LR2 and RR2
                    r2 = (lr2 + rr2) / 2
                    methodName = "geometric mean"
                
                # Store the R2 point
                self.points["R2"] = r2.tolist()
                
                # Create a fiducial for R2
                r2Node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "R2_Calculated")
                r2Node.SetMarkupLabelFormat("R2")
                r2Node.AddControlPoint(r2.tolist())
                
                self.log(f"Calculated R2 point using {methodName}")
                self.showGuidanceDialog(f"R2 calculated using {methodName}")
                
            except Exception as e:
                slicer.util.errorDisplay(f"Error calculating R2: {str(e)}")
        
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

            slicer.util.showStatusMessage("Error comparison lines created successfully!", 4000)
            self.log("Successfully created all error comparison lines.")

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


# Add this right before creating your predictor instance
print("About to create Gerasimow Nose Predictor GUI...")

# Then create your instance
gerasimowPredictor = GerasimowNosePredictor()

# Add this right after
print("GUI created successfully!")
print(f"Main widget exists: {gerasimowPredictor.mainWidget is not None}")
print(f"Main widget is visible: {gerasimowPredictor.mainWidget.isVisible()}")    
