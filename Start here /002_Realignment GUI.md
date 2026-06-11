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

def translate_all_markups(translation_vector):
    """
    Apply translation to all markup nodes (fiducials, lines, planes, curves, ROIs, etc.)
    For planes: translate origin, leave normal unchanged.
    For others: translate each control point.
    """
    scene = slicer.mrmlScene
    def trans(p):
        return [p[0] + translation_vector[0], p[1] + translation_vector[1], p[2] + translation_vector[2]]

    # 1. Fiducial nodes
    fid_nodes = scene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
    fid_nodes.UnRegister(scene)
    for i in range(fid_nodes.GetNumberOfItems()):
        node = fid_nodes.GetItemAsObject(i)
        for j in range(node.GetNumberOfControlPoints()):
            pos = [0.0, 0.0, 0.0]
            node.GetNthControlPointPositionWorld(j, pos)
            node.SetNthControlPointPositionWorld(j, trans(pos))
        node.SetAndObserveTransformNodeID(None)

    # 2. Line, curve, closed curve, angle, ROI nodes
    line_classes = ["vtkMRMLMarkupsLineNode", "vtkMRMLMarkupsCurveNode",
                    "vtkMRMLMarkupsClosedCurveNode", "vtkMRMLMarkupsAngleNode",
                    "vtkMRMLMarkupsROINode"]
    for cls in line_classes:
        nodes = scene.GetNodesByClass(cls)
        nodes.UnRegister(scene)
        for i in range(nodes.GetNumberOfItems()):
            node = nodes.GetItemAsObject(i)
            for j in range(node.GetNumberOfControlPoints()):
                pos = [0.0, 0.0, 0.0]
                node.GetNthControlPointPositionWorld(j, pos)
                node.SetNthControlPointPositionWorld(j, trans(pos))
            node.SetAndObserveTransformNodeID(None)

    # 3. Plane nodes: translate origin, keep normal
    plane_nodes = scene.GetNodesByClass("vtkMRMLMarkupsPlaneNode")
    plane_nodes.UnRegister(scene)
    for i in range(plane_nodes.GetNumberOfItems()):
        plane = plane_nodes.GetItemAsObject(i)
        origin = [0.0, 0.0, 0.0]
        plane.GetOrigin(origin)
        plane.SetOrigin(trans(origin))
        plane.SetAndObserveTransformNodeID(None)

def compute_fhp_transform(poR, poL, orR, orL):
    """
    Compute a rotation matrix that aligns the Frankfort Horizontal Plane to the XY plane
    and the inter‑porion line to the X axis (left‑right).
    Returns a vtkMatrix4x4 (rotation only, no translation).
    """
    # 1. Compute FHP plane normal (best fit of all 4 points)
    pts = numpy.vstack([poR, poL, orR, orL])
    centroid = numpy.mean(pts, axis=0)
    centered = pts - centroid
    U, S, Vt = numpy.linalg.svd(centered)
    normal = Vt[2]                     # plane normal
    if normal[2] < 0:                  # ensure superior direction
        normal = -normal

    # 2. Compute left‑right axis (from left porion to right porion)
    lr = poR - poL
    lr = lr / numpy.linalg.norm(lr)

    # 3. Compute anterior axis (orthogonal to normal and lr)
    anterior = numpy.cross(normal, lr)
    anterior = anterior / numpy.linalg.norm(anterior)

    # 4. Re‑orthogonalise (ensure normal is perpendicular to both)
    normal = numpy.cross(lr, anterior)
    normal = normal / numpy.linalg.norm(normal)

    # 5. Build rotation matrix from world axes to desired basis
    #    We want world X → lr, world Y → anterior, world Z → normal
    rot_matrix = vtk.vtkMatrix4x4()
    for i in range(3):
        rot_matrix.SetElement(i, 0, lr[i])
        rot_matrix.SetElement(i, 1, anterior[i])
        rot_matrix.SetElement(i, 2, normal[i])
    rot_matrix.SetElement(3, 3, 1.0)

    # The above matrix maps local basis to world. We need the inverse (world to local)
    # Since the basis is orthonormal, inverse is transpose.
    rot_matrix_inv = vtk.vtkMatrix4x4()
    rot_matrix_inv.DeepCopy(rot_matrix)
    rot_matrix_inv.Invert()
    return rot_matrix_inv

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

    poR = landmarks['poR']
    poL = landmarks['poL']
    orR = landmarks['orR']
    orL = landmarks['orL']

    # Compute the rotation matrix
    rot_matrix = compute_fhp_transform(poR, poL, orR, orL)

    # Create a transform node with this rotation
    transformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Rotation')
    transformNode.SetMatrixTransformToParent(rot_matrix)

    # Apply to volume and fiducials
    inputVolume.SetAndObserveTransformNodeID(transformNode.GetID())
    fiducials.SetAndObserveTransformNodeID(transformNode.GetID())

    # Update landmark coordinates to their rotated positions (for later use)
    finalMatrix = vtk.vtkMatrix4x4()
    transformNode.GetMatrixTransformToParent(finalMatrix)

    def apply_matrix(pt):
        h = [pt[0], pt[1], pt[2], 1.0]
        return numpy.array(finalMatrix.MultiplyPoint(h)[:3])

    poR_rot = apply_matrix(poR)
    poL_rot = apply_matrix(poL)
    orR_rot = apply_matrix(orR)
    orL_rot = apply_matrix(orL)

    fhpTransformRoot = transformNode

    # Remove transform from fiducials and update their positions
    fiducials.SetAndObserveTransformNodeID(None)
    for i in range(fiducials.GetNumberOfControlPoints()):
        label = fiducials.GetNthControlPointLabel(i)
        if label == 'poR':
            fiducials.SetNthControlPointPositionWorld(i, poR_rot)
        elif label == 'poL':
            fiducials.SetNthControlPointPositionWorld(i, poL_rot)
        elif label == 'orR':
            fiducials.SetNthControlPointPositionWorld(i, orR_rot)
        elif label == 'orL':
            fiducials.SetNthControlPointPositionWorld(i, orL_rot)

    # Harden the rotation transform (makes it permanent)
    slicer.vtkSlicerTransformLogic().hardenTransform(inputVolume)

    # --- Optional translation to move nasion to origin (after hardening) ---
    moveNasionToOrigin = nasionOriginCheckbox.isChecked()
    translation_vector = numpy.array([0.0, 0.0, 0.0])
    nasion_node, nasion_idx = findNasionLandmark()

    if moveNasionToOrigin:
        if nasion_node is None:
            slicer.util.errorDisplay("Nasion landmark not found...")
        else:
            # Get current world position of nasion (after rotation)
            nasion_pos = [0,0,0]
            nasion_node.GetNthControlPointPositionWorld(nasion_idx, nasion_pos)
            translation_vector = -numpy.array(nasion_pos)
            print(f"Translation to move nasion to origin: {translation_vector} mm")

            # Create a combined transform: rotation (already hardened) + translation
            # But the rotation is already hardened, so we apply a new translation transform.
            vTranslate = vtk.vtkTransform()
            vTranslate.Translate(translation_vector)
            translationTransformNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Nasion_Translation')
            translationTransformNode.SetMatrixTransformToParent(vTranslate.GetMatrix())
            
            # Apply translation to volume AND to the nasion's fiducial node (and all others)
            inputVolume.SetAndObserveTransformNodeID(translationTransformNode.GetID())
            
            # Instead of manually moving markups, we set the same translation transform on all markups
            # This keeps them perfectly aligned with the volume.
            scene = slicer.mrmlScene
            all_markup_nodes = scene.GetNodesByClass("vtkMRMLMarkupsNode")
            all_markup_nodes.UnRegister(scene)
            for i in range(all_markup_nodes.GetNumberOfItems()):
                markup = all_markup_nodes.GetItemAsObject(i)
                markup.SetAndObserveTransformNodeID(translationTransformNode.GetID())
            
            # Harden the translation on the volume (makes it permanent)
            slicer.vtkSlicerTransformLogic().hardenTransform(inputVolume)
            
            # Now harden the translation on all markups (bake the translation into their control points)
            for i in range(all_markup_nodes.GetNumberOfItems()):
                markup = all_markup_nodes.GetItemAsObject(i)
                slicer.vtkSlicerTransformLogic().hardenTransform(markup)
            
            # Remove the temporary transform node
            slicer.mrmlScene.RemoveNode(translationTransformNode)
            translationTransformNode = None
            
            # After hardening, the nasion should be at origin. But due to floating point, ensure it.
            nasion_node.SetNthControlPointPositionWorld(nasion_idx, [0.0, 0.0, 0.0])

    # Update UI
    undoButton.enabled = True
    applyButton.enabled = False

    # Extract approximate Euler angles for info (optional)
    # Not needed for correctness.
    info_text = "4-point FHP realignment complete!\nPlane-based alignment applied."
    if moveNasionToOrigin and nasion_node:
        info_text += f"\nNasion moved to origin (Δx={translation_vector[0]:.2f}, Δy={translation_vector[1]:.2f}, Δz={translation_vector[2]:.2f})"
    slicer.util.infoDisplay(info_text)

    # Optional FHP plane (created after rotation and translation, so coordinates are final)
    reply = qt.QMessageBox.question(fhp_widget, "Create FHP Plane?",
                                    "Do you want to create a visualization plane for the new Frankfurt Horizontal Plane?",
                                    qt.QMessageBox.Yes | qt.QMessageBox.No)
    if reply == qt.QMessageBox.Yes:
        # Use the rotated landmark positions (they already include translation if applied)
        createFHPPlane(poR_rot, poL_rot, orR_rot, orL_rot)

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
