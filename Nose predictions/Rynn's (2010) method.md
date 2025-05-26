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
| 13               | 14               | ICR           | ICR           | right maxillary canine cusp tip point | Rynn et al 2006[^2] |
| 14               | 15               | ICL           | ICL           | left maxillary canine cusp tip point |  Rynn et al 2006[^2]|
| 15               | 16               | LCIL          | LCIL           | most lateral point on the left central incisor in the maxilla |  Rynn et al 2006[^2] |
| 16               | 17               | LCIR          | LCIR           | most lateral point on the right central incisor in the maxilla |  Rynn et al 2006[^2] |
| 17               | 18               | MCIL          | MCIL           | most medial point on the left central incisor in the maxilla |  Rynn et al 2006[^2] |
| 18               | 19               | MCIR          | MCIR           | most medial point on the right central incisor in the maxilla |  Rynn et al 2006[^2] |


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

Video on what to expect when running the code: 


https://github.com/user-attachments/assets/3a012692-8a17-4c70-a554-5fac4aa00581



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

``` python
import slicer
import numpy as np
from qt import QPushButton, QVBoxLayout, QWidget, QCheckBox, QLabel, QTextEdit, QSizePolicy

# Function to create a new line in Slicer
def create_line(name, length, color, start_point, direction):
    line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
    line.GetDisplayNode().SetSelectedColor(color)
    start_point = np.array(start_point)
    direction = np.array(direction)
    line.AddControlPoint(start_point.tolist())
    end_point = start_point + direction * length
    line.AddControlPoint(end_point.tolist())
    return line

# Function to calculate length based on the selected equation
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

# Function to create the new line based on the chosen equation
def create_new_line_with_equation(equation):
    print("Inside create_new_line_with_equation function")
    # Get the required nodes from the scene
    rynn_hard_tissue = slicer.util.getNode("Rynn_hard_tissue")
    line_1 = slicer.util.getNode("1")
    rhi_subs_Y = slicer.util.getNode("rhi-subs Y")

    # Define the start point and REVERSED direction for the new line
    start_point = rynn_hard_tissue.GetNthControlPointPosition(0)
    direction = np.array(line_1.GetNthControlPointPosition(1)) - np.array(line_1.GetNthControlPointPosition(0))
    direction = direction / np.linalg.norm(direction)
    direction = -direction  # Reverse the direction

    # Get two points from the "rhi-subs Y" node
    point1 = np.array(rhi_subs_Y.GetNthControlPointPosition(0))
    point2 = np.array(rhi_subs_Y.GetNthControlPointPosition(1))

    # Calculate Y distance between these points
    Y = np.linalg.norm(point2 - point1)

    # Calculate the length from the chosen equation
    length = calculate_length(equation, Y)

    # Set color to purple (RGB: 0.5, 0.0, 0.5)
    purple = (0.5, 0.0, 0.5)

    # Create the new line
    new_line = create_line(equation, length, purple, start_point, direction)
    print(f"Line '{equation}' created with length: {length:.2f}")

# The GUI class for user interaction
class LineCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pronasale Anterior Prediction")

        layout = QVBoxLayout()

        # Add the instruction label at the top
        title_label = QLabel("<b>Please choose the equation(s) for pronasale anterior prediction!</b>")
        layout.addWidget(title_label)

        # Description section with a table
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

        # Use checkboxes for multiple selection
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
        # Collect all checked equations
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

# Create and show the GUI
line_creation_widget = LineCreationWidget()
line_creation_widget.show()
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
    # Example: "pred Rynn PV" -> "RynnPV", "pred Bulut F PV" -> "BulutF-PV"
    eq = eq.replace("pred ", "").replace(" ", "")
    # Add a dash before PV/PA if there's an M or F, for clarity
    eq = eq.replace("MPV", "M-PV").replace("FPV", "F-PV")
    return eq

def create_parallel_line_to_2(pa_line_node, x_line_node, pv_equation, pa_equation):
    # We start from the end of the PA line
    end = get_line_endpoints(pa_line_node)[1]

    # Find line "2"
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
    return new_line  # Return the created line for further use

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

        # --- Add the description table here ---
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

        # Find PA lines
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
        # Get selected PA lines
        selected_pa_lines = [node for cb, node in self.pa_checkboxes if cb.isChecked()]
        if not selected_pa_lines:
            QMessageBox.warning(self, "Selection Error", "Please select at least one PA line.")
            return

        # Find X line
        x_line_node = find_x_line()
        if x_line_node is None:
            QMessageBox.warning(self, "Selection Error", "No line named 'nas-aca X' found in the scene.")
            return

        # Get selected equations
        chosen_equations = [eq for cb, eq in self.checkbox_list if cb.isChecked()]
        if not chosen_equations:
            QMessageBox.warning(self, "Selection Error", "Please select at least one PV equation.")
            return

        for pa_line_node in selected_pa_lines:
            pa_equation = pa_line_node.GetName()  # This is your PA equation choice name
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

The line(s) created via this code will appear in **turquoise**, named according to the linear regression used and all will run from the subspinale point along the "3" line. The length is calculated by your chosen linear regression. Below the table summarises the options, please refer back to the original literature[^3], [^12], [^13]  if in doubt. 

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
    # "pred Rynn pFHP" -> "RynnpFHP", "pred Bulut F pFHP" -> "BulutF-pFHP"
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

        # --- Add the description table here ---
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

        # Equation checkboxes
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
        # Check equation selection
        chosen_equations = [eq for cb, eq in self.checkbox_list if cb.isChecked()]
        if not chosen_equations:
            QMessageBox.warning(self, "Selection Error", "Please select at least one pFHP equation.")
            return

        # Find required nodes
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

        # Get direction of line "3" and reverse it
        line3_start, line3_end = get_line_endpoints(line_3)
        direction = line3_end - line3_start
        norm = np.linalg.norm(direction)
        if norm == 0:
            QMessageBox.warning(self, "Error", "Line '3' has zero length!")
            return
        direction = -direction / norm  # REVERSED direction

        # Get Y length
        Y = get_line_length(rhi_subs_Y)

        for equation in chosen_equations:
            try:
                length = calculate_pfhp_length(equation, Y)
                abbrev = abbreviate_equation_name(equation)
                line_name = abbrev
                create_turquoise_line(start_point, direction, length, line_name)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

widget = PFHPLineCreationWidget()
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
    # Example: "Rynn_soft_tissue_pred_sn pred" -> "sn_pred"
    # You can adjust this logic for your naming style
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

        # Draw circles
        create_circle_node(nd_center, nh_radius, planeNormal, "NH_circle", color=(1.0,0.2,0.2))  # Red
        create_circle_node(nl_center, nl_radius, planeNormal, "NL_circle", color=(0.2,0.2,1.0))  # Blue

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
Additionally, more potential relationship measurements from Rynn et al 2006[^2] are featured with suggested comparisons: 

| Hard Tissue Measurement                           | Soft Tissue Measurement                                 |
|---------------------------------------------------|---------------------------------------------------------|
| rhinion-PLB(XL/XR)-acanthion angle                | soft tissue nasion-pronasale-subnasale angle            |
| MAW (maximum aperture width = XL to XR distance)  | MNW (maximum nasal width = pt6R-pt6L distance)          |
| incisor width L (LCIL-MCIL)                       | MNW (maximum nasal width = pt6R-pt6L distance)          |
| incisor width R (LCIR-MCIL)                       | MNW (maximum nasal width = pt6R-pt6L distance)          |
| intercanine width (ICL-ICR distance)              | MNW (maximum nasal width = pt6R-pt6L distance)          |

<details>

<summary>Triangle network code</summary>

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
    project 


