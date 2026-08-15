```python
import os
import qt
import slicer
import vtk
import numpy as np
import urllib.request
import tempfile
import json
from collections import OrderedDict

class ThitiorulGUI:
    def __init__(self):
        """Initialize the GUI with multi-run comparison and save/load state features."""
        
        self.mainWidget = qt.QWidget()
        self.mainWidget.setWindowTitle("Thitiorul (2020) Nose Prediction Method")
        self.mainWidget.setMinimumSize(650, 800)
        self.mainWidget.setWindowFlags(qt.Qt.Tool)
        scrollArea = qt.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollContent = qt.QWidget()
        mainLayout = qt.QVBoxLayout(scrollContent)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        titleLabel = qt.QLabel("Thitiorul et al. (2020) Method")
        titleLabel.setStyleSheet("font-weight: bold; font-size: 16px;")
        titleLabel.setAlignment(qt.Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)
        
        self.prediction_runs = OrderedDict()
        self.colors = [[1, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0.5, 0], [0.5, 1, 0.5]]
        
        self.topLayout = mainLayout

        self.populateAllSteps(350)

        scrollArea.setWidget(scrollContent)
        outerLayout = qt.QVBoxLayout(self.mainWidget)
        outerLayout.setContentsMargins(0, 0, 0, 0)
        outerLayout.addWidget(scrollArea)
        
        self.refNasionNode = None
        self.hardTissueNode = None
        self.softTissueNode = None
        self.mspPlaneNode = None
        self.xzPlaneNode = None
        self.transformNode = None
        self.transform_applied = False

        self.syncWithScene()
        self.mainWidget.show()

    def createStepGroupBox(self, title, parentLayout):
        groupBox = qt.QGroupBox(title)
        groupBox.setLayout(qt.QVBoxLayout())
        parentLayout.addWidget(groupBox)
        return groupBox

    def setGuiState(self, transform_done):
        """Update UI state based on whether transform has been applied."""
        self.transform_applied = transform_done
        if transform_done:
            self.applyTransformButton.setText("✓ Transform Applied - Re-apply if needed")
            self.applyTransformButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        else:
            self.applyTransformButton.setText("Apply Transform (Set Nasion as Origin)")
            self.applyTransformButton.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 8px;")

    def populateAllSteps(self, buttonWidth):
        self.step1GroupBox = self.createStepGroupBox("Step 1: Load and Position Landmarks", self.topLayout)
        self.step2GroupBox = self.createStepGroupBox("Step 2: Apply Coordinate Transform", self.topLayout)
        self.step3GroupBox = self.createStepGroupBox("Step 3: Create Reference Planes", self.topLayout)
        self.step4GroupBox = self.createStepGroupBox("Step 4: Run Prediction", self.topLayout)
        self.step5GroupBox = self.createStepGroupBox("Step 5: Calculate Errors", self.topLayout)
        self.step6GroupBox = self.createStepGroupBox("Step 6: View and Export Results", self.topLayout)
        
        # Step 1 Layout - Load and Position
        step1Layout = self.step1GroupBox.layout()
        
        step1InfoLabel = qt.QLabel(
            "<b>Recommended Workflow:</b><br><br>"
            "1. Download and load <b>hard tissue</b> landmarks<br>"
            "2. Click 'Create Hard Guide Lines' to help positioning<br>"
            "3. Manually adjust hard tissue landmarks to match your scan<br>"
            "4. Download and load <b>soft tissue</b> landmarks<br>"
            "5. Click 'Create Soft Guide Lines' to help positioning<br>"
            "6. Manually adjust soft tissue landmarks to match your scan<br>"
            "7. When satisfied, proceed to Step 2<br><br>"
            "<b>Tip:</b> Pay special attention to nasion 'n' - it will become the origin!"
        )
        step1InfoLabel.setWordWrap(True)
        step1Layout.addWidget(step1InfoLabel)
        
        # Hard tissue section
        hardSeparator = qt.QFrame()
        hardSeparator.setFrameShape(qt.QFrame.HLine)
        hardSeparator.setFrameShadow(qt.QFrame.Sunken)
        step1Layout.addWidget(hardSeparator)
        
        hardLabel = qt.QLabel("<b>Hard Tissue Landmarks:</b>")
        step1Layout.addWidget(hardLabel)
        
        self.hardTissueSelector = slicer.qMRMLNodeComboBox()
        self.hardTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.hardTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.hardTissueSelector.noneEnabled = True
        step1Layout.addWidget(self.hardTissueSelector)
        
        self.downloadHardButton = qt.QPushButton("Download Hard Tissue Template")
        self.downloadHardButton.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        self.downloadHardButton.setFixedWidth(buttonWidth)
        self.downloadHardButton.clicked.connect(self.onDownloadHardLandmarksClicked)
        step1Layout.addWidget(self.downloadHardButton, 0, qt.Qt.AlignHCenter)
        
        self.createHardGuideLinesButton = qt.QPushButton("Create Hard Guide Lines")
        self.createHardGuideLinesButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px;")
        self.createHardGuideLinesButton.setFixedWidth(buttonWidth)
        self.createHardGuideLinesButton.clicked.connect(self.onCreateHardGuideLinesClicked)
        step1Layout.addWidget(self.createHardGuideLinesButton, 0, qt.Qt.AlignHCenter)
        
        # Soft tissue section
        softSeparator = qt.QFrame()
        softSeparator.setFrameShape(qt.QFrame.HLine)
        softSeparator.setFrameShadow(qt.QFrame.Sunken)
        step1Layout.addWidget(softSeparator)
        
        softLabel = qt.QLabel("<b>Soft Tissue Landmarks (for validation):</b>")
        step1Layout.addWidget(softLabel)
        
        self.softTissueSelector = slicer.qMRMLNodeComboBox()
        self.softTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.softTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.softTissueSelector.noneEnabled = True
        step1Layout.addWidget(self.softTissueSelector)
        
        self.downloadSoftButton = qt.QPushButton("Download Soft Tissue Template")
        self.downloadSoftButton.setStyleSheet("background-color: #8BC34A; color: white; font-weight: bold; padding: 8px;")
        self.downloadSoftButton.setFixedWidth(buttonWidth)
        self.downloadSoftButton.clicked.connect(self.onDownloadSoftLandmarksClicked)
        step1Layout.addWidget(self.downloadSoftButton, 0, qt.Qt.AlignHCenter)
        
        self.createSoftGuideLinesButton = qt.QPushButton("Create Soft Guide Lines")
        self.createSoftGuideLinesButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px;")
        self.createSoftGuideLinesButton.setFixedWidth(buttonWidth)
        self.createSoftGuideLinesButton.clicked.connect(self.onCreateSoftGuideLinesClicked)
        step1Layout.addWidget(self.createSoftGuideLinesButton, 0, qt.Qt.AlignHCenter)

        # Step 2 Layout - Transform
        step2Layout = self.step2GroupBox.layout()
        
        step2InfoLabel = qt.QLabel(
            "<b>Apply coordinate transform:</b><br>"
            "This sets hard tissue nasion 'n' as the origin (0,0,0).<br>"
            "All landmarks and guide lines will be automatically transformed."
        )
        step2InfoLabel.setWordWrap(True)
        step2Layout.addWidget(step2InfoLabel)
        
        self.applyTransformButton = qt.QPushButton("Apply Transform (Set Nasion as Origin)")
        self.applyTransformButton.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 8px;")
        self.applyTransformButton.setFixedWidth(buttonWidth)
        self.applyTransformButton.clicked.connect(self.onApplyTransformClicked)
        step2Layout.addWidget(self.applyTransformButton, 0, qt.Qt.AlignHCenter)
        
        # Step 3 Layout - Planes
        step3Layout = self.step3GroupBox.layout()
        
        step3InfoLabel = qt.QLabel(
            "<b>Create reference planes (optional):</b><br>"
            "Visualize the midsagittal plane and X-Z plane for verification."
        )
        step3InfoLabel.setWordWrap(True)
        step3Layout.addWidget(step3InfoLabel)
        
        self.createPlanesButton = qt.QPushButton("Create MSP and X-Z Plane")
        self.createPlanesButton.setStyleSheet("background-color: #FFDF00; font-weight: bold; padding: 8px;")
        self.createPlanesButton.setFixedWidth(buttonWidth)
        self.createPlanesButton.clicked.connect(self.onCreatePlanesClicked)
        step3Layout.addWidget(self.createPlanesButton, 0, qt.Qt.AlignHCenter)
        
        self.visualizeAxesButton = qt.QPushButton("Visualize Axes (optional)")
        self.visualizeAxesButton.setFixedWidth(buttonWidth)
        self.visualizeAxesButton.clicked.connect(self.onVisualizeAxesClicked)
        step3Layout.addWidget(self.visualizeAxesButton, 0, qt.Qt.AlignHCenter)

        # Step 4 Layout - Predict
        layout4 = self.step4GroupBox.layout()
        
        info4Label = qt.QLabel(
            "<b>Run soft tissue prediction:</b><br>"
            "Uses validated regression equations from the Thitiorul et al. (2020) paper."
        )
        info4Label.setWordWrap(True)
        layout4.addWidget(info4Label)
        
        methodInfoLabel = qt.QLabel(
            "• LEFT side hard tissue landmarks only<br>"
        )
        methodInfoLabel.setWordWrap(True)
        methodInfoLabel.setStyleSheet("margin-left: 20px; color: #666;")
        layout4.addWidget(methodInfoLabel)
        
        self.autoReplaceCheckbox = qt.QCheckBox("Auto-detect missing bilateral landmarks")
        self.autoReplaceCheckbox.setChecked(False)  # UNCHECKED by default
        self.autoReplaceCheckbox.setToolTip(
            "If a LEFT landmark is missing but RIGHT exists, automatically mirror the RIGHT landmark.\n\n"
            "Use this when:\n"
            "• Left side of skull is damaged or incomplete\n"
            "• You only have RIGHT side landmarks available\n\n"
            "Usually keep this UNCHECKED if you have complete landmarks."
        )
        layout4.addWidget(self.autoReplaceCheckbox)
        
        self.predictButton = qt.QPushButton("Run Prediction")
        self.predictButton.setStyleSheet("background-color: #00BCD4; color: white; font-weight: bold; padding: 8px;")
        self.predictButton.setFixedWidth(buttonWidth)
        self.predictButton.clicked.connect(self.onPredictClicked)
        layout4.addWidget(self.predictButton, 0, qt.Qt.AlignHCenter)
        
        # Step 5 Layout - Calculate Errors
        layout5 = self.step5GroupBox.layout()
        
        step5InfoLabel = qt.QLabel(
            "<b>Calculate prediction accuracy:</b><br>"
            "Compares predicted landmarks with the true soft tissue landmarks you placed."
        )
        step5InfoLabel.setWordWrap(True)
        layout5.addWidget(step5InfoLabel)
        
        self.calculateErrorsButton = qt.QPushButton("Calculate All Errors")
        self.calculateErrorsButton.setStyleSheet("background-color: #E91E63; color: white; font-weight: bold; padding: 8px;")
        self.calculateErrorsButton.setFixedWidth(buttonWidth)
        self.calculateErrorsButton.clicked.connect(self.onCalculateAllErrors)
        layout5.addWidget(self.calculateErrorsButton, 0, qt.Qt.AlignHCenter)

        # Step 6 Layout - Results
        layout6 = self.step6GroupBox.layout()
        
        step6InfoLabel = qt.QLabel("<b>View and export your results:</b>")
        step6InfoLabel.setWordWrap(True)
        layout6.addWidget(step6InfoLabel)
        
        self.resultsTable = qt.QTableWidget()
        self.resultsTable.setColumnCount(1)
        self.resultsTable.setHorizontalHeaderLabels(["Landmark"])
        
        landmarks = ["se'", "npp'", "npa'", "pn'", "nd'", "sn'", 
                     "al'L", "als'L", "alp'L", "ali'L", 
                     "al'R", "als'R", "alp'R", "ali'R"]
        self.resultsTable.setRowCount(len(landmarks))
        for i, name in enumerate(landmarks):
            self.resultsTable.setItem(i, 0, qt.QTableWidgetItem(name))
        
        self.resultsTable.setMinimumHeight(300)
        layout6.addWidget(self.resultsTable)
        
        # Export error results section
        errorExportLabel = qt.QLabel("<b>Export Error Results:</b>")
        layout6.addWidget(errorExportLabel)
        
        exportLayout = qt.QHBoxLayout()
        self.saveButton = qt.QPushButton("Save Summary to CSV")
        self.saveButton.setStyleSheet("background-color: #3f51b5; color: white; font-weight: bold; padding: 8px;")
        self.saveButton.clicked.connect(self.onSaveToCSV)
        self.copySummaryButton = qt.QPushButton("Copy Summary to Clipboard")
        self.copySummaryButton.clicked.connect(self.onCopySummaryToClipboard)
        exportLayout.addWidget(self.saveButton)
        exportLayout.addWidget(self.copySummaryButton)
        layout6.addLayout(exportLayout)
        
        # Separator
        separator = qt.QFrame()
        separator.setFrameShape(qt.QFrame.HLine)
        separator.setFrameShadow(qt.QFrame.Sunken)
        layout6.addWidget(separator)
        
        # Export landmark coordinates section
        landmarkExportLabel = qt.QLabel(
            "<b>Export Landmark Coordinates:</b><br>"
            "<small>Export your placed hard and soft tissue landmark coordinates</small>"
        )
        landmarkExportLabel.setWordWrap(True)
        layout6.addWidget(landmarkExportLabel)
        
        landmarkExportLayout = qt.QHBoxLayout()
        
        self.exportHardLandmarksButton = qt.QPushButton("Export Hard Tissue Coords")
        self.exportHardLandmarksButton.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        self.exportHardLandmarksButton.setToolTip("Export Thitiorul_hard_tissue landmark coordinates to CSV")
        self.exportHardLandmarksButton.clicked.connect(self.onExportHardLandmarks)
        landmarkExportLayout.addWidget(self.exportHardLandmarksButton)
        
        self.exportSoftLandmarksButton = qt.QPushButton("Export Soft Tissue Coords")
        self.exportSoftLandmarksButton.setStyleSheet("background-color: #8BC34A; color: white; padding: 8px;")
        self.exportSoftLandmarksButton.setToolTip("Export true_Thitiorul_soft_tissue landmark coordinates to CSV")
        self.exportSoftLandmarksButton.clicked.connect(self.onExportSoftLandmarks)
        landmarkExportLayout.addWidget(self.exportSoftLandmarksButton)
        
        layout6.addLayout(landmarkExportLayout)
        
        # Copy landmark coordinates to clipboard
        landmarkCopyLayout = qt.QHBoxLayout()
        
        self.copyHardLandmarksButton = qt.QPushButton("Copy Hard Coords to Clipboard")
        self.copyHardLandmarksButton.clicked.connect(self.onCopyHardLandmarks)
        landmarkCopyLayout.addWidget(self.copyHardLandmarksButton)
        
        self.copySoftLandmarksButton = qt.QPushButton("Copy Soft Coords to Clipboard")
        self.copySoftLandmarksButton.clicked.connect(self.onCopySoftLandmarks)
        landmarkCopyLayout.addWidget(self.copySoftLandmarksButton)
        
        layout6.addLayout(landmarkCopyLayout)
        
        # Separator
        separator2 = qt.QFrame()
        separator2.setFrameShape(qt.QFrame.HLine)
        separator2.setFrameShadow(qt.QFrame.Sunken)
        layout6.addWidget(separator2)
        
        self.showDetailedButton = qt.QPushButton("Show Detailed Results...")
        self.showDetailedButton.setStyleSheet("background-color: #795548; color: white; padding: 8px;")
        self.showDetailedButton.clicked.connect(self.onShowDetailedResultsClicked)
        layout6.addWidget(self.showDetailedButton)

    
    
    def onCopyToClipboard(self, table_widget):
        """Copies the content of a QTableWidget to the clipboard in tab-separated format."""
        try:
            # Use QApplication from PythonQt instead of qt
            app = qt.QApplication.instance()
            if not app:
                slicer.util.errorDisplay("Could not access clipboard.")
                return False
            
            clipboard = app.clipboard()
            if not clipboard:
                slicer.util.errorDisplay("Clipboard not available on this system.")
                return False
            
            text = ""
            
            # Headers
            headers = []
            for i in range(table_widget.columnCount):
                header_item = table_widget.horizontalHeaderItem(i)
                if header_item:
                    headers.append(header_item.text().replace("\n", " "))
                else:
                    headers.append(f"Column{i}")
            text += "\t".join(headers) + "\n"
            
            # Rows
            for row in range(table_widget.rowCount):
                row_data = []
                for col in range(table_widget.columnCount):
                    item = table_widget.item(row, col)
                    if item and item.text():
                        row_data.append(item.text().replace("\n", " "))
                    else:
                        row_data.append("")
                text += "\t".join(row_data) + "\n"
            
            # Set clipboard text
            clipboard.setText(text, qt.QClipboard.Clipboard)
            
            # Also set selection mode for Linux
            if clipboard.supportsSelection():
                clipboard.setText(text, qt.QClipboard.Selection)
            
            return True
                
        except Exception as e:
            slicer.util.errorDisplay(f"Error copying to clipboard: {e}")
            import traceback
            traceback.print_exc()
            return False

    def onCopySummaryToClipboard(self):
        """Copy the summary results table to clipboard."""
        try:
            # Check if there's actually data to copy
            if self.resultsTable.columnCount < 2:
                slicer.util.warningDisplay(
                    "No results to copy yet!\n\n"
                    "Please:\n"
                    "1. Run a prediction (Step 4)\n"
                    "2. Calculate errors (Step 5)\n"
                    "Then try copying again."
                )
                return
            
            # Check if there are any error values
            has_data = False
            for row in range(self.resultsTable.rowCount):
                if self.resultsTable.columnCount > 1:
                    item = self.resultsTable.item(row, 1)
                    if item and item.text():
                        has_data = True
                        break
            
            if not has_data:
                slicer.util.warningDisplay(
                    "No error data to copy!\n\n"
                    "Calculate errors first (Step 5), then try copying again."
                )
                return
            
            # Copy the data
            success = self.onCopyToClipboard(self.resultsTable)
            
            if success:
                slicer.util.showStatusMessage("✓ Results copied to clipboard!", 3000)
                slicer.util.infoDisplay("✓ Results copied to clipboard!\n\nYou can now paste into Excel or any text editor.")
            else:
                slicer.util.warningDisplay(
                    "Copy to clipboard may have failed.\n\n"
                    "Try using 'Save Summary to CSV' instead."
                )
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to copy to clipboard: {e}")
            import traceback
            traceback.print_exc()

    def export_landmark_coordinates(self, node_name, default_filename):
        """Export landmark coordinates to CSV file."""
        try:
            node = slicer.util.getNode(node_name)
            if not node:
                slicer.util.warningDisplay(f"'{node_name}' not found!\n\nPlease load the landmarks first.")
                return False
            
            result = qt.QFileDialog.getSaveFileName(
                self.mainWidget,
                f"Export {node_name} Coordinates",
                default_filename,
                "CSV Files (*.csv)"
            )
            fileName = result[0] if isinstance(result, tuple) else result
            if not fileName:
                return False
            
            csv_content = "Label,X,Y,Z,Description\n"
            
            for i in range(node.GetNumberOfControlPoints()):
                label = node.GetNthControlPointLabel(i)
                pos = node.GetNthControlPointPosition(i)
                description = node.GetNthControlPointDescription(i) if hasattr(node, 'GetNthControlPointDescription') else ""
                
                csv_content += f'"{label}",{pos[0]:.6f},{pos[1]:.6f},{pos[2]:.6f},"{description}"\n'
            
            with open(fileName, 'w') as f:
                f.write(csv_content)
            
            slicer.util.infoDisplay(f"✓ Coordinates exported!\n\nSaved to:\n{fileName}")
            return True
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to export coordinates: {e}")
            import traceback
            traceback.print_exc()
            return False

    def copy_landmark_coordinates(self, node_name):
        """Copy landmark coordinates to clipboard."""
        try:
            node = slicer.util.getNode(node_name)
            if not node:
                slicer.util.warningDisplay(f"'{node_name}' not found!\n\nPlease load the landmarks first.")
                return False
            
            text = "Label\tX\tY\tZ\tDescription\n"
            
            for i in range(node.GetNumberOfControlPoints()):
                label = node.GetNthControlPointLabel(i)
                pos = node.GetNthControlPointPosition(i)
                description = node.GetNthControlPointDescription(i) if hasattr(node, 'GetNthControlPointDescription') else ""
                
                text += f"{label}\t{pos[0]:.6f}\t{pos[1]:.6f}\t{pos[2]:.6f}\t{description}\n"
            
            # Use QApplication from instance
            app = qt.QApplication.instance()
            if not app:
                slicer.util.errorDisplay("Could not access clipboard.")
                return False
            
            clipboard = app.clipboard()
            if not clipboard:
                slicer.util.errorDisplay("Clipboard not available.")
                return False
            
            clipboard.setText(text, qt.QClipboard.Clipboard)
            if clipboard.supportsSelection():
                clipboard.setText(text, qt.QClipboard.Selection)
            
            slicer.util.showStatusMessage(f"✓ {node_name} coordinates copied!", 3000)
            slicer.util.infoDisplay(f"✓ Coordinates copied!\n\nLandmark set: {node_name}\nTotal landmarks: {node.GetNumberOfControlPoints()}")
            return True
            
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to copy coordinates: {e}")
            import traceback
            traceback.print_exc()
            return False

    def onExportHardLandmarks(self):
        """Export hard tissue landmark coordinates to CSV."""
        self.export_landmark_coordinates("Thitiorul_hard_tissue", "hard_tissue_coordinates.csv")

    def onExportSoftLandmarks(self):
        """Export soft tissue landmark coordinates to CSV."""
        self.export_landmark_coordinates("true_Thitiorul_soft_tissue", "soft_tissue_coordinates.csv")

    def onCopyHardLandmarks(self):
        """Copy hard tissue landmark coordinates to clipboard."""
        self.copy_landmark_coordinates("Thitiorul_hard_tissue")

    def onCopySoftLandmarks(self):
        """Copy soft tissue landmark coordinates to clipboard."""
        self.copy_landmark_coordinates("true_Thitiorul_soft_tissue")

    def syncWithScene(self):
        """Detect what has already been completed in the scene."""
        try:
            self.transformNode = slicer.util.getNode("MoveToOrigin")
            self.setGuiState(True)
        except:
            self.setGuiState(False)
        
        try:
            self.refNasionNode = slicer.util.getNode("reference_nasion")
        except:
            pass
        
        try:
            hard_node = slicer.util.getNode("Thitiorul_hard_tissue")
            self.hardTissueSelector.setCurrentNode(hard_node)
            self.hardTissueNode = hard_node
        except:
            pass
        
        try:
            soft_node = slicer.util.getNode("true_Thitiorul_soft_tissue")
            self.softTissueSelector.setCurrentNode(soft_node)
            self.softTissueNode = soft_node
        except:
            pass
        
        try:
            self.mspPlaneNode = slicer.util.getNode("MSP")
            self.xzPlaneNode = slicer.util.getNode("X-Z plane")
        except:
            pass
        
        try:
            pred_node = slicer.util.getNode("Predicted_Thitiorul")
            if pred_node and "thitiorul" not in self.prediction_runs:
                self.prediction_runs["thitiorul"] = {
                    'node_id': pred_node.GetID(),
                    'color': self.colors[0]
                }
                pred_node.GetDisplayNode().SetSelectedColor(
                    self.colors[0][0],
                    self.colors[0][1],
                    self.colors[0][2]
                )
        except:
            pass
        
        if len(self.prediction_runs) > 0 and self.softTissueNode:
            self.onCalculateAllErrors()

    def onDownloadHardLandmarksClicked(self):
        node = self.download_and_load_markup(
            "https://github.com/user-attachments/files/23696758/Thitiorul_hard_tissue.mrk.json",
            "Thitiorul_hard_tissue",
            [0, 1, 0],
            1.5,
            harden=True
        )
        if node:
            self.hardTissueNode = node
            self.hardTissueSelector.setCurrentNode(node)
            self.show_popup("Hard Tissue Template Loaded",
                           "Template landmarks loaded!\n\n"
                           "Next steps:\n"
                           "1. Click 'Create Hard Guide Lines' below\n"
                           "2. Manually adjust all landmarks to match your scan\n"
                           "3. Pay special attention to nasion 'n'")

    def onDownloadSoftLandmarksClicked(self):
        node = self.download_and_load_markup(
            "https://github.com/user-attachments/files/23696755/true_Thitiorul_soft_tissue.mrk.json",
            "true_Thitiorul_soft_tissue",
            [0, 1, 1],
            1.5,
            harden=True
        )
        if node:
            self.softTissueNode = node
            self.softTissueSelector.setCurrentNode(node)
            self.show_popup("Soft Tissue Template Loaded",
                           "Template landmarks loaded!\n\n"
                           "Next steps:\n"
                           "1. Click 'Create Soft Guide Lines' below\n"
                           "2. Manually adjust all landmarks to match your scan\n"
                           "3. When satisfied, proceed to Step 2")

    def download_and_load_markup(self, url, name, color, scale, harden=False):
        try:
            with urllib.request.urlopen(url) as response:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json') as temp:
                    temp.write(response.read())
                    temp_filename = temp.name
            
            node = slicer.util.loadMarkups(temp_filename)
            node.SetName(name)
            os.unlink(temp_filename)
            
            display_node = node.GetDisplayNode()
            display_node.SetSelectedColor(color[0], color[1], color[2])
            display_node.SetGlyphScale(scale)
            display_node.SetVisibility(True)
            
            if harden and self.transform_applied and self.transformNode:
                node.SetAndObserveTransformNodeID(self.transformNode.GetID())
                slicer.vtkSlicerTransformLogic().hardenTransform(node)
            
            return node
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to download {name}: {e}")
            return None

    def onApplyTransformClicked(self):
        """Apply transform using hard tissue nasion with guide line management."""
        try:
            if self.transform_applied:
                if not self.show_yes_no_popup(
                    "Transform Already Applied",
                    "A transform has already been applied.\n\n"
                    "Re-applying will use the CURRENT position of nasion 'n'.\n\n"
                    "Continue?"
                ):
                    return
            
            # Get hard tissue nasion
            try:
                hard_tissue = slicer.util.getNode("Thitiorul_hard_tissue")
                n_idx = self.findLandmarkByName(hard_tissue, "n")
                
                if n_idx == -1:
                    slicer.util.warningDisplay(
                        "Hard tissue nasion 'n' not found!\n\n"
                        "Please load hard tissue landmarks first (Step 1)."
                    )
                    return
                
                n_coord = hard_tissue.GetNthControlPointPosition(n_idx)
            except:
                slicer.util.warningDisplay(
                    "Hard tissue landmarks not found!\n\n"
                    "Please load hard tissue landmarks first (Step 1)."
                )
                return
            
            # GUIDE LINE MANAGEMENT
            guide_line_info = {}
            guide_line_names = ['for_nr', 'for_ss', 'for_npp_and_npa', 'for_nd']
            
            for line_name in guide_line_names:
                try:
                    line_node = slicer.util.getNode(line_name)
                    if line_node:
                        guide_line_info[line_name] = {'exists': True}
                except:
                    pass
            
            has_guide_lines = len(guide_line_info) > 0
            
            if has_guide_lines:
                line_list = ", ".join(guide_line_info.keys())
                if not self.show_yes_no_popup(
                    "Guide Lines Detected",
                    f"Existing guide lines: {line_list}\n\n"
                    "These will be automatically recreated after transformation.\n\n"
                    "Continue?"
                ):
                    return
                
                for line_name in guide_line_info.keys():
                    try:
                        line_node = slicer.util.getNode(line_name)
                        slicer.mrmlScene.RemoveNode(line_node)
                    except:
                        pass
            
            # Remove old transform
            oldTransform = slicer.mrmlScene.GetFirstNodeByName("MoveToOrigin")
            if oldTransform:
                slicer.mrmlScene.RemoveNode(oldTransform)
            
            # Create new transform
            self.transformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTransformNode", "MoveToOrigin")
            matrix = np.array([
                [1, 0, 0, -n_coord[0]],
                [0, 1, 0, -n_coord[1]],
                [0, 0, 1, -n_coord[2]],
                [0, 0, 0, 1]
            ])
            self.transformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(matrix))
            
            # Transform all fiducial nodes
            allFiducialNodes = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')
            
            transformed_nodes = []
            skipped_nodes = []
            
            for fiducial_node in allFiducialNodes:
                node_name = fiducial_node.GetName()
                
                if node_name == "reference_nasion":
                    continue
                
                if fiducial_node.GetTransformNodeID() is not None:
                    continue
                
                if self.show_yes_no_popup(
                    f"Transform '{node_name}'?",
                    f"Apply transform to '{node_name}'?\n\n"
                    f"This will move all landmarks so nasion is at origin."
                ):
                    fiducial_node.SetAndObserveTransformNodeID(self.transformNode.GetID())
                    slicer.vtkSlicerTransformLogic().hardenTransform(fiducial_node)
                    transformed_nodes.append(node_name)
                    
                    if node_name == "Thitiorul_hard_tissue":
                        self.hardTissueSelector.setCurrentNode(fiducial_node)
                        self.hardTissueNode = fiducial_node
                    elif node_name == "true_Thitiorul_soft_tissue":
                        self.softTissueSelector.setCurrentNode(fiducial_node)
                        self.softTissueNode = fiducial_node
                else:
                    skipped_nodes.append(node_name)
            
            # Transform volumes
            for vol_node in slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode"):
                if not self.show_yes_no_popup("Transform Volume?", 
                                          f"Apply transform to volume '{vol_node.GetName()}'?"):
                    continue
                vol_node.SetAndObserveTransformNodeID(self.transformNode.GetID())
            
            self.setGuiState(True)
            
            # RECREATE GUIDE LINES
            recreated_lines = []
            if has_guide_lines:
                if 'for_nr' in guide_line_info and self.hardTissueNode:
                    try:
                        self.create_line_by_name('for_nr', self.hardTissueNode, "n", "rhi")
                        recreated_lines.append('for_nr')
                    except:
                        pass
                
                if 'for_ss' in guide_line_info and self.hardTissueNode:
                    try:
                        self.create_line_by_name('for_ss', self.hardTissueNode, "a", "pr")
                        recreated_lines.append('for_ss')
                    except:
                        pass
                
                if 'for_npp_and_npa' in guide_line_info and self.softTissueNode:
                    try:
                        self.create_line_by_name('for_npp_and_npa', self.softTissueNode, "n'", "pn'")
                        recreated_lines.append('for_npp_and_npa')
                    except:
                        pass
                
                if 'for_nd' in guide_line_info and self.softTissueNode:
                    try:
                        self.create_line_by_name('for_nd', self.softTissueNode, "pn'", "sn'")
                        recreated_lines.append('for_nd')
                    except:
                        pass
            
            # Verify transformation
            verification_message = f"✓ Transform applied using hard tissue 'n'!\n\n"
            
            if transformed_nodes:
                verification_message += f"Transformed landmark sets:\n"
                for node_name in transformed_nodes:
                    verification_message += f"  • {node_name}\n"
                verification_message += "\n"
            
            if skipped_nodes:
                verification_message += f"Skipped (not transformed):\n"
                for node_name in skipped_nodes:
                    verification_message += f"  • {node_name}\n"
                verification_message += "\n"
            
            if recreated_lines:
                verification_message += f"Recreated guide lines:\n"
                for line_name in recreated_lines:
                    verification_message += f"  • {line_name}\n"
                verification_message += "\n"
            
            # Verify nasion is at origin
            try:
                hard_tissue = slicer.util.getNode("Thitiorul_hard_tissue")
                n_idx = self.findLandmarkByName(hard_tissue, "n")
                if n_idx != -1:
                    n_pos = np.array(hard_tissue.GetNthControlPointPosition(n_idx))
                    distance_from_origin = np.linalg.norm(n_pos)
                    
                    verification_message += f"📍 Nasion verification:\n"
                    verification_message += f"   Position: ({n_pos[0]:.3f}, {n_pos[1]:.3f}, {n_pos[2]:.3f})\n"
                    verification_message += f"   Distance from origin: {distance_from_origin:.3f} mm\n\n"
                    
                    if distance_from_origin > 0.5:
                        verification_message += "⚠️ WARNING: Nasion is {:.2f} mm from origin.\n\n".format(distance_from_origin)
                        verification_message += "To fix:\n"
                        verification_message += "1. Adjust the nasion 'n' landmark position\n"
                        verification_message += "2. Click 'Apply Transform' again"
                    else:
                        verification_message += "✓ Excellent! Nasion is at origin.\n"
                        verification_message += "You can proceed to Step 3."
            except:
                verification_message += "ℹ️ Could not verify nasion position."
            
            slicer.util.infoDisplay(verification_message)
            
        except Exception as e:
            slicer.util.errorDisplay(f"Could not apply transform: {e}")
            import traceback
            traceback.print_exc()
    
    def onCreateHardGuideLinesClicked(self):
        node = self.hardTissueSelector.currentNode()
        if not node:
            slicer.util.warningDisplay("Please load or select hard tissue landmarks first!")
            return
        self.create_line_by_name('for_nr', node, "n", "rhi")
        self.create_line_by_name('for_ss', node, "a", "pr")
        slicer.util.showStatusMessage("Hard tissue guide lines created!", 2000)
    
    def onCreateSoftGuideLinesClicked(self):
        node = self.softTissueSelector.currentNode()
        if not node:
            slicer.util.warningDisplay("Please load or select soft tissue landmarks first!")
            return
        self.create_line_by_name('for_npp_and_npa', node, "n'", "pn'")
        self.create_line_by_name('for_nd', node, "pn'", "sn'")
        slicer.util.showStatusMessage("Soft tissue guide lines created!", 2000)
    
    def create_line_by_name(self, name, node, label1, label2):
        try:
            slicer.mrmlScene.RemoveNode(slicer.util.getNode(name))
        except:
            pass
        p1_idx = self.findLandmarkByName(node, label1)
        p2_idx = self.findLandmarkByName(node, label2)
        if p1_idx != -1 and p2_idx != -1:
            line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
            line.AddControlPoint(node.GetNthControlPointPosition(p1_idx))
            line.AddControlPoint(node.GetNthControlPointPosition(p2_idx))
            line.GetDisplayNode().SetColor(0.0, 1.0, 0.0)
    
    def onVisualizeAxesClicked(self):
        try:
            if not self.mspPlaneNode or not self.xzPlaneNode or not self.hardTissueNode:
                slicer.util.warningDisplay("Create planes first!")
                return
            
            n_idx = self.findLandmarkByName(self.hardTissueNode, "n")
            if n_idx == -1:
                slicer.util.warningDisplay("Nasion 'n' not found!")
                return
            
            n_coord = self.hardTissueNode.GetNthControlPointPosition(n_idx)
            y_axis = np.array(self.mspPlaneNode.GetNormal())
            z_axis = np.array(self.xzPlaneNode.GetNormal())
            x_axis = np.cross(y_axis, z_axis)
            
            def create_axis(axis_name, vector, color):
                try:
                    slicer.mrmlScene.RemoveNode(slicer.util.getNode(axis_name))
                except:
                    pass
                length = np.linalg.norm(vector)
                if length < 1e-6:
                    return
                axis_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', axis_name)
                axis_node.AddControlPoint(n_coord)
                axis_node.AddControlPoint(n_coord + vector / length * 100)
                axis_node.GetDisplayNode().SetSelectedColor(color)
            
            create_axis('X_axis', x_axis, [1,0,0])
            create_axis('Y_axis', y_axis, [0,1,0])
            create_axis('Z_axis', z_axis, [0,0,1])
            slicer.util.showStatusMessage("Axes visualized!", 2000)
        except Exception as e:
            slicer.util.errorDisplay(f"Error visualizing axes: {e}")

    def onPredictClicked(self):
        if "thitiorul" in self.prediction_runs:
            if not self.show_yes_no_popup("Overwrite?", 
                                          "Prediction already exists. Overwrite?"):
                return
        
        self.hardTissueNode = self.hardTissueSelector.currentNode()
        if not self.hardTissueNode:
            slicer.util.warningDisplay("Load hard tissue landmarks first!")
            return
        
        outputName = "Predicted_Thitiorul"
        color = self.colors[0]
        
        use_auto_replace = self.autoReplaceCheckbox.isChecked()
        
        prediction_node = self.runSoftTissueRegression(self.hardTissueNode, outputName, color, use_auto_replace)
        if prediction_node:
            self.prediction_runs["thitiorul"] = {'node_id': prediction_node.GetID(), 'color': color}
            
            # Auto-calculate errors if soft tissue exists
            if self.softTissueSelector.currentNode():
                self.onCalculateAllErrors()
                slicer.util.infoDisplay(
                    "✓ Prediction complete and errors calculated!\n\n"
                    "Check Step 6 for results."
                )
            else:
                slicer.util.infoDisplay(
                    "✓ Prediction complete!\n\n"
                    "Soft tissue landmarks were loaded earlier,\n"
                    "so errors will be calculated in Step 5."
                )

    def get_left_with_fallback(self, node, left_label, right_label, use_auto_replace):
        left_idx = self.findLandmarkByName(node, left_label)
        if left_idx != -1:
            return node.GetNthControlPointPosition(left_idx)
        
        if not use_auto_replace:
            raise ValueError(f"Landmark '{left_label}' not found and auto-replace is disabled.")
        
        right_idx = self.findLandmarkByName(node, right_label)
        if right_idx != -1:
            right_pos = node.GetNthControlPointPosition(right_idx)
            left_pos = (-right_pos[0], right_pos[1], right_pos[2])
            
            print(f"Auto-replace: '{left_label}' not found, using mirrored '{right_label}'")
            slicer.util.showStatusMessage(
                f"Auto-replace: Using mirrored {right_label} for missing {left_label}", 
                3000
            )
            
            return left_pos
        
        raise ValueError(f"Landmark '{left_label}' not found, and fallback '{right_label}' also not found.")

    def runSoftTissueRegression(self, hardTissueNode, outputName, color, use_auto_replace):
        try:
            ss = self.get_point_by_label(hardTissueNode, "ss")
            nr = self.get_point_by_label(hardTissueNode, "nr")
            pr = self.get_point_by_label(hardTissueNode, "pr")
            
            iof_L = self.get_left_with_fallback(hardTissueNode, "iof_L", "iof_R", use_auto_replace)
            ecm_L = self.get_left_with_fallback(hardTissueNode, "ecm_L", "ecm_R", use_auto_replace)
            zy_L = self.get_left_with_fallback(hardTissueNode, "zy_L", "zy_R", use_auto_replace)
            
            ss_y = ss[1]
            ss_z = abs(ss[2])
            nr_y = nr[1]
            nr_z = abs(nr[2])
            pr_y = pr[1]
            pr_z = abs(pr[2])
            
            iof_L_x = abs(iof_L[0])
            iof_L_y = iof_L[1]
            ecm_L_y = ecm_L[1]
            ecm_L_z = abs(ecm_L[2])
            zy_L_x = abs(zy_L[0])
            zy_L_y = zy_L[1]
            zy_L_z = abs(zy_L[2])

            se_y = -0.869 + 0.212*ss_y + 0.139*zy_L_z - 0.073*ecm_L_y
            se_z = -1.198 - 1.159*nr_y + 0.691*nr_z - 0.208*iof_L_y
            
            npp_y = 3.182 + 0.271*ss_y + 0.423*nr_y - 0.098*ecm_L_y
            npp_z = 5.345 - 0.607*nr_y + 0.840*nr_z
            
            npa_y = 0.587 + 0.739*ss_y + 0.109*pr_z + 0.242*zy_L_x
            npa_z = 4.315 - 0.371*ss_y + 0.573*ss_z + 0.285*nr_z
            
            pn_y = -2.091 + 0.818*ss_y + 0.152*pr_z + 0.251*zy_L_x
            pn_z = 2.095 - 0.288*ss_y + 0.456*ss_z + 0.250*pr_z
            
            nd_y = -2.040 + 0.865*ss_y + 0.120*pr_z + 0.241*zy_L_x
            nd_z = 3.626 - 0.392*ss_y + 0.842*ss_z
            
            sn_y = -1.902 + 0.676*ss_y + 0.260*pr_y + 0.198*zy_L_x
            sn_z = 6.455 - 0.269*ss_y + 0.551*ss_z + 0.277*pr_z
            
            alL_x = -(7.101 + 0.107*pr_y + 0.316*iof_L_x - 0.076*zy_L_y)
            alL_y = 2.427 - 0.320*nr_z + 0.733*ss_y + 0.129*pr_z
            alL_z = 2.897 - 0.218*ss_y + 0.464*ss_z + 0.305*pr_z
            
            alsL_x = -(3.167 + 0.174*iof_L_x + 0.097*zy_L_x)
            alsL_y = 3.993 + 0.453*ss_y + 0.270*pr_y + 0.072*pr_z
            alsL_z = 3.827 - 0.466*ss_y + 0.674*ss_z + 0.257*iof_L_y
            
            alpL_x = -(7.885 + 0.060*pr_z + 0.310*iof_L_x)
            alpL_y = 4.199 + 0.398*ss_y + 0.224*pr_y + 0.247*iof_L_y
            alpL_z = 2.054 - 0.419*ss_y + 0.433*ss_z + 0.332*pr_z
            
            aliL_x = -(4.611 + 0.239*iof_L_x - 0.070*zy_L_y)
            aliL_y = -0.890 + 0.476*pr_y + 0.377*ss_y + 0.089*zy_L_x
            aliL_z = 0.404 + 0.499*ss_y + 0.312*pr_z - 0.119*zy_L_y
            
            alR_x = -alL_x
            alR_y = alL_y
            alR_z = alL_z
            
            alsR_x = -alsL_x
            alsR_y = alsL_y
            alsR_z = alsL_z
            
            alpR_x = -alpL_x
            alpR_y = alpL_y
            alpR_z = alpL_z
            
            aliR_x = -aliL_x
            aliR_y = aliL_y
            aliR_z = aliL_z

            try:
                slicer.mrmlScene.RemoveNode(slicer.util.getNode(outputName))
            except:
                pass
            
            result_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", outputName)
            landmarks = [
                ("se'", [0, se_y, se_z]),
                ("npp'", [0, npp_y, npp_z]),
                ("npa'", [0, npa_y, npa_z]),
                ("pn'", [0, pn_y, pn_z]),
                ("nd'", [0, nd_y, nd_z]),
                ("sn'", [0, sn_y, sn_z]),
                ("al'L", [alL_x, alL_y, alL_z]),
                ("als'L", [alsL_x, alsL_y, alsL_z]),
                ("alp'L", [alpL_x, alpL_y, alpL_z]),
                ("ali'L", [aliL_x, aliL_y, aliL_z]),
                ("al'R", [alR_x, alR_y, alR_z]),
                ("als'R", [alsR_x, alsR_y, alsR_z]),
                ("alp'R", [alpR_x, alpR_y, alpR_z]),
                ("ali'R", [aliR_x, aliR_y, aliR_z])
            ]
            
            for i, (label, coords) in enumerate(landmarks):
                result_node.AddControlPoint([coords[0], coords[1], -coords[2]])
                result_node.SetNthControlPointLabel(i, label)
            
            result_node.GetDisplayNode().SetSelectedColor(color[0], color[1], color[2])
            return result_node
            
        except ValueError as e:
            slicer.util.errorDisplay(f"Missing landmark for prediction: {e}")
            return None

    def onCalculateAllErrors(self):
        self.softTissueNode = self.softTissueSelector.currentNode()
        if not self.softTissueNode:
            slicer.util.warningDisplay("Load soft tissue landmarks to calculate errors.")
            return

        self.resultsTable.setColumnCount(2)
        headers = ["Landmark", "Error (mm)"]
        self.resultsTable.setHorizontalHeaderLabels(headers)

        true_dict = {}
        for i in range(self.softTissueNode.GetNumberOfControlPoints()):
            label = self.softTissueNode.GetNthControlPointLabel(i)
            pos = np.array(self.softTissueNode.GetNthControlPointPosition(i))
            true_dict[label] = pos

        for node in slicer.util.getNodesByClass('vtkMRMLMarkupsLineNode'):
            if "error_line" in node.GetName():
                slicer.mrmlScene.RemoveNode(node)

        for method_name, run_data in self.prediction_runs.items():
            pred_node = slicer.mrmlScene.GetNodeByID(run_data['node_id'])
            if not pred_node:
                continue
            
            pred_dict = {}
            for i in range(pred_node.GetNumberOfControlPoints()):
                label = pred_node.GetNthControlPointLabel(i)
                pos = np.array(pred_node.GetNthControlPointPosition(i))
                pred_dict[label] = pos
            
            for row_idx in range(self.resultsTable.rowCount):
                landmark = self.resultsTable.item(row_idx, 0).text()
                if landmark in pred_dict and landmark in true_dict:
                    error = np.linalg.norm(pred_dict[landmark] - true_dict[landmark])
                    self.resultsTable.setItem(row_idx, 1, qt.QTableWidgetItem(f"{error:.2f}"))
                    
                    line_node = slicer.mrmlScene.AddNewNodeByClass(
                        "vtkMRMLMarkupsLineNode",
                        f"error_line_{landmark}"
                    )
                    line_node.AddControlPoint(pred_dict[landmark])
                    line_node.AddControlPoint(true_dict[landmark])
                    displayNode = line_node.GetDisplayNode()
                    if displayNode:
                        displayNode.SetSelectedColor(run_data['color'][0], run_data['color'][1], run_data['color'][2])
                        displayNode.SetGlyphScale(0)
                        displayNode.SetLineThickness(0.5)


    
    def onShowDetailedResultsClicked(self):
        self.detailedWidget = qt.QDialog(self.mainWidget)
        self.detailedWidget.setWindowTitle("Detailed Prediction Results")
        self.detailedWidget.setMinimumSize(1200, 700)
        layout = qt.QVBoxLayout(self.detailedWidget)
        table = qt.QTableWidget()
        
        headers = [
            "Landmark", "Pred X", "Pred Y", "Pred Z",
            "True X", "True Y", "True Z", "Error (mm)", "Error Direction", "Equation"
        ]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        if not self.softTissueSelector.currentNode():
            slicer.util.warningDisplay("Please select soft tissue to show detailed results.")
            return

        formulas = {
            "se'": ["y = -0.869+0.212*ss_y+0.139*zy_z-0.073*ecm_y", "z = -1.198-1.159*nr_y+0.691*nr_z-0.208*iof_y"],
            "npp'": ["y = 3.182+0.271*ss_y+0.423*nr_y-0.098*ecm_y", "z = 5.345-0.607*nr_y+0.840*nr_z"],
            "npa'": ["y = 0.587+0.739*ss_y+0.109*pr_z+0.242*zy_x", "z = 4.315-0.371*ss_y+0.573*ss_z+0.285*nr_z"],
            "pn'": ["y = -2.091+0.818*ss_y+0.152*pr_z+0.251*zy_x", "z = 2.095-0.288*ss_y+0.456*ss_z+0.250*pr_z"],
            "nd'": ["y = -2.040+0.865*ss_y+0.120*pr_z+0.241*zy_x", "z = 3.626-0.392*ss_y+0.842*ss_z"],
            "sn'": ["y = -1.902+0.676*ss_y+0.260*pr_y+0.198*zy_x", "z = 6.455-0.269*ss_y+0.551*ss_z+0.277*pr_z"],
            "al'L": ["x = -(7.101+0.107*pr_y+0.316*iof_x-0.076*zy_y)", "y = 2.427-0.320*nr_z+0.733*ss_y+0.129*pr_z", "z = 2.897-0.218*ss_y+0.464*ss_z+0.305*pr_z"],
            "als'L": ["x = -(3.167+0.174*iof_x+0.097*zy_x)", "y = 3.993+0.453*ss_y+0.270*pr_y+0.072*pr_z", "z = 3.827-0.466*ss_y+0.674*ss_z+0.257*iof_y"],
            "alp'L": ["x = -(7.885+0.060*pr_z+0.310*iof_x)", "y = 4.199+0.398*ss_y+0.224*pr_y+0.247*iof_y", "z = 2.054-0.419*ss_y+0.433*ss_z+0.332*pr_z"],
            "ali'L": ["x = -(4.611+0.239*iof_x-0.070*zy_y)", "y = -0.890+0.476*pr_y+0.377*ss_y+0.089*zy_x", "z = 0.404+0.499*ss_y+0.312*pr_z-0.119*zy_y"],
            "al'R": ["Mirrored from LEFT"],
            "als'R": ["Mirrored from LEFT"],
            "alp'R": ["Mirrored from LEFT"],
            "ali'R": ["Mirrored from LEFT"]
        }
        
        true_dict = {}
        for i in range(self.softTissueSelector.currentNode().GetNumberOfControlPoints()):
            label = self.softTissueSelector.currentNode().GetNthControlPointLabel(i)
            pos = np.array(self.softTissueSelector.currentNode().GetNthControlPointPosition(i))
            true_dict[label] = pos
        
        pred_dict = {}
        if len(self.prediction_runs) > 0:
            run_data = list(self.prediction_runs.values())[0]
            pred_node = slicer.mrmlScene.GetNodeByID(run_data['node_id'])
            if pred_node:
                for i in range(pred_node.GetNumberOfControlPoints()):
                    label = pred_node.GetNthControlPointLabel(i)
                    pos = np.array(pred_node.GetNthControlPointPosition(i))
                    pred_dict[label] = pos
        
        table.setRowCount(len(true_dict))
        current_row = 0
        
        for landmark in sorted(true_dict.keys()):
            if landmark not in pred_dict:
                continue
                
            table.setItem(current_row, 0, qt.QTableWidgetItem(landmark))
            
            pred_pos = pred_dict[landmark]
            true_pos = true_dict[landmark]
            error = np.linalg.norm(pred_pos - true_pos)
            
            table.setItem(current_row, 1, qt.QTableWidgetItem(f"{pred_pos[0]:.2f}"))
            table.setItem(current_row, 2, qt.QTableWidgetItem(f"{pred_pos[1]:.2f}"))
            table.setItem(current_row, 3, qt.QTableWidgetItem(f"{pred_pos[2]:.2f}"))
            table.setItem(current_row, 4, qt.QTableWidgetItem(f"{true_pos[0]:.2f}"))
            table.setItem(current_row, 5, qt.QTableWidgetItem(f"{true_pos[1]:.2f}"))
            table.setItem(current_row, 6, qt.QTableWidgetItem(f"{true_pos[2]:.2f}"))
            table.setItem(current_row, 7, qt.QTableWidgetItem(f"{error:.2f}"))
            table.setItem(current_row, 8, qt.QTableWidgetItem(
                self.get_error_direction_string(true_pos - pred_pos)
            ))
            
            equation_str = "\n".join(formulas.get(landmark, ["Not available"]))
            table.setItem(current_row, 9, qt.QTableWidgetItem(equation_str))
            
            current_row += 1

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        layout.addWidget(table)
        
        copy_button = qt.QPushButton("Copy Table to Clipboard")
        copy_button.clicked.connect(lambda: self.onCopyDetailedToClipboard(table))
        layout.addWidget(copy_button)
        
        self.detailedWidget.show()

    def onCopyDetailedToClipboard(self, table):
        """Copy detailed results table to clipboard with user feedback."""
        success = self.onCopyToClipboard(table)
        if success:
            slicer.util.showStatusMessage("✓ Detailed results copied to clipboard!", 3000)
            slicer.util.infoDisplay("✓ Detailed results copied to clipboard!\n\nYou can now paste into Excel or any text editor.")
        else:
            slicer.util.warningDisplay("Copy to clipboard may have failed.")

    def get_error_direction_string(self, error_vector):
        x, y, z = error_vector
        
        x_dir = ""
        if abs(x) > 0.1:
            x_dir = "Right(+)" if x > 0 else "Left(-)"
        
        y_dir = ""
        if abs(y) > 0.1:
            y_dir = "Ant(+)" if y > 0 else "Post(-)"
        
        z_dir = ""
        if abs(z) > 0.1:
            z_dir = "Sup(+)" if z > 0 else "Inf(-)"
        
        directions = [d for d in [y_dir, z_dir, x_dir] if d]
        return ", ".join(directions) if directions else "Spot on"

    def onSaveToCSV(self):
        result = qt.QFileDialog.getSaveFileName(
            self.mainWidget,
            "Save Summary",
            "thitiorul_summary.csv",
            "CSV Files (*.csv)"
        )
        fileName = result[0] if isinstance(result, tuple) else result
        if not fileName:
            return
        
        self.onCopyToClipboard(self.resultsTable)
        try:
            app = qt.QApplication.instance()
            clipboard = app.clipboard()
            with open(fileName, 'w') as f:
                f.write(clipboard.text(qt.QClipboard.Clipboard))
            slicer.util.infoDisplay(f"Summary table saved to {fileName}")
        except Exception as e:
            slicer.util.errorDisplay(f"Could not save file: {e}")

    def show_popup(self, title, text):
        msgBox = qt.QMessageBox(self.mainWidget)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setIcon(qt.QMessageBox.Information)
        msgBox.setStandardButtons(qt.QMessageBox.Ok)
        msgBox.exec_()

    def show_yes_no_popup(self, title, text):
        return qt.QMessageBox.question(
            self.mainWidget,
            title,
            text,
            qt.QMessageBox.Yes | qt.QMessageBox.No
        ) == qt.QMessageBox.Yes
        
    def findLandmarkByName(self, node, label):
        for i in range(node.GetNumberOfControlPoints()):
            if node.GetNthControlPointLabel(i) == label:
                return i
        return -1
        
    def get_point_by_label(self, node, label):
        idx = self.findLandmarkByName(node, label)
        if idx != -1:
            return node.GetNthControlPointPosition(idx)
        raise ValueError(f"Landmark '{label}' not found.")

    def onCreatePlanesClicked(self):
        self.hardTissueNode = self.hardTissueSelector.currentNode()
        if not self.hardTissueNode:
            slicer.util.warningDisplay("Load hard tissue landmarks first!")
            return
        
        midline_labels = ["n", "a", "pr", "ss", "rhi"]
        indices = [self.findLandmarkByName(self.hardTissueNode, name) for name in midline_labels]
        
        if -1 in indices:
            slicer.util.warningDisplay(f"Cannot create plane. Missing one of: {midline_labels}")
            return
        
        points = np.array([self.hardTissueNode.GetNthControlPointPosition(i) for i in indices])
        centroid = np.mean(points, axis=0)
        _, _, Vt = np.linalg.svd(points - centroid)
        plane_normal = Vt[2, :]
        
        self.mspPlaneNode = self.create_plane('MSP', centroid, plane_normal)
        nasion_coord = self.hardTissueNode.GetNthControlPointPosition(indices[0])
        xz_plane_normal = np.cross(self.mspPlaneNode.GetNormal(), [0, 0, 1])
        self.xzPlaneNode = self.create_plane('X-Z plane', nasion_coord, xz_plane_normal)
        slicer.util.showStatusMessage("Planes created!", 2000)

    def create_plane(self, name, origin, normal):
        try:
            slicer.mrmlScene.RemoveNode(slicer.util.getNode(name))
        except:
            pass
        
        plane = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', name)
        plane.SetOrigin(origin)
        plane.SetNormal(normal)
        return plane


# Main execution block
try:
    if 'gui' in globals() and isinstance(globals().get('gui'), ThitiorulGUI):
        globals()['gui'].mainWidget.close()
    gui = ThitiorulGUI()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Failed to create GUI: {e}")


```
