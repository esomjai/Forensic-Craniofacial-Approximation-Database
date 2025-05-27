# Rynn et al. 2010's technique

For reference code snippets and insight for how 3D Slicer works, please refer to the official 3D Slicer webpage [^1]. 

The technique by Rynn et al 2010[^3] has been applied, tested and recalibrated by numerous studies - mostly the measurements for linear regressions in focus. In this guide, the replication of all their measurements described in the 2006 PhD thesis by Christopher Rynn titled **Craniofacial approximation and reconstruction: tissue depth patterning and the prediction of the nose**. We will also include the recalibrated linear regressions by Sarilita et al. (2018)[^12] and Bulut et al. (2019)[^13].


This will be achieved by:

- Creating the [INB plane](#inb-plane), [NP plane](#np-plane) and [PT plane](#pt-plane) as defined by Rynn et al. (2010)

1) Creating a line from the nasion that is perpendicular to the NPP - for later pronasale ant measurement
2) Creating a line from the nasion along the NPP - for later pronasale vert measurement
3) Creating a line from the subspinale that is parallel to the FHP - for later nasal depth/subnasale prediction
4) Calculating the length of the pronasale anterior (according to the linear regression the chosen method) and measuring it from the nasion onto line 2

> [!WARNING]
> The sample CT (CBCT PreDentalSurgery) used in the screenshots of this guide does not have all the features (inion, bregma) that are to be landmarked. Please refer to the illustrations in the guide for correct placement. In addition, due to the CT being taken pre-surgery for an underbite, the error rate shown in the guide is probably not representative if implemented on a population without pathologies.


### Landmarks in this guide 
> [!TIP]
> If you are only interested in reproducing the x, y, z axes and the pron ant, pron vert, pron pFHP, nasal length (nas ln), nasal height (nas ht), nasal depth (nas dp) measurements, allocate ONLY landmarks highlighted with a 🔵 for hard tissue points and 🟧 for soft tissue points.

#### Hard tissue landmarks
[Rynn_hard_tissue.mrk.json](https://github.com/user-attachments/files/20417966/Rynn_hard_tissue.mrk.json)


| Position in code | Position in file | Name in file | Landmark name | Definition | Defined by |
|------------------|------------------|--------------|--------------|------------|------------|
| 🔵 0                | 1                | nasion       | nasion       | Intersection of the nasofrontal sutures in the median plane | Martin, 1928[^5]; Knussmann, 1988[^6]; Caple & Stephan 2016[^4] |
| 🔵 1                | 2                | inion        | inion        | Median point between the apices of the superior nuchal lines and at the base of the external occipital protuberance (not the tip of the protuberance) | Martin, 1928[^5]; Knussmann, 1988[^6]; Caple & Stephan 2016[^4] |
| 🔵 2                | 3                | bregma       | bregma       | Where the sagittal and coronal sutures meet. Impossible to determine in juvenile skulls with anterior fontanelle, or with complete suture obliteration | Martin, 1928[^5]; Knussmann, 1988[^6]; Caple & Stephan 2016[^4]|
| 🔵 3                | 4                | prosthion    | prosthion    | Median point between the central incisors on the anterior most margin of the maxillary alveolar rim | Martin, 1928[^5]; Knussmann, 1988[^6]; Caple & Stephan 2016[^4] |
| 🔵 4                | 5                | subspinale   | subspinale   | The deepest point seen in the profile view below the anterior nasal spine (orthodontic point A) | Howells, 1937[^7]; Howells, 1974[^8]; Caple & Stephan 2016[^4] |
| 🔵 5                | 6                | rhinion      | rhinion      | Most rostral (end) point on the internasal suture. | Martin, 1928[^5]; Knussmann, 1988[^6]; Caple & Stephan 2016[^4] |
| 🔵 6                | 7                | acanthion    | acanthion    | Most anterior tip of the anterior nasal spine | Howells, 1937[^7]; Howells, 1974[^8]; Caple & Stephan 2016[^4] |
| 7                | 8                | CL           | CL           | midpoint of where the left inferior turbinate or left conch meets the nasal border | Rynn et al 2010[^3]|
| 8                | 9                | CR           | CR           | midpoint of where the left inferior turbinate or left conch meets the nasal border midpoint of where the right  inferior turbinate or right conch meets the nasal border | Rynn et al 2010[^3] |
| 9                | 10               | XL           | XL           | the most posterior point on the left border of the piriform aperture (PLB) | Rynn et al 2010[^3] |
| 10               | 11               | XR           | XR           | the most posterior point on the right border of the piriform aperture (PLB) | Rynn et al 2010[^3] |
| 11               | 12               | LL           | LL           | the left lowest point on the aperture border | Rynn et al 2010[^3] |
| 12               | 13               | LR           | LR           | the right lowest point on the aperture border | Rynn et al 2010[^3] |
| 13               | 14               | ICR           | ICR           | right maxillary canine cusp tip point | Glanville (1969)[^14], Rynn et al 2006[^2] |
| 14               | 15               | ICL           | ICL           | left maxillary canine cusp tip point |  Glanville (1969)[^14], Rynn et al 2006[^2]|
| 15               | 16               | LCIL          | LCIL           | most lateral point on the left central incisor in the maxilla |  Glanville (1969)[^14], Rynn et al 2006[^2] |
| 16               | 17               | LCIR          | LCIR           | most lateral point on the right central incisor in the maxilla |  Glanville (1969)[^14], Rynn et al 2006[^2] |
| 17               | 18               | MCIL          | MCIL           | most medial point on the left central incisor in the maxilla |  Glanville (1969)[^14], Rynn et al 2006[^2] |
| 18               | 19               | MCIR          | MCIR           | most medial point on the right central incisor in the maxilla |  Glanville (1969)[^14], Rynn et al 2006[^2] |


#### Soft tissue landmarks

[Rynn_soft_tissue.mrk.json](https://github.com/user-attachments/files/20264693/Rynn_soft_tissue.mrk.json)

| Position in code | Position in file | Name in file   | Landmark name | Definition                                                                                                            | Defined by |
|------------------|------------------|---------------|--------------|-----------------------------------------------------------------------------------------------------------------------|------------|
| 🟧 0                | 1                | soft nasion   | soft nasion  | Point directly anterior to the nasofrontal suture, in the midline, overlying n                                        |  Kolar, 1997[^9]; Caple & Stephan 2016[^4]          |
| 🟧 1                | 2                | subnasale     | subnasale    | Median point at the junction between the lower border of the nasal septum and the philtrum area                       |  Kolar, 1997[^9]; Caple & Stephan 2016[^4]       |
| 🟧 2                | 3                | pronasale     | pronasale    | The most anteriorly protruded point of the apex nasi. In the case of a bifid nose, the more protruding tip is chosen  | Farkas, 1994[^10]; Caple & Stephan 2016[^4]          |
| 3                | 4                | pt1R          | pt1R         | most anterior point on right nostril border                                                                           | Rynn et al 2010[^3]         |
| 4                | 5                | pt1L          | pt1L         | most anterior point on left nostril border                                                                            | Rynn et al 2010[^3]          |
| 5                | 6                | pt2R          | pt2R         | most posterior point on right nostril border                                                                          | Rynn et al 2010[^3]          |
| 6                | 7                | pt2L          | pt2L         | most posterior point on left nostril border                                                                           | Rynn et al 2010[^3]          |
| 7                | 8                | pt3R          | pt3R         | most superior point on right nostril border                                                                           | Rynn et al 2010[^3]          |
| 8                | 9                | pt3L          | pt3L         | most superior point on left nostril border                                                                            | Rynn et al 2010[^3]          |
| 9                | 10               | pt4R          | pt4R         | most proximal point  on the right on alar groove                                                                      | Rynn et al 2010[^3]          |
| 10               | 11               | pt4L          | pt4L         | most proximal point  on the left on alar groove                                                                       | Rynn et al 2010[^3]          |
| 11               | 12               | pt5R          | pt5R         | most superior point on the right on alar groove                                                                       | Rynn et al 2010[^3]          |
| 12               | 13               | pt5L          | pt5L         | most superior point on the left on alar groove                                                                        | Rynn et al 2010[^3]          |
| 13               | 14               | pt6R          | pt6R         | most lateral point on ala on the right                                                                                | Rynn et al 2010[^3]          |
| 14               | 15               | pt6L          | pt6L         | most lateral point on ala on the left                                                                                 | Rynn et al 2010[^3]          |
| 15               | 16               | pt7R          | pt7R         | most inferior point on the right on alar groove                                                                       | Rynn et al 2010[^3]          |
| 16               | 17               | pt7L          | pt7L         | most inferior point on the left on alar groove                                                                        | Rynn et al 2010[^3]          |
| 17               | 18               | pt8R          | pt8R         | columella break point on the right                                                                                    | Rynn et al 2010[^3]          |
| 18               | 19               | pt8L          | pt8L         | columella break point on the left                                                                                     | Rynn et al 2010[^3]          |



For the precision of this method, follow the 4-point FHP guide in () with downloading and allocating [FH4_landmarks.json](https://github.com/user-attachments/files/20265033/FH4_landmarks.json)



### Illustration of the method

> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

- [ ] The scan has to be re-aligned in the FHP
- [ ] You should have a Bone and Skin model via segmentation (explained later)
- [ ] Have a **4-point FHP**
- [ ] Allocate  landmarks from files


https://github.com/user-attachments/assets/a2b0455f-9f14-4da0-98c5-28cfc1c0bc4b



### INB plane

To help with the side profile, we will establish the “INB” plane as defined by Rynn et al. 2010[^3]. 

> a midsagittal plane (INB) which bisected the inion, nasion and bregma

by downloading markups file for this method, allocating the landmarks and copying and pasting the following code: 

```python
#INB plane#

import numpy as np
import slicer

# Get the points from the "Rynn_hard_tissue" node
hardTissueNode = slicer.util.getNode('Rynn_hard_tissue')
point1 = np.array(hardTissueNode.GetNthControlPointPosition(0))
point2 = np.array(hardTissueNode.GetNthControlPointPosition(1))
point3 = np.array(hardTissueNode.GetNthControlPointPosition(2))

# Calculate the normal of the plane defined by the three points
v1 = point2 - point1
v2 = point3 - point1
planeNormal = np.cross(v1, v2)
planeNormal = planeNormal / np.linalg.norm(planeNormal)  # Normalize the normal vector

# Create a new plane node
newPlaneNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'INB')

# Set the origin of the new plane to the first point
newPlaneNode.SetOrigin(point1)

# Set the normal of the new plane
newPlaneNode.SetNormal(planeNormal)

import slicer

# Get the plane node "INB"
planeNode = slicer.util.getNode("INB")

# Set the color of the plane to turquoise (RGB: 0.25, 0.88, 0.82) when not selected
displayNode = planeNode.GetDisplayNode()
displayNode.SetColor(0.25, 0.88, 0.82)
displayNode.SetSelectedColor(0.25, 0.88, 0.82)
displayNode.SetVisibility(True)


```
<img src="https://github.com/user-attachments/assets/e651bf90-5d0b-4502-b26a-a53b19de2b9b" width="500">


View of the generated INB 
<img src="https://github.com/user-attachments/assets/5c525822-9a71-4c2b-9b22-18bbd3ef6936" width="500">


INB extended via the toggles (green and red dots in all views)

### NP plane
May be referred to as NPP - nasion-prosthion plane; defined by Rynn as 

> a coronal plane which bisects the nasion and prosthion in lateral view, whilst lying at right angles to INB

To create this plane, use this code: 

```python
import numpy as np
import slicer

# Get the 'INB' plane node
inbPlaneNode = slicer.util.getNode('INB')

# Get the 'Rynn_hard_tissue' point list node
hardTissueNode = slicer.util.getNode('Rynn_hard_tissue')

# Get the coordinates of 'prosthion' and 'nasion' from the point list
prosthion = np.array(hardTissueNode.GetNthControlPointPositionWorld(0))
nasion = np.array(hardTissueNode.GetNthControlPointPositionWorld(3))

# Calculate the normal of the 'INB' plane
inbNormal = np.array(inbPlaneNode.GetNormalWorld())

# Calculate the vector between 'prosthion' and 'nasion'
vectorPN = nasion - prosthion

# Calculate the normal of the new plane (perpendicular to 'INB' and fitting 'prosthion' and 'nasion')
newPlaneNormal = np.cross(inbNormal, vectorPN)
newPlaneNormal /= np.linalg.norm(newPlaneNormal)  # Normalize the vector

# Create a new plane node and name it 'NPP'
newPlaneNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'NPP')

# Set the origin of the new plane to 'prosthion'
newPlaneNode.SetOriginWorld(prosthion)

# Set the normal of the new plane
newPlaneNode.SetNormalWorld(newPlaneNormal)

import slicer

# Get the plane node "NPP"
planeNode = slicer.util.getNode("NPP")
# Set the color of the plane to sunset yellow (RGB: 1.0, 0.84, 0.0) when not selected
displayNode = planeNode.GetDisplayNode()
displayNode.SetColor(1.0, 0.84, 0.0)
displayNode.SetSelectedColor(1.0, 0.84, 0.0)
displayNode.SetVisibility(True)


print("New plane 'NPP' created successfully.")
 ```
### PT plane
May be referred to as PT - Prokopec transverse plane; defined by Rynn as 

> a transverse plane set at right angles to both the INB plane and the NPP, corresponding with the profile prediction lines used by Prokopec and Ubelaker[^11]
 
 To create this plane, use this code: 
 
 ```python
import numpy as np
import slicer
 # Get the 'INB' and 'NPP' plane nodes
 inbPlaneNode = slicer.util.getNode('INB')
nppPlaneNode = slicer.util.getNode('NPP')

# Calculate the normals of the 'INB' and 'NPP' planes
 inbNormal = np.array(inbPlaneNode.GetNormalWorld())
 nppNormal = np.array(nppPlaneNode.GetNormalWorld())
# Calculate the normal of the new plane 'PTP' (perpendicular to both 'INB' and 'NPP')
ptpNormal = np.cross(inbNormal, nppNormal)
ptpNormal /= np.linalg.norm(ptpNormal)  # Normalize the vector

# Create a new plane node and name it 'PTP'
ptpPlaneNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'PTP')

# Set the origin of the new plane to the origin of 'INB' (or any other point of your choice)
ptpPlaneNode.SetOriginWorld(inbPlaneNode.GetOriginWorld())

# Set the normal of the new plane
ptpPlaneNode.SetNormalWorld(ptpNormal)

import slicer

# Get the plane node "PTP"
planeNode = slicer.util.getNode("PTP")
# Set the color of the plane to lavender (RGB: 0.71, 0.49, 0.86) when not selected
displayNode = planeNode.GetDisplayNode()
displayNode.SetColor(0.71, 0.49, 0.86)
displayNode.SetSelectedColor(0.71, 0.49, 0.86)
displayNode.SetVisibility(True)

print("New plane 'PTP' created successfully.")
```

![image](https://github.com/user-attachments/assets/8b3c4cc4-80eb-430f-af9c-e32179abb6e4)

Expected view with all  planes established and extended. Landmarks hidden for representative purposes. Please note that the INB plane cannot be reproducibly replicated as there are no bregma and inion landmarks visible on the sample CT used. 

### Creating the x, y and z axes

![image](https://github.com/user-attachments/assets/1c670013-66de-448a-aa60-253e9b7a1800)
Essentially recreating the "scale" on which the pron ant, pron vert, pron pFHP, nasal length (nas ln), nasal height (nas ht), nasal depth (nas dp) is predicted later on via regression equations. 
The x axis runs between the _nasion and acanthion_, the y axis runs between _rhinion and subspinale_ and the z axis between the _nasion and subspinale_. 

```python
import slicer

# X axis
F = slicer.util.getNode('Rynn_hard_tissue')
L = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(6)
L.AddControlPoint(secondPoint)
L.SetName('nas-aca X')
displayNode = L.GetDisplayNode()
displayNode.SetColor(1, 0, 0)  # Red
displayNode.SetSelectedColor(1, 0, 0)  # Red when selected
displayNode.SetVisibility(True)

# Y axis
F = slicer.util.getNode('Rynn_hard_tissue')
L = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(5)
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(4)
L.AddControlPoint(secondPoint)
L.SetName('rhi-subs Y')
displayNode = L.GetDisplayNode()
displayNode.SetColor(0, 1, 0)  # Green
displayNode.SetSelectedColor(0, 1, 0)  # Green when selected
displayNode.SetVisibility(True)

# Z axis
F = slicer.util.getNode('Rynn_hard_tissue')
L = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(4)
L.AddControlPoint(secondPoint)
L.SetName('nas-subs Z')
displayNode = L.GetDisplayNode()
displayNode.SetColor(0, 0, 0)  # Black
displayNode.SetSelectedColor(0, 0, 0)  # Black when selected
displayNode.SetVisibility(True)
```
<img src="https://github.com/user-attachments/assets/b37182c6-a850-4d1a-9e16-793f75d0ee23" width="500">

### Creating the reference network of lines
The code used for this also enforces the lines to be in the same plane as the rhinion, nasion and acanthion to reduce added error in measurements. This may be unnecessary if the INB plane can reliably be established. 

<img src="https://github.com/user-attachments/assets/e392cbde-039a-4f8d-bd9f-2f20f1211174" width="500">

| Line number | Definition | colour in file   | 
|------------------|------------------|---------------|
|  1                |  line from the nasion that is perpendicular to the NPP (PTP); used later for pronasale ant measurement            | orange   | 
|  2                |  line from the nasion along the NPP; used later for pronasale vert measurement           | orange   | 
|  3                | line bisecting the subspinale parallel to the FHP; used later for nasal height/depth measurement             | orange   | 

<details>
<summary>Code for lines 1,2 and 3</summary>

```python
import slicer
import numpy as np

def create_line(name, length, color, start_point, direction):
    line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
    line.GetDisplayNode().SetSelectedColor(color)
    half_length = length / 2
    start_point = np.array(start_point)
    direction = np.array(direction)
    line.AddControlPoint((start_point - direction * half_length).tolist())
    line.AddControlPoint((start_point + direction * half_length).tolist())
    return line

rynn_hard_tissue = slicer.util.getNode("Rynn_hard_tissue")
npp_plane = slicer.util.getNode("NPP")
ptp_plane = slicer.util.getNode("PTP")
fhp_plane = slicer.util.getNode("FHP")

start_point_1 = rynn_hard_tissue.GetNthControlPointPosition(0)
start_point_3 = rynn_hard_tissue.GetNthControlPointPosition(4)

npp_normal = np.array(npp_plane.GetNormal())
ptp_normal = np.array(ptp_plane.GetNormal())
fhp_normal = np.array(fhp_plane.GetNormal())

# Get a direction in the FHP plane (not perpendicular)
reference = np.array([1, 0, 0])
if np.allclose(fhp_normal, reference):
    reference = np.array([0, 1, 0])
fhp_plane_direction = np.cross(fhp_normal, reference)
fhp_plane_direction = fhp_plane_direction / np.linalg.norm(fhp_plane_direction)

orange_color = (1.0, 0.5, 0.0)
line_1 = create_line("1", 200, orange_color, start_point_1, npp_normal)
line_2 = create_line("2", 200, orange_color, start_point_1, ptp_normal)
line_3 = create_line("3", 200, orange_color, start_point_3, fhp_plane_direction)
```

</details>

### Calculating & applying the predicted length of the pronasale anterior

The predicted length of the pronasale anterior will be measured from the nasion onto the previously established line 1. As there are different revised methods available, the code below will offer you to choose the option(s) by which the pronasale anterior distance is calculated. All lines generated by this code will be purple in the environment.
Please make sure you document which method you used and why - the naming convention of the new line(s) will help jog your memory. The table below is a quick summary, please refer to the original studies [^3], [^12], [^13] for explanation.

From this point on, a floating widget will appear to recall the decisions the user made at any point using the GUI's. 


<table>
  <tr>
    <th colspan="5" style="text-align:center">Pronasale ant</th>
  </tr>
  <tr>
    <th>Literature</th>
    <th>Ancestry</th>
    <th>Biological Sex</th>
    <th>Full Equation</th>
    <th>Name of Measurement</th>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>ANY</td>
    <td>All</td>
    <td>pred Rynn PA = 0.83 × Y − 3.5</td>
    <td>pred Rynn PA</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Males</td>
    <td>pred Sarilita M PA = 0.57 × Y + 2.33</td>
    <td>pred Sarilita M PA</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Females</td>
    <td>pred Bulut F PA = 2.711 + 0.681 × Y</td>
    <td>pred Bulut F PA</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Males</td>
    <td>pred Bulut M PA = −0.481 + 0.776 × Y</td>
    <td>pred Bulut M PA</td>
  </tr>
</table>

<details>
<summary>GUI for pronasale anterior</summary>

```python
# === BEGIN SCRIPT FOR SLICER PYTHON INTERACTOR ===

# --- Logging/report system ---
markup_report_log = []

def add_to_markup_report(markup_type, markup_name, user_choices):
    markup_report_log.append({
        "type": markup_type,
        "name": markup_name,
        "choices": user_choices.copy()
    })

def print_markup_report():
    print("=== Markup Creation Report ===")
    for i, entry in enumerate(markup_report_log, 1):
        print(f"\n{i}. {entry['type']} '{entry['name']}'")
        for label, choice in entry['choices'].items():
            print(f"   {label}: {choice}")
    print("=============================")

import slicer
import numpy as np
from qt import QPushButton, QVBoxLayout, QWidget, QCheckBox, QLabel, QSizePolicy, Qt

# --- Function to create a new line in Slicer ---
def create_line(name, length, color, start_point, direction):
    line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
    line.GetDisplayNode().SetSelectedColor(color)
    start_point = np.array(start_point)
    direction = np.array(direction)
    line.AddControlPoint(start_point.tolist())
    end_point = start_point + direction * length
    line.AddControlPoint(end_point.tolist())
    return line

def calculate_length(equation, Y):
    if equation == "pred Rynn PA":
        return 0.83 * Y - 3.5
    elif equation == "pred Sarilita M PA":
        return 0.57 * Y + 2.33
    elif equation == "pred Bulut F PA":
        return 2.711 + 0.681 * Y
    elif equation == "pred Bulut M PA":
        return -0.481 + 0.776 * Y
    else:
        raise ValueError("Invalid equation choice")

def create_new_line_with_equation(equation):
    print("Inside create_new_line_with_equation function")
    rynn_hard_tissue = slicer.util.getNode("Rynn_hard_tissue")
    line_1 = slicer.util.getNode("1")
    rhi_subs_Y = slicer.util.getNode("rhi-subs Y")

    start_point = rynn_hard_tissue.GetNthControlPointPosition(0)
    direction = np.array(line_1.GetNthControlPointPosition(1)) - np.array(line_1.GetNthControlPointPosition(0))
    direction = direction / np.linalg.norm(direction)
    direction = -direction  # Reverse the direction

    point1 = np.array(rhi_subs_Y.GetNthControlPointPosition(0))
    point2 = np.array(rhi_subs_Y.GetNthControlPointPosition(1))
    Y = np.linalg.norm(point2 - point1)
    length = calculate_length(equation, Y)
    purple = (0.5, 0.0, 0.5)
    new_line = create_line(equation, length, purple, start_point, direction)
    print(f"Line '{equation}' created with length: {length:.2f}")

    # --- LOGGING: record this creation ---
    user_choices = {
        "Equation": equation,
        "Y distance": f"{Y:.2f}",
        "Line length": f"{length:.2f}"
    }
    add_to_markup_report("Line", equation, user_choices)

# --- The Line Creation GUI ---
class LineCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pronasale Anterior Prediction")
        layout = QVBoxLayout()
        title_label = QLabel("<b>Please choose the equation(s) for pronasale anterior prediction!</b>")
        layout.addWidget(title_label)

        description_html = """
        <table border="1" cellspacing="0" cellpadding="3">
            <tr>
                <th>Literature</th>
                <th>Ancestry</th>
                <th>Biological Sex</th>
                <th>Full Equation</th>
                <th>Name of Output Measurement</th>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>ANY</td>
                <td>All</td>
                <td>pred Rynn PA = 0.83 × Y − 3.5</td>
                <td>pred Rynn PA</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Males</td>
                <td>pred Sarilita M PA = 0.57 × Y + 2.33</td>
                <td>pred Sarilita M PA</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Females</td>
                <td>pred Bulut F PA = 2.711 + 0.681 × Y</td>
                <td>pred Bulut F PA</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Males</td>
                <td>pred Bulut M PA = −0.481 + 0.776 × Y</td>
                <td>pred Bulut M PA</td>
            </tr>
        </table>
        """
        description_label = QLabel()
        description_label.setText(description_html)
        description_label.setWordWrap(True)
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(description_label)

        self.equations = [
            "pred Rynn PA",
            "pred Sarilita M PA",
            "pred Bulut F PA",
            "pred Bulut M PA"
        ]
        self.checkbox_list = []
        for eq in self.equations:
            checkbox = QCheckBox(eq)
            layout.addWidget(checkbox)
            self.checkbox_list.append(checkbox)

        create_button = QPushButton("Create Line(s)")
        create_button.clicked.connect(self.on_create_button_clicked)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def on_create_button_clicked(self):
        print("Inside on_create_button_clicked method")
        chosen_equations = [eq for eq, cb in zip(self.equations, self.checkbox_list) if cb.isChecked()]
        if chosen_equations:
            for chosen_equation in chosen_equations:
                print(f"Chosen equation: {chosen_equation}")
                try:
                    create_new_line_with_equation(chosen_equation)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print("No equation selected!")

# --- Create and show the GUI ---
line_creation_widget = LineCreationWidget()
line_creation_widget.show()

# --- Always-on-top PRINT REPORT button widget ---
class MarkupReportWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markup Report Printer")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout()
        print_button = QPushButton("Print Markup Report")
        print_button.clicked.connect(print_markup_report)
        layout.addWidget(print_button)
        self.setLayout(layout)

# Ensure only one instance
try:
    markup_report_widget.close()
except:
    pass
markup_report_widget = MarkupReportWidget()
markup_report_widget.show()

# === END SCRIPT ===
```
</details>

### Calculating & applying the predicted length of the pronasale vertical
 The predicted length of the **pronasale vertical** will be measured from the endpoint of the pronasale anterior (if you have multiple, you may need to repeat a step!) its orientation is set to be parallel to line "2" and the length is calculated according to your chosen regression formulae.  As there are different revised methods available, the code below will offer you to choose the option(s) by which the pronasale vertical distance is calculated - and from which pronasale anterior, if you have multiple. Make sure you select the correct pairing.  All lines generated by this code will be **yellow** in the environment. The endpoint of the new yellow line will be added to a new node called "Rynn_soft_tissue_pred", with a prefix of the equations used to obtain it.
Please make sure you document which method you used and why - the naming convention of the new line(s) will help jog your memory. The video shows what to expect when running the code. The table below is a quick summary, please refer to the original studies [^3], [^12], [^13] for explanation.


https://github.com/user-attachments/assets/f40a61ad-a615-4f46-80f0-1f897f134b35


<table>
  <tr>
    <th colspan="5" style="text-align:center">Pronasale vert</th>
  </tr>
  <tr>
    <th>Literature</th>
    <th>Ancestry</th>
    <th>Biological Sex</th>
    <th>Full Equation</th>
    <th>Name of Measurement</th>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>ANY</td>
    <td>All</td>
    <td>pred Rynn PV = 0.9 × X − 2</td>
    <td>pred Rynn PV</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Males</td>
    <td>pred Sarilita M PV = 0.88 × X + 0.68</td>
    <td>pred Sarilita M PV</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Females</td>
    <td>pred Bulut F PV = 5.501 + 0.779 × X</td>
    <td>pred Bulut F PV</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Males</td>
    <td>pred Bulut M PV = −3.53 + 0.954 × X</td>
    <td>pred Bulut M PV</td>
  </tr>
</table>

<details>

<summary>GUI for pronasale vertical</summary>

``` python
import slicer
import numpy as np
from qt import QPushButton, QVBoxLayout, QWidget, QCheckBox, QLabel, QMessageBox, QSizePolicy

def find_pa_lines():
    all_nodes = slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode")
    return [node for node in all_nodes if node.GetName().endswith("PA")]

def find_x_line():
    all_nodes = slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode")
    for node in all_nodes:
        if node.GetName() == "nas-aca X":
            return node
    return None

def find_line_2():
    all_nodes = slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode")
    for node in all_nodes:
        if node.GetName() == "2":
            return node
    return None

def get_line_endpoints(line_node):
    start = np.array(line_node.GetNthControlPointPosition(0))
    end = np.array(line_node.GetNthControlPointPosition(1))
    return start, end

def get_line_length(line_node):
    start, end = get_line_endpoints(line_node)
    return np.linalg.norm(end - start)

def calculate_pv_length(equation, X):
    if equation == "pred Rynn PV":
        return 0.9 * X - 2
    elif equation == "pred Sarilita M PV":
        return 0.88 * X + 0.68
    elif equation == "pred Bulut F PV":
        return 5.501 + 0.779 * X
    elif equation == "pred Bulut M PV":
        return -3.53 + 0.954 * X
    else:
        raise ValueError("Invalid equation name")

def abbreviate_equation_name(eq):
    eq = eq.replace("pred ", "").replace(" ", "")
    eq = eq.replace("MPV", "M-PV").replace("FPV", "F-PV")
    return eq

def create_parallel_line_to_2(pa_line_node, x_line_node, pv_equation, pa_equation):
    end = get_line_endpoints(pa_line_node)[1]
    line2_node = find_line_2()
    if line2_node is None:
        raise ValueError("No line named '2' found in the scene!")
    line2_start, line2_end = get_line_endpoints(line2_node)
    direction = line2_end - line2_start
    norm_dir = np.linalg.norm(direction)
    if norm_dir == 0:
        raise ValueError("Line '2' has zero length!")
    direction = direction / norm_dir
    direction = -direction

    X = get_line_length(x_line_node)
    length = calculate_pv_length(pv_equation, X)

    yellow = (1.0, 1.0, 0.0)
    pa_abbrev = abbreviate_equation_name(pa_equation)
    pv_abbrev = abbreviate_equation_name(pv_equation)
    node_name = f"{pa_abbrev}_{pv_abbrev}_pronasale pred"
    new_line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", node_name)
    new_line.GetDisplayNode().SetSelectedColor(yellow)
    new_line.AddControlPoint(end.tolist())
    new_line.AddControlPoint((end + direction * length).tolist())
    print(f"Created new line '{node_name}' of length {length:.2f}, parallel to line '2'")

    # --- ADD TO LOG ---
    # If add_to_markup_report is defined globally, this will work:
    try:
        user_choices = {
            "PA line": pa_equation,
            "PV equation": pv_equation,
            "X (length of nas-aca X)": f"{X:.2f}",
            "PV line length": f"{length:.2f}"
        }
        add_to_markup_report("Line (PV parallel)", node_name, user_choices)
    except Exception as e:
        print(f"[LOGGING ERROR] {e}")
    return new_line

def save_pv_endpoint_to_pred_list(pv_line_node, pa_equation, pv_equation):
    try:
        pred_node = slicer.util.getNode("Rynn_soft_tissue_pred")
    except slicer.util.MRMLNodeNotFoundException:
        pred_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "Rynn_soft_tissue_pred")
    endpoint = pv_line_node.GetNthControlPointPosition(1)
    pa_abbrev = abbreviate_equation_name(pa_equation)
    pv_abbrev = abbreviate_equation_name(pv_equation)
    label_name = f"{pa_abbrev}_{pv_abbrev}_pronasale pred"
    pred_node.AddControlPoint(endpoint, label_name)
    print(f"Added PV endpoint as fiducial: {label_name} at {endpoint}")

class PVLineCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pronasale Vertical Prediction (PV) [Parallel to line '2']")
        layout = QVBoxLayout()
        title_label = QLabel("<b>Select PA line(s), then PV equation(s) to create lines parallel to line '2'!<br>(X line is always 'nas-aca X')</b>")
        layout.addWidget(title_label)

        description_html = """
        <table border="1" cellspacing="0" cellpadding="3">
            <tr>
                <th>Literature</th>
                <th>Ancestry</th>
                <th>Biological Sex</th>
                <th>Full equation</th>
                <th>Name of measurement in scene</th>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>ANY</td>
                <td>All</td>
                <td>pred Rynn PV = 0.9 × X − 2</td>
                <td>pred Rynn PV</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Males</td>
                <td>pred Sarilita M PV = 0.88 × X + 0.68</td>
                <td>pred Sarilita M PV</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Females</td>
                <td>pred Bulut F PV = 5.501 + 0.779 × X</td>
                <td>pred Bulut F PV</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Males</td>
                <td>pred Bulut M PV = −3.53 + 0.954 × X</td>
                <td>pred Bulut M PV</td>
            </tr>
        </table>
        """
        description_label = QLabel()
        description_label.setText(description_html)
        description_label.setWordWrap(True)
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(description_label)

        self.pa_lines = find_pa_lines()
        self.pa_checkboxes = []

        if len(self.pa_lines) == 0:
            layout.addWidget(QLabel("No PA lines found in the scene."))
        else:
            pa_label = QLabel("Select PA line(s):")
            layout.addWidget(pa_label)
            for node in self.pa_lines:
                checkbox = QCheckBox(node.GetName())
                layout.addWidget(checkbox)
                self.pa_checkboxes.append((checkbox, node))

        pv_label = QLabel("Select PV equations:")
        layout.addWidget(pv_label)
        self.equations = [
            "pred Rynn PV",
            "pred Sarilita M PV",
            "pred Bulut F PV",
            "pred Bulut M PV"
        ]
        self.checkbox_list = []
        for eq in self.equations:
            checkbox = QCheckBox(eq)
            layout.addWidget(checkbox)
            self.checkbox_list.append((checkbox, eq))

        create_button = QPushButton("Create Line(s) Parallel to '2'")
        create_button.clicked.connect(self.on_create_button_clicked)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def on_create_button_clicked(self):
        selected_pa_lines = [node for cb, node in self.pa_checkboxes if cb.isChecked()]
        if not selected_pa_lines:
            QMessageBox.warning(self, "Selection Error", "Please select at least one PA line.")
            return

        x_line_node = find_x_line()
        if x_line_node is None:
            QMessageBox.warning(self, "Selection Error", "No line named 'nas-aca X' found in the scene.")
            return

        chosen_equations = [eq for cb, eq in self.checkbox_list if cb.isChecked()]
        if not chosen_equations:
            QMessageBox.warning(self, "Selection Error", "Please select at least one PV equation.")
            return

        for pa_line_node in selected_pa_lines:
            pa_equation = pa_line_node.GetName()
            for pv_eq in chosen_equations:
                try:
                    pv_line_node = create_parallel_line_to_2(pa_line_node, x_line_node, pv_eq, pa_equation)
                    save_pv_endpoint_to_pred_list(pv_line_node, pa_equation, pv_eq)
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

widget = PVLineCreationWidget()
widget.show()
```
</details>


## Estimating the pFHP

The line(s) created via the **GUI for pFHP** code will appear in **turquoise**, named according to the linear regression used and all will run from the subspinale point along the "3" line. The length is calculated by your chosen linear regression. Below the table summarises the options, please refer back to the original literature[^3], [^12], [^13]  if in doubt. 
After this, the code **GUI for sn** finds the intersection point on the previous turqoise line with the chosen nasal depth equation distance from the predicted pronasale point. 

<table>
  <tr>
    <th colspan="5" style="text-align:center">Pronasale FHP</th>
  </tr>
  <tr>
    <th>Literature</th>
    <th>Ancestry</th>
    <th>Biological Sex</th>
    <th>Full Equation</th>
    <th>Name of Measurement</th>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>ANY</td>
    <td>All</td>
    <td>pred Rynn pFHP = 0.93 × Y − 6</td>
    <td>pred Rynn pFHP</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Males</td>
    <td>pred Sarilita M pFHP = 0.58 × Y + 4.55</td>
    <td>pred Sarilita M pFHP</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Females</td>
    <td>pred Bulut F pFHP = 1.161 + 0.775 × Y</td>
    <td>pred Bulut F pFHP</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Males</td>
    <td>pred Bulut M pFHP = 0.518 + 0.777 × Y</td>
    <td>pred Bulut M pFHP</td>
  </tr>
</table>


<table>
  <tr>
    <th colspan="5" style="text-align:center">Nasal Depth</th>
  </tr>
  <tr>
    <th>Literature</th>
    <th>Ancestry</th>
    <th>Biological Sex</th>
    <th>Full Equation</th>
    <th>Name of Measurement</th>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>ANY</td>
    <td>Females</td>
    <td>pred Rynn F ND = 0.5 × Y + 1.5</td>
    <td>pred Rynn F ND</td>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>ANY</td>
    <td>Males</td>
    <td>pred Rynn M ND = 0.4 × Y + 5</td>
    <td>pred Rynn M ND</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Males</td>
    <td>pred Sarilita M ND = 0.22 × Z + 4.02</td>
    <td>pred Sarilita M ND</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Females</td>
    <td>pred Sarilita F ND = 0.29 × Y + 6.24</td>
    <td>pred Sarilita F ND</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Females</td>
    <td>pred Bulut F ND = 5,169 + 0,423 × Y</td>
    <td>pred Bulut F ND</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Males</td>
    <td>pred Bulut M ND = 6,587 + 0,386 × Y</td>
    <td>pred Bulut M ND</td>
  </tr>
</table>


<details>

<summary>GUI for pFHP</summary>

```python
import slicer
import numpy as np
from qt import QPushButton, QVBoxLayout, QWidget, QCheckBox, QLabel, QMessageBox, QSizePolicy

def find_line_by_name(line_name):
    for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode"):
        if node.GetName() == line_name:
            return node
    return None

def get_nth_point(node, n):
    return np.array(node.GetNthControlPointPosition(n))

def get_line_endpoints(line_node):
    start = get_nth_point(line_node, 0)
    end = get_nth_point(line_node, 1)
    return start, end

def get_line_length(line_node):
    start, end = get_line_endpoints(line_node)
    return np.linalg.norm(end - start)

def calculate_pfhp_length(equation, Y):
    if equation == "pred Rynn pFHP":
        return 0.93 * Y - 6
    elif equation == "pred Sarilita M pFHP":
        return 0.58 * Y + 4.55
    elif equation == "pred Bulut F pFHP":
        return 1.161 + 0.775 * Y
    elif equation == "pred Bulut M pFHP":
        return 0.518 + 0.777 * Y
    else:
        raise ValueError("Invalid equation name")

def abbreviate_equation_name(eq):
    eq = eq.replace("pred ", "").replace(" ", "")
    eq = eq.replace("MpFHP", "M-pFHP").replace("FpFHP", "F-pFHP")
    return eq

def create_turquoise_line(start_point, direction, length, line_name):
    turquoise = (0, 1, 1)
    new_line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", line_name)
    new_line.GetDisplayNode().SetSelectedColor(turquoise)
    new_line.AddControlPoint(start_point.tolist())
    new_line.AddControlPoint((start_point + direction * length).tolist())
    print(f"Created turquoise line '{line_name}' with length {length:.2f}")
    return new_line

class PFHPLineCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prediction of pFHP (Parallel to line '3', reversed direction)")

        layout = QVBoxLayout()
        title_label = QLabel(
            "<b>Select pFHP equation(s) to create turquoise lines parallel to (reversed) line '3'<br>"
            "Start point is position 4 in 'Rynn_hard_tissue', Y is the length of 'rhi-subs Y'</b>"
        )
        layout.addWidget(title_label)

        description_html = """
        <table border="1" cellspacing="0" cellpadding="3">
            <tr>
                <th>Literature</th>
                <th>Ancestry</th>
                <th>Biological Sex</th>
                <th>Full equation</th>
                <th>Name of measurement in scene</th>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>ANY</td>
                <td>All</td>
                <td>pred Rynn pFHP = 0.93 × Y − 6</td>
                <td>pred Rynn pFHP</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Males</td>
                <td>pred Sarilita M pFHP = 0.58 × Y + 4.55</td>
                <td>pred Sarilita M pFHP</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Females</td>
                <td>pred Bulut F pFHP = 1.161 + 0.775 × Y</td>
                <td>pred Bulut F pFHP</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Males</td>
                <td>pred Bulut M pFHP = 0.518 + 0.777 × Y</td>
                <td>pred Bulut M pFHP</td>
            </tr>
        </table>
        """
        description_label = QLabel()
        description_label.setText(description_html)
        description_label.setWordWrap(True)
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(description_label)

        self.equations = [
            "pred Rynn pFHP",
            "pred Sarilita M pFHP",
            "pred Bulut F pFHP",
            "pred Bulut M pFHP"
        ]
        self.checkbox_list = []
        for eq in self.equations:
            checkbox = QCheckBox(eq)
            layout.addWidget(checkbox)
            self.checkbox_list.append((checkbox, eq))

        create_button = QPushButton("Create Turquoise Line(s)")
        create_button.clicked.connect(self.on_create_button_clicked)
        layout.addWidget(create_button)
        self.setLayout(layout)

    def on_create_button_clicked(self):
        chosen_equations = [eq for cb, eq in self.checkbox_list if cb.isChecked()]
        if not chosen_equations:
            QMessageBox.warning(self, "Selection Error", "Please select at least one pFHP equation.")
            return

        rynn_hard_tissue = slicer.util.getNode("Rynn_hard_tissue") if slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode") else None
        if not rynn_hard_tissue:
            QMessageBox.warning(self, "Missing Node", "No node named 'Rynn_hard_tissue' found in the scene.")
            return
        line_3 = find_line_by_name("3")
        if not line_3:
            QMessageBox.warning(self, "Missing Node", "No line named '3' found in the scene.")
            return
        rhi_subs_Y = find_line_by_name("rhi-subs Y")
        if not rhi_subs_Y:
            QMessageBox.warning(self, "Missing Node", "No line named 'rhi-subs Y' found in the scene.")
            return

        try:
            start_point = get_nth_point(rynn_hard_tissue, 4)
        except Exception:
            QMessageBox.warning(self, "Error", "Could not get position 4 from 'Rynn_hard_tissue'.")
            return

        line3_start, line3_end = get_line_endpoints(line_3)
        direction = line3_end - line3_start
        norm = np.linalg.norm(direction)
        if norm == 0:
            QMessageBox.warning(self, "Error", "Line '3' has zero length!")
            return
        direction = -direction / norm  # REVERSED direction

        Y = get_line_length(rhi_subs_Y)

        for equation in chosen_equations:
            try:
                length = calculate_pfhp_length(equation, Y)
                abbrev = abbreviate_equation_name(equation)
                line_name = abbrev
                new_line = create_turquoise_line(start_point, direction, length, line_name)

                # --- LOGGING: record this creation ---
                try:
                    user_choices = {
                        "Equation": equation,
                        "Y distance": f"{Y:.2f}",
                        "Line length": f"{length:.2f}",
                        "Start point index": 4,
                        "Direction ref line": "3 (reversed)"
                    }
                    add_to_markup_report("Line (pFHP parallel)", line_name, user_choices)
                except Exception as logerr:
                    print(f"[LOGGING ERROR] {logerr}")

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

widget = PFHPLineCreationWidget()
widget.show()
```
</details>






<details>
<summary>GUI for sn point</summary>
 
```python
import slicer
import numpy as np
from qt import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox, QButtonGroup, QSizePolicy

def get_pronasale_pred_points():
    points = []
    node = slicer.util.getNode("Rynn_soft_tissue_pred")
    for idx in range(node.GetNumberOfControlPoints()):
        label = node.GetNthControlPointLabel(idx)
        if "pronasale pred" in label:
            points.append((label, idx, np.array(node.GetNthControlPointPosition(idx))))
    return points

def get_pfph_lines():
    lines = []
    for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode"):
        if "pFHP" in node.GetName():
            lines.append(node)
    return lines

def get_line_length(line_name):
    line = slicer.util.getNode(line_name)
    p0 = np.array(line.GetNthControlPointPosition(0))
    p1 = np.array(line.GetNthControlPointPosition(1))
    return np.linalg.norm(p1 - p0)

def calculate_radius(equation, Y, Z):
    if equation == "pred Rynn F ND":
        return 0.5 * Y + 1.5
    elif equation == "pred Rynn M ND":
        return 0.4 * Y + 5
    elif equation == "pred Sarilita M ND":
        return 0.22 * Z + 4.02
    elif equation == "pred Sarilita F ND":
        return 0.29 * Y + 6.24
    elif equation == "pred Bulut F ND":
        return 5.169 + 0.423 * Y
    elif equation == "pred Bulut M ND":
        return 6.587 + 0.386 * Y
    else:
        raise ValueError("Unknown equation")

def abbreviate_equation_name(eq):
    eq = eq.replace("pred ", "").replace(" ", "")
    eq = eq.replace("MND", "M-ND").replace("FND", "F-ND")
    return eq

def create_nd_circle_node(center, radius, planeNormal):
    circle = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsShapeNode", "ND_circle")
    circle.SetShapeName(4)  # 4 is the index for "Ring" shape in ExtraMarkups
    circle.RemoveAllControlPoints()
    circle.AddControlPoint(center)
    norm_pt = center + planeNormal  # Second control point defines the normal
    circle.AddControlPoint(norm_pt.tolist())
    circle.SetAttribute("Shape.Radius", str(radius))
    circle.GetDisplayNode().SetLineThickness(0.5)  # Set circle thickness
    return circle

def line_circle_intersection_in_plane(center, radius, line_p0, line_p1, plane_normal):
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    if np.allclose(plane_normal, [0, 0, 1]):
        u = np.array([1, 0, 0])
    else:
        u = np.cross([0, 0, 1], plane_normal)
        u = u / np.linalg.norm(u)
    v = np.cross(plane_normal, u)
    v = v / np.linalg.norm(v)
    def to_plane_coords(pt):
        rel = pt - center
        return np.dot(rel, u), np.dot(rel, v)
    p0_plane = np.array(to_plane_coords(np.array(line_p0)))
    p1_plane = np.array(to_plane_coords(np.array(line_p1)))
    dp = p1_plane - p0_plane
    a = np.dot(dp, dp)
    b = 2 * np.dot(p0_plane, dp)
    c = np.dot(p0_plane, p0_plane) - radius ** 2
    disc = b ** 2 - 4 * a * c
    if disc < 0:
        return []
    sqrt_disc = np.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    pts = []
    for t in [t1, t2]:
        if 0.0 <= t <= 1.0:
            plane_xy = p0_plane + t * dp
            pt3d = center + plane_xy[0] * u + plane_xy[1] * v
            pts.append(pt3d)
    return pts

def project_point_to_line(point, line_p0, line_p1):
    line_vec = np.array(line_p1) - np.array(line_p0)
    line_len = np.linalg.norm(line_vec)
    if line_len == 0:
        return np.array(line_p0)
    line_vec_norm = line_vec / line_len
    point_vec = np.array(point) - np.array(line_p0)
    proj_length = np.dot(point_vec, line_vec_norm)
    proj_length = np.clip(proj_length, 0, line_len)  # Clamp to line segment
    proj_point = np.array(line_p0) + proj_length * line_vec_norm
    return proj_point

class NDIntersectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ND Circle and pFHP Line Intersection (Soft Tissue ND)")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>1. Choose pronasale pred point (as ND circle center):</b>"))
        self.points = get_pronasale_pred_points()
        self.point_buttons = QButtonGroup(self)
        for i, (label, idx, pos) in enumerate(self.points):
            radio = QRadioButton(f"{label} at {np.round(pos,2)}")
            self.point_buttons.addButton(radio, i)
            layout.addWidget(radio)
        if not self.points:
            layout.addWidget(QLabel("No pronasale pred points found."))

        # --- Add the description table here ---
        table_html = """
        <b>ND equations from literature:</b>
        <table border="1" cellspacing="0" cellpadding="3">
            <tr>
                <th>Literature</th>
                <th>Ancestry</th>
                <th>Biological Sex</th>
                <th>Full equation</th>
                <th>Name of measurement in scene</th>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>ANY</td>
                <td>Females</td>
                <td>pred Rynn F ND=0.5*Y + 1.5</td>
                <td>pred Rynn F ND</td>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>ANY</td>
                <td>Males</td>
                <td>pred Rynn M ND=0.4*Y + 5</td>
                <td>pred Rynn M ND</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Males</td>
                <td>pred Sarilita M ND=0.22*Z + 4.02</td>
                <td>pred Sarilita M ND</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Females</td>
                <td>pred Sarilita F ND=0.29 × Y + 6.24</td>
                <td>pred Sarilita F ND</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Females</td>
                <td>pred Bulut F ND=5,169 + 0,423*Y</td>
                <td>pred Bulut F ND</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Males</td>
                <td>pred Bulut M ND=6,587 + 0,386*Y</td>
                <td>pred Bulut M ND</td>
            </tr>
        </table>
        """
        description_label = QLabel()
        description_label.setText(table_html)
        description_label.setWordWrap(True)
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(description_label)

        layout.addWidget(QLabel("<b>2. Choose ND radius equation:</b>"))
        self.equations = [
            "pred Rynn F ND", "pred Rynn M ND",
            "pred Sarilita M ND", "pred Sarilita F ND",
            "pred Bulut F ND", "pred Bulut M ND"
        ]
        self.equation_buttons = QButtonGroup(self)
        for i, eq in enumerate(self.equations):
            radio = QRadioButton(eq)
            self.equation_buttons.addButton(radio, i)
            layout.addWidget(radio)

        layout.addWidget(QLabel("<b>3. Choose pFHP line to intersect with:</b>"))
        self.lines = get_pfph_lines()
        self.line_buttons = QButtonGroup(self)
        for i, line in enumerate(self.lines):
            radio = QRadioButton(line.GetName())
            self.line_buttons.addButton(radio, i)
            layout.addWidget(radio)
        if not self.lines:
            layout.addWidget(QLabel("No pFHP lines found."))

        self.create_button = QPushButton("Create ND Circle and Find Intersection")
        self.create_button.clicked.connect(self.on_create)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def on_create(self):
        center_id = self.point_buttons.checkedId()
        if center_id == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a pronasale pred point.")
            return
        center_label, center_idx, center = self.points[center_id]
        eq_id = self.equation_buttons.checkedId()
        if eq_id == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a ND radius equation.")
            return
        equation = self.equations[eq_id]
        line_id = self.line_buttons.checkedId()
        if line_id == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a pFHP line.")
            return
        line_node = self.lines[line_id]
        line_p0 = np.array(line_node.GetNthControlPointPosition(0))
        line_p1 = np.array(line_node.GetNthControlPointPosition(1))
        try:
            y_len = get_line_length("rhi-subs Y")
        except Exception as e:
            QMessageBox.warning(self, "Missing line", "Could not find or read 'rhi-subs Y'.")
            return
        try:
            z_len = get_line_length("nas-subs Z")
        except Exception:
            z_len = 0
        try:
            radius = calculate_radius(equation, y_len, z_len)
        except Exception as e:
            QMessageBox.warning(self, "Equation error", str(e))
            return

        # Get normal from the INB plane
        try:
            inb_plane = slicer.util.getNode("INB")
            planeNormal = np.array(inb_plane.GetNormal())
        except Exception:
            QMessageBox.warning(self, "Missing INB", "Could not find 'INB' plane in the scene.")
            return

        # Create the ND Circle using MarkupsShapeNode (on INB plane)
        nd_circle_node = create_nd_circle_node(center, radius, planeNormal)
        # Thickness already set in create_nd_circle_node

        # Find intersection(s) in the INB plane
        intersections = line_circle_intersection_in_plane(center, radius, line_p0, line_p1, planeNormal)
        if not intersections:
            QMessageBox.warning(self, "No Intersection", "No intersection found between ND circle and line.")
            return

        # Project intersection(s) onto the actual 3D line so the fiducials are on the line
        projected_intersections = [project_point_to_line(pt, line_p0, line_p1) for pt in intersections]

        # Add intersection(s) as new fiducial(s) to Rynn_soft_tissue_pred, and draw ND line(s)
        try:
            pred_node = slicer.util.getNode("Rynn_soft_tissue_pred")
        except slicer.util.MRMLNodeNotFoundException:
            pred_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "Rynn_soft_tissue_pred")
        pa_abbrev = abbreviate_equation_name(center_label.split("_pronasale")[0])
        eq_abbrev = abbreviate_equation_name(equation)
        label = f"{pa_abbrev}_{eq_abbrev}_sn pred"
        for i, pt in enumerate(projected_intersections):
            lbl = label if len(projected_intersections)==1 else f"{label}_{i+1}"
            pred_node.AddControlPoint(pt.tolist(), lbl)

            # Create visual line from ND circle center to intersection, labeled "ND line + abbreviated choices"
            line_lbl = f"ND_line_{pa_abbrev}_{eq_abbrev}" if len(projected_intersections) == 1 else f"ND_line_{pa_abbrev}_{eq_abbrev}_{i+1}"
            nd_line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", line_lbl)
            nd_line_node.AddControlPoint(center.tolist())
            nd_line_node.AddControlPoint(pt.tolist())
            nd_line_node.GetDisplayNode().SetSelectedColor(0.2, 0.6, 1.0)  # Example: light blue
            nd_line_node.GetDisplayNode().SetLineThickness(0.5)

        QMessageBox.information(self, "Done", f"ND circle, intersection(s), and ND line(s) created!\nLabel: {label}")

widget = NDIntersectionWidget()
widget.show()
```

</details>


#### Estimating and placing the nasal depth and nasal length measurements to estimate the soft tissue nasion

 This script draws two circles: 

1. the **NH circle**: its centre is the predicted subnasale and its radius is calculated by the following nasal height equations: 

<table>
  <tr>
    <th colspan="5" style="text-align:center">Nasal height</th>
  </tr>
  <tr>
    <th>Literature</th>
    <th>Ancestry</th>
    <th>Biological Sex</th>
    <th>Full Equation</th>
    <th>Name of Measurement</th>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>European</td>
    <td>Males</td>
    <td>pred Rynn EA M NH = 0.78 × Z + 9.5</td>
    <td>pred Rynn EA M NH</td>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>European</td>
    <td>Females</td>
    <td>pred Rynn EA F NH = 0.63 × Z + 17</td>
    <td>pred Rynn EA F NH</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Males</td>
    <td>pred Sarilita M NH = 0.79 × Z + 3.74</td>
    <td>pred Sarilita M NH</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Females</td>
    <td>pred Sarilita F NH = 0.69 × X + 12.36</td>
    <td>pred Sarilita F NH</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Females</td>
    <td>pred Bulut F NH = 15.047 + 0.687 × Z</td>
    <td>pred Bulut F NH</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Males</td>
    <td>pred Bulut M NH = 9.858 + 0.784 × Z</td>
    <td>pred Bulut M NH</td>
  </tr>
</table>


2. the **NL circle**: its centre is the predicted pronasale and its radius is calculated by the following nasal length equations: 
<table>
  <tr>
    <th colspan="5" style="text-align:center">Nasal length</th>
  </tr>
  <tr>
    <th>Literature</th>
    <th>Ancestry</th>
    <th>Biological Sex</th>
    <th>Full Equation</th>
    <th>Name of Measurement</th>
  </tr>
  <tr>
    <td>Rynn et al. 2010</td>
    <td>European</td>
    <td>All</td>
    <td>pred Rynn EA NL = 0.74 × Z + 3.5</td>
    <td>pred Rynn EA NL</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Females</td>
    <td>pred Sarilita F NL = 6.624 + 0.71 × Z</td>
    <td>pred Sarilita F NL</td>
  </tr>
  <tr>
    <td>Bulut et al. 2019</td>
    <td>Turkish</td>
    <td>Males</td>
    <td>pred Sarilita M NL = 0.764 + 0.807 × Z</td>
    <td>pred Sarilita M NL</td>
  </tr>
  <tr>
    <td>Sarilita et al. 2018</td>
    <td>Indonesian</td>
    <td>Males</td>
    <td>pred Bulut M NL = 0.66 × X + 7.77</td>
    <td>pred Bulut M NL</td>
  </tr>
</table>
 
These circles would normally (if not concentric/only touching) intersect in two places, but only the intersection point closest to line 1 will be displayed (line 1 stems from the hard tissue nasion). 


<details>

<summary>GUI for soft tissue nasion </summary>

``` python
import slicer
import numpy as np
from qt import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox, QButtonGroup, QSizePolicy

def get_points_by_label_substring(substring):
    node = slicer.util.getNode("Rynn_soft_tissue_pred")
    points = []
    for idx in range(node.GetNumberOfControlPoints()):
        label = node.GetNthControlPointLabel(idx)
        if substring in label:
            points.append((label, np.array(node.GetNthControlPointPosition(idx))))
    return points

def get_line_length(line_name):
    try:
        line = slicer.util.getNode(line_name)
        p0 = np.array(line.GetNthControlPointPosition(0))
        p1 = np.array(line.GetNthControlPointPosition(1))
        return np.linalg.norm(p1 - p0)
    except Exception:
        return 0

def calculate_nh_radius(equation, X, Y, Z):
    if equation == "pred Rynn EA M NH":
        return 0.78 * Z + 9.5
    elif equation == "pred Rynn EA F NH":
        return 0.63 * Z + 17
    elif equation == "pred Sarilita M NH":
        return 0.79 * Z + 3.74
    elif equation == "pred Sarilita F NH":
        return 0.69 * X + 12.36
    elif equation == "pred Bulut F NH":
        return 15.047 + 0.687 * Z
    elif equation == "pred Bulut M NH":
        return 9.858 + 0.784 * Z
    else:
        raise ValueError("Unknown NH equation")

def calculate_nl_radius(equation, X, Z):
    if equation == "pred Rynn EA NL":
        return 0.74 * Z + 3.5
    elif equation == "pred Sarilita F NL":
        return 6.624 + 0.71 * Z
    elif equation == "pred Sarilita M NL":
        return 0.764 + 0.807 * Z
    elif equation == "pred Bulut M NL":
        return 0.66 * X + 7.77
    else:
        raise ValueError("Unknown NL equation")

def abbreviate_equation_name(eq):
    eq = eq.replace("pred ", "").replace(" ", "")
    eq = eq.replace("MNH", "M-NH").replace("FNH", "F-NH")
    eq = eq.replace("MNL", "M-NL").replace("FNL", "F-NL")
    eq = eq.replace("EA", "EA").replace("Sarilita", "Sarilita").replace("Bulut", "Bulut")
    return eq

def abbreviate_point_label(label):
    label = label.replace(" ", "_")
    return label

def create_circle_node(center, radius, planeNormal, name, color=(1.0,0.0,0.0)):
    circle = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsShapeNode", name)
    circle.SetShapeName(4)  # 4 = "Ring"
    circle.RemoveAllControlPoints()
    circle.AddControlPoint(center)
    norm_pt = center + planeNormal
    circle.AddControlPoint(norm_pt.tolist())
    circle.SetAttribute("Shape.Radius", str(radius))
    display = circle.GetDisplayNode()
    display.SetLineThickness(0.5)
    display.SetColor(*color)
    return circle

def find_circle_circle_intersections(c1, r1, c2, r2, planeNormal):
    planeNormal = np.array(planeNormal) / np.linalg.norm(planeNormal)
    if np.allclose(planeNormal, [0,0,1]):
        u = np.array([1,0,0])
    else:
        u = np.cross([0,0,1], planeNormal)
        u = u / np.linalg.norm(u)
    v = np.cross(planeNormal, u)
    v = v / np.linalg.norm(v)
    c1_in_plane = np.array([np.dot(c1, u), np.dot(c1, v)])
    c2_in_plane = np.array([np.dot(c2, u), np.dot(c2, v)])
    d = np.linalg.norm(c2_in_plane - c1_in_plane)
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return []
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = np.sqrt(max(0, r1**2 - a**2))
    p2 = c1_in_plane + a * (c2_in_plane - c1_in_plane) / d
    inters = []
    for sign in [+1, -1]:
        rx = -(c2_in_plane[1] - c1_in_plane[1]) * (h / d) * sign
        ry =  (c2_in_plane[0] - c1_in_plane[0]) * (h / d) * sign
        pt_plane = p2 + np.array([rx, ry])
        pt3d = pt_plane[0]*u + pt_plane[1]*v
        zval = np.dot(c1, planeNormal)
        plane_offset = zval * planeNormal
        pt3d = pt3d + plane_offset
        inters.append(pt3d)
    return inters

class NHNLCircleWidgetChooseCenters(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draw NH and NL Circles (Choose Centers)")

        layout = QVBoxLayout()

        # NH table
        nh_table_html = """
        <b>Nasal height equations:</b>
        <table border="1" cellspacing="0" cellpadding="3">
            <tr>
                <th>Literature</th>
                <th>Ancestry</th>
                <th>Biological Sex</th>
                <th>Full equation</th>
                <th>Name of measurement in scene</th>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>European</td>
                <td>Males</td>
                <td>pred Rynn EA M NH = 0.78*Z + 9.5</td>
                <td>pred Rynn EA M NH</td>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>European</td>
                <td>Females</td>
                <td>pred Rynn EA F NH = 0.63*Z + 17</td>
                <td>pred Rynn EA F NH</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Males</td>
                <td>pred Sarilita M NH = 0.79*Z + 3.74</td>
                <td>pred Sarilita M NH</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Females</td>
                <td>pred Sarilita F NH = 0.69*X + 12.36</td>
                <td>pred Sarilita F NH</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Females</td>
                <td>pred Bulut F NH = 15.047 + 0.687*Z</td>
                <td>pred Bulut F NH</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Males</td>
                <td>pred Bulut M NH = 9.858 + 0.784*Z</td>
                <td>pred Bulut M NH</td>
            </tr>
        </table>
        """
        nh_table_label = QLabel()
        nh_table_label.setText(nh_table_html)
        nh_table_label.setWordWrap(True)
        nh_table_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(nh_table_label)

        description = QLabel(
            "<b>1. Choose NH (ND) circle center ('_sn pred'):</b>")
        layout.addWidget(description)
        self.nd_points = get_points_by_label_substring("_sn pred")
        self.nd_buttons = QButtonGroup(self)
        for i, (label, pos) in enumerate(self.nd_points):
            radio = QRadioButton(label)
            self.nd_buttons.addButton(radio, i)
            layout.addWidget(radio)
        if not self.nd_points:
            layout.addWidget(QLabel("No '_sn pred' points found."))

        layout.addWidget(QLabel("<b>2. Choose NH equation:</b>"))
        self.nh_equations = [
            "pred Rynn EA M NH", "pred Rynn EA F NH",
            "pred Sarilita M NH", "pred Sarilita F NH",
            "pred Bulut F NH", "pred Bulut M NH"
        ]
        self.nh_eq_buttons = QButtonGroup(self)
        for i, eq in enumerate(self.nh_equations):
            radio = QRadioButton(eq)
            self.nh_eq_buttons.addButton(radio, i)
            layout.addWidget(radio)

        # NL table
        nl_table_html = """
        <b>Nasal length equations:</b>
        <table border="1" cellspacing="0" cellpadding="3">
            <tr>
                <th>Literature</th>
                <th>Ancestry</th>
                <th>Biological Sex</th>
                <th>Full equation</th>
                <th>Name of measurement in scene</th>
            </tr>
            <tr>
                <td>Rynn et al. 2010</td>
                <td>European</td>
                <td>All</td>
                <td>pred Rynn EA NL = 0.74*Z + 3.5</td>
                <td>pred Rynn EA NL</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Females</td>
                <td>pred Sarilita F NL = 6.624 + 0.71*Z</td>
                <td>pred Sarilita F NL</td>
            </tr>
            <tr>
                <td>Bulut et al. 2019</td>
                <td>Turkish</td>
                <td>Males</td>
                <td>pred Sarilita M NL = 0.764 + 0.807*Z</td>
                <td>pred Sarilita M NL</td>
            </tr>
            <tr>
                <td>Sarilita et al. 2018</td>
                <td>Indonesian</td>
                <td>Males</td>
                <td>pred Bulut M NL = 0.66*X + 7.77</td>
                <td>pred Bulut M NL</td>
            </tr>
        </table>
        """
        nl_table_label = QLabel()
        nl_table_label.setText(nl_table_html)
        nl_table_label.setWordWrap(True)
        nl_table_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(nl_table_label)

        layout.addWidget(QLabel("<b>3. Choose NL circle center ('_pronasale pred'):</b>"))
        self.nl_points = get_points_by_label_substring("_pronasale pred")
        self.nl_buttons = QButtonGroup(self)
        for i, (label, pos) in enumerate(self.nl_points):
            radio = QRadioButton(label)
            self.nl_buttons.addButton(radio, i)
            layout.addWidget(radio)
        if not self.nl_points:
            layout.addWidget(QLabel("No '_pronasale pred' points found."))

        layout.addWidget(QLabel("<b>4. Choose NL equation:</b>"))
        self.nl_equations = [
            "pred Rynn EA NL", "pred Sarilita F NL",
            "pred Sarilita M NL", "pred Bulut M NL"
        ]
        self.nl_eq_buttons = QButtonGroup(self)
        for i, eq in enumerate(self.nl_equations):
            radio = QRadioButton(eq)
            self.nl_eq_buttons.addButton(radio, i)
            layout.addWidget(radio)

        self.create_button = QPushButton("Draw Both Circles & Find Closest n' pred to line '1'")
        self.create_button.clicked.connect(self.on_create)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def on_create(self):
        # Get selected NH center (ND)
        nd_idx = self.nd_buttons.checkedId()
        if nd_idx == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a '_sn pred' point for ND circle center.")
            return
        nd_label, nd_center = self.nd_points[nd_idx]

        nh_eq_id = self.nh_eq_buttons.checkedId()
        if nh_eq_id == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a NH equation.")
            return
        nh_equation = self.nh_equations[nh_eq_id]

        # Get selected NL center
        nl_idx = self.nl_buttons.checkedId()
        if nl_idx == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a '_pronasale pred' point for NL circle center.")
            return
        nl_label, nl_center = self.nl_points[nl_idx]

        nl_eq_id = self.nl_eq_buttons.checkedId()
        if nl_eq_id == -1:
            QMessageBox.warning(self, "Missing selection", "Please select a NL equation.")
            return
        nl_equation = self.nl_equations[nl_eq_id]

        # Get X, Y, Z lengths
        x_len = get_line_length("nas-aca X")
        y_len = get_line_length("rhi-subs Y")
        z_len = get_line_length("nas-subs Z")

        # Calculate radii
        try:
            nh_radius = calculate_nh_radius(nh_equation, x_len, y_len, z_len)
        except Exception as e:
            QMessageBox.warning(self, "NH equation error", str(e))
            return
        try:
            nl_radius = calculate_nl_radius(nl_equation, x_len, z_len)
        except Exception as e:
            QMessageBox.warning(self, "NL equation error", str(e))
            return

        # Get INB plane normal
        try:
            inb_plane = slicer.util.getNode("INB")
            planeNormal = np.array(inb_plane.GetNormal())
        except Exception:
            QMessageBox.warning(self, "Missing INB", "Could not find 'INB' plane in the scene.")
            return

        # Draw circles and LOG them
        create_circle_node(nd_center, nh_radius, planeNormal, "NH_circle", color=(1.0,0.2,0.2))  # Red
        add_to_markup_report(
            "Circle (NH)",
            "NH_circle",
            {
                "Center label": nd_label,
                "Center coords": np.round(nd_center, 2).tolist(),
                "NH equation": nh_equation,
                "NH radius": f"{nh_radius:.2f}"
            }
        )
        create_circle_node(nl_center, nl_radius, planeNormal, "NL_circle", color=(0.2,0.2,1.0))  # Blue
        add_to_markup_report(
            "Circle (NL)",
            "NL_circle",
            {
                "Center label": nl_label,
                "Center coords": np.round(nl_center, 2).tolist(),
                "NL equation": nl_equation,
                "NL radius": f"{nl_radius:.2f}"
            }
        )

        # Find intersection(s) and add only the one closest to line "1"
        inters = find_circle_circle_intersections(nd_center, nh_radius, nl_center, nl_radius, planeNormal)
        if not inters:
            QMessageBox.warning(self, "No intersection", "The NH and NL circles do not intersect in the INB plane.")
        else:
            # Find the closest intersection to line "1"
            try:
                line1 = slicer.util.getNode("1")
                line1_p0 = np.array(line1.GetNthControlPointPosition(0))
                line1_p1 = np.array(line1.GetNthControlPointPosition(1))
            except Exception:
                QMessageBox.warning(self, "Missing line", "Could not find line '1' in the scene.")
                return

            def point_to_line_distance(pt, p0, p1):
                line_vec = p1 - p0
                line_len = np.linalg.norm(line_vec)
                if line_len == 0:
                    return np.linalg.norm(pt - p0)
                proj = np.dot(pt - p0, line_vec) / line_len
                proj = np.clip(proj, 0, line_len)
                closest = p0 + proj * (line_vec / line_len)
                return np.linalg.norm(pt - closest)

            closest_pt = min(inters, key=lambda pt: point_to_line_distance(pt, line1_p0, line1_p1))

            try:
                pred_node = slicer.util.getNode("Rynn_soft_tissue_pred")
            except slicer.util.MRMLNodeNotFoundException:
                pred_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "Rynn_soft_tissue_pred")

            # Build abbreviations for the label
            abbrev_nd = abbreviate_point_label(nd_label)
            abbrev_nh_eq = abbreviate_equation_name(nh_equation)
            abbrev_nl = abbreviate_point_label(nl_label)
            abbrev_nl_eq = abbreviate_equation_name(nl_equation)
            label = f"n' pred_{abbrev_nd}_{abbrev_nh_eq}_{abbrev_nl}_{abbrev_nl_eq}"

            pred_node.AddControlPoint(closest_pt.tolist(), label)
            # LOG intersection point
            add_to_markup_report(
                "Intersection Point",
                label,
                {
                    "Closest to line": "1",
                    "NH center": nd_label,
                    "NH equation": nh_equation,
                    "NL center": nl_label,
                    "NL equation": nl_equation,
                    "Intersection coords": np.round(closest_pt, 2).tolist(),
                }
            )

        QMessageBox.information(self, "Done", "Both circles have been drawn and the closest n' pred intersection to line '1' has been marked with all abbreviations.")

widget = NHNLCircleWidgetChooseCenters()
widget.show()
```
</details>


### Reproducing Rynn's network of triangles
The network is described as what can be "used to define profile so that unmeasured lengths could be calculated trigonometrically" as well as the part of research where correlations between the soft and hard tissue measurement can be checked. 

- Point 5 lies around the same height as the inferior turbinate (conch)
- Point 7 lies around 4 mm inferior to the lowest point on the aperture border
- Point 4 lies around 6 mm anterior to the most posterior point on the PLB

In his thesis, Rynn (2006)[^2] concluded that 

> "the heights of each of the 8 landmark points on the nostrils and alae correlate positively and strongly with the bony heights of both the inferior turbinate (conch) and the lowest point on the aperture (low.pt)(...), regression equations would be appropriate to predict the height of each point from either of the bony features. However, this approach would be impractical and produce an inordinate number of equations."

In the light of improving programmes "reading" 3D data in recent future, the addition of egressions to be executed automatically is much more user friendly. To create these regressions accurately and precisely (that provide distances from the nasion along all 3 aforementioned planes), measuring the distances of each of these defined points from all planes may be of worth reproducing and analysing. This theory of visualising the points as almost "toggles" along the distinct planes may be easier to execute than the analysis of the coordinates of these points - also worth a data analysis question. 

For the code below to work, you have to allocate the landmarks NOT highlighted with either blue or orange. 
The following code created measurements of the distances on all planes for points 1, 2...8. 
Additionally, more potential relationship measurements from Rynn et al 2006[^2] (based on Glanville (1969)[^14] are featured with suggested comparisons: 

| Hard Tissue Measurement                           | Soft Tissue Measurement                                 |
|---------------------------------------------------|---------------------------------------------------------|
| rhinion-PLB(XL/XR)-acanthion angle                | soft tissue nasion-pronasale-subnasale angle            |
| MAW (maximum aperture width = XL to XR distance)  | MNW (maximum nasal width = pt6R-pt6L distance)          |
| incisor width L (LCIL-MCIL)                       | MNW (maximum nasal width = pt6R-pt6L distance)          |
| incisor width R (LCIR-MCIL)                       | MNW (maximum nasal width = pt6R-pt6L distance)          |
| intercanine width (ICL-ICR distance)              | MNW (maximum nasal width = pt6R-pt6L distance)          |


<details>

<summary>Rynn's triangle network</summary>

``` python
#pt1R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(3)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt1R')

import numpy as np
import slicer

# Get the original line node
originalLineNode = slicer.util.getNode('n-pt1R')

# Get the plane node
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# Get the start and end points of the original line
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

# Function to project a point onto the plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

# Project the start and end points onto the plane
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

# Create a new line node for the projected line
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt1R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)
# Set the color of the new line to green
projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer

# Get the original line node
originalLineNode = slicer.util.getNode('n-pt1R')

# Get the plane node
planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# Get the start and end points of the original line
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

# Function to project a point onto the plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

# Project the start and end points onto the plane
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

# Create a new line node for the projected line
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt1R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)
# Set the color of the new line to green
projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

# Get the original line node
originalLineNode = slicer.util.getNode('n-pt1R')

# Get the plane node
planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# Get the start and end points of the original line
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

# Function to project a point onto the plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

# Project the start and end points onto the plane
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

# Create a new line node for the projected line
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt1R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)
# Set the color of the new line to green
projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue
##############################################################################

#pt1L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(4)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt1L')

import numpy as np
import slicer

# Get the original line node
originalLineNode = slicer.util.getNode('n-pt1L')

# Get the plane node
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# Get the start and end points of the original line
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

# Function to project a point onto the plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

# Project the start and end points onto the plane
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

# Create a new line node for the projected line
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt1L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)
# Set the color of the new line to green
projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer

# Get the original line node
originalLineNode = slicer.util.getNode('n-pt1L')

# Get the plane node
planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# Get the start and end points of the original line
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

# Function to project a point onto the plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

# Project the start and end points onto the plane
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

# Create a new line node for the projected line
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt1L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)
# Set the color of the new line to green
projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

# Get the original line node
originalLineNode = slicer.util.getNode('n-pt1L')

# Get the plane node
planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# Get the start and end points of the original line
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

# Function to project a point onto the plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

# Project the start and end points onto the plane
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

# Create a new line node for the projected line
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt1L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)
# Set the color of the new line to green
projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

###################################################################################################
#pt2R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(5)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt2R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt2R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt2R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt2R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt2R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt2R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt2R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue
#############################################################################################
#pt2L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(6)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt2L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt2L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt2L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt2L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt2L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt2L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt2L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#########################################################################

#pt3R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(7)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt3R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt3R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt3R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt3R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt3R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt3R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt3R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt3L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(7)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt3L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt3L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt3L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt3L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt3L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt3L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt3L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue
##############################################################
#pt4R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(9)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt4R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt4R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt4R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt4R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt4R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt4R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt4R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt4L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(10)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt4L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt4L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt4L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt4L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt4L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt4L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt4L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue
#######################################################################################
#pt5R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(11)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt5R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt5R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt5R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt5R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt5R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt5R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt5R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt5L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(12)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt5L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt5L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt5L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt5L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt5L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt5L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt5L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

####################################################################################
#pt6R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(13)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt6R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt6R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt6R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt6R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt6R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt6R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt6R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt6L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(14)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt6L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt6L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt6L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt6L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt6L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt6L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt6L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

########################################################################################

#pt7R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(15)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt7R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt7R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt7R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt7R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt7R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt7R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt7R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt7L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(16)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt7L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt7L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt7L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt7L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt7L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt7L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt7L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

##########################################################################
#pt8R#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(17)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt8R')

import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt8R')


planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint

projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8R lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow


import numpy as np
import slicer


originalLineNode = slicer.util.getNode('n-pt8R')


planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8R')


planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))


def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt8L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(18)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt8L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8L')
planeNode = slicer.util.getNode('NPP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8L')

planeNode = slicer.util.getNode('PTP')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())


startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))

def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8L')

planeNode = slicer.util.getNode('INB')
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())
startPoint = np.array(originalLineNode.GetNthControlPointPosition(0))
endPoint = np.array(originalLineNode.GetNthControlPointPosition(1))
def project_point_onto_plane(point, planeOrigin, planeNormal):
    pointToPlaneVector = point - planeOrigin
    distanceToPlane = np.dot(pointToPlaneVector, planeNormal)
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint
projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#Create PLB point by connecting XR and XL, then finding its intersecction with the INB#
import slicer
import numpy as np

# 1. Get the fiducial node with landmarks
F = slicer.util.getNode('Rynn_hard_tissue')

# 2. Get the XL and XR points (as numpy arrays)
pointXL = np.array(F.GetNthControlPointPositionVector(10))
pointXR = np.array(F.GetNthControlPointPositionVector(9))

# 3. (Optional) Create the line node "XL-XR" (not strictly needed for intersection math)
# You can create it if you want to check, but you don't need to visualize or keep it
L = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'XL-XR')
L.AddControlPoint(pointXL)
L.AddControlPoint(pointXR)

# 4. Get the plane node "INB"
planeNode = slicer.util.getNode("INB")
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# 5. Calculate the intersection point (standard line-plane intersection math)
lineDir = pointXR - pointXL
ndotu = planeNormal.dot(lineDir)
if abs(ndotu) < 1e-6:
    raise Exception("Line and plane are parallel and do not intersect.")

w = pointXL - planeOrigin
si = -planeNormal.dot(w) / ndotu
intersection = pointXL + si * lineDir

# 6. Save the intersection as a new point node "PLB"
plbNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "PLB")
plbNode.AddControlPoint(intersection.tolist())

# 7. (Optional) Remove the temporary "XL-XR" line node so it's not displayed
slicer.mrmlScene.RemoveNode(L)

print("Intersection point 'PLB' created at:", intersection)

###rhinion-PLB(XL/XR)-acanthion angle	soft tissue nasion-pronasale-subnasale angle###
import slicer
import numpy as np

# Get the nodes for the existing points and lines
hardTissueNode = slicer.util.getNode('lmrks_Stephan')
PLBnode=slicer.util.getNode('PLB')

# Get the positions of the control points
apexPoint = np.array(hardTissueNode.GetNthControlPointPosition(5))
firstControlPoint = np.array(PLBnode.GetNthControlPointPosition(0))
thirdControlPoint = np.array(hardTissueNode.GetNthControlPointPosition(6))

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'rhi-PLB-aca')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Second control point (apex)
angleNode.AddControlPoint(thirdControlPoint)  # Third control point

print("New angle 'rhi-PLB-aca' created successfully.")


###original soft tissue nasion-pronasale-subnasale angle###
import slicer
import numpy as np

# Get the nodes for the existing points and lines
softTissueNode = slicer.util.getNode('Rynn_soft_tissue')

# Get the positions of the control points
apexPoint = np.array(softTissueNode.GetNthControlPointPosition(0))
firstControlPoint = np.array(softTissueNode.GetNthControlPointPosition(2))
thirdControlPoint = np.array(softTissueNode.GetNthControlPointPosition(1))

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'n'-pn-sn')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Second control point (apex)
angleNode.AddControlPoint(thirdControlPoint)  # Third control point

print("New angle 'n'-pn-sn' created successfully.")

F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(9)     #XL#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(10)	#XR#
L.AddControlPoint(secondPoint)
L.SetName('MAW')


G=getNode('Rynn_soft_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = G.GetNthControlPointPositionVector(13)     #pt6R#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(14)	#pt6L#
L.AddControlPoint(secondPoint)
L.SetName('MNW')


F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(15)     #LCIL#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(17)	#MCIL#
L.AddControlPoint(secondPoint)
L.SetName('incisor width L')

F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(16)     #LCIR#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(18)	#MCIL#
L.AddControlPoint(secondPoint)
L.SetName('incisor width R')

F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(13)     #ICR#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(14)	#ICL#
L.AddControlPoint(secondPoint)
L.SetName('intercanine width')
```
</details>

#### Optional: compare the predicted n'-pn-sn and the actual angle
This GUI creates an angle from the "Rynn_soft_tissue_pred" node where all the nodes created via equations are saved. You will be offered a choice of 3 points: any predicted **soft tissue nasion** as the first control point; any predicted **pronasale** as the apex;  and any predicted **subnasale** as the third  control point.

<details>

<summary>GUI for predicted angle</summary>

``` python
import slicer
import numpy as np
from qt import QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QGroupBox


def get_fiducial_labels_and_indices(node):
    labels = []
    for i in range(node.GetNumberOfControlPoints()):
        labels.append((node.GetNthControlPointLabel(i), i))
    return labels

sourceNode = slicer.util.getNode('Rynn_soft_tissue_pred')
labels_indices = get_fiducial_labels_and_indices(sourceNode)

first_candidates = [(l, i) for l, i in labels_indices if l.startswith("n' pred_")]
apex_candidates = [(l, i) for l, i in labels_indices if l.endswith("_pronasale pred")]
third_candidates = [(l, i) for l, i in labels_indices if l.endswith("_sn pred")]

class AngleCreationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create pred n'-pn-sn Angle")
        layout = QVBoxLayout()

        def create_radio_group(title, candidates):
            groupBox = QGroupBox(title)
            vbox = QVBoxLayout()
            group = QButtonGroup(self)
            for label, idx in candidates:
                btn = QRadioButton(label)
                group.addButton(btn, idx)
                vbox.addWidget(btn)
            groupBox.setLayout(vbox)
            return groupBox, group

        self.firstGroupBox, self.firstGroup = create_radio_group("Choose first control point (starts with n' pred_):", first_candidates)
        layout.addWidget(self.firstGroupBox)

        self.apexGroupBox, self.apexGroup = create_radio_group("Choose apex (ends with _pronasale pred):", apex_candidates)
        layout.addWidget(self.apexGroupBox)

        self.thirdGroupBox, self.thirdGroup = create_radio_group("Choose third control point (ends with _sn pred):", third_candidates)
        layout.addWidget(self.thirdGroupBox)

        self.createButton = QPushButton("Create Angle")
        self.createButton.clicked.connect(self.create_angle)
        layout.addWidget(self.createButton)

        self.setLayout(layout)
        self.angle_counter = 1

    def create_angle(self):
    print("Button was clicked!")  # Add this
        idx1 = self.firstGroup.checkedId()
        idx2 = self.apexGroup.checkedId()
        idx3 = self.thirdGroup.checkedId()

        if idx1 == -1 or idx2 == -1 or idx3 == -1:
            print("Please select a point in each group before creating the angle.")
            return

        # Find the selected radio button texts
        btn1 = self.firstGroup.button(idx1)
        btn2 = self.apexGroup.button(idx2)
        btn3 = self.thirdGroup.button(idx3)
        label1 = btn1.text() if btn1 else ""
        label2 = btn2.text() if btn2 else ""
        label3 = btn3.text() if btn3 else ""

        firstPoint = np.array(sourceNode.GetNthControlPointPosition(idx1))
        apexPoint = np.array(sourceNode.GetNthControlPointPosition(idx2))
        thirdPoint = np.array(sourceNode.GetNthControlPointPosition(idx3))

        angle_name = f"pred n'-pn-sn {self.angle_counter}"
        angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', angle_name)
        angleNode.AddControlPoint(firstPoint)
        angleNode.AddControlPoint(apexPoint)
        angleNode.AddControlPoint(thirdPoint)

        # --- LOGGING ---
        choices = {
            "First control point": label1,
            "Apex": label2,
            "Third control point": label3
        }
        add_to_markup_report("Angle", angle_name, choices)

        self.angle_counter += 1

widget = AngleCreationWidget()
widget.show()
```
</details>


## Error rates
Run only the first code snippet if you want to measure the distance between the predicted landmarks and actual landmarks. 
Additionally, run the second code if you want to check either the error or displacement vectors in Rynn's triangle network



<details>
<summary>Error rate between predicted vs true points</summary>

 ```python
import slicer
import numpy as np
def create_error_lines():
    # Get the nodes
    pred_node = slicer.util.getNode("Rynn_soft_tissue_pred")
    soft_node = slicer.util.getNode("Rynn_soft_tissue")

    # Get the key soft tissue points
    soft_points = {
        "nasion": (0, "soft tissue nasion"),
        "subnasale": (1, "subnasale"),
        "pronasale": (2, "pronasale")
    }

    # Extract positions from soft tissue node
    soft_positions = {}
    for label, (idx, name) in soft_points.items():
        soft_positions[label] = (
            name,
            np.array(soft_node.GetNthControlPointPosition(idx))
        )

    # Go through all predicted points
    for i in range(pred_node.GetNumberOfControlPoints()):
        pred_label = pred_node.GetNthControlPointLabel(i)
        pred_pos = np.array(pred_node.GetNthControlPointPosition(i))

        # Connect n' pred (nasion equivalents)
        if pred_label.startswith("n' pred"):
            soft_name, soft_pos = soft_positions["nasion"]
            line_name = f"error_{pred_label}_{soft_name}"
        # Connect ..._sn pred (subnasale equivalents)
        elif pred_label.endswith("_sn pred"):
            soft_name, soft_pos = soft_positions["subnasale"]
            line_name = f"error_{pred_label}_{soft_name}"
        # Connect ..._pronasale pred (pronasale equivalents)
        elif pred_label.endswith("_pronasale pred"):
            soft_name, soft_pos = soft_positions["pronasale"]
            line_name = f"error_{pred_label}_{soft_name}"
        else:
            continue  # Not a target point

        # Create the error line
        line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", line_name)
        # Set color to hot red (RGB: 1, 0, 0)
        line_node.GetDisplayNode().SetSelectedColor(1, 0, 0)
        # Add endpoints
        line_node.AddControlPoint(pred_pos.tolist())
        line_node.AddControlPoint(soft_pos.tolist())

        print(f"Created line: {line_name}")

create_error_lines()
```
</details>






<details>
<summary>Error/displacement between soft-hard tissue points/distances</summary>
 
```python
import slicer
import numpy as np
def create_colored_lines_and_displacements():
    # Define pairs: (soft label, soft idx, hard label, hard idx, line name, color)
    pairs = [
        # Red pairs
        ("pt5L", 12, "CL", 7, "left Point 5 -left inferior turbinate", (1, 0, 0)),  # red
        ("pt5R", 11, "CR", 8, "right Point 5 -right inferior turbinate", (1, 0, 0)),  # red
        # Green pairs
        ("pt7L", 16, "LL", 11, "left Point 7 -left lowest aperture border", (0.13, 0.55, 0.13)),  # forest green
        ("pt7R", 15, "LR", 12, "right Point 7 -right lowest aperture border", (0.13, 0.55, 0.13)),
        ("pt4L", 10, "XL", 9, "left Point 4 -left most posterior point on the left piriform border", (0.13, 0.55, 0.13)),
        ("pt4R", 9, "XR", 10, "right Point 4 -right most posterior point on the right piriform border", (0.13, 0.55, 0.13)),
    ]

    soft_node = slicer.util.getNode("Rynn_soft_tissue")
    hard_node = slicer.util.getNode("Rynn_hard_tissue")

    for soft_label, soft_idx, hard_label, hard_idx, line_name, color in pairs:
        soft_pos = np.array(soft_node.GetNthControlPointPosition(soft_idx))
        hard_pos = np.array(hard_node.GetNthControlPointPosition(hard_idx))
        line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", line_name)
        line_node.GetDisplayNode().SetSelectedColor(*color)
        line_node.AddControlPoint(hard_pos.tolist())
        line_node.AddControlPoint(soft_pos.tolist())

        # Compute displacement (from hard tissue to soft tissue)
        displacement = soft_pos - hard_pos
        displacement_length = np.linalg.norm(displacement)
        print(f"{line_name}:")
        print(f"  From {hard_label} (hard) at {np.round(hard_pos,2)} to {soft_label} (soft) at {np.round(soft_pos,2)}")
        print(f"  Displacement vector (soft - hard): {np.round(displacement,2)}")
        print(f"  Displacement length: {displacement_length:.2f} mm\n")

def closest_point_between_lines(A0, A1, B0, B1):
    # Returns (pa, pb, dist) where pa is closest point on line A, pb on B, dist is their distance
    A0 = np.array(A0); A1 = np.array(A1); B0 = np.array(B0); B1 = np.array(B1)
    u = A1 - A0
    v = B1 - B0
    w0 = A0 - B0
    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w0)
    e = np.dot(v, w0)
    denom = a * c - b * b
    if denom == 0:
        t = np.dot((A0 - B0), v) / np.dot(v, v)
        pb = B0 + t * v
        pa = A0
    else:
        s = (b * e - c * d) / denom
        t = (a * e - b * d) / denom
        pa = A0 + s * u
        pb = B0 + t * v
    dist = np.linalg.norm(pa - pb)
    return pa, pb, dist

def create_shortest_distance_line_between_MNW_and_MAW():
    MNW = slicer.util.getNode("MNW")
    MAW = slicer.util.getNode("MAW")
    MNW_p0 = np.array(MNW.GetNthControlPointPosition(0))
    MNW_p1 = np.array(MNW.GetNthControlPointPosition(1))
    MAW_p0 = np.array(MAW.GetNthControlPointPosition(0))
    MAW_p1 = np.array(MAW.GetNthControlPointPosition(1))
    pa, pb, dist = closest_point_between_lines(MNW_p0, MNW_p1, MAW_p0, MAW_p1)
    line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "Shortest MNW-MAW")
    # Forest green
    line_node.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)
    line_node.AddControlPoint(pa.tolist())
    line_node.AddControlPoint(pb.tolist())
    displacement = pb - pa
    print("Shortest MNW-MAW:")
    print(f"  From MNW at {np.round(pa,2)} to MAW at {np.round(pb,2)}")
    print(f"  Displacement vector (MAW - MNW): {np.round(displacement,2)}")
    print(f"  Displacement length: {dist:.2f} mm\n")

# Run both parts
create_colored_lines_and_displacements()
create_shortest_distance_line_between_MNW_and_MAW()
```
</details>


## Outputs
Depending on which landmarks you allocated, there are multiple versions of outputs. 

#### Rynn/Sarilita/Bulut regression predictions
You allocated ONLY the marked 🔵 hard tissue points and 🟧soft tissue landmarks AND did not run any of the "Rynn's triangle" codes


#### Rynn's trinagle included 
You allocated ALL landmarks AND ran the "Rynn's triangle" codes




# Bibliography

[^1]: 3D Slicer webpage https://www.slicer.org/
[^2]: Rynn, C. (2006). Craniofacial Approximation and Reconstruction: Tissue Depth Patterning and the Prediction of the Nose. Anatomy and Forensic Anthropology, School of Life Sciences. Dundee, United Kingdom, University of Dundee. Doctor of Philosophy.
[^3]: Rynn, C., et al. (2010). "Prediction of nasal morphology from the skull." Forensic Science Medicine and Pathology 6(1): 20-34.
[^4]: Caple, J. and C. N. Stephan (2016). "A standardized nomenclature for craniofacial and facial anthropometry." International Journal of Legal Medicine 130(3): 863-879.
[^5]: Martin, R. (1928). Lehrbuch der Anthropologie in systematischer Darstellung: mit besonderer Berücksichtigung der anthropologischen Methoden ; für Studierende, Ärzte und Forschungsreisendechichte, Morphologische Methoden. Jena, Gustav Fisher.
[^6]: Knussmann, R. (1988). Anthropologie: Handbuch der vergleichenden Biologie des Menschen, G. Fischer.
[^7]: Howells, W. W. (1937). "The designation of the principle anthrometric landmarks on the head and skull." American Journal of Physical Anthropology 22(3): 477-494.
[^8]: Howells, W. W. (1974). Cranial variation in man: A study by multivariate analysis of patterns of difference among recent human populations. Cambridge, Harvard University.
[^9]: Kolar, J. and E. Salter (1997). Craniofacial anthropometry: practical measurement of the head and face for clinical, surgical, and research use. Springfield, Charles C Thomas.
[^10]:Farkas, L. G. (1994). Anthropometry of the Head and Face, Lippincott Williams & Wilkins.
[^11]: Prokopec, M. and D. H. Ubelaker (2002). "Reconstructing the Shape of the Nose According to the Skull by Miroslav Prokopec (Forensic Science Communications, January 2002)." Research and Technology 4(1).
[^12]: Sarilita, E., et al. (2018). "Nose profile morphology and accuracy study of nose profile estimation method in Scottish subadult and Indonesian adult populations." International Journal of Legal Medicine 132(3): 923-931.
[^13]: Bulut, O., et al. (2019). "Prediction of nasal morphology in facial reconstruction: Validation and recalibration of the Rynn method." Legal Medicine 40: 26-31.
[^14]: Glanville, E. V. (1969). "Nasal shape, prognathism and adaptation in man." American Journal of Physical Anthropology 30(1): 29-37.
