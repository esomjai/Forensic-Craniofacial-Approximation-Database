```python

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
        
        self.colorPalette = [
            (0.0, 0.8, 0.8),  # Teal
            (0.0, 1.0, 0.0),  # Green
            (1.0, 1.0, 0.0),  # Yellow
            (1.0, 0.5, 0.0),  # Orange
            (1.0, 0.0, 0.0),  # Red
            (1.0, 0.0, 1.0)   # Magenta
        ]
        
        self.createStepWidgets()
        self.setupNavigation()
        
        self.currentStep = 0
        self.updateStepUI()
        
    def get_plane_count(self):
        """Get current plane count from slider"""
        return int(self.planeCountSlider.value)
    
    def get_run_label(self):
        """Get and sanitize run label (replace spaces, remove special chars)"""
        # For now, just return empty string since we don't have run labels yet
        return ""
    
    def get_suffix(self):
        """Combined suffix: plane count + optional run label"""
        pc = self.get_plane_count()
        run = self.get_run_label()
        if run:
            return f"_{pc}p_{run}"
        else:
            return f"_{pc}p"
        
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
        
    def addImageFromGitHub(self, layout, imageName, width=400, height=300):
        """Helper function to add educational images from GitHub"""
        imageLabel = qt.QLabel()
        imageLabel.setAlignment(qt.Qt.AlignCenter)
        imageLabel.setContentsMargins(0, 5, 0, 5)
        baseUrl = "https://raw.githubusercontent.com/esomjai/Forensic-Craniofacial-Approximation-Database/basics/Nose%20predictions/images/"
        imageUrl = baseUrl + imageName
        try:
            imageData = urllib.request.urlopen(imageUrl).read()
            pixmap = qt.QPixmap()
            pixmap.loadFromData(imageData)
            imageLabel.setPixmap(pixmap.scaled(width, height, qt.Qt.KeepAspectRatio, qt.Qt.SmoothTransformation))
            layout.addWidget(imageLabel)
            return True
        except Exception as e:
            print(f"Could not load image {imageName}: {e}")
            return False

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
        
        detailLabel = qt.QLabel("Please select your hard tissue landmarks, load them from a file, or download the list.")
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
        
        buttonLayout = qt.QHBoxLayout()
        
        self.loadLandmarksButton = qt.QPushButton("Load From File")
        buttonLayout.addWidget(self.loadLandmarksButton)
        
        self.downloadDemoLandmarksButton = qt.QPushButton("Download Landmarks")
        buttonLayout.addWidget(self.downloadDemoLandmarksButton)
        
        layout.addLayout(buttonLayout)
        
        self.landmarksStatusLabel = qt.QLabel("Please select or load landmarks.")
        self.landmarksStatusLabel.setWordWrap(True)
        layout.addWidget(self.landmarksStatusLabel)
        
        self.loadLandmarksButton.connect('clicked(bool)', self.onLoadLandmarksClicked)
        self.downloadDemoLandmarksButton.connect('clicked(bool)', self.onDownloadHardTissueClicked)
        self.stepStack.addWidget(widget)

    def createStep3Widget(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        title = qt.QLabel("Step 3: Reference Plane Creation")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        planeInfoLabel = qt.QLabel()
        planeInfoLabel.setTextFormat(qt.Qt.RichText)
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
        
        detailLabel = qt.QLabel("First, define the Maximum Aperture Width (MAW) by creating a line. Then, choose the number of mirror planes (4, 5, or 6).")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        
        mawLayout = qt.QHBoxLayout()
        self.mawSelector = slicer.qMRMLNodeComboBox()
        self.mawSelector.nodeTypes = ["vtkMRMLMarkupsLineNode"]
        self.mawSelector.addEnabled = False
        self.mawSelector.removeEnabled = True
        self.mawSelector.noneEnabled = True
        self.mawSelector.setMRMLScene(slicer.mrmlScene)
        mawLayout.addWidget(self.mawSelector)
        
        self.createMAWButton = qt.QPushButton("Create MAW Line")
        mawLayout.addWidget(self.createMAWButton)
        
        selectorLayout.addRow("Maximum Aperture Width:", mawLayout)
        
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
        
        self.createMAWButton.connect('clicked(bool)', self.onCreateMAWClicked)
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
        
        detailLabel = qt.QLabel("Select existing nasal bone outline landmarks OR download new ones. After downloading/selecting, you MUST adjust the point positions to match your skull from a lateral (side/profile) view.\n\nPlace points according to their sides (L - left, R - right), with L1 the most superior on the left.")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # ADD SELECTOR (like in Step 2 and Step 4!)
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        self.nasalBoneOutlineSelector = slicer.qMRMLNodeComboBox()
        self.nasalBoneOutlineSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.nasalBoneOutlineSelector.addEnabled = True
        self.nasalBoneOutlineSelector.removeEnabled = True
        self.nasalBoneOutlineSelector.noneEnabled = True
        self.nasalBoneOutlineSelector.setMRMLScene(slicer.mrmlScene)
        selectorLayout.addRow("Nasal Bone Outline:", self.nasalBoneOutlineSelector)
        layout.addWidget(selectorFrame)
        
        self.downloadOutlineButton = qt.QPushButton("Download Aperture Outline Landmarks")
        layout.addWidget(self.downloadOutlineButton)
        
        self.bonePointsStatusLabel = qt.QLabel("Select existing landmarks or download new ones.")
        self.bonePointsStatusLabel.setWordWrap(True)
        layout.addWidget(self.bonePointsStatusLabel)
        
        # Image container (shown after download)
        self.step6ImageContainer = qt.QWidget()
        self.step6ImageLayout = qt.QVBoxLayout(self.step6ImageContainer)
        self.step6ImageContainer.setVisible(False)
        layout.addWidget(self.step6ImageContainer)
        
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
        
        detailLabel = qt.QLabel("To measure prediction accuracy:\n1) Select existing soft tissue landmarks OR download new ones\n2) Place them on the soft tissue nose (point '1' most superior)\n3) Optionally adjust them to snap to lines\n4) Choose which prediction to compare\n5) Create error measurements")
        detailLabel.setWordWrap(True)
        layout.addWidget(detailLabel)
        
        # ADD SELECTOR (like in Step 2 and Step 4!)
        selectorFrame = qt.QFrame()
        selectorLayout = qt.QFormLayout(selectorFrame)
        self.softTissueOutlineSelector = slicer.qMRMLNodeComboBox()
        self.softTissueOutlineSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.softTissueOutlineSelector.addEnabled = True
        self.softTissueOutlineSelector.removeEnabled = True
        self.softTissueOutlineSelector.noneEnabled = True
        self.softTissueOutlineSelector.setMRMLScene(slicer.mrmlScene)
        selectorLayout.addRow("True Soft Tissue Outline:", self.softTissueOutlineSelector)
        layout.addWidget(selectorFrame)
        
        self.downloadTrueSoftTissueButton = qt.QPushButton("1. Download True Soft Tissue Landmarks")
        layout.addWidget(self.downloadTrueSoftTissueButton)
        
        self.addImageFromGitHub(layout, "8.1.png", width=400, height=280)
        
        self.adjustTrueSoftTissueButton = qt.QPushButton("2. Adjust True Soft Tissue to Lines")
        layout.addWidget(self.adjustTrueSoftTissueButton)
        
        predictionSelectionFrame = qt.QFrame()
        predictionSelectionLayout = qt.QFormLayout(predictionSelectionFrame)
        self.predictionTypeComboBox = qt.QComboBox()
        self.predictionTypeComboBox.addItems([
            "Select prediction type to compare...",
            "Mirrored (no soft tissue)",
            "2mm soft tissue",
            "Custom soft tissue"
        ])
        predictionSelectionLayout.addRow("3a. Choose Prediction Type:", self.predictionTypeComboBox)
        layout.addWidget(predictionSelectionFrame)
        
        self.createErrorsButton = qt.QPushButton("3b. Create Error Measurements for Selected Prediction")
        layout.addWidget(self.createErrorsButton)
        
        self.softTissueStatusLabel = qt.QLabel("Select existing landmarks or download new ones.")
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

    def onDownloadHardTissueClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to download landmarks."):
            url = "https://github.com/user-attachments/files/22872691/hard_tissue_PU.mrk.json"
            node_name = "hard_tissue_PU"
            self.landmarksStatusLabel.setText("Downloading landmarks...")
            slicer.app.processEvents()

            try:
                old_node = slicer.util.getNode(node_name)
                slicer.mrmlScene.RemoveNode(old_node)
            except slicer.util.MRMLNodeNotFoundException:
                pass

            try:
                response = requests.get(url)
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name
                    
                landmarksNode = slicer.util.loadMarkups(temp_file_path)
                os.unlink(temp_file_path)
                
                if landmarksNode:
                    landmarksNode.SetName(node_name)
                    self.landmarksSelector.setCurrentNode(landmarksNode)
                    self.landmarksStatusLabel.setText(f"Loaded '{node_name}' successfully!")
                else:
                    self.landmarksStatusLabel.setText("Failed to load landmarks from downloaded file.")
            except Exception as e:
                self.landmarksStatusLabel.setText(f"Error: {str(e)}")

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

    def onCopyToClipboardClicked(self):
        try:
            table = self.measurementsTable
            if not table:
                self.exportStatusLabel.setText("Results table not found.")
                return

            clipboard = qt.QApplication.clipboard()
            if not clipboard:
                self.exportStatusLabel.setText("Clipboard not available.")
                return
            
            headers = [table.horizontalHeaderItem(c).text() for c in range(table.columnCount)]
            data = "\t".join(headers) + "\n"

            for r in range(table.rowCount):
                row_items = []
                for c in range(table.columnCount):
                    item = table.item(r, c)
                    row_items.append(item.text() if item else "")
                data += "\t".join(row_items) + "\n"
            
            clipboard.setText(data)
            self.exportStatusLabel.setText("Results copied to clipboard!")

        except Exception as e:
            self.exportStatusLabel.setText(f"Error copying: {e}")
            slicer.util.errorDisplay(f"Could not copy to clipboard: {e}")

    def onExportResultsClicked(self):
        try:
            table = self.measurementsTable
            if not table:
                self.exportStatusLabel.setText("Results table not found.")
                return

            # Ask user for a file path to save the CSV
            file_path, _ = qt.QFileDialog.getSaveFileName(self, "Export Results as CSV", "", "CSV Files (*.csv)")
            if not file_path:
                self.exportStatusLabel.setText("Export canceled.")
                return

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                headers = [table.horizontalHeaderItem(c).text() for c in range(table.columnCount)]
                writer.writerow(headers)
                
                # Write data rows
                for r in range(table.rowCount):
                    row_items = []
                    for c in range(table.columnCount):
                        item = table.item(r, c)
                        row_items.append(item.text() if item else "")
                    writer.writerow(row_items)
            
            self.exportStatusLabel.setText(f"Results exported successfully to:\n{file_path}")

        except Exception as e:
            self.exportStatusLabel.setText(f"Error exporting: {e}")
            slicer.util.errorDisplay(f"Could not export results: {e}")

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
                displayNode = planeNode.GetDisplayNode()
                # --- FIX: Use .SetColor() instead of .SetUnselectedColor() ---
                displayNode.SetColor(color) 
                displayNode.SetSelectedColor(color)
                displayNode.SetOpacity(0.7) # Keeping your preferred opacity
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

    def onCreateMAWClicked(self):
        with slicer.util.tryWithErrorDisplay("Failed to set up for MAW line creation."):
            node_name = "MAW"
            slicer.util.selectModule('Markups')
            lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', node_name)
            slicer.modules.markups.logic().SetActiveListID(lineNode)
            interactionNode = slicer.app.applicationLogic().GetInteractionNode()
            interactionNode.SetCurrentInteractionMode(slicer.vtkMRMLInteractionNode.Place)
            self.mawSelector.setCurrentNode(lineNode)
            self.mirrorPlanesStatusLabel.setText("Now placing points for the 'MAW' line. Click in the scene to define it.")

    def onPlaneCountChanged(self, value):
        self.planeCountLabel.setText(f"Number of mirror planes: {value}")

    # --- THIS FUNCTION IS CORRECTED ---
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
                self.mirrorPlanesStatusLabel.setText("Error: Create reference planes first (Step 3).")
                return
            landmarks_node = self.landmarksSelector.currentNode()
            if not landmarks_node:
                self.mirrorPlanesStatusLabel.setText("Error: Select landmarks first (Step 2).")
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
                self.mirrorPlanesStatusLabel.setText("Error: Please define the Maximum Aperture Width (MAW) line.")
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
                
                displayNode = plane.GetDisplayNode()
                color = self.colorPalette[i % len(self.colorPalette)]
                # --- FIX: Use .SetColor() instead of .SetUnselectedColor() ---
                displayNode.SetColor(color)
                displayNode.SetSelectedColor(color)
                displayNode.SetOpacity(0.7) # Keeping your preferred opacity
                
                self.mirrorPlanes.append(plane)
                self.helperNodes.append(plane)
            self.mirrorPlanesStatusLabel.setText(f"Created {plane_count} colored mirror planes.")

    # --- THIS FUNCTION IS CORRECTED ---
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

            def intersect_planes(p1_node, p2_node, line_name, color):
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
                
                displayNode = line_node.GetDisplayNode()
                # --- FIX: Use .SetColor() instead of .SetUnselectedColor() ---
                displayNode.SetColor(color)
                displayNode.SetSelectedColor(color)
                
                return line_node

            count = 0
            for i in range(plane_count):
                letter = chr(65 + i)
                try:
                    mirror_plane = slicer.util.getNode(f"Plane_{letter}{suffix}")
                    line_name = f"{self.activeProfilePlaneName}_{letter}{suffix}"
                    
                    # Get the color from the mirror plane to pass to the line
                    color = mirror_plane.GetDisplayNode().GetColor()
                    
                    line_node = intersect_planes(profile_plane, mirror_plane, line_name, color)
                    if line_node:
                        count += 1
                        self.helperNodes.append(line_node)
                except slicer.util.MRMLNodeNotFoundException:
                    print(f"Could not find mirror plane Plane_{letter}{suffix} to create intersection line.")
                    continue
            self.intersectionLinesStatusLabel.setText(f"Created {count} colored intersection lines.")

    # --- THIS FUNCTION IS CORRECTED ---
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
            displayNode_a = line_a.GetDisplayNode()
            # --- FIX: Use .SetColor() ---
            displayNode_a.SetColor(0.0, 1.0, 1.0) # Cyan
            displayNode_a.SetSelectedColor(0.0, 1.0, 1.0)
            self.helperNodes.append(line_a)

            direction = pos['nasion'] - pos['prosthion']
            direction /= np.linalg.norm(direction)
            line_b = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"Line_B{suffix}")
            line_b.AddControlPoint(pos['rhinion'] - 150 * direction)
            line_b.AddControlPoint(pos['rhinion'] + 150 * direction)
            displayNode_b = line_b.GetDisplayNode()
            # --- FIX: Use .SetColor() ---
            displayNode_b.SetColor(1.0, 1.0, 0.0) # Yellow
            displayNode_b.SetSelectedColor(1.0, 1.0, 0.0)
            self.helperNodes.append(line_b)
            self.linesABStatusLabel.setText("Lines A and B created.")

    def onFindLineAIntersectionClicked(self):
        self.find_line_intersections("Line_A", "mirrorA")

    def onFindLineBIntersectionClicked(self):
        self.find_line_intersections("Line_B", "mirrorB")

    # --- THIS FUNCTION IS CORRECTED ---
    def find_line_intersections(self, target_line_name, point_prefix):
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
                    
                    displayNode = point_node.GetDisplayNode()
                    line_color = intersecting_line.GetDisplayNode().GetColor()
                    # --- FIX: Use .SetColor() ---
                    displayNode.SetColor(line_color)
                    displayNode.SetSelectedColor(line_color)

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
        node = self.download_and_load_markup("nasal_bone_outline", self.bonePointsStatusLabel, urls, show_step6_image=True)
        if node:
            self.nasalBoneOutlineSelector.setCurrentNode(node)

    def onDownloadSoftTissueOutlineClicked(self):
        urls = {
            4: "https://github.com/user-attachments/files/19327865/nose.profile.outline.4.mrk.json",
            5: "https://github.com/user-attachments/files/19327866/nose.profile.outline.5.mrk.json",
            6: "https://github.com/user-attachments/files/23497912/nose_profile_outline_6.mrk.json"
        }
        node = self.download_and_load_markup("nose_profile_outline", self.softTissueStatusLabel, urls)
        if node:
            self.softTissueOutlineSelector.setCurrentNode(node)

    def download_and_load_markup(self, node_name_base, status_label, url_map, show_step6_image=False):
        with slicer.util.tryWithErrorDisplay(f"Failed to download {node_name_base}."):
            plane_count = self.get_plane_count()
            suffix = self.get_suffix()
            node_name = f"{node_name_base}{suffix}"
            status_label.setText("Downloading landmarks...")
            slicer.app.processEvents()
            
            if plane_count not in url_map:
                status_label.setText("No file for this plane count.")
                return None
            
            try:
                # Remove old node with same name
                try:
                    old_node = slicer.util.getNode(node_name)
                    slicer.mrmlScene.RemoveNode(old_node)
                except slicer.util.MRMLNodeNotFoundException:
                    pass
                
                response = requests.get(url_map[plane_count])
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(suffix='.mrk.json', delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name
                
                outlineNode = slicer.util.loadMarkups(temp_file_path)
                os.unlink(temp_file_path)
                
                if outlineNode:
                    outlineNode.SetName(node_name)
                    status_label.setText(f"Landmarks loaded. Adjust positions if needed.")
                    
                    # Show image in Step 6 after download
                    if show_step6_image and hasattr(self, 'step6ImageContainer'):
                        if not self.step6ImageContainer.isVisible():
                            self.addImageFromGitHub(self.step6ImageLayout, "6.1.png", width=400, height=280)
                            self.step6ImageContainer.setVisible(True)
                    
                    slicer.modules.markups.logic().SetActiveListID(outlineNode)
                    slicer.util.selectModule('Markups')
                    self.helperNodes.append(outlineNode)
                    return outlineNode  # RETURN THE NODE!
                else:
                    status_label.setText("Failed to load landmarks from downloaded file.")
                    return None
            except Exception as e:
                status_label.setText(f"Error: {str(e)}")
                return None
            
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
                displayNode = line_node.GetDisplayNode()
                displayNode.SetColor(0.0, 1.0, 0.0)
                displayNode.SetSelectedColor(0.0, 1.0, 0.0)
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
                    displayNode = point_node.GetDisplayNode()
                    displayNode.SetColor(1.0, 0.0, 1.0)
                    displayNode.SetSelectedColor(1.0, 0.0, 1.0)
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
                    displayNode_m = measurement_line.GetDisplayNode()
                    displayNode_m.SetColor(0.8, 0.6, 1.0)
                    displayNode_m.SetSelectedColor(0.8, 0.6, 1.0)
                    self.helperNodes.append(measurement_line)

                    length = np.linalg.norm(bone_pos - mirror_pos)
                    p1 = np.array(profile_line_node.GetNthControlPointPosition(0))
                    p2 = np.array(profile_line_node.GetNthControlPointPosition(1))
                    direction = (p2 - p1) / np.linalg.norm(p2 - p1)
                    end_point = mirror_pos + (length + fstt_value) * direction
                    
                    pred_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', f"{pred_name_base}{i+1}{suffix}")
                    pred_line.AddControlPoint(mirror_pos)
                    pred_line.AddControlPoint(end_point)
                    displayNode_p = pred_line.GetDisplayNode()
                    displayNode_p.SetColor(color)
                    displayNode_p.SetSelectedColor(color)
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
                true_point_index = i
                prediction_node_index = plane_count - i

                try:
                    true_point_pos = np.array(soft_tissue_node.GetNthControlPointPosition(true_point_index))
                    pred_nodes = slicer.util.getNodes(f"pred soft nose outline *{prediction_node_index}{suffix}")

                    for pred_node_name, pred_node in pred_nodes.items():
                        pred_endpoint_pos = np.array(pred_node.GetNthControlPointPosition(1))
                        error_line_name = f"pred error{true_point_index+1}{suffix}"
                        
                        error_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', error_line_name)
                        error_line.AddControlPoint(pred_endpoint_pos)
                        error_line.AddControlPoint(true_point_pos)
                        displayNode = error_line.GetDisplayNode()
                        displayNode.SetColor(0.8, 0.1, 0.1)
                        displayNode.SetSelectedColor(0.8, 0.1, 0.1)
                        error_line.SetLocked(True)
                        error_count += 1
                        self.helperNodes.append(error_line)

                except Exception as e:
                    print(f"Could not create error line for true point {true_point_index+1}: {e}")
                        
            self.softTissueStatusLabel.setText(f"Created {error_count} error measurement lines correctly.")
            self.populateResultsTable()

    def populateResultsTable(self):
        """Populate results table with 4 columns: Prediction Line | Mirror Equivalent | Value (mm) | Error (mm)"""
        self.measurementsTable.setRowCount(0)
        
        # Set up 4 columns
        self.measurementsTable.setColumnCount(4)
        self.measurementsTable.setHorizontalHeaderLabels([
            "Prediction Line", 
            "Mirror Equivalent", 
            "Value (mm)", 
            "Error (mm)"
        ])
        
        plane_count = self.planeCountSlider.value
        suffix = f"_{plane_count}p"
        
        # Get all prediction nodes
        prediction_nodes = {}
        for node_name, node in slicer.util.getNodes(f'pred soft nose outline *{suffix}').items():
            # Extract the number from the node name (e.g., "pred soft nose outline 1" -> 1)
            import re
            match = re.search(r'pred soft nose outline (\d+)', node_name)
            if match:
                pred_num = int(match.group(1))
                prediction_nodes[pred_num] = node
        
        if not prediction_nodes:
            self.measurementsTable.setRowCount(1)
            self.measurementsTable.setItem(0, 0, qt.QTableWidgetItem("No predictions found"))
            return
        
        # Sort by prediction number
        row = 0
        for pred_num in sorted(prediction_nodes.keys()):
            pred_node = prediction_nodes[pred_num]
            
            # Get the prediction length (from mirror point to predicted endpoint)
            pred_length = np.linalg.norm(
                np.array(pred_node.GetNthControlPointPosition(1)) - 
                np.array(pred_node.GetNthControlPointPosition(0))
            )
            
            # Find corresponding mirror equivalent (nasalbonetoB)
            mirror_node_name = f"nasalbonetoB{pred_num}{suffix}"
            mirror_length = None
            mirror_label = f"nasalbonetoB{pred_num}"
            try:
                mirror_node = slicer.util.getNode(mirror_node_name)
                mirror_length = np.linalg.norm(
                    np.array(mirror_node.GetNthControlPointPosition(1)) - 
                    np.array(mirror_node.GetNthControlPointPosition(0))
                )
            except slicer.util.MRMLNodeNotFoundException:
                mirror_label = "N/A"
            
            # Find corresponding error
            # Error for prediction N corresponds to pred error{plane_count - N + 1}
            error_num = plane_count - pred_num + 1
            error_length = None
            try:
                error_node_name = f"pred error{error_num}{suffix}"
                error_node = slicer.util.getNode(error_node_name)
                error_length = np.linalg.norm(
                    np.array(error_node.GetNthControlPointPosition(1)) - 
                    np.array(error_node.GetNthControlPointPosition(0))
                )
            except slicer.util.MRMLNodeNotFoundException:
                pass
            
            # Add row to table
            self.measurementsTable.insertRow(row)
            
            # Column 0: Prediction line name
            self.measurementsTable.setItem(row, 0, qt.QTableWidgetItem(f"pred soft nose outline {pred_num}"))
            
            # Column 1: Mirror equivalent
            self.measurementsTable.setItem(row, 1, qt.QTableWidgetItem(mirror_label))
            
            # Column 2: Value (mirror length)
            if mirror_length is not None:
                self.measurementsTable.setItem(row, 2, qt.QTableWidgetItem(f"{mirror_length:.2f}"))
            else:
                self.measurementsTable.setItem(row, 2, qt.QTableWidgetItem("N/A"))
            
            # Column 3: Error
            if error_length is not None:
                self.measurementsTable.setItem(row, 3, qt.QTableWidgetItem(f"{error_length:.2f}"))
            else:
                self.measurementsTable.setItem(row, 3, qt.QTableWidgetItem("N/A"))
            
            row += 1
        
        # Resize columns to fit content
        self.measurementsTable.resizeColumnsToContents()
        
        # Make the table stretch to fill available space
        header = self.measurementsTable.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(4):
            header.setSectionResizeMode(i, qt.QHeaderView.ResizeToContents)

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
            result = qt.QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        
            # Check if we got a result (user didn't cancel)
            if not result or len(result) == 0:
                self.exportStatusLabel.setText("Export cancelled.")
                return
            
            # Get the filename (handle both tuple and single value returns)
            if isinstance(result, tuple):
                fileName = result[0]
            else:
                fileName = result
            
            # Check if user actually entered a filename
            if not fileName or fileName == "":
                self.exportStatusLabel.setText("Export cancelled.")
                return
            
            # Now proceed with saving
            if fileName:
                with slicer.util.tryWithErrorDisplay("Failed to export results."):
                    with open(fileName, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([self.measurementsTable.horizontalHeaderItem(i).text() for i in range(self.measurementsTable.columnCount())])
                        for row in range(self.measurementsTable.rowCount()):
                            row_data = [self.measurementsTable.item(row, col).text() if self.measurementsTable.item(row, col) else "" for col in range(self.measurementsTable.columnCount())]
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
