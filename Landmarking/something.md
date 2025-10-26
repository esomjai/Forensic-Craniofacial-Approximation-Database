```python

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import ctk

class LandmarkingGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Landmarking")
        self.setObjectName("Landmarking")
        
        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setSpacing(10)
        
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        # Node storage
        self.landmarksNode = None
        self.referencePlane = None
        self.boneModel = None
        self.softTissueModel = None
        
        # Segmentation option
        self.wantsSegmentation = True
        
        # Observers and flags
        self.isDynamicModelerInstalled = False
        
        self.createAllStepWidgets()
        self.setupNavigation()
        self.checkDependencies()  # This method exists now
        self.syncWithScene()
        
        self.currentStep = 0
        self.updateStepUI()

    def createAllStepWidgets(self):
        self.createStep0_FHPRealignment()
        self.createStep1_SegmentationOption()
        self.createStep2_Segmentation()  
        self.createStep3_SoftTissueSegmentation()
        self.createStep4_LandmarkPlacement()

    def checkDependencies(self):
        """Check if required extensions are installed"""
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
                "The <b>Dynamic Modeler</b> extension is required for this tool, but it was not found.<br><br>"
                "Please install it to continue:<br>"
                "1. Go to the menu: <b>View -> Extension Manager</b>.<br>"
                "2. In the 'Search' bar, type <b>Dynamic Modeler</b>.<br>"
                "3. Click the <b>'Install'</b> button.<br>"
                "4. <b>Restart 3D Slicer</b> after the installation is complete.<br><br>"
                "This tool will not function correctly until the extension is installed and Slicer is restarted.")
            msgBox.exec_()

    def setupNavigation(self):
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        navLayout.setContentsMargins(0, 0, 0, 0)
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.setToolTip("Go to the previous step.")
        self.prevButton.clicked.connect(self.onPrevButtonClicked)
        self.stepLabel = qt.QLabel("Step 1/5")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter)
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.nextButton = qt.QPushButton("Next")
        self.nextButton.setToolTip("Go to the next step.")
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        navLayout.addWidget(self.prevButton)
        navLayout.addStretch(1)
        navLayout.addWidget(self.stepLabel)
        navLayout.addStretch(1)
        navLayout.addWidget(self.nextButton)
        self.mainLayout.addWidget(navWidget)

    def createStep0_FHPRealignment(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 0: FHP Realignment")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel("First, we need to realign the volume to the Frankfort Horizontal Plane for proper orientation.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Create FHP realignment widgets
        formLayout = qt.QFormLayout()
        
        self.inputVolumeSelector = slicer.qMRMLNodeComboBox()
        self.inputVolumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputVolumeSelector.setMRMLScene(slicer.mrmlScene)
        self.inputVolumeSelector.setToolTip("Pick the input CT volume to be realigned.")
        formLayout.addRow("Input Volume: ", self.inputVolumeSelector)
        
        self.inputFiducialsSelector = slicer.qMRMLNodeComboBox()
        self.inputFiducialsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.inputFiducialsSelector.setMRMLScene(slicer.mrmlScene)
        self.inputFiducialsSelector.setToolTip("These are the landmarks to define the Frankfort Horizontal Plane.")
        formLayout.addRow("FHP Landmarks:", self.inputFiducialsSelector)
        
        layout.addLayout(formLayout)
        
        # Instructional label
        self.fhpInstructionLabel = qt.QLabel("Please place all three landmarks (poR, poL, zyoL) before proceeding.")
        self.fhpInstructionLabel.setWordWrap(True)
        layout.addWidget(self.fhpInstructionLabel)
        
        # Action buttons
        self.applyFHPButton = qt.QPushButton("Apply FHP Realignment")
        self.applyFHPButton.setToolTip("Run the FHP realignment on the input volume.")
        self.applyFHPButton.setEnabled(False)
        self.applyFHPButton.clicked.connect(self.onFHPRealign)
        layout.addWidget(self.applyFHPButton)
        
        self.undoFHPButton = qt.QPushButton("Undo Realignment")
        self.undoFHPButton.setToolTip("Revert the volume to its original position before realignment.")
        self.undoFHPButton.setEnabled(False)
        self.undoFHPButton.clicked.connect(self.onFHPUndo)
        layout.addWidget(self.undoFHPButton)
        
        # Auto-load landmarks button
        self.autoLoadLandmarksButton = qt.QPushButton("Auto-load FHP Landmarks")
        self.autoLoadLandmarksButton.setToolTip("Download and load standard FHP landmarks.")
        self.autoLoadLandmarksButton.clicked.connect(self.autoLoadFHPlandmarks)
        layout.addWidget(self.autoLoadLandmarksButton)
        
        self.step0StatusLabel = qt.QLabel("Status: Please select input volume and landmarks.")
        self.step0StatusLabel.setWordWrap(True)
        layout.addWidget(self.step0StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
        
        # Connect selectors
        self.inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onFHPSelect)
        self.inputFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onFHPSelect)

    def createStep1_SegmentationOption(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 1: Segmentation Option")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel("Would you like to perform segmentation to create 3D models of the skull and soft tissue?")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Radio buttons for segmentation choice
        self.segmentationYesRadio = qt.QRadioButton("Yes, I want to perform segmentation")
        self.segmentationYesRadio.setChecked(True)
        self.segmentationNoRadio = qt.QRadioButton("No, skip segmentation steps")
        
        layout.addWidget(self.segmentationYesRadio)
        layout.addWidget(self.segmentationNoRadio)
        
        # Info label
        infoLabel = qt.QLabel(
            "Note: If you choose 'No', you will skip the segmentation steps and proceed directly "
            "to landmark placement. Use 'Shift' toggle in the 'VolumeRendering' module to swittch between bone and soft tissue views")
        infoLabel.setWordWrap(True)
        infoLabel.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(infoLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep2_Segmentation(self):
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(15)
        
        title = qt.QLabel("Step 2: Segment, Export, and Re-import the Skull Model")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        mainLayout.addWidget(title)
        
        # Create collapsible button for segmentation instructions
        self.segmentationCollapsible = ctk.ctkCollapsibleButton()
        self.segmentationCollapsible.text = "Show/Hide Segmentation Instructions"
        self.segmentationCollapsible.collapsed = True  # Start collapsed
        
        segmentationLayout = qt.QVBoxLayout(self.segmentationCollapsible)
        segmentationLayout.setContentsMargins(10, 10, 10, 10)
        
        instructions = qt.QLabel()
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setOpenExternalLinks(True)
        instructions.setWordWrap(True)
        instructions.setText(
            "Follow these steps carefully to create a clean 'Bone' model for the next steps.<br><br>"
            "<b>1. Open Segment Editor:</b> Click this button to open the module.<br>"
        )
        segmentationLayout.addWidget(instructions)
        
        self.openSegmentEditorButton = qt.QPushButton("Open Segment Editor Module")
        self.openSegmentEditorButton.clicked.connect(lambda: slicer.util.selectModule('SegmentEditor'))
        segmentationLayout.addWidget(self.openSegmentEditorButton)
        
        instructions2 = qt.QLabel()
        instructions2.setTextFormat(qt.Qt.RichText)
        instructions2.setOpenExternalLinks(True)
        instructions2.setWordWrap(True)
        instructions2.setText(
            "<br><b>2. Rename your segmentation:</b> Click the dropdown menu next to <b>Segmentation:</b> and choose 'Rename current Segmentation'.<br><br>"
            "<b>3. Source Volume</b> should be the name of your DICOM file.<br><br>"
            "<b>4. Click the plus sign [+] 'Add'.</b><br><br>"
            "<b>5. Choose the Threshold tool</b> from the panel below (in the right column, first row).<br><br>"
            "<b>6. Edit the Threshold Range:</b> The minimum is usually 500. (<a href='https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Start%20here%20/003_ROI%20vs%20Segmentation.md'>Refer to this guide for more detail</a>).<br><br>"
            "<b>7. Click 'Apply'</b> (in the Local histogram menu), then find the <b>'Show 3D'</b> button on the top, near to where the 'Add' button was. Click it and wait for the model to appear.<br><br>"
            "<b>8. If you're happy with the details,</b> click on the green right arrow to go to the 'Segmentations' module.<br><br>"
            "<b>9. Double click on the row below 'Name'</b> and in the pop-up, edit the model name into <b>'Bone'</b>.<br><br>"
            "<b>10. Scroll to the dropdown menu 'Export/import models and labelmaps':</b> Make sure the <b>Operation</b> is 'Export' and the <b>Output type</b> is 'Models'. Then move down to the next menu (Export to files), choose the destination folder and click the 'Export' button in this submenu. (You may have to check the Size scale to be 1.000).<br><br>"
            "<b>11. IMPORTANT:</b> You need to import this model back into the scene by clicking the <b>'Data'</b> button (very top of the Slicer window, under 'File'), 'Choose file(s) to add...', and finding the model you just exported, named something like 'Bone_Bone.stl'. Let the description be 'Model' and click 'OK'."
        )
        segmentationLayout.addWidget(instructions2)
        
        mainLayout.addWidget(self.segmentationCollapsible)
        
        confirmGroup = qt.QGroupBox("Final Confirmation")
        confirmLayout = qt.QFormLayout(confirmGroup)
        confirmLabel = qt.QLabel("Once the model is re-imported, please select it below:")
        confirmLabel.setWordWrap(True)
        
        self.boneModelSelector = slicer.qMRMLNodeComboBox()
        self.boneModelSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.boneModelSelector.setMRMLScene(slicer.mrmlScene)
        self.boneModelSelector.addEnabled = False
        self.boneModelSelector.removeEnabled = False
        self.boneModelSelector.noneEnabled = True
        self.boneModelSelector.setToolTip("Select the 'Bone' model you just re-imported.")
        self.boneModelSelector.currentNodeChanged.connect(self.onConfirmSegmentation)
        
        confirmLayout.addRow(confirmLabel)
        confirmLayout.addRow("Re-imported Bone Model:", self.boneModelSelector)
        mainLayout.addWidget(confirmGroup)
        
        self.step2StatusLabel = qt.QLabel("Status: Waiting for user to select the re-imported 'Bone' model.")
        self.step2StatusLabel.setWordWrap(True)
        mainLayout.addWidget(self.step2StatusLabel)
        
        # Make Dynamic Modeler section collapsible too
        self.dynamicModelerCollapsible = ctk.ctkCollapsibleButton()
        self.dynamicModelerCollapsible.text = "Optional: Cut the Bone Model (if needed)"
        self.dynamicModelerCollapsible.collapsed = True  # Start collapsed
        
        dynamicModelerLayout = qt.QVBoxLayout(self.dynamicModelerCollapsible)
        dynamicModelerLayout.setContentsMargins(10, 10, 10, 10)

        # ROI Tip
        roiTipLabel = qt.QLabel()
        roiTipLabel.setTextFormat(qt.Qt.RichText)
        roiTipLabel.setWordWrap(True)
        roiTipLabel.setText(
            "<b>If your model is too large</b> or slow to process, you can use the 'ROI cut' tool to trim it down first:<br><br>"
            "&bull; Go to the <b>'Markups'</b> module and create a new <b>ROI</b>, drawing a box around the area you want to keep."
        )
        dynamicModelerLayout.addWidget(roiTipLabel)

        # NEW: Open Markups button
        openMarkupsLayout = qt.QHBoxLayout()
        openMarkupsLabel = qt.QLabel("Click to open Markups module:")
        self.openMarkupsButton = qt.QPushButton("Open Markups Module")
        self.openMarkupsButton.clicked.connect(lambda: slicer.util.selectModule('Markups'))
        openMarkupsLayout.addWidget(openMarkupsLabel)
        openMarkupsLayout.addStretch()
        openMarkupsLayout.addWidget(self.openMarkupsButton)
        dynamicModelerLayout.addLayout(openMarkupsLayout)

        roiTipLabel2 = qt.QLabel()
        roiTipLabel2.setTextFormat(qt.Qt.RichText)
        roiTipLabel2.setWordWrap(True)
        roiTipLabel2.setText(
            "<br>&bull; Return to the <b>'Dynamic Modeler'</b> module and use the <b>'ROI cut'</b> tool.<br><br>"
            "&bull; Set the 'Input Model' (your bone model) and the 'ROI node' (the box you just drew).<br><br>"
            "&bull; In 'Output nodes', find 'Clipped output model (inside)' and select your original model. This will <b>replace</b> it with the smaller version.<br><br>"
            "&bull; Click 'Apply' to finish."
        )
        dynamicModelerLayout.addWidget(roiTipLabel2)
        
        dynamicModelerLayout.addSpacing(15)

        # Plane Cut Instructions
        planeCutLabel = qt.QLabel()
        planeCutLabel.setTextFormat(qt.Qt.RichText)
        planeCutLabel.setWordWrap(True)
        planeCutLabel.setText(
            "<b>2.</b> Use the <b>'Plane cut'</b> tool to cut your model along the reference plane:<br><br>"
            "&bull; In the Dynamic Modeler module, select the <b>'Plane cut'</b> tool.<br><br>"
            "&bull; Set the 'Input Model' to your bone model.<br><br>"
            "&bull; Set the 'Plane' to your reference plane (INB or MSP).<br><br>"
            "&bull; In 'Output nodes', you can choose to create new models for the positive/negative sides or replace the original.<br><br>"
            "&bull; Click 'Apply' to perform the cut."
        )
        dynamicModelerLayout.addWidget(planeCutLabel)

        dynamicModelerLayout.addSpacing(15)

        # Confirm cut button
        confirmCutLabel = qt.QLabel("<b>3.</b> If you've created the cut models you're happy with, please choose the button below to proceed.")
        confirmCutLabel.setTextFormat(qt.Qt.RichText)
        confirmCutLabel.setWordWrap(True)
        dynamicModelerLayout.addWidget(confirmCutLabel)
        
        self.confirmCutButton = qt.QPushButton("Confirm Model Cut")
        self.confirmCutButton.clicked.connect(self.onConfirmCut)
        dynamicModelerLayout.addWidget(self.confirmCutButton, 0, qt.Qt.AlignHCenter)
        
        dynamicModelerLayout.addSpacing(10)

        self.step2CutStatusLabel = qt.QLabel("Status: Optional - you can cut the model if needed.")
        self.step2CutStatusLabel.setWordWrap(True)
        dynamicModelerLayout.addWidget(self.step2CutStatusLabel)
        
        mainLayout.addWidget(self.dynamicModelerCollapsible)
        mainLayout.addStretch(1)
        
        self.stepStack.addWidget(widget)

    def createStep3_SoftTissueSegmentation(self):
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(15)
        
        title = qt.QLabel("Step 3: Soft Tissue Segmentation")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        mainLayout.addWidget(title)
        
        desc = qt.QLabel(
            "Now we'll create a soft tissue model using a different threshold range. "
            "Follow the same process as before but with these changes:")
        desc.setWordWrap(True)
        mainLayout.addWidget(desc)
        
        instructions = qt.QLabel()
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setWordWrap(True)
        instructions.setText(
            "<b>Instructions for Soft Tissue Segmentation:</b><br><br>"
            "1. In the <b>Segment Editor</b>, create a new segment for soft tissue<br>"
            "2. Use the <b>Threshold tool</b> with a range of approximately <b>-200 to 200</b> Hounsfield Units<br>"
            "3. Name this segment <b>'SoftTissue'</b><br>"
            "4. Export and re-import the model as before<br>"
            "5. Select the re-imported soft tissue model below"
        )
        mainLayout.addWidget(instructions)
        
        self.openSegmentEditorButton2 = qt.QPushButton("Open Segment Editor Module")
        self.openSegmentEditorButton2.clicked.connect(lambda: slicer.util.selectModule('SegmentEditor'))
        mainLayout.addWidget(self.openSegmentEditorButton2)
        
        confirmGroup = qt.QGroupBox("Soft Tissue Model Confirmation")
        confirmLayout = qt.QFormLayout(confirmGroup)
        confirmLabel = qt.QLabel("Once the soft tissue model is re-imported, please select it below:")
        confirmLabel.setWordWrap(True)
        
        self.softTissueModelSelector = slicer.qMRMLNodeComboBox()
        self.softTissueModelSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.softTissueModelSelector.setMRMLScene(slicer.mrmlScene)
        self.softTissueModelSelector.addEnabled = False
        self.softTissueModelSelector.removeEnabled = False
        self.softTissueModelSelector.noneEnabled = True
        self.softTissueModelSelector.setToolTip("Select the 'SoftTissue' model you just re-imported.")
        self.softTissueModelSelector.currentNodeChanged.connect(self.onConfirmSoftTissueSegmentation)
        
        confirmLayout.addRow(confirmLabel)
        confirmLayout.addRow("Re-imported Soft Tissue Model:", self.softTissueModelSelector)
        mainLayout.addWidget(confirmGroup)
        
        self.step3StatusLabel = qt.QLabel("Status: Waiting for user to select the re-imported 'SoftTissue' model.")
        self.step3StatusLabel.setWordWrap(True)
        mainLayout.addWidget(self.step3StatusLabel)
        
        mainLayout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep4_LandmarkPlacement(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 4: Landmark Placement")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "Now that you have your segmented models, you can load the landmark templates "
            "and place them on the appropriate models.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Landmark download buttons
        buttonLayout = qt.QVBoxLayout()
        buttonLayout.setSpacing(10)
        
        self.loadHardLandmarksButton = qt.QPushButton("Load Hard Tissue Landmarks")
        self.loadHardLandmarksButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;")
        self.loadHardLandmarksButton.setToolTip("Load hard tissue landmarks for placement on the bone model.")
        self.loadHardLandmarksButton.clicked.connect(self.onDownloadHardLandmarks)
        buttonLayout.addWidget(self.loadHardLandmarksButton)
        
        self.loadSoftLandmarksButton = qt.QPushButton("Load Soft Tissue Landmarks") 
        self.loadSoftLandmarksButton.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 8px;")
        self.loadSoftLandmarksButton.setToolTip("Load soft tissue landmarks for placement on the soft tissue model.")
        self.loadSoftLandmarksButton.clicked.connect(self.onDownloadSoftLandmarks)
        buttonLayout.addWidget(self.loadSoftLandmarksButton)
        
        layout.addLayout(buttonLayout)
        
        # Instructions
        instructions = qt.QLabel(
            "<b>Instructions:</b><br>"
            "1. Click the buttons above to load the landmark templates<br>"
            "2. Place the hard tissue landmarks on your 'Bone' model<br>"
            "3. Place the soft tissue landmarks on your 'SoftTissue' model<br>"
            "4. You can adjust landmark positions as needed"
        )
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # NEW: Export to Clipboard Section
        exportGroup = qt.QGroupBox("Export Landmarks to Excel")
        exportLayout = qt.QVBoxLayout(exportGroup)
        
        exportInstructions = qt.QLabel(
            "Click the button below to copy all landmark names and RAS coordinates to clipboard "
            "in a format that can be easily pasted into Excel."
        )
        exportInstructions.setWordWrap(True)
        exportLayout.addWidget(exportInstructions)
        
        self.exportToClipboardButton = qt.QPushButton("Copy Landmarks to Clipboard")
        self.exportToClipboardButton.setStyleSheet("background-color: #ffc107; color: black; font-weight: bold; padding: 8px;")
        self.exportToClipboardButton.setToolTip("Copy all landmark coordinates to clipboard for Excel")
        self.exportToClipboardButton.clicked.connect(self.exportLandmarksToClipboard)
        exportLayout.addWidget(self.exportToClipboardButton)
        
        layout.addWidget(exportGroup)
        
        self.step4StatusLabel = qt.QLabel("Status: Ready to load landmarks.")
        self.step4StatusLabel.setWordWrap(True)
        layout.addWidget(self.step4StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    # FHP Realignment Methods
    def onFHPSelect(self):
        volumeNode = self.inputVolumeSelector.currentNode()
        fiducialNode = self.inputFiducialsSelector.currentNode()
        
        self.applyFHPButton.setEnabled(False)
        
        if volumeNode and fiducialNode:
            labels = []
            for i in range(fiducialNode.GetNumberOfControlPoints()):
                labels.append(fiducialNode.GetNthControlPointLabel(i))
            
            has_poR = any('por' in label.lower() for label in labels)
            has_poL = any('pol' in label.lower() for label in labels) 
            has_zyoL = any('zyol' in label.lower() for label in labels)
            
            hasPoints = has_poR and has_poL and has_zyoL
            
            if hasPoints:
                self.applyFHPButton.setEnabled(True)
                self.step0StatusLabel.setText("Status: Ready to apply FHP realignment.")
            else:
                self.step0StatusLabel.setText("Status: Please place all three landmarks (poR, poL, zyoL).")
        else:
            if not volumeNode:
                self.step0StatusLabel.setText("Status: Please select input volume.")
            elif not fiducialNode:
                self.step0StatusLabel.setText("Status: Please select FHP landmarks.")

    def onFHPRealign(self):
        inputVolume = self.inputVolumeSelector.currentNode()
        fiducials = self.inputFiducialsSelector.currentNode()
        
        if not inputVolume or not fiducials:
            slicer.util.errorDisplay("Please select both input volume and landmarks.")
            return
            
        self.step0StatusLabel.setText("Status: Applying FHP realignment...")
        slicer.app.processEvents()
        
        try:
            poR_pos, poL_pos, zyoL_pos = None, None, None
            for i in range(fiducials.GetNumberOfControlPoints()):
                label = fiducials.GetNthControlPointLabel(i)
                pos = [0,0,0]; fiducials.GetNthControlPointPositionWorld(i, pos)
                if label.lower() == 'por': poR_pos = np.array(pos)
                if label.lower() == 'pol': poL_pos = np.array(pos)
                if label.lower() == 'zyol': zyoL_pos = np.array(pos)

            if poR_pos is None or poL_pos is None or zyoL_pos is None:
                raise ValueError("Could not find all required landmarks (poR, poL, zyoL)")

            # Calculate transformations (same as before)
            po_vec = poR_pos - poL_pos
            vTransform1 = vtk.vtkTransform()
            vTransform1.RotateZ(-np.arctan2(po_vec[1], po_vec[0]) * 180 / np.pi)
            
            zyoL_p1 = np.array(vTransform1.GetMatrix().MultiplyPoint(np.append(zyoL_pos, 1.0)))[:3]
            poR_p1 = np.array(vTransform1.GetMatrix().MultiplyPoint(np.append(poR_pos, 1.0)))[:3]
            poL_p1 = np.array(vTransform1.GetMatrix().MultiplyPoint(np.append(poL_pos, 1.0)))[:3]
            
            po_vec_p1 = poR_p1 - poL_p1
            vTransform2 = vtk.vtkTransform()
            vTransform2.RotateY(np.arctan2(po_vec_p1[2], po_vec_p1[0]) * 180 / np.pi)
            
            zyoL_p2 = np.array(vTransform2.GetMatrix().MultiplyPoint(np.append(zyoL_p1, 1.0)))[:3]
            poR_p2 = np.array(vTransform2.GetMatrix().MultiplyPoint(np.append(poR_p1, 1.0)))[:3]
            poL_p2 = np.array(vTransform2.GetMatrix().MultiplyPoint(np.append(poL_p1, 1.0)))[:3]
            
            mid_porion_p2 = (poR_p2 + poL_p2) / 2.0
            po_zyo_vec = zyoL_p2 - mid_porion_p2
            vTransform3 = vtk.vtkTransform()
            vTransform3.RotateX(-np.arctan2(po_zyo_vec[2], po_zyo_vec[1]) * 180 / np.pi)
            
            final_transform = vtk.vtkTransform()
            final_transform.Concatenate(vTransform1)
            final_transform.Concatenate(vTransform2)
            final_transform.Concatenate(vTransform3)

            fhpTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Realign_Transform')
            fhpTransformNode.SetMatrixTransformToParent(final_transform.GetMatrix())
            inputVolume.SetAndObserveTransformNodeID(fhpTransformNode.GetID())
            
            self.undoFHPButton.setEnabled(True)
            self.step0StatusLabel.setText("Status: FHP realignment applied successfully! You can proceed to the next step.")
            slicer.util.showStatusMessage("FHP realignment applied!", 3000)
            
        except Exception as e:
            self.step0StatusLabel.setText(f"Status: Error during FHP realignment: {e}")
            slicer.util.errorDisplay(f"FHP realignment failed: {e}")

    def onFHPUndo(self):
        inputVolume = self.inputVolumeSelector.currentNode()
        if not inputVolume:
            return
            
        fhpTransformNode = slicer.util.getFirstNodeByName('FHP_Realign_Transform')
        if fhpTransformNode:
            inputVolume.SetAndObserveTransformNodeID(None)
            slicer.mrmlScene.RemoveNode(fhpTransformNode)
            
        self.undoFHPButton.setEnabled(False)
        self.step0StatusLabel.setText("Status: FHP realignment undone.")
        slicer.util.showStatusMessage("FHP realignment undone!", 3000)

    def autoLoadFHPlandmarks(self):
        if slicer.mrmlScene.GetFirstNodeByName("FHP_Standard_Landmarks"):
            self.inputFiducialsSelector.setCurrentNode(slicer.mrmlScene.GetFirstNodeByName("FHP_Standard_Landmarks"))
            self.step0StatusLabel.setText("Status: FHP landmarks already loaded.")
            return
            
        self.step0StatusLabel.setText("Status: Downloading FHP landmarks...")
        slicer.app.processEvents()
        
        url = "https://github.com/user-attachments/files/22434441/FHP_landmarks.json"
        fileName = "FHP_landmarks.json"
        try:
            tempPath = os.path.join(slicer.app.temporaryPath, fileName)
            urllib.request.urlretrieve(url, tempPath)
            loadedNode = slicer.util.loadMarkups(tempPath)
            if loadedNode: 
                loadedNode.SetName("FHP_Standard_Landmarks")
                self.inputFiducialsSelector.setCurrentNode(loadedNode)
                self.step0StatusLabel.setText("Status: FHP landmarks loaded successfully.")
        except Exception as e:
            self.step0StatusLabel.setText(f"Status: Error downloading landmarks: {e}")
            slicer.util.errorDisplay(f"Could not download landmarks file: {e}")

    def syncWithScene(self):
        self.boneModel = slicer.util.getFirstNodeByName("Bone")
        if self.boneModel: 
            self.boneModelSelector.setCurrentNode(self.boneModel)
            
        self.softTissueModel = slicer.util.getFirstNodeByName("SoftTissue")
        if self.softTissueModel:
            self.softTissueModelSelector.setCurrentNode(self.softTissueModel)
        
        # Update cut status if bone model exists
        if self.boneModel and hasattr(self, 'step2CutStatusLabel'):
            self.step2CutStatusLabel.setText("Status: Bone model ready. You can proceed with cutting if needed.")

    def onLoadLocalLandmarks(self, fileName=None, nodeName=None):
        if not fileName: 
            fileName, _ = qt.QFileDialog.getOpenFileName(self, "Load Landmarks", "", "Markup JSON Files (*.mrk.json)")
        if fileName:
            loadedNode = slicer.util.loadMarkups(fileName)
            if loadedNode:
                finalName = nodeName if nodeName else "Hard_tissue"
                loadedNode.SetName(finalName)
                slicer.util.showStatusMessage(f"'{finalName}' loaded!", 3000)
            else: 
                slicer.util.errorDisplay(f"Failed to load landmarks from {fileName}.")

    def onDownloadHardLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/23121222/hard_tissue.mrk.json", "Hard_tissue_landmarks", self.step4StatusLabel)

    def onDownloadSoftLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/23121223/soft_tissue.mrk.json", "Soft_tissue_landmarks", self.step4StatusLabel)

    def onDownloadAndLoad(self, url, nodeName, statusLabel):
        statusLabel.setText("Status: Downloading..."); slicer.app.processEvents()
        try:
            with urllib.request.urlopen(url) as response: 
                fileData = response.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile: 
                tempFile.write(fileData); tempFilePath = tempFile.name
            self.onLoadLocalLandmarks(tempFilePath, nodeName)
            statusLabel.setText(f"Status: Successfully loaded '{nodeName}'.")
        except Exception as e:
            statusLabel.setText(f"Status: Error! Could not download. Error: {e}"); slicer.util.errorDisplay(f"Failed to download from the web. Error: {e}")
        finally:
            if 'tempFilePath' in locals() and os.path.exists(tempFilePath): 
                os.remove(tempFilePath)

    def onConfirmSegmentation(self, node):
        if node:
            self.boneModel = node; self.step2StatusLabel.setText(f"Status: Confirmed '{self.boneModel.GetName()}' as the bone model. Ready to proceed!")
            slicer.util.showStatusMessage("Bone model confirmed!", 3000)
        else:
            self.boneModel = None; self.step2StatusLabel.setText("Status: Waiting for user to select the re-imported 'Bone' model.")

    def onConfirmSoftTissueSegmentation(self, node):
        if node:
            self.softTissueModel = node
            self.step3StatusLabel.setText(f"Status: Confirmed '{self.softTissueModel.GetName()}' as the soft tissue model. Ready to proceed!")
            slicer.util.showStatusMessage("Soft tissue model confirmed!", 3000)
        else:
            self.softTissueModel = None
            self.step3StatusLabel.setText("Status: Waiting for user to select the re-imported 'SoftTissue' model.")

    def onNextButtonClicked(self):
        self.syncWithScene() 
        stepComplete = False
        
        if self.currentStep == 1:  # Segmentation option step
            self.wantsSegmentation = self.segmentationYesRadio.isChecked()
            stepComplete = True
        elif self.currentStep == 0:  # FHP Realignment
            stepComplete = self.inputVolumeSelector.currentNode() is not None
        elif self.currentStep == 2:  # Bone segmentation
            stepComplete = self.boneModel is not None
        elif self.currentStep == 3:  # Soft tissue segmentation
            stepComplete = self.softTissueModel is not None
        elif self.currentStep == 4:  # Landmark placement
            stepComplete = True

        if not stepComplete: 
            slicer.util.warningDisplay(f"Please complete Step {self.currentStep + 1} before proceeding.")
            return
            
        nextStep = self.currentStep + 1
        if self.currentStep == 1 and not self.wantsSegmentation:
            nextStep = 4  # Skip to landmark placement
        
        if nextStep < self.stepStack.count: 
            self.currentStep = nextStep
            self.updateStepUI()

    def onPrevButtonClicked(self):
        if self.currentStep > 0: 
            prevStep = self.currentStep - 1
            if self.currentStep == 4 and not self.wantsSegmentation:
                prevStep = 1
            self.currentStep = prevStep
            self.updateStepUI()

    def updateStepUI(self):
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        
        if self.currentStep == 1 or self.currentStep == 4:
            self.nextButton.setEnabled(True)  
        else:
            self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)

    def onOpenDynamicModeler(self):
        """Open the Dynamic Modeler module"""
        slicer.util.selectModule('DynamicModeler')
        self.step2CutStatusLabel.setText("Status: Dynamic Modeler opened. Follow the instructions above.")

    def onConfirmCut(self):
        """Confirm that the model has been cut"""
        self.step2CutStatusLabel.setText("Status: Model cut confirmed! You can proceed to the next step.")
        slicer.util.showStatusMessage("Model cut confirmed!", 3000)


    def exportLandmarksToClipboard(self):
        """Export all landmark coordinates to clipboard in Excel-friendly format"""
        try:
            # Get all landmark nodes in the scene
            landmark_nodes = []
            all_nodes = slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
            all_nodes.InitTraversal()
            node = all_nodes.GetNextItemAsObject()
            while node:
                if node.GetNumberOfControlPoints() > 0:
                    landmark_nodes.append(node)
                node = all_nodes.GetNextItemAsObject()
            
            if not landmark_nodes:
                slicer.util.errorDisplay("No landmark nodes found in the scene.")
                return
            
            # Collect all landmarks with their coordinates
            landmarks_data = []
            
            for node in landmark_nodes:
                node_name = node.GetName()
                for i in range(node.GetNumberOfControlPoints()):
                    label = node.GetNthControlPointLabel(i)
                    pos = [0, 0, 0]
                    node.GetNthControlPointPositionWorld(i, pos)
                    
                    landmarks_data.append({
                        'node': node_name,
                        'label': label,
                        'x': pos[0],
                        'y': pos[1],
                        'z': pos[2]
                    })
            
            if not landmarks_data:
                slicer.util.errorDisplay("No landmarks found in the scene.")
                return
            
            # Sort by node name and label
            landmarks_data.sort(key=lambda x: (x['node'], x['label']))
            
            # Create CSV format for Excel
            csv_lines = ["Node Name,Landmark Name,RAS-X,RAS-Y,RAS-Z"]
            
            for landmark in landmarks_data:
                csv_line = f"{landmark['node']},{landmark['label']},{landmark['x']:.3f},{landmark['y']:.3f},{landmark['z']:.3f}"
                csv_lines.append(csv_line)
            
            csv_text = "\n".join(csv_lines)
            
            # Copy to clipboard
            clipboard = qt.QApplication.clipboard()
            clipboard.setText(csv_text)
            
            # Show success message
            num_landmarks = len(landmarks_data)
            slicer.util.showStatusMessage(f"Copied {num_landmarks} landmarks to clipboard!", 5000)
            self.step4StatusLabel.setText(f"Status: Success! Copied {num_landmarks} landmarks to clipboard. You can paste into Excel.")
            
            # Optional: Show preview in dialog
            preview_text = f"Copied {num_landmarks} landmarks to clipboard:\n\n"
            preview_text += "First few landmarks:\n"
            for landmark in landmarks_data[:5]:  # Show first 5 as preview
                preview_text += f"{landmark['node']} - {landmark['label']}: ({landmark['x']:.1f}, {landmark['y']:.1f}, {landmark['z']:.1f})\n"
            
            if num_landmarks > 5:
                preview_text += f"... and {num_landmarks - 5} more landmarks"
                
            qt.QMessageBox.information(self, "Landmarks Copied", preview_text)
            
        except Exception as e:
            slicer.util.errorDisplay(f"Error exporting landmarks: {str(e)}")
            self.step4StatusLabel.setText(f"Status: Error exporting landmarks: {str(e)}")
# --- Entry Point ---
try:
    mainWindow = slicer.util.mainWindow()
    old_gui = mainWindow.findChild(qt.QWidget, "LandmarkingGUI")
    if old_gui:
        if hasattr(old_gui, 'cleanup'): 
            old_gui.cleanup()
        old_gui.deleteLater()
        slicer.app.processEvents()
except Exception as e: 
    print(f"Error during cleanup: {e}")

landmarkingGui = LandmarkingGUI()
landmarkingGui.show()
```
