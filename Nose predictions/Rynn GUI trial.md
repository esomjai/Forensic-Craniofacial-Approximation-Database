```python

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile

# --- Main GUI Class ---
class RynnMethodGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Rynn (2010) Method")
        self.setObjectName("RynnMethodGUI")

        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setSpacing(10)

        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        # To keep track of the active profile plane (INB or MSP)
        self.activeProfilePlaneName = "INB" 

        # Create the UI for each step
        self.createAllStepWidgets()
        
        # Create the navigation buttons
        self.setupNavigation()

        self.currentStep = 0
        self.updateStepUI()

    def createAllStepWidgets(self):
        """Creates and adds all the step widgets to the stacked widget."""
        self.createStep1_Welcome()
        self.createStep2_LandmarkSetup()
        self.createStep3_PlaneSetup()
        self.createStep4_Scaffolding()
        # Future steps will be added here

    def setupNavigation(self):
        """Creates the 'Previous' and 'Next' buttons for navigation."""
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        navLayout.setContentsMargins(0, 0, 0, 0)
        
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.clicked.connect(self.onPrevButtonClicked)
        
        self.stepLabel = qt.QLabel("Step 1/4")
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

    # --- Step 1: Welcome Screen ---
    def createStep1_Welcome(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Welcome to the Rynn (2010) Method GUI")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel("This tool provides a guided workflow for the Rynn nasal prediction method.\n\nClick 'Next' to begin.")
        desc.setWordWrap(True)
        desc.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(desc)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    # --- Step 2: Landmark Setup ---
    def createStep2_LandmarkSetup(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)

        title = qt.QLabel("Step 2: Load and Place Landmarks")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Button to download landmarks
        self.downloadHardButton = qt.QPushButton("1. Download Hard Tissue Landmarks")
        self.downloadHardButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;")
        self.downloadHardButton.clicked.connect(self.onDownloadHardLandmarks)
        layout.addWidget(self.downloadHardButton)
        
        # Informative note for the user
        noteLabel = qt.QLabel()
        noteLabel.setTextFormat(qt.Qt.RichText)
        noteLabel.setWordWrap(True)
        noteLabel.setText(
            "<b>2. Place the following landmarks on your model.</b><br><br>"
            "If you are only interested in reproducing the x, y, z axes and the pron ant, pron vert, "
            "pron pFHP, nasal length (nas ln), nasal height (nas ht), nasal depth (nas dp) measurements, "
            "<b>allocate ONLY these hard tissue landmarks:</b>"
        )
        layout.addWidget(noteLabel)

        # Landmark Table
        self.landmarkTable = qt.QTableWidget(7, 1)
        self.landmarkTable.setHorizontalHeaderLabels(["Required Hard Tissue Landmarks"])
        landmarks = ["nasion", "inion (if visible)", "bregma (if visible)", "prosthion", "subspinale", "rhinion", "acanthion"]
        for i, landmark in enumerate(landmarks):
            self.landmarkTable.setItem(i, 0, qt.QTableWidgetItem(landmark))
        self.landmarkTable.horizontalHeader().setStretchLastSection(True)
        self.landmarkTable.verticalHeader().setVisible(False)
        self.landmarkTable.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.landmarkTable.setFixedHeight(self.landmarkTable.verticalHeader().defaultSectionSize * self.landmarkTable.rowCount + self.landmarkTable.horizontalHeader().height)
        layout.addWidget(self.landmarkTable)

        # Selector to confirm the node
        selectorLayout = qt.QFormLayout()
        self.landmarksSelector = slicer.qMRMLNodeComboBox()
        self.landmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.landmarksSelector.setMRMLScene(slicer.mrmlScene)
        self.landmarksSelector.addEnabled = False
        self.landmarksSelector.removeEnabled = False
        self.landmarksSelector.noneEnabled = True
        selectorLayout.addRow("<b>3. Confirm Landmark Node:</b>", self.landmarksSelector)
        layout.addLayout(selectorLayout)

        self.step2StatusLabel = qt.QLabel("Status: Waiting for user to download landmarks.")
        self.step2StatusLabel.setWordWrap(True)
        layout.addWidget(self.step2StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    # --- Step 3: Plane Creation ---
    def createStep3_PlaneSetup(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)

        title = qt.QLabel("Step 3: Create Reference Planes")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel("First, choose a method to define the primary profile plane (INB or MSP). The tool will then automatically generate the required NPP and PTP planes based on your choice.")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Plane choice
        planeChoiceLayout = qt.QFormLayout()
        self.planeChoiceComboBox = qt.QComboBox()
        self.planeChoiceComboBox.addItems(["Select a method...", "INB (Inion-Nasion-Bregma)", "MSP (Midsagittal Best-Fit)"])
        planeChoiceLayout.addRow("Profile Plane Method:", self.planeChoiceComboBox)
        layout.addLayout(planeChoiceLayout)

        # Create button
        self.createPlanesButton = qt.QPushButton("Create All Reference Planes")
        self.createPlanesButton.clicked.connect(self.onCreatePlanes)
        layout.addWidget(self.createPlanesButton)

        self.step3StatusLabel = qt.QLabel("Status: Please choose a plane creation method.")
        self.step3StatusLabel.setWordWrap(True)
        layout.addWidget(self.step3StatusLabel)

        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    # --- Step 4: Scaffolding ---
    def createStep4_Scaffolding(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)

        title = qt.QLabel("Step 4: Create Geometric Scaffolding")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Group for Axes
        axesGroup = qt.QGroupBox("1. Coordinate Axes")
        axesLayout = qt.QVBoxLayout(axesGroup)
        axesDesc = qt.QLabel("Create the X, Y, and Z axes based on the reference planes.")
        axesDesc.setWordWrap(True)
        self.createAxesButton = qt.QPushButton("Create X, Y, Z Axes")
        self.createAxesButton.clicked.connect(self.onCreateAxes)
        axesLayout.addWidget(axesDesc)
        axesLayout.addWidget(self.createAxesButton)
        layout.addWidget(axesGroup)

        # Group for Network Lines
        networkGroup = qt.QGroupBox("2. Reference Network")
        networkLayout = qt.QVBoxLayout(networkGroup)
        networkDesc = qt.QLabel("Create the three parallel reference lines (1, 2, and 3).")
        networkDesc.setWordWrap(True)
        self.createNetworkButton = qt.QPushButton("Create Network Lines 1, 2, 3")
        self.createNetworkButton.clicked.connect(self.onCreateNetwork)
        networkLayout.addWidget(networkDesc)
        networkLayout.addWidget(self.createNetworkButton)
        layout.addWidget(networkGroup)

        self.step4StatusLabel = qt.QLabel("Status: Waiting for user.")
        self.step4StatusLabel.setWordWrap(True)
        layout.addWidget(self.step4StatusLabel)

        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    # --- Navigation and UI Update Logic ---
    def onPrevButtonClicked(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()

    def onNextButtonClicked(self):
        if self.currentStep < self.stepStack.count - 1:
            self.currentStep += 1
            self.updateStepUI()

    def updateStepUI(self):
        """Updates the UI elements based on the current step."""
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)
        
        # Automatically select the 'Rynn_hard_tissue' node if it exists
        rynn_node = slicer.util.getFirstNodeByName("Rynn_hard_tissue")
        if rynn_node:
            self.landmarksSelector.setCurrentNode(rynn_node)
            self.step2StatusLabel.setText("Status: 'Rynn_hard_tissue' found. Please place points, then proceed.")

    # --- Helper function to get landmark positions ---
    def get_landmark_positions(self, node, required_landmarks):
        """
        Gets landmark positions from a node, ignoring case and handling optional points.
        Returns a dictionary of positions.
        """
        positions = {}
        # First, get all available points from the node, converted to lowercase
        available_points = {}
        for i in range(node.GetNumberOfControlPoints()):
            label = node.GetNthControlPointLabel(i).lower()
            pos = np.zeros(3)
            node.GetNthControlPointPositionWorld(i, pos)
            available_points[label] = pos

        # Now, check for the required landmarks
        for name in required_landmarks:
            # Clean the required name, e.g., "inion (if visible)" -> "inion"
            clean_name = name.lower().split(" ")[0]
            
            if clean_name in available_points:
                positions[clean_name] = available_points[clean_name]
            else:
                # If the point is not optional, raise an error
                if "(if visible)" not in name:
                    raise ValueError(f"The required landmark '{clean_name}' was not found. Please place it and try again.")
        return positions
        
    # --- Button Click Logic ---
    def downloadAndLoad(self, url, nodeName, statusLabel):
        """Generic function to download and load a landmark file."""
        statusLabel.setText(f"Status: Downloading {nodeName}...")
        slicer.app.processEvents()
        
        try:
            # Remove existing node to avoid duplicates
            existing_node = slicer.util.getFirstNodeByName(nodeName)
            if existing_node:
                slicer.mrmlScene.RemoveNode(existing_node)

            # Download the file to a temporary location
            with urllib.request.urlopen(url) as response:
                fileData = response.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile:
                tempFile.write(fileData)
                tempFilePath = tempFile.name

            # Load the landmarks from the temp file without changing the camera view
            properties = {"center": False}
            loadedNode = slicer.util.loadMarkups(tempFilePath, properties)
            os.remove(tempFilePath) # Clean up the temp file

            if loadedNode:
                loadedNode.SetName(nodeName)
                slicer.util.showStatusMessage(f"'{nodeName}' loaded!", 3000)
                
                # --- THIS IS THE UPDATED PART ---
                # We only update the selector and status label. We do NOT
                # switch modules or activate the list, which prevents the view from changing.
                if "hard" in nodeName.lower():
                    self.landmarksSelector.setCurrentNode(loadedNode)
                    statusLabel.setText(f"Status: '{nodeName}' loaded. You can now place the points on your model.")
                else:
                    statusLabel.setText(f"Status: Hard and soft tissue landmarks loaded.")

            else:
                raise IOError("Failed to load landmarks from the downloaded file.")
                
        except Exception as e:
            statusLabel.setText(f"Status: Error! Could not download or load {nodeName}. Error: {e}")
            slicer.util.errorDisplay(f"Failed to get {nodeName}: {e}")

    def onDownloadHardLandmarks(self):
        """Downloads the Rynn hard tissue landmark file."""
        url = "https://github.com/user-attachments/files/22989769/Rynn_hard_tissue.mrk.json"
        self.downloadAndLoad(url, "Rynn_hard_tissue", self.step2StatusLabel)

    def onCreatePlanes(self):
        """Creates the primary profile plane and the dependent NPP and PTP planes."""
        self.step3StatusLabel.setText("Status: Processing planes...")
        slicer.app.processEvents()
        
        try:
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                raise ValueError("Please select or confirm the landmark node in Step 2.")

            choice_index = self.planeChoiceComboBox.currentIndex
            if choice_index == 0:
                raise ValueError("Please select a plane creation method (INB or MSP).")

            # Helper to create or update a plane
            def create_or_update_plane(name, origin, normal, color, size=300):
                planeNode = slicer.util.getFirstNodeByName(name)
                if not planeNode:
                    planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', name)
                
                planeNode.SetOrigin(origin)
                planeNode.SetNormal(normal)
                planeNode.SetSize(size, size)
                displayNode = planeNode.GetDisplayNode()
                if not displayNode:
                    planeNode.CreateDefaultDisplayNodes()
                    displayNode = planeNode.GetDisplayNode()
                displayNode.SetSelectedColor(color)
                displayNode.SetOpacity(0.8)
                return planeNode

            profile_plane = None
            if choice_index == 1: # INB Plane
                self.activeProfilePlaneName = "INB"
                required = ["inion (if visible)", "nasion", "bregma (if visible)"]
                positions = self.get_landmark_positions(landmarksNode, required)
                if 'inion' not in positions or 'bregma' not in positions:
                    raise ValueError("The INB method requires both 'inion' and 'bregma' landmarks. Please place them if they are visible on your model.")
                v1 = positions['nasion'] - positions['inion']
                v2 = positions['bregma'] - positions['inion']
                profile_normal = np.cross(v1, v2)
                profile_normal /= np.linalg.norm(profile_normal)
                profile_plane = create_or_update_plane('INB', positions['inion'], profile_normal, (1, 0, 0))
            
            elif choice_index == 2: # MSP Plane
                self.activeProfilePlaneName = "MSP"
                required = ["nasion", "acanthion", "prosthion", "subspinale"]
                positions = self.get_landmark_positions(landmarksNode, required)
                points = np.array(list(positions.values()))
                
                centroid = np.mean(points, axis=0)
                covariance_matrix = np.cov(points - centroid, rowvar=False)
                eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
                
                profile_normal = eigenvectors[:, np.argmin(eigenvalues)]
                profile_plane = create_or_update_plane('MSP', centroid, profile_normal, (1, 0.5, 0))

            # Now create NPP and PTP based on the profile plane
            if profile_plane:
                nasion_pos = self.get_landmark_positions(landmarksNode, ["nasion"])["nasion"]
                prosthion_pos = self.get_landmark_positions(landmarksNode, ["prosthion"])["prosthion"]
                
                # Create NPP (Nasal Profile Plane)
                vectorPN = nasion_pos - prosthion_pos
                npp_normal = np.cross(np.array(profile_plane.GetNormal()), vectorPN)
                npp_normal /= np.linalg.norm(npp_normal)
                create_or_update_plane('NPP', prosthion_pos, npp_normal, (0, 1, 0))
                
                # Create PTP (Trans-Porion Plane), perpendicular to both Profile and NPP
                ptp_normal = np.cross(np.array(profile_plane.GetNormal()), npp_normal)
                ptp_normal /= np.linalg.norm(ptp_normal)
                create_or_update_plane('PTP', nasion_pos, ptp_normal, (0, 0, 1))
                
                self.step3StatusLabel.setText(f"Status: Successfully created '{self.activeProfilePlaneName}', 'NPP', and 'PTP' planes.")
            else:
                raise RuntimeError("Failed to create the primary profile plane.")

        except Exception as e:
            self.step3StatusLabel.setText(f"Status: Error! {e}")
            slicer.util.errorDisplay(f"Failed to create planes: {e}")

    def onCreateAxes(self):
        """Creates the X, Y, and Z axes based on landmark positions."""
        self.step4StatusLabel.setText("Status: Creating X, Y, Z axes...")
        slicer.app.processEvents()
        try:
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                raise ValueError("Landmark node not found. Please complete Step 2.")

            # Define a helper to create a line
            def create_axis_line(name, start_pos, end_pos, color):
                # Remove old line if it exists
                oldLine = slicer.util.getFirstNodeByName(name)
                if oldLine:
                    slicer.mrmlScene.RemoveNode(oldLine)
                
                line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
                line.AddControlPoint(start_pos)
                line.AddControlPoint(end_pos)
                displayNode = line.GetDisplayNode()
                displayNode.SetColor(color)
                displayNode.SetSelectedColor(color)
                return line

            # Get all required points at once
            required = ["nasion", "acanthion", "rhinion", "subspinale"]
            positions = self.get_landmark_positions(landmarksNode, required)

            # X axis (nas-aca)
            create_axis_line('nas-aca X', positions['nasion'], positions['acanthion'], (1, 0, 0)) # Red

            # Y axis (rhi-subs)
            create_axis_line('rhi-subs Y', positions['rhinion'], positions['subspinale'], (0, 1, 0)) # Green

            # Z axis (nas-subs)
            create_axis_line('nas-subs Z', positions['nasion'], positions['subspinale'], (0, 0, 0)) # Black

            self.step4StatusLabel.setText("Status: X, Y, and Z axes created successfully.")

        except Exception as e:
            self.step4StatusLabel.setText(f"Status: Error creating axes! {e}")
            slicer.util.errorDisplay(f"Failed to create axes: {e}")

    def onCreateNetwork(self):
        """Creates the parallel network lines 1, 2, and 3."""
        self.step4StatusLabel.setText("Status: Creating network lines...")
        slicer.app.processEvents()
        try:
            # Check for all required nodes first
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                raise ValueError("Landmark node not found.")
            
            npp_plane = slicer.util.getNode("NPP")
            ptp_plane = slicer.util.getNode("PTP")
            fhp_plane = slicer.util.getNode("FHP") # This is the critical one
            
            if not all([npp_plane, ptp_plane, fhp_plane]):
                raise ValueError("One or more required planes (NPP, PTP, FHP) not found in the scene. Please create the FHP plane manually for now.")
                
            # Helper function from your snippet
            def create_line(name, length, color, start_point, direction):
                # Remove old line if it exists
                oldLine = slicer.util.getFirstNodeByName(name)
                if oldLine:
                    slicer.mrmlScene.RemoveNode(oldLine)
            
                line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
                line.GetDisplayNode().SetSelectedColor(color)
                half_length = length / 2
                start_point = np.array(start_point)
                # Normalize direction to be safe
                norm_direction = np.array(direction) / np.linalg.norm(direction)
                line.AddControlPoint((start_point - norm_direction * half_length).tolist())
                line.AddControlPoint((start_point + norm_direction * half_length).tolist())
                return line

            # Get landmark positions using the specific indices from your original code
            # This is less flexible but matches the code that you know works
            start_point_1_vec = [0,0,0]; landmarksNode.GetNthControlPointPositionWorld(0, start_point_1_vec)
            start_point_3_vec = [0,0,0]; landmarksNode.GetNthControlPointPositionWorld(4, start_point_3_vec)

            # Get plane normals
            npp_normal = np.array(npp_plane.GetNormal())
            ptp_normal = np.array(ptp_plane.GetNormal())
            fhp_normal = np.array(fhp_plane.GetNormal())

            # --- THIS IS YOUR ORIGINAL, WORKING LOGIC ---
            reference = np.array([1, 0, 0])
            if np.allclose(fhp_normal, reference):
                reference = np.array([0, 1, 0])
            fhp_plane_direction = np.cross(fhp_normal, reference)
            
            # Create the lines
            orange_color = (1.0, 0.5, 0.0)
            create_line("1", 200, orange_color, start_point_1_vec, npp_normal)
            create_line("2", 200, orange_color, start_point_1_vec, ptp_normal)
            create_line("3", 200, orange_color, start_point_3_vec, fhp_plane_direction)

            self.step4StatusLabel.setText("Status: Network lines 1, 2, and 3 created successfully.")

        except Exception as e:
            self.step4StatusLabel.setText(f"Status: Error creating network! {e}")
            slicer.util.errorDisplay(f"Failed to create network lines: {e}")


# --- Entry Point to start the GUI ---
try:
    # This makes sure the GUI is not created multiple times
    old_gui = slicer.util.mainWindow().findChild(qt.QWidget, "RynnMethodGUI")
    if old_gui:
        old_gui.deleteLater()
except:
    pass # No instance found

# Create and show the GUI
rynnGui = RynnMethodGUI()
rynnGui.show()
```
