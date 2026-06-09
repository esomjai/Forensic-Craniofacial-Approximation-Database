This GUI uses a 4-point approach to relign the scan and create a Frankfort Horizontal Plane.

```python
import qt
import ctk
import slicer
import urllib.request
import urllib.error
import os
import vtk
import numpy
import json

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
fhp_widget.setWindowTitle("4-Point FHP Realign Tool")

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
inputFiducialsSelector.setToolTip("4 landmarks: poR, poL, orR, orL define the Frankfurt Horizontal Plane.")
formLayout.addRow("Frankfort Plane landmarks (poR, poL, orR, orL):", inputFiducialsSelector)

# --- Add the instructional label ---
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

# Add vertical spacer at the end
panelLayout.addStretch(1)

# --- Global variables to manage state ---
originalTransformNode = None
fhpTransformRoot = None
originalFiducialTransform = None

# --- Define the functions that make the buttons work ---

def onSelect():
    """Enable the apply button only if both inputs are selected AND all 4 landmarks exist."""
    fiducialNode = inputFiducialsSelector.currentNode()
    if fiducialNode:
        labels = [fiducialNode.GetNthControlPointLabel(i) for i in range(fiducialNode.GetNumberOfControlPoints())]
        hasAllPoints = all(label in labels for label in ['poR', 'poL', 'orR', 'orL'])
        applyButton.enabled = bool(inputVolumeSelector.currentNode() and hasAllPoints)
    else:
        applyButton.enabled = False
    undoButton.enabled = bool(fhpTransformRoot)

def transformLandmarks(fiducials, transformMatrix):
    """Apply a transform to all control points of a fiducial node."""
    for i in range(fiducials.GetNumberOfControlPoints()):
        pos = [0, 0, 0]
        fiducials.GetNthControlPointPositionWorld(i, pos)
        new_pos = transformMatrix.MultiplyPoint([pos[0], pos[1], pos[2], 1.0])[:3]
        fiducials.SetNthControlPointPositionWorld(i, new_pos)

def createFHPPlane(poR, poL, orR, orL):
    """
    Creates the Frankfurt Horizontal Plane as a best-fit plane through all 4 landmarks.
    The FHP is a transverse plane (horizontal) that passes through porions and orbitales.
    """
    # Collect all 4 points
    points = numpy.vstack([poR, poL, orR, orL])
    
    # Calculate the centroid (center of the 4 points)
    centroid = numpy.mean(points, axis=0)
    
    # Center the points
    centered_points = points - centroid
    
    # Perform SVD to find the best-fit plane
    # The normal vector is the singular vector with the smallest singular value
    U, S, Vt = numpy.linalg.svd(centered_points)
    normal = Vt[2]  # Third row of Vt corresponds to smallest singular value
    
    # Ensure the normal points upward (positive Z in LPS coordinate system)
    # LPS: +Z is superior (toward head)
    if normal[2] < 0:
        normal = -normal
    
    # Check if an FHP plane already exists and remove it
    existingPlane = slicer.mrmlScene.GetFirstNodeByName("FHP")
    if existingPlane:
        slicer.mrmlScene.RemoveNode(existingPlane)
        print("Removed existing FHP plane.")
    
    # Create new plane with name "FHP"
    planeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", "FHP")
    planeNode.SetOrigin(centroid)
    planeNode.SetNormal(normal)
    
    # Set plane display properties
    displayNode = planeNode.GetDisplayNode()
    displayNode.SetColor(0.31, 0.78, 0.47)  # Green
    displayNode.SetSelectedColor(0.31, 0.78, 0.47)
    displayNode.SetVisibility(True)
    
    # Make the plane larger for better visibility
    planeNode.SetSize(200, 200)  # Size in mm
    
    print(f"Created 'FHP' transverse plane")
    print(f"  Plane normal (should point superior): {normal}")
    print(f"  Plane origin (centroid of 4 points): {centroid}")
    
    return planeNode

def onRealignButton():
    """Performs the 4-point FHP realignment using yaw, roll, then pitch (balanced)."""
    global originalTransformNode, fhpTransformRoot, originalFiducialTransform
    
    inputVolume = inputVolumeSelector.currentNode()
    fiducials = inputFiducialsSelector.currentNode()
    
    # Save original transforms if not already saved
    if not originalTransformNode:
        existingTransformID = inputVolume.GetTransformNodeID()
        if existingTransformID: 
            originalTransformNode = slicer.mrmlScene.GetNodeByID(existingTransformID)
        else:
            identityMatrix = vtk.vtkMatrix4x4()
            originalTransformNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", "Original_Position_Backup")
            originalTransformNode.SetMatrixTransformToParent(identityMatrix)
        print("Saved original volume position.")
    
    # Save original fiducial transform
    originalFiducialTransform = fiducials.GetTransformNodeID()
    
    # Get landmark coordinates
    landmarks = {}
    for i in range(fiducials.GetNumberOfControlPoints()):
        label = fiducials.GetNthControlPointLabel(i)
        pos = [0,0,0]
        fiducials.GetNthControlPointPositionWorld(i, pos)
        landmarks[label] = numpy.array(pos)
    
    # Verify all 4 landmarks exist
    required = ['poR', 'poL', 'orR', 'orL']
    for req in required:
        if req not in landmarks:
            slicer.util.errorDisplay(f"Missing landmark: {req}. Please add it to the fiducial list.")
            return
    
    poR = landmarks['poR'].copy()
    poL = landmarks['poL'].copy()
    orR = landmarks['orR'].copy()
    orL = landmarks['orL'].copy()
    
    print(f"Initial landmark positions:")
    print(f"  poR: {poR}")
    print(f"  poL: {poL}")
    print(f"  orR: {orR}")
    print(f"  orL: {orL}")
    
    # --- STEP 1: Yaw rotation (align porions to LR axis) ---
    po_vector = poR - poL
    yaw_angle = -numpy.arctan2(po_vector[1], po_vector[0]) * 180 / numpy.pi
    
    vTransform1 = vtk.vtkTransform()
    vTransform1.RotateZ(yaw_angle)
    
    transform1 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Yaw')
    transform1.SetMatrixTransformToParent(vTransform1.GetMatrix())
    
    # Apply to volume and fiducials
    inputVolume.SetAndObserveTransformNodeID(transform1.GetID())
    fiducials.SetAndObserveTransformNodeID(transform1.GetID())
    
    # Get the combined transform matrix and apply to landmark coordinates
    currentMatrix = vtk.vtkMatrix4x4()
    currentMatrix.DeepCopy(transform1.GetMatrixTransformToParent())
    
    # Update landmark coordinates by applying the transform
    poR_h = [poR[0], poR[1], poR[2], 1.0]
    poL_h = [poL[0], poL[1], poL[2], 1.0]
    orR_h = [orR[0], orR[1], orR[2], 1.0]
    orL_h = [orL[0], orL[1], orL[2], 1.0]
    
    poR = numpy.array(currentMatrix.MultiplyPoint(poR_h)[:3])
    poL = numpy.array(currentMatrix.MultiplyPoint(poL_h)[:3])
    orR = numpy.array(currentMatrix.MultiplyPoint(orR_h)[:3])
    orL = numpy.array(currentMatrix.MultiplyPoint(orL_h)[:3])
    
    print(f"After Yaw (angle: {yaw_angle:.2f}°):")
    print(f"  poR: {poR}")
    print(f"  poL: {poL}")
    
    # --- STEP 2: Roll rotation (align porions in AP direction) ---
    po_vector = poR - poL
    roll_angle = numpy.arctan2(po_vector[2], po_vector[0]) * 180 / numpy.pi
    
    vTransform2 = vtk.vtkTransform()
    vTransform2.RotateY(roll_angle)
    
    transform2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Roll')
    transform2.SetMatrixTransformToParent(vTransform2.GetMatrix())
    transform1.SetAndObserveTransformNodeID(transform2.GetID())
    
    # Get the combined transform matrix
    currentMatrix = vtk.vtkMatrix4x4()
    currentMatrix.DeepCopy(transform2.GetMatrixTransformToParent())
    
    # Update landmark coordinates
    poR_h = [poR[0], poR[1], poR[2], 1.0]
    poL_h = [poL[0], poL[1], poL[2], 1.0]
    orR_h = [orR[0], orR[1], orR[2], 1.0]
    orL_h = [orL[0], orL[1], orL[2], 1.0]
    
    poR = numpy.array(currentMatrix.MultiplyPoint(poR_h)[:3])
    poL = numpy.array(currentMatrix.MultiplyPoint(poL_h)[:3])
    orR = numpy.array(currentMatrix.MultiplyPoint(orR_h)[:3])
    orL = numpy.array(currentMatrix.MultiplyPoint(orL_h)[:3])
    
    print(f"After Roll (angle: {roll_angle:.2f}°):")
    print(f"  poR: {poR}")
    print(f"  poL: {poL}")
    
    # --- STEP 3: Pitch rotation (using BOTH orbitales for balanced alignment) ---
    or_midpoint = (orR + orL) / 2.0
    po_midpoint = (poR + poL) / 2.0
    po_or_vector = or_midpoint - po_midpoint
    pitch_angle = -numpy.arctan2(po_or_vector[2], po_or_vector[1]) * 180 / numpy.pi
    
    vTransform3 = vtk.vtkTransform()
    vTransform3.RotateX(pitch_angle)
    
    transform3 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'FHP_Pitch')
    transform3.SetMatrixTransformToParent(vTransform3.GetMatrix())
    transform2.SetAndObserveTransformNodeID(transform3.GetID())
    
    # Get the final combined transform matrix
    finalMatrix = vtk.vtkMatrix4x4()
    finalMatrix.DeepCopy(transform3.GetMatrixTransformToParent())
    
    # Update landmark coordinates one more time for the final positions
    poR_h = [poR[0], poR[1], poR[2], 1.0]
    poL_h = [poL[0], poL[1], poL[2], 1.0]
    orR_h = [orR[0], orR[1], orR[2], 1.0]
    orL_h = [orL[0], orL[1], orL[2], 1.0]
    
    poR_final = numpy.array(finalMatrix.MultiplyPoint(poR_h)[:3])
    poL_final = numpy.array(finalMatrix.MultiplyPoint(poL_h)[:3])
    orR_final = numpy.array(finalMatrix.MultiplyPoint(orR_h)[:3])
    orL_final = numpy.array(finalMatrix.MultiplyPoint(orL_h)[:3])
    
    print(f"After Pitch (angle: {pitch_angle:.2f}°):")
    print(f"  poR: {poR_final}")
    print(f"  poL: {poL_final}")
    print(f"  orR: {orR_final}")
    print(f"  orL: {orL_final}")
    
    # Store the root transform for undo
    fhpTransformRoot = transform1
    
    # Now harden the transform on the volume (this makes the transform permanent)
    # But first, we need to apply the final transform to the landmarks as well
    # The landmarks currently have transform1 applied, but we need the full chain
    # Remove the transform from fiducials before hardening
    fiducials.SetAndObserveTransformNodeID(None)
    
    # Now apply the final transform to the landmark positions
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
    
    # Hardening must be done after we've updated the landmarks
    slicer.vtkSlicerTransformLogic().hardenTransform(inputVolume)
    
    # Update UI
    undoButton.enabled = True
    applyButton.enabled = False  # Can't apply again until new landmarks are placed
    
    # Calculate final midpoints for the plane (using the transformed coordinates)
    or_midpoint_final = (orR_final + orL_final) / 2.0
    po_midpoint_final = (poR_final + poL_final) / 2.0
    
    slicer.util.infoDisplay(f"4-point FHP realignment complete!\n"
                           f"Yaw: {yaw_angle:.1f}°, Roll: {roll_angle:.1f}°, Pitch: {pitch_angle:.1f}°\n"
                           "The transform has been hardened (made permanent) and landmarks have been updated.")
    
    # Optional: Create a plane visualization
    reply = qt.QMessageBox.question(fhp_widget, "Create FHP Plane?",
                                    "Do you want to create a visualization plane for the new Frankfurt Horizontal Plane?",
                                    qt.QMessageBox.Yes | qt.QMessageBox.No)
    if reply == qt.QMessageBox.Yes:
        # Create FHP plane using all 4 transformed landmarks
        createFHPPlane(poR_final, poL_final, orR_final, orL_final)  

def onUndoButton():
    """Reverts the volume to its original saved position."""
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
    
    # Revert fiducial transform
    if originalFiducialTransform:
        fiducials.SetAndObserveTransformNodeID(originalFiducialTransform)
    else:
        fiducials.SetAndObserveTransformNodeID(None)
    
    # Remove our transform chain
    if fhpTransformRoot:
        slicer.mrmlScene.RemoveNode(fhpTransformRoot)
        fhpTransformRoot = None
    
    undoButton.enabled = False
    applyButton.enabled = True
    slicer.util.infoDisplay("Realignment undone (transform removed).")

def download_github_attachment(url, destination):
    """
    Special function to download GitHub attachment files.
    GitHub attachments require following redirects and proper headers.
    """
    try:
        # Create a request with a proper User-Agent header
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Open the URL (this will follow redirects automatically)
        with urllib.request.urlopen(req, timeout=30) as response:
            # Check if we got a successful response
            if response.getcode() == 200:
                # Read the content
                content = response.read()
                
                # Write to file
                with open(destination, 'wb') as f:
                    f.write(content)
                
                return True
            else:
                print(f"Failed to download: HTTP {response.getcode()}")
                return False
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"Download error: {str(e)}")
        return False

def autoLoadLandmarks():
    """Downloads and loads the 4-point FHP landmarks from GitHub attachment."""
    # Check if already loaded
    existing = slicer.mrmlScene.GetFirstNodeByName("FHP_4Point_Landmarks")
    if existing:
        inputFiducialsSelector.setCurrentNode(existing)
        print("Landmarks already loaded in scene.")
        return
    
    # GitHub attachment URL
    url = "https://github.com/user-attachments/files/26278568/FHP4.mrk.json"
    fileName = "FHP4.mrk.json"
    tempPath = os.path.join(slicer.app.temporaryPath, fileName)
    
    # Try to download using the special function
    print("Downloading landmarks from GitHub...")
    if download_github_attachment(url, tempPath):
        try:
            # Load the markups file
            loadedNode = slicer.util.loadMarkups(tempPath)
            if loadedNode:
                loadedNode.SetName("FHP_4Point_Landmarks")
                inputFiducialsSelector.setCurrentNode(loadedNode)
                print("Successfully loaded 4-point landmarks from GitHub.")
                
                # Optional: Clean up temp file
                # os.remove(tempPath)
                return
            else:
                print("Failed to load markups from downloaded file.")
        except Exception as e:
            print(f"Error loading markups: {e}")
    else:
        print("Download failed. Please load the landmarks manually.")
        slicer.util.warningDisplay(
            "Could not auto-download landmarks from GitHub.\n\n"
            "Please load the FHP4.mrk.json file manually using:\n"
            "File > Add Data\n\n"
            "You can also place the four landmarks manually using the Markups module."
        )

# --- Connect buttons to functions and show the window ---
applyButton.connect('clicked(bool)', onRealignButton)
undoButton.connect('clicked(bool)', onUndoButton)
inputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)
inputFiducialsSelector.connect("currentNodeChanged(vtkMRMLNode*)", onSelect)

fhp_widget.show()
autoLoadLandmarks()
onSelect()
print("4-Point FHP Realign panel is now showing. Ready for use.")

```
