# Landmarking Workflow GUI

This guide provides a custom Python script that creates a user-friendly, step-by-step Graphical User Interface (GUI) inside 3D Slicer for a complete landmarking study. It is designed for beginners and walks the user through every stage, from initial setup to final landmark export.

The GUI includes the following steps:
- **Step 0: FHP Realignment:** Orient the skull correctly using the Frankfort Horizontal Plane.
- **Step 1 & 2: Bone Segmentation:** Create a 3D model of the skull from a CT scan.
- **Step 3: Soft Tissue Segmentation:** Create a 3D model of the soft tissues.
- **Step 4: Landmark Placement:** Load landmark templates and place them on the models.
- **Export:** Copy all landmark coordinates to the clipboard to easily paste them into Excel.

***

### How to Use This Guide

1.  **Open 3D Slicer.**
2.  Import the DICOM of the CT
3.  Click the DCM button, then find the folder


<img width="750"  alt="import 1" src="https://github.com/user-attachments/assets/8169cb06-a4bf-43b3-bf97-bf8b2e3a626e" />

4. Open the imported scan
<img width="750"  alt="import 2" src="https://github.com/user-attachments/assets/d76381ad-659c-40d5-84ac-1beaaf4cb842" />

5. For the 3D rendering to appear in the "blue" scene, drag and drop it: 

<img width="750" alt="import 3" src="https://github.com/user-attachments/assets/dee9fe49-0a60-49dd-9262-49be0ce17e1e" />

6. Navigate to the **Python Interactor** by clicking `View -> Python Interactor` in the top menu.
 
<img width="750" alt="open python" src="https://github.com/user-attachments/assets/5f6adbd4-31ef-4c54-9ba1-edd77f71292d" />

7.  **Copy the entire Python script** from the code block below.
8.  **Paste the script** into the Python Interactor window.
9.  Press **Enter** to run the script. The "Landmarking" GUI will appear in the Slicer window.

### Python Script

Copy the complete script below to run the Landmarking GUI in 3D Slicer.

```python

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import ctk
import logging
from SegmentEditorEffects import *

class InstructionDialog(qt.QDialog):
    def __init__(self, modelName, parent=None):
        qt.QDialog.__init__(self, parent)
        self.setWindowTitle(f"{modelName} Segmentation Instructions")
        self.setWindowFlags(self.windowFlags() | qt.Qt.WindowStaysOnTopHint)
        
        self.mainLayout = qt.QVBoxLayout(self)

        buttonGroup = qt.QGroupBox("Quick Access")
        buttonLayout = qt.QVBoxLayout(buttonGroup)
        
        actions = [
            {
                "name": "SegmentEditor",
                "icon": ":/Icons/SegmentEditor.png",
                "action": lambda: slicer.util.selectModule("SegmentEditor")
            },
            {
                "name": "VolumeRendering",
                "icon": ":/Icons/VolumeRendering.png",
                "action": lambda: slicer.util.selectModule("VolumeRendering")
            },
            {
                "name": "Segmentations",
                "icon": ":/Icons/Segmentations.png",
                "action": lambda: slicer.util.selectModule("Segmentations")
            },
            {
                "name": "Models",
                "icon": ":/Icons/Models.png",
                "action": lambda: slicer.util.selectModule("Models")
            },
            {
                "name": "Add Data",
                "icon": ":/Icons/AddData.png",
                "action": slicer.util.openAddDataDialog
            }
        ]

        for item in actions:
            button_text = f" Open {item['name']}"
            if "Module" not in item["name"] and "Data" not in item["name"]:
                 button_text += " Module"

            btn = qt.QPushButton(button_text)
            btn.setIcon(qt.QIcon(item["icon"]))
            btn.clicked.connect(item["action"])
            buttonLayout.addWidget(btn)

        self.mainLayout.addWidget(buttonGroup)

        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        if modelName == "Bone":
            recommended_threshold = "500"
        else:
            recommended_threshold = "-500"

        instructions_text = f"""
            <p><b>How to Create Your {modelName} Model</b></p>
            <p>This window will stay open while you work. You can move it to another screen.</p>
            <p><b>Your Steps:</b></p>
            <p>1. <b>Add a Segment:</b> A new, empty segmentation called '<b>{modelName}_Segmentation</b>' has been created for you in the 'Segment Editor' panel. Click the green '<b>Add</b>' button to create a new segment inside it.</p>
            <p>2. <b>Select Threshold Tool:</b> From the list of tools, click on '<b>Threshold</b>'. It is usually in the top row on the right.</p>
            <p>3. <b>Adjust Threshold:</b> Use the 'Threshold Range' slider to select the tissue you want. For {modelName}, a good starting point is <b>{recommended_threshold}</b>. You will see the selected area highlighted in the slice views.</p>
            <p>4. <b>Apply:</b> Once you are happy with the highlighted area, click the '<b>Apply</b>' button.</p>
            <p>5. <b>Show 3D Model:</b> At the top of the Segment Editor panel, click the '<b>Show 3D</b>' button. After a moment, your 3D model will appear!</p>
            <p>6. <b>Export the Model:</b> Click the '<b>Open Segmentations Module</b>' button above. Find the 'Export/import...' section and the 'Export to files' section. Make sure '<b>Export</b>' and '<b>Models</b>' are selected. Then, choose a folder and click the final '<b>Export</b>' button.</p>
            <p>7. <b>Re-import the Model:</b> Click the '<b>Open Add Data</b>' button above and choose the STL file you just saved. You can check that it loaded correctly in the '<b>Models</b>' module.</p>
            <p>8. <b>Confirm:</b> Come back to the main 'Landmarking' window and select your new, re-imported model from the '<b>{modelName} Model</b>' dropdown menu to continue.</p>
            <br>
            <p><a href='{video_url}'>Click here to watch a tutorial video.</a></p>
        """

        instructionLabel = qt.QLabel(instructions_text)
        instructionLabel.setTextFormat(qt.Qt.RichText)
        instructionLabel.setWordWrap(True)
        instructionLabel.setOpenExternalLinks(True)
        self.mainLayout.addWidget(instructionLabel)

        self.closeButton = qt.QPushButton("Close")
        # --- THIS IS THE FIX for the popup window ---
        self.closeButton.clicked.connect(lambda: self.close())
        self.mainLayout.addWidget(self.closeButton)


class LandmarkingGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Landmarking")
        self.setObjectName("LandmarkingGUI")
        
        self.setWindowFlags(self.windowFlags() | qt.Qt.WindowStaysOnTopHint)

        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setSpacing(10)
        
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        self.landmarksNode = None
        self.referencePlane = None
        self.boneModel = None
        self.softTissueModel = None
        self.inputVolume = None
        self.croppedVolume = None
        
        self.wantsSegmentation = True
        self.isDynamicModelerInstalled = False
        self.currentStep = 0
        
        self.createAllStepWidgets()
        self.setupNavigation()
        self.checkDependencies()
        self.syncWithScene()
        
        self.updateStepUI()

    def createAllStepWidgets(self):
        self.createStep0_FHPRealignment()
        self.createStep1_ROICrop()
        self.createStep2_SegmentationOption()
        self.createStep3_Segmentation()  
        self.createStep4_SoftTissueSegmentation()
        self.createStep5_LandmarkPlacement()

    def checkDependencies(self):
        moduleName = "DynamicModeler" 
        if moduleName in slicer.app.moduleManager().factoryManager().registeredModuleNames():
            self.isDynamicModelerInstalled = True

    def setupNavigation(self):
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        navLayout.setContentsMargins(0, 0, 0, 0)
        
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.setToolTip("Go to the previous step.")
        self.prevButton.clicked.connect(self.onPrevButtonClicked)
        
        self.stepLabel = qt.QLabel("Step 1/6")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter)
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.nextButton = qt.QPushButton("Next")
        self.nextButton.setToolTip("Go to the next step.")
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        
        self.finishButton = qt.QPushButton("Finish")
        self.finishButton.setToolTip("Close this tool.")
        # --- THIS IS THE FIX for the main GUI window ---
        self.finishButton.clicked.connect(lambda: self.close())
        self.finishButton.hide()
        
        navLayout.addWidget(self.prevButton)
        navLayout.addStretch(1)
        navLayout.addWidget(self.stepLabel)
        navLayout.addStretch(1)
        navLayout.addWidget(self.nextButton)
        navLayout.addWidget(self.finishButton)
        
        self.mainLayout.addWidget(navWidget)

    def createStep0_FHPRealignment(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 1: FHP Realignment")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel("First, we need to realign the volume to the Frankfort Horizontal Plane for proper orientation.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        formLayout = qt.QFormLayout()
        
        self.inputVolumeSelector = slicer.qMRMLNodeComboBox()
        self.inputVolumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputVolumeSelector.setMRMLScene(slicer.mrmlScene)
        self.inputVolumeSelector.setToolTip("Pick the input CT volume to be realigned.")
        self.inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onVolumeSelected)
        formLayout.addRow("Input Volume: ", self.inputVolumeSelector)
        
        self.inputFiducialsSelector = slicer.qMRMLNodeComboBox()
        self.inputFiducialsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.inputFiducialsSelector.setMRMLScene(slicer.mrmlScene)
        self.inputFiducialsSelector.setToolTip("These are the landmarks to define the Frankfort Horizontal Plane.")
        formLayout.addRow("FHP Landmarks:", self.inputFiducialsSelector)
        
        layout.addLayout(formLayout)
        
        self.fhpInstructionLabel = qt.QLabel("Please place all three landmarks (poR, poL, zyoL) before proceeding.")
        self.fhpInstructionLabel.setWordWrap(True)
        layout.addWidget(self.fhpInstructionLabel)
        
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
        
        self.autoLoadLandmarksButton = qt.QPushButton("Auto-load FHP Landmarks")
        self.autoLoadLandmarksButton.setToolTip("Download and load standard FHP landmarks.")
        self.autoLoadLandmarksButton.clicked.connect(self.autoLoadFHPlandmarks)
        layout.addWidget(self.autoLoadLandmarksButton)

        self.skipFHPButton = qt.QPushButton("Skip this step (if already done)")
        self.skipFHPButton.setToolTip("Go directly to the next step without performing realignment.")
        self.skipFHPButton.clicked.connect(self.onSkipStep0)
        layout.addWidget(self.skipFHPButton)
        
        self.step0StatusLabel = qt.QLabel("Status: Please select input volume and landmarks.")
        self.step0StatusLabel.setWordWrap(True)
        layout.addWidget(self.step0StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
        
        self.inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onFHPSelect)
        self.inputFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onFHPSelect)

    def createStep1_ROICrop(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)

        title = qt.QLabel("Step 2 (Optional): Crop Volume with ROI")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc_text = """
            <p>If your volume is very large, you can draw an ROI (Region of Interest) box to speed up later steps. If not, just click 'Next'.</p>
            <p><b>To Crop the Volume:</b>
            <br>1. Click the '<b>Open Volume Rendering Module</b>' button below.
            <br>2. Find the '<b>Crop</b>' section and make sure '<b>Enable</b>' is ticked and the '<b>Display ROI</b>' eye icon is open.
            <br>3. Adjust the box to include all relevant features but exclude extra scanner material.
            <br>4. In this window, select '<b>Volume Rendering ROI</b>' from the 'ROI Node' dropdown.
            <br>5. Click the '<b>Crop Volume</b>' button. A new volume ending in '..._cropped' will be created and activated.</p>
        """
        desc = qt.QLabel(desc_text)
        desc.setTextFormat(qt.Qt.RichText)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        vr_button = qt.QPushButton(" Open Volume Rendering Module")
        vr_button.setIcon(qt.QIcon(":/Icons/VolumeRendering.png"))
        vr_button.setToolTip("Open the Volume Rendering module to help visualize the ROI placement.")
        vr_button.clicked.connect(lambda: slicer.util.selectModule("VolumeRendering"))
        layout.addWidget(vr_button)

        formLayout = qt.QFormLayout()
        self.roiNodeSelector = slicer.qMRMLNodeComboBox()
        self.roiNodeSelector.nodeTypes = ["vtkMRMLAnnotationROINode", "vtkMRMLMarkupsROINode"]
        self.roiNodeSelector.setMRMLScene(slicer.mrmlScene)
        self.roiNodeSelector.setToolTip("Select an ROI box you have drawn in the scene.")
        self.roiNodeSelector.noneEnabled = True
        formLayout.addRow("ROI Node:", self.roiNodeSelector)
        layout.addLayout(formLayout)

        self.cropVolumeButton = qt.QPushButton("Crop Volume")
        self.cropVolumeButton.setToolTip("Crop the input volume using the selected ROI.")
        self.cropVolumeButton.clicked.connect(self.onCropVolume)
        layout.addWidget(self.cropVolumeButton)

        self.step1StatusLabel = qt.QLabel("Status: Select an ROI and click 'Crop Volume', or skip this step.")
        self.step1StatusLabel.setWordWrap(True)
        layout.addWidget(self.step1StatusLabel)

        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep2_SegmentationOption(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 3: Segmentation Option")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel("Would you like to perform segmentation to create 3D models of the skull and soft tissue?")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        self.segmentationYesRadio = qt.QRadioButton("Yes, I want to perform segmentation")
        self.segmentationYesRadio.setChecked(True)
        self.segmentationNoRadio = qt.QRadioButton("No, skip segmentation steps")
        
        layout.addWidget(self.segmentationYesRadio)
        layout.addWidget(self.segmentationNoRadio)
        
        infoLabel = qt.QLabel(
            "Note: If you choose 'No', you will skip the segmentation steps and proceed directly "
            "to landmark placement. Use 'Shift' toggle in the 'VolumeRendering' module to switch between bone and soft tissue views")
        infoLabel.setWordWrap(True)
        infoLabel.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(infoLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep3_Segmentation(self):
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(15)
        
        title = qt.QLabel("Step 4: Create the Skull Model")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        mainLayout.addWidget(title)

        desc = qt.QLabel(
            "This step will help you create a 3D model of the bone using Slicer's built-in tools."
        )
        desc.setWordWrap(True)
        mainLayout.addWidget(desc)

        manualGroup = qt.QGroupBox("Guided Manual Segmentation")
        manualLayout = qt.QVBoxLayout(manualGroup)
        
        manualDesc = qt.QLabel(
            "Click the button below to switch to the Segment Editor and get step-by-step instructions."
        )
        manualDesc.setWordWrap(True)
        manualLayout.addWidget(manualDesc)
        
        self.setupBoneSegmentationButton = qt.QPushButton("Setup Bone Segmentation")
        self.setupBoneSegmentationButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;")
        self.setupBoneSegmentationButton.clicked.connect(self.setupBoneSegmentation)
        manualLayout.addWidget(self.setupBoneSegmentationButton)
        
        mainLayout.addWidget(manualGroup)

        confirmGroup = qt.QGroupBox("Model Confirmation")
        confirmLayout = qt.QFormLayout(confirmGroup)
        
        confirmLabel = qt.QLabel("Once your model is created, select it here to continue:")
        confirmLabel.setWordWrap(True)
        
        self.boneModelSelector = slicer.qMRMLNodeComboBox()
        self.boneModelSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.boneModelSelector.setMRMLScene(slicer.mrmlScene)
        self.boneModelSelector.addEnabled = False
        self.boneModelSelector.removeEnabled = False
        self.boneModelSelector.noneEnabled = True
        self.boneModelSelector.setToolTip("Select the 'Bone' model you created.")
        self.boneModelSelector.currentNodeChanged.connect(self.onConfirmBoneSegmentation)
        
        confirmLayout.addRow(confirmLabel)
        confirmLayout.addRow("Bone Model:", self.boneModelSelector)
        mainLayout.addWidget(confirmGroup)
        
        self.step3StatusLabel = qt.QLabel("Status: Ready to create bone model.")
        self.step3StatusLabel.setWordWrap(True)
        mainLayout.addWidget(self.step3StatusLabel)
        
        mainLayout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep4_SoftTissueSegmentation(self):
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(15)
        
        title = qt.QLabel("Step 5: Create the Skin Model")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        mainLayout.addWidget(title)
        
        desc = qt.QLabel(
            "Follow the same process as bone segmentation, but with different threshold values for skin."
        )
        desc.setWordWrap(True)
        mainLayout.addWidget(desc)
        
        manualGroup = qt.QGroupBox("Guided Manual Segmentation")
        manualLayout = qt.QVBoxLayout(manualGroup)

        manualDesc = qt.QLabel(
            "Click the button below to switch to the Segment Editor and get step-by-step instructions."
        )
        manualDesc.setWordWrap(True)
        manualLayout.addWidget(manualDesc)

        self.setupSkinSegmentationButton = qt.QPushButton("Setup Skin Segmentation")
        self.setupSkinSegmentationButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;")
        self.setupSkinSegmentationButton.clicked.connect(self.setupSkinSegmentation)
        manualLayout.addWidget(self.setupSkinSegmentationButton)
        mainLayout.addWidget(manualGroup)

        confirmGroup = qt.QGroupBox("Model Confirmation")
        confirmLayout = qt.QFormLayout(confirmGroup)
        
        confirmLabel = qt.QLabel("Once your model is created, select it here to continue:")
        confirmLabel.setWordWrap(True)
        
        self.softTissueModelSelector = slicer.qMRMLNodeComboBox()
        self.softTissueModelSelector.nodeTypes = ["vtkMRMLModelNode"]
        self.softTissueModelSelector.setMRMLScene(slicer.mrmlScene)
        self.softTissueModelSelector.addEnabled = False
        self.softTissueModelSelector.removeEnabled = False
        self.softTissueModelSelector.noneEnabled = True
        self.softTissueModelSelector.setToolTip("Select the 'Skin' model you created.")
        self.softTissueModelSelector.currentNodeChanged.connect(self.onConfirmSoftTissueSegmentation)
        
        confirmLayout.addRow(confirmLabel)
        confirmLayout.addRow("Skin Model:", self.softTissueModelSelector)
        mainLayout.addWidget(confirmGroup)
        
        self.step4StatusLabel = qt.QLabel("Status: Ready to create skin model.")
        self.step4StatusLabel.setWordWrap(True)
        mainLayout.addWidget(self.step4StatusLabel)
        
        mainLayout.addStretch(1)
        self.stepStack.addWidget(widget)

    def setupBoneSegmentation(self):
        self.setupSegmentation("Bone")

    def setupSkinSegmentation(self):
        self.setupSegmentation("Skin")

    def setupSegmentation(self, modelName):
        sourceVolume = self.croppedVolume if self.croppedVolume else self.inputVolume
        if not sourceVolume:
            slicer.util.errorDisplay("No source volume found. Please select one in Step 1.")
            return

        statusLabel = self.step3StatusLabel if modelName == "Bone" else self.step4StatusLabel
        statusLabel.setText(f"Status: Switching to Segment Editor module...")
        slicer.app.processEvents()

        try:
            slicer.util.selectModule('SegmentEditor')
            
            try:
                segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", f"{modelName}_Segmentation")
                segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(sourceVolume)
                
                topLevelWidget = slicer.modules.segmenteditor.widgetRepresentation()
                segmentEditorWidget = slicer.util.findChild(topLevelWidget, 'qMRMLSegmentEditorWidget')

                if segmentEditorWidget:
                    segmentEditorWidget.setSegmentationNode(segmentationNode)
                    segmentEditorWidget.setSourceVolumeNode(sourceVolume)
            except Exception as e:
                logging.info(f"Could not pre-configure Segment Editor, but this is okay. Error: {e}")
            
            statusLabel.setText("Status: Segment Editor is ready. Follow the instructions in the popup.")
            
            self.instructionDialog = InstructionDialog(modelName, self)
            self.instructionDialog.show()
            
        except Exception as e:
            slicer.util.errorDisplay(f"Could not automatically switch to Segment Editor. Please open it manually from the 'Modules' dropdown.\n\nError: {e}")

    def onConfirmBoneSegmentation(self, node):
        if node:
            self.boneModel = node
            self.step3StatusLabel.setText(f"Status: Confirmed '{node.GetName()}' as bone model. You can proceed.")
        else:
            self.boneModel = None
            self.step3StatusLabel.setText("Status: Waiting for bone model selection.")

    def onConfirmSoftTissueSegmentation(self, node):
        if node:
            self.softTissueModel = node
            self.step4StatusLabel.setText(f"Status: Confirmed '{node.GetName()}' as skin model. You can proceed.")
        else:
            self.softTissueModel = None
            self.step4StatusLabel.setText("Status: Waiting for skin model selection.")

    def createStep5_LandmarkPlacement(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 6: Landmark Placement")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        title.setAlignment(qt.Qt.AlignCenter)
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "Now that you have your models, you can load the landmark templates "
            "and place them on the appropriate models.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        buttonLayout = qt.QVBoxLayout()
        buttonLayout.setSpacing(10)
        
        self.loadHardLandmarksButton = qt.QPushButton("Load Hard Tissue Landmarks")
        self.loadHardLandmarksButton.clicked.connect(self.onDownloadHardLandmarks)
        buttonLayout.addWidget(self.loadHardLandmarksButton)
        
        self.loadSoftLandmarksButton = qt.QPushButton("Load Soft Tissue Landmarks") 
        self.loadSoftLandmarksButton.clicked.connect(self.onDownloadSoftLandmarks)
        buttonLayout.addWidget(self.loadSoftLandmarksButton)
        
        layout.addLayout(buttonLayout)
        
        instructions = qt.QLabel(
            "<b>Instructions:</b><br>"
            "1. Click the buttons above to load the landmark templates<br>"
            "2. Place the hard tissue landmarks on your 'Bone' model<br>"
            "3. Place the soft tissue landmarks on your 'Skin' model"
        )
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        exportGroup = qt.QGroupBox("Export Landmarks to Excel")
        exportLayout = qt.QVBoxLayout(exportGroup)
        
        exportInstructions = qt.QLabel(
            "Click the button below to copy all landmark names and RAS coordinates to the clipboard."
        )
        exportInstructions.setWordWrap(True)
        exportLayout.addWidget(exportInstructions)
        
        self.exportToClipboardButton = qt.QPushButton("Copy Landmarks to Clipboard")
        self.exportToClipboardButton.clicked.connect(self.exportLandmarksToClipboard)
        exportLayout.addWidget(self.exportToClipboardButton)
        
        layout.addWidget(exportGroup)
        
        self.step5StatusLabel = qt.QLabel("Status: Ready to load landmarks.")
        self.step5StatusLabel.setWordWrap(True)
        layout.addWidget(self.step5StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def onSkipStep0(self):
        if not self.inputVolumeSelector.currentNode():
            slicer.util.warningDisplay("Please select an input volume before skipping.")
            return
        
        self.currentStep += 1
        self.updateStepUI()

    def onVolumeSelected(self, node):
        self.inputVolume = node
        if node and node.GetTransformNodeID():
            self.undoFHPButton.setEnabled(True)
            self.step0StatusLabel.setText("Status: Loaded volume appears to be realigned. You can proceed or undo.")
        elif node:
            self.undoFHPButton.setEnabled(False)
        self.onFHPSelect()

    def onCropVolume(self):
        roiNode = self.roiNodeSelector.currentNode()
        if not self.inputVolume:
            slicer.util.warningDisplay("Please select an input volume in Step 1 first.")
            return
        if not roiNode:
            slicer.util.warningDisplay("Please select an ROI node to crop with.")
            return
        
        self.step1StatusLabel.setText("Status: Cropping volume...")
        slicer.app.processEvents()

        cropVolumeLogic = slicer.modules.cropvolume.logic()
        
        self.croppedVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", self.inputVolume.GetName() + "_cropped")
        
        cropVolumeLogic.CropVoxelBased(roiNode, self.inputVolume, self.croppedVolume)
        
        self.inputVolume.GetDisplayNode().SetVisibility(False)
        slicer.util.setSliceViewerLayers(background=self.croppedVolume)

        self.step1StatusLabel.setText(f"Status: Volume cropped successfully. The new volume '{self.croppedVolume.GetName()}' is now active.")
        slicer.util.showStatusMessage("Volume cropped!", 3000)
                
    def onFHPSelect(self):
        volumeNode = self.inputVolumeSelector.currentNode()
        fiducialNode = self.inputFiducialsSelector.currentNode()
        
        self.applyFHPButton.setEnabled(False)
        
        if volumeNode and fiducialNode:
            labels = [fiducialNode.GetNthControlPointLabel(i) for i in range(fiducialNode.GetNumberOfControlPoints())]
            
            has_poR = any('por' in label.lower() for label in labels)
            has_poL = any('pol' in label.lower() for label in labels) 
            has_zyoL = any('zyol' in label.lower() for label in labels)
            
            if has_poR and has_poL and has_zyoL:
                self.applyFHPButton.setEnabled(True)
                self.step0StatusLabel.setText("Status: Ready to apply FHP realignment.")
            else:
                self.step0StatusLabel.setText("Status: Please place all three landmarks (poR, poL, zyoL).")
        elif not volumeNode:
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
                if 'por' in label.lower(): poR_pos = np.array(pos)
                if 'pol' in label.lower(): poL_pos = np.array(pos)
                if 'zyol' in label.lower(): zyoL_pos = np.array(pos)

            if poR_pos is None or poL_pos is None or zyoL_pos is None:
                raise ValueError("Could not find all required landmarks (poR, poL, zyoL)")

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
        if not inputVolume: return
            
        transformNode = inputVolume.GetParentTransformNode()
        if transformNode:
            inputVolume.SetAndObserveTransformNodeID(None)
            slicer.mrmlScene.RemoveNode(transformNode)
            
        self.undoFHPButton.setEnabled(False)
        self.step0StatusLabel.setText("Status: FHP realignment undone.")
        slicer.util.showStatusMessage("FHP realignment undone!", 3000)

    def autoLoadFHPlandmarks(self):
        nodeName = "FHP_Standard_Landmarks"
        if slicer.mrmlScene.GetFirstNodeByName(nodeName):
            self.inputFiducialsSelector.setCurrentNode(slicer.mrmlScene.GetFirstNodeByName(nodeName))
            self.step0StatusLabel.setText("Status: FHP landmarks already loaded.")
            return
            
        self.step0StatusLabel.setText("Status: Downloading FHP landmarks...")
        slicer.app.processEvents()
        
        url = "https://github.com/user-attachments/files/22434441/FHP_landmarks.json"
        try:
            tempPath = os.path.join(slicer.app.temporaryPath, "FHP_landmarks.json")
            urllib.request.urlretrieve(url, tempPath)
            loadedNode = slicer.util.loadMarkups(tempPath)
            if loadedNode: 
                loadedNode.SetName(nodeName)
                self.inputFiducialsSelector.setCurrentNode(loadedNode)
                self.step0StatusLabel.setText("Status: FHP landmarks loaded successfully.")
        except Exception as e:
            self.step0StatusLabel.setText(f"Status: Error downloading landmarks: {e}")
            slicer.util.errorDisplay(f"Could not download landmarks file: {e}")

    def syncWithScene(self):
        if not self.boneModel: self.boneModel = slicer.util.getFirstNodeByName("Bone")
        if not self.softTissueModel: self.softTissueModel = slicer.util.getFirstNodeByName("Skin")
        
        if self.inputVolumeSelector.currentNode():
            self.onVolumeSelected(self.inputVolumeSelector.currentNode())

    def onDownloadHardLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/23121222/hard_tissue.mrk.json", "Hard_tissue_landmarks", self.step5StatusLabel)

    def onDownloadSoftLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/23121223/soft_tissue.mrk.json", "Soft_tissue_landmarks", self.step5StatusLabel)

    def onDownloadAndLoad(self, url, nodeName, statusLabel):
        statusLabel.setText(f"Status: Downloading '{nodeName}'..."); slicer.app.processEvents()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json') as tempFile:
                urllib.request.urlretrieve(url, tempFile.name)
                tempFilePath = tempFile.name
            
            loadedNode = slicer.util.loadMarkups(tempFilePath)
            if loadedNode:
                loadedNode.SetName(nodeName)
                statusLabel.setText(f"Status: Successfully loaded '{nodeName}'.")
            else:
                slicer.util.errorDisplay(f"Failed to load landmarks from {tempFilePath}.")

        except Exception as e:
            statusLabel.setText(f"Status: Error! Could not download. Error: {e}"); slicer.util.errorDisplay(f"Failed to download from the web. Error: {e}")
        finally:
            if 'tempFilePath' in locals() and os.path.exists(tempFilePath): 
                os.remove(tempFilePath)
    
    def onNextButtonClicked(self):
        stepComplete = False
        
        if self.currentStep == 0:
            isVolumeSelected = self.inputVolume is not None
            isVolumeTransformed = isVolumeSelected and self.inputVolume.GetTransformNodeID() is not None
            isUndoEnabled = self.undoFHPButton.isEnabled()
            stepComplete = isVolumeSelected and (isVolumeTransformed or isUndoEnabled)

        elif self.currentStep == 1:
            stepComplete = True
        elif self.currentStep == 2:
            self.wantsSegmentation = self.segmentationYesRadio.isChecked()
            stepComplete = True
        elif self.currentStep == 3:
            stepComplete = self.boneModel is not None
        elif self.currentStep == 4:
            stepComplete = self.softTissueModel is not None
        elif self.currentStep == 5:
            stepComplete = True

        if not stepComplete: 
            if self.currentStep == 0:
                slicer.util.warningDisplay("Please apply the FHP Realignment or use the 'Skip' button before proceeding.")
            elif self.currentStep == 3 or self.currentStep == 4:
                slicer.util.warningDisplay("Please create and/or select your model in the 'Model Confirmation' dropdown before proceeding.")
            else:
                slicer.util.warningDisplay(f"Please complete the current step before proceeding.")
            return
            
        nextStep = self.currentStep + 1
        if self.currentStep == 2 and not self.wantsSegmentation:
            nextStep = 5
        
        if nextStep < self.stepStack.count: 
            self.currentStep = nextStep
            self.updateStepUI()

    def onPrevButtonClicked(self):
        if self.currentStep > 0: 
            prevStep = self.currentStep - 1
            if self.currentStep == 5 and not self.wantsSegmentation:
                prevStep = 2
            self.currentStep = prevStep
            self.updateStepUI()

    def updateStepUI(self):
        self.stepStack.setCurrentIndex(self.currentStep)
        totalSteps = self.stepStack.count
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{totalSteps}")
        
        isLastStep = self.currentStep == totalSteps - 1
        self.nextButton.setVisible(not isLastStep)
        self.finishButton.setVisible(isLastStep)
        
        self.prevButton.setEnabled(self.currentStep > 0)

    def exportLandmarksToClipboard(self):
        try:
            landmark_nodes = slicer.mrmlScene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
            if landmark_nodes.GetNumberOfItems() == 0:
                slicer.util.warningDisplay("No landmark nodes found in the scene.")
                return

            landmarks_data = []
            for i in range(landmark_nodes.GetNumberOfItems()):
                node = landmark_nodes.GetItemAsObject(i)
                if node.GetNumberOfControlPoints() > 0 and "FHP_Standard_Landmarks" not in node.GetName():
                    for j in range(node.GetNumberOfControlPoints()):
                        pos = [0,0,0]
                        node.GetNthControlPointPositionWorld(j, pos)
                        landmarks_data.append({
                            'node': node.GetName(), 'label': node.GetNthControlPointLabel(j),
                            'x': pos[0], 'y': pos[1], 'z': pos[2]
                        })
            
            if not landmarks_data:
                slicer.util.warningDisplay("No landmarks with points found to export.")
                return

            landmarks_data.sort(key=lambda x: (x['node'], x['label']))
            
            clipboard_lines = ["Node Name\tLandmark Name\tRAS-X\tRAS-Y\tRAS-Z"]
            clipboard_lines.extend([f"{lm['node']}\t{lm['label']}\t{lm['x']:.3f}\t{lm['y']:.3f}\t{lm['z']:.3f}" for lm in landmarks_data])
            
            qt.QApplication.clipboard().setText("\n".join(clipboard_lines))
            
            num_landmarks = len(landmarks_data)
            self.step5StatusLabel.setText(f"Status: Copied {num_landmarks} landmarks to clipboard.")
            qt.QMessageBox.information(self, "Landmarks Copied", f"Copied {num_landmarks} landmarks to clipboard.\nYou can now paste into Excel or another spreadsheet program.")
            
        except Exception as e:
            slicer.util.errorDisplay(f"Error exporting landmarks: {str(e)}")
            self.step5StatusLabel.setText(f"Status: Error exporting landmarks: {str(e)}")

# --- Entry Point ---
try:
    slicer.util.findChild(slicer.util.mainWindow(), "LandmarkingGUI").deleteLater()
except:
    pass

landmarkingGui = LandmarkingGUI()
landmarkingGui.show()
```



### Using the GUI: Step-by-Step

After running the script, the "Landmarking" window will appear. Here is how to use it:

#### Step 1: FHP Realignment
This step orients your CT scan correctly.
1.  **Input Volume:** Select your loaded CT scan from the dropdown menu.
2.  **FHP Landmarks:** Click **"Auto-load FHP Landmarks"** to download the points needed, or select your own if you have them.
3.  
    <img width="750"  alt="GUI1" src="https://github.com/user-attachments/assets/c52ea595-ee2a-450f-a733-f4bc208039d3" />
    
Now, place them on the model - you may have to adjust the visiblility to see ONLY bone in the **Volume Renedering** module. Then, this button should be available to click:

<img width="473" height="222" alt="GUI2" src="https://github.com/user-attachments/assets/19579707-3326-4e25-b9d3-55ee81fefb5f" />


5.  **Apply Realignment:** Once the volume and landmarks are selected and placed, click **"Apply FHP Realignment"**.
6.  Click **"Next"**.



#### Step 2: Segmentation Option
Choose whether you need to create 3D models from your CT scan.
- If you already have 3D models (`.stl`, `.obj`), you can select **"No, skip segmentation steps"** and click **"Next"** to jump to Step 5.
- Otherwise, leave **"Yes"** selected and click **"Next"**.

#### Step 3: Skull Segmentation
Follow the instructions in the GUI to create a 3D model of the skull. The instructions are hidden by default; click on **"Show/Hide Segmentation Instructions"** to see them.





<img width="750"  alt="Segm step1" src="https://github.com/user-attachments/assets/daf08fba-e3af-4ab9-89e7-06662189099a" />

<img width="195" height="102" alt="Segm step2" src="https://github.com/user-attachments/assets/5a9ba052-dd7e-4b23-9fb8-cc8cfe48427f" />

<img width="1925" height="550" alt="Segm step3" src="https://github.com/user-attachments/assets/7b994fb2-9d08-42b9-aa74-4a63e7b5a0f0" />

<img width="750" height="1476" alt="Segm step4" src="https://github.com/user-attachments/assets/d8e13688-fa16-45fd-b796-36fe530e6381" />

<img width="750" height="27" alt="Segm step5" src="https://github.com/user-attachments/assets/dce389f8-d65d-4f48-ba7e-cfb4d008f519" />

<img width="750"  alt="Segm step6" src="https://github.com/user-attachments/assets/648f2f97-3541-44a1-bca4-fe234ab4121d" />

<img width="750"" alt="Segm step7" src="https://github.com/user-attachments/assets/66076a1b-6a28-49f7-a6bf-a401e492279e" />

<img width="750" alt="Segm step8" src="https://github.com/user-attachments/assets/644c2da7-f1ed-4279-b9a0-7122ad2b40a6" />





1.  Follow the numbered steps to create a segment, threshold it for bone, and export it as a model named "Bone".
2.  **Re-import** that "Bone" model back into Slicer.
3.  In the GUI, select your re-imported model in the **"Re-imported Bone Model"** dropdown.
4.  Click **"Next"**.


#### Step 4: Soft Tissue Segmentation
This is similar to the previous step, but for creating the soft tissue model.
1.  Follow the instructions to create a new segment using a different threshold.
2.  Name it, export it, and re-import it as "SoftTissue".
3.  Select it from the dropdown in the GUI.
4.  Click **"Next"**.

#### Step 5: Landmark Placement
This is the final step where you place the landmarks.
1.  Click **"Load Hard Tissue Landmarks"** and **"Load Soft Tissue Landmarks"**. This will add two new landmark lists to the scene.
2.  Select a landmark from the list and click on the corresponding model in the 3D view to place it.
3.  Once you have placed all your landmarks, use the **"Export Landmarks to Excel"** section. Click the **"Copy Landmarks to Clipboard"** button.
4.  You can now open Excel (or Google Sheets) and paste the data. It will be perfectly formatted in columns.

![Placeholder for image showing landmark export](https://placehold.co/600x400?text=Image:+Landmark+Placement+and+Export)

***

This format should make it much easier for a new user to follow along. You can now take screenshots of your GUI at each step and replace the `![Placeholder...` links with your actual images. Let me know if you'd like any more help with this!
