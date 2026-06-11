This GUI uses a 4-point approach to relign the scan and create a Frankfort Horizontal Plane.
It also adds an option to make nasion the origin of the RAS coordinate system - you have to allocate the nasion from another landmark file (usually in the landmark files for any method or manually adding it, but must be called "n" or "nasion")

```python
import qt
import slicer
import urllib.request
import urllib.error
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
    pass

# --- Create our main widget (the floating window) ---
fhp_widget = qt.QWidget()
fhp_widget.setWindowTitle("4-Point FHP Realign + Nasion Origin")

# --- Set up the layout ---
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
inputFiducialsSelector.setToolTip("FHP landmarks (poR, poL, orR, orL).")
formLayout.addRow("Frankfort Plane landmarks (poR, poL, orR, orL):", inputFiducialsSelector)

instructionLabel = qt.QLabel("Please place all four landmarks (poR, poL, orR, orL) before proceeding.\n\n"
                             "poR = right porion, poL = left porion,\norR = right orbitale, orL = left orbitale\n\n"
                             "If you check the box below, also place a point named 'nasion' or 'n' in ANY fiducial list.")
instructionLabel.setWordWrap(True)
panelLayout.addWidget(instructionLabel)

# --- Option to move nasion to origin AFTER FHP realignment ---
nasionOriginCheckbox = qt.QCheckBox("After FHP realignment, move nasion to origin (0,0,0)")
nasionOriginCheckbox.setToolTip("Will search all fiducial nodes for a point labelled 'nasion' or 'n'.")
panelLayout.addWidget(nasionOriginCheckbox)

# --- Action Buttons ---
applyButton = qt.QPushButton("Apply 4-Point FHP Realignment")
applyButton.toolTip = "Run the 4-point FHP realignment on the input volume (makes transform permanent)."
applyButton.enabled = False
panelLayout.addWidget(applyButton)

undoButton = qt.QPushButton("Undo Realignment")
undoButton.toolTip = "Revert the volume to its original position before realignment."
undoButton.enabled = False
panelLayout.addWidget(undoButton)

panelLayout.addStretch(1)

# --- Global variables to manage state ---
originalTransformNode = None
fhpTransformRoot = None
originalFiducialTransform = None
translationTransformNode = None

def findNasionLandmark():
    """Search all MarkupsFiducial nodes for a point with label 'nasion' or 'n' (case‑insensitive)."""
    scene = slicer.mrmlScene
    nodes = scene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
    nodes.UnRegister(scene)
    for i in range(nodes.GetNumberOfItems()):
        node = nodes.GetItemAsObject(i)
        for j in range(node.GetNumberOfControlPoints()):
            label = node.GetNthControlPointLabel(j).strip().lower()
            if label in ["nasion", "n"]:
                return node, j
    return None, -1

def onSelect():
    fiducialNode = inputFiducialsSelector.currentNode()
    if fiducialNode:
        labels = [fiducialNode.GetNthControlPointLabel(i) for i in range(fiducialNode.GetNumberOfControlPoints())]
        hasAllPoints = all(label in labels for label in ['poR', 'poL', 'orR', 'orL'])
        applyButton.enabled = bool(inputVolumeSelector.currentNode() and hasAllPoints)
    else:
        applyButton.enabled = False
    undoButton.enabled = bool(fhpTransformRoot) or bool(translationTransformNode)

def createFHPPlane(poR, poL, orR, orL):
    points = numpy.vstack([poR, poL, orR, orL])
    centroid = numpy.mean(points, axis=0)
    centered_points = points - centroid
    U, S, Vt = numpy.linalg.svd(centered_points)
    normal = Vt[2]
    if normal[2] < 0:
        normal = -normal
    existingPlane = slicer.mrmlScene.GetFirstNodeByName("FHP")
    if existingPlane:
        slicer.mrmlScene.RemoveNode(existingPlane)
    planeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "FHP")
    planeNode.SetOrigin(centroid)
    planeNode.SetNormal(normal)
    displayNode = planeNode.GetDisplayNode()
    displayNode.SetColor(0.31, 0.78, 0.47)
    displayNode.SetSelectedColor(0.31, 0.78, 0.47)
    displayNode.SetVisibility(True)
    planeNode.SetSize(200, 200)
    print("Created 'FHP' transverse plane")
    return planeNode

def onRealignButton():
    global originalTransformNode, fhpTransformRoot, originalFiducialTransform, translationTransformNode

    inputVolume = inputVolumeSelector.currentNode()
    fiducials = inputFiducialsSelector.currentNode()

    # Save original transforms
    if not originalTransformNode:
        existingTransformID = inputVolume.GetTransformNodeID()
        if existingTransformID:
            originalTransformNode = slicer.mrmlScene.GetNodeByID(existingTransformID)
        else:
            identityMatrix = vtk.vtkMatrix4x4()
            originalTransformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "Original_Position_Backup")
            originalTransformNode.SetMatrixTransformToParent(identityMatrix)
        print("Saved original volume position.")

    originalFiducialTransform = fiducials.GetTransformNodeID()

    # Get FHP landmark coordinates
    landmarks = {}
    for i in range(fiducials.GetNumberOfControlPoints()):
        label = fiducials.GetNthControlPointLabel(i)
        pos = [0,0,0]
        fiducials.GetNthControlPointPositionWorld(i, pos)
        landmarks[label] = numpy.array(pos)

    required = ['poR', 'poL', 'orR', 'orL']
    for req in required:
        if req not in landmarks:
            slicer.util.errorDisplay(f"Missing landmark: {req}. Please add it to the fiducial list.")
            return

    poR = landmarks['poR'].copy()
    poL = landmarks['poL'].copy()
    orR = landmarks['orR'].copy()
    orL = landmarks['orL'].copy()

    # --- Yaw ---
    po_vector = poR - poL
    yaw_angle = -numpy.arctan2(po_vector[1], po_vector[0]) * 180 / numpy.pi
    vTransform1 = vtk.vtkTransform()
    vTransform1.RotateZ(yaw_angle)
    transform1 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Yaw')
    transform1.SetMatrixTransformToParent(vTransform1.GetMatrix())
    inputVolume.SetAndObserveTransformNodeID(transform1.GetID())
    fiducials.SetAndObserveTransformNodeID(transform1.GetID())

    currentMatrix = vtk.vtkMatrix4x4()
    currentMatrix.DeepCopy(transform1.GetMatrixTransformToParent())
    poR = numpy.array(currentMatrix.MultiplyPoint([poR[0], poR[1], poR[2], 1.0])[:3])
    poL = numpy.array(currentMatrix.MultiplyPoint([poL[0], poL[1], poL[2], 1.0])[:3])
    orR = numpy.array(currentMatrix.MultiplyPoint([orR[0], orR[1], orR[2], 1.0])[:3])
    orL = numpy.array(currentMatrix.MultiplyPoint([orL[0], orL[1], orL[2], 1.0])[:3])

    # --- Roll ---
    po_vector = poR - poL
    roll_angle = numpy.arctan2(po_vector[2], po_vector[0]) * 180 / numpy.pi
    vTransform2 = vtk.vtkTransform()
    vTransform2.RotateY(roll_angle)
    transform2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Roll')
    transform2.SetMatrixTransformToParent(vTransform2.GetMatrix())
    transform1.SetAndObserveTransformNodeID(transform2.GetID())
    currentMatrix.DeepCopy(transform2.GetMatrixTransformToParent())
    poR = numpy.array(currentMatrix.MultiplyPoint([poR[0], poR[1], poR[2], 1.0])[:3])
    poL = numpy.array(currentMatrix.MultiplyPoint([poL[0], poL[1], poL[2], 1.0])[:3])
    orR = numpy.array(currentMatrix.MultiplyPoint([orR[0], orR[1], orR[2], 1.0])[:3])
    orL = numpy.array(currentMatrix.MultiplyPoint([orL[0], orL[1], orL[2], 1.0])[:3])

    # --- Pitch ---
    or_midpoint = (orR + orL) / 2.0
    po_midpoint = (poR + poL) / 2.0
    po_or_vector = or_midpoint - po_midpoint
    pitch_angle = -numpy.arctan2(po_or_vector[2], po_or_vector[1]) * 180 / numpy.pi
    vTransform3 = vtk.vtkTransform()
    vTransform3.RotateX(pitch_angle)
    transform3 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Pitch')
    transform3.SetMatrixTransformToParent(vTransform3.GetMatrix())
    transform2.SetAndObserveTransformNodeID(transform3.GetID())
    finalMatrix = vtk.vtkMatrix4x4()
    finalMatrix.DeepCopy(transform3.GetMatrixTransformToParent())

    # Update FHP landmarks after full rotation
    poR_final = numpy.array(finalMatrix.MultiplyPoint([poR[0], poR[1], poR[2], 1.0])[:3])
    poL_final = numpy.array(finalMatrix.MultiplyPoint([poL[0], poL[1], poL[2], 1.0])[:3])
    orR_final = numpy.array(finalMatrix.MultiplyPoint([orR[0], orR[1], orR[2], 1.0])[:3])
    orL_final = numpy.array(finalMatrix.MultiplyPoint([orL[0], orL[1], orL[2], 1.0])[:3])

    fhpTransformRoot = transform1

    # Remove transform from FHP fiducials and update their positions
    fiducials.SetAndObserveTransformNodeID(None)
    for i in range(fiducials.GetNumberOfControlPoints()):
        label = fiducials.GetNthControlPointLabel(i)
        if label == 'poR':
            fiducials.SetNthControlPointPositionWorld(i, poR_final)
        elif label == 'poL':
            fiducials.SetNthControlPointPositionWorld(i, poL_final)
        elif label == 'orR':
            fiducials.SetNthControlPointPositionWorld(i, orR_final)
        elif label == 'orL':
            fiducials.SetNthControlPointPositionWorld(i, orL_final)

    # Harden the rotation transform (makes it permanent)
    slicer.vtkSlicerTransformLogic().hardenTransform(inputVolume)

    # --- Optional translation to move nasion to origin (after hardening) ---
    moveNasionToOrigin = nasionOriginCheckbox.isChecked()
    translation_vector = numpy.array([0.0, 0.0, 0.0])
    nasion_node, nasion_idx = findNasionLandmark()

    if moveNasionToOrigin:
        if nasion_node is None:
            slicer.util.errorDisplay("Nasion landmark not found.\nPlease add a point named 'nasion' or 'n' in any fiducial list.")
        else:
            # Get current world position of nasion (after rotation)
            nasion_pos = [0,0,0]
            nasion_node.GetNthControlPointPositionWorld(nasion_idx, nasion_pos)
            translation_vector = -numpy.array(nasion_pos)
            print(f"Translation to move nasion to origin: {translation_vector} mm")

            # Create and apply a translation transform
            vTranslate = vtk.vtkTransform()
            vTranslate.Translate(translation_vector)
            translationTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Nasion_Translation')
            translationTransformNode.SetMatrixTransformToParent(vTranslate.GetMatrix())
            inputVolume.SetAndObserveTransformNodeID(translationTransformNode.GetID())

            # Apply the same translation to ALL fiducial points in the scene
            # so they stay aligned with the volume.
            scene = slicer.mrmlScene
            allFiducialNodes = scene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
            allFiducialNodes.UnRegister(scene)
            for i in range(allFiducialNodes.GetNumberOfItems()):
                node = allFiducialNodes.GetItemAsObject(i)
                for j in range(node.GetNumberOfControlPoints()):
                    pos = [0,0,0]
                    node.GetNthControlPointPositionWorld(j, pos)
                    new_pos = vTranslate.TransformPoint(pos)
                    node.SetNthControlPointPositionWorld(j, new_pos)

            # Harden the translation transform
            slicer.vtkSlicerTransformLogic().hardenTransform(inputVolume)
            # Remove the temporary transform node
            slicer.mrmlScene.RemoveNode(translationTransformNode)
            translationTransformNode = None

            # Ensure the nasion landmark is exactly at (0,0,0)
            if nasion_node:
                nasion_node.SetNthControlPointPositionWorld(nasion_idx, [0.0, 0.0, 0.0])

    # Update UI
    undoButton.enabled = True
    applyButton.enabled = False

    # Info message
    info_text = f"4-point FHP realignment complete!\nYaw: {yaw_angle:.1f}°, Roll: {roll_angle:.1f}°, Pitch: {pitch_angle:.1f}°"
    if moveNasionToOrigin and nasion_node:
        info_text += f"\nNasion moved to origin (Δx={translation_vector[0]:.2f}, Δy={translation_vector[1]:.2f}, Δz={translation_vector[2]:.2f})"
    slicer.util.infoDisplay(info_text)

    # Optional FHP plane
    reply = qt.QMessageBox.question(fhp_widget, "Create FHP Plane?",
                                    "Do you want to create a visualization plane for the new Frankfurt Horizontal Plane?",
                                    qt.QMessageBox.Yes | qt.QMessageBox.No)
    if reply == qt.QMessageBox.Yes:
        createFHPPlane(poR_final, poL_final, orR_final, orL_final)

def onUndoButton():
    global fhpTransformRoot, originalFiducialTransform, translationTransformNode
    inputVolume = inputVolumeSelector.currentNode()
    fiducials = inputFiducialsSelector.currentNode()

    if not inputVolume:
        return

    # Revert volume transform
    if originalTransformNode:
        inputVolume.SetAndObserveTransformNodeID(originalTransformNode.GetID())
    else:
        inputVolume.SetAndObserveTransformNodeID(None)

    # Revert FHP fiducials transform
    if originalFiducialTransform:
        fiducials.SetAndObserveTransformNodeID(originalFiducialTransform)
    else:
        fiducials.SetAndObserveTransformNodeID(None)

    # Remove our transform nodes
    if fhpTransformRoot:
        slicer.mrmlScene.RemoveNode(fhpTransformRoot)
        fhpTransformRoot = None
    if translationTransformNode:
        slicer.mrmlScene.RemoveNode(translationTransformNode)
        translationTransformNode = None

    undoButton.enabled = False
    applyButton.enabled = True
    slicer.util.infoDisplay("Realignment undone (transform removed).")

def download_github_attachment(url, destination):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.getcode() == 200:
                with open(destination, 'wb') as f:
                    f.write(response.read())
                return True
    except Exception as e:
        print(f"Download error: {e}")
    return False

def autoLoadLandmarks():
    existing = slicer.mrmlScene.GetFirstNodeByName("FHP_4Point_Landmarks")
    if existing:
        inputFiducialsSelector.setCurrentNode(existing)
        print("Landmarks already loaded in scene.")
        return
    url = "https://github.com/user-attachments/files/26278568/FHP4.mrk.json"
    fileName = "FHP4.mrk.json"
    tempPath = os.path.join(slicer.app.temporaryPath, fileName)
    print("Downloading landmarks from GitHub...")
    if download_github_attachment(url, tempPath):
        try:
            loadedNode = slicer.util.loadMarkups(tempPath)
            if loadedNode:
                loadedNode.SetName("FHP_4Point_Landmarks")
                inputFiducialsSelector.setCurrentNode(loadedNode)
                print("Successfully loaded 4-point landmarks.")
                return
        except Exception as e:
            print(f"Error loading markups: {e}")
    print("Download failed. Please load the landmarks manually.")
    slicer.util.warningDisplay(
        "Could not auto-download landmarks from GitHub.\n\n"
        "Please load the FHP4.mrk.json file manually using File > Add Data.\n"
        "You can also place the four landmarks manually using the Markups module."
    )

# --- Connect buttons and show ---
applyButton.connect('clicked(bool)', onRealignButton)
undoButton.connect('clicked(bool)', onUndoButton)
inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)
inputFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)

fhp_widget.show()
autoLoadLandmarks()
onSelect()
print("4-Point FHP Realign panel is now showing. Ready for use.")
```
