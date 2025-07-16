# The Purkait and Singh (2024) method

### This document contains instructions for: 

> [!WARNING]
> The sample CT (CBCT PreDentalSurgery) used in the screenshots of this guide was taken pre-surgery for an underbite, the error rate shown in the guide is probably not representative if implemented on a population without pathologies.


### Landmarks in this guide (for prediction of soft tissues)
[PS_hard_tissue.mrk.json](https://github.com/user-attachments/files/21217369/PS_hard_tissue.mrk.json)

> [!IMPORTANT]  
The original paper uses a "backward" projected hard sn described as: 
_"(...) measured from the soft ‘sn’ point to the maxillary bone (bony sn) parallel to the FH plane"_
This in not feasible to use if only hard tissue is available to reconstruct - therefore the closest hard tissue landmark **subspinale or ss** defined by  Howells (1937)[^4]; Howells (1974)[^5]; Caple & Stephan (2016)[^5]Caple & Stephan (2016)[^3] was implemented.
The instructions and codes for the full recreation of the study will revert back to the original placement of this landmark, as described by Purkait and Singh (2024)[^1] via a guiding line. 


| Position in code | Position in file | Name in file   | Landmark name | Definition                                                                                                     | Defined by     |
|------------------|-----------------|---------------|---------------|----------------------------------------------------------------------------------------------------------------|----------------|
| 0                | 1               | n             | nasion             | midpoint of the frontonasal suture on the midsagittal plane                                                    | Purkait & Singh, 2024[^2]  |
| 1                | 2               | rhi           | rhinion           | the point located on the most inferior end of the internasal suture                                            |  Martin (1928)[^6];  Knussman (1988)[^7]; Caple & Stephan (2016)[^3]  |
| 2                | 3               | ss            | subspinale            | CHANGED! The deepest point seen in the profile view below the anterior nasal spine (orthodontic point A)       |  Howells (1937)[^4]; Howells (1974)[^5]; Caple & Stephan (2016)[^3] |
| 3                | 4               | ANS           | anterior nasal spine or acanthion           | Most anterior tip of the anterior nasal spine                                                                  | Howells (1937)[^4]; Howells (1974)[^5]; Caple & Stephan (2016)[^3]  |
| 4                | 5               | A (PA_R)      | A (PA_R)      | most lateral point on the right of the bony pyriform aperture                                                  | Purkait & Singh, 2024[^2]  |
| 5                | 6             | B (PA_L)      | B (PA_L)      | most lateral point on the left of the bony pyriform aperture                                                   | Purkait & Singh, 2024[^2]  |
| 6                | 7              | C (PAB_R)     | C (PAB_R)     | lowest point on the right base of the bony pyriform aperture                                                   | Purkait & Singh, 2024[^2]  |
| 7                | 8              | D (PAB_L)     | D (PAB_L)     | lowest point on the left base of the bony pyriform aperture                                                    | Purkait & Singh, 2024[^2] |

### Additional soft tissue landmarks in this guide (for replicating the full method; not necessary for ONLY estimation)

[PS_soft_tissue.mrk.json](https://github.com/user-attachments/files/21217705/PS_soft_tissue.mrk.json)

| Position in code | Position in file | Name in file   | Landmark name | Definition                | Defined by    |
|------------------|-----------------|---------------|---------------|--------------------------------------|--------------|
| 0                | 1               | n'            | n'            | Point directly anterior to the nasofrontal suture, in the midline, overlying n            | Kolar,  (1997)[^8]; Caple & Stephan (2016)[^5] |
| 1                | 2               | rhi'          | rhi'          | Point overlying rhi, at the end of the internasal suture where bone ends and cartilage begins | Stephan, 2008[^9]; Caple & Stephan (2016)[^3]|
| 2                | 3               | sn'           | sn'           | Median point at the junction between the lower border of the nasal septum and the philtrum area | Caple & Stephan (2016)[^3]|
| 3                | 4               | nt            | nasal tip            | lowest point on the lower margin of the nasal tip in the midsagittal plane                | Purkait & Singh, 2024[^2]|
| 4                | 5               | X1(alL)       | left nasal ala       | The most lateral point on the left nasal ala                                              | Purkait & Singh, 2024[^2]|
| 5                | 6               | X2(alR)       | right nasal ala      | The most lateral point on the right nasal ala                                             | Purkait & Singh, 2024[^2]|
| 6               | 7               | Y1(nbL)       | left nasal base       | the base of the left attachment of nasal wings on the upper lip                           | Purkait & Singh, 2024[^2] |
| 7                | 8               | Y2(nbR)       | right nasal base       | the base of the right attachment of nasal wings on the upper lip                          | Purkait & Singh, 2024[^2]|
| 8                | 9              | prn           | pronasale           | The most anteriorly protruded point of the apex nasi                                      | Farkas (1994)[^10]; Caple & Stephan (2016)[^3]|


### Illustration of the method


> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

- [ ] Re-aligned the scene in the FHP
- [ ] Created a 4-point FHP 
- [ ] Allocated all hard tissue landmarks

### Creating the midsagittal plane (MSP)

In this case, the midsagittal plane was defined as a plane best fitting the **nasion, rhinion, subspinale and anterior nasal spine**

<details>
<summary> Code for MSP </summary>

``` python
import numpy as np

# Get your landmark node (update the name if needed)
lmrks = slicer.util.getNode('PS_hard_tissue')

# Indices you want to use for the best fit plane
indices = [0, 1, 2, 3]

# Get the coordinates of those points (in world coordinates)
points = []
for i in indices:
    pos = np.array(lmrks.GetNthControlPointPositionWorld(i))
    points.append(pos)
points = np.array(points)

# Compute the centroid
centroid = np.mean(points, axis=0)

# Subtract centroid from points
pts_centered = points - centroid

# Singular Value Decomposition (SVD) for best-fit plane
U, S, Vt = np.linalg.svd(pts_centered)
normal = Vt[2, :]  # The normal of the best-fit plane is the last singular vector

# Create the MSP plane
mspPlaneNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'MSP')
mspPlaneNode.SetOriginWorld(centroid)
mspPlaneNode.SetNormalWorld(normal)

print("Best-fit 'MSP' plane created through selected landmarks.")

```


</details>

Expected view after code implementation, showing both the FHP and MSP: 


<img width="3365" height="1559" alt="Picture1" src="https://github.com/user-attachments/assets/a1c1cb8b-dac7-475b-8643-4f1152096c8b" />



### Hard tissue measurements and guides

In the following code, we recreate all the hard tissue measurements mentioned in the paper regardless of their correlation and participation in the regression equations; and additionally, establish some lines that are not true measurements but provide navigation for following lines of code (these will be annotated with a yellow dot in the table below). 
After pasting the code, a pop-up window will as for a facial soft tissue thickness to provide for predicting the sn' based on this measurement - this is in agreement with the original instructions by Purkait and Singh (2024)[^1] and the default measurement is set to 13.5 mm (as described by Hona et al. (2023)[^11] in [Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC10861615/table/Tab3/v))



<details>
<summary> Hard tissue measurements </summary>


``` python
import numpy as np
import slicer
import qt

print("Starting line creation and customization...")

# ---- STEP 1: Get Plane Data (handles both plane nodes or fiducial nodes) ----
mspNode = slicer.util.getNode('MSP')
fhpNode = slicer.util.getNode('FHP')

# Check what type of nodes we're dealing with
msp_is_plane = 'Plane' in mspNode.GetClassName()
fhp_is_plane = 'Plane' in fhpNode.GetClassName()

print(f"MSP is a plane node: {msp_is_plane}")
print(f"FHP is a plane node: {fhp_is_plane}")

# Function to get normal from 3 points
def plane_normal(p1, p2, p3):
    v1 = np.array(p2) - np.array(p1)
    v2 = np.array(p3) - np.array(p1)
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)

# Get normals for each plane
if msp_is_plane:
    msp_origin = [0, 0, 0]
    msp_normal = [0, 0, 0]
    mspNode.GetOrigin(msp_origin)
    mspNode.GetNormal(msp_normal)
    msp_origin = np.array(msp_origin)
    msp_normal = np.array(msp_normal)
else:
    # Assuming it's a fiducial node
    msp_pts = []
    for i in range(3):  # Get first 3 points
        pt = [0, 0, 0]
        mspNode.GetNthControlPointPosition(i, pt)
        msp_pts.append(pt)
    msp_origin = np.array(msp_pts[0])
    msp_normal = plane_normal(*msp_pts)

if fhp_is_plane:
    fhp_origin = [0, 0, 0]
    fhp_normal = [0, 0, 0]
    fhpNode.GetOrigin(fhp_origin)
    fhpNode.GetNormal(fhp_normal)
    fhp_origin = np.array(fhp_origin)
    fhp_normal = np.array(fhp_normal)
else:
    # Assuming it's a fiducial node
    fhp_pts = []
    for i in range(3):  # Get first 3 points
        pt = [0, 0, 0]
        fhpNode.GetNthControlPointPosition(i, pt)
        fhp_pts.append(pt)
    fhp_origin = np.array(fhp_pts[0])
    fhp_normal = plane_normal(*fhp_pts)

print("Got plane data successfully")

# ---- STEP 2: Calculate intersection line (FHP guide) ----
line_direction = np.cross(msp_normal, fhp_normal)
line_direction /= np.linalg.norm(line_direction)
point_on_line = msp_origin  # Use MSP origin as a point on the line

# Create start and end points for the FHP guide line
length = 70.0  # Length of the line in mm
half_vec = 0.5 * length * line_direction
fhp_start = point_on_line - half_vec
fhp_end = point_on_line + half_vec

# Create the FHP guide line
fhpGuideNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'FHP guide')
fhpGuideNode.AddControlPoint(fhp_start.tolist())
fhpGuideNode.AddControlPoint(fhp_end.tolist())
print("FHP guide line created")

# ---- STEP 3: Create the three parallel guide lines through landmarks ----
hardTissueNode = slicer.util.getNode('PS_hard_tissue')
guide_names = ['st n guide', 'st rhi guide', 'st sn guide']

for i, name in enumerate(guide_names):
    landmark_pos = [0, 0, 0]
    hardTissueNode.GetNthControlPointPosition(i, landmark_pos)
    landmark_pos = np.array(landmark_pos)
    
    start = landmark_pos - half_vec
    end = landmark_pos + half_vec
    
    lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    lineNode.AddControlPoint(start.tolist())
    lineNode.AddControlPoint(end.tolist())
    print(f"{name} created!")

# ---- NEW CODE: Create pred_FSTT_sn and sn' prediction ----
# First, create a new fiducial node to store predicted soft tissue points
pred_FSTT_sn = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pred_FSTT_sn')
print("Created pred_FSTT_sn node")

# Create a popup dialog for user input of soft tissue thickness
thickness_dialog = qt.QInputDialog()
thickness_dialog.setWindowTitle("Soft Tissue Thickness Input")
thickness_dialog.setLabelText("Enter facial soft tissue thickness (mm) for sn': (default is set to 13.5 mm based on Hona et al. 2024 (https://rdcu.be/ewjor)")
thickness_dialog.setDoubleValue(13.50)  # Default value of 13.5 mm as requested
thickness_dialog.setDoubleDecimals(2)   # Allow 2 decimal places
thickness_dialog.setDoubleRange(0.01, 30.00)  # Set reasonable limits
thickness_dialog.setDoubleStep(0.1)     # Increment by 0.1
thickness_dialog.setMinimumWidth(400)  # Make the dialog wider to show the full reference

# Show dialog and get user input
if thickness_dialog.exec_():
    sn_thickness = thickness_dialog.doubleValue()
    print(f"User entered FSTT for sn': {sn_thickness:.2f} mm")
else:
    sn_thickness = 13.50  # Default if user cancels
    print(f"Using default FSTT for sn': {sn_thickness:.2f} mm")

# Get the st sn guide line and its direction
st_sn_guide_node = slicer.util.getNode('st sn guide')
sn_guide_start = [0, 0, 0]
sn_guide_end = [0, 0, 0]
st_sn_guide_node.GetNthControlPointPosition(0, sn_guide_start)
st_sn_guide_node.GetNthControlPointPosition(1, sn_guide_end)

# Convert to numpy arrays for calculations
sn_guide_start = np.array(sn_guide_start)
sn_guide_end = np.array(sn_guide_end)

# Calculate unit vector along the guide line
guide_vec = sn_guide_end - sn_guide_start
guide_unit_vec = guide_vec / np.linalg.norm(guide_vec)

# Get hard tissue ss point (index 2 based on your original code)
ss_point = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(2, ss_point)  # Index 2 is 'ss' based on STEP 3
ss_point = np.array(ss_point)

# As requested: anterior direction is from point 2 to point 1 (end to start)
guide_unit_vec = -guide_unit_vec
print("Using st sn guide-2 to st sn guide-1 as anterior direction")

# Calculate the predicted sn' position by moving along guide line by thickness amount
pred_sn_position = ss_point + guide_unit_vec * sn_thickness
print(f"Predicted sn' position: {pred_sn_position.tolist()}")

# FIXED LINE: Use pred_FSTT_sn instead of pred_soft_tissue
pred_FSTT_sn.AddControlPoint(pred_sn_position.tolist(), "sn'_FSTT")
print("Added predicted sn' point to pred_FSTT_sn")

# Create the line connecting n to predicted sn'
n_point = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(0, n_point)  # Index 0 is 'n'

# Create the line connecting n to predicted sn'
n_to_sn_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'n to sn FSTT')
n_to_sn_node.AddControlPoint(n_point)
n_to_sn_node.AddControlPoint(pred_sn_position.tolist())
print("Created 'n to sn FSTT' line")

# Setup display properties for the pred_FSTT_sn node
displayNode = pred_FSTT_sn.GetDisplayNode()
if displayNode:
    displayNode.SetColor(0.0, 0.8, 0.0)  # Green color
    displayNode.SetSelectedColor(1.0, 0.0, 0.0)  # Red when selected
    displayNode.SetGlyphScale(1.8)  # Match your other points
    displayNode.SetTextScale(3.0)  # Readable text
    displayNode.SetGlyphType(1)  # Standard sphere glyph
    displayNode.SetSliceProjection(True)  # Show in slice views

# ---- STEP 4: Create additional lines (AB, CD, baseline) ----
# AB: connects points 4 and 5
ab_start = [0, 0, 0]
ab_end = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(4, ab_start)
hardTissueNode.GetNthControlPointPosition(5, ab_end)

abNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'AB')
abNode.AddControlPoint(ab_start)
abNode.AddControlPoint(ab_end)
print("AB line created!")

# CD: connects points 6 and 7
cd_start = [0, 0, 0]
cd_end = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(6, cd_start)
hardTissueNode.GetNthControlPointPosition(7, cd_end)

cdNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'CD')
cdNode.AddControlPoint(cd_start)
cdNode.AddControlPoint(cd_end)
print("CD line created!")

# baseline: connects points 0 and 3
baseline_start = [0, 0, 0]
baseline_end = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(0, baseline_start)
hardTissueNode.GetNthControlPointPosition(3, baseline_end)

baselineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'baseline')
baselineNode.AddControlPoint(baseline_start)
baselineNode.AddControlPoint(baseline_end)
print("baseline created!")

# ---- STEP 5: NEW LINE - "n to rhi" connecting points 0 and 1 ----
n_to_rhi_start = [0, 0, 0]
n_to_rhi_end = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(0, n_to_rhi_start)
hardTissueNode.GetNthControlPointPosition(1, n_to_rhi_end)

nToRhiNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'n to rhi')
nToRhiNode.AddControlPoint(n_to_rhi_start)
nToRhiNode.AddControlPoint(n_to_rhi_end)
print("n to rhi line created!")

# ---- STEP 6: NEW LINE - "rhi to baseline" ----
# Get point 1 (RHI)
rhi_point = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(1, rhi_point)
rhi_point = np.array(rhi_point)

# Get baseline endpoints (we already have them from above)
baseline_start = np.array(baseline_start)
baseline_end = np.array(baseline_end)

# Calculate the closest point on the baseline to RHI
# Vector from start of line to point
v = rhi_point - baseline_start
# Vector representing the line
line_vec = baseline_end - baseline_start
# Length of the line
line_length = np.linalg.norm(line_vec)
# Unit vector along the line
line_unit_vec = line_vec / line_length

# Projection of v onto the line
proj_length = np.dot(v, line_unit_vec)
# Closest point on the line
closest_point = baseline_start + proj_length * line_unit_vec

# Create the rhi to baseline line
rhiToBaselineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'rhi to baseline')
rhiToBaselineNode.AddControlPoint(rhi_point.tolist())
rhiToBaselineNode.AddControlPoint(closest_point.tolist())
print("rhi to baseline line created!")

# Calculate distance for information
distance = np.linalg.norm(rhi_point - closest_point)
print(f"Distance from RHI to baseline: {distance:.2f} mm")

# ---- STEP 7: Customize line appearance for all lines ----
# List all line names
line_names = [
    "FHP guide", 
    "st n guide", 
    "st rhi guide", 
    "st sn guide",
    "AB",
    "CD",
    "baseline",
    "n to rhi",
    "rhi to baseline",
    "n to sn FSTT"
]

# Colors for when lines are SELECTED (RGB format from 0-1)
selected_colors = {
    "FHP guide": [1.0, 0.0, 0.0],      # Red
    "st n guide": [0.0, 1.0, 0.0],     # Green
    "st rhi guide": [0.0, 0.0, 1.0],   # Blue
    "st sn guide": [1.0, 1.0, 0.0],    # Yellow
    "AB": [1.0, 0.0, 1.0],             # Magenta
    "CD": [0.0, 1.0, 1.0],             # Cyan
    "baseline": [1.0, 0.5, 0.0],       # Orange
    "n to rhi": [0.5, 0.0, 0.5],       # Purple
    "rhi to baseline": [0.7, 0.3, 0.3], # Brick red
    "n to sn FSTT": [0.5, 0.5, 0.0]    # Olive
}

# All lines will be white when unselected
unselected_color = [1.0, 1.0, 1.0]  # White

# Customize each line with YOUR settings
for line_name in line_names:
    try:
        # Get the line node
        lineNode = slicer.util.getNode(line_name)
        
        # Get its display node
        displayNode = lineNode.GetDisplayNode()
        
        # Set unselected color to white
        displayNode.SetColor(*unselected_color)
        
        # Set selected color (from our color dictionary)
        displayNode.SetSelectedColor(*selected_colors.get(line_name, [0.5, 0.5, 0.5]))
        
        # Set glyph size to 1.8 as you requested
        displayNode.SetGlyphScale(1.8)
        
        # Set line thickness to 0.25 as you requested
        displayNode.SetLineThickness(0.25)
        
        print(f"✓ Customized {line_name}")
        
    except Exception as e:
        print(f"× Could not customize {line_name}: {e}")

print("ALL LINES CREATED AND CUSTOMIZED SUCCESSFULLY!")
```


</details>

Expected view after code implementation: 

<img width="746" height="788" alt="image" src="https://github.com/user-attachments/assets/0f912a6d-6911-4041-9110-ddb4aec07e5a" />




| Line name        | name in paper | Definition                                                                                     | Colour                         |
|------------------|--------------|-----------------------------------------------------------------------------------------------|--------------------------------|
|🟡 FHP guide        |     N/A         | line where the MSP and FHP planes intersect (where FHP is perpendicular to MSP by definition)  | <span style="color:Red">Red</span> |
| 🟡st n guide       |      N/A        | parallell line to the FHP guide bisecting the hard tissue nasion (for FSTT for n')            | <span style="color:Green">Green</span> |
| 🟡st rhi guide     |         N/A      | parallell line to the FHP guide bisecting the hard tissue rhinion (for FSTT for rhi')         | <span style="color:Blue">Blue</span> |
| 🟡st sn guide      |    N/A           | parallell line to the FHP guide bisecting the hard tissue ss (for FSTT for sn)                | <span style="color:Yellow">Yellow</span> |
| sn'_FSTT (landmark!)              |    sn          | The position of   soft tissue ‘sn’ was determined by adding the STT at ‘bony sn'         |  |
| n to sn FSTT             |   bony n to sn          | line between the hard tissue nasion and the predicted sn' (via FSTT)        | <span style="color:Olive">Olive</span> |
| AB               |    same          | line connecting A and B - the most lateral points of the bony piriform aperture               | <span style="color:Magenta">Magenta</span> |
| CD               |        same      | line connecting C and D - the lowest points of the bony piriform aperture                     | <span style="color:Cyan">Cyan</span> |
| baseline         |    bony n-ans          | line connecting the hard tissue nasion  ‘n’ and the tip of ANS (ss)                           | <span style="color:Orange">Orange</span> |
| n to rhi         |   bony n-rhi            | line connecting the hard tissue nasion  ‘n’ and the rhinion                                   | <span style="color:Purple">Purple</span> |
| rhi to baseline  |   bony rhi ⟂ baseline            | The shortest perpendicular distance between the rhinion and the baseline (n-ANS)              | <span style="color:#B22222">Brick Red</span> |


## Predicting the soft tissue landmarks

The theory behind both of the codes offered is the same. They define the soft tissue measurements as a line perpendicular to the bone/skin surface, parallel to the FHP, therefore the code project lines of an arbitrary length (70 mm) from the hard tissue landmark to gauge an approximate position of the soft tissue landmarks along the planes (knowing their positions relative to the FHP and MSP, but not the distance from the hard tissue landmark yet) - hence the role of the lines ending with "guide" in this step. 

We will consider distances defined by the statistically significant equations intersecting these guide lines for predicting the **subnasale** (different approach) and **pronasale**. This is where we run into an issue with the **nt** soft tissue prediction - we could proceed with a predicted soft nasion, based on an FSTT value, but there is no "line" guiding the position of this; therefore only a radius closest to an arbitrary line can be stablished which is not justified by any anatomical or geometric knowledge. Therefore, the prediction of this will be excluded. 

| Predicted Distance | Regression Equation | Biological Sex | Note
|--------------------|---------------------|----------------|---------|
| bony n-sn | 4.385 + 0.988 × (baseline) | male |
| soft n-nt | 31.76 + 1.009 × (n to rhi) | male | excluded (see above)
| prn baseline | 19.544 + 0.299 × (rhi to baseline) | male | 
| alL-alR | 25.256 + 0.55 × (AB) | male | not relevant for prediction from hard tissue |
| nbL-nbR | 33.433 + 0.362 × (CD) | male |  not relevant for prediction from hard tissue |
| bony n-sn | 7.673 + 0.909 × (baseline) | female |
| soft n-nt | 33.23 + 0.768 × (n to rhi) | female | excluded (see above) |
| prn baseline | 15.056 + 0.622 × (rhi to baseline) | female |  

Left with two equations for each biological sex and the distances they provide, we will draw two circles each (with an imaginary pair of compassess). 

- One arm of the compass is placed at the hard tissue **nasion**, opened to the distance given by the equation for **bony n- sn** and a circle is drawn (_pred_sn_circle_{sex}_). In theory, it can have two intersection points with the line **st sn guide**, but only the more anterior makes sense anatomically, so that one is chosen by the script. We now created the predicted sn as defined by the regression (as opposed to the previous method with a manual distance of a soft tissue thickness measurement regardless of sex, stored in _pred_FSTT_sn_!)


- The equations featuring the baseline calculate the perpendicular distance between the **baseline** and the **pronasale**. Because Fig. 1 in Purkait & Singh, 2024[^2] shows a line starting from the ANS, perpendicular to the baseline connecting to the pronasale, we create the ANS perpendicular line. The "origin" from where we can apply the distance estimated by the equation will be where the baseline intersects the ANS perpendicular line, anteriorly. This is how we get the **pred_prn**. 

<details>
<summary> GUI for prediction </summary>

``` python

import numpy as np
import slicer
import math
import qt

class NasalPredictionWidget(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()
        # Store the regression coefficients for easy access
        self.regression_coefficients = {
            'male': {
                'bony_n_sn': (4.385, 0.988),  # (intercept, coefficient)
                'prn_baseline': (19.544, 0.299)
            },
            'female': {
                'bony_n_sn': (7.673, 0.909),
                'prn_baseline': (15.056, 0.622)
            }
        }
        
    def setup_ui(self):
        # Create the main layout
        layout = qt.QVBoxLayout(self)
        
        # Add title
        title_label = qt.QLabel("<h2>Nasal Prediction Tool</h2>")
        title_label.alignment = qt.Qt.AlignCenter
        layout.addWidget(title_label)
        
        # Create a form layout for options
        form_layout = qt.QFormLayout()
        
        # Biological sex selection
        self.sex_combo = qt.QComboBox()
        self.sex_combo.addItems(["Female", "Male"])
        form_layout.addRow("Biological Sex:", self.sex_combo)
        
        # Create checkbox for showing circles
        self.show_circles_checkbox = qt.QCheckBox()
        self.show_circles_checkbox.checked = True
        form_layout.addRow("Show Circle Visualization:", self.show_circles_checkbox)
        
        # Create checkbox for showing lines
        self.show_lines_checkbox = qt.QCheckBox()
        self.show_lines_checkbox.checked = True
        form_layout.addRow("Show Line Visualization:", self.show_lines_checkbox)
        
        # Add the form to the main layout
        layout.addLayout(form_layout)
        
        # Add some information text
        info_text = """
        <b>Required Input Nodes:</b>
        <ul>
          <li>PS_hard_tissue</li>
          <li>baseline</li>
          <li>rhi to baseline</li>
          <li>st sn guide</li>
          <li>MSP</li>
        </ul>
        <br>
        <b>Points that will be created:</b>
        <ul>
          <li>pred_sn_[sex] - Predicted subnasale point</li>
          <li>pred_prn_[sex] - Predicted pronasale point</li>
        </ul>
        <br>
        <b>You can run both male and female predictions</b> to compare them!
        """
        
        info_label = qt.QLabel(info_text)
        layout.addWidget(info_label)
        
        # Add Run button
        self.run_button = qt.QPushButton("Run Prediction")
        self.run_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(self.run_button)
        
        # Add status label
        self.status_label = qt.QLabel("Ready to run")
        self.status_label.setStyleSheet("color: blue;")
        layout.addWidget(self.status_label)
        
        # Set the window properties
        self.setWindowTitle("Nasal Prediction Tool")
        self.resize(400, 420)
    
    def connect_signals(self):
        self.run_button.clicked.connect(self.run_prediction)
    
    def run_prediction(self):
        self.status_label.setText("Running prediction...")
        self.status_label.setStyleSheet("color: blue;")
        slicer.app.processEvents()
        
        try:
            # Get the selected sex
            selected_sex = "male" if self.sex_combo.currentText == "Male" else "female"
            show_circles = self.show_circles_checkbox.checked
            show_lines = self.show_lines_checkbox.checked
            
            # Run the prediction with the selected options
            self.create_nasal_prediction(
                selected_sex, 
                show_circles, 
                show_lines
            )
            
            self.status_label.setText(f"✅ {selected_sex.capitalize()} prediction completed successfully!")
            self.status_label.setStyleSheet("color: green;")
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            
            # Show a friendly error message
            error_box = qt.QMessageBox()
            error_box.setIcon(qt.QMessageBox.Critical)
            error_box.setText("Error during prediction")
            error_box.setInformativeText(str(e))
            error_box.setDetailedText("Check that you have all required nodes:\n" + 
                                     "- PS_hard_tissue\n" +
                                     "- baseline\n" +
                                     "- rhi to baseline\n" +
                                     "- st sn guide\n" +
                                     "- MSP")
            error_box.setWindowTitle("Prediction Error")
            error_box.exec_()
    
    # Main function to create the nasal prediction points
    def create_nasal_prediction(self, sex, show_circles, show_lines):
        # Get the regression coefficients for the selected sex
        coeffs = self.regression_coefficients[sex]
        
        # Output what we're doing
        print(f"Creating nasal prediction points for {sex}...")
        if show_circles:
            print("Circle visualization is enabled")
        if show_lines:
            print("Line visualization is enabled")
        
        # Get nodes and create pred_soft_tissue_[sex] if needed
        try:
            # Use standard name "PS_hard_tissue"
            hardTissueNode = slicer.util.getNode('PS_hard_tissue')
            baselineNode = slicer.util.getNode('baseline')
            rhiToBaselineNode = slicer.util.getNode('rhi to baseline')
            stSnGuideNode = slicer.util.getNode('st sn guide')
            mspNode = slicer.util.getNode('MSP')
            
            # Use sex-specific node name
            pred_node_name = f'pred_soft_tissue_{sex}'
            
            try:
                pred_soft_tissue_node = slicer.util.getNode(pred_node_name)
                # Clear existing points
                while pred_soft_tissue_node.GetNumberOfControlPoints() > 0:
                    pred_soft_tissue_node.RemoveNthControlPoint(0)
            except slicer.util.MRMLNodeNotFoundException:
                pred_soft_tissue_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', pred_node_name)
                print(f"Created new '{pred_node_name}' markup node.")
            print("Found all required nodes")
        except Exception as e:
            print(f"ERROR: Could not find required nodes: {e}")
            raise

        # MSP orientation
        msp_normal = [0, 0, 0]
        if 'Plane' in mspNode.GetClassName():
            mspNode.GetNormal(msp_normal)
            msp_normal = np.array(msp_normal)
        else:
            if mspNode.GetNumberOfControlPoints() >= 3:
                p1 = [0, 0, 0]
                p2 = [0, 0, 0]
                p3 = [0, 0, 0]
                mspNode.GetNthControlPointPosition(0, p1)
                mspNode.GetNthControlPointPosition(1, p2)
                mspNode.GetNthControlPointPosition(2, p3)
                v1 = np.array(p2) - np.array(p1)
                v2 = np.array(p3) - np.array(p1)
                msp_normal = np.cross(v1, v2)
                msp_normal = msp_normal / np.linalg.norm(msp_normal)
            else:
                raise ValueError("MSP doesn't have enough points")

        # MSP basis vectors
        if abs(np.dot(msp_normal, [0, 1, 0])) < 0.9:
            temp_vec = np.array([0, 1, 0])
        else:
            temp_vec = np.array([0, 0, 1])
        msp_basis1 = np.cross(msp_normal, temp_vec)
        msp_basis1 = msp_basis1 / np.linalg.norm(msp_basis1)
        msp_basis2 = np.cross(msp_normal, msp_basis1)
        msp_basis2 = msp_basis2 / np.linalg.norm(msp_basis2)

        # Find ANS point
        ans_found = False
        for i in range(hardTissueNode.GetNumberOfControlPoints()):
            label = hardTissueNode.GetNthControlPointLabel(i)
            if "ANS" in label:
                ans_index = i
                ans_found = True
                break
        if not ans_found:
            ans_index = 3
        ans_point = self.get_point(hardTissueNode, ans_index)

        # Baseline direction and perpendicular
        baseline_start = [0, 0, 0]
        baseline_end = [0, 0, 0]
        baselineNode.GetNthControlPointPosition(0, baseline_start)
        baselineNode.GetNthControlPointPosition(1, baseline_end)
        baseline_start = np.array(baseline_start)
        baseline_end = np.array(baseline_end)
        baseline_vec = baseline_end - baseline_start
        baseline_unit = baseline_vec / np.linalg.norm(baseline_vec)
        perp_vec = np.cross(baseline_unit, msp_normal)
        perp_vec = perp_vec / np.linalg.norm(perp_vec)
        if perp_vec[1] < 0:
            perp_vec = -perp_vec
            
        # Create sex-specific perpendicular line name
        if show_lines:
            ans_perp_length = 60
            ans_perp_start = ans_point - (ans_perp_length/2) * perp_vec
            ans_perp_end = ans_point + (ans_perp_length/2) * perp_vec
            self.create_line(
                ans_perp_start, 
                ans_perp_end, 
                f"ANS perpendicular_{sex}", 
                [0.0, 0.8, 0.8], 
                [0.0, 1.0, 1.0]
            )

        # pred_sn
        baseline_length = self.get_line_length(baselineNode)
        n_point = self.get_point(hardTissueNode, 0)
        
        # Get the appropriate coefficients and calculate the distance
        intercept, coeff = coeffs['bony_n_sn']
        pred_sn_distance = intercept + coeff * baseline_length
        print(f"Using {sex} equation for pred_sn: {intercept} + {coeff} * {baseline_length} = {pred_sn_distance}")
        
        sn_guide_start = [0, 0, 0]
        sn_guide_end = [0, 0, 0]
        stSnGuideNode.GetNthControlPointPosition(0, sn_guide_start)
        stSnGuideNode.GetNthControlPointPosition(1, sn_guide_end)
        sn_guide_start = np.array(sn_guide_start)
        sn_guide_end = np.array(sn_guide_end)
        
        # Draw pred_sn circle if enabled with sex-specific name
        if show_circles:
            self.draw_circle(
                n_point, 
                pred_sn_distance, 
                msp_basis1, 
                msp_basis2, 
                f"pred_sn_circle_{sex}"
            )
            
        pred_sn_point, error = self.find_circle_line_intersection_in_msp(
            n_point, 
            pred_sn_distance, 
            sn_guide_start, 
            sn_guide_end,
            f"pred_sn_{sex}"
        )
        if error:
            raise ValueError(f"pred_sn calculation failed with error: {error}")
            
        # Use sex-specific line name
        if show_lines:
            self.create_line(
                n_point, 
                pred_sn_point, 
                f"n to pred_sn_{sex}", 
                [0.8, 0.8, 0.0], 
                [1.0, 0.7, 0.0]
            )
            
        # Add point with sex-specific label
        pred_soft_tissue_node.AddControlPoint(pred_sn_point.tolist(), f"pred_sn_{sex}")
        pred_soft_tissue_node.SetNthControlPointDescription(0, f"Predicted subnasale point ({sex})")

        # pred_prn
        rhi_to_baseline_length = self.get_line_length(rhiToBaselineNode)
        
        # Get the appropriate coefficients and calculate the distance
        intercept, coeff = coeffs['prn_baseline']
        pred_prn_distance = intercept + coeff * rhi_to_baseline_length
        print(f"Using {sex} equation for pred_prn: {intercept} + {coeff} * {rhi_to_baseline_length} = {pred_prn_distance}")
        
        pred_prn_point = ans_point + pred_prn_distance * perp_vec
        
        # Use sex-specific line name
        if show_lines:
            self.create_line(
                ans_point, 
                pred_prn_point, 
                f"ANS to pred_prn_{sex}", 
                [0.8, 0.8, 0.0], 
                [1.0, 0.7, 0.0]
            )
            
        # Add point with sex-specific label
        pred_soft_tissue_node.AddControlPoint(pred_prn_point.tolist(), f"pred_prn_{sex}")
        pred_soft_tissue_node.SetNthControlPointDescription(1, f"Predicted pronasale point ({sex})")

        # Create a line connecting the two prediction points with sex-specific name
        if show_lines:
            self.create_line(
                pred_prn_point, 
                pred_sn_point, 
                f"pred_prn to pred_sn_{sex}", 
                [0.8, 0.0, 0.8], 
                [1.0, 0.0, 1.0]
            )

        # Set different colors based on sex
        displayNode = pred_soft_tissue_node.GetDisplayNode()
        if displayNode:
            if sex == "male":
                # Blue color for male points
                displayNode.SetColor(0.0, 0.0, 0.8)
                displayNode.SetSelectedColor(0.0, 0.0, 1.0)
            else:
                # Green color for female points
                displayNode.SetColor(0.0, 0.8, 0.0)
                displayNode.SetSelectedColor(0.0, 1.0, 0.0)
                
            displayNode.SetGlyphScale(1.8)
            displayNode.SetTextScale(3.0)
            displayNode.SetGlyphType(1)
            displayNode.SetSliceProjection(True)

        print(f"\n✅ DONE! Created nasal prediction points for {sex}.")

    # Helper functions
    def get_point(self, node, index):
        point = [0, 0, 0]
        node.GetNthControlPointPosition(index, point)
        return np.array(point)

    def get_line_length(self, node):
        start = [0, 0, 0]
        end = [0, 0, 0]
        node.GetNthControlPointPosition(0, start)
        node.GetNthControlPointPosition(1, end)
        return np.linalg.norm(np.array(end) - np.array(start))

    def find_circle_line_intersection_in_msp(self, center, radius, line_pt1, line_pt2, debug_name=""):
        center_to_start = line_pt1 - center
        line_vec = line_pt2 - line_pt1
        line_length = np.linalg.norm(line_vec)
        line_unit = line_vec / line_length
        a = np.dot(line_unit, line_unit)
        b = 2 * np.dot(line_unit, center_to_start)
        c = np.dot(center_to_start, center_to_start) - radius**2
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return None, "NO_INTERSECTION"
        t1 = (-b + math.sqrt(discriminant)) / (2*a)
        t2 = (-b - math.sqrt(discriminant)) / (2*a)
        intersect1 = line_pt1 + t1 * line_unit
        intersect2 = line_pt1 + t2 * line_unit
        in_segment1 = (0 <= t1 <= line_length)
        in_segment2 = (0 <= t2 <= line_length)
        if not in_segment1 and not in_segment2:
            return None, "OUT_OF_SEGMENT"
        if in_segment1 and in_segment2:
            chosen_point = intersect1 if t1 > t2 else intersect2
        else:
            chosen_point = intersect1 if in_segment1 else intersect2
        return chosen_point, None

    def create_line(self, p1, p2, name, color=[1.0, 1.0, 1.0], selected_color=[1.0, 0.5, 0.0], thickness=0.25):
        # Check if line already exists and remove it
        existing_node = slicer.util.getFirstNodeByName(name)
        if existing_node:
            slicer.mrmlScene.RemoveNode(existing_node)
            
        line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
        line_node.AddControlPoint(p1.tolist())
        line_node.AddControlPoint(p2.tolist())
        display_node = line_node.GetDisplayNode()
        if display_node:
            display_node.SetColor(*color)
            display_node.SetSelectedColor(*selected_color)
            display_node.SetLineThickness(thickness)
        return line_node

    def draw_circle(self, center, radius, basis1, basis2, name):
        """Draw a thin forest green circle for visualisation in Slicer."""
        # Check if circle already exists and remove it
        existing_node = slicer.util.getFirstNodeByName(name)
        if existing_node:
            slicer.mrmlScene.RemoveNode(existing_node)
            
        curve = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsClosedCurveNode', name)
        n_points = 60
        for i in range(n_points):
            angle = 2 * math.pi * i / n_points
            pt = center + radius * (math.cos(angle) * basis1 + math.sin(angle) * basis2)
            curve.AddControlPoint(pt)
        disp = curve.GetDisplayNode()
        if disp:
            disp.SetColor(0.13, 0.55, 0.13)        # Forest green (unselected)
            disp.SetSelectedColor(0.13, 0.55, 0.13) # Forest green (selected)
            disp.SetLineThickness(0.2)             # Thin line
            disp.SetOpacity(0.7)
        return curve

# Create and show the dialog
widget = NasalPredictionWidget()
widget.show()
```

</details>

### Measuring the prediction errors
For the following code to work, please place the [soft tissue landmarks] on the model. These are stored in [PS_soft_tissue.mrk.json](https://github.com/user-attachments/files/21253770/PS_soft_tissue.mrk.json). 
The script below connects all the prediction set landmarks with the true landmark, measuring the distance between them and creates  red lines called"error_{predicted lmrk name}". 

Draw close attention as there are wo differently defined/predicted subnasale landmarks!


<details>
<summary> Prediction error </summary>

``` python
import slicer
import numpy as np

def get_point_by_label(node, label):
    """Find a point by its label instead of index"""
    for i in range(node.GetNumberOfControlPoints()):
        if node.GetNthControlPointLabel(i) == label:
            point = [0, 0, 0]
            node.GetNthControlPointPosition(i, point)
            return np.array(point)
    
    # If we get here, the point wasn't found
    print(f"⚠️ Warning: Point with label '{label}' not found in {node.GetName()}")
    print("Available points in this node:")
    for i in range(node.GetNumberOfControlPoints()):
        print(f"  - {node.GetNthControlPointLabel(i)}")
    return None

def create_red_line(p1, p2, name):
    """Create a thin red line between two points"""
    # Check if line already exists and remove it
    existing_node = slicer.util.getFirstNodeByName(name)
    if existing_node:
        slicer.mrmlScene.RemoveNode(existing_node)
        
    node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    node.AddControlPoint(p1.tolist())
    node.AddControlPoint(p2.tolist())
    disp = node.GetDisplayNode()
    if disp:
        disp.SetColor(1, 0, 0)           # Red, unselected
        disp.SetSelectedColor(1, 0, 0)   # Red, selected
        disp.SetLineThickness(0.2)
    return node

print("Creating error lines for all predictions...")

# Try to get all the required nodes
try:
    # Ground truth soft tissue
    ps_soft_tissue = slicer.util.getNode('PS_soft_tissue')
    
    # Get the male prediction node
    pred_soft_tissue_male = slicer.util.getNode('pred_soft_tissue_male')
    
    # Get the female prediction node
    pred_soft_tissue_female = slicer.util.getNode('pred_soft_tissue_female')
    
    # Get the FSTT prediction node
    pred_fstt_sn = slicer.util.getNode('pred_FSTT_sn')
    
    missing_nodes = []
    if not ps_soft_tissue:
        missing_nodes.append("PS_soft_tissue")
    
    # Only warn about other nodes if they're missing, don't stop execution
    nodes_to_check = {
        'pred_soft_tissue_male': pred_soft_tissue_male,
        'pred_soft_tissue_female': pred_soft_tissue_female,
        'pred_FSTT_sn': pred_fstt_sn
    }
    
    for name, node in nodes_to_check.items():
        if not node:
            missing_nodes.append(name)
            print(f"⚠️ Warning: {name} not found. Error lines using this node will be skipped.")
    
    if not ps_soft_tissue:
        print("❌ Error: PS_soft_tissue node is missing. This node contains the ground truth landmarks.")
        raise ValueError("Missing PS_soft_tissue node")
        
except Exception as e:
    print(f"❌ Error finding nodes: {e}")
    raise

# Define all the connections we want to make
connections = []

# MALE PREDICTIONS TO GROUND TRUTH
if pred_soft_tissue_male:
    connections.extend([
        # Male sn prediction to ground truth
        (pred_soft_tissue_male, "pred_sn_male", ps_soft_tissue, "sn'", "error_sn_male"),
        # Male prn prediction to ground truth
        (pred_soft_tissue_male, "pred_prn_male", ps_soft_tissue, "prn", "error_prn_male"),
    ])

# FEMALE PREDICTIONS TO GROUND TRUTH
if pred_soft_tissue_female:
    connections.extend([
        # Female sn prediction to ground truth
        (pred_soft_tissue_female, "pred_sn_female", ps_soft_tissue, "sn'", "error_sn_female"),
        # Female prn prediction to ground truth
        (pred_soft_tissue_female, "pred_prn_female", ps_soft_tissue, "prn", "error_prn_female"),
    ])

# FSTT PREDICTIONS TO GROUND TRUTH
if pred_fstt_sn:
    connections.extend([
        # FSTT sn prediction to ground truth
        (pred_fstt_sn, "sn'_FSTT", ps_soft_tissue, "sn'", "error_FSTT_sn"),
    ])

# MALE PREDICTIONS TO FSTT
if pred_soft_tissue_male and pred_fstt_sn:
    connections.extend([
        # Male sn prediction to FSTT sn
        (pred_soft_tissue_male, "pred_sn_male", pred_fstt_sn, "sn'_FSTT", "error_sn_male_to_FSTT"),
    ])

# FEMALE PREDICTIONS TO FSTT
if pred_soft_tissue_female and pred_fstt_sn:
    connections.extend([
        # Female sn prediction to FSTT sn
        (pred_soft_tissue_female, "pred_sn_female", pred_fstt_sn, "sn'_FSTT", "error_sn_female_to_FSTT"),
    ])

# Create all the connection lines
created_lines = 0
for source_node, source_label, target_node, target_label, line_name in connections:
    source_point = get_point_by_label(source_node, source_label)
    target_point = get_point_by_label(target_node, target_label)
    
    if source_point is not None and target_point is not None:
        create_red_line(source_point, target_point, line_name)
        created_lines += 1
        print(f"✅ Created red line: {line_name}")
    else:
        print(f"❌ Could not create line {line_name} - one or both points missing")

print(f"\n✅ Created {created_lines} red error lines")
```

You can expect a view like this: 

<img width="830" height="724" alt="image" src="https://github.com/user-attachments/assets/554aab25-1d06-4c1e-938a-3a9e171e40ef" />



</details>


### Recreating all soft and hard tissue measurements 

If you wish to run data analysis on the whole of the study to see different relationships or find equations that suits your population, the code below creates the rest of (soft tissue dependent) measurements mentioned in the study, regardless of their significance. 


<details>
<summary> Rest of the measurements </summary>

``` python
import numpy as np
import slicer
import qt

print("Starting landmark measurement script...")

def get_point(markups_node, label):
    """Gets a point by label from a markup fiducial node"""
    if markups_node is None:
        raise ValueError(f"Cannot find landmark '{label}' - node is missing")
        
    for i in range(markups_node.GetNumberOfControlPoints()):
        if markups_node.GetNthControlPointLabel(i) == label:
            point = [0, 0, 0]
            markups_node.GetNthControlPointPosition(i, point)
            return np.array(point)
            
    # If we get here, the landmark wasn't found
    print(f"⚠️ WARNING: Landmark '{label}' not found in {markups_node.GetName()}")
    print(f"   Available landmarks in {markups_node.GetName()}:")
    for i in range(markups_node.GetNumberOfControlPoints()):
        print(f"   - {markups_node.GetNthControlPointLabel(i)}")
    
    # Show a warning dialog
    msg = qt.QMessageBox()
    msg.setIcon(qt.QMessageBox.Warning)
    msg.setText(f"Landmark '{label}' not found")
    msg.setInformativeText(f"The landmark '{label}' was not found in node '{markups_node.GetName()}'")
    msg.setWindowTitle("Missing Landmark")
    msg.exec_()
    
    raise ValueError(f"Landmark '{label}' not found")

def create_measurement_line(name, point1, point2):
    """Creates a line between two points and returns the distance"""
    line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
    line_node.AddControlPoint(point1.tolist())
    line_node.AddControlPoint(point2.tolist())
    display_node = line_node.GetDisplayNode()
    if display_node:
        display_node.SetTextScale(3)
    return np.linalg.norm(point2 - point1)

def create_angle(name, point1, apex, point2):
    """Creates an angle measurement and returns the angle in degrees"""
    angle_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsAngleNode", name)
    angle_node.AddControlPoint(point1.tolist())
    angle_node.AddControlPoint(apex.tolist())
    angle_node.AddControlPoint(point2.tolist())
    display_node = angle_node.GetDisplayNode()
    if display_node:
        display_node.SetTextScale(3)
    return angle_node.GetAngleDegrees()

def shortest_line_between_lines(p1, p2, q1, q2):
    """Returns closest points and distance between two lines"""
    v = p2 - p1
    u = q2 - q1
    w0 = p1 - q1
    
    a = np.dot(v, v)
    b = np.dot(v, u)
    c = np.dot(u, u)
    d = np.dot(v, w0)
    e = np.dot(u, w0)
    
    denom = a*c - b*b
    if abs(denom) < 1e-6:  # Parallel lines
        w = p1 - q1
        distance = np.linalg.norm(np.cross(w, u)) / np.linalg.norm(u)
        mid_p = (p1 + p2)/2
        mid_q = (q1 + q2)/2
        return mid_p.astype(float), mid_q.astype(float), distance
    else:
        s = (b*e - c*d) / denom
        t = (a*e - b*d) / denom
    
    P = p1 + s*v
    Q = q1 + t*u
    return P.astype(float), Q.astype(float), np.linalg.norm(P-Q)

# Find the landmark nodes - checking multiple possible names
print("Looking for landmark nodes...")

# Try to get nodes with different possible names
hard_tissue = None
soft_tissue = None

possible_hard_names = ["PS_hard_tissue", "PS_hard_tissue", "P_and_S_hard_tissue", "Hard_tissue"]
possible_soft_names = ["PS_soft_tissue", "P&S_soft_tissue", "P_and_S_soft_tissue", "Soft_tissue"]

for name in possible_hard_names:
    node = slicer.util.getFirstNodeByName(name)
    if node:
        hard_tissue = node
        print(f"✅ Found hard tissue landmarks as: {name}")
        break

for name in possible_soft_names:
    node = slicer.util.getFirstNodeByName(name)
    if node:
        soft_tissue = node
        print(f"✅ Found soft tissue landmarks as: {name}")
        break

# If we couldn't find the nodes, show what's available
if hard_tissue is None or soft_tissue is None:
    print("\n❌ Could not find landmark nodes. Here are all available markup nodes:")
    all_nodes = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')
    for node in all_nodes:
        print(f"  - {node.GetName()}")
    
    # Show error dialog with available nodes
    msg = qt.QMessageBox()
    msg.setIcon(qt.QMessageBox.Critical)
    msg.setText("Missing landmark nodes")
    msg.setInformativeText("Please make sure you have created landmark points with correct names.")
    msg.setDetailedText("Available fiducial nodes:\n" + 
                        "\n".join([node.GetName() for node in all_nodes]))
    msg.setWindowTitle("Missing Landmarks")
    msg.exec_()
    
    raise ValueError("Missing required landmark nodes")

# Get baseline or create if missing
try:
    baseline_node = slicer.util.getFirstNodeByName("baseline")
    if baseline_node:
        baseline_start = np.zeros(3)
        baseline_end = np.zeros(3)
        baseline_node.GetNthControlPointPosition(0, baseline_start)
        baseline_node.GetNthControlPointPosition(1, baseline_end)
        baseline_dir = (baseline_end - baseline_start)
        baseline_dir = baseline_dir / np.linalg.norm(baseline_dir)
        print("✅ Found existing baseline")
    else:
        raise ValueError("Baseline node exists but couldn't get points")
except:
    print("⚠️ Creating new baseline along X-axis")
    try:
        n_soft = get_point(soft_tissue, "n'")
        baseline_dir = np.array([1.0, 0.0, 0.0])  # Default X-direction
        baseline_start = n_soft.copy()
        baseline_end = n_soft + baseline_dir * 100.0
        baseline_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "baseline")
        baseline_node.AddControlPoint(baseline_start.tolist())
        baseline_node.AddControlPoint(baseline_end.tolist())
    except Exception as e:
        print(f"❌ Error creating baseline: {e}")
        raise

print("\n==================================================")
print("LINEAR MEASUREMENTS")
print("==================================================")

try:
    # 1. n-n'
    print("Creating n-n' measurement...")
    n_hard = get_point(hard_tissue, "n")
    n_soft = get_point(soft_tissue, "n'")
    nn_dist = create_measurement_line("n-n'", n_hard, n_soft)
    print(f"  Distance: {nn_dist:.2f} mm")

    # 2. rhi-rhi'
    print("Creating rhi-rhi' measurement...")
    rhi_hard = get_point(hard_tissue, "rhi")
    rhi_soft = get_point(soft_tissue, "rhi'")
    rhi_dist = create_measurement_line("rhi-rhi'", rhi_hard, rhi_soft)
    print(f"  Distance: {rhi_dist:.2f} mm")

    # 3. sn' (single point, no measurement)
    print("Finding sn'...")
    sn = get_point(soft_tissue, "sn'")
    print(f"  Found at: {sn}")

    # 4. al-al
    print("Creating al-al measurement...")
    alL = get_point(soft_tissue, "X1(alL)")
    alR = get_point(soft_tissue, "X2(alR)")
    al_dist = create_measurement_line("al-al", alL, alR)
    print(f"  Distance: {al_dist:.2f} mm")

    # 5. nb-nb
    print("Creating nb-nb measurement...")
    nbL = get_point(soft_tissue, "Y1(nbL)")
    nbR = get_point(soft_tissue, "Y2(nbR)")
    nb_dist = create_measurement_line("nb-nb", nbL, nbR)
    print(f"  Distance: {nb_dist:.2f} mm")

    # 6. X-Y (shortest distance between al-al and nb-nb)
    print("Creating X-Y (shortest distance) measurement...")
    P, Q, xy_dist = shortest_line_between_lines(alL, alR, nbL, nbR)
    xy_line = create_measurement_line("X-Y", P, Q)
    disp = slicer.util.getNode("X-Y").GetDisplayNode()
    if disp:
        disp.SetGlyphType(4)  # Spheres at ends
    print(f"  Distance: {xy_dist:.2f} mm")

    # 7. soft n-nt
    print("Creating soft n-nt measurement...")
    nt = get_point(soft_tissue, "nt")
    n_nt_dist = create_measurement_line("soft n-nt", n_soft, nt)
    print(f"  Distance: {n_nt_dist:.2f} mm")

    # 8. prn perp baseline
    print("Creating prn perpendicular to baseline measurement...")
    prn = get_point(soft_tissue, "prn")
    prn_proj = baseline_start + np.dot(prn - baseline_start, baseline_dir) * baseline_dir
    prn_perp_dist = create_measurement_line("prn perp baseline", prn, prn_proj)
    print(f"  Distance: {prn_perp_dist:.2f} mm")

    print("\n==================================================")
    print("ANGULAR MEASUREMENTS")
    print("==================================================")

    # soft rhi'-prn-sn'
    print("Creating soft rhi'-prn-sn' angle...")
    rhi_prn_sn_angle = create_angle("soft rhi'-prn-sn'", rhi_soft, prn, sn)
    print(f"  Angle: {rhi_prn_sn_angle:.2f} degrees")

    # prn-sn'-nt
    print("Creating prn-sn'-nt angle...")
    prn_sn_nt_angle = create_angle("prn-sn'-nt", prn, sn, nt)
    print(f"  Angle: {prn_sn_nt_angle:.2f} degrees")

    # al-prn-al
    print("Creating al-prn-al angle...")
    al_prn_al_angle = create_angle("al-prn-al", alL, prn, alR)
    print(f"  Angle: {al_prn_al_angle:.2f} degrees")

    print("\n✅ All measurements created successfully!")

except Exception as e:
    print(f"\n❌ Error during measurements: {e}")
    
    # Show friendly error dialog
    msg = qt.QMessageBox()
    msg.setIcon(qt.QMessageBox.Warning)
    msg.setText("Problem creating measurements")
    msg.setInformativeText(str(e))
    msg.setWindowTitle("Measurement Error")
    msg.exec_()
```


</details>

| Measurement | Script Implementation | Landmarks Used |
|-------------|----------------------|----------------|
| n-n' | distance between hard and soft tissue nasions| n (hard), n' (soft) |
| rhi-rhi' | distance between hard and soft tissue rhinions | rhi (hard), rhi' (soft) |
| al-al | distance between most laterally projected points on the nasal wings  | X1(alL), X2(alR) |
| nb-nb | distance between the base of the left and right attachment of nasal wings on the upper lip | Y1(nbL), Y2(nbR) |
| X-Y | "X-Y" | Shortest perpendicular distance between al-al and nb-nb |
| soft n-nt | distance between soft nasion and nasal tip | n', nt |
| prn perp baseline | Shortest perpendicular distance between the baseline and the pronasale | prn, projected point on baseline |
| soft rhi'-prn-sn' | angle of the nose tip | rhi', prn, sn' |
| prn-sn'-nt | angle predicting the dipping of the lower part of the nose below the ‘prn’ landmark | prn, sn', nt |
| al-prn-al |  angle of the nasal wing | X1(alL), prn, X2(alR) |

## Output
What can you expect as the outputs from the previous codes? We deleted a few extra lines with the **Remove helper lines** button, but there are still a few pseudo-lines to ignore when copying the measurements as described in [this guide](https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Start%20here%20/004_Copy%20measurements%20to%20clipboard.md#code-to-copy-linear-measurements). 
We will show an example: 

<details>
<summary> Everything was enabled, both male and female predictions </summary>

| Patient ID | Axis/Detail | Value | Notes/Comments |
|------------|-------------|-------|----------------|
|            | FHP guide | 70 | ❌ - not a real measurement |
|            | st n guide | 70 | ❌ - not a real measurement |
|            | st rhi guide | 70 | ❌ - not a real measurement |
|            | st sn guide | 70 | ❌ - not a real measurement |
|            | n to sn FSTT | 53.34 | |
|            | AB | 27.66 | |
|            | CD | 10.87 | |
|            | baseline | 50.29 | |
|            | n to rhi | 19.44 | |
|            | rhi to baseline | 10.93 | |
|            | ANS perpendicular_female | 60 | ❌ - not a real measurement |
|            | n to pred_sn_female | 53.39 | result of equation bony n-sn for females |
|            | ANS to pred_prn_female | 21.86 | result of equation baseline to prn for females |
|            | pred_prn to pred_sn_female | 26.12 | ❌  for visualisation |
|            | ANS perpendicular_male | 60 | ❌ - not a real measurement |
|            | n to pred_sn_male | 54.08 | result of equation bony n-sn for males  |
|            | ANS to pred_prn_male | 22.81 | result of equation baseline to prn for females |
|            | pred_prn to pred_sn_male | 30.86 | ❌ for visualisation |
|            | error_sn_male | 23.52 | |
|            | error_prn_male | 8.38 | |
|            | error_sn_female | 19.74 | |
|            | error_prn_female | 9.1 | |
|            | error_FSTT_sn | 4.65 | |
|            | error_sn_male_to_FSTT | 19.08 | |
|            | error_sn_female_to_FSTT | 15.29 | |
|            | n-n' | 6.17 | |
|            | rhi-rhi' | 2.27 | |
|            | al-al | 34.54 | |
|            | nb-nb | 25.52 | |
|            | X-Y | 7.39 | |
|            | soft n-nt | 53.15 | |
|            | prn perp baseline | 28.99 | |
|            | soft rhi'-prn-sn' | 83.97 | |
|            | prn-sn'-nt | 27.18 | |
|            | al-prn-al | 83.86 | |

*the lines pred_prn to pred_sn_{sex} were left is as this line also appeared on Fig. 1 in Purkait & Singh, 2024[^2]

</details>

#### Research idea

It may be worth implementing the coordinate system mentioned by [Thitiorul et al. 2020](https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Nose%20predictions/Thitiorul2020.md#the-thitiorul-2020-method) to this method as the nasion is also a central landmark in this method, and run analysis on the individual coordinates to see it these landmarks have significant correlations and/or predictive power to estimate soft tissue landmarks. The description of nt' by Purkait & Singh, 2024[^2] is similar to nd' in [Thitiorul et al. 2020](https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Nose%20predictions/Thitiorul2020.md#landmarks-in-this-guide). 

# Bibliography

[^1]: 3D Slicer webpage https://www.slicer.org/
[^2]: Singh, S. and R. Purkait (2024). "Three-dimensional prediction of the nose for facial reconstruction: A preliminary study on North Indian adults." Journal of Forensic and Legal Medicine 105: 102708.
[^3]: Caple, J. and C. N. Stephan (2016). "A standardized nomenclature for craniofacial and facial anthropometry." International Journal of Legal Medicine 130(3): 863-879.
[^4]: Howells, W. W. (1937). "The designation of the principle anthrometric landmarks on the head and skull." American Journal of Physical Anthropology 22(3): 477-494.
[^5]: Howells, W. W. (1974). Cranial variation in man: A study by multivariate analysis of patterns of difference among recent human populations. Cambridge, Harvard University.
[^6]: Martin, R. (1928). Lehrbuch der Anthropologie in systematischer Darstellung: mit besonderer Berücksichtigung der anthropologischen Methoden ; für Studierende, Ärzte und Forschungsreisendechichte, Morphologische Methoden. Jena, Gustav Fisher.
[^7]: Knussmann, R. (1988). Anthropologie: Handbuch der vergleichenden Biologie des Menschen, G. Fischer.
[^8]: Kolar, J. and E. Salter (1997). Craniofacial anthropometry: practical measurement of the head and face for clinical, surgical, and research use. Springfield, Charles C Thomas.
[^9]: Stephan, C. N. and E. K. Simpson (2008). "Facial soft tissue depths in craniofacial identification (part I): An analytical review of the published adult data." Journal of Forensic Sciences 53(6): 1257-1272.
[^10]: Farkas, L. G. (1994). Anthropometry of the Head and Face, Lippincott Williams & Wilkins.	
[^11]: Hona, T. W. P. T. and C. N. Stephan (2024). "Global facial soft tissue thicknesses for craniofacial identification (2023): a review of 140 years of data since Welcker’s first study." International Journal of Legal Medicine 138(2): 519-535.

