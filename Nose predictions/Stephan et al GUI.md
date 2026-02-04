```python
# =============================================================================
#
#  Stephan Method GUI - Final, Feature-Complete Version
#
#  Hello esomjai! This is the final version of your script, with all the
#  new features and UI improvements you requested. Congratulations!
#
#  Changes in this version:
#  - Step 3: The framework table now includes the description for the
#    "nasal aperture base" line.
#  - Step 4: A new table has been added to explain measurements A-E.
#  - Step 5: The prediction formulas are now displayed in the GUI.
#  - Step 6: This step is now fully functional! It creates an error line,
#    displays coordinates and error distance in tables, and includes
#    "Copy to Clipboard" buttons for easy data export.
#
#  Instructions:
#  1. Open the Python Console in 3D Slicer.
#  2. Copy and paste this entire script.
#  3. Press Enter. Your custom GUI window will appear!
#
# =============================================================================

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import logging
import math

class StephanMethodGUI(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("Stephan Method GUI")
        self.setObjectName("StephanMethodGUI")
        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setSpacing(10)
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        self.logic = StephanMethodLogic()
        self.currentStep = 0
        self.createAllStepWidgets()
        self.setupNavigation()
        self.updateStepUI()

    def createAllStepWidgets(self):
        self.createStep1_Setup()
        self.createStep2_PlaneSetup()
        self.createStep3_Framework()
        self.createStep4_Measurements()
        self.createStep5_Prediction()
        self.createStep6_Validation()

    def setupNavigation(self):
        navWidget = qt.QWidget()
        navLayout = qt.QHBoxLayout(navWidget)
        navLayout.setContentsMargins(0, 0, 0, 0)
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.clicked.connect(self.onPrevButtonClicked)
        self.stepLabel = qt.QLabel("Step 1/6")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter)
        self.stepLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.nextButton = qt.QPushButton("Next")
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        navLayout.addWidget(self.prevButton); navLayout.addStretch(1)
        navLayout.addWidget(self.stepLabel); navLayout.addStretch(1)
        navLayout.addWidget(self.nextButton)
        self.mainLayout.addWidget(navWidget)

    def createStep1_Setup(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 1: Load Hard Tissue Landmarks"); title.setStyleSheet("font-weight: bold; font-size: 16px;")
        desc = qt.QLabel("Begin by loading the required hard tissue landmarks. This file contains all the necessary points for the workflow.")
        desc.setWordWrap(True)
        self.downloadLandmarksButton = qt.QPushButton("Download and Load Landmarks")
        self.downloadLandmarksButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;")
        self.downloadLandmarksButton.clicked.connect(self.onDownloadHardTissue)
        self.step1StatusLabel = qt.QLabel("Status: Waiting for user.")
        layout.addWidget(title); layout.addWidget(desc); layout.addWidget(self.downloadLandmarksButton, 0, qt.Qt.AlignHCenter)
        layout.addWidget(self.step1StatusLabel); layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep2_PlaneSetup(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 2: Create a Reference Plane"); title.setStyleSheet("font-weight: bold; font-size: 16px;")
        desc = qt.QLabel("Choose a method to create the main reference plane for all subsequent geometric constructions.")
        desc.setWordWrap(True)
        buttonLayout = qt.QHBoxLayout()
        self.createINBButton = qt.QPushButton("Create INB Plane"); self.createMSPButton = qt.QPushButton("Create MSP Plane")
        buttonLayout.addWidget(self.createINBButton); buttonLayout.addWidget(self.createMSPButton)
        self.createINBButton.clicked.connect(lambda: self.onCreatePlane('INB'))
        self.createMSPButton.clicked.connect(lambda: self.onCreatePlane('MSP'))
        self.step2StatusLabel = qt.QLabel("Status: Waiting for user.")
        layout.addWidget(title); layout.addWidget(desc); layout.addLayout(buttonLayout)
        layout.addWidget(self.step2StatusLabel); layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep3_Framework(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 3: Create Geometric Framework"); title.setStyleSheet("font-weight: bold; font-size: 16px;")
        desc = qt.QLabel("This step builds the foundational network of reference lines and points. The table below explains what will be created.")
        desc.setWordWrap(True)
        table = qt.QTableWidget(6, 2)
        table.setHorizontalHeaderLabels(["Item to be Created", "Description"])
        table.setItem(0, 0, qt.QTableWidgetItem("nasion-point A")); table.setItem(0, 1, qt.QTableWidgetItem("Line from Nasion through Point A, on the reference plane."))
        table.setItem(1, 0, qt.QTableWidgetItem("AA FHP")); table.setItem(1, 1, qt.QTableWidgetItem("Line parallel to FHP, bisecting Point AA."))
        table.setItem(2, 0, qt.QTableWidgetItem("Point X")); table.setItem(2, 1, qt.QTableWidgetItem("Intersection of the two lines above."))
        table.setItem(3, 0, qt.QTableWidgetItem("nasal aperture base")); table.setItem(3, 1, qt.QTableWidgetItem("Line connecting LL and RL, the lowest part of the nasal aperture in profile view."))
        table.setItem(4, 0, qt.QTableWidgetItem("NAB point")); table.setItem(4, 1, qt.QTableWidgetItem("Intersection of the nasal aperture base and the plane."))
        table.setItem(5, 0, qt.QTableWidgetItem("for c)")); table.setItem(5, 1, qt.QTableWidgetItem("Line through NAB point, parallel to nasion-point A."))
        table.horizontalHeader().setStretchLastSection(True); table.verticalHeader().setVisible(False)
        table.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        table.setFixedHeight(table.verticalHeader().defaultSectionSize * table.rowCount + table.horizontalHeader().height)
        self.createFrameworkButton = qt.QPushButton("Create Framework")
        self.createFrameworkButton.clicked.connect(self.onCreateFramework)
        self.step3StatusLabel = qt.QLabel("Status: Waiting for user.")
        layout.addWidget(title); layout.addWidget(desc); layout.addWidget(table)
        layout.addWidget(self.createFrameworkButton); layout.addWidget(self.step3StatusLabel); layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep4_Measurements(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 4: Create All Measurements"); title.setStyleSheet("font-weight: bold; font-size: 16px;")
        desc = qt.QLabel("Click the button below to create all the final measurements. This requires the framework from Step 3 to be complete.")
        desc.setWordWrap(True)
        
        table = qt.QTableWidget(5, 2)
        table.setHorizontalHeaderLabels(["Measurement", "Description"])
        table.setItem(0, 0, qt.QTableWidgetItem("A) nasal bone angle")); table.setItem(0, 1, qt.QTableWidgetItem("Angle from FHP, at nasion, to rhinion."))
        table.setItem(1, 0, qt.QTableWidgetItem("B) line")); table.setItem(1, 1, qt.QTableWidgetItem("Shortest distance from acanthion to the nasal aperture base."))
        table.setItem(2, 0, qt.QTableWidgetItem("C) line")); table.setItem(2, 1, qt.QTableWidgetItem("Shortest distance from rhinion to the 'for c)' line."))
        table.setItem(3, 0, qt.QTableWidgetItem("D) nasal spine angle")); table.setItem(3, 1, qt.QTableWidgetItem("Angle from acanthion, at Point X, to the FHP."))
        table.setItem(4, 0, qt.QTableWidgetItem("E) line")); table.setItem(4, 1, qt.QTableWidgetItem("Distance from nasion to Point X."))
        table.horizontalHeader().setStretchLastSection(True); table.verticalHeader().setVisible(False)
        table.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        table.setFixedHeight(table.verticalHeader().defaultSectionSize * table.rowCount + table.horizontalHeader().height)
        
        self.createMeasurementsButton = qt.QPushButton("Create Measurements (A, B, C, D, E)")
        self.createMeasurementsButton.clicked.connect(self.onCreateMeasurements)
        self.step4StatusLabel = qt.QLabel("Status: Waiting for user.")
        layout.addWidget(title); layout.addWidget(desc); layout.addWidget(table)
        layout.addWidget(self.createMeasurementsButton)
        layout.addWidget(self.step4StatusLabel); layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep5_Prediction(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 5: Final Pronasale Prediction"); title.setStyleSheet("font-weight: bold; font-size: 16px;")
        desc = qt.QLabel("Select the subject's sex and click the button to run the final prediction formulas and create the result.")
        desc.setWordWrap(True)
        
        formulas_label = qt.QLabel("<b>Prediction Formulas:</b><br>"
                                     "<i>Projection (x) for Males:</i> x = -0.32(a) + 0.85(b) - 0.42(c) + 49.58<br>"
                                     "<i>Projection (x) for Females:</i> x = -0.41(a) + 0.37(b) + 49.87<br>"
                                     "<i>Height (y) for Both:</i> y = (-0.002(d) + 0.83) * e")
        formulas_label.setWordWrap(True)

        formLayout = qt.QFormLayout()
        self.sexSelector = qt.QComboBox(); self.sexSelector.addItems(["Female", "Male"])
        formLayout.addRow("Sex:", self.sexSelector)
        
        self.calculatePredictionButton = qt.QPushButton("Calculate Prediction")
        self.calculatePredictionButton.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 8px;")
        self.calculatePredictionButton.clicked.connect(self.onCalculatePrediction)
        
        self.step5StatusLabel = qt.QLabel("Status: Waiting for user.")
        layout.addWidget(title); layout.addWidget(desc); layout.addWidget(formulas_label)
        layout.addLayout(formLayout)
        layout.addWidget(self.calculatePredictionButton); layout.addWidget(self.step5StatusLabel); layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep6_Validation(self):
        widget = qt.QWidget(); layout = qt.QVBoxLayout(widget); layout.setSpacing(15)
        title = qt.QLabel("Step 6: Validation"); title.setStyleSheet("font-weight: bold; font-size: 16px;")
        desc = qt.QLabel("If you have the 'true' soft tissue landmarks, load them, then measure the prediction error.")
        desc.setWordWrap(True)
        
        self.downloadSoftTissueButton = qt.QPushButton("Download and Load True Soft Tissue Points")
        self.downloadSoftTissueButton.clicked.connect(self.onDownloadSoftTissue)
        
        self.compareButton = qt.QPushButton("Measure Prediction Error")
        self.compareButton.clicked.connect(self.onCompare)
        
        # Create widgets for results, initially hidden
        self.step6ResultsWidget = qt.QWidget(); resultsLayout = qt.QVBoxLayout(self.step6ResultsWidget)
        self.step6ResultsWidget.setVisible(False)
        
        # Table 1: Coordinates
        self.coordsTable = qt.QTableWidget(2, 4); self.coordsTable.setHorizontalHeaderLabels(["Point", "R (x)", "A (y)", "S (z)"])
        self.coordsTable.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.coordsTable.verticalHeader().setVisible(False)
        self.copyCoordsButton = qt.QPushButton("Copy Coordinates to Clipboard")
        self.copyCoordsButton.clicked.connect(self.onCopyCoords)
        
        # Table 2: Error
        self.errorTable = qt.QTableWidget(1, 2); self.errorTable.setHorizontalHeaderLabels(["Item", "Value"])
        self.errorTable.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.errorTable.verticalHeader().setVisible(False)
        self.copyErrorButton = qt.QPushButton("Copy Error to Clipboard")
        self.copyErrorButton.clicked.connect(self.onCopyError)

        resultsLayout.addWidget(qt.QLabel("<b>Results:</b>")); resultsLayout.addWidget(self.coordsTable); resultsLayout.addWidget(self.copyCoordsButton)
        resultsLayout.addSpacing(15); resultsLayout.addWidget(self.errorTable); resultsLayout.addWidget(self.copyErrorButton)
        
        self.step6StatusLabel = qt.QLabel("Status: Waiting for user.")

        # A finish button to close the GUI
        finishButton = qt.QPushButton("Finish")
        finishButton.setStyleSheet("background-color: #6c757d; color: white; padding: 8px;")
        finishButton.clicked.connect(self.close) # self.close is a built-in function to close the widget

        layout.addWidget(title); layout.addWidget(desc); layout.addWidget(self.downloadSoftTissueButton)
        layout.addWidget(self.compareButton); layout.addWidget(self.step6ResultsWidget); layout.addWidget(self.step6StatusLabel); layout.addStretch(1)
        layout.addWidget(finishButton) # Add the finish button at the end
        self.stepStack.addWidget(widget)

    def onPrevButtonClicked(self):
        if self.currentStep > 0: self.currentStep -= 1; self.updateStepUI()
    
    def onNextButtonClicked(self):
        self.updateStepUI()
        isComplete, _ = self.logic.isStepComplete(self.currentStep)
        if isComplete:
            if self.currentStep < self.stepStack.count - 1: self.currentStep += 1; self.updateStepUI()
        else: slicer.util.warningDisplay("Please complete the current step before proceeding.")
    
    def updateStepUI(self):
        self.checkSceneAndSetState()
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1}/{self.stepStack.count}")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)

    def checkSceneAndSetState(self):
        status_labels = [self.step1StatusLabel, self.step2StatusLabel, self.step3StatusLabel, self.step4StatusLabel, self.step5StatusLabel, self.step6StatusLabel]
        for i, label in enumerate(status_labels):
            isComplete, message = self.logic.isStepComplete(i)
            label.setText(f"Status: {message}" if isComplete else "Status: Waiting for user.")
    
    def onDownloadHardTissue(self): self.logic.downloadAndLoadHardTissue(); self.updateStepUI()
    def onCreatePlane(self, plane_type): self.logic.createReferencePlane(plane_type); self.updateStepUI()
    def onCreateFramework(self): self.logic.createFramework(); self.updateStepUI()
    def onCreateMeasurements(self): self.logic.createMeasurements(); self.updateStepUI()
    def onCalculatePrediction(self): self.logic.calculatePrediction(self.sexSelector.currentText); self.updateStepUI()
    def onDownloadSoftTissue(self): self.logic.downloadAndLoadSoftTissue(); self.updateStepUI()
    
    def onCompare(self):
        results = self.logic.comparePrediction()
        if results:
            true_pos, pred_pos, error_dist = results
            # Populate coordinates table
            self.coordsTable.setItem(0, 0, qt.QTableWidgetItem("True Pronasale")); self.coordsTable.setItem(1, 0, qt.QTableWidgetItem("Predicted Pronasale"))
            for i in range(3):
                self.coordsTable.setItem(0, i+1, qt.QTableWidgetItem(f"{true_pos[i]:.2f}"))
                self.coordsTable.setItem(1, i+1, qt.QTableWidgetItem(f"{pred_pos[i]:.2f}"))
            self.coordsTable.resizeColumnsToContents()
            
            # Populate error table
            self.errorTable.setItem(0, 0, qt.QTableWidgetItem("pronasale error")); self.errorTable.setItem(0, 1, qt.QTableWidgetItem(f"{error_dist:.2f} mm"))
            self.errorTable.resizeColumnsToContents()
            
            self.step6ResultsWidget.setVisible(True)
            self.updateStepUI()

    def onCopyCoords(self):
        clipboard = qt.QApplication.clipboard()
        text = "Point\tR (x)\tA (y)\tS (z)\n"
        text += f"True Pronasale\t{self.coordsTable.item(0, 1).text()}\t{self.coordsTable.item(0, 2).text()}\t{self.coordsTable.item(0, 3).text()}\n"
        text += f"Predicted Pronasale\t{self.coordsTable.item(1, 1).text()}\t{self.coordsTable.item(1, 2).text()}\t{self.coordsTable.item(1, 3).text()}"
        clipboard.setText(text)
        slicer.util.infoDisplay("Coordinates copied to clipboard.")

    def onCopyError(self):
        clipboard = qt.QApplication.clipboard()
        text = "Item\tValue\n"
        text += f"pronasale error\t{self.errorTable.item(0, 1).text()}"
        clipboard.setText(text)
        slicer.util.infoDisplay("Error measurement copied to clipboard.")

#
# LOGIC CLASS - THE "ENGINE"
#
class StephanMethodLogic:
    def isStepComplete(self, step_index):
        if step_index == 0:
            return self.getNode('lmrks_Stephan', "vtkMRMLMarkupsFiducialNode") is not None, "Landmarks loaded successfully."
        elif step_index == 1:
            plane_node = self.getNode('INB', "vtkMRMLMarkupsPlaneNode") or self.getNode('MSP', "vtkMRMLMarkupsPlaneNode")
            return plane_node is not None, f"'{plane_node.GetName()}' plane is active." if plane_node else ""
        elif step_index == 2:
            return self.isFrameworkComplete(), "Geometric framework is complete."
        elif step_index == 3:
            return self.areMeasurementsComplete(), "All measurements created successfully."
        elif step_index == 4:
            return self.getNode('pronasale pred', "vtkMRMLMarkupsFiducialNode") is not None, "Prediction complete."
        elif step_index == 5:
            if self.getNode('pronasale error', 'vtkMRMLMarkupsLineNode'):
                return True, "Comparison complete."
            elif self.getNode('soft_tissue_Stephan', "vtkMRMLMarkupsFiducialNode"):
                return True, "True landmarks loaded. Ready to measure error."
            return False, ""
        return False, ""

    def cleanup(self, partial=False, measurements=False, prediction=False, comparison=False):
        nodes_to_remove = []
        framework_nodes = ["x axis", "y axis", "AA FHP", "nasion-point A", "nasal aperture base", "for c)", "Point X", "NAB point"]
        measurement_nodes = ["A) nasal bone angle", "B) line", "C) line", "D) nasal spine angle", "E) line"]
        prediction_nodes = ["pronasale pred"]
        comparison_nodes = ["pronasale error"]
        
        if comparison: nodes_to_remove.extend(comparison_nodes)
        if prediction: nodes_to_remove.extend(prediction_nodes)
        if measurements: nodes_to_remove.extend(measurement_nodes)
        if partial: nodes_to_remove.extend(framework_nodes)
        if not any([partial, measurements, prediction, comparison]):
             nodes_to_remove.extend(["INB", "MSP"] + framework_nodes + measurement_nodes + prediction_nodes + comparison_nodes)
        
        for name in nodes_to_remove:
            node = self.getNode(name, exact=True)
            if node: slicer.mrmlScene.RemoveNode(node)

    def getNode(self, name, className=None, exact=False):
        if exact: return slicer.util.getFirstNodeByName(name)
        name_lower = name.lower().strip()
        nodes = slicer.mrmlScene.GetNodesByClass(className if className else "vtkMRMLNode")
        for i in range(nodes.GetNumberOfItems()):
            node = nodes.GetItemAsObject(i)
            if name_lower in node.GetName().lower(): return node
        return None

    def lineIntersection(self, p1, v1, p2, v2):
        A = np.array([v1, -v2]).T; b = p2 - p1
        try:
            ts = np.linalg.lstsq(A, b, rcond=None)[0]; return p1 + ts[0] * v1
        except np.linalg.LinAlgError: return None

    def getPointPosByName(self, nodeName, pointNames):
        node = self.getNode(nodeName, className="vtkMRMLMarkupsFiducialNode")
        if not node: return None
        available_points_lower = {node.GetNthControlPointLabel(i).lower(): self.getNthPointPos(node, i) for i in range(node.GetNumberOfControlPoints())}
        found_pos = {}
        for name in pointNames:
            name_lower = name.lower().replace(" ", "")
            for label, pos in available_points_lower.items():
                label_lower = label.lower().replace(" ", "")
                if name_lower in label_lower:
                    found_pos[name] = pos
                    break
        if len(found_pos) != len(pointNames):
            missing = set(pointNames) - set(found_pos.keys()); logging.warning(f"Could not find points: {missing} in node '{nodeName}'"); return None
        return [found_pos[name] for name in pointNames] if len(pointNames) > 1 else found_pos[pointNames[0]]

    def getNthPointPos(self, node, i):
        pos = np.zeros(3); node.GetNthControlPointPositionWorld(i, pos); return pos

    def downloadFile(self, url, filename):
        local_path = os.path.join(slicer.app.temporaryPath, filename)
        if not os.path.exists(local_path) or slicer.util.confirmOkCancelDisplay(f"'{filename}' exists. Download a fresh copy?"):
            try: print(f"Downloading {filename}..."); urllib.request.urlretrieve(url, local_path); return local_path
            except Exception as e: slicer.util.errorDisplay(f"Download failed: {e}"); return None
        return local_path

    def downloadAndLoadHardTissue(self):
        path = self.downloadFile("https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/raw/main/Nose%20predictions/Stephan%20(2003)/lmrks_Stephan.mrk.json", "lmrks_Stephan.mrk.json")
        if path:
            self.getNode("lmrks_Stephan", exact=True) and slicer.mrmlScene.RemoveNode(self.getNode("lmrks_Stephan", exact=True))
            node = slicer.util.loadMarkups(path); node.SetName("lmrks_Stephan")
            return True
        return False

    def createReferencePlane(self, plane_type):
        self.cleanup()
        points = self.getPointPosByName('lmrks_Stephan', ["Inion", "Nasion", "Bregma"] if plane_type == 'INB' else ["Nasion", "Rhinion", "Acanthion", "Point A", "Prosthion"])
        if not points: return False
        if plane_type == 'INB':
            normal = np.cross(points[1] - points[0], points[2] - points[0]); origin = points[0]
        else:
            points_array = np.array(points); centroid = np.mean(points_array, axis=0)
            covariance_matrix = np.cov(points_array - centroid, rowvar=False); eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
            normal = eigenvectors[:, np.argmin(eigenvalues)]; origin = centroid
        planeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", plane_type)
        planeNode.SetOrigin(origin); planeNode.SetNormal(normal); planeNode.GetDisplayNode().SetOpacity(0.7)
        return True

    def isFrameworkComplete(self):
        items = { "x axis": "vtkMRMLMarkupsLineNode", "y axis": "vtkMRMLMarkupsLineNode", "nasion-point A": "vtkMRMLMarkupsLineNode",
                  "AA FHP": "vtkMRMLMarkupsLineNode", "nasal aperture base": "vtkMRMLMarkupsLineNode", "for c)": "vtkMRMLMarkupsLineNode", 
                  "Point X": "vtkMRMLMarkupsFiducialNode", "NAB point": "vtkMRMLMarkupsFiducialNode" }
        return all(self.getNode(name, className) for name, className in items.items())

    def areMeasurementsComplete(self):
        items = { "A) nasal bone angle": "vtkMRMLMarkupsAngleNode", "B) line": "vtkMRMLMarkupsLineNode", "C) line": "vtkMRMLMarkupsLineNode",
                  "D) nasal spine angle": "vtkMRMLMarkupsAngleNode", "E) line": "vtkMRMLMarkupsLineNode" }
        return all(self.getNode(name, className) for name, className in items.items())

    def createFramework(self):
        self.cleanup(partial=True)
        planeNode = self.getNode('INB', "vtkMRMLMarkupsPlaneNode") or self.getNode('MSP', "vtkMRMLMarkupsPlaneNode")
        lmrks_node = self.getNode('lmrks_Stephan', "vtkMRMLMarkupsFiducialNode")
        if not all([lmrks_node, planeNode]): 
            slicer.util.errorDisplay("Please ensure landmarks (Step 1) and a plane (Step 2) are created first.")
            return False
        
        points = self.getPointPosByName('lmrks_Stephan', ["Nasion", "Point A", "point AA", "LL", "RL"])
        if not points: return False

        nasion_pos, pointA_pos, pointAA_pos, ll_pos, rl_pos = points
        planeNormal = np.array(planeNode.GetNormal()); fhpNormal = np.array([0, 0, 1])
        dirX = np.cross(fhpNormal, planeNormal); dirX /= np.linalg.norm(dirX)
        dirY = np.cross(dirX, planeNormal); dirY /= np.linalg.norm(dirY)
        def create_line(name, p1, p2, color):
            node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
            node.AddControlPoint(p1); node.AddControlPoint(p2)
            node.GetDisplayNode().SetColor(color); node.GetDisplayNode().SetSelectedColor(color)
            return node
        create_line("x axis", nasion_pos - 100*dirX, nasion_pos + 100*dirX, [0, 1, 1])
        create_line("y axis", nasion_pos - 100*dirY, nasion_pos + 100*dirY, [0, 1, 1])
        nasion_proj = [0,0,0]; vtk.vtkPlane.ProjectPoint(nasion_pos, planeNode.GetOrigin(), planeNode.GetNormal(), nasion_proj)
        pointA_proj = [0,0,0]; vtk.vtkPlane.ProjectPoint(pointA_pos, planeNode.GetOrigin(), planeNode.GetNormal(), pointA_proj)
        dir_n_A = np.array(pointA_proj) - np.array(nasion_proj); dir_n_A /= np.linalg.norm(dir_n_A)
        n_A_line = create_line("nasion-point A", np.array(nasion_proj) - 100 * dir_n_A, np.array(nasion_proj) + 100 * dir_n_A, [0, 0, 1])
        aa_fhp_line = create_line("AA FHP", pointAA_pos - 100 * dirX, pointAA_pos + 100 * dirX, [1, 0.5, 0])
        pX_pos = self.lineIntersection(self.getNthPointPos(n_A_line, 0), dir_n_A, self.getNthPointPos(aa_fhp_line, 0), dirX)
        if pX_pos is None: return False
        
        nab_base_line = create_line("nasal aperture base", ll_pos, rl_pos, [0.1, 0.5, 0.1])
        
        t = vtk.mutable(0); intersection_point = [0,0,0]
        intersect_status = vtk.vtkPlane.IntersectWithLine(ll_pos, rl_pos, planeNode.GetOrigin(), planeNode.GetNormal(), t, intersection_point)
        if intersect_status != 0: nab_point_pos = intersection_point
        else: nab_point_pos = (np.array(ll_pos) + np.array(rl_pos)) / 2.0

        create_line("for c)", nab_point_pos - 100 * dir_n_A, nab_point_pos + 100 * dir_n_A, [1, 0.7, 0.8])
        pointX_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', "Point X"); pointX_node.AddControlPoint(pX_pos, "Point X")
        nab_point_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', "NAB point"); nab_point_node.AddControlPoint(nab_point_pos, "NAB point")
        return True

    def createMeasurements(self):
        self.cleanup(measurements=True)
        try:
            required_nodes = { "lmrks_Stephan": self.getNode("lmrks_Stephan", "vtkMRMLMarkupsFiducialNode"), "Point X": self.getNode("Point X", "vtkMRMLMarkupsFiducialNode"),
                               "x axis": self.getNode("x axis", "vtkMRMLMarkupsLineNode"), "nasal aperture base": self.getNode("nasal aperture base", "vtkMRMLMarkupsLineNode"),
                               "for c)": self.getNode("for c)", "vtkMRMLMarkupsLineNode"), "AA FHP": self.getNode("AA FHP", "vtkMRMLMarkupsLineNode") }
            for name, node in required_nodes.items():
                if not node: raise ValueError(f"Required node '{name}' not found in the scene.")

            points = self.getPointPosByName('lmrks_Stephan', ["Nasion", "Rhinion", "Acanthion"])
            if not points: raise ValueError("Required points (Nasion, Rhinion, Acanthion) not found in 'lmrks_Stephan'.")
            
            nasion_pos, rhinion_pos, acanthion_pos = points
            pointX_pos = self.getNthPointPos(required_nodes["Point X"], 0)
            
            x_axis_p2 = self.getNthPointPos(required_nodes["x axis"], 1)
            angleNodeA = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'A) nasal bone angle'); angleNodeA.AddControlPoint(x_axis_p2); angleNodeA.AddControlPoint(nasion_pos); angleNodeA.AddControlPoint(rhinion_pos)

            nab_base_line = required_nodes["nasal aperture base"]
            p1 = self.getNthPointPos(nab_base_line, 0); p2 = self.getNthPointPos(nab_base_line, 1)
            closest_point_b = [0,0,0]; vtk.vtkLine.DistanceToLine(acanthion_pos, p1, p2, vtk.mutable(0), closest_point_b)
            line_b = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'B) line'); line_b.AddControlPoint(acanthion_pos); line_b.AddControlPoint(closest_point_b)

            for_c_line = required_nodes["for c)"]
            p1_c = self.getNthPointPos(for_c_line, 0); p2_c = self.getNthPointPos(for_c_line, 1)
            closest_point_c = [0,0,0]; vtk.vtkLine.DistanceToLine(rhinion_pos, p1_c, p2_c, vtk.mutable(0), closest_point_c)
            line_c = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'C) line'); line_c.AddControlPoint(rhinion_pos); line_c.AddControlPoint(closest_point_c)

            aa_fhp_ant = self.getNthPointPos(required_nodes["AA FHP"], 1)
            angleNodeD = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'D) nasal spine angle'); angleNodeD.AddControlPoint(acanthion_pos); angleNodeD.AddControlPoint(pointX_pos); angleNodeD.AddControlPoint(aa_fhp_ant)
            
            line_e = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'E) line'); line_e.AddControlPoint(nasion_pos); line_e.AddControlPoint(pointX_pos)
            return True
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to create measurements. Please ensure the framework is complete. Error: {e}")
            return False

    def calculatePrediction(self, sex):
        self.cleanup(prediction=True)
        try:
            measurement_nodes = { "A) nasal bone angle": self.getNode("A) nasal bone angle", "vtkMRMLMarkupsAngleNode"),
                                  "B) line": self.getNode("B) line", "vtkMRMLMarkupsLineNode"), "C) line": self.getNode("C) line", "vtkMRMLMarkupsLineNode"),
                                  "D) nasal spine angle": self.getNode("D) nasal spine angle", "vtkMRMLMarkupsAngleNode"), "E) line": self.getNode("E) line", "vtkMRMLMarkupsLineNode") }
            if not all(measurement_nodes.values()): raise ValueError("Not all measurement nodes (A, B, C, D, E) were found.")
            
            nasion_pos = self.getPointPosByName("lmrks_Stephan", ["Nasion"])
            if nasion_pos is None: raise ValueError("Nasion point not found in 'lmrks_Stephan'.")

            val_a = measurement_nodes["A) nasal bone angle"].GetAngleDegrees()
            val_b = np.linalg.norm(self.getNthPointPos(measurement_nodes["B) line"], 0) - self.getNthPointPos(measurement_nodes["B) line"], 1))
            val_c = np.linalg.norm(self.getNthPointPos(measurement_nodes["C) line"], 0) - self.getNthPointPos(measurement_nodes["C) line"], 1))
            val_d = measurement_nodes["D) nasal spine angle"].GetAngleDegrees()
            val_e = np.linalg.norm(self.getNthPointPos(measurement_nodes["E) line"], 0) - self.getNthPointPos(measurement_nodes["E) line"], 1))

            if sex == "Female":
                pos_x = -0.41 * val_a + 0.37 * val_b + 49.87
            else: # Male
                pos_x = -0.32 * val_a + 0.85 * val_b - 0.42 * val_c + 49.58
            pos_y = (-0.002 * val_d + 0.83) * val_e

            anterior_dir = np.array([0, 1, 0]); inferior_dir = np.array([0, 0, -1])
            intermediate_point = np.array(nasion_pos) + (inferior_dir * pos_y)
            final_point = intermediate_point + (anterior_dir * pos_x)

            pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pronasale pred')
            pred_node.AddControlPoint(final_point, 'Pronasale (Predicted)')
            pred_node.GetDisplayNode().SetSelectedColor(1, 0, 0)
            return True
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to calculate prediction. Error: {e}")
            return False

    def downloadAndLoadSoftTissue(self):
        path = self.downloadFile("https://github.com/user-attachments/files/20213398/soft_tissue_Stephan.mrk.json", "soft_tissue_Stephan.mrk.json")
        if path:
            self.getNode("soft_tissue_Stephan", exact=True) and slicer.mrmlScene.RemoveNode(self.getNode("soft_tissue_Stephan", exact=True))
            node = slicer.util.loadMarkups(path); node.SetName("soft_tissue_Stephan")
            return True
        return False

    def comparePrediction(self):
        self.cleanup(comparison=True)
        try:
            pred_node = self.getNode("pronasale pred", "vtkMRMLMarkupsFiducialNode")
            true_node = self.getNode("soft_tissue_Stephan", "vtkMRMLMarkupsFiducialNode")
            if not pred_node or not true_node:
                raise ValueError("Predicted pronasale and/or true soft tissue points not found.")
            
            pred_pos = self.getNthPointPos(pred_node, 0)
            true_pos = self.getNthPointPos(true_node, 0) # Assuming the true pronasale is the first point

            error_line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "pronasale error")
            error_line.AddControlPoint(pred_pos)
            error_line.AddControlPoint(true_pos)
            error_line.GetDisplayNode().SetSelectedColor(1,1,0) # Yellow
            
            error_dist = np.linalg.norm(pred_pos - true_pos)
            return true_pos, pred_pos, error_dist

        except Exception as e:
            slicer.util.errorDisplay(f"Failed to measure error. Error: {e}")
            return None

# --- Entry Point to start the GUI ---
try:
    old_gui = slicer.util.mainWindow().findChild(qt.QWidget, "StephanMethodGUI")
    if old_gui: old_gui.deleteLater()
except: pass
stephanGui = StephanMethodGUI()
stephanGui.show()

```
