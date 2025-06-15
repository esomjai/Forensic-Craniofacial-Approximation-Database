# The Threefold ANS Method by Krogman & Iscan, 1986[^2], as interpreted by Rynn et al. (2010)[^7]


Summary: 

Krogman and Iscan's original equation as interpreted by Taylor, 2001[^3] and Rynn et al. (2010)[^7]
Revised equation for elderly Japanese individuals
Revised equation for Caucasian/White subadults

The method interpretation for the threefold ANS in this guide is based on Rynn et al. (2010)[^7]. We also added optional recalibration methods to the regression equation by Matsuda et al. 2023

They describe it as follows:

> “A line is projected, following the direction of the ANS, and the average soft tissue depth at mid-philtrum is vertically transposed up to it. The length of the ANS, from the vomer-maxillary junction (VMJ) to the acanthion (at the tip on the ANS) is tripled and added to the transferred average of soft tissue depth” (Krogman 1968[^2], Taylor, 2001[^3])

Stephan et al. 2003[^5] trialled _“substituting original nasal spine length for that determined by margin of most prominent lateral nasal aperture line to tip of nasal spine on lateral radiographs where the vomer was not detectable_ (referred in Rynn et al. 2010[^7] as PLB)”, but found larger margins of error. Therefore, the VMJ in this guide will be described as the junction of the vomer and maxilla (at the base of the nasal spine) and placed at the purple dot on figure 1 (modified from Grey's 1918[^6]). 

<img src="https://github.com/user-attachments/assets/7e44016c-eaee-4b31-96ea-27af828d6bdf" width="500">



## The Rynn et al. (2010) and Taylor (2001)[^3] interpretation

To repeat this interpretation by Rynn et al. (2010)[^7], we will:

- [Establish an INB plane](#inb-plane)
- [Make a profile view](#profile-view-model)
- [Draw an acanthion vector](#establishing-the-acanthion-vector)
- [Create and adjust the mid-philtrum point](#mid-philtrum-and-reference-to-mp)
- [Choose a path to Soft tissue depth markers](#soft-tissue-depth-markers)
- [Line as the FSTT](#path1-line-as-the-fstt)
- [Line error of estimate](#line-error-of-estimate)
- [Line method output](#line-method-output)
- [Cylinder as the FSTT](#path2-cylinder-as-the-fstt)
- [Cylinder Error of estimate](#cylinder-error-of-estimate)
- [Cylinder method output](#cylinder-method-output)
- [Combined method output](#combining-methods-output)


Landmarks in this  guide for the Rynn interpretation: 
[KrogmanIscan_hard_tissue.mrk.json](https://github.com/user-attachments/files/20212533/KrogmanIscan_hard_tissue.mrk.json)

[KrogmanIscan_soft_tissue.mrk.json](https://github.com/user-attachments/files/20234679/KrogmanIscan_soft_tissue.mrk.json)

> [!WARNING]
> The sample CT (CBCT PreDentalSurgery) used in the screenshots of this guide does not have all the features (inion, bregma) that are to be landmarked. Please refer to the illustrations in the guide for correct placement. In addition, due to the CT being taken pre-surgery for an underbite, the error rate shown in the guide is probably not representative if implemented on a population without pathologies.

KrogmanIscan_soft_tissue contains:
| Position in code | Position in file | Name in file | Landmark name | Definition                                                                                                                     | Defined by            |
|------------------|------------------|--------------|---------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| 0                | 1                | pronasale    | pronasale     | The most anteriorly protruded point of the apex nasi. In the case of a bifid nose, the more protruding tip is chosen           | Caple and Stephan 2016[^8]|

KrogmanIscan_hard_tissue contains:

| Position in code | Position in file | Name in file | Landmark name | Definition                                                                                                                     | Defined by            |
|------------------|------------------|--------------|---------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| 0                | 1                | nasion       | nasion        | Intersection of the nasofrontal sutures in the median plane                                                                    | Rynn et al. 2010[^7]      |
| 1                | 2                | inion        | inion         | Median point between the apices of the superior nuchal lines and at the base of the external occipital protuberance (not the tip of the protuberance) | Rynn et al. 2010[^7]      |
| 2                | 3                | bregma       | bregma        | Where the sagittal and coronal sutures meet. Impossible to determine in juvenile skulls with anterior fontanelle, or with complete suture obliteration | Rynn et al. 2010[^7]      |
| 3                | 4                | subspinale      | subspinale       | Most rostral (end) point on the internasal suture.                                                                            | Rynn et al. 2010[^7]      |
| 4                | 5                | acanthion    | acanthion     | Most anterior tip of the anterior nasal spine                                                                                 | Rynn et al. 2010[^7]      |
| 5                | 6                |  VMJ  | vomer-maxillary junction      |    the point on the cranium where the maxilla and the vomer meet in the midline, at the posterior end of the anterior nasal spine        | Somjai 2025 (unpublished) |
| 6                | 7                |  prosthion  | prosthion      |   Median point between the central incisors on the anterior most margin of the maxillary alveolar rim        | Caple and Stephan 2016[^8], Martin, 1928[^9], Knussmann 1988[^10] |



Illustration of the method: 

> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

- [ ] The scan has to be re-aligned in the FHP
- [ ] You should have a Bone and Skin model via segmentation (explained later)



### INB plane

To help with the side profile, we will establish the “INB” plane as defined by Rynn et al. 2010[^7]. 

> a midsagittal plane (INB) which bisected the inion, nasion and bregma

by downloading the hard tissue markups file for this method: [KrogmanIscan_hard_tissue.mrk.json](https://github.com/user-attachments/files/20212533/KrogmanIscan_hard_tissue.mrk.json)
 allocating the first three landmarks (nasion, inion, bregma) and copying and pasting the following code: 
 
<details>
	
<summary>INB plane</summary>

```python

import numpy as np
import slicer

# Get the points from the "KrogmanIscan_hard_tissue" node
hardTissueNode = slicer.util.getNode('KrogmanIscan_hard_tissue')
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

```

</details>

<img src="https://github.com/user-attachments/assets/536f67fe-0479-43ce-a871-b70eb6f0abf6" width="500">


View after only the first 3 landmarks are allocated correctly AND INB extended via the toggles (dots)

### Segmentation
[link to step-by-step](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/003_Roi%20vs%20Segmentation.md)

You can hide all of these and keep only the models if you wish.

In case still need the red/green/yellow slice windows for precise landmark placement, keep only the original volume node (CTBrain in the example) and the models visible. 

### Profile view model

For this method, a profile view will be useful. 

To open the appropriate module, click on the magnifying glass icon next to the modules: 

![module](https://github.com/user-attachments/assets/08aeb820-240a-4cfd-a9c7-01d017c09c36)

And start typing “dynamic modeller” in the search bar.
![module2](https://github.com/user-attachments/assets/c9dfd153-3c8b-4e99-82a2-8ed83320aec7)

Click “Switch to Module” to open. 

You’ll see this menu on the left side of the screen: 

![dynamic-modeller](https://github.com/user-attachments/assets/035ea262-8235-4665-8c4d-c3df49945944)

The "INB” is established in the environment. To cut the model along this plane (technically cutting it in 2 and choosing which side to keep), choose the first button (Plane Cut).


![image](https://github.com/user-attachments/assets/9c297c00-d350-4994-9386-1e2aea9e3e25)

Make sure you create your cut model with the settings on the screenshot to cut the Bone model at the INB Plane: 

- [ ] Make sure the source volume is the full model of the Bone
- [ ] Choose INB as the plane node
- [ ]  Operation type should be **Intersection**
- [ ]  You MUST chose the **Create new model as...** from the drop-down menu and type in the custom name with the side prefix - otherwise you'll override your existing models. This time, the negative output will be the right side of the cut and the positive side is the left side
- [ ] DO NOT FORGET TO CLICK APPLY


- [ ] Check if this was executed by finding your 2 new models under the "Models" module

With these settings, the Model list will be the following: 


![image](https://github.com/user-attachments/assets/ca5973b4-e666-4070-8a1c-e1c12584bf46)



And you should have the following individual views (excluding/hiding the original full models for demonstration purposes):

<img src="(https://github.com/user-attachments/assets/1c18929a-71af-4793-a502-f02438d7ee68)" width="500">


You can now allocate the remainder of the landmarks on either model - they should appear on ALL of them. 


### Establishing the acanthion vector
Re-orient the view of either your left-bone model to see its right side OR your right-bone model to see its left side to look inside the cranium: 

To establish the tangent described as in the general direction of the acanthion, like an arrow, manually draw a vector in the general direction of the acanthion by going to “Markups” >”line” and creating a tangent relatively in the vicinity of the INB plane. Name this line “aca vector” (by double clicking on the name automatically added to the line - likely "L"- and typing it in)

<img src="https://github.com/user-attachments/assets/57341433-009a-47cf-be85-a6fd329fa4b8" width="500">


Now, execute the **aca vector to INB** code  that projects the lines to the INB, ensures that it bisects the acanthion and elongates the line in both directions. 


<details>
	
<summary>aca vector to INB</summary>

```python

import numpy as np
import slicer
from slicer.util import getNode

# Get the nodes for the line and the plane
line = getNode('aca vector')
plane = getNode('INB')

# Get the positions of the control points of the line
point1 = np.array(line.GetNthControlPointPositionVector(0))
point2 = np.array(line.GetNthControlPointPositionVector(1))

# Calculate the direction vector and normalize it
direction = point2 - point1
direction_normalized = direction / np.linalg.norm(direction)

# Extend the line by 50 mm in both directions
extension_length = 50  # mm
extended_point1 = point1 - extension_length * direction_normalized
extended_point2 = point2 + extension_length * direction_normalized

# Get the plane origin and normal
planeOrigin = np.array(plane.GetOriginWorld())
planeNormal = np.array(plane.GetNormalWorld())

# Function to project a point onto a plane
def project_point_onto_plane(point, planeOrigin, planeNormal):
    vector = point - planeOrigin
    distance = np.dot(vector, planeNormal)
    projected_point = point - distance * planeNormal
    return projected_point

# Project the extended points onto the plane
projected_point1 = project_point_onto_plane(extended_point1, planeOrigin, planeNormal)
projected_point2 = project_point_onto_plane(extended_point2, planeOrigin, planeNormal)

# Create a new line node for the projected line
projected_line = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
projected_line.AddControlPoint(projected_point1.tolist())
projected_line.AddControlPoint(projected_point2.tolist())
projected_line.SetName('aca vector projected onto INB plane')
```
</details>

<img src="https://github.com/user-attachments/assets/f792e15c-1def-482d-ac0c-8ff577017d9c" width="500">



### Mid-philtrum and reference to mp
The hard tissue mid-philtrum is defined as the _Median point midway between subspinale and prosthion_ – therefore a line connecting the subspinale and prosthion can be established and the midline found programmatically, which is a visual guide to allocate the **mp** landmark via the script 003_lines.txt, that also creates the VMJ-acanthion distance. An issue I found is that the average soft tissue thickness measurements often do not meet the acanthion vector - to combat this, an elongated soft tissue depth line called  "soft tissue projection line" with an arbitrary length of 50 mm is established. 

<details>
	
<summary>Mid-philtrum landmark & VMJ-aca line</summary>

```python

F=getNode('KrogmanIscan_hard_tissue')  
#opens up the collection of point you stored in the markup file#
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(4)     
#number is the number on list of saved points#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(5)
L.AddControlPoint(secondPoint)
L.SetName('VMJ-aca')     
#name of your measurements#

F=getNode('KrogmanIscan_hard_tissue')  
#opens up the collection of point you stored in the markup file#
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(3)     
#number is the number on list of saved points#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(6)
L.AddControlPoint(secondPoint)
L.SetName('ss-pr')     
#name of your measurements#

import slicer
from slicer.util import getNode

# Get the Markups node for the line 'ss-pr'
lineNode = getNode('ss-pr')

# Get the Markups node for 'KrogmanIscan_hard_tissue'
hardTissueNode = getNode('KrogmanIscan_hard_tissue')

# Get the coordinates of the endpoints from 'KrogmanIscan_hard_tissue' at positions 3 and 6
point1 = [0, 0, 0]
point2 = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(3, point1)
hardTissueNode.GetNthControlPointPosition(6, point2)

# Calculate the midpoint
midpoint = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2, (point1[2] + point2[2]) / 2]

# Add the midpoint to the 'KrogmanIscan_hard_tissue' node using AddControlPoint and set its label to "mp"
midpointIndex = hardTissueNode.AddControlPoint(midpoint)
hardTissueNode.SetNthControlPointLabel(midpointIndex, "mp")
```

</details>


If this “mp” does not meet the model, you may have to manually allocate it onto the surface of the maxilla. The script saves “mp” in the “hard tissue” node, in case you’d have to re-allocate or find it.

<img src="https://github.com/user-attachments/assets/58f738d2-d20f-4610-b039-472f26cf9bf4" width="500">

Example of programmatically placing mp that does not meet the bone surface

<img src="https://github.com/user-attachments/assets/628a6079-f810-4ea8-9fc9-5d8294dc45d3" width="500">

Example of the manually adjusted mp

For the soft tissue depth ”marker”, establish manually a line on both sides of the **mp** landmark that aligns with the surface of the maxilla called **reference for mp** (do not worry if the line does not meet the mp, the script will make sure it does), like this:


<img src="https://github.com/user-attachments/assets/89d0d6ea-02a3-49c8-bf8f-061f397989ee3" width="500">


This is needed to create the mid-philtrum soft tissue thickness’ direction perpendicular to the maxillary plane. An issue I found is that the average soft tissue thickness measurements often do not meet the acanthion vector. Therefore, a 5 cm extension is built-in the codes: **elongated mp soft tissue depth** and **cyl KrogmanIscan_soft_tissue ext** .
**Both methods** described will try to establish the line from the endpoint of the tissue marker a line perpendicular to the “aca projected to  INB” and find their intersection point to then measure the aca-VMJ distance 3 times from there, establishing the predicted pronasale as the anterior endpoint of the _"prd pred"/"prn pred-cyl"_ line. 

### Soft tissue depth markers
You have paths to establish a soft tissue depth marker for the method and ultimately, the pronasale prediction. The FSTT in the example is arbitrarily set to 12mm - if you wish to change this, look for either 

```python
# Set the length of the perpendicular line
length = 12  # mm
```
in the **Line Soft tissue Marker script** and re-write the number in the code.

OR

 ```python
# Define cylinder parameters
radius = 3.0  # 6mm diameter
height = 24.0
```
in **Cylinder Soft tissue Marker** script and re-write the number in the code. 
The reason the actual length is doubled in the code is due to the setup of a cylinder. To position it correctly, the mp landmark is in the middle of the cylinder body, so if we want to have 12mm from this, it has to be doubled to represent the correct height on the bone surface.


#### PATH1-Line as the FSTT
FSTT - facial soft tissue thickness
**Line Soft Tissue Marker** will try to establish the line from the endpoint of the tissue marker a line perpendicular to the “aca projected to  INB” and find their intersection point to then measure the aca-VMJ distance 3 times from there, establishing the predicted pronasale. 

<details>
	
<summary>Line Soft tissue Marker</summary>

```python

import numpy as np
import slicer
from slicer.util import getNode

#Get the Markups node for 'KrogmanIscan_hard_tissue'
hardTissueNode = getNode('KrogmanIscan_hard_tissue')

#Get the coordinates of the point 'mp' at position 7
mp = np.array(hardTissueNode.GetNthControlPointPositionVector(7))

#Get the 'reference for mp' line node
referenceLineNode = getNode('reference for mp')

#Get the coordinates of the reference line's endpoints
referencePoint1 = np.array(referenceLineNode.GetNthControlPointPositionVector(0))
referencePoint2 = np.array(referenceLineNode.GetNthControlPointPositionVector(1))

#Calculate the direction vector of the reference line
referenceDirection = referencePoint2 - referencePoint1
referenceDirection /= np.linalg.norm(referenceDirection)  # Normalize the vector

#Calculate the length of the reference line
lineLength = np.linalg.norm(referencePoint2 - referencePoint1)

#Calculate the new endpoints so that 'mp' is at the midpoint
adjustedPoint1 = mp - (referenceDirection * (lineLength / 2))
adjustedPoint2 = mp + (referenceDirection * (lineLength / 2))

#Update the 'reference for mp' line node with the new endpoints
referenceLineNode.SetNthControlPointPosition(0, *adjustedPoint1)
referenceLineNode.SetNthControlPointPosition(1, *adjustedPoint2)


import numpy as np
import slicer
from slicer.util import getNode

#Get the Markups node for 'KrogmanIscan_hard_tissue'
hardTissueNode = getNode('KrogmanIscan_hard_tissue')

#Get the coordinates of the point 'mp' at position 7
mp = np.array(hardTissueNode.GetNthControlPointPositionVector(7))

#Get the coordinates of the reference point (assuming it's at position 6)
referencePoint = np.array(hardTissueNode.GetNthControlPointPositionVector(6))

#Calculate the direction vector of the "reference to mp" line
referenceDirection = mp - referencePoint
referenceDirection /= np.linalg.norm(referenceDirection)  # Normalize the vector

#Define a vector that is not parallel to the referenceDirection (e.g., [1, 0, 0])
arbitraryVector = np.array([1, 0, 0])

#Calculate the perpendicular direction using the cross product
direction = np.cross(referenceDirection, arbitraryVector)
direction /= np.linalg.norm(direction)  # Normalize the vector

#Set the length of the perpendicular line
length = 12  # mm

#Calculate the endpoints of the perpendicular line
point1 = mp - (length / 2) * direction
point2 = mp + (length / 2) * direction

#Create a new line node for the perpendicular line
perpendicularLine = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
perpendicularLine.AddControlPoint(point1.tolist())
perpendicularLine.AddControlPoint(point2.tolist())
perpendicularLine.SetName('mp soft tissue depth')

import numpy as np
import slicer
from slicer.util import getNode

#Function to calculate the intersection point of two lines in 3D space
def line_intersection(p1, d1, p2, d2):
    # Create the matrix A and vector b for the system of equations
    A = np.array([d1, -d2]).T
    b = p2 - p1
    
    # Solve the system using least squares to handle non-square matrices
    t, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    intersection = p1 + t[0] * d1
    return intersection
	
import slicer
import numpy as np

#Get the original line node
original_line = slicer.util.getNode("mp soft tissue depth")

#Get the start and end points of the original line
start_point = np.array(original_line.GetNthControlPointPosition(0))
end_point = np.array(original_line.GetNthControlPointPosition(1))

#Calculate the direction vector of the original line
direction_vector = end_point - start_point
direction_vector /= np.linalg.norm(direction_vector)

#Define the new length (50 mm)
new_length = 50.0

#Get the start point from "KrogmanIscan_hard_tissue" at position 7
krogman_iscan_node = slicer.util.getNode("KrogmanIscan_hard_tissue")
new_start_point = np.array(krogman_iscan_node.GetNthControlPointPosition(7))

#Calculate the new end point based on the new start point
new_end_point = new_start_point + direction_vector * new_length

#Create a new line node for the elongated line
elongated_line = slicer.vtkMRMLMarkupsLineNode()
elongated_line.SetName("elongated mp soft tissue depth")
slicer.mrmlScene.AddNode(elongated_line)

#Set the control points for the new line
elongated_line.AddControlPoint(new_start_point)
elongated_line.AddControlPoint(new_end_point)

print("Elongated line created successfully.")	

#Get the 'elongated mp soft tissue depth' line node
softTissueProjectionLine = getNode('elongated mp soft tissue depth')

#Get the coordinates of the 'elongated mp soft tissue depth' line's endpoints
softTissuePoint1 = np.array(softTissueProjectionLine.GetNthControlPointPositionVector(0))
softTissuePoint2 = np.array(softTissueProjectionLine.GetNthControlPointPositionVector(1))

#Calculate the direction vector of the 'elongated mp soft tissue depth' line
softTissueDirection = softTissuePoint2 - softTissuePoint1
softTissueDirection /= np.linalg.norm(softTissueDirection)  # Normalize the vector

#Get the 'aca vector projected onto INB plane' line node
acaVectorLine = getNode('aca vector projected onto INB plane')

#Get the coordinates of the aca vector's endpoints
acaPoint1 = np.array(acaVectorLine.GetNthControlPointPositionVector(0))
acaPoint2 = np.array(acaVectorLine.GetNthControlPointPositionVector(1))

#Calculate the direction vector of the aca vector
acaDirection = acaPoint2 - acaPoint1
acaDirection /= np.linalg.norm(acaDirection)  # Normalize the vector

#Calculate the intersection point
intersectionPoint = line_intersection(softTissuePoint1, softTissueDirection, acaPoint1, acaDirection)

#Get the 'KrogmanIscan_hard_tissue' Markups node
hardTissueNode = getNode('KrogmanIscan_hard_tissue')

#Add the intersection point as a new control point
hardTissueNode.AddControlPoint(intersectionPoint.tolist())
hardTissueNode.SetNthControlPointLabel(hardTissueNode.GetNumberOfControlPoints() - 1, 'intersection')

import numpy as np
import slicer
from slicer.util import getNode

#Get the 'KrogmanIscan_hard_tissue' Markups node
hardTissueNode = getNode('KrogmanIscan_hard_tissue')

#Get the coordinates of the point at position 8
startPoint = np.array(hardTissueNode.GetNthControlPointPositionVector(8))

#Get the 'aca vector projected onto INB plane' line node
acaVectorLine = getNode('aca vector projected onto INB plane')

#Get the coordinates of the aca vector's endpoints
acaPoint1 = np.array(acaVectorLine.GetNthControlPointPositionVector(0))
acaPoint2 = np.array(acaVectorLine.GetNthControlPointPositionVector(1))

#Calculate the direction vector of the aca vector
acaDirection = acaPoint2 - acaPoint1
acaDirection /= np.linalg.norm(acaDirection)  # Normalize the vector

#Get the 'VMJ-aca' line node
vmjAcaLine = getNode('VMJ-aca')

#Get the coordinates of the VMJ-aca line's endpoints
vmjAcaPoint1 = np.array(vmjAcaLine.GetNthControlPointPositionVector(0))
vmjAcaPoint2 = np.array(vmjAcaLine.GetNthControlPointPositionVector(1))

#Calculate the length of the VMJ-aca line
vmjAcaLength = np.linalg.norm(vmjAcaPoint2 - vmjAcaPoint1)

#Set the length of the new line to be three times the length of the VMJ-aca line
newLineLength = 3 * vmjAcaLength

#Calculate the endpoints of the new line
endPoint = startPoint + acaDirection * newLineLength

#Create a new line node for the 'prn pred' line
prnPredLine = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
prnPredLine.AddControlPoint(startPoint.tolist())
prnPredLine.AddControlPoint(endPoint.tolist())
prnPredLine.SetName('prn pred')

#Set the color of the new line to magenta (RGB: 255, 0, 255)
displayNode = prnPredLine.GetDisplayNode()
displayNode.SetSelectedColor(255/255, 0/255, 255/255)
displayNode.SetColor(255/255, 0/255, 255/255)

```
</details>


Here, the anterior endpoint of the prn pred line will serve as the predicted pronasale (see image under the error section).

### Line Error of estimate
As a research question, you can also allocate the original pronasale (included in the _KrogmanIscan_soft_tissue.lmrk.json_ ) and check the error rate (copy and paste the code "prn error"). 

<details>
	
<summary>Line prn error</summary>

```python

import numpy as np
import slicer
from slicer.util import getNode

# Get the 'prn pred' line node
prnPredLine = getNode('prn pred')

# Get the endpoint of the 'prn pred' line (assuming it's the second point)
prnPredEndpoint = np.array(prnPredLine.GetNthControlPointPositionVector(1))

# Get the 'KrogmanIscan_soft_tissue' Markups node
softTissueNode = getNode('KrogmanIscan_soft_tissue')

# Get the coordinates of the point at position 0
softTissuePoint = np.array(softTissueNode.GetNthControlPointPositionVector(0))

# Create a new line node for the new line
newLine = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
newLine.AddControlPoint(prnPredEndpoint.tolist())
newLine.AddControlPoint(softTissuePoint.tolist())
newLine.SetName('prn error')

# Set the color of the new line to a desired color (e.g., blue)
displayNode = newLine.GetDisplayNode()
displayNode.SetSelectedColor(0/255, 0/255, 255/255)
displayNode.SetColor(0/255, 0/255, 255/255)

```

</details>

<img src="https://github.com/user-attachments/assets/5d29afaf-6b5a-485a-bdd6-1f126bd0a826" width="500">

To copy the error measurement, use the method described in [this guide](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/004_Copying%20measurements%20to%20Clipboard.md). 

### Line method output
The output will look like this: 
| ID | line | mm |
|-----------|------------|-------------------|
| (unknown) | aca vector | 12.36696035 |
| (unknown) | aca vector projected onto INB plane | 102.4995228 |
| (unknown) | VMJ-aca | 7.541734761 |
| (unknown) | ss-pr | 10.43245139 |
| (unknown) | reference for mp | 10.67855989 |
| (unknown) | mp soft tissue depth | 12 |
| (unknown) | elongated mp soft tissue depth | 50 |
| (unknown) | prn pred | 22.62520428 |
| (unknown) | prn error | 7.478958585 |

> [!IMPORTANT]
> Only "pred error" is a true measurement, do not use the other measurements as such in your data analysis!!!!

#### PATH2-Cylinder as the FSTT
FSTT - facial soft tissue thickness
In Taylor (2001)[^3], the method is described with the vinyl cylinders as the soft tissue markers which “are approximately 6 mm in diameter” – we can recreate this via script “” . The cylinder will be found in the “Model” area, called “Cylinder". 

<details>
	
<summary>Cylinder Soft tissue Marker</summary>
	
```python

import numpy as np
import vtk
import slicer

#Get nodes
referenceLine = slicer.util.getNode('reference for mp')
hardTissue = slicer.util.getNode('KrogmanIscan_hard_tissue')

#Calculate center point and direction
centerPoint = np.array(hardTissue.GetNthControlPointPosition(7))
p1 = np.array(referenceLine.GetNthControlPointPosition(0))
p2 = np.array(referenceLine.GetNthControlPointPosition(1))
direction = p2 - p1
direction /= np.linalg.norm(direction)  # Normalize the direction vector

#Calculate perpendicular direction
arbitrary_vector = np.array([1, 0, 0]) if direction[0] == 0 else np.array([0, 1, 0])
perpendicular_direction = np.cross(direction, arbitrary_vector)
perpendicular_direction /= np.linalg.norm(perpendicular_direction)  # Normalize

#Create cylinder node
cylinder = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLModelNode', 'Cylinder')
cylinder.CreateDefaultDisplayNodes()

#Define cylinder parameters
radius = 3.0  # 6mm diameter
height = 24.0

#Create cylinder source
cylinderSource = vtk.vtkCylinderSource()
cylinderSource.SetRadius(radius)
cylinderSource.SetHeight(height)
cylinderSource.SetResolution(50)
cylinderSource.Update()

#Apply transformation to align with the perpendicular direction and center point
transform = vtk.vtkTransform()
transform.Translate(centerPoint)
transform.RotateWXYZ(90, direction)  # Rotate to align with the reference line direction
transform.RotateWXYZ(90, [0, 0, 1])  # Additional rotation for left-to-right tilt

transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetInputConnection(cylinderSource.GetOutputPort())
transformFilter.SetTransform(transform)
transformFilter.Update()

#Set and observe mesh
cylinder.SetAndObserveMesh(transformFilter.GetOutput())


import numpy as np
import slicer
from slicer.util import getNode

try:
    # Get the cylinder model node
    cylinderModelNode = getNode('Cylinder')

    # Get the 'aca vector projected onto INB plane' line node
    acaVectorLine = getNode('aca vector projected onto INB plane')

    # Get the coordinates of the aca vector's endpoints
    acaPoint1 = np.array(acaVectorLine.GetNthControlPointPositionVector(0))
    acaPoint2 = np.array(acaVectorLine.GetNthControlPointPositionVector(1))

    # Calculate the direction vector of the aca vector
    acaDirection = acaPoint2 - acaPoint1
    acaDirection /= np.linalg.norm(acaDirection)  # Normalize the vector

    # Get the cylinder's polydata
    cylinderPolyData = cylinderModelNode.GetPolyData()

    # Initialize the minimum distance to a large value
    minDistance = float('inf')
    closestPoint = None

    # Iterate over all points in the cylinder's polydata
    for i in range(cylinderPolyData.GetNumberOfPoints()):
        point = np.array(cylinderPolyData.GetPoint(i))
        
        # Calculate the vector from the line point to the cylinder point
        vector = point - acaPoint1
        
        # Project the vector onto the line direction
        projectionLength = np.dot(vector, acaDirection)
        projectionPoint = acaPoint1 + projectionLength * acaDirection
        
        # Calculate the distance from the cylinder point to the projection point
        distance = np.linalg.norm(point - projectionPoint)
        
        # Update the minimum distance and closest point if necessary
        if distance < minDistance:
            minDistance = distance
            closestPoint = point

    # Create a new markups node for the closest point
    closestPointNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'closest to vector')
    closestPointNode.AddControlPoint(closestPoint[0], closestPoint[1], closestPoint[2])

    # Calculate a perpendicular vector to acaDirection that points upwards
    perpendicularDirection = np.cross(acaDirection, np.array([1, 0, 0]))
    perpendicularDirection /= np.linalg.norm(perpendicularDirection)  # Normalize the vector

    # Ensure the perpendicular direction is pointing upwards
    if perpendicularDirection[2] < 0:
        perpendicularDirection = -perpendicularDirection

    # Calculate the end point of the new line in the perpendicular direction
    endPoint = closestPoint + 50 * perpendicularDirection

    # Create a new line node for the "KrogmanIscan_soft_tissue ext"
    softTissueExtNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'cyl KrogmanIscan_soft_tissue ext')
    softTissueExtNode.AddControlPoint(closestPoint[0], closestPoint[1], closestPoint[2])
    softTissueExtNode.AddControlPoint(endPoint[0], endPoint[1], endPoint[2])

    # Find the intersection point between the two lines
    t = np.dot((closestPoint - acaPoint1), acaDirection) / np.dot(acaDirection, acaDirection)
    intersectionPoint = acaPoint1 + t * acaDirection

    # Add the intersection point to the existing "KrogmanIscan_hard_tissue" node
    hardTissueNode = getNode('KrogmanIscan_hard_tissue')
    hardTissueNode.AddControlPoint(intersectionPoint[0], intersectionPoint[1], intersectionPoint[2])
    hardTissueNode.SetNthControlPointLabel(hardTissueNode.GetNumberOfControlPoints() - 1, 'cyl intersection')

    print(f'The shortest distance is {minDistance} mm')
    print(f'The closest point on the cylinder is {closestPoint}')
    print(f'The new line "KrogmanIscan_soft_tissue ext" has been created.')
    print(f'The intersection point has been added to the "KrogmanIscan_hard_tissue" node as "cyl intersection"')

except Exception as e:
    print(f'An error occurred: {e}')

import numpy as np
import slicer
from slicer.util import getNode

#Get the 'KrogmanIscan_hard_tissue' Markups node
hardTissueNode = getNode('KrogmanIscan_hard_tissue')

#Get the coordinates of the point at position 8
startPoint = np.array(hardTissueNode.GetNthControlPointPositionVector(8))

#Get the 'aca vector projected onto INB plane' line node
acaVectorLine = getNode('aca vector projected onto INB plane')

#Get the coordinates of the aca vector's endpoints
acaPoint1 = np.array(acaVectorLine.GetNthControlPointPositionVector(0))
acaPoint2 = np.array(acaVectorLine.GetNthControlPointPositionVector(1))

#Calculate the direction vector of the aca vector
acaDirection = acaPoint2 - acaPoint1
acaDirection /= np.linalg.norm(acaDirection)  # Normalize the vector

#Get the 'VMJ-aca' line node
vmjAcaLine = getNode('VMJ-aca')

#Get the coordinates of the VMJ-aca line's endpoints
vmjAcaPoint1 = np.array(vmjAcaLine.GetNthControlPointPositionVector(0))
vmjAcaPoint2 = np.array(vmjAcaLine.GetNthControlPointPositionVector(1))

#Calculate the length of the VMJ-aca line
vmjAcaLength = np.linalg.norm(vmjAcaPoint2 - vmjAcaPoint1)

#Set the length of the new line to be three times the length of the VMJ-aca line
newLineLength = 3 * vmjAcaLength

#Calculate the endpoints of the new line
endPoint = startPoint + acaDirection * newLineLength

#Create a new line node for the 'prn pred - cyl' line
prnPredLine = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
prnPredLine.AddControlPoint(startPoint.tolist())
prnPredLine.AddControlPoint(endPoint.tolist())
prnPredLine.SetName('prn pred - cyl')

#Set the color of the new line to magenta (RGB: 255, 0, 255)
displayNode = prnPredLine.GetDisplayNode()
displayNode.SetSelectedColor(255/255, 0/255, 255/255)
displayNode.SetColor(255/255, 0/255, 255/255)

```

</details>

<img src="https://github.com/user-attachments/assets/8cb7cd0d-9938-43be-ae59-4f54a96968e4" width="500">


### Cylinder Error of estimate
As a research question, you can also allocate the original pronasale (included in the _KrogmanIscan_soft_tissue.lmrk.json_ ) and check the error rate (copy and paste the code "cylinder prn error"). 

<details>
	
<summary>Cylinder prn error</summary>
	
```python

import numpy as np
import slicer
from slicer.util import getNode

# Get the 'prn pred' line node
prnPredLine = getNode('prn pred - cyl')

# Get the endpoint of the 'prn pred' line (assuming it's the second point)
prnPredEndpoint = np.array(prnPredLine.GetNthControlPointPositionVector(1))

# Get the 'KrogmanIscan_soft_tissue' Markups node
softTissueNode = getNode('KrogmanIscan_soft_tissue')

# Get the coordinates of the point at position 0
softTissuePoint = np.array(softTissueNode.GetNthControlPointPositionVector(0))

# Create a new line node for the new line
newLine = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
newLine.AddControlPoint(prnPredEndpoint.tolist())
newLine.AddControlPoint(softTissuePoint.tolist())
newLine.SetName('prn error - cyl')

# Set the color of the new line to a desired color (e.g., blue)
displayNode = newLine.GetDisplayNode()
displayNode.SetSelectedColor(0/255, 0/255, 255/255)
displayNode.SetColor(0/255, 0/255, 255/255)
```

</details>

![image](https://github.com/user-attachments/assets/e58fa837-9be8-45eb-9d23-0f741a0068df)

To copy the error measurement, use the method described in [this guide](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/004_Copying%20measurements%20to%20Clipboard.md). 

### Cylinder method output
The output will look like this: 
| ID | line | mm |
|-----------|------------|-------------------|
| (unknown) | aca vector | 12.366960351887142 |
| (unknown) | aca vector projected onto INB plane | 102.49952284624524 |
| (unknown) | VMJ-aca | 7.541734760923145 |
| (unknown) | ss-pr | 10.432451394420564 |
| (unknown) | reference for mp | 10.678559893806572 |
| (unknown) | cyl KrogmanIscan_soft_tissue ext | 50.0 |
| (unknown) | prn pred - cyl | 22.62520428276943 |
| (unknown) | prn error - cyl | 7.2860215755338915 |

Again, the only true measurement here is the error. 


### Combining methods output
You can also just carry out both methods (line/cylinder) one after the other - there will be lines duplicated, but as long as the numbers are the same, they can be just ignored (they measure the same thing, but twice due to coding). Then, the error of the line and cylinder can be compared. If you do this in the order **FSTT line, line error, then FSTT cylinder, cylinder error**, the output will look like this: 

| ID | line | mm |
|-----------|------------|-------------------|
| (unknown) | aca vector | 12.366960351887142 |
| (unknown) | aca vector projected onto INB plane | 102.49952284624524 |
| (unknown) | VMJ-aca | 7.541734760923145 |
| (unknown) | ss-pr | 10.432451394420564 |
| (unknown) | reference for mp | 10.678559893806572 |
| (unknown) | mp soft tissue depth | 11.999999999999998 |
| (unknown) | elongated mp soft tissue depth | 49.99999999999999 |
| (unknown) | prn pred | 22.62520428276943 |
| (unknown) | prn error | 7.2860215755338915 |
| (unknown) | cyl KrogmanIscan_soft_tissue ext | 50.0 |
| (unknown) | prn pred - cyl | 22.62520428276943 |
| (unknown) | prn error - cyl | 7.2860215755338915 |


UNDER CONSTRUCTION1!!!!!
## Matsuda et al. (2023)[^11] ' s formula for the elderly Japanese

They convert the original formula from Krogman  & Iscan (1) AND (2)

	(1) TNP = 1.9 × ANSP + MPD
 
 	(2) TNP = ENP + MPD = 3 × ANSP + MPD

  
  to 	
  
  	(3) TNP = ENP (1.9 × ANSP) + MPD
   
  
where: TNP is total nasal projection, ANSP is anterior nasal spine projection, MPD is mid-philtrum depth and ENP is exposed nasal projection

> [!NOTE]
> This equation was calibrated on a population of 146 elderly Japanese individuals with the age range of 58-105 years; imaged via postmortem CTs . Please consider the applicability of the method to your data.

The landmarks for this method will include the points needed to replicate ALL measurements in the study, but the ones included in the equation (to estimate TNP) are noted with 🔵 in the table. The Rynn method used the INB plane as the midsagittal plane, but this midline plane is not defined by the same landmarks in Matsuda et al. 2023 - therefore this plane will be defined best fitting the hard tissue landmarks that are described as midline & can be allocated on the skull surface (a, ss, pr).

Make sure you have a [4-point FHP](https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Start%20here%20/002_Realign%20CT%20in%20the%20standard%20FHP.md#fhp-options) established before creating the midline plane via the code. 

### Landmarks for Matsuda et al. 2023 



### All measurements/lines

| Abbreviation      | Measurement Name              | Definition                                                                 | Also Known As                | Landmark 1  | Landmark 2 |
|-------------------|------------------------------|----------------------------------------------------------------------------|------------------------------|-------------|------------|
| TNP               | Total nose projection        | nose projection from anterior nasal spine base to pronasale                |                              | ANSbase     | pn         |
| ENP 🔵               | Exposed nose projection      | nose projection from subnasale to pronasale                                |                              | sn          | pn         |
| ANSP   🔵           | Anterior nasal spine projection | anterior nasal spine length from base to tip                               | ANS                          | ANS_base    | ANS_tip    |
| ht_guide for MPD 🔵 |                              | vertical line connecting anterior nasal spine base and alveolar region      |                              | ANS_base    | mp         |
| st_guide for MPD 🔵 |                              | soft tissue equivalent                                                     |                              | mp'         | ls         |
| MPD 🔵              | Mid-philtrum depth           | depth of vertical line connecting anterior nasal spine base and alveolar region, which corresponds to marker 5 for 3D facial reconstruction | arbitrary number, based on population data |             |            |
| st guide for MPG  |                              | line running along the deepest part of the philtrum                        |                              |             |            |
| MPG               | Mid-philtrum groove depth    | maximum depth of mid-philtrum groove (distance between the st guide for NDP and st guide for MPG) |                              |             |            |
| TNW               | Total nasal width            | maximum width between the most lateral points on the nasal ala              | MNW: maximum nasal width     | al'L        | al'R       |
| ANAW              | Anterior nasal aperture width| maximum width of the anterior nasal aperture                                | MAW: maximum aperture width  | alL         | alR        |


### the MSP (midsagittal/midline) plane & profile view (Matsuda method)

To create the mid-sagittal plane (essential to locate the ANS base/VMJ landmark!), ensure you allocated the **acanthion/ANS tip, subspinale and prosthion** landmarks from _Matsuda_hard_tissue.mrk.json_; then copy and paste the code below. 

<details>
	
<summary>MSP creation</summary>

```python
import slicer
import numpy as np
from qt import QMessageBox

# Get your landmark node (update the name if needed)
lmrks = slicer.util.getNode('Matsuda_hard_tissue')

# Indices you want to use for the best fit plane
indices = [0, 1, 2]

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

# Show a popup message to confirm and remind next steps
msg = QMessageBox()
msg.setIcon(QMessageBox.Information)
msg.setWindowTitle("MSP Plane Created!")
msg.setText(
    "Best-fit 'MSP' plane was created through selected landmarks.\n\n"
    "Next steps:\n"
    "1) Create a side profile model cut using the Dynamic Modeler module and the 'MSP' plane.\n"
    "2) Place the VMJ/anterior nasal spine base landmark."
)
msg.addButton("OK", QMessageBox.AcceptRole)
msg.exec_()
```

</details>

A message box will pop up as a reminder for the next steps. 
(1) Follow the steps detailed in [Make a profile view](#profile-view-model), BUT **use this new plane (MSP) instead if the INB** to slice the skull along and reveal the anterior nasal spine. 

(2) Allocate the base of the ANS/VMJ. 

(3) Copy and paste the snippet below to instrumentally place the mp. Make sure you manually adjust it so that it is on the bone surface - a reminder will pop up!

<details>
	
<summary>Mid-philtrum landmark for Matsuda</summary>

```python

import slicer
from slicer.util import getNode
from qt import QMessageBox

# Get the Markups node for 'Matsuda_hard_tissue'
hardTissueNode = getNode('Matsuda_hard_tissue')

# Get the coordinates of the endpoints at positions 1 (ss) and 2 (pr)
point1 = [0, 0, 0]
point2 = [0, 0, 0]
hardTissueNode.GetNthControlPointPosition(1, point1)  # ss
hardTissueNode.GetNthControlPointPosition(2, point2)  # pr

# Calculate the midpoint
midpoint = [
    (point1[0] + point2[0]) / 2,
    (point1[1] + point2[1]) / 2,
    (point1[2] + point2[2]) / 2
]

# Add the midpoint to 'Matsuda_hard_tissue', label it "mp" and add a description
midpointIndex = hardTissueNode.AddControlPoint(midpoint)
hardTissueNode.SetNthControlPointLabel(midpointIndex, "mp")
hardTissueNode.SetNthControlPointDescription(
    midpointIndex, 
    "Median point midway between ss and pr on bone surface"
)

# Show a popup message to remind the user
msg = QMessageBox()
msg.setIcon(QMessageBox.Information)
msg.setWindowTitle("Reminder: Adjust Midpoint")
msg.setText(
    "Please move the new 'mp' point so it sits on the surface of the maxilla.\n\n"
    "You can use the Markups control point editing tool to adjust its position as needed."
)
msg.addButton("Noted!", QMessageBox.AcceptRole)
msg.exec_()
```

</details>

### Predicting the TNP (MNW) (Matsuda method)

The measurements ENP, ANSP and MPD need to be established to estimate the total napal projection according to Matsuda's method. 



## Bibliography: 

[^1]: [Slicer Script Repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
[^2]: Krogman, W. M. and M. Y. Isçan (1986). The human skeleton in forensic medicine. The human skeleton in forensic medicine. Springfield, IL, Charles C Thomas. 15: 202-208.
[^3]: Taylor, K. T. (2001). Forensic art and illustration, CRC press.
[^4]: Gatliff, B. P. (1984). "Facial sculpture on the skull for identification." American Journal of Forensic Medicine and Pathology 5(4): 327-332.
[^5]: Stephan, C. N., et al. (2003). "Predicting nose projection and pronasale position in facial approximation: a test of published methods and proposal of new guidelines." American Journal of Physical Anthropology: The Official Publication of the American Association of Physical Anthropologists 122(3): 240-250.
[^6]: Henry Gray Anatomy of the Human Body. 1918.[Bartleby link] (https://www.bartleby.com/lit-hub/anatomy-of-the-human-body/fig-173)
[^7]: Rynn, C., Wilkinson, C.M. & Peters, H.L. (2010) "Prediction of nasal morphology from the skull." Forensic Sci Med Pathol 6, 20–34. https://doi.org/10.1007/s12024-009-9124-6
[^8]: Caple, J. and C. N. Stephan (2016). "A standardized nomenclature for craniofacial and facial anthropometry." Int J Legal Med 130(3): 863-879.
[^9]: Martin, R. (1928). Lehrbuch der Anthropologie in systematischer Darstellung: mit besonderer Berücksichtigung der anthropologischen Methoden ; für Studierende, Ärzte und Forschungsreisendechichte, Morphologische Methoden. Jena, Gustav Fisher.	
[^10]: Knussmann, R. (1988). Anthropologie: Handbuch der vergleichenden Biologie des Menschen, G. Fischer.
[^11]: Matsuda, H., et al. (2023). "Simplified Formula for Estimating Nasal Dimensions for 3-Dimensional Facial Reconstruction
among Japanese Adults." Forensic Sciences 3: 381–393.
	
	
