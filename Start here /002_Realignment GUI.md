```ptyhon
import qt
import ctk
import slicer
import urllib.request
import os
import vtk
import numpy

# --- Use a global variable to keep track of our widget ---
global fhp_widget

# --- If the window already exists, close it before creating a new one ---
try:
    fhp_widget.close()
    print("Closed the old FHP Realign panel.")
except:
    pass # Do nothing if it's the first time running

# --- Create our main widget (the floating window) ---
fhp_widget = qt.QWidget()
fhp_widget.setWindowTitle("FHP Realign Tool")

# --- Set up the layout and widgets inside our window ---
panelLayout = qt.QVBoxLayout(fhp_widget)
formLayout = qt.QFormLayout()
panelLayout.addLayout(formLayout)

# --- Input and Landmark Selectors ---
inputVolumeSelector = slicer.qMRMLNodeComboBox()
inputVolumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
inputVolumeSelector.setMRMLScene(slicer.mrmlScene)
inputVolumeSelector.setToolTip("Pick the input CT volume to be realigned.")
formLayout.addRow("Input Volume: ", inputVolumeSelector)

inputFiducialsSelector = slicer.qMRMLNodeComboBox()
inputFiducialsSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
inputFiducialsSelector.setMRMLScene(slicer.mrmlScene)
inputFiducialsSelector.setToolTip("These are the landmarks to define the Frankfort Horizontal Plane.")
formLayout.addRow("Frankfort Horizontal Plane aligner landmarks:", inputFiducialsSelector)

# --- Add the instructional label ---
instructionLabel = qt.QLabel("Please place all three landmarks (poR, poL, zyoL) before proceeding.")
instructionLabel.setWordWrap(True)
panelLayout.addWidget(instructionLabel)

# --- Action Buttons ---
applyButton = qt.QPushButton("Apply Realign")
applyButton.toolTip = "Run the FHP realignment on the input volume."
applyButton.enabled = False
panelLayout.addWidget(applyButton)

undoButton = qt.QPushButton("Undo Realignment")
undoButton.toolTip = "Revert the volume to its original position before realignment."
undoButton.enabled = False
panelLayout.addWidget(undoButton)

# --- Widgets for the new 4-Point Plane feature (initially hidden) ---
fhp4_instructionLabel = qt.QLabel("\nPlease re-allocate all four landmarks for the measurement plane. The transformation did not involve these new landmarks.")
fhp4_instructionLabel.setWordWrap(True)
fhp4_instructionLabel.visible = False
panelLayout.addWidget(fhp4_instructionLabel)

createFHP4Button = qt.QPushButton("Create 4-point FHP")
createFHP4Button.toolTip = "Create a best-fit plane from the four adjusted landmarks."
createFHP4Button.visible = False
panelLayout.addWidget(createFHP4Button)

# Add vertical spacer at the end
panelLayout.addStretch(1)

# --- Global variables to manage state ---
originalTransformNode = None
fhpTransformNode = None

# --- Define the functions that make the buttons work ---

def onSelect():
    """Enable the apply button only if both inputs are selected."""
    fiducialNode = inputFiducialsSelector.currentNode()
    if fiducialNode:
        labels = [fiducialNode.GetNthControlPointLabel(i) for i in range(fiducialNode.GetNumberOfControlPoints())]
        hasPoints = 'poR' in labels and 'poL' in labels and 'zyoL' in labels
        applyButton.enabled = bool(inputVolumeSelector.currentNode() and hasPoints)
    else:
        applyButton.enabled = False
    undoButton.enabled = bool(fhpTransformNode)

def onRealignButton():
    """Performs the realignment logic and then asks about the next step."""
    global originalTransformNode, fhpTransformNode
    
    inputVolume = inputVolumeSelector.currentNode()
    fiducials = inputFiducialsSelector.currentNode()
    slicer.util.infoDisplay("Applying FHP realignment...")

    if not originalTransformNode:
        existingTransformID = inputVolume.GetTransformNodeID()
        if existingTransformID: originalTransformNode = slicer.mrmlScene.GetNodeByID(existingTransformID)
        else:
            identityMatrix = vtk.vtkMatrix4x4()
            originalTransformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "Original_Position_Backup")
            originalTransformNode.SetMatrixTransformToParent(identityMatrix)
        print("Saved original volume position.")

    poR_pos, poL_pos, zyoL_pos = None, None, None
    for i in range(fiducials.GetNumberOfControlPoints()):
        label = fiducials.GetNthControlPointLabel(i)
        pos = [0,0,0]; fiducials.GetNthControlPointPositionWorld(i, pos)
        if label == 'poR': poR_pos = numpy.array(pos)
        if label == 'poL': poL_pos = numpy.array(pos)
        if label == 'zyoL': zyoL_pos = numpy.array(pos)

    po_vec = poR_pos - poL_pos
    vTransform1 = vtk.vtkTransform(); vTransform1.RotateZ(-numpy.arctan2(po_vec[1], po_vec[0]) * 180 / numpy.pi)
    zyoL_p1 = numpy.array(vTransform1.GetMatrix().MultiplyPoint(numpy.append(zyoL_pos, 1.0)))[:3]
    poR_p1 = numpy.array(vTransform1.GetMatrix().MultiplyPoint(numpy.append(poR_pos, 1.0)))[:3]
    poL_p1 = numpy.array(vTransform1.GetMatrix().MultiplyPoint(numpy.append(poL_pos, 1.0)))[:3]
    
    po_vec_p1 = poR_p1 - poL_p1
    vTransform2 = vtk.vtkTransform(); vTransform2.RotateY(numpy.arctan2(po_vec_p1[2], po_vec_p1[0]) * 180 / numpy.pi)
    
    zyoL_p2 = numpy.array(vTransform2.GetMatrix().MultiplyPoint(numpy.append(zyoL_p1, 1.0)))[:3]
    poR_p2 = numpy.array(vTransform2.GetMatrix().MultiplyPoint(numpy.append(poR_p1, 1.0)))[:3]
    poL_p2 = numpy.array(vTransform2.GetMatrix().MultiplyPoint(numpy.append(poL_p1, 1.0)))[:3]
    
    mid_porion_p2 = (poR_p2 + poL_p2) / 2.0
    po_zyo_vec = zyoL_p2 - mid_porion_p2
    vTransform3 = vtk.vtkTransform(); vTransform3.RotateX(-numpy.arctan2(po_zyo_vec[2], po_zyo_vec[1]) * 180 / numpy.pi)
    
    final_transform = vtk.vtkTransform(); final_transform.Concatenate(vTransform1); final_transform.Concatenate(vTransform2); final_transform.Concatenate(vTransform3)

    if not fhpTransformNode: fhpTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Realign_Transform')
    fhpTransformNode.SetMatrixTransformToParent(final_transform.GetMatrix())
    inputVolume.SetAndObserveTransformNodeID(fhpTransformNode.GetID())
    
    undoButton.enabled = True
    slicer.util.infoDisplay("Realignment applied. Use 'Undo' to revert.")

    msgBox = qt.QMessageBox()
    msgBox.setText("Realignment complete.")
    msgBox.setInformativeText("Do you want to create a 4-point FHP for later measurements?")
    msgBox.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.No)
    msgBox.setDefaultButton(qt.QMessageBox.Yes)
    ret = msgBox.exec_()
    
    if ret == qt.QMessageBox.Yes:
        setupFHP4PointPlane()

def onUndoButton():
    """Reverts the volume to its original saved position."""
    global fhpTransformNode
    inputVolume = inputVolumeSelector.currentNode()
    if not inputVolume: return
    if originalTransformNode: inputVolume.SetAndObserveTransformNodeID(originalTransformNode.GetID())
    else: inputVolume.SetAndObserveTransformNodeID(None)
    if fhpTransformNode: slicer.mrmlScene.RemoveNode(fhpTransformNode); fhpTransformNode = None
    undoButton.enabled = False
    slicer.util.infoDisplay("Realignment undone.")

def setupFHP4PointPlane():
    """Downloads the 4-point landmarks and shows the UI."""
    # --- THIS IS THE CORRECTED LINK ---
    url = "https://github.com/user-attachments/files/22434548/FH4_landmarks.json"
    fileName = "FH4_landmarks.json"
    
    if slicer.mrmlScene.GetFirstNodeByName("FH4_landmarks"):
        print("4-point landmarks file already in scene.")
    else:
        try:
            tempPath = os.path.join(slicer.app.temporaryPath, fileName)
            urllib.request.urlretrieve(url, tempPath)
            loadedNode = slicer.util.loadMarkups(tempPath)
            if loadedNode: loadedNode.SetName("FH4_landmarks")
        except Exception as e:
            slicer.util.errorDisplay(f"Could not download 4-point landmarks file: {e}")
    
    fhp4_instructionLabel.visible = True
    createFHP4Button.visible = True

def createFHP4PointPlane():
    """Creates the best-fit plane from the 4 landmarks."""
    slicer.util.infoDisplay("Creating 4-point FHP plane...")
    landmarksNode = slicer.util.getNode("FH4_landmarks")
    if not landmarksNode or landmarksNode.GetNumberOfControlPoints() < 4:
        slicer.util.errorDisplay("Could not find 'FH4_landmarks' node or it has fewer than 4 points. Please place all four points.")
        return

    points = numpy.array([landmarksNode.GetNthControlPointPosition(i) for i in range(landmarksNode.GetNumberOfControlPoints())])
    centroid = points.mean(axis=0)
    _, _, vh = numpy.linalg.svd(points - centroid)
    normal = vh[2]

    planeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "FHP")
    planeNode.SetOrigin(centroid)
    planeNode.SetNormal(normal)
    
    displayNode = planeNode.GetDisplayNode()
    displayNode.SetColor(0.31, 0.78, 0.47)
    displayNode.SetSelectedColor(0.31, 0.78, 0.47)
    displayNode.SetVisibility(True)
    
    print("Successfully created 'FHP' plane.")
    createFHP4Button.enabled = False

def autoLoadLandmarks():
    """Downloads and loads the initial 3-point FHP landmarks."""
    if slicer.mrmlScene.GetFirstNodeByName("FHP_Standard_Landmarks"):
        inputFiducialsSelector.setCurrentNode(slicer.mrmlScene.GetFirstNodeByName("FHP_Standard_Landmarks"))
        return
    url = "https://github.com/user-attachments/files/22434441/FHP_landmarks.json"
    fileName = "FHP_landmarks.json"
    try:
        tempPath = os.path.join(slicer.app.temporaryPath, fileName)
        urllib.request.urlretrieve(url, tempPath)
        loadedNode = slicer.util.loadMarkups(tempPath)
        if loadedNode: loadedNode.SetName("FHP_Standard_Landmarks"); inputFiducialsSelector.setCurrentNode(loadedNode)
    except Exception as e:
        slicer.util.errorDisplay(f"Could not download landmarks file: {e}")

# --- Connect buttons to functions and show the window ---
applyButton.connect('clicked(bool)', onRealignButton)
undoButton.connect('clicked(bool)', onUndoButton)
createFHP4Button.connect('clicked(bool)', createFHP4PointPlane)
inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)
inputFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)

fhp_widget.show()
autoLoadLandmarks()
onSelect()
print("FHP Realign panel is now showing. Ready for use.")
```
