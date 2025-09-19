```python
# A beginner-friendly GUI for the Prokopec-Ubelaker nasal prediction method
# This version is corrected for 3D Slicer 5.8.1 and includes the user-requested MSP plane feature and all UI/logic fixes.
# Just copy-paste this entire script into 3D Slicer's Python console!

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import math
import csv
import requests

class ProkopecUbelakerGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.mainLayout = qt.QVBoxLayout(self)
        
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        self.helperNodes = []
        self.helpersVisible = True
        self.activeProfilePlaneName = "INB" # Default to INB
        
        self.createStepWidgets()
        self.setupNavigation()
        
        self.currentStep = 0
        self.updateStepUI()
        
    def setupNavigation(self):
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.setMaximumWidth(120)
        navLayout.addWidget(self.prevButton)
        self.prevButton.connect('clicked(bool)', self.onPrevButtonClicked)
        
        self.stepLabel = qt.QLabel("Step 1/9")
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        navLayout.addWidget(self.stepLabel)
        
        self.nextButton = qt.QPushButton("Next")
        self.nextButton.setMaximumWidth(120)
        navLayout.addWidget(self.nextButton)
        self.nextButton.connect('clicked(bool)', self.onNextButtonClicked)
        
        self.mainLayout.addWidget(navWidget)
        
    def onPrevButtonClicked(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()
            
    def onNextButtonClicked(self):
        if self.currentStep == 6:
            self.onStepCompleted()
        elif self.currentStep < self.stepStack.count - 1:
            self.currentStep += 1
            self.updateStepUI()

    def onStepCompleted(self):
        messageBox = qt.QMessageBox()
        messageBox.setIcon(qt.QMessageBox.Question)
        messageBox.setWindowTitle("Continue to Soft Tissue Comparison?")
        messageBox.setText("Step 7 is complete. Do you want to proceed to Step 8 to compare your predictions with true soft tissue?")
        messageBox.setInformativeText("This is optional. If not, you can proceed to the final results step.")
        
        compareButton = messageBox.addButton("Yes, Compare", qt.QMessageBox.YesRole)
        resultsButton = messageBox.addButton("No, Go to Results", qt.QMessageBox.NoRole)
        messageBox.setDefaultButton(resultsButton)
        
        messageBox.exec_()
        
        if messageBox.clickedButton() == compareButton:
            self.currentStep += 1
        else:
            self.currentStep = 8
            
        self.updateStepUI()

    def cleanupScene(self, plane_count):
        suffix = f"_{plane_count}p"
        prefixes_to_delete = [
            "Plane_", "INB_", "MSP_", "Line_A", "Line_B", "mirrorB_", "mirrorA_",
            "nasal_bone_outline", "nasal outline", "bone", "nasalboneto",
            "pred soft nose outline", "pred error", "nose_profile_outline"
        ]
        
        nodes_to_remove = []
        all_nodes = slicer.mrmlScene.GetNodes()
        for i in range(all_nodes.GetNumberOfItems()):
            node = all_nodes.GetItemAsObject(i)
            if not node: continue
            node_name = node.GetName()
            for prefix in prefixes_to_delete:
                if node_name.startswith(prefix):
                    nodes_to_remove.append(node)
                    break
        
        if nodes_to_remove:
            print(f"Cleaning up {len(set(nodes_to_remove))} old items...")
            with slicer.util.tryWithErrorDisplay("Failed to clean up scene."):
                slicer.mrmlScene.StartState(slicer.mrmlScene.BatchProcessState)
                for node in list(set(nodes_to_remove)):
                    if node in slicer.mrmlScene.GetNodes():
                        slicer.mrmlScene.RemoveNode(node)
                slicer.mrmlScene.EndState(slicer.mrmlScene.BatchProcessState)
        
        self.helperNodes = []

    def createStepWidgets(self):
        self.createStep1Widget()
        self.createStep2Widget()
        self.createStep3Widget()
        self.createStep4Widget()
        self.createStep5Widget()
        self.createStep6Widget()
        self.createStep7Widget()
        self.createStep8Widget()
        self.createStep9Widget()

    def createStep1Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Welcome to the Prokopec-Ubelaker Nasal Prediction Tool!")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        desc = qt.QLabel("This interactive tool will guide you through the nasal prediction method step-by-step.\nYou can go back to previous steps to change parameters (like the number of planes) and re-run the analysis.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        self.stepStack.addWidget(widget)

    def createStep2Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 2: Hard Tissue Landmark Selection")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        detailLabel = qt.QLabel("Please select or load your hard tissue landmarks. The next step will explain which landmarks are required for each calculation method.")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        self.landmarksSelector = slicer.qMRMLNodeComboBox()
        self.landmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.landmarksSelector.selectNodeUponCreation = True
        self.landmarksSelector.addEnabled = True
        self.landmarksSelector.removeEnabled = True
        self.landmarksSelector.noneEnabled = True
        self.landmarksSelector.setMRMLScene(slicer.mrmlScene)
        selectorLayout.addRow("Hard Tissue Landmarks:", self.landmarksSelector)
        layout.addWidget(selectorFrame)
        
        self.loadLandmarksButton = qt.QPushButton("Load From File")
        layout.addWidget(self.loadLandmarksButton)
        
        self.landmarksStatusLabel = qt.QLabel("Please select or load landmarks.")
        self.landmarksStatusLabel.setWordWrap(True)
        layout.addWidget(self.landmarksStatusLabel)
        
        self.loadLandmarksButton.connect('clicked(bool)', self.onLoadLandmarksClicked)
        self.stepStack.addWidget(widget)

    def createStep3Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 3: Reference Plane Creation")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        planeInfoLabel = qt.QLabel()
        planeInfoLabel.setTextFormat(qt.Qt.RichText) # This is the fix for the bold tag
        planeInfoLabel.setText("The method for creating the profile plane determines which landmarks are required:<br>• <b>INB plane:</b> nasion, inion, bregma<br>• <b>MSP (best fit):</b> nasion, prosthion, subspinale, rhinion, acanthion")
        planeInfoLabel.setWordWrap(True)
        layout.addWidget(planeInfoLabel)
        
        self.checkLandmarksButton = qt.QPushButton("1. Check Landmarks")
        layout.addWidget(self.checkLandmarksButton)
        
        self.planeChoiceWidget = qt.QWidget()
        planeChoiceLayout = qt.QFormLayout(self.planeChoiceWidget)
        self.planeChoiceComboBox = qt.QComboBox()
        self.planeChoiceComboBox.addItems([
            "Select a method...",
            "INB plane (nasion, inion, bregma)",
            "MSP (best fit midsagittal plane)"
        ])
        planeChoiceLayout.addRow("2. Choose Profile Plane:", self.planeChoiceComboBox)
        layout.addWidget(self.planeChoiceWidget)
        self.planeChoiceWidget.setVisible(False)

        self.createReferencePlanesButton = qt.QPushButton("3. Create / Update Reference Planes")
        layout.addWidget(self.createReferencePlanesButton)
        self.createReferencePlanesButton.setEnabled(False)

        self.planesStatusLabel = qt.QLabel("Ready to create reference planes.")
        self.planesStatusLabel.setWordWrap(True)
        layout.addWidget(self.planesStatusLabel)
        
        self.checkLandmarksButton.connect('clicked(bool)', self.onCheckLandmarksClicked)
        self.planeChoiceComboBox.connect('currentIndexChanged(int)', self.onPlaneChoiceChanged)
        self.createReferencePlanesButton.connect('clicked(bool)', self.onCreateReferencePlanesClicked)
        self.stepStack.addWidget(widget)

    def createStep4Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 4: Mirror Plane Configuration")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        detailLabel = qt.QLabel("Choose the number of mirror planes (4, 5, or 6). This will clean up items from any previous run with the same number of planes.")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        self.mawSelector = slicer.qMRMLNodeComboBox()
        self.mawSelector.nodeTypes = ["vtkMRMLMarkupsLineNode"]
        self.mawSelector.addEnabled = True
        self.mawSelector.noneEnabled = True
        self.mawSelector.setMRMLScene(slicer.mrmlScene)
        selectorLayout.addRow("Maximum Aperture Width:", self.mawSelector)
        self.planeCountSlider = qt.QSlider(qt.Qt.Horizontal)
        self.planeCountSlider.minimum = 4
        self.planeCountSlider.maximum = 6
        self.planeCountSlider.value = 5
        self.planeCountSlider.setTickPosition(qt.QSlider.TicksBelow)
        self.planeCountSlider.setTickInterval(1)
        self.planeCountLabel = qt.QLabel(f"Number of mirror planes: {self.planeCountSlider.value}")
        selectorLayout.addRow(self.planeCountLabel, self.planeCountSlider)
        layout.addWidget(selectorFrame)
        self.createMirrorPlanesButton = qt.QPushButton("Create Mirror Planes")
        layout.addWidget(self.createMirrorPlanesButton)
        self.mirrorPlanesStatusLabel = qt.QLabel("Ready to create mirror planes.")
        self.mirrorPlanesStatusLabel.setWordWrap(True)
        layout.addWidget(self.mirrorPlanesStatusLabel)
        self.planeCountSlider.connect('valueChanged(int)', self.onPlaneCountChanged)
        self.createMirrorPlanesButton.connect('clicked(bool)', self.onCreateMirrorPlanesClicked)
        self.stepStack.addWidget(widget)

    def createStep5Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 5: Create Intersection Lines and Points")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        group1 = qt.QGroupBox("1. Create Intersection Lines")
        groupLayout1 = qt.QVBoxLayout(group1)
        self.createIntersectionLinesButton = qt.QPushButton("Create ProfilePlane-Mirror Intersection Lines")
        groupLayout1.addWidget(self.createIntersectionLinesButton)
        self.intersectionLinesStatusLabel = qt.QLabel("Status: Waiting")
        groupLayout1.addWidget(self.intersectionLinesStatusLabel)
        layout.addWidget(group1)
        group2 = qt.QGroupBox("2. Create Reference Lines A & B")
        groupLayout2 = qt.QVBoxLayout(group2)
        self.createLinesABButton = qt.QPushButton("Create Lines A and B")
        groupLayout2.addWidget(self.createLinesABButton)
        self.linesABStatusLabel = qt.QLabel("Status: Waiting")
        groupLayout2.addWidget(self.linesABStatusLabel)
        layout.addWidget(group2)
        group3 = qt.QGroupBox("3. Find Intersection Points")
        groupLayout3 = qt.QVBoxLayout(group3)
        self.lineAIntersectionButton = qt.QPushButton("Find Intersections on Line A")
        groupLayout3.addWidget(self.lineAIntersectionButton)
        self.lineBIntersectionButton = qt.QPushButton("Find Intersections on Line B")
        groupLayout3.addWidget(self.lineBIntersectionButton)
        self.intersectionsStatusLabel = qt.QLabel("Status: Waiting")
        groupLayout3.addWidget(self.intersectionsStatusLabel)
        layout.addWidget(group3)
        self.createIntersectionLinesButton.connect('clicked(bool)', self.onCreateIntersectionLinesClicked)
        self.createLinesABButton.connect('clicked(bool)', self.onCreateLinesABClicked)
        self.lineAIntersectionButton.connect('clicked(bool)', self.onFindLineAIntersectionClicked)
        self.lineBIntersectionButton.connect('clicked(bool)', self.onFindLineBIntersectionClicked)
        self.stepStack.addWidget(widget)

    def createStep6Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 6: Nasal Aperture Outline Setup")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        detailLabel = qt.QLabel("Download the nasal bone outline landmarks. After downloading, you MUST adjust the point positions to match your skull from a lateral (side) view.")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        self.downloadOutlineButton = qt.QPushButton("Download Aperture Outline Landmarks")
        layout.addWidget(self.downloadOutlineButton)
        self.bonePointsStatusLabel = qt.QLabel("Ready to download.")
        self.bonePointsStatusLabel.setWordWrap(True)
        layout.addWidget(self.bonePointsStatusLabel)
        
        self.toggleVisibilityButton6 = qt.QPushButton("Toggle Helper Visibility")
        layout.addWidget(self.toggleVisibilityButton6)
        
        self.confirmationLabel = qt.QLabel("Important: After adjusting, click 'Next' to proceed.")
        self.confirmationLabel.setStyleSheet("color: orange; font-weight: bold;")
        self.confirmationLabel.setWordWrap(True)
        layout.addWidget(self.confirmationLabel)
        self.downloadOutlineButton.connect('clicked(bool)', self.onDownloadNasalBoneOutlineClicked)
        self.toggleVisibilityButton6.connect('clicked(bool)', self.onToggleVisibilityClicked)
        self.stepStack.addWidget(widget)

    def createStep7Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 7: Generate Nasal Prediction")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        group1 = qt.QGroupBox("1. Process Bone Outline")
        groupLayout1 = qt.QVBoxLayout(group1)
        self.connectOutlinesButton = qt.QPushButton("Connect Outline Points")
        groupLayout1.addWidget(self.connectOutlinesButton)
        self.findBoneIntersectionsButton = qt.QPushButton("Find Bone Intersection Points")
        groupLayout1.addWidget(self.findBoneIntersectionsButton)
        layout.addWidget(group1)
        group2 = qt.QGroupBox("2. Create Predictions")
        groupLayout2 = qt.QVBoxLayout(group2)
        self.createMirrorPredictionButton = qt.QPushButton("Create Mirrored Prediction (No Soft Tissue)")
        groupLayout2.addWidget(self.createMirrorPredictionButton)
        self.create2mmPredictionButton = qt.QPushButton("Create Prediction with 2mm FSTT")
        groupLayout2.addWidget(self.create2mmPredictionButton)
        customFSTTLayout = qt.QHBoxLayout()
        self.createCustomPredictionButton = qt.QPushButton("Create Prediction with Custom FSTT:")
        self.customFSTTSpinBox = qt.QDoubleSpinBox()
        self.customFSTTSpinBox.value = 3.0
        self.customFSTTSpinBox.singleStep = 0.5
        customFSTTLayout.addWidget(self.createCustomPredictionButton)
        customFSTTLayout.addWidget(self.customFSTTSpinBox)
        groupLayout2.addLayout(customFSTTLayout)
        layout.addWidget(group2)

        self.toggleVisibilityButton7 = qt.QPushButton("Toggle Helper Visibility")
        layout.addWidget(self.toggleVisibilityButton7)

        self.predictionStatusLabel = qt.QLabel("Ready to create predictions.")
        self.predictionStatusLabel.setWordWrap(True)
        layout.addWidget(self.predictionStatusLabel)
        self.connectOutlinesButton.connect('clicked(bool)', self.onConnectOutlinesClicked)
        self.findBoneIntersectionsButton.connect('clicked(bool)', self.onFindBoneIntersectionsClicked)
        self.createMirrorPredictionButton.connect('clicked(bool)', self.onCreateMirrorPredictionClicked)
        self.create2mmPredictionButton.connect('clicked(bool)', self.onCreate2mmPredictionClicked)
        self.createCustomPredictionButton.connect('clicked(bool)', self.onCreateCustomPredictionClicked)
        self.toggleVisibilityButton7.connect('clicked(bool)', self.onToggleVisibilityClicked)
        self.stepStack.addWidget(widget)

    def createStep8Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 8: Compare with True Soft Tissue (Optional)")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        detailLabel = qt.QLabel("To measure prediction accuracy, download the true soft tissue landmarks, adjust them, and then create error measurements.")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        self.downloadTrueSoftTissueButton = qt.QPushButton("1. Download True Soft Tissue Landmarks")
        layout.addWidget(self.downloadTrueSoftTissueButton)
        self.adjustTrueSoftTissueButton = qt.QPushButton("2. Adjust True Soft Tissue to Lines")
        layout.addWidget(self.adjustTrueSoftTissueButton)
        self.createErrorsButton = qt.QPushButton("3. Create All Error Measurements")
        layout.addWidget(self.createErrorsButton)
        self.softTissueStatusLabel = qt.QLabel("Ready for comparison.")
        self.softTissueStatusLabel.setWordWrap(True)
        layout.addWidget(self.softTissueStatusLabel)
        self.downloadTrueSoftTissueButton.connect('clicked(bool)', self.onDownloadSoftTissueOutlineClicked)
        self.adjustTrueSoftTissueButton.connect('clicked(bool)', self.onAdjustTrueSoftTissueClicked)
        self.createErrorsButton.connect('clicked(bool)', self.onCreateErrorsClicked)
        self.stepStack.addWidget(widget)

    def createStep9Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 9: Results Analysis")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        detailLabel = qt.QLabel("Review the measurements in the table below. You can copy the data to the clipboard or export it as a CSV file.")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable.setColumnCount(4)
        self.measurementsTable.setHorizontalHeaderLabels(["Prediction Type", "Measurement Name", "Value (mm)", "Error (mm)"])
        layout.addWidget(self.measurementsTable)
        exportButtonLayout = qt.QHBoxLayout()
        self.copyToClipboardButton = qt.QPushButton("Copy to Clipboard")
        self.exportResultsButton = qt.QPushButton("Export Results to CSV")
        exportButtonLayout.addWidget(self.copyToClipboardButton)
        exportButtonLayout.addWidget(self.exportResultsButton)
        layout.addLayout(exportButtonLayout)
        self.exportStatusLabel = qt.QLabel("Ready to export results.")
        self.exportStatusLabel.setWordWrap(True)
        layout.addWidget(self.exportStatusLabel)
        completionLabel = qt.QLabel("Congratulations! You've completed the prediction process.")
        completionLabel.setStyleSheet("font-weight: bold; color: green;")
        layout.addWidget(completionLabel)
        self.copyToClipboardButton.connect('clicked(bool)', self.onCopyToClipboardClicked)
        self.exportResultsButton.connect('clicked(bool)', self.onExportResultsClicked)
        self.stepStack.addWidget(widget)

    def updateStepUI(self):
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)
        if self.currentStep == 8:
            self.populateResultsTable()

    def onToggleVisibilityClicked(self):
        self.helpersVisible = not self.helpersVisible
        plane_name_part = self.activeProfilePlaneName
        for node in self.helperNodes:
            if not (node and node in slicer.mrmlScene.GetNodes()):
                continue
            if node.GetName().startswith(f"{plane_name_part}_"):
                node.SetDisplayVisibility(True)
            else:
                node.SetDisplayVisibility(self.helpersVisible)
        status = "shown" if self.helpersVisible else "hidden"
        slicer.util.delayDisplay(f"Helper nodes {status}. {plane_name_part} lines remain visible.", 500)

    def onLoadLandmarksClicked(self):
        fileName, _ = qt.QFileDialog.getOpenFileName(self, "Load Landmarks", "", "Markup Files (*.mrk.json)")
        if fileName:
            landmarksNode = slicer.util.loadMarkups(fileName)
            if landmarksNode:
                self.landmarksSelector.setCurrentNode(landmarksNode)
                self.landmarksStatusLabel.setText(f"Loaded {landmarksNode.GetName()} successfully!")
            else:
                self.landmarksStatusLabel.setText("Failed to load landmarks from file.")

    def onCheckLandmarksClicked(self):
        landmarksNode = self.landmarksSelector.currentNode()
        if not landmarksNode:
            self.planesStatusLabel.setText("Error: Please select landmarks first!")
            return
        
        required = ["nasion", "inion", "bregma", "prosthion", "subspinale", "rhinion", "acanthion"]
        found = {req: False for req in required}
        for i in range(landmarksNode.GetNumberOfControlPoints()):
            label = landmarksNode.GetNthControlPointLabel(i).lower()
            for req in required:
                if req in label:
                    found[req] = True
        
        summary = "\n".join([f"• {req}: {'✓ Found' if found[req] else '✗ Missing'}" for req in required])
        qt.QMessageBox.information(self, "Landmark Check", f"Landmark Status:\n{summary}")
        
        self.planeChoiceWidget.setVisible(True)
        self.planeChoiceComboBox.setCurrentIndex(0)
        self.createReferencePlanesButton.setEnabled(False)
        self.planesStatusLabel.setText("Please choose a plane creation method.")

    def onPlaneChoiceChanged(self, index):
        if index > 0:
            self.createReferencePlanesButton.setEnabled(True)
            self.planesStatusLabel.setText("Ready to create planes.")
        else:
            self.createReferencePlanesButton.setEnabled(False)
            self.planesStatusLabel.setText("Please choose a plane creation method.")

    def onCreateReferencePlanesClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to create reference planes."):
            choice_index = self.planeChoiceComboBox.currentIndex
            if choice_index == 0:
                self.planesStatusLabel.setText("Error: Please select a plane creation method first.")
                return

            self.planesStatusLabel.setText("Processing reference planes...")
            slicer.app.processEvents()
            hardTissueNode = self.landmarksSelector.currentNode()
            if not hardTissueNode:
                self.planesStatusLabel.setText("Error: Select landmarks first.")
                return

            def get_positions(node, required_landmarks):
                positions = {}
                for name in required_landmarks:
                    for i in range(node.GetNumberOfControlPoints()):
                        if name in node.GetNthControlPointLabel(i).lower():
                            positions[name] = np.array(node.GetNthControlPointPosition(i))
                            break
                if len(positions) < len(required_landmarks):
                    missing = [name for name in required_landmarks if name not in positions]
                    raise ValueError(f"Missing key landmarks: {', '.join(missing)}")
                return positions

            def create_or_update_plane(name, origin, normal, color):
                try:
                    planeNode = slicer.util.getNode(name)
                except slicer.util.MRMLNodeNotFoundException:
                    planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode')
                planeNode.SetName(name)
                planeNode.SetOrigin(origin)
                planeNode.SetNormal(normal)
                planeNode.SetSize(450, 450)
                planeNode.GetDisplayNode().SetSelectedColor(*color)
                planeNode.GetDisplayNode().SetOpacity(0.3)
                return planeNode
            
            profile_plane = None
            if choice_index == 1: # INB Plane
                self.activeProfilePlaneName = "INB"
                required = ["inion", "nasion", "bregma"]
                positions = get_positions(hardTissueNode, required)
                v1 = positions['nasion'] - positions['inion']
                v2 = positions['bregma'] - positions['inion']
                profile_normal = np.cross(v1, v2)
                profile_normal /= np.linalg.norm(profile_normal)
                profile_plane = create_or_update_plane('INB', positions['inion'], profile_normal, (1,0,0))
            
            elif choice_index == 2: # MSP Plane
                self.activeProfilePlaneName = "MSP"
                required = ["nasion", "prosthion", "subspinale", "rhinion", "acanthion"]
                positions = get_positions(hardTissueNode, required)
                points = np.array(list(positions.values()))
                
                centroid = np.mean(points, axis=0)
                centered_points = points - centroid
                covariance_matrix = np.cov(centered_points, rowvar=False)
                eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
                
                profile_normal = eigenvectors[:, np.argmin(eigenvalues)]
                profile_plane = create_or_update_plane('MSP', centroid, profile_normal, (1,0.5,0))

            if profile_plane:
                nasion_pos = get_positions(hardTissueNode, ["nasion"])["nasion"]
                prosthion_pos = get_positions(hardTissueNode, ["prosthion"])["prosthion"]
                
                vectorPN = nasion_pos - prosthion_pos
                npp_normal = np.cross(np.array(profile_plane.GetNormal()), vectorPN)
                npp_normal /= np.linalg.norm(npp_normal)
                create_or_update_plane('NPP', prosthion_pos, npp_normal, (0,1,0))
                
                ptp_normal = np.cross(np.array(profile_plane.GetNormal()), npp_normal)
                ptp_normal /= np.linalg.norm(ptp_normal)
                create_or_update_plane('PTP', nasion_pos, ptp_normal, (0,0,1))
                
                self.planesStatusLabel.setText(f"{self.activeProfilePlaneName}, NPP, and PTP planes created/updated.")
            else:
                self.planesStatusLabel.setText("Failed to create the primary profile plane.")

    def onPlaneCountChanged(self, value):
        self.planeCountLabel.setText(f"Number of mirror planes: {value}")

    def onCreateMirrorPlanesClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to create mirror planes."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.mirrorPlanesStatusLabel.setText(f"Creating {plane_count} mirror planes...")
            slicer.app.processEvents()
            self.cleanupScene(plane_count)
            try:
                ptp_plane = slicer.util.getNode('PTP')
            except slicer.util.MRMLNodeNotFoundException:
                self.mirrorPlanesStatusLabel.setText("Error: Create reference planes first.")
                return
            landmarks_node = self.landmarksSelector.currentNode()
            if not landmarks_node:
                self.mirrorPlanesStatusLabel.setText("Error: Select landmarks first.")
                return
            rhinion_pos = None
            for i in range(landmarks_node.GetNumberOfControlPoints()):
                if "rhinion" in landmarks_node.GetNthControlPointLabel(i).lower():
                    rhinion_pos = np.array(landmarks_node.GetNthControlPointPosition(i))
                    break
            if rhinion_pos is None:
                self.mirrorPlanesStatusLabel.setText("Error: Rhinion landmark not found.")
                return
            maw_node = self.mawSelector.currentNode()
            if not maw_node or maw_node.GetNumberOfControlPoints() < 2:
                self.mirrorPlanesStatusLabel.setText("Error: Please define the Maximum Aperture Width line.")
                return
            p1 = np.array([0,0,0]); maw_node.GetNthControlPointPosition(0, p1)
            p2 = np.array([0,0,0]); maw_node.GetNthControlPointPosition(1, p2)
            maw_midpoint = (p1 + p2) / 2.0
            ptp_normal = np.array(ptp_plane.GetNormal())
            vector_to_maw = maw_midpoint - rhinion_pos
            dist = np.dot(vector_to_maw, ptp_normal)
            self.mirrorPlanes = []
            plane_letters = [chr(65 + i) for i in range(plane_count)]
            for i, letter in enumerate(plane_letters):
                fraction = (plane_count - 1 - i) / (plane_count - 1) if plane_count > 1 else 0
                plane_pos = rhinion_pos + fraction * dist * ptp_normal
                plane = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", f"Plane_{letter}{suffix}")
                plane.SetOrigin(plane_pos)
                plane.SetNormal(ptp_normal)
                plane.SetSize(150, 150)
                plane.GetDisplayNode().SetOpacity(0.4)
                self.mirrorPlanes.append(plane)
                self.helperNodes.append(plane)
            self.mirrorPlanesStatusLabel.setText(f"Created {plane_count} mirror planes.")

    def onCreateIntersectionLinesClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to create intersection lines."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.intersectionLinesStatusLabel.setText("Creating intersection lines...")
            slicer.app.processEvents()

            try:
                profile_plane = slicer.util.getNode(self.activeProfilePlaneName)
                landmarks_node = self.landmarksSelector.currentNode()
                if not landmarks_node:
                    raise slicer.util.MRMLNodeNotFoundException("Landmarks not selected")
                
                positions = {}
                for name in ["inion", "rhinion"]:
                    try:
                        for i in range(landmarks_node.GetNumberOfControlPoints()):
                            if name in landmarks_node.GetNthControlPointLabel(i).lower():
                                positions[name] = np.array(landmarks_node.GetNthControlPointPosition(i))
                                break
                    except:
                        pass
                if "rhinion" not in positions:
                     raise slicer.util.MRMLNodeNotFoundException("Rhinion not found")
                
                anatomical_anterior_vector = positions.get('rhinion', [1,0,0]) - positions.get('inion', [0,0,0])

            except slicer.util.MRMLNodeNotFoundException as e:
                self.intersectionLinesStatusLabel.setText(f"Error: Prerequisite missing - {e}")
                return

            def intersect_planes(p1_node, p2_node, line_name):
                n1, o1 = np.array(p1_node.GetNormal()), np.array(p1_node.GetOrigin())
                n2, o2 = np.array(p2_node.GetNormal()), np.array(p2_node.GetOrigin())
                
                direction = np.cross(n1, n2)
                if np.linalg.norm(direction) < 1e-6: return None

                if np.dot(direction, anatomical_anterior_vector) < 0:
                    direction = -direction
                
                direction /= np.linalg.norm(direction)
                
                A = np.array([n1, n2, direction])
                b = np.array([np.dot(n1, o1), np.dot(n2, o2), np.dot(direction, o1)])
                try:
                    point = np.linalg.solve(A, b)
                except np.linalg.LinAlgError: return None
                
                line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', line_name)
                line_node.AddControlPoint(point)
                line_node.AddControlPoint(point + 300 * direction)
                line_node.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)
                return line_node

            count = 0
            for i in range(plane_count):
                letter = chr(65 + i)
                try:
                    mirror_plane = slicer.util.getNode(f"Plane_{letter}{suffix}")
                    line_name = f"{self.activeProfilePlaneName}_{letter}{suffix}"
                    line_node = intersect_planes(profile_plane, mirror_plane, line_name)
                    if line_node:
                        count += 1
                        self.helperNodes.append(line_node)
                except slicer.util.MRMLNodeNotFoundException:
                    print(f"Could not find mirror plane Plane_{letter}{suffix} to create intersection line.")
                    continue
            self.intersectionLinesStatusLabel.setText(f"Created {count} intersection lines.")

    def onCreateLinesABClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to create lines A and B."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.linesABStatusLabel.setText("Creating Lines A and B...")
            slicer.app.processEvents()
            landmarks_node = self.landmarksSelector.currentNode()
            if not landmarks_node:
                self.linesABStatusLabel.setText("Error: Select landmarks first.")
                return
            pos = {}
            for name in ["prosthion", "nasion", "rhinion"]:
                for i in range(landmarks_node.GetNumberOfControlPoints()):
                    if name in landmarks_node.GetNthControlPointLabel(i).lower():
                        pos[name] = np.array(landmarks_node.GetNthControlPointPosition(i))
                        break
            if len(pos) < 3:
                self.linesABStatusLabel.setText("Error: Missing prosthion, nasion, or rhinion.")
                return
            line_a = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"Line_A{suffix}")
            line_a.AddControlPoint(pos['prosthion'])
            line_a.AddControlPoint(pos['nasion'])
            line_a.GetDisplayNode().SetSelectedColor(0.0, 1.0, 1.0)
            self.helperNodes.append(line_a)

            direction = pos['nasion'] - pos['prosthion']
            direction /= np.linalg.norm(direction)
            line_b = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"Line_B{suffix}")
            line_b.AddControlPoint(pos['rhinion'] - 150 * direction)
            line_b.AddControlPoint(pos['rhinion'] + 150 * direction)
            line_b.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)
            self.helperNodes.append(line_b)
            self.linesABStatusLabel.setText("Lines A and B created.")

    def onFindLineAIntersectionClicked(self):
        self.find_line_intersections("Line_A", "mirrorA", color=(0.25, 0.88, 0.82))

    def onFindLineBIntersectionClicked(self):
        self.find_line_intersections("Line_B", "mirrorB", color=(1.0, 1.0, 0.0))

    def find_line_intersections(self, target_line_name, point_prefix, color):
        with slicer.util.tryWithErrorDisplay(f"Failed to find intersections on {target_line_name}."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.intersectionsStatusLabel.setText(f"Finding intersections on {target_line_name}...")
            slicer.app.processEvents()
            
            try:
                target_line = slicer.util.getNode(f"{target_line_name}{suffix}")
            except slicer.util.MRMLNodeNotFoundException:
                self.intersectionsStatusLabel.setText(f"Error: {target_line_name}{suffix} not found.")
                return

            p1 = np.array(target_line.GetNthControlPointPosition(0))
            p2 = np.array(target_line.GetNthControlPointPosition(1))
            
            count = 0
            for i in range(plane_count):
                letter = chr(65 + i)
                try:
                    intersecting_line = slicer.util.getNode(f"{self.activeProfilePlaneName}_{letter}{suffix}")
                    
                    q1 = np.array(intersecting_line.GetNthControlPointPosition(0))
                    q2 = np.array(intersecting_line.GetNthControlPointPosition(1))

                    t = vtk.mutable(0)
                    u = vtk.mutable(0)
                    
                    vtk.vtkLine.Intersection(p1, p2, q1, q2, t, u)
                    
                    intersection_point = p1 + t.get() * (p2 - p1)
                    
                    point_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f"{point_prefix}_{letter}{suffix}")
                    point_node.AddControlPoint(intersection_point)
                    point_node.GetDisplayNode().SetSelectedColor(color)
                    count += 1
                    self.helperNodes.append(point_node)

                except slicer.util.MRMLNodeNotFoundException:
                    print(f"Warning: Could not find {self.activeProfilePlaneName}_{letter}{suffix} to calculate intersection.")
                    continue
                except Exception as e:
                    print(f"An error occurred during intersection calculation for {self.activeProfilePlaneName}_{letter}{suffix}: {e}")
                    continue
                    
            self.intersectionsStatusLabel.setText(f"Found {count} intersections on {target_line_name}.")
        
    def onDownloadNasalBoneOutlineClicked(self):
        urls = {
            4: "https://github.com/user-attachments/files/19318005/nasal.bone.outline.4.mrk.json",
            5: "https://github.com/user-attachments/files/19318009/nasal.bone.outline.5.mrk.json",
            6: "https://github.com/user-attachments/files/19318010/nasal.bone.outline.6.mrk.json"
        }
        self.download_and_load_markup("nasal_bone_outline", self.bonePointsStatusLabel, urls)

    def onDownloadSoftTissueOutlineClicked(self):
        urls = {
            4: "https://github.com/user-attachments/files/19327865/nose.profile.outline.4.mrk.json",
            5: "https://github.com/user-attachments/files/19327866/nose.profile.outline.5.mrk.json",
            6: "https://github.com/user-attachments/files/19327871/nose.profile.outline.6.mrk.json"
        }
        self.download_and_load_markup("nose_profile_outline", self.softTissueStatusLabel, urls)

    def download_and_load_markup(self, node_name_base, status_label, url_map):
        with slicer.util.tryWithErrorDisplay(f"Failed to download {node_name_base}."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            node_name = f"{node_name_base}{suffix}"
            status_label.setText("Downloading landmarks...")
            slicer.app.processEvents()
            
            if plane_count not in url_map:
                status_label.setText("No file for this plane count.")
                return
                
            try:
                old_node = slicer.util.getNode(node_name)
                slicer.mrmlScene.RemoveNode(old_node)
            except slicer.util.MRMLNodeNotFoundException:
                pass
                
            try:
                response = requests.get(url_map[plane_count])
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name
                    
                outlineNode = slicer.util.loadMarkups(temp_file_path)
                os.unlink(temp_file_path)
                
                if outlineNode:
                    outlineNode.SetName(node_name)
                    status_label.setText(f"Landmarks loaded. Please adjust positions if needed.")
                    slicer.modules.markups.logic().SetActiveListID(outlineNode)
                    slicer.util.selectModule('Markups')
                    self.helperNodes.append(outlineNode)
                else:
                    status_label.setText("Failed to load landmarks from downloaded file.")
            except Exception as e:
                status_label.setText(f"Error: {str(e)}")

    def onConnectOutlinesClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to connect outlines."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.predictionStatusLabel.setText("Connecting outline points...")
            slicer.app.processEvents()
            try:
                outline_node = slicer.util.getNode(f"nasal_bone_outline{suffix}")
            except slicer.util.MRMLNodeNotFoundException:
                self.predictionStatusLabel.setText("Error: Nasal bone outline not found.")
                return
                
            if outline_node.GetNumberOfControlPoints() < plane_count * 2:
                self.predictionStatusLabel.setText(f"Error: Not enough outline points.")
                return
                
            points = [np.array(outline_node.GetNthControlPointPosition(i)) for i in range(outline_node.GetNumberOfControlPoints())]
            count = 0
            for i in range(plane_count):
                line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"nasal outline{i+1}{suffix}")
                line_node.AddControlPoint(points[i])
                line_node.AddControlPoint(points[i + plane_count])
                line_node.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)
                count += 1
                self.helperNodes.append(line_node)
            self.predictionStatusLabel.setText(f"Connected {count} outline lines.")

    def onFindBoneIntersectionsClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to find bone intersections."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.predictionStatusLabel.setText("Finding bone intersections...")
            slicer.app.processEvents()

            profile_lines = []
            for i in range(plane_count):
                letter = chr(65 + i)
                try:
                    line = slicer.util.getNode(f"{self.activeProfilePlaneName}_{letter}{suffix}")
                    profile_lines.append(line)
                except slicer.util.MRMLNodeNotFoundException:
                    self.predictionStatusLabel.setText(f"Error: Profile line {self.activeProfilePlaneName}_{letter}{suffix} not found.")
                    return
            
            profile_lines.reverse()

            count = 0
            for i in range(plane_count):
                try:
                    outline_line = slicer.util.getNode(f"nasal outline{i+1}{suffix}")
                    paired_profile_line = profile_lines[i]

                    p1 = np.array(outline_line.GetNthControlPointPosition(0))
                    p2 = np.array(outline_line.GetNthControlPointPosition(1))
                    q1 = np.array(paired_profile_line.GetNthControlPointPosition(0))
                    q2 = np.array(paired_profile_line.GetNthControlPointPosition(1))
                    
                    t = vtk.mutable(0)
                    u = vtk.mutable(0)
                    vtk.vtkLine.Intersection(p1, p2, q1, q2, t, u)
                    
                    intersection_point = p1 + t.get() * (p2 - p1)

                    point_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f"bone{i+1}{suffix}")
                    point_node.AddControlPoint(intersection_point)
                    point_node.GetDisplayNode().SetSelectedColor(1.0, 0.0, 1.0)
                    count += 1
                    self.helperNodes.append(point_node)
                except (slicer.util.MRMLNodeNotFoundException, IndexError) as e:
                    print(f"Warning: Could not create bone intersection {i+1}. {e}")
                    continue
            self.predictionStatusLabel.setText(f"Found {count} correct bone intersection points.")

    def create_prediction(self, fstt_value, pred_name_base, color):
        with slicer.util.tryWithErrorDisplay(f"Failed to create {pred_name_base} prediction."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.predictionStatusLabel.setText(f"Creating prediction: {pred_name_base}...")
            slicer.app.processEvents()
            count = 0
            for i in range(plane_count):
                letter = chr(65 + i)
                bone_point_index = plane_count - i
                try:
                    mirror_point_node = slicer.util.getNode(f"mirrorB_{letter}{suffix}")
                    bone_point_node = slicer.util.getNode(f"bone{bone_point_index}{suffix}")
                    profile_line_node = slicer.util.getNode(f"{self.activeProfilePlaneName}_{letter}{suffix}")
                    
                    mirror_pos = np.array(mirror_point_node.GetNthControlPointPosition(0))
                    bone_pos = np.array(bone_point_node.GetNthControlPointPosition(0))
                    measurement_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"nasalbonetoB{i+1}{suffix}")
                    measurement_line.AddControlPoint(mirror_pos)
                    measurement_line.AddControlPoint(bone_pos)
                    measurement_line.GetDisplayNode().SetSelectedColor(0.8, 0.6, 1.0)
                    self.helperNodes.append(measurement_line)

                    length = np.linalg.norm(bone_pos - mirror_pos)
                    p1 = np.array(profile_line_node.GetNthControlPointPosition(0))
                    p2 = np.array(profile_line_node.GetNthControlPointPosition(1))
                    direction = (p2 - p1) / np.linalg.norm(p2 - p1)
                    end_point = mirror_pos + (length + fstt_value) * direction
                    
                    pred_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"{pred_name_base}{i+1}{suffix}")
                    pred_line.AddControlPoint(mirror_pos)
                    pred_line.AddControlPoint(end_point)
                    pred_line.GetDisplayNode().SetSelectedColor(color)
                    count += 1
                    self.helperNodes.append(pred_line)
                except (slicer.util.MRMLNodeNotFoundException, IndexError) as e:
                    print(f"Warning: Could not find node for prediction {i+1}: {e}")
                    continue
            self.predictionStatusLabel.setText(f"Created {count} {pred_name_base} predictions correctly.")

    def onCreateMirrorPredictionClicked(self):
        self.create_prediction(0.0, "pred soft nose outline ", (0.3, 0.0, 0.5))

    def onCreate2mmPredictionClicked(self):
        self.create_prediction(2.0, "pred soft nose outline 2mm ", (0.85, 0.0, 0.85))

    def onCreateCustomPredictionClicked(self):
        custom_fstt = self.customFSTTSpinBox.value
        self.create_prediction(custom_fstt, f"pred soft nose outline custom{custom_fstt}mm ", (0.0, 0.7, 0.9))

    def onAdjustTrueSoftTissueClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to adjust soft tissue points."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.softTissueStatusLabel.setText("Adjusting points to corresponding lines...")
            slicer.app.processEvents()

            try:
                soft_tissue_node = slicer.util.getNode(f"nose_profile_outline{suffix}")
            except slicer.util.MRMLNodeNotFoundException:
                self.softTissueStatusLabel.setText("Error: True soft tissue outline not found.")
                return
                
            if soft_tissue_node.GetNumberOfControlPoints() < plane_count:
                self.softTissueStatusLabel.setText(f"Error: Not enough points (need {plane_count}).")
                return

            profile_lines = []
            for i in range(plane_count):
                letter = chr(65 + i)
                try:
                    line = slicer.util.getNode(f"{self.activeProfilePlaneName}_{letter}{suffix}")
                    profile_lines.append(line)
                except slicer.util.MRMLNodeNotFoundException:
                    continue
            
            if len(profile_lines) < plane_count:
                self.softTissueStatusLabel.setText(f"Error: Not enough {self.activeProfilePlaneName} lines found.")
                return

            profile_lines.reverse()
                
            adjust_count = 0
            for i in range(min(soft_tissue_node.GetNumberOfControlPoints(), len(profile_lines))):
                point_pos = np.array(soft_tissue_node.GetNthControlPointPosition(i))
                line = profile_lines[i]
                
                p1 = np.array(line.GetNthControlPointPosition(0))
                p2 = np.array(line.GetNthControlPointPosition(1))
                
                line_vec = p2 - p1
                point_vec = point_pos - p1
                line_vec_norm = line_vec / np.linalg.norm(line_vec)
                
                projection_length = np.dot(point_vec, line_vec_norm)
                adjusted_pos = p1 + projection_length * line_vec_norm
                
                soft_tissue_node.SetNthControlPointPosition(i, *adjusted_pos)
                adjust_count += 1
            
            self.softTissueStatusLabel.setText(f"Adjusted {adjust_count} points to lines correctly.")

    # --- THIS IS THE CORRECTED FUNCTION ---
    def onCreateErrorsClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to create error measurements."):
            plane_count = self.planeCountSlider.value
            suffix = f"_{plane_count}p"
            self.softTissueStatusLabel.setText("Creating error measurements...")
            slicer.app.processEvents()
            
            try:
                soft_tissue_node = slicer.util.getNode(f"nose_profile_outline{suffix}")
            except slicer.util.MRMLNodeNotFoundException:
                self.softTissueStatusLabel.setText("Error: True soft tissue outline not found.")
                return

            if soft_tissue_node.GetNumberOfControlPoints() < plane_count:
                self.softTissueStatusLabel.setText("Error: True soft tissue outline has too few points.")
                return

            error_count = 0
            for i in range(plane_count):
                # True soft tissue points are 0, 1, 2... (top to bottom)
                true_point_index = i
                
                # Prediction lines are 1, 2, 3... (bottom to top)
                # We need to pair true point 0 with prediction 'plane_count'
                prediction_node_index = plane_count - i

                try:
                    true_point_pos = np.array(soft_tissue_node.GetNthControlPointPosition(true_point_index))

                    # This will find all prediction types (mirror, 2mm, custom) for the correctly paired index
                    pred_nodes = slicer.util.getNodes(f"pred soft nose outline *{prediction_node_index}{suffix}")

                    for pred_node_name, pred_node in pred_nodes.items():
                        pred_endpoint_pos = np.array(pred_node.GetNthControlPointPosition(1))
                        
                        # The error line corresponds to the true point number (i+1)
                        error_line_name = f"pred error{true_point_index+1}{suffix}"
                        
                        error_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', error_line_name)
                        error_line.AddControlPoint(pred_endpoint_pos)
                        error_line.AddControlPoint(true_point_pos)
                        error_line.GetDisplayNode().SetSelectedColor(0.8, 0.1, 0.1)
                        error_line.SetLocked(True)
                        error_count += 1
                        self.helperNodes.append(error_line)

                except Exception as e:
                    print(f"Could not create error line for true point {true_point_index+1}: {e}")
                        
            self.softTissueStatusLabel.setText(f"Created {error_count} error measurement lines correctly.")
            self.populateResultsTable()

    def populateResultsTable(self):
        self.measurementsTable.setRowCount(0)
        plane_count = self.planeCountSlider.value
        suffix = f"_{plane_count}p"
        
        all_nodes = []
        for prefix in ['nasalboneto', 'pred soft nose outline', 'pred error']:
            nodes = slicer.util.getNodes(f'{prefix}*{suffix}')
            all_nodes.extend(nodes.values())

        row = 0
        processed_names = set()

        for node in all_nodes:
            name = node.GetName()
            if name in processed_names: continue
            
            length = np.linalg.norm(np.array(node.GetNthControlPointPosition(1)) - np.array(node.GetNthControlPointPosition(0)))

            self.measurementsTable.insertRow(row)
            base_name = name.replace(suffix, '')
            
            self.measurementsTable.setItem(row, 1, qt.QTableWidgetItem(base_name))
            
            if name.startswith('pred error'):
                self.measurementsTable.setItem(row, 0, qt.QTableWidgetItem("error"))
                self.measurementsTable.setItem(row, 3, qt.QTableWidgetItem(f"{length:.2f}"))
            elif name.startswith('pred soft nose outline'):
                self.measurementsTable.setItem(row, 0, qt.QTableWidgetItem("prediction"))
                self.measurementsTable.setItem(row, 2, qt.QTableWidgetItem(f"{length:.2f}"))
                
                try:
                    num_str = ''.join(filter(str.isdigit, base_name.split(" ")[-1]))
                    if not num_str: continue

                    # Find the corresponding error line
                    # The prediction number is the 'flipped' index, we need the 'true' index
                    pred_num = int(num_str)
                    true_num = plane_count - pred_num + 1

                    error_node_name = f"pred error{true_num}{suffix}"
                    error_node = slicer.util.getNode(error_node_name)
                    error_length = np.linalg.norm(np.array(error_node.GetNthControlPointPosition(1)) - np.array(error_node.GetNthControlPointPosition(0)))
                    self.measurementsTable.setItem(row, 3, qt.QTableWidgetItem(f"{error_length:.2f}"))
                except Exception as e:
                    print(f"Could not find matching error for {name}: {e}")
                    pass
            else:
                self.measurementsTable.setItem(row, 0, qt.QTableWidgetItem("measurement"))
                self.measurementsTable.setItem(row, 2, qt.QTableWidgetItem(f"{length:.2f}"))

            processed_names.add(name)
            row += 1
            
        self.measurementsTable.resizeColumnsToContents()

    def onCopyToClipboardClicked(self):
        clipboard = qt.QApplication.clipboard()
        header = "\t".join([self.measurementsTable.horizontalHeaderItem(i).text() for i in range(self.measurementsTable.columnCount)])
        table_text = header + "\n"
        for row in range(self.measurementsTable.rowCount):
            row_data = [self.measurementsTable.item(row, col).text() if self.measurementsTable.item(row, col) else "" for col in range(self.measurementsTable.columnCount)]
            table_text += "\t".join(row_data) + "\n"
        clipboard.setText(table_text)
        self.exportStatusLabel.setText("Results copied to clipboard.")

    def onExportResultsClicked(self):
        fileName, _ = qt.QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if fileName:
            with slicer.util.tryWithErrorDisplay("Failed to export results."):
                with open(fileName, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([self.measurementsTable.horizontalHeaderItem(i).text() for i in range(self.measurementsTable.columnCount)])
                    for row in range(self.measurementsTable.rowCount):
                        row_data = [self.measurementsTable.item(row, col).text() if self.measurementsTable.item(row, col) else "" for col in range(self.measurementsTable.columnCount)]
                        writer.writerow(row_data)
                self.exportStatusLabel.setText(f"Results exported to {os.path.basename(fileName)}.")

# --- This part runs the GUI ---
if not hasattr(slicer, 'ProkopecUbelakerGUIWidget') or not slicer.ProkopecUbelakerGUIWidget.isVisible():
    if hasattr(slicer, 'ProkopecUbelakerGUIWidget'):
        slicer.ProkopecUbelakerGUIWidget.delete()
    slicer.ProkopecUbelakerGUIWidget = ProkopecUbelakerGUI()
    slicer.ProkopecUbelakerGUIWidget.setWindowTitle("Prokopec-Ubelaker Nasal Prediction")

slicer.ProkopecUbelakerGUIWidget.show()
slicer.ProkopecUbelakerGUIWidget.raise_()
```
