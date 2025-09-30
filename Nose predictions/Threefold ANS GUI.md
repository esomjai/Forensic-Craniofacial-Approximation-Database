'''python
# Threefold ANS Method GUI - Version 45 (Bug Fixes)
# A beginner-friendly, step-by-step tool for 3D Slicer.
#
# This version fixes two bugs from the previous merge:
# 1. Removes duplicated code in onAdjustMP to fix a Qt layout error.
# 2. Corrects a typo in createMidphiltrumGuide to fix a Python TypeError.

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile

class ThreefoldANSGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Threefold ANS Method")
        self.setObjectName("ThreefoldANSGUI") # Give the widget a unique name
        
        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setSpacing(10)
        
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        
        # Node storage
        self.landmarksNode = None
        self.referencePlane = None
        self.boneModel = None
        self.boneLeftModel = None
        self.boneRightModel = None
        self.vmjAcaLine = None
        self.nasalSpineVector = None
        self.subProLine = None
        self.predictedPronasaleNode = None
        self.trueSoftTissueNode = None # Added for Step 8
        
        # Observers and flags
        self.vmjObserver = None
        self.vectorObserver = None
        self.mpObserver = None
        self.isDynamicModelerInstalled = False
        self._isUpdatingVector = False
        self._isUpdatingMP = False
        self._initialMPPos = None
        self._mp_index = -1
        self.step6_complete = False
        self.step5_complete = False
        
        # --- This is the corrected structure ---
        self.createAllStepWidgets()
        self.setupNavigation()
        self.checkDependencies()
        self.syncWithScene()
        
        self.currentStep = 0
        self.updateStepUI()



    def createAllStepWidgets(self):
        self.createStep1_Welcome()
        self.createStep2_PlaneSetup()
        self.createStep3_Segmentation()
        self.createStep4_CutModel()
        self.createStep5_VMJ_Line()
        self.createStep6_VectorAndMidphiltrum()
        self.createStep7_PronasalePrediction()
        self.createStep8_Validation()
        self.createStep9_Results()

    def cleanup(self):
        """A dedicated method to remove all observers."""
        if self.vmjObserver and self.landmarksNode:
            self.landmarksNode.RemoveObserver(self.vmjObserver)
            self.vmjObserver = None
        if self.vectorObserver and self.nasalSpineVector:
            self.nasalSpineVector.RemoveObserver(self.vectorObserver)
            self.vectorObserver = None
        if self.mpObserver and self.landmarksNode:
            self.landmarksNode.RemoveObserver(self.mpObserver)
            self.mpObserver = None

    def checkDependencies(self):
        moduleName = "DynamicModeler" 
        if moduleName in slicer.app.moduleManager().factoryManager().registeredModuleNames():
            self.isDynamicModelerInstalled = True
        else:
            self.isDynamicModelerInstalled = False
            msgBox = qt.QMessageBox(); msgBox.setWindowTitle("Missing Required Extension")
            msgBox.setIcon(qt.QMessageBox.Warning); msgBox.setTextFormat(qt.Qt.RichText)
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
        self.stepLabel = qt.QLabel("Step 1/9")  # Changed from 1/8 to 1/9
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

    def createStep1_Welcome(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Welcome to the Threefold ANS Method"); title.setStyleSheet("font-weight: bold; font-size: 18px;"); title.setAlignment(qt.Qt.AlignCenter); layout.addWidget(title)
        desc = qt.QLabel("This tool will guide you through the workflow step-by-step.\n\nPlease begin by loading the required hard tissue landmarks using one of the options below."); desc.setWordWrap(True); layout.addWidget(desc)
        buttonLayout = qt.QVBoxLayout(); buttonLayout.setSpacing(10)
        self.loadLocalButton = qt.QPushButton("Load Landmarks from Local File"); self.loadLocalButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;"); self.loadLocalButton.setToolTip("Recommended: Load the '.mrk.json' file you saved on your computer."); self.loadLocalButton.clicked.connect(self.onLoadLocalLandmarks); buttonLayout.addWidget(self.loadLocalButton, 0, qt.Qt.AlignHCenter)
        self.downloadButton = qt.QPushButton("Download from Web"); self.downloadButton.setStyleSheet("background-color: #6c757d; color: white; padding: 8px;"); self.downloadButton.setToolTip("Convenient, but may fail if the temporary link expires."); self.downloadButton.clicked.connect(self.onDownloadLandmarks); buttonLayout.addWidget(self.downloadButton, 0, qt.Qt.AlignHCenter)
        layout.addLayout(buttonLayout)
        self.step1StatusLabel = qt.QLabel("Status: Waiting for user."); self.step1StatusLabel.setWordWrap(True); layout.addWidget(self.step1StatusLabel)
        layout.addStretch(1); self.stepStack.addWidget(widget)

    def createStep2_PlaneSetup(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 2: Create a Reference Plane"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        desc_html = """
        <p>Now, create a reference plane using the landmarks you just loaded.</p>
        <p>
            • <b>INB Plane</b>: Uses Nasion, Inion, and Bregma. This creates a simple three-point plane.<br><br>
            • <b>MSP (Best-Fit) Plane</b>: Uses multiple midsagittal landmarks (nasion, acanthion, prosthion, subspinale) to calculate a more robust, best-fit midsagittal plane.
        </p>
        """
        desc = qt.QLabel(desc_html); desc.setTextFormat(qt.Qt.RichText); desc.setWordWrap(True); layout.addWidget(desc)
        planeChoiceLayout = qt.QVBoxLayout(); planeChoiceLayout.setSpacing(10)
        self.planeChoiceComboBox = qt.QComboBox(); self.planeChoiceComboBox.addItems(["Select a method...", "INB (Inion-Nasion-Bregma)", "MSP (Midsagittal Best-Fit)"])
        self.createPlaneButton = qt.QPushButton("Create Plane"); self.createPlaneButton.clicked.connect(self.onCreatePlane)
        planeChoiceLayout.addWidget(self.planeChoiceComboBox); planeChoiceLayout.addWidget(self.createPlaneButton); layout.addLayout(planeChoiceLayout)
        self.step2StatusLabel = qt.QLabel("Status: Please choose a plane creation method."); self.step2StatusLabel.setWordWrap(True); layout.addWidget(self.step2StatusLabel)
        layout.addStretch(1); self.stepStack.addWidget(widget)

    def createStep3_Segmentation(self):
        widget = qt.QWidget()
        mainLayout = qt.QVBoxLayout(widget)
        mainLayout.setSpacing(15)
        
        title = qt.QLabel("Step 3: Segment, Export, and Re-import the Skull Model")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        mainLayout.addWidget(title)
        
        # Create scroll area for the detailed instructions
        scrollArea = qt.QScrollArea()
        scrollArea.setWidgetResizable(True)
        instructions_container = qt.QWidget()
        instructions_layout = qt.QVBoxLayout(instructions_container)
        instructions_layout.setContentsMargins(0,0,0,0)
        scrollArea.setWidget(instructions_container)
        
        # Original detailed instructions
        instructions = qt.QLabel()
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setOpenExternalLinks(True)
        instructions.setWordWrap(True)
        instructions.setText(
            "Follow these steps carefully to create a clean 'Bone' model for the next steps.<br><br>"
            "<b>1. Open Segment Editor:</b> Click this button to open the module.<br>"
        )
        instructions_layout.addWidget(instructions)
        
        self.openSegmentEditorButton = qt.QPushButton("Open Segment Editor Module")
        self.openSegmentEditorButton.clicked.connect(lambda: slicer.util.selectModule('SegmentEditor'))
        instructions_layout.addWidget(self.openSegmentEditorButton)
        
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
        instructions_layout.addWidget(instructions2)
        
        mainLayout.addWidget(scrollArea)
        mainLayout.addStretch(1)
        
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
        
        self.step3StatusLabel = qt.QLabel("Status: Waiting for user to select the re-imported 'Bone' model.")
        self.step3StatusLabel.setWordWrap(True)
        mainLayout.addWidget(self.step3StatusLabel)
        
        self.stepStack.addWidget(widget)
    def createStep4_CutModel(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(10)
        title = qt.QLabel("Step 4: Cut the Bone Model"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        
        open_modeller_layout = qt.QHBoxLayout()
        open_modeller_label = qt.QLabel("<b>1.</b> First, click the button to open the Dynamic Modeler module.")
        open_modeller_label.setTextFormat(qt.Qt.RichText)
        self.openDynamicModelerButton = qt.QPushButton("Open Dynamic Modeler")
        self.openDynamicModelerButton.clicked.connect(self.onOpenDynamicModeler)
        open_modeller_layout.addWidget(open_modeller_label); open_modeller_layout.addStretch(); open_modeller_layout.addWidget(self.openDynamicModelerButton)
        layout.addLayout(open_modeller_layout)
        
        layout.addSpacing(15) 

        roi_tip_label = qt.QLabel()
        roi_tip_label.setTextFormat(qt.Qt.RichText)
        roi_tip_label.setWordWrap(True)
        roi_tip_label.setText(
            "<b>If your model is too large</b> or slow to process, you can use the 'ROI cut' tool to trim it down first:<br><br>"
            "&bull; Go to the <b>'Markups'</b> module and create a new <b>ROI</b>, drawing a box around the area you want to keep.<br><br>"
            "&bull; Return to the <b>'Dynamic Modeler'</b> module and use the <b>'ROI cut'</b> tool.<br><br>"
            "&bull; Set the 'Input Model' (your bone model) and the 'ROI node' (the box you just drew).<br><br>"
            "&bull; In 'Output nodes', find 'Clipped output model (inside)' and select your original model. This will <b>replace</b> it with the smaller version.<br><br>"
            "&bull; Click 'Apply' to finish."
        )
        layout.addWidget(roi_tip_label)
        
        layout.addSpacing(15)

        plane_cut_label = qt.QLabel(); plane_cut_label.setTextFormat(qt.Qt.RichText); plane_cut_label.setWordWrap(True)
        plane_cut_label.setText(
            "<b>2.</b> Now, for the main task, use the '<b>Plane Cut</b>' option in the Dynamic Modeler:<br><br>"
            "&bull; Set the 'Input Model' to your re-imported 'Bone' model and the 'Input Plane' to the reference plane you created in Step 2.<br><br>"
            "&bull; In the 'Parameters' line, tick <b>'Cap surface'</b> for better visibility and leave the 'Operation type' as 'Union'.<br><br>"
            "&bull; Make sure you create new models for each side. Choose <b>'Create new Model as...'</b> in the 'Output models' dropdowns.<br><br>"
            "&bull; Name them '<b>Bone_Left</b>' (for the negative side) and '<b>Bone_Right</b>' (for the positive side).<br><br>"
            "&bull; Click 'Apply' and hide the original 'Bone' model to see the result."
        )
        layout.addWidget(plane_cut_label)

        layout.addSpacing(15) 

        confirm_label = qt.QLabel("<b>3.</b> If you've created the cut models you're happy with, please choose the button below to proceed.")
        confirm_label.setTextFormat(qt.Qt.RichText); confirm_label.setWordWrap(True)
        layout.addWidget(confirm_label)
        
        self.confirmCutButton = qt.QPushButton("Confirm Model Cut")
        self.confirmCutButton.clicked.connect(self.onConfirmCut)
        layout.addWidget(self.confirmCutButton, 0, qt.Qt.AlignHCenter)
        
        layout.addSpacing(10)

        self.step4StatusLabel = qt.QLabel("Status: Waiting for user to cut the model.")
        self.step4StatusLabel.setWordWrap(True)
        layout.addWidget(self.step4StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep5_VMJ_Line(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 5: Confirm VMJ Landmark and Create the ANS measurement"); title.setStyleSheet("font-weight: bold; font-size: 16px;"); layout.addWidget(title)
        
        layout.addWidget(qt.QLabel("1. Manually adjust the 'VMJ' point position if needed."))
        layout.addWidget(qt.QLabel("2. Click to confirm the VMJ position."))
        self.confirmVMJButton = qt.QPushButton("Confirm VMJ Position"); self.confirmVMJButton.clicked.connect(self.onConfirmVMJ)
        layout.addWidget(self.confirmVMJButton)

        layout.addWidget(qt.QLabel("3. Click to create the 'VMJ-aca' line."))
        self.measureANSButton = qt.QPushButton("Create VMJ-aca Line"); self.measureANSButton.clicked.connect(self.onMeasureANS)
        self.measureANSButton.setEnabled(False) # Starts disabled
        layout.addWidget(self.measureANSButton)
        
        self.step5StatusLabel = qt.QLabel("Status: Please manually adjust VMJ point if needed, then confirm."); layout.addWidget(self.step5StatusLabel)
        self.stepStack.addWidget(widget)

    def createStep6_VectorAndMidphiltrum(self):
        # --- UI CHANGE: All sections and buttons are visible, but disabled initially ---
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        layout.addWidget(qt.QLabel("Step 6: Define ANS direction and Midphiltrum Point"))

        # Part A: Vector
        layout.addWidget(qt.QLabel("<b>Part A: Define the Nasal Spine Vector</b><br>Manipulate the purple vector to follow the nasal spine."))
        
        # Part B: Midphiltrum
        layout.addWidget(qt.QLabel("<b>Part B: Place the Midphiltrum (mp) Point</b>"))
        
        self.createMPGuideButton = qt.QPushButton("1. Create 'mp' Guide Point")
        self.createMPGuideButton.setToolTip("Creates the 'mp' point between subspinale and prosthion.")
        self.createMPGuideButton.clicked.connect(self.onCreateMPGuide)
        layout.addWidget(self.createMPGuideButton)

        self.adjustMPButton = qt.QPushButton("2. Adjust 'mp' Point"); self.adjustMPButton.clicked.connect(self.onAdjustMP)
        self.adjustMPButton.setEnabled(False) # --- Starts disabled
        layout.addWidget(self.adjustMPButton)
        
        self.confirmMPButton = qt.QPushButton("3. Confirm 'mp' Placement"); self.confirmMPButton.clicked.connect(self.onConfirmMP)
        self.confirmMPButton.setEnabled(False) # --- Starts disabled
        layout.addWidget(self.confirmMPButton)

        self.step6StatusLabel = qt.QLabel("Status: Align the purple vector, then create 'mp' point."); layout.addWidget(self.step6StatusLabel)
        self.stepStack.addWidget(widget)

    
    def createStep7_PronasalePrediction(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 7: Predict Pronasale")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        instructions = qt.QLabel()
        instructions.setTextFormat(qt.Qt.RichText)
        instructions.setOpenExternalLinks(True)
        instructions.setWordWrap(True)
        instructions.setText(
            "Set the parameters below and click the button to calculate the predicted pronasale position. "
            "The default value for the facial soft tissue thickness is based on "
            "<a href='https://link.springer.com/article/10.1007/s00414-023-03087-x'>Hona and Stephan 2024</a>."
        )
        layout.addWidget(instructions)
        
        formLayout = qt.QFormLayout()
        
        self.perpDistanceSpinBox = qt.QDoubleSpinBox()
        self.perpDistanceSpinBox.setRange(0, 100)
        self.perpDistanceSpinBox.setValue(11.5)
        self.perpDistanceSpinBox.setSuffix(" mm")
        formLayout.addRow("Perpendicular Distance from 'mp':", self.perpDistanceSpinBox)
        
        self.multiplierComboBox = qt.QComboBox()
        self.multiplierComboBox.addItem("3.0 × ANS (Krogman and Iscan, 1986)")
        self.multiplierComboBox.addItem("1.9 × ANS (Matsuda et al., 2023)")
        self.multiplierComboBox.currentIndex = 0  # Set 3x as default
        formLayout.addRow("Multiplier Method:", self.multiplierComboBox)
        
        self.showCylinderCheckbox = qt.QCheckBox("Show FSTT cylinder")
        self.showCylinderCheckbox.setToolTip("Visualize the FSTT as a 3D cylinder.")
        formLayout.addRow(self.showCylinderCheckbox)
        
        layout.addLayout(formLayout)
        
        self.predictPronasaleButton = qt.QPushButton("Predict Pronasale")
        self.predictPronasaleButton.clicked.connect(self.onPredictPronasale)
        layout.addWidget(self.predictPronasaleButton, 0, qt.Qt.AlignHCenter)
        
        self.step7StatusLabel = qt.QLabel("Status: Waiting for user to set parameters.")
        self.step7StatusLabel.setWordWrap(True)
        layout.addWidget(self.step7StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def onAdjustMP(self):
        try:
            # Find the existing mp point
            self._mp_index = self.findPointIndex("mp")
            
            # If mp point doesn't exist, create it first
            if self._mp_index == -1:
                self.createMidphiltrumGuide()
                self._mp_index = self.findPointIndex("mp")
                if self._mp_index == -1:
                    raise ValueError("Failed to create 'mp' point.")

            # Store initial position for constraint
            self._initialMPPos = np.zeros(3)
            self.landmarksNode.GetNthControlPointPositionWorld(self._mp_index, self._initialMPPos)

            # Just refocus on the point without activating placement mode
            slicer.modules.markups.logic().JumpSlicesToNthPointInMarkup(self.landmarksNode.GetID(), self._mp_index)

            # Remove any existing observer first
            if self.mpObserver and self.landmarksNode:
                self.landmarksNode.RemoveObserver(self.mpObserver)
                self.mpObserver = None

            # Add observer for constraint
            self.mpObserver = self.landmarksNode.AddObserver(
                slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.onMPModified
            )

            self.confirmMPButton.setEnabled(True)
            self.adjustMPButton.setEnabled(False)
            self.step6StatusLabel.setText("Status: Ready to adjust 'mp' point. Click and drag the point in the 3D view (movement is constrained to Y-axis).")
            
        except Exception as e:
            slicer.util.warningDisplay(f"Cannot start adjustment: {e}")

            

    def createStep8_Validation(self):
        # --- UI CHANGE: Buttons are enabled/disabled based on logic ---
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)  # This is the main layout
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 8: Validate Prediction (Optional)")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        self.downloadTrueButton = qt.QPushButton("Download/Load True Landmarks")
        self.downloadTrueButton.clicked.connect(self.onDownloadTrueLandmarks)
        layout.addWidget(self.downloadTrueButton)
        
        self.trueLandmarksSelector = slicer.qMRMLNodeComboBox()
        self.trueLandmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.trueLandmarksSelector.setMRMLScene(slicer.mrmlScene)
        self.trueLandmarksSelector.currentNodeChanged.connect(self.onTrueLandmarkSelected)
        layout.addWidget(self.trueLandmarksSelector)

        # Add instruction before the compare button:
        step8Instruction = qt.QLabel("Please allocate the true pronasale point on your CT scan or segmented model before proceeding")
        step8Instruction.wordWrap = True
        layout.addWidget(step8Instruction)  # Use 'layout' not 'self.step8Layout'
        
        self.compareButton = qt.QPushButton("Compare True vs. Predicted")
        self.compareButton.clicked.connect(self.onComparePronasale)
        self.compareButton.setEnabled(False)  # Starts disabled
        layout.addWidget(self.compareButton)
        
        self.step8StatusLabel = qt.QLabel("Status: Waiting for user.")
        layout.addWidget(self.step8StatusLabel)
        
        self.stepStack.addWidget(widget)

    def createStep9_Results(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 9: Results and Validation")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        # Results table
        resultsLabel = qt.QLabel("Prediction Results:")
        layout.addWidget(resultsLabel)
        
        # Create table widget with checkbox column
        self.resultsTable = qt.QTableWidget()
        self.resultsTable.setRowCount(3)
        self.resultsTable.setColumnCount(5)  # Added one column for checkboxes
        self.resultsTable.setHorizontalHeaderLabels(["Select", "Metric", "X", "Y", "Z"])
        
        # Set row data with checkboxes in first column
        row_metrics = ["Predicted Pronasale", "True Pronasale", "Error Distance"]
        
        for i, metric in enumerate(row_metrics):
            # Checkbox in first column
            checkbox_item = qt.QTableWidgetItem()
            checkbox_item.setFlags(qt.Qt.ItemIsUserCheckable | qt.Qt.ItemIsEnabled)
            checkbox_item.setCheckState(qt.Qt.Checked)
            self.resultsTable.setItem(i, 0, checkbox_item)
            
            # Metric in second column
            metric_item = qt.QTableWidgetItem(metric)
            metric_item.setFlags(qt.Qt.ItemIsEnabled)  # Not editable
            self.resultsTable.setItem(i, 1, metric_item)
            
            # Initialize empty data columns
            self.resultsTable.setItem(i, 2, qt.QTableWidgetItem(""))
            self.resultsTable.setItem(i, 3, qt.QTableWidgetItem(""))
            self.resultsTable.setItem(i, 4, qt.QTableWidgetItem(""))
        
        self.resultsTable.horizontalHeader().setStretchLastSection(True)
        self.resultsTable.setMinimumHeight(150)
        layout.addWidget(self.resultsTable)
        
        # Copy to clipboard button
        self.copyButton = qt.QPushButton("Copy Selected to Clipboard")
        self.copyButton.clicked.connect(self.onCopyToClipboard)
        layout.addWidget(self.copyButton)
        
        # Finish button
        self.finishButton = qt.QPushButton("Finish")
        self.finishButton.clicked.connect(self.onFinish)
        layout.addWidget(self.finishButton)
        
        self.step9StatusLabel = qt.QLabel("Status: Complete! Review results above.")
        layout.addWidget(self.step9StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def onCopyToClipboard(self):
        """Copy selected results to clipboard"""
        try:
            clipboard_text = "Metric\tX\tY\tZ\n"
            
            for row in range(self.resultsTable.rowCount()):
                # Check if checkbox in first column is checked
                checkbox_item = self.resultsTable.item(row, 0)
                if checkbox_item and checkbox_item.checkState() == qt.Qt.Checked:
                    metric_item = self.resultsTable.item(row, 1)
                    x_item = self.resultsTable.item(row, 2)
                    y_item = self.resultsTable.item(row, 3)
                    z_item = self.resultsTable.item(row, 4)
                    
                    metric = metric_item.text() if metric_item else ""
                    x_val = x_item.text() if x_item else ""
                    y_val = y_item.text() if y_item else ""
                    z_val = z_item.text() if z_item else ""
                    
                    clipboard_text += f"{metric}\t{x_val}\t{y_val}\t{z_val}\n"
            
            # Copy to clipboard - FIXED: Use different variable name to avoid conflict
            from qt import QApplication
            app_clipboard = QApplication.clipboard()  # Changed variable name
            app_clipboard.setText(clipboard_text)     # Use the new variable name
            slicer.util.infoDisplay("Selected results copied to clipboard!")
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to copy to clipboard: {e}")
    def updateResultsTable(self):
        """Update the results table with current data"""
        try:
            # Get predicted pronasale position
            if self.predictedPronasaleNode and self.predictedPronasaleNode.GetNumberOfControlPoints() > 0:
                pred_pos = [0, 0, 0]
                self.predictedPronasaleNode.GetNthControlPointPositionWorld(0, pred_pos)
                self.resultsTable.item(0, 2).setText(f"{pred_pos[0]:.2f}")
                self.resultsTable.item(0, 3).setText(f"{pred_pos[1]:.2f}")
                self.resultsTable.item(0, 4).setText(f"{pred_pos[2]:.2f}")
            
            # Get true pronasale position
            if self.trueSoftTissueNode:
                true_pos = [0, 0, 0]
                # Find the pronasale point in true landmarks
                for i in range(self.trueSoftTissueNode.GetNumberOfControlPoints()):
                    label = self.trueSoftTissueNode.GetNthControlPointLabel(i)
                    if "pronasale" in label.lower():
                        self.trueSoftTissueNode.GetNthControlPointPositionWorld(i, true_pos)
                        self.resultsTable.item(1, 2).setText(f"{true_pos[0]:.2f}")
                        self.resultsTable.item(1, 3).setText(f"{true_pos[1]:.2f}")
                        self.resultsTable.item(1, 4).setText(f"{true_pos[2]:.2f}")
                        
                        # Calculate error distance
                        if self.predictedPronasaleNode and self.predictedPronasaleNode.GetNumberOfControlPoints() > 0:
                            pred_pos = [0, 0, 0]
                            self.predictedPronasaleNode.GetNthControlPointPositionWorld(0, pred_pos)
                            error_distance = np.linalg.norm(np.array(pred_pos) - np.array(true_pos))
                            self.resultsTable.item(2, 2).setText(f"{error_distance:.2f}")
                            self.resultsTable.item(2, 3).setText("")  # Clear Y column for error distance
                            self.resultsTable.item(2, 4).setText("")  # Clear Z column for error distance
                        break
            else:
                # If no true landmarks, clear the true pronasale and error rows
                self.resultsTable.item(1, 2).setText("")
                self.resultsTable.item(1, 3).setText("")
                self.resultsTable.item(1, 4).setText("")
                self.resultsTable.item(2, 2).setText("")
                self.resultsTable.item(2, 3).setText("")
                self.resultsTable.item(2, 4).setText("")
            
        except Exception as e:
            print(f"Error updating results table: {e}")

    def onFinish(self):
        """Close the GUI"""
        self.close()
    
    def onShowMidphiltrumSection(self):
        """Reveals the midphiltrum placement section within Step 6."""
        self.midphiltrumContainer.setVisible(True)
        self.guideForMidphiltrumButton.setEnabled(False)
        self.guideForMidphiltrumButton.setText("Midphiltrum Section Unlocked")
        self.step6StatusLabel.setText("Status: Vector set. Now check the 'mp' point.")
        self.createMidphiltrumGuide()


    def syncWithScene(self):
        self.landmarksNode = slicer.util.getFirstNodeByName("KrogmanIscan_hard_tissue")
        if self.landmarksNode: self.step1StatusLabel.setText("Status: Found 'KrogmanIscan_hard_tissue'.")
        
        self.referencePlane = slicer.util.getFirstNodeByName("INB") or slicer.util.getFirstNodeByName("MSP")
        if self.referencePlane: self.step2StatusLabel.setText(f"Status: Found '{self.referencePlane.GetName()}'.")
        
        self.boneModel = slicer.util.getFirstNodeByName("Bone")
        if self.boneModel: self.boneModelSelector.setCurrentNode(self.boneModel)
        
        self.onConfirmCut(updateStatusOnly=True)
        
        # Updated Step 5 logic
        self.vmjAcaLine = slicer.util.getFirstNodeByName("VMJ-aca")
        if self.vmjAcaLine:
            self.confirmVMJButton.setEnabled(False)
            self.measureANSButton.setEnabled(False)
            self.step5_complete = True
            self.step5StatusLabel.setText("Status: Found 'VMJ-aca' line. Step complete.")
        elif self.landmarksNode and self.findPointIndex("vmj") != -1:
            # VMJ point exists but line not created yet
            self.confirmVMJButton.setEnabled(True)
            self.measureANSButton.setEnabled(False)
            self.step5StatusLabel.setText("Status: Found VMJ point. Please confirm position.")

        self.nasalSpineVector = slicer.util.getFirstNodeByName("nasal spine vector")
        
        # This is the key logic for saved scenes:
        if self.landmarksNode and self.findPointIndex("mp") != -1:
            self._mp_index = self.findPointIndex("mp")
            self.createMPGuideButton.setEnabled(False)
            self.adjustMPButton.setEnabled(True)
            self.confirmMPButton.setEnabled(True)
            self.step6StatusLabel.setText("Status: Found existing 'mp' point. Please adjust and/or confirm.")
        
        self.predictedPronasaleNode = slicer.util.getFirstNodeByName("predicted pronasale")
        self.trueSoftTissueNode = slicer.util.getFirstNodeByName("KrogmanIscan_soft_tissue")
        if self.trueSoftTissueNode: self.trueLandmarksSelector.setCurrentNode(self.trueSoftTissueNode)

    def findPointIndex(self, name):
        """Helper function to find the index of a point by name."""
        if not self.landmarksNode:
            return -1

        for i in range(self.landmarksNode.GetNumberOfControlPoints()):
            label = self.landmarksNode.GetNthControlPointLabel(i)
            if name.lower() in label.lower():
                return i

        return -1

    def getPos(self, name, node=None):
        """Get the position of a landmark by name from the specified node or the default landmarks node."""
        landmark_node = node if node is not None else self.landmarksNode
        if not landmark_node:
            raise ValueError("Landmarks node not found.")
        
        for i in range(landmark_node.GetNumberOfControlPoints()):
            if name.lower() in landmark_node.GetNthControlPointLabel(i).lower():
                pos = np.zeros(3)
                landmark_node.GetNthControlPointPositionWorld(i, pos)
                return pos
        
        raise ValueError(f"Landmark '{name}' not found in the specified node!")

    def onLoadLocalLandmarks(self, fileName=None, nodeName=None):
        if not fileName: fileName, _ = qt.QFileDialog.getOpenFileName(self, "Load Landmarks", "", "Markup JSON Files (*.mrk.json)")
        if fileName:
            loadedNode = slicer.util.loadMarkups(fileName)
            if loadedNode:
                finalName = nodeName if nodeName else "KrogmanIscan_hard_tissue"
                loadedNode.SetName(finalName)
                if finalName == "KrogmanIscan_hard_tissue":
                    self.landmarksNode = loadedNode
                    self.step1StatusLabel.setText("Status: Successfully loaded 'KrogmanIscan_hard_tissue'.")
                elif finalName == "KrogmanIscan_soft_tissue":
                    self.trueSoftTissueNode = loadedNode
                    self.trueLandmarksSelector.setCurrentNode(loadedNode)
                    self.step8StatusLabel.setText("Status: Successfully loaded 'KrogmanIscan_soft_tissue'.")
                slicer.util.showStatusMessage(f"'{finalName}' loaded!", 3000)
            else: slicer.util.errorDisplay(f"Failed to load landmarks from {fileName}.")

    def onDownloadLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/20212533/KrogmanIscan_hard_tissue.mrk.json", "KrogmanIscan_hard_tissue", self.step1StatusLabel)

    def onDownloadTrueLandmarks(self):
        self.onDownloadAndLoad("https://github.com/user-attachments/files/20234679/KrogmanIscan_soft_tissue.mrk.json", "KrogmanIscan_soft_tissue", self.step8StatusLabel)

    def onDownloadAndLoad(self, url, nodeName, statusLabel):
        statusLabel.setText("Status: Downloading..."); slicer.app.processEvents()
        try:
            with urllib.request.urlopen(url) as response: fileData = response.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile: tempFile.write(fileData); tempFilePath = tempFile.name
            self.onLoadLocalLandmarks(tempFilePath, nodeName)
        except Exception as e:
            statusLabel.setText(f"Status: Error! Could not download. Error: {e}"); slicer.util.errorDisplay(f"Failed to download from the web. Error: {e}")
        finally:
            if 'tempFilePath' in locals() and os.path.exists(tempFilePath): os.remove(tempFilePath)

    def onCreatePlane(self):
        if not self.landmarksNode: self.syncWithScene()
        if not self.landmarksNode: self.step2StatusLabel.setText("Status: Error! Please go back and load the landmarks first."); return
        choice_index = self.planeChoiceComboBox.currentIndex
        if choice_index == 0: self.step2StatusLabel.setText("Status: Error! Please select a plane creation method."); return
        self.step2StatusLabel.setText("Status: Creating plane..."); slicer.app.processEvents()
        try:
            plane_name = ""
            if choice_index == 1:
                plane_name = "INB"; p_inion, p_nasion, p_bregma = self.getPos("inion"), self.getPos("nasion"), self.getPos("bregma")
                v1, v2 = p_nasion - p_inion, p_bregma - p_inion; normal, origin = np.cross(v1, v2), p_inion
            elif choice_index == 2:
                plane_name = "MSP"; required = ["nasion", "acanthion", "prosthion", "subspinale"]
                points = np.array([self.getPos(name) for name in required]); centroid = np.mean(points, axis=0)
                covariance_matrix = np.cov(points - centroid, rowvar=False); eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
                normal, origin = eigenvectors[:, np.argmin(eigenvalues)], centroid
            try: oldPlane = slicer.util.getNode(plane_name); slicer.mrmlScene.RemoveNode(oldPlane)
            except: pass
            planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', plane_name)
            planeNode.SetOrigin(origin); planeNode.SetNormal(normal); planeNode.SetSize(300, 300); planeNode.GetDisplayNode().SetOpacity(1.0)
            self.referencePlane = planeNode
            self.step2StatusLabel.setText(f"Status: Successfully created '{plane_name}' plane. You can now proceed.")
            slicer.util.showStatusMessage(f"'{plane_name}' created!", 3000)
        except Exception as e:
            self.step2StatusLabel.setText(f"Status: Error! Could not create plane. Error: {e}"); slicer.util.errorDisplay(f"Failed to create plane: {e}")

    def onConfirmSegmentation(self, node):
        if node:
            self.boneModel = node; self.step3StatusLabel.setText(f"Status: Confirmed '{self.boneModel.GetName()}' as the bone model. Ready to proceed!")
            slicer.util.showStatusMessage("Bone model confirmed!", 3000)
        else:
            self.boneModel = None; self.step3StatusLabel.setText("Status: Waiting for user to select the re-imported 'Bone' model.")
            
    def onOpenDynamicModeler(self):
        if not self.boneModel: slicer.util.warningDisplay("Please select the re-imported 'Bone' model in Step 3 before proceeding."); return
        if self.isDynamicModelerInstalled:
            slicer.util.selectModule('DynamicModeler')
            dynamicModelerWidget = slicer.modules.dynamicmodeler.widgetRepresentation()
            if dynamicModelerWidget:
                modelSelectors = dynamicModelerWidget.findChildren(slicer.qMRMLNodeComboBox)
                for selector in modelSelectors:
                    if "vtkMRMLModelNode" in selector.nodeTypes:
                        selector.setCurrentNode(self.boneModel); return
        else:
            qt.QMessageBox.warning(self, "Extension Not Found", "The 'Dynamic Modeler' extension is not installed.")

    def onConfirmCut(self, updateStatusOnly=False):
        if not updateStatusOnly: self.step4StatusLabel.setText("Status: Checking for cut models...")
        left_model_found, right_model_found = None, None
        all_models = slicer.util.getNodesByClass('vtkMRMLModelNode')
        for model in all_models:
            model_name = model.GetName().lower()
            if "bone" in model_name and "left" in model_name: left_model_found = model
            if "bone" in model_name and "right" in model_name: right_model_found = model
        
        if left_model_found and right_model_found:
            self.boneLeftModel = left_model_found; self.boneRightModel = right_model_found
            self.step4StatusLabel.setText(f"Status: Found '{left_model_found.GetName()}' and '{right_model_found.GetName()}'!")
            if not updateStatusOnly: slicer.util.showStatusMessage("Model cut confirmed!", 3000)
        elif not updateStatusOnly:
            self.step4StatusLabel.setText("Status: Error! Could not find models with 'bone' and 'left'/'right' in their names.")
            slicer.util.errorDisplay("Could not find the left and right bone models.")

    
    
    def onConfirmVMJ(self):
        try:
            # Simply confirm that VMJ exists and enable next step
            if not self.landmarksNode: 
                self.syncWithScene()
            if not self.landmarksNode:
                raise ValueError("Landmarks node not found.")
                
            vmj_index = self.findPointIndex("vmj")
            if vmj_index == -1:
                raise ValueError("VMJ point not found. Please ensure it exists in the landmarks.")
                
            self.step5StatusLabel.setText("Status: VMJ position confirmed. You can now create the line.")
            self.confirmVMJButton.setEnabled(False)
            self.measureANSButton.setEnabled(True)
            
        except Exception as e:
            self.step5StatusLabel.setText(f"Status: Error! {e}")
            slicer.util.errorDisplay(f"Failed to confirm VMJ: {e}")


    def onMeasureANS(self):
        self.step5StatusLabel.setText("Status: Searching for VMJ and acanthion landmarks...")
        try:
            if not self.landmarksNode: self.syncWithScene()
            if not self.landmarksNode: raise ValueError("Landmarks node 'KrogmanIscan_hard_tissue' not found.")
            acanthion_pos = self.getPos("acanthion")
            vmj_pos = self.getPos("vmj")
            self.step5StatusLabel.setText("Status: Landmarks found. Creating line...")
            try: oldLine = slicer.util.getNode('VMJ-aca'); slicer.mrmlScene.RemoveNode(oldLine)
            except: pass
            lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'VMJ-aca')
            lineNode.AddControlPoint(vmj_pos); lineNode.AddControlPoint(acanthion_pos)
            lineNode.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0); lineNode.GetDisplayNode().SetLineThickness(0.5)
            self.vmjAcaLine = lineNode
            self.step5StatusLabel.setText("Status: 'VMJ-aca' line created successfully! You can now proceed to the next step.")
            self.measureANSButton.setEnabled(False) # --- Disable the button after use
        except Exception as e:
            self.step5StatusLabel.setText(f"Status: Error! Could not create VMJ-aca line. {e}"); slicer.util.errorDisplay(f"Failed to create line: {e}")

    def createNasalSpineVector(self):
        self.step6StatusLabel.setText("Status: Creating nasal spine vector...")
        try:
            if not self.referencePlane: raise ValueError("Reference plane not found.")
            if not self.landmarksNode: raise ValueError("Landmarks node not found.")
            
            aca_pos = self.getPos("acanthion")

            plane_origin = np.array(self.referencePlane.GetOrigin())
            plane_normal = np.array(self.referencePlane.GetNormal())

            arbitrary_vec = np.array([0, 1, 0])
            direction_on_plane = arbitrary_vec - np.dot(arbitrary_vec, plane_normal) * plane_normal
            direction_on_plane /= np.linalg.norm(direction_on_plane)

            p1 = aca_pos + 30 * direction_on_plane
            p2 = aca_pos - 30 * direction_on_plane

            try: oldVector = slicer.util.getNode('nasal spine vector'); slicer.mrmlScene.RemoveNode(oldVector)
            except: pass
            
            self.nasalSpineVector = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'nasal spine vector')
            self.nasalSpineVector.AddControlPoint(p1); self.nasalSpineVector.AddControlPoint(p2)
            
            displayNode = self.nasalSpineVector.GetDisplayNode()
            displayNode.SetSelectedColor(0.8, 0.4, 0.8); displayNode.SetLineThickness(0.5)

            if self.vectorObserver: self.nasalSpineVector.RemoveObserver(self.vectorObserver)
            self.vectorObserver = self.nasalSpineVector.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.onNasalSpineVectorModified)
            self.step6StatusLabel.setText("Status: Please align the purple vector.")
            
        except Exception as e:
            self.step6StatusLabel.setText(f"Status: Error creating vector! {e}")
            slicer.util.errorDisplay(f"Failed to create nasal spine vector: {e}")

    def onNasalSpineVectorModified(self, caller, event):
        if self._isUpdatingVector: return
        self._isUpdatingVector = True
        try:
            lineNode = caller
            if not lineNode or lineNode.GetNumberOfControlPoints() != 2: self._isUpdatingVector = False; return

            plane_origin = np.array(self.referencePlane.GetOrigin())
            plane_normal = np.array(self.referencePlane.GetNormal())
            
            aca_pos = self.getPos("acanthion")

            lastModified = lineNode.GetDisplayNode().GetActiveControlPoint()
            p_moved = np.zeros(3)
            lineNode.GetNthControlPointPositionWorld(lastModified, p_moved)

            p_moved_on_plane = p_moved - (np.dot(p_moved - plane_origin, plane_normal) * plane_normal)
            
            new_dir = p_moved_on_plane - aca_pos
            if np.linalg.norm(new_dir) < 1e-6: self._isUpdatingVector = False; return
            new_dir /= np.linalg.norm(new_dir)
            
            p1 = np.zeros(3); lineNode.GetNthControlPointPositionWorld(0, p1)
            p2 = np.zeros(3); lineNode.GetNthControlPointPositionWorld(1, p2)
            dist = np.linalg.norm(p1 - p2) / 2.0
            
            new_p1 = aca_pos + dist * new_dir
            new_p2 = aca_pos - dist * new_dir

            lineNode.SetNthControlPointPositionWorld(0, new_p1)
            lineNode.SetNthControlPointPositionWorld(1, new_p2)
        finally:
            self._isUpdatingVector = False
            
    def createMidphiltrumGuide(self):
        try:
            sub_pos, pro_pos = self.getPos("subspinale"), self.getPos("prosthion")
            self.subProLine = slicer.util.getFirstNodeByName('subspinale-prosthion') or slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'subspinale-prosthion')
            self.subProLine.RemoveAllControlPoints()
            self.subProLine.AddControlPoint(sub_pos)
            self.subProLine.AddControlPoint(pro_pos)
            self.subProLine.GetDisplayNode().SetVisibility(True)
            mid_pos = (sub_pos + pro_pos) / 2.0
            
            # If mp point already exists, just update its position. Otherwise, create it.
            self._mp_index = self.findPointIndex("mp")
            if self._mp_index != -1:
                self.landmarksNode.SetNthControlPointPositionWorld(self._mp_index, mid_pos)
            else:
                self._mp_index = self.landmarksNode.AddControlPoint(mid_pos, "mp")
            
            self._initialMPPos = mid_pos.copy()
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to create 'mp' guide: {e}")

    def onCreateMPGuide(self):
        self.createMidphiltrumGuide()
        self.adjustMPButton.setEnabled(True)
        self.createMPGuideButton.setEnabled(False)
        self.step6StatusLabel.setText("Status: 'mp' point created. You may now adjust it.")


    def onMPModified(self, caller, event):
        if self._isUpdatingMP or self._mp_index == -1:
            return
            
        self._isUpdatingMP = True
        try:
            # Get current position of mp point
            current_pos = np.zeros(3)
            self.landmarksNode.GetNthControlPointPositionWorld(self._mp_index, current_pos)
            
            # Constrain to Y-axis only movement (keep X and Z at initial position)
            constrained_pos = [self._initialMPPos[0], current_pos[1], self._initialMPPos[2]]
            
            # Only update if the position actually changed
            if not np.allclose(current_pos, constrained_pos, atol=0.01):
                self.landmarksNode.SetNthControlPointPositionWorld(self._mp_index, constrained_pos)
            
        except Exception:
            # Silent fail - don't show error messages during normal operation
            pass
        finally:
            self._isUpdatingMP = False

    def onConfirmMP(self):
        self.step6StatusLabel.setText("Status: 'mp' point placement confirmed. Step complete!")
        
        # Remove observer
        if self.mpObserver and self.landmarksNode:
            self.landmarksNode.RemoveObserver(self.mpObserver)
            self.mpObserver = None
        
        # Reset flags
        self._isUpdatingMP = False
        
        self.confirmMPButton.setEnabled(False)
        self.step6_complete = True

    def onPredictPronasale(self):
        try:
            self.step7StatusLabel.setText("Status: Starting prediction...")
            if not all([self.boneModel, self.landmarksNode, self.vmjAcaLine, self.nasalSpineVector]): 
                raise ValueError("A required node from a previous step is missing.")
            
            mp_pos = self.getPos("mp")
            
            # Use 3D Slicer's coordinate system anterior direction
            # In RAS coordinate system: 
            # - Anterior is typically +Y axis (but let's verify)
            # - Let's use the actual scene coordinate system
            anterior_dir = np.array([0, 1, 0])  # Y-axis in RAS is usually anterior
            
            # Alternative: If you want to be more explicit about coordinate system:
            # anterior_dir = np.array([0, 1, 0])  # RAS: Y = Anterior
            # Or if using LPS: anterior_dir = np.array([0, -1, 0])
            
            # Make sure it's pointing in the correct anterior direction
            # We want it to point away from the skull surface (anterior)
            point_locator = vtk.vtkPointLocator()
            point_locator.SetDataSet(self.boneModel.GetPolyData())
            point_locator.BuildLocator()
            
            normals_filter = vtk.vtkPolyDataNormals()
            normals_filter.SetInputData(self.boneModel.GetPolyData())
            normals_filter.ComputePointNormalsOn()
            normals_filter.Update()
            
            avg_normal = np.array(normals_filter.GetOutput().GetPointData().GetNormals().GetTuple(
                point_locator.FindClosestPoint(mp_pos)))
            
            # FIX: Ensure the normal points ANTERIORLY (in the same general direction as anterior_dir)
            if np.dot(avg_normal, anterior_dir) < 0:
                avg_normal = -avg_normal
            
            perp_distance = self.perpDistanceSpinBox.value
            end_point_perp = mp_pos + avg_normal * perp_distance
            
            # Create FSTT line (perpendicular from mp)
            fstt_line = slicer.util.getFirstNodeByName("FSTT mp")
            if not fstt_line:
                fstt_line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "FSTT mp")
            fstt_line.RemoveAllControlPoints()
            fstt_line.AddControlPoint(mp_pos)
            fstt_line.AddControlPoint(end_point_perp)
            fstt_line.GetDisplayNode().SetSelectedColor(0, 1, 0)
            fstt_line.GetDisplayNode().SetLineThickness(0.3)
            
            # Create cylinder if requested
            cylinder_model = slicer.util.getFirstNodeByName("FSTT mp cylinder")
            if self.showCylinderCheckbox.checked:
                if not cylinder_model: 
                    cylinder_model = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "FSTT mp cylinder")
                
                # Ensure display node exists and is visible
                if not cylinder_model.GetDisplayNode():
                    cylinder_model.CreateDefaultDisplayNodes()
                display_node = cylinder_model.GetDisplayNode()
                display_node.SetVisibility(True)

                cylinder = vtk.vtkCylinderSource()
                cylinder.SetRadius(2.0)
                cylinder.SetHeight(perp_distance)
                cylinder.SetResolution(30)
                
                direction = end_point_perp - mp_pos
                vtk.vtkMath.Normalize(direction)
                center = mp_pos + 0.5 * perp_distance * direction
                
                transform = vtk.vtkTransform()
                initial_axis = [0, 1, 0]  # Cylinder initially along Y-axis
                rotation_axis = np.cross(initial_axis, direction)
                angle_rad = np.arccos(np.dot(initial_axis, direction))
                transform.Translate(center)
                transform.RotateWXYZ(np.rad2deg(angle_rad), rotation_axis)
                
                transform_polydata = vtk.vtkTransformPolyDataFilter()
                transform_polydata.SetTransform(transform)
                transform_polydata.SetInputConnection(cylinder.GetOutputPort())
                transform_polydata.Update()
                
                cylinder_model.SetAndObservePolyData(transform_polydata.GetOutput())
                
                # Safe color setting
                if display_node:
                    display_node.SetColor(1, 1, 0)  # Yellow
            elif cylinder_model:
                # Hide cylinder if checkbox is unchecked
                display_node = cylinder_model.GetDisplayNode()
                if display_node:
                    display_node.SetVisibility(False)
            
            # Calculate pronasale position (anterior projection)
            multiplier = 3.0 if self.multiplierComboBox.currentIndex == 0 else 1.9
            pronasale_pos = end_point_perp + anterior_dir * (self.vmjAcaLine.GetLineLengthWorld() * multiplier)
            
            # Create final prediction line
            final_line = slicer.util.getFirstNodeByName("pronasale_vector")
            if not final_line:
                final_line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "pronasale_vector")
            final_line.RemoveAllControlPoints()
            final_line.AddControlPoint(end_point_perp)
            final_line.AddControlPoint(pronasale_pos)
            final_line.GetDisplayNode().SetSelectedColor(0, 0, 1)
            final_line.GetDisplayNode().SetLineThickness(0.3)
            
            # Create predicted pronasale point
            self.predictedPronasaleNode = slicer.util.getFirstNodeByName("predicted pronasale")
            if not self.predictedPronasaleNode:
                self.predictedPronasaleNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "predicted pronasale")
            self.predictedPronasaleNode.RemoveAllControlPoints()
            self.predictedPronasaleNode.AddControlPoint(pronasale_pos, "pronasale")
            self.predictedPronasaleNode.GetDisplayNode().SetSelectedColor(1, 0, 0)
            self.predictedPronasaleNode.GetDisplayNode().SetGlyphScale(3.0)
            
            self.step7StatusLabel.setText("Status: Prediction complete!")
            
            # Enable comparison if true landmarks exist
            if self.trueSoftTissueNode: 
                self.compareButton.setEnabled(True)
                self.updateResultsTable() 
                
        except Exception as e: 
            self.step7StatusLabel.setText(f"Status: Error! {e}")
            slicer.util.errorDisplay(f"Prediction failed: {e}")
    
    def onTrueLandmarkSelected(self, node):
            self.trueSoftTissueNode = node
            # Enable the compare button only if both predicted and true nodes exist
            if self.predictedPronasaleNode and self.trueSoftTissueNode:
                self.compareButton.setEnabled(True)
                self.step8StatusLabel.setText("Status: Ready to compare.")
            else:
                self.compareButton.setEnabled(False)

    def onComparePronasale(self):
        try:
            self.step8StatusLabel.setText("Status: Comparing...")
            if not hasattr(self, 'predictedPronasaleNode') or not self.predictedPronasaleNode:
                raise ValueError("Predicted pronasale not found. Please complete Step 7.")
            if not hasattr(self, 'trueSoftTissueNode') or not self.trueSoftTissueNode:
                raise ValueError("True soft tissue landmarks not loaded or selected.")
            
            # Use a more robust approach to find the points
            predicted_pos = None
            true_pos = None
            
            # Find predicted position
            for i in range(self.predictedPronasaleNode.GetNumberOfControlPoints()):
                if "pronasale" in self.predictedPronasaleNode.GetNthControlPointLabel(i).lower():
                    predicted_pos = np.zeros(3)
                    self.predictedPronasaleNode.GetNthControlPointPositionWorld(i, predicted_pos)
                    break
                    
            # Find true position
            for i in range(self.trueSoftTissueNode.GetNumberOfControlPoints()):
                if "pronasale" in self.trueSoftTissueNode.GetNthControlPointLabel(i).lower():
                    true_pos = np.zeros(3)
                    self.trueSoftTissueNode.GetNthControlPointPositionWorld(i, true_pos)
                    break
                    
            if predicted_pos is None:
                raise ValueError("Could not find 'pronasale' in predicted landmarks")
            if true_pos is None:
                raise ValueError("Could not find 'pronasale' in true landmarks")
                
            # Create error visualization line
            error_line = slicer.util.getFirstNodeByName("prediction_error") or slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "prediction_error")
            if not error_line.GetDisplayNode():
                error_line.CreateDefaultDisplayNodes()
            
            error_line.RemoveAllControlPoints()
            error_line.AddControlPoint(predicted_pos)
            error_line.AddControlPoint(true_pos)
            error_line.GetDisplayNode().SetSelectedColor(1, 0, 0)  # Red
            
            error_distance = np.linalg.norm(predicted_pos - true_pos)
            self.step8StatusLabel.setText(f"Status: Comparison complete. Prediction Error: {error_distance:.2f} mm")
            
            # Update results table
            self.updateResultsTable()
            
        except Exception as e:
            self.step8StatusLabel.setText(f"Status: Error! {e}")
            slicer.util.errorDisplay(f"Comparison failed: {e}")

    def onPrevButtonClicked(self):
        if self.currentStep > 0: self.currentStep -= 1; self.updateStepUI()
            
    def onNextButtonClicked(self):
        self.syncWithScene() 
        stepComplete = False
        if self.currentStep == 0: stepComplete = self.landmarksNode is not None
        elif self.currentStep == 1: stepComplete = self.referencePlane is not None
        elif self.currentStep == 2: stepComplete = self.boneModel is not None
        elif self.currentStep == 3: stepComplete = self.boneLeftModel is not None and self.boneRightModel is not None
        elif self.currentStep == 4: stepComplete = self.step5_complete
        elif self.currentStep == 5: stepComplete = self.step6_complete 
        elif self.currentStep == 6: stepComplete = self.predictedPronasaleNode is not None
        elif self.currentStep == 7: stepComplete = True  # Step 8 is always complete
        elif self.currentStep == 8: stepComplete = True  # Step 9 is always complete

        if not stepComplete: 
            slicer.util.warningDisplay(f"Please complete Step {self.currentStep + 1} before proceeding.")
            return
            
        if self.currentStep < self.stepStack.count - 1: 
            self.currentStep += 1
            self.updateStepUI()
            
    def updateStepUI(self):
        self.cleanup()
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)
        
        is_vector_step = (self.currentStep == 5)
        
        # Manage visibility of items for Step 6
        if self.nasalSpineVector:
            self.nasalSpineVector.GetDisplayNode().SetVisibility(is_vector_step)
            self.nasalSpineVector.SetLocked(not is_vector_step)
        
        if self.subProLine:
            self.subProLine.GetDisplayNode().SetVisibility(is_vector_step)

        if is_vector_step:
            if not self.nasalSpineVector: 
                self.createNasalSpineVector()
            if self.nasalSpineVector and not self.vectorObserver:
                self.vectorObserver = self.nasalSpineVector.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.onNasalSpineVectorModified)

# --- Entry Point ---
try:
    mainWindow = slicer.util.mainWindow()
    old_gui = mainWindow.findChild(qt.QWidget, "ThreefoldANSGUI")
    if old_gui:
        if hasattr(old_gui, 'cleanup'): old_gui.cleanup()
        old_gui.deleteLater(); slicer.app.processEvents()
except Exception as e: print(f"Error during cleanup: {e}")

threefoldGui = ThreefoldANSGUI(); threefoldGui.show()
```
