This GUI uses a 4-point approach to relign the scan and create a Frankfort Horizontal Plane.
The next snippet adds an option to make nasion the origin of the RAS coordinate system - you have to allocate the nasion from another landmark file (usually in the landmark files for any method or manually adding it, but must be called "n" or "nasion"); after the FHP realignment is hardened. 


<details>
<summary>Code for 4-point FHP realignment </summary>


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
fhp_widget.setWindowTitle("4-Point FHP Realign Tool")

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
                             "poR = right porion, poL = left porion,\norR = right orbitale, orL = left orbitale")
instructionLabel.setWordWrap(True)
panelLayout.addWidget(instructionLabel)

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

def onSelect():
    fiducialNode = inputFiducialsSelector.currentNode()
    if fiducialNode:
        labels = [fiducialNode.GetNthControlPointLabel(i) for i in range(fiducialNode.GetNumberOfControlPoints())]
        hasAllPoints = all(label in labels for label in ['poR', 'poL', 'orR', 'orL'])
        applyButton.enabled = bool(inputVolumeSelector.currentNode() and hasAllPoints)
    else:
        applyButton.enabled = False
    undoButton.enabled = bool(fhpTransformRoot)

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

def compute_fhp_transform(poR, poL, orR, orL):
    """
    Compute a rotation matrix that aligns the Frankfort Horizontal Plane to the XY plane
    and the inter‑porion line to the X axis (left‑right).
    Returns a vtkMatrix4x4 (rotation only, no translation).
    """
    pts = numpy.vstack([poR, poL, orR, orL])
    centroid = numpy.mean(pts, axis=0)
    centered = pts - centroid
    U, S, Vt = numpy.linalg.svd(centered)
    normal = Vt[2]
    if normal[2] < 0:
        normal = -normal

    lr = poR - poL
    lr = lr / numpy.linalg.norm(lr)

    anterior = numpy.cross(normal, lr)
    anterior = anterior / numpy.linalg.norm(anterior)

    normal = numpy.cross(lr, anterior)
    normal = normal / numpy.linalg.norm(normal)

    rot_matrix = vtk.vtkMatrix4x4()
    for i in range(3):
        rot_matrix.SetElement(i, 0, lr[i])
        rot_matrix.SetElement(i, 1, anterior[i])
        rot_matrix.SetElement(i, 2, normal[i])
    rot_matrix.SetElement(3, 3, 1.0)

    rot_matrix_inv = vtk.vtkMatrix4x4()
    rot_matrix_inv.DeepCopy(rot_matrix)
    rot_matrix_inv.Invert()
    return rot_matrix_inv

def onRealignButton():
    global originalTransformNode, fhpTransformRoot, originalFiducialTransform

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

    # Update UI
    undoButton.enabled = True
    applyButton.enabled = False

    slicer.util.infoDisplay("4-point FHP realignment complete!\nPlane-based alignment applied.")

    # Optional FHP plane
    reply = qt.QMessageBox.question(fhp_widget, "Create FHP Plane?",
                                    "Do you want to create a visualization plane for the new Frankfurt Horizontal Plane?",
                                    qt.QMessageBox.Yes | qt.QMessageBox.No)
    if reply == qt.QMessageBox.Yes:
        createFHPPlane(poR_rot, poL_rot, orR_rot, orL_rot)

def onUndoButton():
    global fhpTransformRoot, originalFiducialTransform
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

    # Remove our transform node
    if fhpTransformRoot:
        slicer.mrmlScene.RemoveNode(fhpTransformRoot)
        fhpTransformRoot = None

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
</details>



<details>
<summary>Code for setting nasion at origin (0,0,0)</summary>


```python
def move_nasion_to_origin():
    """
    Translate the whole scene so that the nasion landmark becomes (0,0,0) in RAS.
    Searches all MarkupsFiducial nodes for a point labelled 'nasion' or 'n' (case‑insensitive).
    Updates all scene nodes directly (no transform chains) to avoid orientation errors and deprecation warnings.
    """
    import slicer
    import vtk

    scene = slicer.mrmlScene

    # ---- 1. Find nasion landmark ----
    nasion_node = None
    nasion_idx = -1
    fiducial_nodes = scene.GetNodesByClass("vtkMRMLMarkupsFiducialNode")
    fiducial_nodes.UnRegister(scene)
    for i in range(fiducial_nodes.GetNumberOfItems()):
        node = fiducial_nodes.GetItemAsObject(i)
        for j in range(node.GetNumberOfControlPoints()):
            label = node.GetNthControlPointLabel(j).strip().lower()
            if label in ["nasion", "n"]:
                nasion_node = node
                nasion_idx = j
                break
        if nasion_node:
            break

    if nasion_node is None:
        slicer.util.errorDisplay("Nasion landmark not found.\nPlease create a fiducial point named 'nasion' or 'n' in any markup list.")
        return

    # ---- 2. Get current world position of nasion ----
    nasion_pos = [0.0, 0.0, 0.0]
    nasion_node.GetNthControlPointPositionWorld(nasion_idx, nasion_pos)
    translation = [-nasion_pos[0], -nasion_pos[1], -nasion_pos[2]]
    print(f"Moving nasion from {nasion_pos} to (0,0,0) with translation {translation}")

    # ---- Helper: apply translation to a point ----
    def trans(p):
        return [p[0] + translation[0], p[1] + translation[1], p[2] + translation[2]]

    # ---- 3. Process volumes (using a temporary transform then harden) ----
    volume_nodes = scene.GetNodesByClass("vtkMRMLScalarVolumeNode")
    volume_nodes.UnRegister(scene)
    if volume_nodes.GetNumberOfItems() > 0:
        vtk_transform = vtk.vtkTransform()
        vtk_transform.Translate(translation)
        transform_node = scene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "temp_nasion_translation")
        transform_node.SetMatrixTransformToParent(vtk_transform.GetMatrix())
        for i in range(volume_nodes.GetNumberOfItems()):
            vol = volume_nodes.GetItemAsObject(i)
            vol.SetAndObserveTransformNodeID(transform_node.GetID())
            slicer.vtkSlicerTransformLogic().hardenTransform(vol)
        scene.RemoveNode(transform_node)

    # ---- 4. Process models ----
    model_nodes = scene.GetNodesByClass("vtkMRMLModelNode")
    model_nodes.UnRegister(scene)
    if model_nodes.GetNumberOfItems() > 0:
        vtk_transform = vtk.vtkTransform()
        vtk_transform.Translate(translation)
        transform_node = scene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "temp_nasion_translation")
        transform_node.SetMatrixTransformToParent(vtk_transform.GetMatrix())
        for i in range(model_nodes.GetNumberOfItems()):
            model = model_nodes.GetItemAsObject(i)
            model.SetAndObserveTransformNodeID(transform_node.GetID())
            slicer.vtkSlicerTransformLogic().hardenTransform(model)
        scene.RemoveNode(transform_node)

    # ---- 5. Markup nodes: translate control points directly ----
    # Fiducials
    for i in range(fiducial_nodes.GetNumberOfItems()):
        node = fiducial_nodes.GetItemAsObject(i)
        for j in range(node.GetNumberOfControlPoints()):
            pos = [0.0, 0.0, 0.0]
            node.GetNthControlPointPositionWorld(j, pos)
            node.SetNthControlPointPositionWorld(j, trans(pos))
        node.SetAndObserveTransformNodeID(None)

    # Lines, curves, angles, ROIs
    other_markups = ["vtkMRMLMarkupsLineNode", "vtkMRMLMarkupsCurveNode",
                     "vtkMRMLMarkupsClosedCurveNode", "vtkMRMLMarkupsAngleNode",
                     "vtkMRMLMarkupsROINode"]
    for cls in other_markups:
        nodes = scene.GetNodesByClass(cls)
        nodes.UnRegister(scene)
        for i in range(nodes.GetNumberOfItems()):
            node = nodes.GetItemAsObject(i)
            for j in range(node.GetNumberOfControlPoints()):
                pos = [0.0, 0.0, 0.0]
                node.GetNthControlPointPositionWorld(j, pos)
                node.SetNthControlPointPositionWorld(j, trans(pos))
            node.SetAndObserveTransformNodeID(None)

    # Planes: translate origin only, leave normal untouched
    plane_nodes = scene.GetNodesByClass("vtkMRMLMarkupsPlaneNode")
    plane_nodes.UnRegister(scene)
    for i in range(plane_nodes.GetNumberOfItems()):
        plane = plane_nodes.GetItemAsObject(i)
        origin = [0.0, 0.0, 0.0]
        plane.GetOrigin(origin)
        plane.SetOrigin(trans(origin))
        plane.SetAndObserveTransformNodeID(None)

    # ---- 6. Ensure nasion is exactly at (0,0,0) ----
    nasion_node.SetNthControlPointPositionWorld(nasion_idx, [0.0, 0.0, 0.0])

    slicer.util.infoDisplay(f"Nasion moved to origin.\nTranslation applied: {translation[0]:.2f}, {translation[1]:.2f}, {translation[2]:.2f} mm")

# Run the function
move_nasion_to_origin()


```
</details>
