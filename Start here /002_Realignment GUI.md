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

# Add vertical spacer at the end
panelLayout.addStretch(1)

# --- Global variables to manage state ---
originalTransformNode = None # To store the volume's original transform
fhpTransformNode = None # To store the new FHP transform we create

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
    
    # The undo button should only be enabled if a transform has been applied
    undoButton.enabled = bool(fhpTransformNode)

def onRealignButton():
    """Performs the realignment logic, modifying the original volume."""
    global originalTransformNode, fhpTransformNode
    
    inputVolume = inputVolumeSelector.currentNode()
    fiducials = inputFiducialsSelector.currentNode()
    
    slicer.util.infoDisplay("Applying FHP realignment...")

    # --- Save the original transform if it hasn't been saved yet ---
    if not originalTransformNode:
        # Check if the volume already has a transform
        existingTransformID = inputVolume.GetTransformNodeID()
        if existingTransformID:
            originalTransformNode = slicer.mrmlScene.GetNodeByID(existingTransformID)
        else:
            # If no transform, create an identity matrix (which means "no change")
            identityMatrix = vtk.vtkMatrix4x4()
            originalTransformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "Original_Position_Backup")
            originalTransformNode.SetMatrixTransformToParent(identityMatrix)
        print("Saved original volume position.")

    # --- Calculate the new FHP transform ---
    # (This logic is the same as before)
    poR_pos, poL_pos, zyoL_pos = None, None, None
    for i in range(fiducials.GetNumberOfControlPoints()):
        label = fiducials.GetNthControlPointLabel(i)
        pos = [0,0,0]; fiducials.GetNthControlPointPositionWorld(i, pos)
        if label == 'poR': poR_pos = numpy.array(pos)
        if label == 'poL': poL_pos = numpy.array(pos)
        if label == 'zyoL': zyoL_pos = numpy.array(pos)

    # Yaw
    po_vec = poR_pos - poL_pos
    vTransform1 = vtk.vtkTransform(); vTransform1.RotateZ(-numpy.arctan2(po_vec[1], po_vec[0]) * 180 / numpy.pi)
    
    # Roll
    poR_p1 = numpy.array(vTransform1.GetMatrix().MultiplyPoint(numpy.append(poR_pos, 1.0)))[:3]
    poL_p1 = numpy.array(vTransform1.GetMatrix().MultiplyPoint(numpy.append(poL_pos, 1.0)))[:3]
    zyoL_p1 = numpy.array(vTransform1.GetMatrix().MultiplyPoint(numpy.append(zyoL_pos, 1.0)))[:3]
    po_vec_p1 = poR_p1 - poL_p1
    vTransform2 = vtk.vtkTransform(); vTransform2.RotateY(numpy.arctan2(po_vec_p1[2], po_vec_p1[0]) * 180 / numpy.pi)
    
    # Pitch
    zyoL_p2 = numpy.array(vTransform2.GetMatrix().MultiplyPoint(numpy.append(zyoL_p1, 1.0)))[:3]
    poR_p2 = numpy.array(vTransform2.GetMatrix().MultiplyPoint(numpy.append(poR_p1, 1.0)))[:3]
    poL_p2 = numpy.array(vTransform2.GetMatrix().MultiplyPoint(numpy.append(poL_p1, 1.0)))[:3]
    mid_porion_p2 = (poR_p2 + poL_p2) / 2.0
    po_zyo_vec = zyoL_p2 - mid_porion_p2
    vTransform3 = vtk.vtkTransform(); vTransform3.RotateX(-numpy.arctan2(po_zyo_vec[2], po_zyo_vec[1]) * 180 / numpy.pi)
    
    # Combine all transforms into a single matrix
    final_transform = vtk.vtkTransform()
    final_transform.Concatenate(vTransform1)
    final_transform.Concatenate(vTransform2)
    final_transform.Concatenate(vTransform3)

    # --- Apply the new transform to the volume ---
    if not fhpTransformNode:
        fhpTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Realign_Transform')
    
    fhpTransformNode.SetMatrixTransformToParent(final_transform.GetMatrix())
    inputVolume.SetAndObserveTransformNodeID(fhpTransformNode.GetID())
    
    undoButton.enabled = True
    slicer.util.infoDisplay("Realignment applied. Use 'Undo' to revert.")

def onUndoButton():
    """Reverts the volume to its original saved position."""
    global fhpTransformNode
    
    inputVolume = inputVolumeSelector.currentNode()
    if not inputVolume:
        slicer.util.warningDisplay("No input volume selected.")
        return
        
    if originalTransformNode:
        inputVolume.SetAndObserveTransformNodeID(originalTransformNode.GetID())
        slicer.util.infoDisplay("Realignment undone. Volume restored to original position.")
    else:
        # If there was no original transform, just untransform the volume
        inputVolume.SetAndObserveTransformNodeID(None)
        slicer.util.infoDisplay("Realignment undone.")
    
    # Clean up the FHP transform we created
    if fhpTransformNode:
        slicer.mrmlScene.RemoveNode(fhpTransformNode)
        fhpTransformNode = None
    
    undoButton.enabled = False

def autoLoadLandmarks():
    """Downloads and loads the FHP landmarks file."""
    if slicer.mrmlScene.GetFirstNodeByName("FHP_Standard_Landmarks"):
        inputFiducialsSelector.setCurrentNode(slicer.mrmlScene.GetFirstNodeByName("FHP_Standard_Landmarks"))
        return

    url = "https://github.com/user-attachments/files/21429663/FHP_landmarks.mrk.json"
    fileName = "FHP_landmarks.mrk.json"
    tempPath = os.path.join(slicer.app.temporaryPath, fileName)
    
    try:
        urllib.request.urlretrieve(url, tempPath)
        loadedNode = slicer.util.loadMarkups(tempPath)
        if loadedNode:
            loadedNode.SetName("FHP_Standard_Landmarks")
            inputFiducialsSelector.setCurrentNode(loadedNode)
    except Exception as e:
        slicer.util.errorDisplay(f"Could not download landmarks file: {e}")

# --- Connect buttons to functions and show the window ---
applyButton.connect('clicked(bool)', onRealignButton)
undoButton.connect('clicked(bool)', onUndoButton)
inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)
inputFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)

fhp_widget.show()
autoLoadLandmarks()
onSelect()
print("FHP Realign panel is now showing. Ready for use.")
```
