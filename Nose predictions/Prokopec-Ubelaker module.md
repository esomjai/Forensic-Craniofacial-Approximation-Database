# ProkopecUbelakerGUI.py
# A beginner-friendly GUI for the Prokopec-Ubelaker nasal prediction method
# Just copy-paste this entire script into 3D Slicer's Python console!

# ProkopecUbelakerGUI.py
# A beginner-friendly GUI for the Prokopec-Ubelaker nasal prediction method
# Just copy-paste this entire script into 3D Slicer's Python console!

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import math  # Add this import

class ProkopecUbelakerGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.mainLayout = qt.QVBoxLayout(self)  # Use mainLayout instead of layout
        
        # Create stacked widget for steps
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        # Create step widgets
        self.createStepWidgets()
        
        # Set up navigation
        self.setupNavigation()
        
        # Initialize step tracking
        self.currentStep = 0
        self.updateStepUI()
        
    def setupNavigation(self):
        """Set up navigation buttons"""
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        
        # Previous button
        self.prevButton = qt.QPushButton("← Previous")
        self.prevButton.setMaximumWidth(120)
        navLayout.addWidget(self.prevButton)
        self.prevButton.connect('clicked(bool)', self.onPrevButtonClicked)
        
        # Step counter
        self.stepLabel = qt.QLabel("Step 1/9")
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        navLayout.addWidget(self.stepLabel)
        
        # Next button
        self.nextButton = qt.QPushButton("Next →")
        self.nextButton.setMaximumWidth(120)
        navLayout.addWidget(self.nextButton)
        self.nextButton.connect('clicked(bool)', self.onNextButtonClicked)
        
        # Help button
        self.helpButton = qt.QPushButton("Help")
        self.helpButton.setMaximumWidth(80)
        navLayout.addWidget(self.helpButton)
        self.helpButton.connect('clicked(bool)', self.onHelpClicked)
        
        self.mainLayout.addWidget(navWidget)
        
    def onPrevButtonClicked(self):
        """Go to previous step"""
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()
            print(f"Now showing step {self.currentStep+1}")
            
    def onNextButtonClicked(self):
        """Go to next step"""
        if self.currentStep < self.stepStack.count - 1:
            self.currentStep += 1
            self.updateStepUI()
            print(f"Now showing step {self.currentStep+1}")
            
    def checkPrerequisites(self):
        """Check if prerequisites are completed"""
        # Create a message box for the FHP alignment check
        messageBox = qt.QMessageBox()
        messageBox.setIcon(qt.QMessageBox.Question)
        messageBox.setWindowTitle("Prerequisite Check")
        messageBox.setText("Before proceeding, please confirm that your skull model is properly aligned in the Frankfurt Horizontal Plane (FHP).")
        messageBox.setInformativeText("Has the skull model been aligned in the FHP?")
        messageBox.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.No)
        messageBox.setDefaultButton(qt.QMessageBox.No)
        
        # Show the message box
        choice = messageBox.exec_()
        
        # If the user hasn't aligned the skull, show instructions
        if choice == qt.QMessageBox.No:
            # Create a dialog with more options (NON-MODAL so user can interact with scene)
            alignmentDialog = qt.QDialog()
            alignmentDialog.setWindowTitle("FHP Alignment Helper")
            alignmentDialog.setMinimumWidth(500)
            alignmentDialog.setWindowFlags(qt.Qt.Window | qt.Qt.WindowStaysOnTopHint)  # Make non-modal!
            layout = qt.QVBoxLayout(alignmentDialog)
            
            # Add instructions label
            instructionsLabel = qt.QLabel("Please align the skull in the FHP before using this tool.")
            instructionsLabel.setWordWrap(True)
            layout.addWidget(instructionsLabel)
            
            # Add detailed instructions with link
            detailedLabel = qt.QLabel(
                "Quick steps for FHP alignment:\n\n"
                "1. Load your CT volume in 3D Slicer\n"
                "2. Download and place the FHP landmarks onto the cranium (3 points)\n"
                "3. Run the automatic FHP alignment\n"
                "4. Harden the transform when finished"
            )
            detailedLabel.setWordWrap(True)
            layout.addWidget(detailedLabel)
            
            # Add link to detailed instructions
            linkLabel = qt.QLabel("<a href='https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Start%20here%20/002_Realign%20CT%20in%20the%20standard%20FHP.md#re-alignment-of-scans'>View detailed instructions on GitHub</a>")
            linkLabel.setOpenExternalLinks(True)
            layout.addWidget(linkLabel)
            
            # Add volume selector (right after the link label)
            volumeSelectFrame = qt.QFrame()
            volumeSelectLayout = qt.QFormLayout(volumeSelectFrame)
            volumeSelector = slicer.qMRMLNodeComboBox()
            volumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
            volumeSelector.selectNodeUponCreation = True
            volumeSelector.addEnabled = False
            volumeSelector.removeEnabled = False
            volumeSelector.noneEnabled = True
            volumeSelector.setMRMLScene(slicer.mrmlScene)
            volumeSelector.setToolTip("Select the skull volume to align")
            volumeSelectLayout.addRow("Skull Volume:", volumeSelector)
            layout.addWidget(volumeSelectFrame)
            
            # Add spacing
            layout.addSpacing(10)
            
            # Add download landmarks button
            downloadButton = qt.QPushButton("Download FHP Landmarks")
            layout.addWidget(downloadButton)
            
            # Add status label
            statusLabel = qt.QLabel("Ready to download FHP landmarks...")
            statusLabel.setWordWrap(True)
            layout.addWidget(statusLabel)
            
            # Add run alignment button (initially disabled)
            alignmentButton = qt.QPushButton("Run Automatic FHP Alignment")
            alignmentButton.enabled = False
            layout.addWidget(alignmentButton)
            
            # Add alignment status label
            alignmentStatusLabel = qt.QLabel("")
            alignmentStatusLabel.setWordWrap(True)
            layout.addWidget(alignmentStatusLabel)
            
            # Add continue button (initially disabled)
            continueButton = qt.QPushButton("Continue to Nasal Prediction")
            continueButton.enabled = False
            layout.addWidget(continueButton)
            
            # Define button click functions
            def onDownloadLandmarksClicked():
                try:
                    # URL for the FHP landmarks
                    url = "https://github.com/user-attachments/files/21429663/FHP_landmarks.mrk.json"
                    
                    # Create a temporary file to download to
                    with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                        temp_path = temp_file.name
                    
                    try:
                        # Show download status
                        statusLabel.text = "Downloading landmarks..."
                        slicer.app.processEvents()
                        
                        # Download the file
                        urllib.request.urlretrieve(url, temp_path)
                        
                        # Load the downloaded file
                        fhpNode = slicer.util.loadMarkups(temp_path)
                        
                        if fhpNode:
                            # Rename for clarity
                            fhpNode.SetName("FHP_Landmarks")
                            statusLabel.text = "FHP Landmarks loaded successfully! Please adjust the points on your skull."
                            alignmentButton.enabled = True
                        else:
                            statusLabel.text = "Failed to load FHP landmarks."
                        
                        # Clean up the temporary file
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                            
                    except Exception as e:
                        statusLabel.text = f"Error downloading landmarks: {str(e)}"
                        
                except Exception as e:
                    statusLabel.text = f"Error: {str(e)}"
            
            def onAlignmentClicked():
                try:
                    alignmentStatusLabel.text = "Running FHP alignment... Please wait."
                    slicer.app.processEvents()
                    
                    # Find the FHP landmarks node
                    fhpNode = None
                    for node in slicer.mrmlScene.GetNodesByClass('vtkMRMLMarkupsFiducialNode'):
                        if node.GetName() == "FHP_Landmarks":
                            fhpNode = node
                            break
                    
                    if not fhpNode:
                        alignmentStatusLabel.text = "Error: FHP landmarks not found. Please download and place them first."
                        return
                    
                    # Get the selected volume
                    V = volumeSelector.currentNode()
                    if not V:
                        alignmentStatusLabel.text = "Error: No volume selected. Please select a skull model to align."
                        return
                    
                    # Get the fiducial IDs of porions and zygomatico-orbitale suture from the fiducial list by name
                    po1_id = -1; po2_id = -1; zyo_id = -1;
                    
                    for i in range(0, fhpNode.GetNumberOfControlPoints()):
                        if fhpNode.GetNthControlPointLabel(i) == 'poR':
                            po1_id = i
                        if fhpNode.GetNthControlPointLabel(i) == 'poL':
                            po2_id = i
                        if fhpNode.GetNthControlPointLabel(i) == 'zyoL':
                            zyo_id = i
                    
                    # Check if all landmarks were found
                    if po1_id == -1 or po2_id == -1 or zyo_id == -1:
                        alignmentStatusLabel.text = "Error: Could not find all required landmarks (poR, poL, zyoL)."
                        return
                    
                    # Get the coordinates of landmarks
                    po1 = [0, 0, 0]
                    po2 = [0, 0, 0]
                    zyo = [0, 0, 0]
                    
                    fhpNode.GetNthControlPointPosition(po1_id, po1)
                    fhpNode.GetNthControlPointPosition(po2_id, po2)
                    fhpNode.GetNthControlPointPosition(zyo_id, zyo)
                    
                    # The vector between two porions that we will align to LR axis by calculating the yaw angle
                    po = [po1[0] - po2[0], po1[1] - po2[1], po1[2] - po2[2]]
                    vTransform = vtk.vtkTransform()
                    vTransform.RotateZ(-np.arctan2(po[1], po[0]) * 180 / np.pi)
                    transform = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode')
                    transform.SetMatrixTransformToParent(vTransform.GetMatrix())
                    
                    # Apply the transform to the fiducials and the volume
                    V.SetAndObserveTransformNodeID(transform.GetID())
                    fhpNode.SetAndObserveTransformNodeID(transform.GetID())
                    
                    # Get the updated (transformed) coordinates from the list
                    po1 = [0, 0, 0]
                    po2 = [0, 0, 0]
                    zyo = [0, 0, 0]
                    
                    fhpNode.GetNthControlPointPosition(po1_id, po1)
                    fhpNode.GetNthControlPointPosition(po2_id, po2)
                    fhpNode.GetNthControlPointPosition(zyo_id, zyo)
                    
                    # Apply the transform to the coordinates
                    po1_t = vTransform.GetMatrix().MultiplyPoint([po1[0], po1[1], po1[2], 0])
                    po2_t = vTransform.GetMatrix().MultiplyPoint([po2[0], po2[1], po2[2], 0])
                    zyo_t = vTransform.GetMatrix().MultiplyPoint([zyo[0], zyo[1], zyo[2], 0])
                    po = [po1_t[0] - po2_t[0], po1_t[1] - po2_t[1], po1_t[2] - po2_t[2]]
                    
                    # Calculate the rotation for the roll 
                    vTransform2 = vtk.vtkTransform()
                    vTransform2.RotateY(np.arctan2(po[2], po[0]) * 180 / np.pi)
                    
                    # Apply the transform to previous transform hierarchy
                    transform2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode')
                    transform2.SetMatrixTransformToParent(vTransform2.GetMatrix())
                    transform.SetAndObserveTransformNodeID(transform2.GetID())
                    
                    # Get the coordinates again
                    po1 = [0, 0, 0]
                    po2 = [0, 0, 0]
                    zyo = [0, 0, 0]
                    
                    fhpNode.GetNthControlPointPosition(po1_id, po1)
                    fhpNode.GetNthControlPointPosition(po2_id, po2)
                    fhpNode.GetNthControlPointPosition(zyo_id, zyo)
                    
                    # The vector for pitch angle
                    po_zyo = [
                        zyo[0] - (po1[0] + po2[0]) / 2, 
                        zyo[1] - (po1[1] + po2[1]) / 2, 
                        zyo[2] - (po1[2] + po2[2]) / 2
                    ]
                    
                    # Calculate the transform for aligning pitch
                    vTransform3 = vtk.vtkTransform()
                    vTransform3.RotateX(-np.arctan2(po_zyo[2], po_zyo[1]) * 180 / np.pi)
                    
                    # Apply the transform to both fiducial list and the volume
                    transform3 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode')
                    transform3.SetMatrixTransformToParent(vTransform3.GetMatrix())
                    transform2.SetAndObserveTransformNodeID(transform3.GetID())
                    
                    # Harden the transform to apply it permanently
                    slicer.vtkSlicerTransformLogic().hardenTransform(V)
                    
                    # Update status and enable continue button
                    alignmentStatusLabel.text = "✅ Alignment completed successfully!"
                    continueButton.enabled = True
                    
                except Exception as e:
                    alignmentStatusLabel.text = f"❌ Alignment error: {str(e)}"
            
            def onContinueClicked():
                alignmentDialog.accept()
            
            # Connect button signals
            downloadButton.connect('clicked(bool)', onDownloadLandmarksClicked)
            alignmentButton.connect('clicked(bool)', onAlignmentClicked)
            continueButton.connect('clicked(bool)', onContinueClicked)
            
            # Show the dialog (non-modal)
            alignmentDialog.show()
            
            # We need another way to check the result since we're not using exec_()
            self.fhpDialogComplete = False
            
            def onDialogFinished(result):
                self.fhpDialogComplete = (result == qt.QDialog.Accepted)
                
            alignmentDialog.finished.connect(onDialogFinished)
            
            # Wait a moment to let user see instructions
            slicer.util.delayDisplay("Please place the landmarks and click Continue when done", 3000)
            
    def createStepWidgets(self):
        """Create all step widgets for the GUI"""
        # Step 1: Welcome and Introduction
        self.createStep1Widget()
        # Step 2: Landmark Selection
        self.createStep2Widget()
        # Step 3: Reference Plane Creation
        self.createStep3Widget()
        # Step 4: Mirror Plane Configuration
        self.createStep4Widget()
        # Step 5: Intersection Creation
        self.createStep5Widget()
        # Step 6: Bone Point Setup
        self.createStep6Widget()
        # Step 7: Bone Profile Results
        self.createStep7Widget()
        # Step 8: Soft Tissue Options
        self.createStep8Widget()
        # Step 9: Results Analysis
        self.createStep9Widget()    
        
    def createStep1Widget(self):
        """Create widget for Step 1: Welcome Screen"""
        step1Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step1Widget)
        
        # Add welcome title
        titleLabel = qt.QLabel("Welcome to the Prokopec-Ubelaker Nasal Prediction Tool!")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Add description
        instructionsLabel = qt.QLabel(
            "This tool will guide you through the steps of creating a nasal prediction.\n\n"
            "Click 'Next' to begin setting up your landmarks."
        )
        instructionsLabel.setWordWrap(True)
        layout.addWidget(instructionsLabel)
        
        # Add to step stack
        self.stepStack.addWidget(step1Widget)

    def createStep2Widget(self):
        """Create widget for Step 2: Input Selection"""
        step2Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step2Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 2: Hard Tissue Landmark Selection")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Please select or load the required 7 hard tissue landmarks:\n\n"
            "• nasion - intersection of nasofrontal sutures\n"
            "• inion - median point at base of external occipital protuberance\n"
            "• bregma - where sagittal and coronal sutures meet\n"
            "• prosthion - median point between central incisors\n"
            "• subspinale - deepest point below anterior nasal spine\n"
            "• rhinion - most rostral point on internasal suture\n"
            "• acanthion - most anterior tip of anterior nasal spine"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create landmark selector frame
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        
        # Create landmark selector
        self.landmarksSelector = slicer.qMRMLNodeComboBox()
        self.landmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.landmarksSelector.selectNodeUponCreation = True
        self.landmarksSelector.addEnabled = True
        self.landmarksSelector.removeEnabled = True
        self.landmarksSelector.noneEnabled = True
        self.landmarksSelector.setMRMLScene(slicer.mrmlScene)
        self.landmarksSelector.setToolTip("Select the landmarks node")
        selectorLayout.addRow("Hard Tissue Landmarks: ", self.landmarksSelector)
        
        layout.addWidget(selectorFrame)
        
        # Create load button (removed the Sample Data button)
        self.loadLandmarksButton = qt.QPushButton("Load From File")
        layout.addWidget(self.loadLandmarksButton)
        
        # Add status label
        self.landmarksStatusLabel = qt.QLabel("Please select or load landmarks")
        self.landmarksStatusLabel.setWordWrap(True)
        layout.addWidget(self.landmarksStatusLabel)
        
        # Connect button
        self.loadLandmarksButton.connect('clicked(bool)', self.onLoadLandmarksClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step2Widget)

    def createStep3Widget(self):
        """Create widget for Step 3: Reference Plane Creation"""
        step3Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step3Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 3: Reference Plane Creation")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Create the reference planes needed for the Prokopec-Ubelaker method:\n\n"
            "• INB plane: defined by inion, nasion, and bregma\n"
            "• NP plane: perpendicular to INB, through nasion and prosthion\n"
            "• PT plane: perpendicular to both INB and NP planes"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Add debug button for beginners
        self.checkLandmarksButton = qt.QPushButton("Check Landmarks")
        self.checkLandmarksButton.toolTip = "Check if all required landmarks are detected correctly"
        layout.addWidget(self.checkLandmarksButton)
        
        # Create button to create planes
        self.createReferencePlanesButton = qt.QPushButton("Create Reference Planes")
        layout.addWidget(self.createReferencePlanesButton)
        
        # Add status label
        self.planesStatusLabel = qt.QLabel("Ready to create reference planes")
        self.planesStatusLabel.setWordWrap(True)
        layout.addWidget(self.planesStatusLabel)
        
        # Connect buttons
        self.checkLandmarksButton.connect('clicked(bool)', self.onCheckLandmarksClicked)
        self.createReferencePlanesButton.connect('clicked(bool)', self.onCreateReferencePlanesClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step3Widget)

    def createStep4Widget(self):
        """Create widget for Step 4: Mirror Plane Configuration"""
        step4Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step4Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 4: Mirror Plane Configuration")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Set up the mirror planes for the nasal prediction:\n\n"
            "• Choose between 4, 5, or 6 mirror planes\n"
            "• The planes will be placed equidistant between rhinion and maximum nasal width\n"
            "• You need to select or create a Maximum Nasal Width measurement"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create selector for maximum width
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        
        self.mawSelector = slicer.qMRMLNodeComboBox()
        self.mawSelector.nodeTypes = ["vtkMRMLMarkupsLineNode"]  # LINE node, not fiducials
        self.mawSelector.selectNodeUponCreation = False
        self.mawSelector.addEnabled = True  # Allow creating a new line
        self.mawSelector.removeEnabled = False
        self.mawSelector.noneEnabled = True
        self.mawSelector.setMRMLScene(slicer.mrmlScene)
        selectorLayout.addRow("Maximum Aperture Width: ", self.mawSelector)
        
        # Add plane count selector
        self.planeCountSlider = qt.QSlider(qt.Qt.Horizontal)
        self.planeCountSlider.minimum = 4
        self.planeCountSlider.maximum = 6
        self.planeCountSlider.value = 5
        self.planeCountSlider.setTickPosition(qt.QSlider.TicksBelow)
        self.planeCountSlider.setTickInterval(1)
        self.planeCountSlider.setSingleStep(1)
        
        self.planeCountLabel = qt.QLabel(f"Number of mirror planes: {self.planeCountSlider.value}")
        
        selectorLayout.addRow("", self.planeCountLabel)
        selectorLayout.addRow("", self.planeCountSlider)
        
        layout.addWidget(selectorFrame)
        
        # Create button to create planes
        self.createMirrorPlanesButton = qt.QPushButton("Create Mirror Planes")
        layout.addWidget(self.createMirrorPlanesButton)
        
        # Add status label
        self.mirrorPlanesStatusLabel = qt.QLabel("Ready to create mirror planes")
        self.mirrorPlanesStatusLabel.setWordWrap(True)
        layout.addWidget(self.mirrorPlanesStatusLabel)
        
        # Connect buttons and sliders
        self.planeCountSlider.connect('valueChanged(int)', self.onPlaneCountChanged)
        self.createMirrorPlanesButton.connect('clicked(bool)', self.onCreateMirrorPlanesClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step4Widget)

    def createStep5Widget(self):
        """Create the widget for step 5"""
        step5Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step5Widget)
        # Title
        titleLabel = qt.QLabel("Step 5: Mirror Planes and Intersections")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Create intersection planes and locate important intersection points:"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Step instructions
        instructionsLabel = qt.QLabel("Step 5: Create intersection lines")
        instructionsLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(instructionsLabel)
        
        # Description
        descriptionLabel = qt.QLabel("Create lines where planes intersect.")
        descriptionLabel.setWordWrap(True)
        layout.addWidget(descriptionLabel)
        
        # First button - Intersection Lines
        self.createIntersectionLinesButton = qt.QPushButton("Create Intersection Lines")
        self.createIntersectionLinesButton.toolTip = "Create intersection lines between INB and mirror planes"
        self.createIntersectionLinesButton.connect('clicked(bool)', self.onCreateIntersectionLinesClicked)
        layout.addWidget(self.createIntersectionLinesButton)
        
        # Status label for intersection lines
        self.intersectionLinesStatusLabel = qt.QLabel("Ready to create intersection lines...")
        self.intersectionLinesStatusLabel.setStyleSheet("background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.intersectionLinesStatusLabel)
        
        # Add some space
        layout.addWidget(qt.QLabel(""))
        
        # Second button - Lines A and B
        self.createLinesABButton = qt.QPushButton("Create Lines A and B")
        self.createLinesABButton.toolTip = "Create reference lines A and B"
        self.createLinesABButton.connect('clicked(bool)', self.onCreateLinesABClicked)
        layout.addWidget(self.createLinesABButton)
        
        # Status label for lines A and B
        self.linesABStatusLabel = qt.QLabel("Ready to create lines A and B...")
        self.linesABStatusLabel.setStyleSheet("background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.linesABStatusLabel)
        
        # Add Line B intersection button (NEW!)
        self.lineBIntersectionButton = qt.QPushButton("Find intersection points between the intersection lines and Line B")
        self.lineBIntersectionButton.toolTip = "This will create points called mirrorB_A, etc"
        layout.addWidget(self.lineBIntersectionButton)
        
        # Add Line A intersection button (NEW!)
        self.lineAIntersectionButton = qt.QPushButton("Find intersection points between the intersection lines and Line A")
        self.lineAIntersectionButton.toolTip = "This will create points called mirrorA_A, etc"
        layout.addWidget(self.lineAIntersectionButton)
        
        # Add explanatory labels (NEW!)
        lineBLabel = qt.QLabel("This will create points called mirrorB_A, mirrorB_B, etc.")
        lineBLabel.setWordWrap(True)
        layout.addWidget(lineBLabel)
        
        lineALabel = qt.QLabel("This will create points called mirrorA_A, mirrorA_B, etc.")
        lineALabel.setWordWrap(True)
        layout.addWidget(lineALabel)
        
        # Status label
        self.intersectionsStatusLabel = qt.QLabel("Ready to create intersections")
        self.intersectionsStatusLabel.setWordWrap(True)
        layout.addWidget(self.intersectionsStatusLabel)
        
        # Connect the new buttons (NEW!)
        self.lineBIntersectionButton.connect('clicked(bool)', self.onFindLineBIntersectionClicked)
        self.lineAIntersectionButton.connect('clicked(bool)', self.onFindLineAIntersectionClicked)
        
         # Add to step stack
        self.stepStack.addWidget(step5Widget)

    def createStep6Widget(self):
        """Create widget for Step 6: Nasal Aperture Outline"""
        step6Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step6Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 6: Nasal Aperture Outline Outline Setup")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Download the nasal bone outline landmarks based on your chosen number of mirror planes:\n\n"
            "• The outline landmarks must be placed along the lateral view of the nasal aperture\n"
            "• Points will automatically be named to match the number of planes you selected\n"
            "• After downloading, you will need to adjust point positions to match your skull"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create download button 
        self.downloadOutlineButton = qt.QPushButton("Download the aperture outline landmarks")
        layout.addWidget(self.downloadOutlineButton)
        
        # Add status label
        self.bonePointsStatusLabel = qt.QLabel("Ready to download bone outline landmarks")
        self.bonePointsStatusLabel.setWordWrap(True)
        layout.addWidget(self.bonePointsStatusLabel)
        
        # Add confirmation message near the next button
        self.confirmationLabel = qt.QLabel("✓ Have you allocated the outline points as described from a lateral view?")
        self.confirmationLabel.setStyleSheet("color: orange; font-weight: bold;")
        self.confirmationLabel.setWordWrap(True)
        layout.addWidget(self.confirmationLabel)
        
        # Connect button
        self.downloadOutlineButton.connect('clicked(bool)', self.onDownloadOutlineClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step6Widget)

    def createStep7Widget(self):
        """Create widget for Step 7: Bone Profile Results"""
        step7Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step7Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 7: Bone Profile Results")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Create and view bone measurements before adding soft tissue:\n\n"
            "• Click 'Create Bone Measurements' to generate measurements\n"
            "• View the measurements in the table\n"
            "• Export the bone measurements if needed"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create buttons
        self.createBoneMeasurementsButton = qt.QPushButton("Create Bone Measurements")
        layout.addWidget(self.createBoneMeasurementsButton)
        
        # Add measurements table
        self.boneMeasurementsTable = qt.QTableWidget()
        self.boneMeasurementsTable.setColumnCount(2)
        self.boneMeasurementsTable.setHorizontalHeaderLabels(["Measurement", "Value (mm)"])
        self.boneMeasurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self.boneMeasurementsTable.horizontalHeader().setSectionResizeMode(1, qt.QHeaderView.ResizeToContents)
        self.boneMeasurementsTable.verticalHeader().setVisible(False)
        layout.addWidget(self.boneMeasurementsTable)
        
        # Export button
        self.exportBoneResultsButton = qt.QPushButton("Export Bone Measurements")
        self.exportBoneResultsButton.enabled = False  # Initially disabled
        layout.addWidget(self.exportBoneResultsButton)
        
        # Add status label
        self.boneMeasurementsStatusLabel = qt.QLabel("Ready to create bone measurements")
        self.boneMeasurementsStatusLabel.setWordWrap(True)
        layout.addWidget(self.boneMeasurementsStatusLabel)
        
        # Connect buttons
        self.createBoneMeasurementsButton.connect('clicked(bool)', self.onCreateBoneMeasurementsClicked)
        self.exportBoneResultsButton.connect('clicked(bool)', self.onExportBoneResultsClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step7Widget)

    def createStep8Widget(self):
        """Create widget for Step 8: Soft Tissue Options"""
        step8Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step8Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 8: Soft Tissue Options")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Choose how to add soft tissue to your prediction:"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create radio button group for soft tissue method
        methodFrame = qt.QFrame()
        methodLayout = qt.QVBoxLayout(methodFrame)
        
        self.softTissueMethodGroup = qt.QButtonGroup()
        
        # No soft tissue option
        self.noSoftTissueRadio = qt.QRadioButton("No soft tissue (continue with bone measurements only)")
        self.softTissueMethodGroup.addButton(self.noSoftTissueRadio, 0)
        methodLayout.addWidget(self.noSoftTissueRadio)
        
        # Standard method option
        self.standardMethodRadio = qt.QRadioButton("Standard Prokopec-Ubelaker (+2mm soft tissue)")
        self.standardMethodRadio.setChecked(True)  # Default option
        self.softTissueMethodGroup.addButton(self.standardMethodRadio, 1)
        methodLayout.addWidget(self.standardMethodRadio)
        
        # Custom method option
        self.customMethodRadio = qt.QRadioButton("Custom soft tissue thickness values")
        self.softTissueMethodGroup.addButton(self.customMethodRadio, 2)
        methodLayout.addWidget(self.customMethodRadio)
        
        layout.addWidget(methodFrame)
        
        # Custom thickness options (initially hidden)
        self.customThicknessFrame = qt.QFrame()
        customThicknessLayout = qt.QFormLayout(self.customThicknessFrame)
        
        self.topThicknessSpinBox = qt.QDoubleSpinBox()
        self.topThicknessSpinBox.setRange(1.0, 5.0)
        self.topThicknessSpinBox.setSingleStep(0.1)
        self.topThicknessSpinBox.setValue(1.2)
        self.topThicknessSpinBox.setSuffix("x")
        customThicknessLayout.addRow("Top third factor:", self.topThicknessSpinBox)
        
        self.middleThicknessSpinBox = qt.QDoubleSpinBox()
        self.middleThicknessSpinBox.setRange(1.0, 5.0)
        self.middleThicknessSpinBox.setSingleStep(0.1)
        self.middleThicknessSpinBox.setValue(1.3)
        self.middleThicknessSpinBox.setSuffix("x")
        customThicknessLayout.addRow("Middle third factor:", self.middleThicknessSpinBox)
        
        self.bottomThicknessSpinBox = qt.QDoubleSpinBox()
        self.bottomThicknessSpinBox.setRange(1.0, 5.0)
        self.bottomThicknessSpinBox.setSingleStep(0.1)
        self.bottomThicknessSpinBox.setValue(1.4)
        self.bottomThicknessSpinBox.setSuffix("x")
        customThicknessLayout.addRow("Bottom third factor:", self.bottomThicknessSpinBox)
        
        layout.addWidget(self.customThicknessFrame)
        self.customThicknessFrame.setVisible(False)  # Initially hidden
        
        # Create button to generate soft tissue
        self.generateSoftTissueButton = qt.QPushButton("Generate Soft Tissue Predictions")
        layout.addWidget(self.generateSoftTissueButton)
        
        # Add status label
        self.softTissueStatusLabel = qt.QLabel("Ready to generate soft tissue predictions")
        self.softTissueStatusLabel.setWordWrap(True)
        layout.addWidget(self.softTissueStatusLabel)
        
        # Connect buttons
        self.generateSoftTissueButton.connect('clicked(bool)', self.onGenerateSoftTissueClicked)
        self.customMethodRadio.connect('toggled(bool)', self.onCustomMethodToggled)
        
        # Add to step stack
        self.stepStack.addWidget(step8Widget)

    def createStep9Widget(self):
        """Create widget for Step 9: Results Analysis"""
        step9Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step9Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 9: Results Analysis")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Review the measurements and export the results:"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Add measurements table
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable.setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Predicted (mm)", "Actual (mm)"])
        self.measurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self.measurementsTable.horizontalHeader().setSectionResizeMode(1, qt.QHeaderView.ResizeToContents)
        self.measurementsTable.horizontalHeader().setSectionResizeMode(2, qt.QHeaderView.ResizeToContents)
        self.measurementsTable.verticalHeader().setVisible(False)
        layout.addWidget(self.measurementsTable)
        
        # Export buttons
        exportButtonFrame = qt.QFrame()
        exportButtonLayout = qt.QHBoxLayout(exportButtonFrame)
        
        self.copyToClipboardButton = qt.QPushButton("Copy to Clipboard")
        self.exportResultsButton = qt.QPushButton("Export Results to CSV")
        
        exportButtonLayout.addWidget(self.copyToClipboardButton)
        exportButtonLayout.addWidget(self.exportResultsButton)
        
        layout.addWidget(exportButtonFrame)
        
        # Add status label
        self.exportStatusLabel = qt.QLabel("Ready to export results")
        self.exportStatusLabel.setWordWrap(True)
        layout.addWidget(self.exportStatusLabel)
        
        # Add completion message
        completionLabel = qt.QLabel("🎉 Congratulations! You've completed the Prokopec-Ubelaker nasal prediction process!")
        completionLabel.setStyleSheet("font-weight: bold; color: green;")
        completionLabel.setWordWrap(True)
        layout.addWidget(completionLabel)
        
        # Connect buttons
        self.copyToClipboardButton.connect('clicked(bool)', self.onCopyToClipboardClicked)
        self.exportResultsButton.connect('clicked(bool)', self.onExportResultsClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step9Widget)

    def updateStepUI(self):
        """Update UI for current step"""
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep+1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)

   
    def onBackClicked(self):
        """Handle back button click"""
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()

    def onNextClicked(self):
        """Handle next button click"""
        print(f"Next button clicked! Current step: {self.currentStep}, Total steps: {self.stepStack.count}")
        if self.currentStep < self.stepStack.count - 1:
            print("Moving to next step")
            self.currentStep += 1
            self.updateStepUI()
        else:
            print("Already at last step")

    def onHelpClicked(self):
        """Show help information for the current step"""
        helpMessages = [
            {
                "title": "Step 1: Input Selection",
                "text": "In this step, you need to load or select your landmarks file.",
                "details": (
                    "Required landmarks are:\n"
                    "• nasion - intersection of nasofrontal sutures\n"
                    "• inion - median point at base of external occipital protuberance\n"
                    "• bregma - where sagittal and coronal sutures meet\n"
                    "• prosthion - median point between central incisors\n"
                    "• subspinale - deepest point below anterior nasal spine\n"
                    "• rhinion - most rostral point on internasal suture\n"
                    "• acanthion - most anterior tip of anterior nasal spine"
                )
            },
            {
                "title": "Step 2: Reference Plane Creation",
                "text": "Create the reference planes needed for the Prokopec-Ubelaker method.",
                "details": (
                    "This step creates three reference planes:\n"
                    "• INB plane: defined by inion, nasion, and bregma\n"
                    "• NP plane: perpendicular to INB, through nasion and prosthion\n"
                    "• PT plane: perpendicular to both INB and NP planes"
                )
            },
            {
                "title": "Step 3: Mirror Plane Configuration",
                "text": "Set up the mirror planes for the nasal prediction.",
                "details": (
                    "Choose between 4, 5, or 6 mirror planes:\n"
                    "• More planes can give higher accuracy but requires more landmarks\n"
                    "• The planes will be placed equidistant between rhinion and maximum nasal width\n"
                    "• You need to select or create a Maximum Nasal Width measurement"
                )
            },
            {
                "title": "Step 4: Intersection Creation",
                "text": "Create intersection lines between reference planes.",
                "details": (
                    "This step creates:\n"
                    "• Intersection lines between the INB plane and each mirror plane\n"
                    "• Reference Line A: through nasion and prosthion\n"
                    "• Reference Line B: parallel to Line A through rhinion\n"
                    "• Intersection points between Line B and all mirror planes"
                )
            },
            {
                "title": "Step 5: Bone Point Setup",
                "text": "Place the bone points needed for measurement.",
                "details": (
                    "This step automatically:\n"
                    "• Finds existing bone points in your scene\n"
                    "• Loads missing bone points from your repository if available\n"
                    "• Creates new bone points if needed\n\n"
                    "Click 'Auto-Setup Bone Points' to have the tool download the number of points you need with the correct names"
                )
            },
            {
                "title": "Step 6: Bone Profile Results",
                "text": "Create and view bone measurements before adding soft tissue.",
                "details": (
                    "This step creates measurements for the nasal bone only (pred_no_soft):\n"
                    "• Click 'Create Bone Measurements' to generate measurements\n"
                    "• View the measurements in the table\n"
                    "• Export the bone measurements if needed\n\n"
                    "After this step, you'll decide how to add soft tissue."
                )
            },
            {
                "title": "Step 7: Soft Tissue Options",
                "text": "Choose how to add soft tissue to your prediction.",
                "details": (
                    "Choose from three options:\n"
                    "• No soft tissue: continue with bone measurements only (pred_no_soft)\n"
                    "• Standard Prokopec-Ubelaker: adds 2mm to each predicted point (pred_PU_soft)\n"
                    "• Custom values: set your own thickness factors (but be warned - these aren't official facial soft tissue thickness measurements!)\n\n"
                    "Click 'Generate Soft Tissue Predictions' after making your choice."
                )
            },
            {
                "title": "Step 8: Optional - Compare with Real Soft Tissue",
                "text": "Compare predictions with actual soft tissue (OPTIONAL).",
                "details": (
                    "This step is completely OPTIONAL and only needed if you want to measure prediction error.\n\n"
                    "If you have a real soft tissue model:\n"
                    "• Select it in the dropdown\n"
                    "• Click 'Compare with Real Soft Tissue' to see the difference\n\n"
                    "If you don't have a soft tissue model, just click 'Skip This Step'."
                )
            },
            {
                "title": "Step 9: Results Analysis",
                "text": "Review the measurements and export the results.",
                "details": (
                    "The measurements table shows:\n"
                    "• noseprofiletoB# - distances from mirror points to soft tissue\n"
                    "• nasalbonetoB# - distances from mirror points to nasal bone\n"
                    "• Comparison between predicted and actual values (if available)\n\n"
                    "You can export these measurements to CSV or copy them to clipboard."
                )
            }
        ]
        
        # Show the help message for the current step
        if self.currentStep < len(helpMessages):
            helpMessage = helpMessages[self.currentStep]
            
            # Create a message box
            messageBox = qt.QMessageBox()
            messageBox.setIcon(qt.QMessageBox.Information)
            messageBox.setWindowTitle(helpMessage["title"])
            messageBox.setText(helpMessage["text"])
            messageBox.setInformativeText(helpMessage["details"])
            messageBox.setStandardButtons(qt.QMessageBox.Ok)
            
            # Show the message box
            messageBox.exec_()
        else:
            # Generic help message for steps without specific help
            messageBox = qt.QMessageBox()
            messageBox.setIcon(qt.QMessageBox.Information)
            messageBox.setWindowTitle("Help")
            messageBox.setText("Help information for this step is not available.")
            messageBox.setStandardButtons(qt.QMessageBox.Ok)
            messageBox.exec_()

    # Required helper methods for functionality
    def onLoadLandmarksClicked(self):
        """Handle loading landmarks from file"""
        fileName = qt.QFileDialog.getOpenFileName(None, "Load Landmarks", "", "Markup Files (*.mrk.json);;All Files (*.*)")
        if fileName:
            try:
                landmarksNode = slicer.util.loadMarkups(fileName)
                if landmarksNode:
                    self.landmarksSelector.setCurrentNode(landmarksNode)
                    self.landmarksStatusLabel.text = "Landmarks loaded successfully!"
                else:
                    self.landmarksStatusLabel.text = "Failed to load landmarks from file."
            except Exception as e:
                self.landmarksStatusLabel.text = f"Error loading landmarks: {str(e)}"

    def onSampleLandmarksClicked(self):
        """Handle loading sample landmarks"""
        try:
            # URL for the sample landmarks
            url = "https://github.com/user-attachments/files/21412636/skull_landmarks.mrk.json"
            
            # Update status
            self.landmarksStatusLabel.text = "Downloading sample landmarks..."
            slicer.app.processEvents()
            
            # Create a temporary file to download to
            with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Download and load the file
            urllib.request.urlretrieve(url, temp_path)
            landmarksNode = slicer.util.loadMarkups(temp_path)
            
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            
            # Update UI
            if landmarksNode:
                self.landmarksSelector.setCurrentNode(landmarksNode)
                self.landmarksStatusLabel.text = "Sample landmarks loaded successfully!"
            else:
                self.landmarksStatusLabel.text = "Failed to load sample landmarks."
                
        except Exception as e:
            self.landmarksStatusLabel.text = f"Error: {str(e)}"

    def onPlaneCountChanged(self, value):
        """Update the plane count label when slider changes"""
        self.planeCountLabel.text = f"Number of mirror planes: {value}"

    def onCustomMethodToggled(self, checked):
        """Handle toggling custom method radio button"""
        self.customThicknessFrame.setVisible(checked)

    # These methods need to be implemented based on your functionality
    # They can be simple placeholders for now
        def onCreateReferencePlanesClicked(self):
            """Create reference planes using the EXACT code provided by the user"""
            try:
                # Add this safety check
                if not hasattr(self, 'planesStatusLabel') or not isinstance(self.planesStatusLabel, qt.QLabel):
                    # Create the label if it doesn't exist or is the wrong type
                    self.planesStatusLabel = qt.QLabel("Ready to create reference planes")
                    if hasattr(self, 'stepContentWidgets') and len(self.stepContentWidgets) > 2:
                        # Try to add it to the right layout
                        layout = self.stepContentWidgets[2].layout()
                        if layout:
                            layout.addWidget(self.planesStatusLabel)
                
                # Now safely update the label
                self.planesStatusLabel.setText("Creating reference planes...")  # Use setText() instead of .text =
                slicer.app.processEvents()
                
                import numpy as np
                
                # === COPY OF YOUR EXACT CODE FOR INB PLANE ===
                # Get the points from the landmarks node (your "hard_tissue_PU")
                hardTissueNode = self.landmarksSelector.currentNode()
                if not hardTissueNode:
                    self.planesStatusLabel.text.text = "Error: Please select landmarks first!"
                    return
                    
                # Get the first three points EXACTLY as in your code
                point1 = np.array(hardTissueNode.GetNthControlPointPosition(0))
                point2 = np.array(hardTissueNode.GetNthControlPointPosition(1))
                point3 = np.array(hardTissueNode.GetNthControlPointPosition(2))

                # Calculate the normal of the plane defined by the three points - EXACTLY as in your code
                v1 = point2 - point1
                v2 = point3 - point1
                planeNormal = np.cross(v1, v2)
                planeNormal = planeNormal / np.linalg.norm(planeNormal)  # Normalize the normal vector

                # Create a new plane node - EXACTLY as in your code
                self.inbPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'INB')

                # Set the origin of the new plane to the first point - EXACTLY as in your code
                self.inbPlane.SetOrigin(point1)

                # Set the normal of the new plane - EXACTLY as in your code
                self.inbPlane.SetNormal(planeNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.inbPlane.SetSize(200.0, 200.0)
                self.inbPlane.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                self.inbPlane.GetDisplayNode().SetOpacity(0.3)
                self.inbPlane.GetDisplayNode().SetVisibility(True)
                self.inbPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.inbPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR NPP PLANE ===
                # Get the 'INB' plane node - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')

                # Get the coordinates of 'prosthion' and 'nasion' - EXACTLY as in your code
                # Assuming prosthion is point 0 and nasion is point 3 as in your code
                prosthion = np.array(hardTissueNode.GetNthControlPointPositionWorld(0))
                nasion = np.array(hardTissueNode.GetNthControlPointPositionWorld(3))

                # Calculate the normal of the 'INB' plane - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())

                # Calculate the vector between 'prosthion' and 'nasion' - EXACTLY as in your code
                vectorPN = nasion - prosthion

                # Calculate the normal of the new plane - EXACTLY as in your code
                newPlaneNormal = np.cross(inbNormal, vectorPN)
                newPlaneNormal /= np.linalg.norm(newPlaneNormal)  # Normalize the vector

                # Create a new plane node and name it 'NPP' - EXACTLY as in your code
                self.nppPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'NPP')

                # Set the origin of the new plane to 'prosthion' - EXACTLY as in your code
                self.nppPlane.SetOriginWorld(prosthion)

                # Set the normal of the new plane - EXACTLY as in your code
                self.nppPlane.SetNormalWorld(newPlaneNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.nppPlane.SetSize(200.0, 200.0)
                self.nppPlane.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green
                self.nppPlane.GetDisplayNode().SetOpacity(1)
                self.nppPlane.GetDisplayNode().SetVisibility(True)
                self.nppPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.nppPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR PTP PLANE ===
                # Get the 'INB' and 'NPP' plane nodes - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')
                nppPlaneNode = slicer.util.getNode('NPP')

                # Calculate the normals of the 'INB' and 'NPP' planes - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())
                nppNormal = np.array(nppPlaneNode.GetNormalWorld())

                # Calculate the normal of the new plane 'PTP' - EXACTLY as in your code
                ptpNormal = np.cross(inbNormal, nppNormal)
                ptpNormal /= np.linalg.norm(ptpNormal)  # Normalize the vector

                # Create a new plane node and name it 'PTP' - EXACTLY as in your code
                self.ptPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'PTP')

                # Set the origin of the new plane to the origin of 'INB' - EXACTLY as in your code
                self.ptPlane.SetOriginWorld(inbPlaneNode.GetOriginWorld())

                # Set the normal of the new plane - EXACTLY as in your code
                self.ptPlane.SetNormalWorld(ptpNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.ptPlane.SetSize(200.0, 200.0)
                self.ptPlane.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)  # Blue
                self.ptPlane.GetDisplayNode().SetOpacity(0.3)
                self.ptPlane.GetDisplayNode().SetVisibility(True)
                self.ptPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.ptPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # Update status
                self.planesStatusLabel.text.text = "✅ Created INB, NPP, and PTP planes successfully!"
                
            except Exception as e:
                self.planesStatusLabel.text.text = f"❌ Error: {str(e)}"
                import traceback
                traceback.print_exc()
        def onCreateMirrorPlanesClicked(self):
            """Create mirror planes following Prokopec-Ubelaker method"""
            try:
                # Update status
                self.mirrorPlanesStatusLabel.text = "Creating mirror planes..."
                slicer.app.processEvents()
                
                # Check prerequisites
                if not hasattr(self, 'inbPlane') or not self.inbPlane:
                    self.mirrorPlanesStatusLabel.text = "Error: Please create reference planes first!"
                    return
                    
                # Get landmarks
                landmarksNode = self.landmarksSelector.currentNode()
                if not landmarksNode:
                    self.mirrorPlanesStatusLabel.text = "Error: Please select landmarks first!"
                    return
                    
                # Get rhinion position
                rhinion_id = -1
                for i in range(landmarksNode.GetNumberOfControlPoints()):
                    label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                    if "rhinion" in label:
                        rhinion_id = i
                        break
                        
                if rhinion_id == -1:
                    self.mirrorPlanesStatusLabel.text = "Error: Rhinion landmark not found!"
                    return
                    
                rhinion_pos = [0, 0, 0]
                landmarksNode.GetNthControlPointPosition(rhinion_id, rhinion_pos)
                
                # Create or get MAW
                mawNode = self.mawSelector.currentNode()
                if not mawNode or mawNode.GetNumberOfControlPoints() < 2:
                    # Create a default MAW
                    pt_normal = [0, 0, 0]
                    self.ptPlane.GetNormal(pt_normal)
                    
                    mawNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "maximum_nasal_width_MAW")
                    
                    left_point = [
                        rhinion_pos[0] + pt_normal[0] * 30.0,
                        rhinion_pos[1] + pt_normal[1] * 30.0,
                        rhinion_pos[2] + pt_normal[2] * 30.0
                    ]
                    
                    right_point = [
                        rhinion_pos[0] - pt_normal[0] * 30.0,
                        rhinion_pos[1] - pt_normal[1] * 30.0,
                        rhinion_pos[2] - pt_normal[2] * 30.0
                    ]
                    
                    # IMPORTANT: Clear any existing points first
                    while mawNode.GetNumberOfControlPoints() > 0:
                        mawNode.RemoveNthControlPoint(0)
                        
                    # Now add our points
                    mawNode.AddControlPoint(vtk.vtkVector3d(left_point))
                    mawNode.AddControlPoint(vtk.vtkVector3d(right_point))
                    
                    self.mawSelector.setCurrentNode(mawNode)
                
                # Get MAW points
                left_point = [0, 0, 0]
                right_point = [0, 0, 0]
                mawNode.GetNthControlPointPosition(0, left_point)
                mawNode.GetNthControlPointPosition(1, right_point)
                
                maw_midpoint = [
                    (left_point[0] + right_point[0]) / 2.0,
                    (left_point[1] + right_point[1]) / 2.0,
                    (left_point[2] + right_point[2]) / 2.0
                ]
                
                # Setup for planes
                num_planes = self.planeCountSlider.value
                
                # Remove old planes
                for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsPlaneNode"):
                    if node.GetName().startswith("Plane_"):
                        slicer.mrmlScene.RemoveNode(node)
                
                self.mirrorPlanes = []
                
                # Get normal for planes
                inb_normal = [0, 0, 0]
                self.inbPlane.GetNormal(inb_normal)
                
                # Calculate distance vector from rhinion to MAW
                rhinion_to_maw = [
                    maw_midpoint[0] - rhinion_pos[0],
                    maw_midpoint[1] - rhinion_pos[1],
                    maw_midpoint[2] - rhinion_pos[2]
                ]
                
                # Calculate the distance
                distance = math.sqrt(
                    rhinion_to_maw[0]**2 + 
                    rhinion_to_maw[1]**2 + 
                    rhinion_to_maw[2]**2
                )
                
                # Normalize the direction vector
                direction = [
                    rhinion_to_maw[0] / distance,
                    rhinion_to_maw[1] / distance,
                    rhinion_to_maw[2] / distance
                ]
                
                # First create Plane_A at MAW position - USING YOUR APPROACH
                planeA = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "Plane_A")
                planeA.SetPlaneType(slicer.vtkMRMLMarkupsPlaneNode.PlaneTypePointNormal)
                # Use SetOrigin directly instead of adding control points
                planeA.SetOrigin(maw_midpoint)
                planeA.SetNormal(inb_normal)
                planeA.SetSize(150.0, 150.0)
                planeA.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                planeA.GetDisplayNode().SetOpacity(0.7)
                self.mirrorPlanes.append(planeA)
                
                # Use letters for naming (B, C, D, etc.)
                plane_names = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                plane_colors = [
                    (0.0, 1.0, 0.0),    # Green
                    (0.0, 0.0, 1.0),    # Blue
                    (1.0, 1.0, 0.0),    # Yellow
                    (1.0, 0.0, 1.0),    # Magenta
                    (0.0, 1.0, 1.0),    # Cyan
                    (1.0, 0.5, 0.0),    # Orange
                    (0.5, 0.0, 1.0),    # Purple
                    (0.0, 0.5, 0.5),    # Teal
                    (0.5, 0.5, 0.0)     # Olive
                ]
                
                # Create evenly spaced planes (B, C, D, etc.)
                for i in range(num_planes - 1):  # -1 because we already created Plane_A
                    fraction = (i + 1) / (num_planes)
                    
                    # Calculate position
                    plane_pos = [
                        rhinion_pos[0] + fraction * distance * direction[0],
                        rhinion_pos[1] + fraction * distance * direction[1],
                        rhinion_pos[2] + fraction * distance * direction[2]
                    ]
                    
                    # Create plane with proper name - USING YOUR APPROACH
                    plane_name = f"Plane_{plane_names[i]}"
                    plane = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", plane_name)
                    plane.SetPlaneType(slicer.vtkMRMLMarkupsPlaneNode.PlaneTypePointNormal)
                    # Use SetOrigin directly instead of adding control points
                    plane.SetOrigin(plane_pos)
                    plane.SetNormal(inb_normal)
                    plane.SetSize(150.0, 150.0)
                    
                    # Use predefined colors
                    if i < len(plane_colors):
                        plane.GetDisplayNode().SetSelectedColor(*plane_colors[i])
                    else:
                        plane.GetDisplayNode().SetSelectedColor(0.8, 0.8, 0.8)
                        
                    plane.GetDisplayNode().SetOpacity(0.7)
                    
                    self.mirrorPlanes.append(plane)
                
                # Show MAW measurement
                maw_distance = self.getMawDistance(mawNode)
                mawNode.SetName(f"maximum_nasal_width_MAW: {maw_distance:.2f}mm")
                
                self.mirrorPlanesStatusLabel.text = f"✅ Created {num_planes} planes (A-{plane_names[num_planes-2]}) successfully!"
                
            except Exception as e:
                self.mirrorPlanesStatusLabel.text = f"❌ Error: {str(e)}"
                import traceback
                traceback.print_exc()
    
            
            
    def onCreateIntersectionsClicked(self):
        """Create intersections following the Prokopec-Ubelaker method"""
        try:
            # Update status
            self.intersectionsStatusLabel.text = "Creating intersections..."
            slicer.app.processEvents()
            
            # Check if we have planes
            if not hasattr(self, 'inbPlane') or not self.inbPlane:
                self.intersectionsStatusLabel.text = "Error: Please create reference planes first!"
                return
                
            if not hasattr(self, 'mirrorPlanes') or not self.mirrorPlanes:
                self.intersectionsStatusLabel.text = "Error: Please create mirror planes first!"
                return
                
            # Get landmarks
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.intersectionsStatusLabel.text = "Error: Please select landmarks first!"
                return
                
            # Find required landmarks
            nasion_id = -1
            prosthion_id = -1
            rhinion_id = -1
            
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                if "nasion" in label:
                    nasion_id = i
                elif "prosthion" in label:
                    prosthion_id = i
                elif "rhinion" in label:
                    rhinion_id = i
                    
            if nasion_id == -1 or prosthion_id == -1 or rhinion_id == -1:
                self.intersectionsStatusLabel.text = "Error: Missing landmarks (nasion, prosthion, or rhinion)!"
                return
                
            # Get landmark positions
            nasion_pos = [0, 0, 0]
            prosthion_pos = [0, 0, 0]
            rhinion_pos = [0, 0, 0]
            
            landmarksNode.GetNthControlPointPosition(nasion_id, nasion_pos)
            landmarksNode.GetNthControlPointPosition(prosthion_id, prosthion_pos)
            landmarksNode.GetNthControlPointPosition(rhinion_id, rhinion_pos)
            
            # Clear existing intersection objects
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsCurveNode"):
                if node.GetName().startswith("Intersection_"):
                    slicer.mrmlScene.RemoveNode(node)
                    
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsLineNode"):
                if node.GetName().startswith("Line_A_") or node.GetName().startswith("Line_B_"):
                    slicer.mrmlScene.RemoveNode(node)
                    
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsFiducialNode"):
                if node.GetName() == "B_Intersection_Points":
                    slicer.mrmlScene.RemoveNode(node)
            
            # Create Line A (nasion to prosthion)
            lineA = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "Line_A_NasionProsthion")
            lineA.AddControlPoint(vtk.vtkVector3d(nasion_pos))
            lineA.AddControlPoint(vtk.vtkVector3d(prosthion_pos))
            lineA.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)  # Yellow
            lineA.GetDisplayNode().SetLineThickness(3.0)  # Make line thicker
            
            # Calculate Line A direction
            lineA_dir = [
                prosthion_pos[0] - nasion_pos[0],
                prosthion_pos[1] - nasion_pos[1],
                prosthion_pos[2] - nasion_pos[2]
            ]
            vtk.vtkMath.Normalize(lineA_dir)
            
            # Create Line B (through rhinion, parallel to Line A)
            # Extend it 100mm in each direction
            lineB_start = [
                rhinion_pos[0] - lineA_dir[0] * 100.0,
                rhinion_pos[1] - lineA_dir[1] * 100.0, 
                rhinion_pos[2] - lineA_dir[2] * 100.0
            ]
            
            lineB_end = [
                rhinion_pos[0] + lineA_dir[0] * 100.0,
                rhinion_pos[1] + lineA_dir[1] * 100.0,
                rhinion_pos[2] + lineA_dir[2] * 100.0
            ]
            
            lineB = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "Line_B_ThroughRhinion")
            lineB.AddControlPoint(vtk.vtkVector3d(lineB_start))
            lineB.AddControlPoint(vtk.vtkVector3d(lineB_end))
            lineB.GetDisplayNode().SetSelectedColor(0.0, 1.0, 1.0)  # Cyan
            lineB.GetDisplayNode().SetLineThickness(3.0)  # Make line thicker
            
            # Store lines for later use
            self.lineA = lineA
            self.lineB = lineB
            
            # Create intersection lines between INB and each mirror plane
            self.intersection_lines = []
            
            # Create node for B intersection points
            b_points = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "B_Intersection_Points")
            
            # Store intersection points
            self.intersection_points = []
            
            # For each mirror plane:
            for i, mirror_plane in enumerate(self.mirrorPlanes):
                # Create intersection with INB plane
                # First get plane positions and normals
                inb_origin = [0, 0, 0]
                inb_normal = [0, 0, 0]
                self.inbPlane.GetOrigin(inb_origin)
                self.inbPlane.GetNormal(inb_normal)
                
                mirror_origin = [0, 0, 0]
                mirror_normal = [0, 0, 0]
                mirror_plane.GetOrigin(mirror_origin)
                mirror_plane.GetNormal(mirror_normal)
                
                # Calculate the direction of the intersection line
                # It's the cross product of the two plane normals
                line_dir = [0, 0, 0]
                vtk.vtkMath.Cross(inb_normal, mirror_normal, line_dir)
                vtk.vtkMath.Normalize(line_dir)
                
                # Find a point on the intersection line
                # This requires solving a system of equations
                # For simplicity, we project a point onto both planes
                
                # Start with the mirror origin
                point_on_line = [
                    mirror_origin[0],
                    mirror_origin[1],
                    mirror_origin[2]
                ]
                
                # Project onto INB plane
                distance = vtk.vtkPlane.DistanceToPlane(
                    point_on_line,
                    inb_normal,
                    inb_origin
                )
                
                point_on_line = [
                    point_on_line[0] - distance * inb_normal[0],
                    point_on_line[1] - distance * inb_normal[1],
                    point_on_line[2] - distance * inb_normal[2]
                ]
                
                # Create the intersection line
                intersection_line = slicer.mrmlScene.AddNewNodeByClass(
                    "vtkMRMLMarkupsLineNode",
                    f"Intersection_INB_Mirror{i+1}"
                )
                
                # Add points to create a 100mm line in each direction
                start_point = [
                    point_on_line[0] - line_dir[0] * 100.0,
                    point_on_line[1] - line_dir[1] * 100.0,
                    point_on_line[2] - line_dir[2] * 100.0
                ]
                
                end_point = [
                    point_on_line[0] + line_dir[0] * 100.0,
                    point_on_line[1] + line_dir[1] * 100.0,
                    point_on_line[2] + line_dir[2] * 100.0
                ]
                
                intersection_line.AddControlPoint(vtk.vtkVector3d(start_point))
                intersection_line.AddControlPoint(vtk.vtkVector3d(end_point))
                
                # Set color to match mirror plane
                color = [0, 0, 0]
                mirror_plane.GetDisplayNode().GetSelectedColor(color)
                intersection_line.GetDisplayNode().SetSelectedColor(color[0], color[1], color[2])
                intersection_line.GetDisplayNode().SetLineThickness(2.0)
                
                # Store line
                self.intersection_lines.append(intersection_line)
                
                # Now find intersection of Line B with this intersection line
                # This is the closest point between two 3D lines
                
                # Line B parameters
                lineB_p1 = lineB_start
                lineB_p2 = lineB_end
                
                # Intersection line parameters
                int_p1 = start_point
                int_p2 = end_point
                
                # Find closest point
                closest_point = self.findClosestPointBetweenLines(lineB_p1, lineB_p2, int_p1, int_p2)
                
                # Add point to collection
                b_points.AddControlPoint(vtk.vtkVector3d(closest_point), f"B{i+1}")
                
                # Store for later use
                self.intersection_points.append(closest_point)
                
            # Update status
            self.intersectionsStatusLabel.text = f"✅ Created all intersections for {len(self.mirrorPlanes)} planes!"
            
        except Exception as e:
            self.intersectionsStatusLabel.text = f"❌ Error: {str(e)}"
            import traceback
            traceback.print_exc()
        
    def findClosestPointBetweenLines(self, line1_p1, line1_p2, line2_p1, line2_p2):
        """Find the closest point between two lines in 3D space"""
        # Direction vectors for both lines
        line1_dir = [
            line1_p2[0] - line1_p1[0],
            line1_p2[1] - line1_p1[1],
            line1_p2[2] - line1_p1[2]
        ]
        
        line2_dir = [
            line2_p2[0] - line2_p1[0],
            line2_p2[1] - line2_p1[1],
            line2_p2[2] - line2_p1[2]
        ]
        
        # Normalize direction vectors
        vtk.vtkMath.Normalize(line1_dir)
        vtk.vtkMath.Normalize(line2_dir)
        
        # Vector connecting the starting points of each line
        r = [
            line1_p1[0] - line2_p1[0],
            line1_p1[1] - line2_p1[1],
            line1_p1[2] - line2_p1[2]
        ]
        
        # Calculate dot products for the system of equations
        a = vtk.vtkMath.Dot(line1_dir, line1_dir)  # Should be 1.0 if normalized
        b = vtk.vtkMath.Dot(line1_dir, line2_dir)
        c = vtk.vtkMath.Dot(line2_dir, line2_dir)  # Should be 1.0 if normalized
        d = vtk.vtkMath.Dot(line1_dir, r)
        e = vtk.vtkMath.Dot(line2_dir, r)
        
        # Calculate parameters for closest points
        denom = a*c - b*b
        
        if abs(denom) < 1e-8:
            # Lines are parallel, just use the midpoint of line1
            return [
                (line1_p1[0] + line1_p2[0]) / 2,
                (line1_p1[1] + line1_p2[1]) / 2,
                (line1_p1[2] + line1_p2[2]) / 2
            ]
        
        t = (b*e - c*d) / denom
        s = (a*e - b*d) / denom
        
        # Calculate closest point on line 1
        closest_point = [
            line1_p1[0] + t * line1_dir[0],
            line1_p1[1] + t * line1_dir[1],
            line1_p1[2] + t * line1_dir[2]
        ]
        
        return closest_point
        
    def onFindLineBIntersectionClicked(self):
        """Find intersection points between intersection lines and Line B"""
        try:
            # Update status
            self.intersectionsStatusLabel.text = "Finding Line B intersections..."
            slicer.app.processEvents()
            
            # Get number of planes
            planeCount = self.planeCountSlider.value
            
            # Check for Line_B
            try:
                lineNode = slicer.util.getNode('Line_B')
            except:
                self.intersectionsStatusLabel.text = "Error: Line_B not found! Please create it first."
                return
            
            # Remove any existing intersection points
            for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
                if node.GetName().startswith('mirrorB_'):
                    slicer.mrmlScene.RemoveNode(node)
            
            # Execute appropriate code based on plane count
            if planeCount == 4:
                # Code for 4 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                    
                # Store intersections for later use
                self.intersection_points = []
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to yellow (RGB: 255, 255, 0)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(1.0, 1.0, 0.0)
                            
                            # Store for later use
                            self.intersection_points.append(intersection_point)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                
            elif planeCount == 5:
                # Code for 5 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                # Store intersections for later use
                self.intersection_points = []
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to yellow (RGB: 255, 255, 0)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(1.0, 1.0, 0.0)
                            
                            # Store for later use
                            self.intersection_points.append(intersection_point)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                
            elif planeCount == 6:
                # Code for 6 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                # Store intersections for later use
                self.intersection_points = []
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to yellow (RGB: 255, 255, 0)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(1.0, 1.0, 0.0)
                            
                            # Store for later use
                            self.intersection_points.append(intersection_point)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
            
            # Update status
            self.intersectionsStatusLabel.text = f"✅ Created {len(self.intersection_points)} Line B intersection points!"
            
        except Exception as e:
            self.intersectionsStatusLabel.text = f"❌ Error finding Line B intersections: {str(e)}"
            import traceback
            traceback.print_exc()
            
    def onFindLineAIntersectionClicked(self):
        """Find intersection points between intersection lines and Line A"""
        try:
            # Update status
            self.intersectionsStatusLabel.text = "Finding Line A intersections..."
            slicer.app.processEvents()
            
            # Get number of planes
            planeCount = self.planeCountSlider.value
            
            # Check for Line_A
            try:
                lineNode = slicer.util.getNode('Line_A')
            except:
                self.intersectionsStatusLabel.text = "Error: Line_A not found! Please create it first."
                return
            
            # Remove any existing intersection points
            for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
                if node.GetName().startswith('mirrorA_'):
                    slicer.mrmlScene.RemoveNode(node)
                    
            # Execute appropriate code based on plane count
            if planeCount == 4:
                # Code for 4 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to turquoise (RGB: 64, 224, 208)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(64/255, 224/255, 208/255)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                        
            elif planeCount == 5:
                # Code for 5 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E']
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1 = np.array(line1Node.GetLineStartPositionWorld())
                    d1 = np.array(line1Node.GetLineEndPositionWorld()) - p1
                    p2 = np.array(line2Node.GetLineStartPositionWorld())
                    d2 = np.array(line2Node.GetLineEndPositionWorld()) - p2
                
                    # Normalize directions
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        print("Lines are parallel")
                        return None  # Lines are parallel
                
                    t = np.dot(np.cross((p2 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to turquoise (RGB: 64, 224, 208)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(64/255, 224/255, 208/255)
                        else:
                            print(f"No intersection found for {line_name}")
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                        
            elif planeCount == 6:
                # Code for 6 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None  # Avoid division by zero
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None  # Lines are parallel
                
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to turquoise (RGB: 64, 224, 208)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(64/255, 224/255, 208/255)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
            
            # Update status
            count = 0
            for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
                if node.GetName().startswith('mirrorA_'):
                    count += 1
            self.intersectionsStatusLabel.text = f"✅ Created {count} Line A intersection points!"
            
        except Exception as e:
            self.intersectionsStatusLabel.text = f"❌ Error finding Line A intersections: {str(e)}"
            import traceback
            traceback.print_exc()
            
    def onDownloadOutlineClicked(self):
        """Download bone outline landmarks based on selected number of planes"""
        try:
            # Update status
            self.bonePointsStatusLabel.text = "Downloading bone outline landmarks..."
            slicer.app.processEvents()
            
            # Get number of planes from slider
            planeCount = self.planeCountSlider.value
            
            # Choose the correct URL based on number of planes
            if planeCount == 4:
                url = "https://github.com/user-attachments/files/19318005/nasal.bone.outline.4.mrk.json"
                filename = "nasal_bone_outline_4.mrk.json"
            elif planeCount == 5:
                url = "https://github.com/user-attachments/files/19318009/nasal.bone.outline.5.mrk.json" 
                filename = "nasal_bone_outline_5.mrk.json"
            elif planeCount == 6:
                url = "https://github.com/user-attachments/files/19318010/nasal.bone.outline.6.mrk.json"
                filename = "nasal_bone_outline_6.mrk.json"
            else:
                self.bonePointsStatusLabel.text = f"Error: No outline file available for {planeCount} planes"
                return
                
            # Create a temporary file to download to
            with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                temp_path = temp_file.name
                
            # Download the file
            urllib.request.urlretrieve(url, temp_path)
            
            # Remove any existing outline points with the same name
            try:
                existingNode = slicer.util.getNode("nasal_bone_outline")
                if existingNode:
                    slicer.mrmlScene.RemoveNode(existingNode)
            except:
                pass
                
            # Load the downloaded file
            outlineNode = slicer.util.loadMarkups(temp_path)
            
            # Rename for clarity
            if outlineNode:
                outlineNode.SetName("nasal_bone_outline")
                self.bonePointsStatusLabel.text = f"✅ Outline landmarks for {planeCount} planes loaded successfully!"
                
                # Simply select the node and switch to Markups module
                slicer.modules.markups.logic().SetActiveListID(outlineNode)
                slicer.util.selectModule('Markups')
                
                # Tell the user what to do next
                slicer.util.delayDisplay(
                    f"Please adjust the {planeCount} outline landmarks if needed\n"
                    "Make sure to view from the lateral perspective", 
                    3000
                )
            else:
                self.bonePointsStatusLabel.text = "❌ Failed to load outline landmarks"
                
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
        except Exception as e:
            self.bonePointsStatusLabel.text = f"❌ Error downloading landmarks: {str(e)}"
            import traceback
            traceback.print_exc()
        
    def onCreateBoneMeasurementsClicked(self):
        """Create bone measurements"""
        self.boneMeasurementsStatusLabel.text = "Creating bone measurements... (not implemented yet)"
        # Enable export button after measurements are created
        self.exportBoneResultsButton.enabled = True
        
    def onExportBoneResultsClicked(self):
        """Export bone results"""
        self.boneMeasurementsStatusLabel.text = "Exporting bone measurements... (not implemented yet)"
        
    def onGenerateSoftTissueClicked(self):
        """Generate soft tissue predictions"""
        self.softTissueStatusLabel.text = "Generating soft tissue predictions... (not implemented yet)"
        
    def onCopyToClipboardClicked(self):
        """Copy results to clipboard"""
        self.exportStatusLabel.text = "Copying to clipboard... (not implemented yet)"
        
    def onExportResultsClicked(self):
        """Export results to CSV"""
        self.exportStatusLabel.text = "Exporting results... (not implemented yet)"
        
        
    def onCheckLandmarksClicked(self):
        """Check if all required landmarks are detected correctly"""
        try:
            # Get selected landmarks node
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.planesStatusLabel.text = "Error: Please select landmarks first!"
                return
            
            # List all landmarks in the node
            all_labels = []
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i)
                all_labels.append(f"{i}: {label}")
            
            # Check for the required landmarks
            required_landmarks = ["nasion", "inion", "bregma", "prosthion", "subspinale", "rhinion", "acanthion"]
            found_landmarks = {}
            
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                
                # Try exact match first
                if label in [l.lower() for l in required_landmarks]:
                    for req in required_landmarks:
                        if label == req.lower():
                            found_landmarks[req] = i
                            break
                # Then try partial match
                else:
                    for req in required_landmarks:
                        if req.lower() in label or label in req.lower():
                            found_landmarks[req] = i
                            break
            
            # Generate summary
            found_msg = [f"{req}: {'✓ Found' if req in found_landmarks else '❌ Missing'}" for req in required_landmarks]
            
            # Display results in a dialog
            message = qt.QMessageBox()
            message.setWindowTitle("Landmark Check Results")
            message.setText("Required landmark status:")
            message.setInformativeText("\n".join(found_msg))
            message.setDetailedText("All landmarks in the node:\n" + "\n".join(all_labels))
            message.setStandardButtons(qt.QMessageBox.Ok)
            message.exec_()
            
        except Exception as e:
            self.planesStatusLabel.text = f"Error checking landmarks: {str(e)}"

    def onCreateReferencePlanesClicked(self):
            """Create reference planes using the EXACT code provided by the user"""
            try:
                # Add this safety check
                if not hasattr(self, 'planesStatusLabel') or not isinstance(self.planesStatusLabel, qt.QLabel):
                    # Create the label if it doesn't exist or is the wrong type
                    self.planesStatusLabel = qt.QLabel("Ready to create reference planes")
                    if hasattr(self, 'stepContentWidgets') and len(self.stepContentWidgets) > 2:
                        # Try to add it to the right layout
                        layout = self.stepContentWidgets[2].layout()
                        if layout:
                            layout.addWidget(self.planesStatusLabel)
                
                # Now safely update the label
                self.planesStatusLabel.setText("Creating reference planes...")  # Use setText() instead of .text =
                slicer.app.processEvents()
                
                import numpy as np
                
                # === COPY OF YOUR EXACT CODE FOR INB PLANE ===
                # Get the points from the landmarks node (your "hard_tissue_PU")
                hardTissueNode = self.landmarksSelector.currentNode()
                if not hardTissueNode:
                    self.planesStatusLabel.text.text = "Error: Please select landmarks first!"
                    return
                    
                # Get the first three points EXACTLY as in your code
                point1 = np.array(hardTissueNode.GetNthControlPointPosition(0))
                point2 = np.array(hardTissueNode.GetNthControlPointPosition(1))
                point3 = np.array(hardTissueNode.GetNthControlPointPosition(2))

                # Calculate the normal of the plane defined by the three points - EXACTLY as in your code
                v1 = point2 - point1
                v2 = point3 - point1
                planeNormal = np.cross(v1, v2)
                planeNormal = planeNormal / np.linalg.norm(planeNormal)  # Normalize the normal vector

                # Create a new plane node - EXACTLY as in your code
                self.inbPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'INB')

                # Set the origin of the new plane to the first point - EXACTLY as in your code
                self.inbPlane.SetOrigin(point1)

                # Set the normal of the new plane - EXACTLY as in your code
                self.inbPlane.SetNormal(planeNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.inbPlane.SetSize(200.0, 200.0)
                self.inbPlane.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                self.inbPlane.GetDisplayNode().SetOpacity(0.3)
                self.inbPlane.GetDisplayNode().SetVisibility(True)
                self.inbPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.inbPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR NPP PLANE ===
                # Get the 'INB' plane node - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')

                # Get the coordinates of 'prosthion' and 'nasion' - EXACTLY as in your code
                # Assuming prosthion is point 0 and nasion is point 3 as in your code
                prosthion = np.array(hardTissueNode.GetNthControlPointPositionWorld(0))
                nasion = np.array(hardTissueNode.GetNthControlPointPositionWorld(3))

                # Calculate the normal of the 'INB' plane - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())

                # Calculate the vector between 'prosthion' and 'nasion' - EXACTLY as in your code
                vectorPN = nasion - prosthion

                # Calculate the normal of the new plane - EXACTLY as in your code
                newPlaneNormal = np.cross(inbNormal, vectorPN)
                newPlaneNormal /= np.linalg.norm(newPlaneNormal)  # Normalize the vector

                # Create a new plane node and name it 'NPP' - EXACTLY as in your code
                self.nppPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'NPP')

                # Set the origin of the new plane to 'prosthion' - EXACTLY as in your code
                self.nppPlane.SetOriginWorld(prosthion)

                # Set the normal of the new plane - EXACTLY as in your code
                self.nppPlane.SetNormalWorld(newPlaneNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.nppPlane.SetSize(200.0, 200.0)
                self.nppPlane.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green
                self.nppPlane.GetDisplayNode().SetOpacity(1)
                self.nppPlane.GetDisplayNode().SetVisibility(True)
                self.nppPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.nppPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR PTP PLANE ===
                # Get the 'INB' and 'NPP' plane nodes - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')
                nppPlaneNode = slicer.util.getNode('NPP')

                # Calculate the normals of the 'INB' and 'NPP' planes - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())
                nppNormal = np.array(nppPlaneNode.GetNormalWorld())

                # Calculate the normal of the new plane 'PTP' - EXACTLY as in your code
                ptpNormal = np.cross(inbNormal, nppNormal)
                ptpNormal /= np.linalg.norm(ptpNormal)  # Normalize the vector

                # Create a new plane node and name it 'PTP' - EXACTLY as in your code
                self.ptPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'PTP')

                # Set the origin of the new plane to the origin of 'INB' - EXACTLY as in your code
                self.ptPlane.SetOriginWorld(inbPlaneNode.GetOriginWorld())

                # Set the normal of the new plane - EXACTLY as in your code
                self.ptPlane.SetNormalWorld(ptpNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.ptPlane.SetSize(200.0, 200.0)
                self.ptPlane.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)  # Blue
                self.ptPlane.GetDisplayNode().SetOpacity(0.3)
                self.ptPlane.GetDisplayNode().SetVisibility(True)
                self.ptPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.ptPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # Update status
                self.planesStatusLabel.text.text = "✅ Created INB, NPP, and PTP planes successfully!"
                
            except Exception as e:
                self.planesStatusLabel.text.text = f"❌ Error: {str(e)}"
                import traceback
                traceback.print_exc()

    def onCreateMirrorPlanesClicked(self):
        """Create mirror planes using YOUR exact method"""
        try:
            # Update status
            self.mirrorPlanesStatusLabel.text = "Creating mirror planes..."
            slicer.app.processEvents()
            
            import numpy as np
            
            # Check if we have reference planes
            if not hasattr(self, 'ptPlane') or not self.ptPlane:
                self.mirrorPlanesStatusLabel.text = "Error: Please create reference planes first!"
                return
                
            # === USING YOUR EXACT METHOD ===
            
            # Get the PTP plane node (exactly as in your code)
            ptpPlaneNode = self.ptPlane
            
            # Get the MAW node (exactly as in your code)
            mawNode = self.mawSelector.currentNode()
            if not mawNode:
                self.mirrorPlanesStatusLabel.text = "Error: Please select MAW line first!"
                return
            
            # Get MAW position - using midpoint of MAW line
            left_point = np.array(mawNode.GetNthControlPointPositionWorld(0))
            right_point = np.array(mawNode.GetNthControlPointPositionWorld(1))
            mawPosition = (left_point + right_point) / 2
            
            # Get the PTP plane position and normal (exactly as in your code)
            ptpPlanePosition = np.array(ptpPlaneNode.GetOrigin())
            ptpPlaneNormal = np.array(ptpPlaneNode.GetNormal())
            
            # Get landmarks node
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.mirrorPlanesStatusLabel.text = "Error: Please select landmarks first!"
                return
                
            # Get rhinion position (exactly as in your code)
            rhinion_id = -1
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                if "rhinion" in label:
                    rhinion_id = i
                    break
                    
            if rhinion_id == -1:
                self.mirrorPlanesStatusLabel.text = "Error: Rhinion landmark not found!"
                return
                
            rhinionPosition = np.array(landmarksNode.GetNthControlPointPositionWorld(rhinion_id))
            
            # Remove old planes
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsPlaneNode"):
                if node.GetName().startswith("Plane_"):
                    slicer.mrmlScene.RemoveNode(node)
            
            # Create the new plane "A" at the MAW level (exactly as in your code)
            planeA = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'Plane_A')
            planeA.SetOrigin(mawPosition)
            planeA.SetNormal(ptpPlaneNormal)
            planeA.SetSize(150.0, 150.0)
            planeA.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
            planeA.GetDisplayNode().SetOpacity(0.7)
            
            # Store planes for later use
            self.mirrorPlanes = [planeA]
            
            # Calculate the distance between Plane_A and the rhinion (exactly as in your code)
            distance = np.dot(mawPosition - rhinionPosition, ptpPlaneNormal)
            
            # Get the number of mirror planes from the slider (minus 1 because we already created A)
            numPlanes = self.planeCountSlider.value - 1
            
            # Generate plane names based on number of planes (exactly as in your code)
            planeNames = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'][:numPlanes]
            
            # Calculate the positions for the new planes (exactly using your formula)
            planePositions = [rhinionPosition + (i + 1) * distance / (numPlanes + 1) * ptpPlaneNormal for i in range(numPlanes)]
            
            # Create new planes with names (exactly as in your code)
            for i, pos in enumerate(planePositions):
                planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', f'Plane_{planeNames[i]}')
                planeNode.SetOrigin(pos)
                planeNode.SetNormal(ptpPlaneNormal)
                planeNode.SetSize(150.0, 150.0)
                
                # Add colors for better visibility
                if i == 0:
                    planeNode.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green
                elif i == 1:
                    planeNode.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)  # Blue
                elif i == 2:
                    planeNode.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)  # Yellow
                else:
                    planeNode.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)  # Orange
                    
                planeNode.GetDisplayNode().SetOpacity(0.7)
                
                # Add to our collection
                self.mirrorPlanes.append(planeNode)
            
            # Display the MAW measurement in the node name
            maw_distance = np.linalg.norm(right_point - left_point)
            mawNode.SetName(f"maximum_nasal_width_MAW: {maw_distance:.2f}mm")
            
            # Update status
            self.mirrorPlanesStatusLabel.text = f"✅ Created {numPlanes+1} planes (A-{planeNames[-1]}) successfully!"
            
        except Exception as e:
            self.mirrorPlanesStatusLabel.text = f"❌ Error: {str(e)}"
            import traceback
            traceback.print_exc()
            
    def onCreateIntersectionLinesClicked(self):
        """Create intersection lines between planes"""
        try:
            # Update status
            self.intersectionLinesStatusLabel.text = "Creating intersection lines..."
            slicer.app.processEvents()
            
            import numpy as np
            
            # Check for required planes
            if not slicer.util.getNode('INB'):
                self.intersectionLinesStatusLabel.text = "Error: INB plane not found! Create reference planes first."
                return
                
            # Get number of mirror planes from UI to determine how many intersection lines to create
            planeCount = self.planeCountSlider.value if hasattr(self, 'planeCountSlider') else 6
            
            # Clear any existing intersection lines
            for lineName in ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']:
                try:
                    node = slicer.util.getNode(lineName)
                    if node:
                        slicer.mrmlScene.RemoveNode(node)
                except:
                    pass
            
            # YOUR EXACT CODE FOR CREATING INTERSECTION LINES
            # Function to create intersection line between two planes
            def create_intersection_line(planeNode1, planeNode2, lineNodeName):
                # Create a new line node for the intersection line
                intersectionLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', lineNodeName)

                # Get the normal vectors and points on the planes
                normal1 = np.array(planeNode1.GetNormalWorld())
                point1 = np.array(planeNode1.GetOriginWorld())
                normal2 = np.array(planeNode2.GetNormalWorld())
                point2 = np.array(planeNode2.GetOriginWorld())

                # Calculate the direction vector of the intersection line
                direction = np.cross(normal1, normal2)

                # Check if the planes are parallel
                if np.linalg.norm(direction) == 0:
                    print(f"The planes {planeNode1.GetName()} and {planeNode2.GetName()} are parallel and do not intersect.")
                    return False
                else:
                    # Calculate a point on the intersection line
                    A = np.array([normal1, normal2, direction])
                    b = np.array([np.dot(normal1, point1), np.dot(normal2, point2), 0])
                    intersection_point = np.linalg.solve(A, b)

                    # Define the start and end points of the line, extending further
                    extension_factor = 1000  # Adjust this factor as needed
                    start_point = intersection_point - extension_factor * direction
                    end_point = intersection_point + extension_factor * direction

                    # Set the points in the line node
                    intersectionLineNode.AddControlPointWorld(start_point)
                    intersectionLineNode.AddControlPointWorld(end_point)

                    print(f"Extended intersection line {lineNodeName} created successfully.")
                    return True

            # List of plane pairs and corresponding line node names
            plane_pairs = []
            planeNames = ['A', 'B', 'C', 'D', 'E', 'F'][:planeCount]
            for planeName in planeNames:
                plane_pairs.append(('INB', f'Plane_{planeName}', f'INB_{planeName}'))
                
            # Counter for successful lines
            successCount = 0

            # Iterate over each pair and create the intersection lines
            for plane1, plane2, lineName in plane_pairs:
                try:
                    planeNode1 = slicer.util.getNode(plane1)
                    planeNode2 = slicer.util.getNode(plane2)
                    if create_intersection_line(planeNode1, planeNode2, lineName):
                        successCount += 1
                        
                        # Add color to the line
                        lineNode = slicer.util.getNode(lineName)
                        lineNode.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)  # Orange
                        lineNode.GetDisplayNode().SetLineWidth(0.3)  
                        
                except Exception as e:
                    print(f"Error creating line {lineName}: {str(e)}")
            
            # Update status
            self.intersectionLinesStatusLabel.text = f"✅ Created {successCount} intersection lines successfully!"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.intersectionLinesStatusLabel.text = f"❌ Error: {str(e)}"

    def onCreateLinesABClicked(self):
        """Create reference lines A and B"""
        try:
            # Update status
            self.linesABStatusLabel.text = "Creating lines A and B..."
            slicer.app.processEvents()
            
            # Clear any existing lines A and B
            for lineName in ['Line_A', 'Line_B']:
                try:
                    node = slicer.util.getNode(lineName)
                    if node:
                        slicer.mrmlScene.RemoveNode(node)
                except:
                    pass
            
            # YOUR EXACT CODE FOR CREATING LINES A AND B
            import vtk
            
            # Get the "hard_tissue_PU" node (using your landmarks selector instead)
            F = self.landmarksSelector.currentNode()
            if not F:
                self.linesABStatusLabel.text = "Error: Please select landmarks first!"
                return
                
            # Create the first line node
            L_A = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'Line_A')

            # Retrieve and add the first point (position 0)
            firstPoint = F.GetNthControlPointPositionVector(0)
            L_A.AddControlPoint(firstPoint)

            # Retrieve and add the second point (position 3)
            secondPoint = F.GetNthControlPointPositionVector(3)
            L_A.AddControlPoint(secondPoint)
            
            # Set display properties
            L_A.GetDisplayNode().SetSelectedColor(0.0, 1.0, 1.0)  # Cyan
            L_A.GetDisplayNode().SetLineWidth(0.3)  

            # Retrieve the point at position 5
            thirdPoint = F.GetNthControlPointPositionVector(5)

            # Calculate the direction vector of the first line
            directionVector = vtk.vtkVector3d()
            directionVector.SetX(secondPoint.GetX() - firstPoint.GetX())
            directionVector.SetY(secondPoint.GetY() - firstPoint.GetY())
            directionVector.SetZ(secondPoint.GetZ() - firstPoint.GetZ())

            # Create the second line node
            L_B = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'Line_B')

            # Add the third point (position 5)
            L_B.AddControlPoint(thirdPoint)

            # Extend the direction vector by a factor (e.g., 2 for doubling the length)
            factor = 2
            extendedDirectionVector = vtk.vtkVector3d()
            extendedDirectionVector.SetX(directionVector.GetX() * factor)
            extendedDirectionVector.SetY(directionVector.GetY() * factor)
            extendedDirectionVector.SetZ(directionVector.GetZ() * factor)

            # Calculate and add the fourth point (extended)
            fourthPoint = vtk.vtkVector3d()
            fourthPoint.SetX(thirdPoint.GetX() + extendedDirectionVector.GetX())
            fourthPoint.SetY(thirdPoint.GetY() + extendedDirectionVector.GetY())
            fourthPoint.SetZ(thirdPoint.GetZ() + extendedDirectionVector.GetZ())
            L_B.AddControlPoint(fourthPoint)
            
            # Set display properties
            L_B.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)  # Yellow
            L_B.GetDisplayNode().SetLineWidth(0.3)  
            
            # Update status
            self.linesABStatusLabel.text = "✅ Lines A and B created successfully!"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.linesABStatusLabel.text = f"❌ Error: {str(e)}"

# Create an instance of the GUI
nasal_gui = ProkopecUbelakerGUI()
nasal_gui.setWindowTitle("Prokopec-Ubelaker Nasal Prediction")
nasal_gui.show()# ProkopecUbelakerGUI.py
# A beginner-friendly GUI for the Prokopec-Ubelaker nasal prediction method
# Just copy-paste this entire script into 3D Slicer's Python console!

# ProkopecUbelakerGUI.py
# A beginner-friendly GUI for the Prokopec-Ubelaker nasal prediction method
# Just copy-paste this entire script into 3D Slicer's Python console!

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import math  # Add this import

class ProkopecUbelakerGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.mainLayout = qt.QVBoxLayout(self)  # Use mainLayout instead of layout
        
        # Create stacked widget for steps
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        # Create step widgets
        self.createStepWidgets()
        
        # Set up navigation
        self.setupNavigation()
        
        # Initialize step tracking
        self.currentStep = 0
        self.updateStepUI()
        
    def setupNavigation(self):
        """Set up navigation buttons"""
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        
        # Previous button
        self.prevButton = qt.QPushButton("← Previous")
        self.prevButton.setMaximumWidth(120)
        navLayout.addWidget(self.prevButton)
        self.prevButton.connect('clicked(bool)', self.onPrevButtonClicked)
        
        # Step counter
        self.stepLabel = qt.QLabel("Step 1/9")
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        navLayout.addWidget(self.stepLabel)
        
        # Next button
        self.nextButton = qt.QPushButton("Next →")
        self.nextButton.setMaximumWidth(120)
        navLayout.addWidget(self.nextButton)
        self.nextButton.connect('clicked(bool)', self.onNextButtonClicked)
        
        # Help button
        self.helpButton = qt.QPushButton("Help")
        self.helpButton.setMaximumWidth(80)
        navLayout.addWidget(self.helpButton)
        self.helpButton.connect('clicked(bool)', self.onHelpClicked)
        
        self.mainLayout.addWidget(navWidget)
        
    def onPrevButtonClicked(self):
        """Go to previous step"""
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()
            print(f"Now showing step {self.currentStep+1}")
            
    def onNextButtonClicked(self):
        """Go to next step"""
        if self.currentStep < self.stepStack.count - 1:
            self.currentStep += 1
            self.updateStepUI()
            print(f"Now showing step {self.currentStep+1}")
            
    def checkPrerequisites(self):
        """Check if prerequisites are completed"""
        # Create a message box for the FHP alignment check
        messageBox = qt.QMessageBox()
        messageBox.setIcon(qt.QMessageBox.Question)
        messageBox.setWindowTitle("Prerequisite Check")
        messageBox.setText("Before proceeding, please confirm that your skull model is properly aligned in the Frankfurt Horizontal Plane (FHP).")
        messageBox.setInformativeText("Has the skull model been aligned in the FHP?")
        messageBox.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.No)
        messageBox.setDefaultButton(qt.QMessageBox.No)
        
        # Show the message box
        choice = messageBox.exec_()
        
        # If the user hasn't aligned the skull, show instructions
        if choice == qt.QMessageBox.No:
            # Create a dialog with more options (NON-MODAL so user can interact with scene)
            alignmentDialog = qt.QDialog()
            alignmentDialog.setWindowTitle("FHP Alignment Helper")
            alignmentDialog.setMinimumWidth(500)
            alignmentDialog.setWindowFlags(qt.Qt.Window | qt.Qt.WindowStaysOnTopHint)  # Make non-modal!
            layout = qt.QVBoxLayout(alignmentDialog)
            
            # Add instructions label
            instructionsLabel = qt.QLabel("Please align the skull in the FHP before using this tool.")
            instructionsLabel.setWordWrap(True)
            layout.addWidget(instructionsLabel)
            
            # Add detailed instructions with link
            detailedLabel = qt.QLabel(
                "Quick steps for FHP alignment:\n\n"
                "1. Load your CT volume in 3D Slicer\n"
                "2. Download and place the FHP landmarks onto the cranium (3 points)\n"
                "3. Run the automatic FHP alignment\n"
                "4. Harden the transform when finished"
            )
            detailedLabel.setWordWrap(True)
            layout.addWidget(detailedLabel)
            
            # Add link to detailed instructions
            linkLabel = qt.QLabel("<a href='https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Start%20here%20/002_Realign%20CT%20in%20the%20standard%20FHP.md#re-alignment-of-scans'>View detailed instructions on GitHub</a>")
            linkLabel.setOpenExternalLinks(True)
            layout.addWidget(linkLabel)
            
            # Add volume selector (right after the link label)
            volumeSelectFrame = qt.QFrame()
            volumeSelectLayout = qt.QFormLayout(volumeSelectFrame)
            volumeSelector = slicer.qMRMLNodeComboBox()
            volumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
            volumeSelector.selectNodeUponCreation = True
            volumeSelector.addEnabled = False
            volumeSelector.removeEnabled = False
            volumeSelector.noneEnabled = True
            volumeSelector.setMRMLScene(slicer.mrmlScene)
            volumeSelector.setToolTip("Select the skull volume to align")
            volumeSelectLayout.addRow("Skull Volume:", volumeSelector)
            layout.addWidget(volumeSelectFrame)
            
            # Add spacing
            layout.addSpacing(10)
            
            # Add download landmarks button
            downloadButton = qt.QPushButton("Download FHP Landmarks")
            layout.addWidget(downloadButton)
            
            # Add status label
            statusLabel = qt.QLabel("Ready to download FHP landmarks...")
            statusLabel.setWordWrap(True)
            layout.addWidget(statusLabel)
            
            # Add run alignment button (initially disabled)
            alignmentButton = qt.QPushButton("Run Automatic FHP Alignment")
            alignmentButton.enabled = False
            layout.addWidget(alignmentButton)
            
            # Add alignment status label
            alignmentStatusLabel = qt.QLabel("")
            alignmentStatusLabel.setWordWrap(True)
            layout.addWidget(alignmentStatusLabel)
            
            # Add continue button (initially disabled)
            continueButton = qt.QPushButton("Continue to Nasal Prediction")
            continueButton.enabled = False
            layout.addWidget(continueButton)
            
            # Define button click functions
            def onDownloadLandmarksClicked():
                try:
                    # URL for the FHP landmarks
                    url = "https://github.com/user-attachments/files/21429663/FHP_landmarks.mrk.json"
                    
                    # Create a temporary file to download to
                    with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                        temp_path = temp_file.name
                    
                    try:
                        # Show download status
                        statusLabel.text = "Downloading landmarks..."
                        slicer.app.processEvents()
                        
                        # Download the file
                        urllib.request.urlretrieve(url, temp_path)
                        
                        # Load the downloaded file
                        fhpNode = slicer.util.loadMarkups(temp_path)
                        
                        if fhpNode:
                            # Rename for clarity
                            fhpNode.SetName("FHP_Landmarks")
                            statusLabel.text = "FHP Landmarks loaded successfully! Please adjust the points on your skull."
                            alignmentButton.enabled = True
                        else:
                            statusLabel.text = "Failed to load FHP landmarks."
                        
                        # Clean up the temporary file
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                            
                    except Exception as e:
                        statusLabel.text = f"Error downloading landmarks: {str(e)}"
                        
                except Exception as e:
                    statusLabel.text = f"Error: {str(e)}"
            
            def onAlignmentClicked():
                try:
                    alignmentStatusLabel.text = "Running FHP alignment... Please wait."
                    slicer.app.processEvents()
                    
                    # Find the FHP landmarks node
                    fhpNode = None
                    for node in slicer.mrmlScene.GetNodesByClass('vtkMRMLMarkupsFiducialNode'):
                        if node.GetName() == "FHP_Landmarks":
                            fhpNode = node
                            break
                    
                    if not fhpNode:
                        alignmentStatusLabel.text = "Error: FHP landmarks not found. Please download and place them first."
                        return
                    
                    # Get the selected volume
                    V = volumeSelector.currentNode()
                    if not V:
                        alignmentStatusLabel.text = "Error: No volume selected. Please select a skull model to align."
                        return
                    
                    # Get the fiducial IDs of porions and zygomatico-orbitale suture from the fiducial list by name
                    po1_id = -1; po2_id = -1; zyo_id = -1;
                    
                    for i in range(0, fhpNode.GetNumberOfControlPoints()):
                        if fhpNode.GetNthControlPointLabel(i) == 'poR':
                            po1_id = i
                        if fhpNode.GetNthControlPointLabel(i) == 'poL':
                            po2_id = i
                        if fhpNode.GetNthControlPointLabel(i) == 'zyoL':
                            zyo_id = i
                    
                    # Check if all landmarks were found
                    if po1_id == -1 or po2_id == -1 or zyo_id == -1:
                        alignmentStatusLabel.text = "Error: Could not find all required landmarks (poR, poL, zyoL)."
                        return
                    
                    # Get the coordinates of landmarks
                    po1 = [0, 0, 0]
                    po2 = [0, 0, 0]
                    zyo = [0, 0, 0]
                    
                    fhpNode.GetNthControlPointPosition(po1_id, po1)
                    fhpNode.GetNthControlPointPosition(po2_id, po2)
                    fhpNode.GetNthControlPointPosition(zyo_id, zyo)
                    
                    # The vector between two porions that we will align to LR axis by calculating the yaw angle
                    po = [po1[0] - po2[0], po1[1] - po2[1], po1[2] - po2[2]]
                    vTransform = vtk.vtkTransform()
                    vTransform.RotateZ(-np.arctan2(po[1], po[0]) * 180 / np.pi)
                    transform = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode')
                    transform.SetMatrixTransformToParent(vTransform.GetMatrix())
                    
                    # Apply the transform to the fiducials and the volume
                    V.SetAndObserveTransformNodeID(transform.GetID())
                    fhpNode.SetAndObserveTransformNodeID(transform.GetID())
                    
                    # Get the updated (transformed) coordinates from the list
                    po1 = [0, 0, 0]
                    po2 = [0, 0, 0]
                    zyo = [0, 0, 0]
                    
                    fhpNode.GetNthControlPointPosition(po1_id, po1)
                    fhpNode.GetNthControlPointPosition(po2_id, po2)
                    fhpNode.GetNthControlPointPosition(zyo_id, zyo)
                    
                    # Apply the transform to the coordinates
                    po1_t = vTransform.GetMatrix().MultiplyPoint([po1[0], po1[1], po1[2], 0])
                    po2_t = vTransform.GetMatrix().MultiplyPoint([po2[0], po2[1], po2[2], 0])
                    zyo_t = vTransform.GetMatrix().MultiplyPoint([zyo[0], zyo[1], zyo[2], 0])
                    po = [po1_t[0] - po2_t[0], po1_t[1] - po2_t[1], po1_t[2] - po2_t[2]]
                    
                    # Calculate the rotation for the roll 
                    vTransform2 = vtk.vtkTransform()
                    vTransform2.RotateY(np.arctan2(po[2], po[0]) * 180 / np.pi)
                    
                    # Apply the transform to previous transform hierarchy
                    transform2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode')
                    transform2.SetMatrixTransformToParent(vTransform2.GetMatrix())
                    transform.SetAndObserveTransformNodeID(transform2.GetID())
                    
                    # Get the coordinates again
                    po1 = [0, 0, 0]
                    po2 = [0, 0, 0]
                    zyo = [0, 0, 0]
                    
                    fhpNode.GetNthControlPointPosition(po1_id, po1)
                    fhpNode.GetNthControlPointPosition(po2_id, po2)
                    fhpNode.GetNthControlPointPosition(zyo_id, zyo)
                    
                    # The vector for pitch angle
                    po_zyo = [
                        zyo[0] - (po1[0] + po2[0]) / 2, 
                        zyo[1] - (po1[1] + po2[1]) / 2, 
                        zyo[2] - (po1[2] + po2[2]) / 2
                    ]
                    
                    # Calculate the transform for aligning pitch
                    vTransform3 = vtk.vtkTransform()
                    vTransform3.RotateX(-np.arctan2(po_zyo[2], po_zyo[1]) * 180 / np.pi)
                    
                    # Apply the transform to both fiducial list and the volume
                    transform3 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode')
                    transform3.SetMatrixTransformToParent(vTransform3.GetMatrix())
                    transform2.SetAndObserveTransformNodeID(transform3.GetID())
                    
                    # Harden the transform to apply it permanently
                    slicer.vtkSlicerTransformLogic().hardenTransform(V)
                    
                    # Update status and enable continue button
                    alignmentStatusLabel.text = "✅ Alignment completed successfully!"
                    continueButton.enabled = True
                    
                except Exception as e:
                    alignmentStatusLabel.text = f"❌ Alignment error: {str(e)}"
            
            def onContinueClicked():
                alignmentDialog.accept()
            
            # Connect button signals
            downloadButton.connect('clicked(bool)', onDownloadLandmarksClicked)
            alignmentButton.connect('clicked(bool)', onAlignmentClicked)
            continueButton.connect('clicked(bool)', onContinueClicked)
            
            # Show the dialog (non-modal)
            alignmentDialog.show()
            
            # We need another way to check the result since we're not using exec_()
            self.fhpDialogComplete = False
            
            def onDialogFinished(result):
                self.fhpDialogComplete = (result == qt.QDialog.Accepted)
                
            alignmentDialog.finished.connect(onDialogFinished)
            
            # Wait a moment to let user see instructions
            slicer.util.delayDisplay("Please place the landmarks and click Continue when done", 3000)
            
    def createStepWidgets(self):
        """Create all step widgets for the GUI"""
        # Step 1: Welcome and Introduction
        self.createStep1Widget()
        # Step 2: Landmark Selection
        self.createStep2Widget()
        # Step 3: Reference Plane Creation
        self.createStep3Widget()
        # Step 4: Mirror Plane Configuration
        self.createStep4Widget()
        # Step 5: Intersection Creation
        self.createStep5Widget()
        # Step 6: Bone Point Setup
        self.createStep6Widget()
        # Step 7: Bone Profile Results
        self.createStep7Widget()
        # Step 8: Soft Tissue Options
        self.createStep8Widget()
        # Step 9: Results Analysis
        self.createStep9Widget()    
        
    def createStep1Widget(self):
        """Create widget for Step 1: Welcome Screen"""
        step1Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step1Widget)
        
        # Add welcome title
        titleLabel = qt.QLabel("Welcome to the Prokopec-Ubelaker Nasal Prediction Tool!")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Add description
        instructionsLabel = qt.QLabel(
            "This tool will guide you through the steps of creating a nasal prediction.\n\n"
            "Click 'Next' to begin setting up your landmarks."
        )
        instructionsLabel.setWordWrap(True)
        layout.addWidget(instructionsLabel)
        
        # Add to step stack
        self.stepStack.addWidget(step1Widget)

    def createStep2Widget(self):
        """Create widget for Step 2: Input Selection"""
        step2Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step2Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 2: Hard Tissue Landmark Selection")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Please select or load the required 7 hard tissue landmarks:\n\n"
            "• nasion - intersection of nasofrontal sutures\n"
            "• inion - median point at base of external occipital protuberance\n"
            "• bregma - where sagittal and coronal sutures meet\n"
            "• prosthion - median point between central incisors\n"
            "• subspinale - deepest point below anterior nasal spine\n"
            "• rhinion - most rostral point on internasal suture\n"
            "• acanthion - most anterior tip of anterior nasal spine"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create landmark selector frame
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        
        # Create landmark selector
        self.landmarksSelector = slicer.qMRMLNodeComboBox()
        self.landmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.landmarksSelector.selectNodeUponCreation = True
        self.landmarksSelector.addEnabled = True
        self.landmarksSelector.removeEnabled = True
        self.landmarksSelector.noneEnabled = True
        self.landmarksSelector.setMRMLScene(slicer.mrmlScene)
        self.landmarksSelector.setToolTip("Select the landmarks node")
        selectorLayout.addRow("Hard Tissue Landmarks: ", self.landmarksSelector)
        
        layout.addWidget(selectorFrame)
        
        # Create load button (removed the Sample Data button)
        self.loadLandmarksButton = qt.QPushButton("Load From File")
        layout.addWidget(self.loadLandmarksButton)
        
        # Add status label
        self.landmarksStatusLabel = qt.QLabel("Please select or load landmarks")
        self.landmarksStatusLabel.setWordWrap(True)
        layout.addWidget(self.landmarksStatusLabel)
        
        # Connect button
        self.loadLandmarksButton.connect('clicked(bool)', self.onLoadLandmarksClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step2Widget)

    def createStep3Widget(self):
        """Create widget for Step 3: Reference Plane Creation"""
        step3Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step3Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 3: Reference Plane Creation")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Create the reference planes needed for the Prokopec-Ubelaker method:\n\n"
            "• INB plane: defined by inion, nasion, and bregma\n"
            "• NP plane: perpendicular to INB, through nasion and prosthion\n"
            "• PT plane: perpendicular to both INB and NP planes"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Add debug button for beginners
        self.checkLandmarksButton = qt.QPushButton("Check Landmarks")
        self.checkLandmarksButton.toolTip = "Check if all required landmarks are detected correctly"
        layout.addWidget(self.checkLandmarksButton)
        
        # Create button to create planes
        self.createReferencePlanesButton = qt.QPushButton("Create Reference Planes")
        layout.addWidget(self.createReferencePlanesButton)
        
        # Add status label
        self.planesStatusLabel = qt.QLabel("Ready to create reference planes")
        self.planesStatusLabel.setWordWrap(True)
        layout.addWidget(self.planesStatusLabel)
        
        # Connect buttons
        self.checkLandmarksButton.connect('clicked(bool)', self.onCheckLandmarksClicked)
        self.createReferencePlanesButton.connect('clicked(bool)', self.onCreateReferencePlanesClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step3Widget)

    def createStep4Widget(self):
        """Create widget for Step 4: Mirror Plane Configuration"""
        step4Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step4Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 4: Mirror Plane Configuration")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Set up the mirror planes for the nasal prediction:\n\n"
            "• Choose between 4, 5, or 6 mirror planes\n"
            "• The planes will be placed equidistant between rhinion and maximum nasal width\n"
            "• You need to select or create a Maximum Nasal Width measurement"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create selector for maximum width
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        
        self.mawSelector = slicer.qMRMLNodeComboBox()
        self.mawSelector.nodeTypes = ["vtkMRMLMarkupsLineNode"]  # LINE node, not fiducials
        self.mawSelector.selectNodeUponCreation = False
        self.mawSelector.addEnabled = True  # Allow creating a new line
        self.mawSelector.removeEnabled = False
        self.mawSelector.noneEnabled = True
        self.mawSelector.setMRMLScene(slicer.mrmlScene)
        selectorLayout.addRow("Maximum Aperture Width: ", self.mawSelector)
        
        # Add plane count selector
        self.planeCountSlider = qt.QSlider(qt.Qt.Horizontal)
        self.planeCountSlider.minimum = 4
        self.planeCountSlider.maximum = 6
        self.planeCountSlider.value = 5
        self.planeCountSlider.setTickPosition(qt.QSlider.TicksBelow)
        self.planeCountSlider.setTickInterval(1)
        self.planeCountSlider.setSingleStep(1)
        
        self.planeCountLabel = qt.QLabel(f"Number of mirror planes: {self.planeCountSlider.value}")
        
        selectorLayout.addRow("", self.planeCountLabel)
        selectorLayout.addRow("", self.planeCountSlider)
        
        layout.addWidget(selectorFrame)
        
        # Create button to create planes
        self.createMirrorPlanesButton = qt.QPushButton("Create Mirror Planes")
        layout.addWidget(self.createMirrorPlanesButton)
        
        # Add status label
        self.mirrorPlanesStatusLabel = qt.QLabel("Ready to create mirror planes")
        self.mirrorPlanesStatusLabel.setWordWrap(True)
        layout.addWidget(self.mirrorPlanesStatusLabel)
        
        # Connect buttons and sliders
        self.planeCountSlider.connect('valueChanged(int)', self.onPlaneCountChanged)
        self.createMirrorPlanesButton.connect('clicked(bool)', self.onCreateMirrorPlanesClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step4Widget)

    def createStep5Widget(self):
        """Create the widget for step 5"""
        step5Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step5Widget)
        # Title
        titleLabel = qt.QLabel("Step 5: Mirror Planes and Intersections")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Create intersection planes and locate important intersection points:"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Step instructions
        instructionsLabel = qt.QLabel("Step 5: Create intersection lines")
        instructionsLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(instructionsLabel)
        
        # Description
        descriptionLabel = qt.QLabel("Create lines where planes intersect.")
        descriptionLabel.setWordWrap(True)
        layout.addWidget(descriptionLabel)
        
        # First button - Intersection Lines
        self.createIntersectionLinesButton = qt.QPushButton("Create Intersection Lines")
        self.createIntersectionLinesButton.toolTip = "Create intersection lines between INB and mirror planes"
        self.createIntersectionLinesButton.connect('clicked(bool)', self.onCreateIntersectionLinesClicked)
        layout.addWidget(self.createIntersectionLinesButton)
        
        # Status label for intersection lines
        self.intersectionLinesStatusLabel = qt.QLabel("Ready to create intersection lines...")
        self.intersectionLinesStatusLabel.setStyleSheet("background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.intersectionLinesStatusLabel)
        
        # Add some space
        layout.addWidget(qt.QLabel(""))
        
        # Second button - Lines A and B
        self.createLinesABButton = qt.QPushButton("Create Lines A and B")
        self.createLinesABButton.toolTip = "Create reference lines A and B"
        self.createLinesABButton.connect('clicked(bool)', self.onCreateLinesABClicked)
        layout.addWidget(self.createLinesABButton)
        
        # Status label for lines A and B
        self.linesABStatusLabel = qt.QLabel("Ready to create lines A and B...")
        self.linesABStatusLabel.setStyleSheet("background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.linesABStatusLabel)
        
        # Add Line B intersection button (NEW!)
        self.lineBIntersectionButton = qt.QPushButton("Find intersection points between the intersection lines and Line B")
        self.lineBIntersectionButton.toolTip = "This will create points called mirrorB_A, etc"
        layout.addWidget(self.lineBIntersectionButton)
        
        # Add Line A intersection button (NEW!)
        self.lineAIntersectionButton = qt.QPushButton("Find intersection points between the intersection lines and Line A")
        self.lineAIntersectionButton.toolTip = "This will create points called mirrorA_A, etc"
        layout.addWidget(self.lineAIntersectionButton)
        
        # Add explanatory labels (NEW!)
        lineBLabel = qt.QLabel("This will create points called mirrorB_A, mirrorB_B, etc.")
        lineBLabel.setWordWrap(True)
        layout.addWidget(lineBLabel)
        
        lineALabel = qt.QLabel("This will create points called mirrorA_A, mirrorA_B, etc.")
        lineALabel.setWordWrap(True)
        layout.addWidget(lineALabel)
        
        # Status label
        self.intersectionsStatusLabel = qt.QLabel("Ready to create intersections")
        self.intersectionsStatusLabel.setWordWrap(True)
        layout.addWidget(self.intersectionsStatusLabel)
        
        # Connect the new buttons (NEW!)
        self.lineBIntersectionButton.connect('clicked(bool)', self.onFindLineBIntersectionClicked)
        self.lineAIntersectionButton.connect('clicked(bool)', self.onFindLineAIntersectionClicked)
        
         # Add to step stack
        self.stepStack.addWidget(step5Widget)

    def createStep6Widget(self):
        """Create widget for Step 6: Bone Point Setup"""
        step6Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step6Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 6: Bone Outline Setup")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Download the nasal bone outline landmarks based on your chosen number of mirror planes:\n\n"
            "• The outline landmarks must be placed along the lateral view of the nasal aperture\n"
            "• Points will automatically be named to match the number of planes you selected\n"
            "• After downloading, you may need to adjust point positions to match your skull"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create download button (renamed from "Auto-Setup Bone Points")
        self.downloadOutlineButton = qt.QPushButton("Download the aperture outline landmarks")
        layout.addWidget(self.downloadOutlineButton)
        
        # Add status label
        self.bonePointsStatusLabel = qt.QLabel("Ready to download bone outline landmarks")
        self.bonePointsStatusLabel.setWordWrap(True)
        layout.addWidget(self.bonePointsStatusLabel)
        
        # Add confirmation message near the next button
        self.confirmationLabel = qt.QLabel("✓ Have you allocated the outline points as described from a lateral view?")
        self.confirmationLabel.setStyleSheet("color: orange; font-weight: bold;")
        self.confirmationLabel.setWordWrap(True)
        layout.addWidget(self.confirmationLabel)
        
        # Connect button (rename the method too!)
        self.downloadOutlineButton.connect('clicked(bool)', self.onDownloadOutlineClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step6Widget)

    def createStep7Widget(self):
        """Create widget for Step 7: Bone Profile Results"""
        step7Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step7Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 7: Bone Profile Results")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Create and view bone measurements before adding soft tissue:\n\n"
            "• Click 'Create Bone Measurements' to generate measurements\n"
            "• View the measurements in the table\n"
            "• Export the bone measurements if needed"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create buttons
        self.createBoneMeasurementsButton = qt.QPushButton("Create Bone Measurements")
        layout.addWidget(self.createBoneMeasurementsButton)
        
        # Add measurements table
        self.boneMeasurementsTable = qt.QTableWidget()
        self.boneMeasurementsTable.setColumnCount(2)
        self.boneMeasurementsTable.setHorizontalHeaderLabels(["Measurement", "Value (mm)"])
        self.boneMeasurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self.boneMeasurementsTable.horizontalHeader().setSectionResizeMode(1, qt.QHeaderView.ResizeToContents)
        self.boneMeasurementsTable.verticalHeader().setVisible(False)
        layout.addWidget(self.boneMeasurementsTable)
        
        # Export button
        self.exportBoneResultsButton = qt.QPushButton("Export Bone Measurements")
        self.exportBoneResultsButton.enabled = False  # Initially disabled
        layout.addWidget(self.exportBoneResultsButton)
        
        # Add status label
        self.boneMeasurementsStatusLabel = qt.QLabel("Ready to create bone measurements")
        self.boneMeasurementsStatusLabel.setWordWrap(True)
        layout.addWidget(self.boneMeasurementsStatusLabel)
        
        # Connect buttons
        self.createBoneMeasurementsButton.connect('clicked(bool)', self.onCreateBoneMeasurementsClicked)
        self.exportBoneResultsButton.connect('clicked(bool)', self.onExportBoneResultsClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step7Widget)

    def createStep8Widget(self):
        """Create widget for Step 8: Soft Tissue Options"""
        step8Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step8Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 8: Soft Tissue Options")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Choose how to add soft tissue to your prediction:"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Create radio button group for soft tissue method
        methodFrame = qt.QFrame()
        methodLayout = qt.QVBoxLayout(methodFrame)
        
        self.softTissueMethodGroup = qt.QButtonGroup()
        
        # No soft tissue option
        self.noSoftTissueRadio = qt.QRadioButton("No soft tissue (continue with bone measurements only)")
        self.softTissueMethodGroup.addButton(self.noSoftTissueRadio, 0)
        methodLayout.addWidget(self.noSoftTissueRadio)
        
        # Standard method option
        self.standardMethodRadio = qt.QRadioButton("Standard Prokopec-Ubelaker (+2mm soft tissue)")
        self.standardMethodRadio.setChecked(True)  # Default option
        self.softTissueMethodGroup.addButton(self.standardMethodRadio, 1)
        methodLayout.addWidget(self.standardMethodRadio)
        
        # Custom method option
        self.customMethodRadio = qt.QRadioButton("Custom soft tissue thickness values")
        self.softTissueMethodGroup.addButton(self.customMethodRadio, 2)
        methodLayout.addWidget(self.customMethodRadio)
        
        layout.addWidget(methodFrame)
        
        # Custom thickness options (initially hidden)
        self.customThicknessFrame = qt.QFrame()
        customThicknessLayout = qt.QFormLayout(self.customThicknessFrame)
        
        self.topThicknessSpinBox = qt.QDoubleSpinBox()
        self.topThicknessSpinBox.setRange(1.0, 5.0)
        self.topThicknessSpinBox.setSingleStep(0.1)
        self.topThicknessSpinBox.setValue(1.2)
        self.topThicknessSpinBox.setSuffix("x")
        customThicknessLayout.addRow("Top third factor:", self.topThicknessSpinBox)
        
        self.middleThicknessSpinBox = qt.QDoubleSpinBox()
        self.middleThicknessSpinBox.setRange(1.0, 5.0)
        self.middleThicknessSpinBox.setSingleStep(0.1)
        self.middleThicknessSpinBox.setValue(1.3)
        self.middleThicknessSpinBox.setSuffix("x")
        customThicknessLayout.addRow("Middle third factor:", self.middleThicknessSpinBox)
        
        self.bottomThicknessSpinBox = qt.QDoubleSpinBox()
        self.bottomThicknessSpinBox.setRange(1.0, 5.0)
        self.bottomThicknessSpinBox.setSingleStep(0.1)
        self.bottomThicknessSpinBox.setValue(1.4)
        self.bottomThicknessSpinBox.setSuffix("x")
        customThicknessLayout.addRow("Bottom third factor:", self.bottomThicknessSpinBox)
        
        layout.addWidget(self.customThicknessFrame)
        self.customThicknessFrame.setVisible(False)  # Initially hidden
        
        # Create button to generate soft tissue
        self.generateSoftTissueButton = qt.QPushButton("Generate Soft Tissue Predictions")
        layout.addWidget(self.generateSoftTissueButton)
        
        # Add status label
        self.softTissueStatusLabel = qt.QLabel("Ready to generate soft tissue predictions")
        self.softTissueStatusLabel.setWordWrap(True)
        layout.addWidget(self.softTissueStatusLabel)
        
        # Connect buttons
        self.generateSoftTissueButton.connect('clicked(bool)', self.onGenerateSoftTissueClicked)
        self.customMethodRadio.connect('toggled(bool)', self.onCustomMethodToggled)
        
        # Add to step stack
        self.stepStack.addWidget(step8Widget)

    def createStep9Widget(self):
        """Create widget for Step 9: Results Analysis"""
        step9Widget = qt.QWidget()
        layout = qt.QVBoxLayout(step9Widget)
        
        # Title
        titleLabel = qt.QLabel("Step 9: Results Analysis")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(titleLabel)
        
        # Instructions
        detailLabel = qt.QLabel(
            "Review the measurements and export the results:"
        )
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # Add measurements table
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable.setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Predicted (mm)", "Actual (mm)"])
        self.measurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self.measurementsTable.horizontalHeader().setSectionResizeMode(1, qt.QHeaderView.ResizeToContents)
        self.measurementsTable.horizontalHeader().setSectionResizeMode(2, qt.QHeaderView.ResizeToContents)
        self.measurementsTable.verticalHeader().setVisible(False)
        layout.addWidget(self.measurementsTable)
        
        # Export buttons
        exportButtonFrame = qt.QFrame()
        exportButtonLayout = qt.QHBoxLayout(exportButtonFrame)
        
        self.copyToClipboardButton = qt.QPushButton("Copy to Clipboard")
        self.exportResultsButton = qt.QPushButton("Export Results to CSV")
        
        exportButtonLayout.addWidget(self.copyToClipboardButton)
        exportButtonLayout.addWidget(self.exportResultsButton)
        
        layout.addWidget(exportButtonFrame)
        
        # Add status label
        self.exportStatusLabel = qt.QLabel("Ready to export results")
        self.exportStatusLabel.setWordWrap(True)
        layout.addWidget(self.exportStatusLabel)
        
        # Add completion message
        completionLabel = qt.QLabel("🎉 Congratulations! You've completed the Prokopec-Ubelaker nasal prediction process!")
        completionLabel.setStyleSheet("font-weight: bold; color: green;")
        completionLabel.setWordWrap(True)
        layout.addWidget(completionLabel)
        
        # Connect buttons
        self.copyToClipboardButton.connect('clicked(bool)', self.onCopyToClipboardClicked)
        self.exportResultsButton.connect('clicked(bool)', self.onExportResultsClicked)
        
        # Add to step stack
        self.stepStack.addWidget(step9Widget)

    def updateStepUI(self):
        """Update UI for current step"""
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep+1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)

   
    def onBackClicked(self):
        """Handle back button click"""
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()

    def onNextClicked(self):
        """Handle next button click"""
        print(f"Next button clicked! Current step: {self.currentStep}, Total steps: {self.stepStack.count}")
        if self.currentStep < self.stepStack.count - 1:
            print("Moving to next step")
            self.currentStep += 1
            self.updateStepUI()
        else:
            print("Already at last step")

    def onHelpClicked(self):
        """Show help information for the current step"""
        helpMessages = [
            {
                "title": "Step 1: Input Selection",
                "text": "In this step, you need to load or select your landmarks file.",
                "details": (
                    "Required landmarks are:\n"
                    "• nasion - intersection of nasofrontal sutures\n"
                    "• inion - median point at base of external occipital protuberance\n"
                    "• bregma - where sagittal and coronal sutures meet\n"
                    "• prosthion - median point between central incisors\n"
                    "• subspinale - deepest point below anterior nasal spine\n"
                    "• rhinion - most rostral point on internasal suture\n"
                    "• acanthion - most anterior tip of anterior nasal spine"
                )
            },
            {
                "title": "Step 2: Reference Plane Creation",
                "text": "Create the reference planes needed for the Prokopec-Ubelaker method.",
                "details": (
                    "This step creates three reference planes:\n"
                    "• INB plane: defined by inion, nasion, and bregma\n"
                    "• NP plane: perpendicular to INB, through nasion and prosthion\n"
                    "• PT plane: perpendicular to both INB and NP planes"
                )
            },
            {
                "title": "Step 3: Mirror Plane Configuration",
                "text": "Set up the mirror planes for the nasal prediction.",
                "details": (
                    "Choose between 4, 5, or 6 mirror planes:\n"
                    "• More planes can give higher accuracy but requires more landmarks\n"
                    "• The planes will be placed equidistant between rhinion and maximum nasal width\n"
                    "• You need to select or create a Maximum Nasal Width measurement"
                )
            },
            {
                "title": "Step 4: Intersection Creation",
                "text": "Create intersection lines between reference planes.",
                "details": (
                    "This step creates:\n"
                    "• Intersection lines between the INB plane and each mirror plane\n"
                    "• Reference Line A: through nasion and prosthion\n"
                    "• Reference Line B: parallel to Line A through rhinion\n"
                    "• Intersection points between Line B and all mirror planes"
                )
            },
            {
                "title": "Step 5: Bone Point Setup",
                "text": "Place the bone points needed for measurement.",
                "details": (
                    "This step automatically:\n"
                    "• Finds existing bone points in your scene\n"
                    "• Loads missing bone points from your repository if available\n"
                    "• Creates new bone points if needed\n\n"
                    "Click 'Auto-Setup Bone Points' to have the tool download the number of points you need with the correct names"
                )
            },
            {
                "title": "Step 6: Bone Profile Results",
                "text": "Create and view bone measurements before adding soft tissue.",
                "details": (
                    "This step creates measurements for the nasal bone only (pred_no_soft):\n"
                    "• Click 'Create Bone Measurements' to generate measurements\n"
                    "• View the measurements in the table\n"
                    "• Export the bone measurements if needed\n\n"
                    "After this step, you'll decide how to add soft tissue."
                )
            },
            {
                "title": "Step 7: Soft Tissue Options",
                "text": "Choose how to add soft tissue to your prediction.",
                "details": (
                    "Choose from three options:\n"
                    "• No soft tissue: continue with bone measurements only (pred_no_soft)\n"
                    "• Standard Prokopec-Ubelaker: adds 2mm to each predicted point (pred_PU_soft)\n"
                    "• Custom values: set your own thickness factors (but be warned - these aren't official facial soft tissue thickness measurements!)\n\n"
                    "Click 'Generate Soft Tissue Predictions' after making your choice."
                )
            },
            {
                "title": "Step 8: Optional - Compare with Real Soft Tissue",
                "text": "Compare predictions with actual soft tissue (OPTIONAL).",
                "details": (
                    "This step is completely OPTIONAL and only needed if you want to measure prediction error.\n\n"
                    "If you have a real soft tissue model:\n"
                    "• Select it in the dropdown\n"
                    "• Click 'Compare with Real Soft Tissue' to see the difference\n\n"
                    "If you don't have a soft tissue model, just click 'Skip This Step'."
                )
            },
            {
                "title": "Step 9: Results Analysis",
                "text": "Review the measurements and export the results.",
                "details": (
                    "The measurements table shows:\n"
                    "• noseprofiletoB# - distances from mirror points to soft tissue\n"
                    "• nasalbonetoB# - distances from mirror points to nasal bone\n"
                    "• Comparison between predicted and actual values (if available)\n\n"
                    "You can export these measurements to CSV or copy them to clipboard."
                )
            }
        ]
        
        # Show the help message for the current step
        if self.currentStep < len(helpMessages):
            helpMessage = helpMessages[self.currentStep]
            
            # Create a message box
            messageBox = qt.QMessageBox()
            messageBox.setIcon(qt.QMessageBox.Information)
            messageBox.setWindowTitle(helpMessage["title"])
            messageBox.setText(helpMessage["text"])
            messageBox.setInformativeText(helpMessage["details"])
            messageBox.setStandardButtons(qt.QMessageBox.Ok)
            
            # Show the message box
            messageBox.exec_()
        else:
            # Generic help message for steps without specific help
            messageBox = qt.QMessageBox()
            messageBox.setIcon(qt.QMessageBox.Information)
            messageBox.setWindowTitle("Help")
            messageBox.setText("Help information for this step is not available.")
            messageBox.setStandardButtons(qt.QMessageBox.Ok)
            messageBox.exec_()

    # Required helper methods for functionality
    def onLoadLandmarksClicked(self):
        """Handle loading landmarks from file"""
        fileName = qt.QFileDialog.getOpenFileName(None, "Load Landmarks", "", "Markup Files (*.mrk.json);;All Files (*.*)")
        if fileName:
            try:
                landmarksNode = slicer.util.loadMarkups(fileName)
                if landmarksNode:
                    self.landmarksSelector.setCurrentNode(landmarksNode)
                    self.landmarksStatusLabel.text = "Landmarks loaded successfully!"
                else:
                    self.landmarksStatusLabel.text = "Failed to load landmarks from file."
            except Exception as e:
                self.landmarksStatusLabel.text = f"Error loading landmarks: {str(e)}"

    def onSampleLandmarksClicked(self):
        """Handle loading sample landmarks"""
        try:
            # URL for the sample landmarks
            url = "https://github.com/user-attachments/files/21412636/skull_landmarks.mrk.json"
            
            # Update status
            self.landmarksStatusLabel.text = "Downloading sample landmarks..."
            slicer.app.processEvents()
            
            # Create a temporary file to download to
            with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Download and load the file
            urllib.request.urlretrieve(url, temp_path)
            landmarksNode = slicer.util.loadMarkups(temp_path)
            
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            
            # Update UI
            if landmarksNode:
                self.landmarksSelector.setCurrentNode(landmarksNode)
                self.landmarksStatusLabel.text = "Sample landmarks loaded successfully!"
            else:
                self.landmarksStatusLabel.text = "Failed to load sample landmarks."
                
        except Exception as e:
            self.landmarksStatusLabel.text = f"Error: {str(e)}"

    def onPlaneCountChanged(self, value):
        """Update the plane count label when slider changes"""
        self.planeCountLabel.text = f"Number of mirror planes: {value}"

    def onCustomMethodToggled(self, checked):
        """Handle toggling custom method radio button"""
        self.customThicknessFrame.setVisible(checked)

    # These methods need to be implemented based on your functionality
    # They can be simple placeholders for now
        def onCreateReferencePlanesClicked(self):
            """Create reference planes using the EXACT code provided by the user"""
            try:
                # Update status
                self.planesStatusLabel.text.text = "Creating reference planes..."
                slicer.app.processEvents()
                
                import numpy as np
                
                # === COPY OF YOUR EXACT CODE FOR INB PLANE ===
                # Get the points from the landmarks node (your "hard_tissue_PU")
                hardTissueNode = self.landmarksSelector.currentNode()
                if not hardTissueNode:
                    self.planesStatusLabel.text.text = "Error: Please select landmarks first!"
                    return
                    
                # Get the first three points EXACTLY as in your code
                point1 = np.array(hardTissueNode.GetNthControlPointPosition(0))
                point2 = np.array(hardTissueNode.GetNthControlPointPosition(1))
                point3 = np.array(hardTissueNode.GetNthControlPointPosition(2))

                # Calculate the normal of the plane defined by the three points - EXACTLY as in your code
                v1 = point2 - point1
                v2 = point3 - point1
                planeNormal = np.cross(v1, v2)
                planeNormal = planeNormal / np.linalg.norm(planeNormal)  # Normalize the normal vector

                # Create a new plane node - EXACTLY as in your code
                self.inbPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'INB')

                # Set the origin of the new plane to the first point - EXACTLY as in your code
                self.inbPlane.SetOrigin(point1)

                # Set the normal of the new plane - EXACTLY as in your code
                self.inbPlane.SetNormal(planeNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.inbPlane.SetSize(200.0, 200.0)
                self.inbPlane.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                self.inbPlane.GetDisplayNode().SetOpacity(0.3)
                self.inbPlane.GetDisplayNode().SetVisibility(True)
                self.inbPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.inbPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR NPP PLANE ===
                # Get the 'INB' plane node - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')

                # Get the coordinates of 'prosthion' and 'nasion' - EXACTLY as in your code
                # Assuming prosthion is point 0 and nasion is point 3 as in your code
                prosthion = np.array(hardTissueNode.GetNthControlPointPositionWorld(0))
                nasion = np.array(hardTissueNode.GetNthControlPointPositionWorld(3))

                # Calculate the normal of the 'INB' plane - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())

                # Calculate the vector between 'prosthion' and 'nasion' - EXACTLY as in your code
                vectorPN = nasion - prosthion

                # Calculate the normal of the new plane - EXACTLY as in your code
                newPlaneNormal = np.cross(inbNormal, vectorPN)
                newPlaneNormal /= np.linalg.norm(newPlaneNormal)  # Normalize the vector

                # Create a new plane node and name it 'NPP' - EXACTLY as in your code
                self.nppPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'NPP')

                # Set the origin of the new plane to 'prosthion' - EXACTLY as in your code
                self.nppPlane.SetOriginWorld(prosthion)

                # Set the normal of the new plane - EXACTLY as in your code
                self.nppPlane.SetNormalWorld(newPlaneNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.nppPlane.SetSize(200.0, 200.0)
                self.nppPlane.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green
                self.nppPlane.GetDisplayNode().SetOpacity(1)
                self.nppPlane.GetDisplayNode().SetVisibility(True)
                self.nppPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.nppPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR PTP PLANE ===
                # Get the 'INB' and 'NPP' plane nodes - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')
                nppPlaneNode = slicer.util.getNode('NPP')

                # Calculate the normals of the 'INB' and 'NPP' planes - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())
                nppNormal = np.array(nppPlaneNode.GetNormalWorld())

                # Calculate the normal of the new plane 'PTP' - EXACTLY as in your code
                ptpNormal = np.cross(inbNormal, nppNormal)
                ptpNormal /= np.linalg.norm(ptpNormal)  # Normalize the vector

                # Create a new plane node and name it 'PTP' - EXACTLY as in your code
                self.ptPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'PTP')

                # Set the origin of the new plane to the origin of 'INB' - EXACTLY as in your code
                self.ptPlane.SetOriginWorld(inbPlaneNode.GetOriginWorld())

                # Set the normal of the new plane - EXACTLY as in your code
                self.ptPlane.SetNormalWorld(ptpNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.ptPlane.SetSize(200.0, 200.0)
                self.ptPlane.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)  # Blue
                self.ptPlane.GetDisplayNode().SetOpacity(0.3)
                self.ptPlane.GetDisplayNode().SetVisibility(True)
                self.ptPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.ptPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # Update status
                self.planesStatusLabel.text.text = "✅ Created INB, NPP, and PTP planes successfully!"
                
            except Exception as e:
                self.planesStatusLabel.text.text = f"❌ Error: {str(e)}"
                import traceback
                traceback.print_exc()
        
        def onCreateMirrorPlanesClicked(self):
            """Create mirror planes following Prokopec-Ubelaker method"""
            try:
                # Update status
                self.mirrorPlanesStatusLabel.text = "Creating mirror planes..."
                slicer.app.processEvents()
                
                # Check prerequisites
                if not hasattr(self, 'inbPlane') or not self.inbPlane:
                    self.mirrorPlanesStatusLabel.text = "Error: Please create reference planes first!"
                    return
                    
                # Get landmarks
                landmarksNode = self.landmarksSelector.currentNode()
                if not landmarksNode:
                    self.mirrorPlanesStatusLabel.text = "Error: Please select landmarks first!"
                    return
                    
                # Get rhinion position
                rhinion_id = -1
                for i in range(landmarksNode.GetNumberOfControlPoints()):
                    label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                    if "rhinion" in label:
                        rhinion_id = i
                        break
                        
                if rhinion_id == -1:
                    self.mirrorPlanesStatusLabel.text = "Error: Rhinion landmark not found!"
                    return
                    
                rhinion_pos = [0, 0, 0]
                landmarksNode.GetNthControlPointPosition(rhinion_id, rhinion_pos)
                
                # Create or get MAW
                mawNode = self.mawSelector.currentNode()
                if not mawNode or mawNode.GetNumberOfControlPoints() < 2:
                    # Create a default MAW
                    pt_normal = [0, 0, 0]
                    self.ptPlane.GetNormal(pt_normal)
                    
                    mawNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "maximum_nasal_width_MAW")
                    
                    left_point = [
                        rhinion_pos[0] + pt_normal[0] * 30.0,
                        rhinion_pos[1] + pt_normal[1] * 30.0,
                        rhinion_pos[2] + pt_normal[2] * 30.0
                    ]
                    
                    right_point = [
                        rhinion_pos[0] - pt_normal[0] * 30.0,
                        rhinion_pos[1] - pt_normal[1] * 30.0,
                        rhinion_pos[2] - pt_normal[2] * 30.0
                    ]
                    
                    # IMPORTANT: Clear any existing points first
                    while mawNode.GetNumberOfControlPoints() > 0:
                        mawNode.RemoveNthControlPoint(0)
                        
                    # Now add our points
                    mawNode.AddControlPoint(vtk.vtkVector3d(left_point))
                    mawNode.AddControlPoint(vtk.vtkVector3d(right_point))
                    
                    self.mawSelector.setCurrentNode(mawNode)
                
                # Get MAW points
                left_point = [0, 0, 0]
                right_point = [0, 0, 0]
                mawNode.GetNthControlPointPosition(0, left_point)
                mawNode.GetNthControlPointPosition(1, right_point)
                
                maw_midpoint = [
                    (left_point[0] + right_point[0]) / 2.0,
                    (left_point[1] + right_point[1]) / 2.0,
                    (left_point[2] + right_point[2]) / 2.0
                ]
                
                # Setup for planes
                num_planes = self.planeCountSlider.value
                
                # Remove old planes
                for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsPlaneNode"):
                    if node.GetName().startswith("Plane_"):
                        slicer.mrmlScene.RemoveNode(node)
                
                self.mirrorPlanes = []
                
                # Get normal for planes
                inb_normal = [0, 0, 0]
                self.inbPlane.GetNormal(inb_normal)
                
                # Calculate distance vector from rhinion to MAW
                rhinion_to_maw = [
                    maw_midpoint[0] - rhinion_pos[0],
                    maw_midpoint[1] - rhinion_pos[1],
                    maw_midpoint[2] - rhinion_pos[2]
                ]
                
                # Calculate the distance
                distance = math.sqrt(
                    rhinion_to_maw[0]**2 + 
                    rhinion_to_maw[1]**2 + 
                    rhinion_to_maw[2]**2
                )
                
                # Normalize the direction vector
                direction = [
                    rhinion_to_maw[0] / distance,
                    rhinion_to_maw[1] / distance,
                    rhinion_to_maw[2] / distance
                ]
                
                # First create Plane_A at MAW position - USING YOUR APPROACH
                planeA = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "Plane_A")
                planeA.SetPlaneType(slicer.vtkMRMLMarkupsPlaneNode.PlaneTypePointNormal)
                # Use SetOrigin directly instead of adding control points
                planeA.SetOrigin(maw_midpoint)
                planeA.SetNormal(inb_normal)
                planeA.SetSize(150.0, 150.0)
                planeA.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                planeA.GetDisplayNode().SetOpacity(0.7)
                self.mirrorPlanes.append(planeA)
                
                # Use letters for naming (B, C, D, etc.)
                plane_names = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                plane_colors = [
                    (0.0, 1.0, 0.0),    # Green
                    (0.0, 0.0, 1.0),    # Blue
                    (1.0, 1.0, 0.0),    # Yellow
                    (1.0, 0.0, 1.0),    # Magenta
                    (0.0, 1.0, 1.0),    # Cyan
                    (1.0, 0.5, 0.0),    # Orange
                    (0.5, 0.0, 1.0),    # Purple
                    (0.0, 0.5, 0.5),    # Teal
                    (0.5, 0.5, 0.0)     # Olive
                ]
                
                # Create evenly spaced planes (B, C, D, etc.)
                for i in range(num_planes - 1):  # -1 because we already created Plane_A
                    fraction = (i + 1) / (num_planes)
                    
                    # Calculate position
                    plane_pos = [
                        rhinion_pos[0] + fraction * distance * direction[0],
                        rhinion_pos[1] + fraction * distance * direction[1],
                        rhinion_pos[2] + fraction * distance * direction[2]
                    ]
                    
                    # Create plane with proper name - USING YOUR APPROACH
                    plane_name = f"Plane_{plane_names[i]}"
                    plane = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", plane_name)
                    plane.SetPlaneType(slicer.vtkMRMLMarkupsPlaneNode.PlaneTypePointNormal)
                    # Use SetOrigin directly instead of adding control points
                    plane.SetOrigin(plane_pos)
                    plane.SetNormal(inb_normal)
                    plane.SetSize(150.0, 150.0)
                    
                    # Use predefined colors
                    if i < len(plane_colors):
                        plane.GetDisplayNode().SetSelectedColor(*plane_colors[i])
                    else:
                        plane.GetDisplayNode().SetSelectedColor(0.8, 0.8, 0.8)
                        
                    plane.GetDisplayNode().SetOpacity(0.7)
                    
                    self.mirrorPlanes.append(plane)
                
                # Show MAW measurement
                maw_distance = self.getMawDistance(mawNode)
                mawNode.SetName(f"maximum_nasal_width_MAW: {maw_distance:.2f}mm")
                
                self.mirrorPlanesStatusLabel.text = f"✅ Created {num_planes} planes (A-{plane_names[num_planes-2]}) successfully!"
                
            except Exception as e:
                self.mirrorPlanesStatusLabel.text = f"❌ Error: {str(e)}"
                import traceback
                traceback.print_exc()
    
            
            
    def onCreateIntersectionsClicked(self):
        """Create intersections following the Prokopec-Ubelaker method"""
        try:
            # Update status
            self.intersectionsStatusLabel.text = "Creating intersections..."
            slicer.app.processEvents()
            
            # Check if we have planes
            if not hasattr(self, 'inbPlane') or not self.inbPlane:
                self.intersectionsStatusLabel.text = "Error: Please create reference planes first!"
                return
                
            if not hasattr(self, 'mirrorPlanes') or not self.mirrorPlanes:
                self.intersectionsStatusLabel.text = "Error: Please create mirror planes first!"
                return
                
            # Get landmarks
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.intersectionsStatusLabel.text = "Error: Please select landmarks first!"
                return
                
            # Find required landmarks
            nasion_id = -1
            prosthion_id = -1
            rhinion_id = -1
            
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                if "nasion" in label:
                    nasion_id = i
                elif "prosthion" in label:
                    prosthion_id = i
                elif "rhinion" in label:
                    rhinion_id = i
                    
            if nasion_id == -1 or prosthion_id == -1 or rhinion_id == -1:
                self.intersectionsStatusLabel.text = "Error: Missing landmarks (nasion, prosthion, or rhinion)!"
                return
                
            # Get landmark positions
            nasion_pos = [0, 0, 0]
            prosthion_pos = [0, 0, 0]
            rhinion_pos = [0, 0, 0]
            
            landmarksNode.GetNthControlPointPosition(nasion_id, nasion_pos)
            landmarksNode.GetNthControlPointPosition(prosthion_id, prosthion_pos)
            landmarksNode.GetNthControlPointPosition(rhinion_id, rhinion_pos)
            
            # Clear existing intersection objects
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsCurveNode"):
                if node.GetName().startswith("Intersection_"):
                    slicer.mrmlScene.RemoveNode(node)
                    
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsLineNode"):
                if node.GetName().startswith("Line_A_") or node.GetName().startswith("Line_B_"):
                    slicer.mrmlScene.RemoveNode(node)
                    
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsFiducialNode"):
                if node.GetName() == "B_Intersection_Points":
                    slicer.mrmlScene.RemoveNode(node)
            
            # Create Line A (nasion to prosthion)
            lineA = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "Line_A_NasionProsthion")
            lineA.AddControlPoint(vtk.vtkVector3d(nasion_pos))
            lineA.AddControlPoint(vtk.vtkVector3d(prosthion_pos))
            lineA.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)  # Yellow
            lineA.GetDisplayNode().SetLineThickness(3.0)  # Make line thicker
            
            # Calculate Line A direction
            lineA_dir = [
                prosthion_pos[0] - nasion_pos[0],
                prosthion_pos[1] - nasion_pos[1],
                prosthion_pos[2] - nasion_pos[2]
            ]
            vtk.vtkMath.Normalize(lineA_dir)
            
            # Create Line B (through rhinion, parallel to Line A)
            # Extend it 100mm in each direction
            lineB_start = [
                rhinion_pos[0] - lineA_dir[0] * 100.0,
                rhinion_pos[1] - lineA_dir[1] * 100.0, 
                rhinion_pos[2] - lineA_dir[2] * 100.0
            ]
            
            lineB_end = [
                rhinion_pos[0] + lineA_dir[0] * 100.0,
                rhinion_pos[1] + lineA_dir[1] * 100.0,
                rhinion_pos[2] + lineA_dir[2] * 100.0
            ]
            
            lineB = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "Line_B_ThroughRhinion")
            lineB.AddControlPoint(vtk.vtkVector3d(lineB_start))
            lineB.AddControlPoint(vtk.vtkVector3d(lineB_end))
            lineB.GetDisplayNode().SetSelectedColor(0.0, 1.0, 1.0)  # Cyan
            lineB.GetDisplayNode().SetLineThickness(3.0)  # Make line thicker
            
            # Store lines for later use
            self.lineA = lineA
            self.lineB = lineB
            
            # Create intersection lines between INB and each mirror plane
            self.intersection_lines = []
            
            # Create node for B intersection points
            b_points = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "B_Intersection_Points")
            
            # Store intersection points
            self.intersection_points = []
            
            # For each mirror plane:
            for i, mirror_plane in enumerate(self.mirrorPlanes):
                # Create intersection with INB plane
                # First get plane positions and normals
                inb_origin = [0, 0, 0]
                inb_normal = [0, 0, 0]
                self.inbPlane.GetOrigin(inb_origin)
                self.inbPlane.GetNormal(inb_normal)
                
                mirror_origin = [0, 0, 0]
                mirror_normal = [0, 0, 0]
                mirror_plane.GetOrigin(mirror_origin)
                mirror_plane.GetNormal(mirror_normal)
                
                # Calculate the direction of the intersection line
                # It's the cross product of the two plane normals
                line_dir = [0, 0, 0]
                vtk.vtkMath.Cross(inb_normal, mirror_normal, line_dir)
                vtk.vtkMath.Normalize(line_dir)
                
                # Find a point on the intersection line
                # This requires solving a system of equations
                # For simplicity, we project a point onto both planes
                
                # Start with the mirror origin
                point_on_line = [
                    mirror_origin[0],
                    mirror_origin[1],
                    mirror_origin[2]
                ]
                
                # Project onto INB plane
                distance = vtk.vtkPlane.DistanceToPlane(
                    point_on_line,
                    inb_normal,
                    inb_origin
                )
                
                point_on_line = [
                    point_on_line[0] - distance * inb_normal[0],
                    point_on_line[1] - distance * inb_normal[1],
                    point_on_line[2] - distance * inb_normal[2]
                ]
                
                # Create the intersection line
                intersection_line = slicer.mrmlScene.AddNewNodeByClass(
                    "vtkMRMLMarkupsLineNode",
                    f"Intersection_INB_Mirror{i+1}"
                )
                
                # Add points to create a 100mm line in each direction
                start_point = [
                    point_on_line[0] - line_dir[0] * 100.0,
                    point_on_line[1] - line_dir[1] * 100.0,
                    point_on_line[2] - line_dir[2] * 100.0
                ]
                
                end_point = [
                    point_on_line[0] + line_dir[0] * 100.0,
                    point_on_line[1] + line_dir[1] * 100.0,
                    point_on_line[2] + line_dir[2] * 100.0
                ]
                
                intersection_line.AddControlPoint(vtk.vtkVector3d(start_point))
                intersection_line.AddControlPoint(vtk.vtkVector3d(end_point))
                
                # Set color to match mirror plane
                color = [0, 0, 0]
                mirror_plane.GetDisplayNode().GetSelectedColor(color)
                intersection_line.GetDisplayNode().SetSelectedColor(color[0], color[1], color[2])
                intersection_line.GetDisplayNode().SetLineThickness(2.0)
                
                # Store line
                self.intersection_lines.append(intersection_line)
                
                # Now find intersection of Line B with this intersection line
                # This is the closest point between two 3D lines
                
                # Line B parameters
                lineB_p1 = lineB_start
                lineB_p2 = lineB_end
                
                # Intersection line parameters
                int_p1 = start_point
                int_p2 = end_point
                
                # Find closest point
                closest_point = self.findClosestPointBetweenLines(lineB_p1, lineB_p2, int_p1, int_p2)
                
                # Add point to collection
                b_points.AddControlPoint(vtk.vtkVector3d(closest_point), f"B{i+1}")
                
                # Store for later use
                self.intersection_points.append(closest_point)
                
            # Update status
            self.intersectionsStatusLabel.text = f"✅ Created all intersections for {len(self.mirrorPlanes)} planes!"
            
        except Exception as e:
            self.intersectionsStatusLabel.text = f"❌ Error: {str(e)}"
            import traceback
            traceback.print_exc()
        
    def findClosestPointBetweenLines(self, line1_p1, line1_p2, line2_p1, line2_p2):
        """Find the closest point between two lines in 3D space"""
        # Direction vectors for both lines
        line1_dir = [
            line1_p2[0] - line1_p1[0],
            line1_p2[1] - line1_p1[1],
            line1_p2[2] - line1_p1[2]
        ]
        
        line2_dir = [
            line2_p2[0] - line2_p1[0],
            line2_p2[1] - line2_p1[1],
            line2_p2[2] - line2_p1[2]
        ]
        
        # Normalize direction vectors
        vtk.vtkMath.Normalize(line1_dir)
        vtk.vtkMath.Normalize(line2_dir)
        
        # Vector connecting the starting points of each line
        r = [
            line1_p1[0] - line2_p1[0],
            line1_p1[1] - line2_p1[1],
            line1_p1[2] - line2_p1[2]
        ]
        
        # Calculate dot products for the system of equations
        a = vtk.vtkMath.Dot(line1_dir, line1_dir)  # Should be 1.0 if normalized
        b = vtk.vtkMath.Dot(line1_dir, line2_dir)
        c = vtk.vtkMath.Dot(line2_dir, line2_dir)  # Should be 1.0 if normalized
        d = vtk.vtkMath.Dot(line1_dir, r)
        e = vtk.vtkMath.Dot(line2_dir, r)
        
        # Calculate parameters for closest points
        denom = a*c - b*b
        
        if abs(denom) < 1e-8:
            # Lines are parallel, just use the midpoint of line1
            return [
                (line1_p1[0] + line1_p2[0]) / 2,
                (line1_p1[1] + line1_p2[1]) / 2,
                (line1_p1[2] + line1_p2[2]) / 2
            ]
        
        t = (b*e - c*d) / denom
        s = (a*e - b*d) / denom
        
        # Calculate closest point on line 1
        closest_point = [
            line1_p1[0] + t * line1_dir[0],
            line1_p1[1] + t * line1_dir[1],
            line1_p1[2] + t * line1_dir[2]
        ]
        
        return closest_point
        
    def onFindLineBIntersectionClicked(self):
        """Find intersection points between intersection lines and Line B"""
        try:
            # Update status
            self.intersectionsStatusLabel.text = "Finding Line B intersections..."
            slicer.app.processEvents()
            
            # Get number of planes
            planeCount = self.planeCountSlider.value
            
            # Check for Line_B
            try:
                lineNode = slicer.util.getNode('Line_B')
            except:
                self.intersectionsStatusLabel.text = "Error: Line_B not found! Please create it first."
                return
            
            # Remove any existing intersection points
            for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
                if node.GetName().startswith('mirrorB_'):
                    slicer.mrmlScene.RemoveNode(node)
            
            # Execute appropriate code based on plane count
            if planeCount == 4:
                # Code for 4 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                    
                # Store intersections for later use
                self.intersection_points = []
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to yellow (RGB: 255, 255, 0)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(1.0, 1.0, 0.0)
                            
                            # Store for later use
                            self.intersection_points.append(intersection_point)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                
            elif planeCount == 5:
                # Code for 5 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                # Store intersections for later use
                self.intersection_points = []
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to yellow (RGB: 255, 255, 0)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(1.0, 1.0, 0.0)
                            
                            # Store for later use
                            self.intersection_points.append(intersection_point)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                
            elif planeCount == 6:
                # Code for 6 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                # Store intersections for later use
                self.intersection_points = []
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to yellow (RGB: 255, 255, 0)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(1.0, 1.0, 0.0)
                            
                            # Store for later use
                            self.intersection_points.append(intersection_point)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
            
            # Update status
            self.intersectionsStatusLabel.text = f"✅ Created {len(self.intersection_points)} Line B intersection points!"
            
        except Exception as e:
            self.intersectionsStatusLabel.text = f"❌ Error finding Line B intersections: {str(e)}"
            import traceback
            traceback.print_exc()
            
    def onFindLineAIntersectionClicked(self):
        """Find intersection points between intersection lines and Line A"""
        try:
            # Update status
            self.intersectionsStatusLabel.text = "Finding Line A intersections..."
            slicer.app.processEvents()
            
            # Get number of planes
            planeCount = self.planeCountSlider.value
            
            # Check for Line_A
            try:
                lineNode = slicer.util.getNode('Line_A')
            except:
                self.intersectionsStatusLabel.text = "Error: Line_A not found! Please create it first."
                return
            
            # Remove any existing intersection points
            for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
                if node.GetName().startswith('mirrorA_'):
                    slicer.mrmlScene.RemoveNode(node)
                    
            # Execute appropriate code based on plane count
            if planeCount == 4:
                # Code for 4 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                    
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                    
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None
                    
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                    
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to turquoise (RGB: 64, 224, 208)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(64/255, 224/255, 208/255)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                        
            elif planeCount == 5:
                # Code for 5 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E']
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1 = np.array(line1Node.GetLineStartPositionWorld())
                    d1 = np.array(line1Node.GetLineEndPositionWorld()) - p1
                    p2 = np.array(line2Node.GetLineStartPositionWorld())
                    d2 = np.array(line2Node.GetLineEndPositionWorld()) - p2
                
                    # Normalize directions
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        print("Lines are parallel")
                        return None  # Lines are parallel
                
                    t = np.dot(np.cross((p2 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to turquoise (RGB: 64, 224, 208)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(64/255, 224/255, 208/255)
                        else:
                            print(f"No intersection found for {line_name}")
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
                        
            elif planeCount == 6:
                # Code for 6 planes
                import numpy as np
                
                lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']
                
                def get_line_points(lineNode):
                    startPoint = np.array([0.0, 0.0, 0.0])
                    endPoint = np.array([0.0, 0.0, 0.0])
                    lineNode.GetNthControlPointPositionWorld(0, startPoint)
                    lineNode.GetNthControlPointPositionWorld(1, endPoint)
                    return startPoint, endPoint
                
                def find_line_intersection(line1Node, line2Node):
                    # Get points and directions of the lines
                    p1, p2 = get_line_points(line1Node)
                    d1 = p2 - p1
                    q1, q2 = get_line_points(line2Node)
                    d2 = q2 - q1
                
                    # Normalize directions
                    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
                        return None  # Avoid division by zero
                    d1 /= np.linalg.norm(d1)
                    d2 /= np.linalg.norm(d2)
                
                    # Calculate intersection
                    cross_d1_d2 = np.cross(d1, d2)
                    if np.linalg.norm(cross_d1_d2) == 0:
                        return None  # Lines are parallel
                
                    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
                    intersection_point = p1 + t * d1
                    return intersection_point
                
                for i, line_name in enumerate(lines):
                    try:
                        line2Node = slicer.util.getNode(line_name)
                        if line2Node is None:
                            print(f"Node {line_name} not found")
                            continue
                        intersection_point = find_line_intersection(lineNode, line2Node)
                        if intersection_point is not None:
                            fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
                            fiducialNode.AddControlPointWorld(intersection_point)
                            # Set the color to turquoise (RGB: 64, 224, 208)
                            displayNode = fiducialNode.GetDisplayNode()
                            displayNode.SetSelectedColor(64/255, 224/255, 208/255)
                    except Exception as e:
                        print(f"Error with {line_name}: {str(e)}")
            
            # Update status
            count = 0
            for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
                if node.GetName().startswith('mirrorA_'):
                    count += 1
            self.intersectionsStatusLabel.text = f"✅ Created {count} Line A intersection points!"
            
        except Exception as e:
            self.intersectionsStatusLabel.text = f"❌ Error finding Line A intersections: {str(e)}"
            import traceback
            traceback.print_exc()
            
    def onDownloadOutlineClicked(self):
        """Download bone outline landmarks based on selected number of planes"""
        try:
            # Update status
            self.bonePointsStatusLabel.text = "Downloading bone outline landmarks..."
            slicer.app.processEvents()
            
            # Get number of planes from slider
            planeCount = self.planeCountSlider.value
            
            # Choose the correct URL based on number of planes
            if planeCount == 4:
                url = "https://github.com/user-attachments/files/19318005/nasal.bone.outline.4.mrk.json"
                filename = "nasal_bone_outline_4.mrk.json"
            elif planeCount == 5:
                url = "https://github.com/user-attachments/files/19318009/nasal.bone.outline.5.mrk.json" 
                filename = "nasal_bone_outline_5.mrk.json"
            elif planeCount == 6:
                url = "https://github.com/user-attachments/files/19318010/nasal.bone.outline.6.mrk.json"
                filename = "nasal_bone_outline_6.mrk.json"
            else:
                self.bonePointsStatusLabel.text = f"Error: No outline file available for {planeCount} planes"
                return
                
            # Create a temporary file to download to
            with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                temp_path = temp_file.name
                
            # Download the file
            urllib.request.urlretrieve(url, temp_path)
            
            # Remove any existing outline points with the same name
            try:
                existingNode = slicer.util.getNode("nasal_bone_outline")
                if existingNode:
                    slicer.mrmlScene.RemoveNode(existingNode)
            except:
                pass
                
            # Load the downloaded file
            outlineNode = slicer.util.loadMarkups(temp_path)
            
            # Rename for clarity
            if outlineNode:
                outlineNode.SetName("nasal_bone_outline")
                self.bonePointsStatusLabel.text = f"✅ Outline landmarks for {planeCount} planes loaded successfully!"
                
                # Switch to Markups module to help with adjusting points
                slicer.util.selectModule('Markups')
                
                # Select the node in the markups module (FIXED LINE)
                slicer.modules.markups.logic().SetActiveListID(outlineNode)
                
                # Show a helpful message
                slicer.util.delayDisplay(
                    f"Landmarks downloaded for {planeCount} planes!\n"
                    "Adjust points if needed from the lateral view", 
                    3000
                )
            else:
                self.bonePointsStatusLabel.text = "❌ Failed to load outline landmarks"
                
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
        except Exception as e:
            self.bonePointsStatusLabel.text = f"❌ Error downloading landmarks: {str(e)}"
            import traceback
            traceback.print_exc()
        
    def onCreateReferencePlanesClicked(self):
            """Create reference planes using the EXACT code provided by the user"""
            try:
                # Update status
                self.planesStatusLabel.text.text = "Creating reference planes..."
                slicer.app.processEvents()
                
                import numpy as np
                
                # === COPY OF YOUR EXACT CODE FOR INB PLANE ===
                # Get the points from the landmarks node (your "hard_tissue_PU")
                hardTissueNode = self.landmarksSelector.currentNode()
                if not hardTissueNode:
                    self.planesStatusLabel.text.text = "Error: Please select landmarks first!"
                    return
                    
                # Get the first three points EXACTLY as in your code
                point1 = np.array(hardTissueNode.GetNthControlPointPosition(0))
                point2 = np.array(hardTissueNode.GetNthControlPointPosition(1))
                point3 = np.array(hardTissueNode.GetNthControlPointPosition(2))

                # Calculate the normal of the plane defined by the three points - EXACTLY as in your code
                v1 = point2 - point1
                v2 = point3 - point1
                planeNormal = np.cross(v1, v2)
                planeNormal = planeNormal / np.linalg.norm(planeNormal)  # Normalize the normal vector

                # Create a new plane node - EXACTLY as in your code
                self.inbPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'INB')

                # Set the origin of the new plane to the first point - EXACTLY as in your code
                self.inbPlane.SetOrigin(point1)

                # Set the normal of the new plane - EXACTLY as in your code
                self.inbPlane.SetNormal(planeNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.inbPlane.SetSize(200.0, 200.0)
                self.inbPlane.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
                self.inbPlane.GetDisplayNode().SetOpacity(0.3)
                self.inbPlane.GetDisplayNode().SetVisibility(True)
                self.inbPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.inbPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR NPP PLANE ===
                # Get the 'INB' plane node - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')

                # Get the coordinates of 'prosthion' and 'nasion' - EXACTLY as in your code
                # Assuming prosthion is point 0 and nasion is point 3 as in your code
                prosthion = np.array(hardTissueNode.GetNthControlPointPositionWorld(0))
                nasion = np.array(hardTissueNode.GetNthControlPointPositionWorld(3))

                # Calculate the normal of the 'INB' plane - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())

                # Calculate the vector between 'prosthion' and 'nasion' - EXACTLY as in your code
                vectorPN = nasion - prosthion

                # Calculate the normal of the new plane - EXACTLY as in your code
                newPlaneNormal = np.cross(inbNormal, vectorPN)
                newPlaneNormal /= np.linalg.norm(newPlaneNormal)  # Normalize the vector

                # Create a new plane node and name it 'NPP' - EXACTLY as in your code
                self.nppPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'NPP')

                # Set the origin of the new plane to 'prosthion' - EXACTLY as in your code
                self.nppPlane.SetOriginWorld(prosthion)

                # Set the normal of the new plane - EXACTLY as in your code
                self.nppPlane.SetNormalWorld(newPlaneNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.nppPlane.SetSize(200.0, 200.0)
                self.nppPlane.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green
                self.nppPlane.GetDisplayNode().SetOpacity(1)
                self.nppPlane.GetDisplayNode().SetVisibility(True)
                self.nppPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.nppPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # === COPY OF YOUR EXACT CODE FOR PTP PLANE ===
                # Get the 'INB' and 'NPP' plane nodes - EXACTLY as in your code
                inbPlaneNode = slicer.util.getNode('INB')
                nppPlaneNode = slicer.util.getNode('NPP')

                # Calculate the normals of the 'INB' and 'NPP' planes - EXACTLY as in your code
                inbNormal = np.array(inbPlaneNode.GetNormalWorld())
                nppNormal = np.array(nppPlaneNode.GetNormalWorld())

                # Calculate the normal of the new plane 'PTP' - EXACTLY as in your code
                ptpNormal = np.cross(inbNormal, nppNormal)
                ptpNormal /= np.linalg.norm(ptpNormal)  # Normalize the vector

                # Create a new plane node and name it 'PTP' - EXACTLY as in your code
                self.ptPlane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'PTP')

                # Set the origin of the new plane to the origin of 'INB' - EXACTLY as in your code
                self.ptPlane.SetOriginWorld(inbPlaneNode.GetOriginWorld())

                # Set the normal of the new plane - EXACTLY as in your code
                self.ptPlane.SetNormalWorld(ptpNormal)
                
                # Add size and color (not in your original code, but helps visibility)
                self.ptPlane.SetSize(200.0, 200.0)
                self.ptPlane.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)  # Blue
                self.ptPlane.GetDisplayNode().SetOpacity(0.3)
                self.ptPlane.GetDisplayNode().SetVisibility(True)
                self.ptPlane.GetDisplayNode().SetSliceIntersectionVisibility(True)
                self.ptPlane.GetDisplayNode().SetHandlesInteractive(True)
                
                # Update status
                self.planesStatusLabel.text.text = "✅ Created INB, NPP, and PTP planes successfully!"
                
            except Exception as e:
                self.planesStatusLabel.text.text = f"❌ Error: {str(e)}"
                import traceback
                traceback.print_exc()
            # Enable export button after measurements are created
            self.exportBoneResultsButton.enabled = True
        
    def onExportBoneResultsClicked(self):
        """Export bone results"""
        self.boneMeasurementsStatusLabel.text = "Exporting bone measurements... (not implemented yet)"
        
    def onGenerateSoftTissueClicked(self):
        """Generate soft tissue predictions"""
        self.softTissueStatusLabel.text = "Generating soft tissue predictions... (not implemented yet)"
        
    def onCopyToClipboardClicked(self):
        """Copy results to clipboard"""
        self.exportStatusLabel.text = "Copying to clipboard... (not implemented yet)"
        
    def onExportResultsClicked(self):
        """Export results to CSV"""
        self.exportStatusLabel.text = "Exporting results... (not implemented yet)"
        
        
    def onCheckLandmarksClicked(self):
        """Check if all required landmarks are detected correctly"""
        try:
            # Get selected landmarks node
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.planesStatusLabel.text = "Error: Please select landmarks first!"
                return
            
            # List all landmarks in the node
            all_labels = []
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i)
                all_labels.append(f"{i}: {label}")
            
            # Check for the required landmarks
            required_landmarks = ["nasion", "inion", "bregma", "prosthion", "subspinale", "rhinion", "acanthion"]
            found_landmarks = {}
            
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                
                # Try exact match first
                if label in [l.lower() for l in required_landmarks]:
                    for req in required_landmarks:
                        if label == req.lower():
                            found_landmarks[req] = i
                            break
                # Then try partial match
                else:
                    for req in required_landmarks:
                        if req.lower() in label or label in req.lower():
                            found_landmarks[req] = i
                            break
            
            # Generate summary
            found_msg = [f"{req}: {'✓ Found' if req in found_landmarks else '❌ Missing'}" for req in required_landmarks]
            
            # Display results in a dialog
            message = qt.QMessageBox()
            message.setWindowTitle("Landmark Check Results")
            message.setText("Required landmark status:")
            message.setInformativeText("\n".join(found_msg))
            message.setDetailedText("All landmarks in the node:\n" + "\n".join(all_labels))
            message.setStandardButtons(qt.QMessageBox.Ok)
            message.exec_()
            
        except Exception as e:
            self.planesStatusLabel.text = f"Error checking landmarks: {str(e)}"

    def onCreateReferencePlanesClicked(self):
        """Create reference planes the simple way"""
        try:
            # Update status
            self.planesStatusLabel.text = "Creating reference planes..."
            slicer.app.processEvents()
            
            import numpy as np
            
            # Get landmarks
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.planesStatusLabel.text = "Error: Please select landmarks!"
                return
            
            # Create brand new plane nodes (delete old ones first)
            for name in ['INB', 'NPP', 'PTP']:
                nodes = slicer.util.getNodes(name + '*')
                for node in nodes:
                    slicer.mrmlScene.RemoveNode(node)
            
            # === INB PLANE ===
            # Just using SetOrigin and SetNormal directly without any control points
            point1 = np.array(landmarksNode.GetNthControlPointPosition(0))
            point2 = np.array(landmarksNode.GetNthControlPointPosition(1))
            point3 = np.array(landmarksNode.GetNthControlPointPosition(2))
            
            v1 = point2 - point1
            v2 = point3 - point1
            inb_normal = np.cross(v1, v2)
            inb_normal = inb_normal / np.linalg.norm(inb_normal)
            
            self.inbPlane = slicer.vtkMRMLMarkupsPlaneNode()
            self.inbPlane.SetName('INB')
            slicer.mrmlScene.AddNode(self.inbPlane)
            self.inbPlane.SetOrigin(point1)
            self.inbPlane.SetNormal(inb_normal)
            
            # Add display properties
            displayNode = slicer.vtkMRMLMarkupsDisplayNode()
            slicer.mrmlScene.AddNode(displayNode)
            self.inbPlane.SetAndObserveDisplayNodeID(displayNode.GetID())
            displayNode.SetSelectedColor(1.0, 0.0, 0.0)  # Red
            displayNode.SetOpacity(1)
            
            # === NPP PLANE ===
            prosthion = np.array(landmarksNode.GetNthControlPointPosition(0))
            nasion = np.array(landmarksNode.GetNthControlPointPosition(3))
            vectorPN = nasion - prosthion
            
            npp_normal = np.cross(inb_normal, vectorPN)
            npp_normal = npp_normal / np.linalg.norm(npp_normal)
            
            self.nppPlane = slicer.vtkMRMLMarkupsPlaneNode()
            self.nppPlane.SetName('NPP')
            slicer.mrmlScene.AddNode(self.nppPlane)
            self.nppPlane.SetOrigin(prosthion)
            self.nppPlane.SetNormal(npp_normal)
            
            # Add display properties
            displayNode = slicer.vtkMRMLMarkupsDisplayNode()
            slicer.mrmlScene.AddNode(displayNode)
            self.nppPlane.SetAndObserveDisplayNodeID(displayNode.GetID())
            displayNode.SetSelectedColor(0.0, 1.0, 0.0)  # Green
            displayNode.SetOpacity(1)
            
            # === PTP PLANE ===
            ptp_normal = np.cross(inb_normal, npp_normal)
            ptp_normal = ptp_normal / np.linalg.norm(ptp_normal)
            
            self.ptPlane = slicer.vtkMRMLMarkupsPlaneNode()
            self.ptPlane.SetName('PTP')
            slicer.mrmlScene.AddNode(self.ptPlane)
            self.ptPlane.SetOrigin(point1)
            self.ptPlane.SetNormal(ptp_normal)
            
            # Add display properties
            displayNode = slicer.vtkMRMLMarkupsDisplayNode()
            slicer.mrmlScene.AddNode(displayNode)
            self.ptPlane.SetAndObserveDisplayNodeID(displayNode.GetID())
            displayNode.SetSelectedColor(0.0, 0.0, 1.0)  # Blue
            displayNode.SetOpacity(1)
            
            # Update status
            self.planesStatusLabel.text = "✅ Created INB, NPP, and PTP planes!"
            
        except Exception as e:
            self.planesStatusLabel.text = f"❌ Error: {str(e)}"
            import traceback
            traceback.print_exc()

    def onCreateMirrorPlanesClicked(self):
        """Create mirror planes using YOUR exact method"""
        try:
            # Update status
            self.mirrorPlanesStatusLabel.text = "Creating mirror planes..."
            slicer.app.processEvents()
            
            import numpy as np
            
            # Check if we have reference planes
            if not hasattr(self, 'ptPlane') or not self.ptPlane:
                self.mirrorPlanesStatusLabel.text = "Error: Please create reference planes first!"
                return
                
            # === USING YOUR EXACT METHOD ===
            
            # Get the PTP plane node (exactly as in your code)
            ptpPlaneNode = self.ptPlane
            
            # Get the MAW node (exactly as in your code)
            mawNode = self.mawSelector.currentNode()
            if not mawNode:
                self.mirrorPlanesStatusLabel.text = "Error: Please select MAW line first!"
                return
            
            # Get MAW position - using midpoint of MAW line
            left_point = np.array(mawNode.GetNthControlPointPositionWorld(0))
            right_point = np.array(mawNode.GetNthControlPointPositionWorld(1))
            mawPosition = (left_point + right_point) / 2
            
            # Get the PTP plane position and normal (exactly as in your code)
            ptpPlanePosition = np.array(ptpPlaneNode.GetOrigin())
            ptpPlaneNormal = np.array(ptpPlaneNode.GetNormal())
            
            # Get landmarks node
            landmarksNode = self.landmarksSelector.currentNode()
            if not landmarksNode:
                self.mirrorPlanesStatusLabel.text = "Error: Please select landmarks first!"
                return
                
            # Get rhinion position (exactly as in your code)
            rhinion_id = -1
            for i in range(landmarksNode.GetNumberOfControlPoints()):
                label = landmarksNode.GetNthControlPointLabel(i).lower().strip()
                if "rhinion" in label:
                    rhinion_id = i
                    break
                    
            if rhinion_id == -1:
                self.mirrorPlanesStatusLabel.text = "Error: Rhinion landmark not found!"
                return
                
            rhinionPosition = np.array(landmarksNode.GetNthControlPointPositionWorld(rhinion_id))
            
            # Remove old planes
            for node in slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsPlaneNode"):
                if node.GetName().startswith("Plane_"):
                    slicer.mrmlScene.RemoveNode(node)
            
            # Create the new plane "A" at the MAW level (exactly as in your code)
            planeA = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'Plane_A')
            planeA.SetOrigin(mawPosition)
            planeA.SetNormal(ptpPlaneNormal)
            planeA.SetSize(150.0, 150.0)
            planeA.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red
            planeA.GetDisplayNode().SetOpacity(0.7)
            
            # Store planes for later use
            self.mirrorPlanes = [planeA]
            
            # Calculate the distance between Plane_A and the rhinion (exactly as in your code)
            distance = np.dot(mawPosition - rhinionPosition, ptpPlaneNormal)
            
            # Get the number of mirror planes from the slider (minus 1 because we already created A)
            numPlanes = self.planeCountSlider.value - 1
            
            # Generate plane names based on number of planes (exactly as in your code)
            planeNames = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'][:numPlanes]
            
            # Calculate the positions for the new planes (exactly using your formula)
            planePositions = [rhinionPosition + (i + 1) * distance / (numPlanes + 1) * ptpPlaneNormal for i in range(numPlanes)]
            
            # Create new planes with names (exactly as in your code)
            for i, pos in enumerate(planePositions):
                planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', f'Plane_{planeNames[i]}')
                planeNode.SetOrigin(pos)
                planeNode.SetNormal(ptpPlaneNormal)
                planeNode.SetSize(150.0, 150.0)
                
                # Add colors for better visibility
                if i == 0:
                    planeNode.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)  # Green
                elif i == 1:
                    planeNode.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)  # Blue
                elif i == 2:
                    planeNode.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)  # Yellow
                else:
                    planeNode.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)  # Orange
                    
                planeNode.GetDisplayNode().SetOpacity(0.7)
                
                # Add to our collection
                self.mirrorPlanes.append(planeNode)
            
            # Display the MAW measurement in the node name
            maw_distance = np.linalg.norm(right_point - left_point)
            mawNode.SetName(f"maximum_nasal_width_MAW: {maw_distance:.2f}mm")
            
            # Update status
            self.mirrorPlanesStatusLabel.text = f"✅ Created {numPlanes+1} planes (A-{planeNames[-1]}) successfully!"
            
        except Exception as e:
            self.mirrorPlanesStatusLabel.text = f"❌ Error: {str(e)}"
            import traceback
            traceback.print_exc()
            
    def onCreateIntersectionLinesClicked(self):
        """Create intersection lines between planes"""
        try:
            # Update status
            self.intersectionLinesStatusLabel.text = "Creating intersection lines..."
            slicer.app.processEvents()
            
            import numpy as np
            
            # Check for required planes
            if not slicer.util.getNode('INB'):
                self.intersectionLinesStatusLabel.text = "Error: INB plane not found! Create reference planes first."
                return
                
            # Get number of mirror planes from UI to determine how many intersection lines to create
            planeCount = self.planeCountSlider.value if hasattr(self, 'planeCountSlider') else 6
            
            # Clear any existing intersection lines
            for lineName in ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']:
                try:
                    node = slicer.util.getNode(lineName)
                    if node:
                        slicer.mrmlScene.RemoveNode(node)
                except:
                    pass
            
            # YOUR EXACT CODE FOR CREATING INTERSECTION LINES
            # Function to create intersection line between two planes
            def create_intersection_line(planeNode1, planeNode2, lineNodeName):
                # Create a new line node for the intersection line
                intersectionLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', lineNodeName)

                # Get the normal vectors and points on the planes
                normal1 = np.array(planeNode1.GetNormalWorld())
                point1 = np.array(planeNode1.GetOriginWorld())
                normal2 = np.array(planeNode2.GetNormalWorld())
                point2 = np.array(planeNode2.GetOriginWorld())

                # Calculate the direction vector of the intersection line
                direction = np.cross(normal1, normal2)

                # Check if the planes are parallel
                if np.linalg.norm(direction) == 0:
                    print(f"The planes {planeNode1.GetName()} and {planeNode2.GetName()} are parallel and do not intersect.")
                    return False
                else:
                    # Calculate a point on the intersection line
                    A = np.array([normal1, normal2, direction])
                    b = np.array([np.dot(normal1, point1), np.dot(normal2, point2), 0])
                    intersection_point = np.linalg.solve(A, b)

                    # Define the start and end points of the line, extending further
                    extension_factor = 1000  # Adjust this factor as needed
                    start_point = intersection_point - extension_factor * direction
                    end_point = intersection_point + extension_factor * direction

                    # Set the points in the line node
                    intersectionLineNode.AddControlPointWorld(start_point)
                    intersectionLineNode.AddControlPointWorld(end_point)

                    print(f"Extended intersection line {lineNodeName} created successfully.")
                    return True

            # List of plane pairs and corresponding line node names
            plane_pairs = []
            planeNames = ['A', 'B', 'C', 'D', 'E', 'F'][:planeCount]
            for planeName in planeNames:
                plane_pairs.append(('INB', f'Plane_{planeName}', f'INB_{planeName}'))
                
            # Counter for successful lines
            successCount = 0

            # Iterate over each pair and create the intersection lines
            for plane1, plane2, lineName in plane_pairs:
                try:
                    planeNode1 = slicer.util.getNode(plane1)
                    planeNode2 = slicer.util.getNode(plane2)
                    if create_intersection_line(planeNode1, planeNode2, lineName):
                        successCount += 1
                        
                        # Add color to the line
                        lineNode = slicer.util.getNode(lineName)
                        lineNode.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)  # Orange
                        lineNode.GetDisplayNode().SetLineWidth(0.3)  
                        
                except Exception as e:
                    print(f"Error creating line {lineName}: {str(e)}")
            
            # Update status
            self.intersectionLinesStatusLabel.text = f"✅ Created {successCount} intersection lines successfully!"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.intersectionLinesStatusLabel.text = f"❌ Error: {str(e)}"

    def onCreateLinesABClicked(self):
        """Create reference lines A and B"""
        try:
            # Update status
            self.linesABStatusLabel.text = "Creating lines A and B..."
            slicer.app.processEvents()
            
            # Clear any existing lines A and B
            for lineName in ['Line_A', 'Line_B']:
                try:
                    node = slicer.util.getNode(lineName)
                    if node:
                        slicer.mrmlScene.RemoveNode(node)
                except:
                    pass
            
            # YOUR EXACT CODE FOR CREATING LINES A AND B
            import vtk
            
            # Get the "hard_tissue_PU" node (using your landmarks selector instead)
            F = self.landmarksSelector.currentNode()
            if not F:
                self.linesABStatusLabel.text = "Error: Please select landmarks first!"
                return
                
            # Create the first line node
            L_A = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'Line_A')

            # Retrieve and add the first point (position 0)
            firstPoint = F.GetNthControlPointPositionVector(0)
            L_A.AddControlPoint(firstPoint)

            # Retrieve and add the second point (position 3)
            secondPoint = F.GetNthControlPointPositionVector(3)
            L_A.AddControlPoint(secondPoint)
            
            # Set display properties
            L_A.GetDisplayNode().SetSelectedColor(0.0, 1.0, 1.0)  # Cyan
            L_A.GetDisplayNode().SetLineWidth(0.3)  

            # Retrieve the point at position 5
            thirdPoint = F.GetNthControlPointPositionVector(5)

            # Calculate the direction vector of the first line
            directionVector = vtk.vtkVector3d()
            directionVector.SetX(secondPoint.GetX() - firstPoint.GetX())
            directionVector.SetY(secondPoint.GetY() - firstPoint.GetY())
            directionVector.SetZ(secondPoint.GetZ() - firstPoint.GetZ())

            # Create the second line node
            L_B = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'Line_B')

            # Add the third point (position 5)
            L_B.AddControlPoint(thirdPoint)

            # Extend the direction vector by a factor (e.g., 2 for doubling the length)
            factor = 2
            extendedDirectionVector = vtk.vtkVector3d()
            extendedDirectionVector.SetX(directionVector.GetX() * factor)
            extendedDirectionVector.SetY(directionVector.GetY() * factor)
            extendedDirectionVector.SetZ(directionVector.GetZ() * factor)

            # Calculate and add the fourth point (extended)
            fourthPoint = vtk.vtkVector3d()
            fourthPoint.SetX(thirdPoint.GetX() + extendedDirectionVector.GetX())
            fourthPoint.SetY(thirdPoint.GetY() + extendedDirectionVector.GetY())
            fourthPoint.SetZ(thirdPoint.GetZ() + extendedDirectionVector.GetZ())
            L_B.AddControlPoint(fourthPoint)
            
            # Set display properties
            L_B.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)  # Yellow
            L_B.GetDisplayNode().SetLineWidth(0.3)  
            
            # Update status
            self.linesABStatusLabel.text = "✅ Lines A and B created successfully!"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.linesABStatusLabel.text = f"❌ Error: {str(e)}"

# Create an instance of the GUI
nasal_gui = ProkopecUbelakerGUI()
nasal_gui.setWindowTitle("Prokopec-Ubelaker Nasal Prediction")
nasal_gui.show()
