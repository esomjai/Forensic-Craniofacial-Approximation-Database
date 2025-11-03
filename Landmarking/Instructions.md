# Landmarking Workflow GUI

[Soft_tissue_landmarks.mrk.json](https://github.com/user-attachments/files/23317570/Soft_tissue_landmarks.mrk.json)
[Hard_tissue_landmarks.mrk.json](https://github.com/user-attachments/files/23317568/Hard_tissue_landmarks.mrk.json)




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
        
        # --- THIS IS THE UPDATED BUTTON LIST ---
        # We now have a list of dictionaries, which is more flexible.
        # It lets us have different actions for different buttons.
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
                "action": slicer.util.openAddDataDialog # This function opens the "Add Data" dialog
            }
        ]

        for item in actions:
            # For "Add Data", the name is good. For modules, we add "Module" to the end.
            button_text = f" Open {item['name']}"
            if "Module" not in item["name"] and "Data" not in item["name"]:
                 button_text += " Module"

            btn = qt.QPushButton(button_text)
            btn.setIcon(qt.QIcon(item["icon"]))
            btn.clicked.connect(item["action"])
            buttonLayout.addWidget(btn)
        # --- END OF UPDATED BUTTON LIST ---

        self.mainLayout.addWidget(buttonGroup)

        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
       
        instructions_text = (
            f"<b>How to Create Your {modelName} Model</b><br><br>"
            f"This window will stay open while you work. You can move it to another screen.<br><br>"
            f"<b>Your Steps:</b><br>"
            f"1. <b>Add a Segment:A new, empty segmentation called '<b>{modelName}_Segmentation</b>' has been created for you in the 'Segment Editor' panel.<br><br>"
            f"2. <b>Select Threshold Tool:</b> From the list of tools, click on '<b>Threshold</b>' - it is in the top row on the right.<br>"
            f"3. <b>Adjust Threshold:</b> Use the 'Threshold Range' slider to select the tissue you want. For bone, a good starting point is 500. You will see the selected area highlighted and 'blinking' in the slice views.<br>"
            f"4. <b>Apply:</b> Once you are happy with the highlighted area, click the '<b>Apply</b>' button.<br>"
            f"5. <b>Show 3D Model:</b> At the top of the Segment Editor panel, click the '<b>Show 3D</b>' button. After a moment, your 3D model will appear!  <br>"
            f"6. <b>Now, click the green arrow next to the 'Show 3D' or click the '<b>Open Segmentations module</b>' button. Scroll down and open the '<b>Export/import models and labelmaps' as well as the '<b>Export to files</b>' dropdown menus. "
            f"7. <b> Make sure the following are chosen: '<b>Export</b>', '<b>Models</b>' in the fist section; then choose your folder to export to in the next section and click '<b>Export</b>'in the second section"
            f"8. <b> Re-import your saved model by clicking the '<b>Add Data</b>' widget on top of Slicer or in this window and choose the resently created STL file.  Check that this model now exists by clicking '<b>Open Models module</b>. "
            f"9. <b>Confirm:</b> Come back to this 'Landmarking' window and select your new model from the '<b>{modelName} Model</b>' dropdown menu to continue.<br><br>"
            f"<a href='{video_url}'>Click here to watch a tutorial video.</a>"
        )
        instructionLabel = qt.QLabel(instructions_text)
        instructionLabel.setTextFormat(qt.Qt.RichText)
        instructionLabel.setWordWrap(True)
        instructionLabel.setOpenExternalLinks(True)
        self.mainLayout.addWidget(instructionLabel)

        self.closeButton = qt.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
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
        self.finishButton.clicked.connect(self.close)
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
    <p>If your volume is very large, you can crop it with an ROI (Region of Interest) box to speed up later steps.</p>
    <p>If you don't need to crop, just click '<b>Next</b>' to skip this step.</p>
    
    <p><b>How to Crop the Volume:</b></p>
    <ol>
        <li>Click the '<b>Open Volume Rendering Module</b>' button below.</li>
        <li>In the Volume Rendering module, find the '<b>Crop</b>' section.</li>
        <li>Make sure '<b>Enable</b>' is checked (✓).</li>
        <li>Click the eye icon next to '<b>Display ROI</b>' to make the box visible.</li>
        <li>Adjust the red box in the 3D view to include all relevant anatomy but exclude extra scanner material.</li>
        <li>Come back to this window and select '<b>Volume Rendering ROI</b>' from the 'ROI Node' dropdown above.</li>
        <li>Click the '<b>Crop Volume</b>' button.</li>
        <li>A new volume ending in '<b>_cropped</b>' will be created and automatically activated! ✅</li>
    </ol>
    
    <p><i>Tip: Cropping is optional but recommended for very large scans.</i></p>
"""
        
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
        """
        Fully automated segmentation - no manual steps required!
        Creates a 3D model of bone or skin automatically.
        """
        sourceVolume = self.croppedVolume if self.croppedVolume else self.inputVolume
        if not sourceVolume:
            slicer.util.errorDisplay("No source volume found. Please select one in Step 1.")
            return

        statusLabel = self.step3StatusLabel if modelName == "Bone" else self.step4StatusLabel
        statusLabel.setText(f"Status: Creating {modelName} segmentation automatically...")
        slicer.app.processEvents()

        try:
            # Get the actual minimum and maximum values from the CT scan
            imageData = sourceVolume.GetImageData()
            minValue, maxValue = imageData.GetScalarRange()
            
            statusLabel.setText(f"Status: Analyzing CT scan (range: {minValue:.0f} to {maxValue:.0f})...")
            slicer.app.processEvents()
            
            # Step 1: Create a new segmentation node with a clean name
            segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", f"{modelName}_Segmentation")
            segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(sourceVolume)
            
            # Step 2: Create a new segment with the exact name we want (e.g., "Bone" or "Skin")
            # This is the key change - we're giving it the modelName directly!
            segment = segmentationNode.GetSegmentation().AddEmptySegment(modelName, modelName)
            segmentID = segment
            
            # Step 3: Set up the Segment Editor logic (this is the "brain" that does the work)
            segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
            segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
            segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
            segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
            segmentEditorWidget.setSegmentationNode(segmentationNode)
            segmentEditorWidget.setSourceVolumeNode(sourceVolume)
            
            # Step 4: Apply threshold automatically (this is like using the Threshold tool)
            statusLabel.setText(f"Status: Applying threshold for {modelName}...")
            slicer.app.processEvents()
            
            # Set the threshold range based on tissue type
            if modelName == "Bone":
                minThreshold = 500  # Bone typically starts at 500 HU (Hounsfield Units)
                maxThreshold = maxValue  # Use the highest value in the scan!
            else:  # Skin
                minThreshold = -500  # Soft tissue range
                maxThreshold = 500  # Soft tissue upper limit
            
            # Show the user what values we're using
            statusLabel.setText(f"Status: Using threshold {minThreshold:.0f} to {maxThreshold:.0f} for {modelName}...")
            slicer.app.processEvents()
            
            # Get the Threshold effect
            segmentEditorWidget.setActiveEffectByName("Threshold")
            effect = segmentEditorWidget.activeEffect()
            effect.setParameter("MinimumThreshold", str(minThreshold))
            effect.setParameter("MaximumThreshold", str(maxThreshold))
            effect.self().onApply()  # This is like clicking the "Apply" button
            
            # Step 5: Create the 3D model (this is like clicking "Show 3D")
            statusLabel.setText(f"Status: Creating 3D surface representation...")
            slicer.app.processEvents()
            
            # This creates the 3D visualization from the segmentation
            segmentationNode.CreateClosedSurfaceRepresentation()
            
            # Step 6: Export to a model node with the clean name!
            statusLabel.setText(f"Status: Exporting to model...")
            slicer.app.processEvents()
            
            # Create a model node with the EXACT name we want: "Bone" or "Skin"
            modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", modelName)
            
            # Export the segment to this specific model node
            segmentationLogic = slicer.modules.segmentations.logic()
            success = segmentationLogic.ExportSegmentToRepresentationNode(
                segmentationNode.GetSegmentation().GetSegment(segmentID),
                modelNode
            )
            
            if success:
                statusLabel.setText(f"Status: Model exported, applying colors...")
                slicer.app.processEvents()
                
                # Make the model look nice (set color based on tissue type)
                displayNode = modelNode.GetDisplayNode()
                if not displayNode:
                    modelNode.CreateDefaultDisplayNodes()
                    displayNode = modelNode.GetDisplayNode()
                
                if displayNode:
                    if modelName == "Bone":
                        displayNode.SetColor(0.9, 0.9, 0.8)  # Bone white color
                    else:
                        displayNode.SetColor(1.0, 0.8, 0.7)  # Skin peachy color
                    displayNode.SetOpacity(1.0)
                    displayNode.SetVisibility(True)
                
                # Automatically select it in the dropdown
                if modelName == "Bone":
                    self.boneModel = modelNode
                    self.boneModelSelector.setCurrentNode(modelNode)
                else:
                    self.softTissueModel = modelNode
                    self.softTissueModelSelector.setCurrentNode(modelNode)
                
                statusLabel.setText(f"Status: ✅ {modelName} model created successfully! (Threshold: {minThreshold:.0f} to {maxThreshold:.0f})")
                slicer.util.showStatusMessage(f"✅ {modelName} segmentation completed!", 3000)
                
                # Optional: Hide the segmentation node so only the model shows
                if segmentationNode.GetDisplayNode():
                    segmentationNode.GetDisplayNode().SetVisibility(False)
                
            else:
                raise Exception("Failed to export segment to model node")
            
            # Clean up the temporary segment editor node
            slicer.mrmlScene.RemoveNode(segmentEditorNode)
            
        except Exception as e:
            statusLabel.setText(f"Status: ❌ Error: {str(e)}")
            slicer.util.errorDisplay(f"Automatic segmentation failed:\n\n{str(e)}\n\nPlease try the manual method or report this issue.")
            import traceback
            traceback.print_exc()

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
        self.onDownloadAndLoad("https://github.com/user-attachments/files/23305190/Hard_tissue_landmarks.mrk.json", "Hard_tissue_landmarks", self.step5StatusLabel)

    def onDownloadSoftLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/23305193/Soft_tissue_landmarks.mrk.json", "Soft_tissue_landmarks", self.step5StatusLabel)

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

