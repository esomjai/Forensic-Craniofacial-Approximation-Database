# The Stephan et al. (2003) method


## Table of Contents
- [Short summary of the Stephan et al. (2003) method](#the-stephan-et-al-2003-method)
- [Landmarks](#landmarks-in-this-guide)
- [Illustration of the method](#illustration-of-the-method)
- [INB Plane](#inb-plane)
- [Establishing the x and y axes](#establishing-the-x-and-y-axes)
- [Creating Point X via AA FHP](#creating-point-x-via-aa-fhp)
- [Measuring the Nasal Bone Angle](#measuring-the-nasal-bone-angle)
- [Setup for Measurement C](#setup-for-measurement-c)
- [Setting Up Lines for Measurement B](#setting-up-lines-for-measurement-b)
- [Apex for Angle D and the Angle Options](#apex-for-angle-d-and-the-angle-options)
  - [Option 1](#option-1)
  - [Option 2](#option-2)
  - [Option 3](#option-3)
- [Measurement E](#measurement-e)
- [Prediction Point - Pronasale](#prediction-point---pronasale)
- [Error Measurements](#error-measurements)
  - [Option 1](#error-measurement-if-option-1-was-used-for-d-nasal-spine-angle)
  - [Option 2](#error-measurement-if-option-2-was-used-for-d-nasal-spine-angle)
  - [Option 3](#error-measurement-if-option-3-was-used-for-d-nasal-spine-angle)
- [Output](#output)
- [Bibliography](#bibliography)

---


 [Stephan et al. 2003](https://doi.org/10.1002/ajpa.10300) compared three methods on lateral cephalogram tracings: method 1 by Gerasimov[^3] (1971); method 2 by Krogman[^4] (1962); method 3 by Prokopec and Ubelaker [^5] (2002); method 4 by George [^6] (1978) and came up with his compound method uniting his findings from the aforementioned studies. 


> [!NOTE]
> The method is illustrated by the 3D Slicer[^1] Sample Data for Post Dental Surgery CT in screenshots. For representing the general population, individuals without facial surgery would be chosen in research - this is only for demonstration purposes. Also note that some landmarks were not visible - again, you would exclude individuals from a study where landmarks cannot be reliably placed, but we proceeded to show our methodology. 
> The performance of this  method was later compared with Rynn et al. (2010)[^7] in a validation study by Mala et al. (2016)[^8].

The guide contains the following steps: 

- Allocating [landmarks (#landmarks-in-this-guide): Please note this file contains landmarks for replicating both methods, but the codes remain unaffected - just omit placing the ones you do not need.   
- Establishing the [INB Plane](#inb-plane)
- Establishing the [x and y axes](#establishing-the-x-and-y-axes) 
- Creating [Point X](#creating-point-x-via-aa-fhp) via AA FHP
- Replicating the original measurements: [nasal bone angle](#measuring-the-nasal-bone-angle); [measurement C](#setup-for-measurement-c); [measurement B](#setting-up-lines-for-measurement-b); [measurement E](#measurement-e)
- Choosing a method for determining the [apex and definition of Angle D](#apex-for-angle-d-and-the-angle-options): Explanation of options for defining Angle D ([Option 1](#option-1), [Option 2](#option-2), [Option 3](#option-3)).  
- Applying the linear regressions by Stephan et al. 2003[^3] to predict the [pronasale](#prediction-point---pronasale) position: divided by the chosen angle D and biological sexes.  
- [Error Measurements](#error-measurements): Steps for error measurement based on chosen angle options ([Option 1](#error-measurement-if-option-1-was-used-for-d-nasal-spine-angle), [Option 2](#error-measurement-if-option-2-was-used-for-d-nasal-spine-angle), [Option 3](#error-measurement-if-option-3-was-used-for-d-nasal-spine-angle)).  
- [Output](#output): Instructions for copying measurements and an example output table.  

> [!WARNING]
> This method also follows first two steps mentioned in the “Start here” section – after loading the DICOM file, please re-orient the scan in the Frankfort horizontal plane. 


### Landmarks in this guide: 

| Position in code | Position in file | Name in file | Landmark name   | Definition                                                                                                                     | Defined by       |
|------------------|------------------|--------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------|------------------|
| 0                | 1                | nasion       | nasion          | Intersection of the nasofrontal sutures in the median plane                                                                    | Rynn et al. 2010[^7] |
| 1                | 2                | inion        | inion           | Median point between the apices of the superior nuchal lines and at the base of the external occipital protuberance (not the tip of the protuberance) | Rynn et al. 2010[^7] |
| 2                | 3                | bregma       | bregma          | Where the sagittal and coronal sutures meet. Impossible to determine in juvenile skulls with anterior fontanelle, or with complete suture obliteration | Rynn et al. 2010[^7] |
| 3                | 4                | prosthion    | prosthion       | Median point between the central incisors on the anterior most margin of the maxillary alveolar rim                            | Rynn et al. 2010[^7] |
| 4                | 5                | rhinion      | rhinion         | Most rostral (end) point on the internasal suture                                                                              | Rynn et al. 2010[^7] |
| 5                | 6                | acanthion    | acanthion       | Most anterior tip of the anterior nasal spine                                                                                 | Rynn et al. 2010[^7] |
| 6                | 7                | point A      | point A         | Point of most flexion on maxilla in profile/The deepest point seen in the profile view below the anterior nasal spine          | George 1987[^6]      |
| 7                | 8                | LL           | left lowest     | The left lowest point on the aperture border in profile view                                                                  | Somjai           |
| 8                | 9                | RL           | right lowest    | The right lowest point on the aperture border in profile view                                                                 | Somjai           |

Download the landmarks file 
[lmrks_Stephan.mrk.json](https://github.com/user-attachments/files/20213400/lmrks_Stephan.mrk.json)

Optional soft tissue landmark file for the [error measurements step](#error-measurements) 


[soft_tissue_Stephan.mrk.json](https://github.com/user-attachments/files/20213398/soft_tissue_Stephan.mrk.json)


| Position in code | Position in file | Name in file | Landmark name   | Definition                                                                                                                     | Defined by       |
|------------------|------------------|--------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------|------------------|
| 0                | 1                | pronasale       | pronasale          | The most   anteriorly protruded point of the apex nasi. In the case of a bifid nose, the   more protruding tip is chosen  |  Caple and   Stephan 2016[^9] | 

### Illustration of the method: 

> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

- [ ] The scan has to be re-aligned in the FHP
- [ ] You should have a Bone and Skin model via segmentation [link to step-by-step](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/003_Roi%20vs%20Segmentation.md)

### INB plane

To help with the side profile, we will establish the “INB” plane as defined by Rynn et al. 2010. 

> a midsagittal plane (INB) which bisected the inion, nasion and bregma

by downloading the [markups file](https://github.com/user-attachments/files/20213400/lmrks_Stephan.mrk.json) for this method and allocating all landmarks on the Bone model or volume. 
This is a pre-emptive measure to facilitate the later steps: by having the INB and FHP as planes and the following codes containing restrictions in the establisment of later reference planes, the "planes" which would correspond to lines in the original study can indeed remain lines. 

<details>
<summary>Code for INB</summary>

```python
#INB plane#

import numpy as np
import slicer

# Get the points from the "lmrks_Stephan" node
hardTissueNode = slicer.util.getNode('lmrks_Stephan')
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


![image](https://github.com/user-attachments/assets/88247495-a178-4e97-8faf-69e60165738d)

View after landmarks were placed, the code above employed and INB extended via the toggles (dots)

The following steps can be executed in one step by copy & pasting the entire code (LINK), but for the sake of explanation, the tutorial breaks it down to its components. The method also splits in execution at measurement e) and depends on the biological sex of the skull, so please keep these in mind when batch processing!!!!

### Establishing the x and y axes
The code creates an x axis in green, defined as a line bisecting the nasion landmark and parallel to the FHP, while being on the INB plane. 
The code creates a y axis in navy, defined as a line bisecting the nasion landmark and perpendicular to the FHP, while being on the INB plane. 

Make sure you have a plane based on the 4 landmarks of the Frankfurt Horizontal Plane and is named "FHP", then employ this snippet: 

<details>
<summary>Code for x and y axes</summary>
	
``` python
import slicer
import numpy as np

# Get the 'FHP' plane node
fhpPlaneNode = slicer.util.getNode('FHP')

# Get the 'INB' plane node
inbPlaneNode = slicer.util.getNode('INB')

# Get the 'lmrks_Stephan' node
hardTissueNode = slicer.util.getNode('lmrks_Stephan')

# Get the position of the first point in 'lmrks_Stephan'
position = [0.0, 0.0, 0.0]
hardTissueNode.GetNthControlPointPosition(0, position)

# Get the normal of the 'FHP' plane
fhpNormal = [0.0, 0.0, 0.0]
fhpPlaneNode.GetNormal(fhpNormal)

# Get the normal of the 'INB' plane
inbNormal = [0.0, 0.0, 0.0]
inbPlaneNode.GetNormal(inbNormal)

# Create a new line node for the 'x axis'
xAxisNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x axis')

# Create a direction vector parallel to the 'FHP' plane
directionX = np.cross(fhpNormal, [1, 0, 0])
if np.linalg.norm(directionX) == 0:  # If the normal is parallel to the x-axis, use a different unit vector
    directionX = np.cross(fhpNormal, [0, 1, 0])
directionX = directionX / np.linalg.norm(directionX)  # Normalize the direction vector

# Set the 'x axis' line to be parallel to the 'FHP' plane and bisect the 'lmrks_Stephan' node at position 0
lineLength = 100  # Half of the total length (200mm)
lineStartX = np.array(position) - lineLength * directionX
lineEndX = np.array(position) + lineLength * directionX
xAxisNode.AddControlPoint(lineStartX)
xAxisNode.AddControlPoint(lineEndX)

# Set the 'x axis' line color to lime
xAxisNode.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)
xAxisNode.GetDisplayNode().SetColor(0.0, 1.0, 0.0)

# Create a new line node for the 'y axis'
yAxisNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y axis')

# Create a direction vector perpendicular to the 'x axis' and lying on the 'INB' plane
directionY = np.cross(directionX, inbNormal)
directionY = directionY / np.linalg.norm(directionY)  # Normalize the direction vector

# Set the 'y axis' line to be perpendicular to the 'x axis' and bisect the 'lmrks_Stephan' node at position 0
lineStartY = np.array(position) - lineLength * directionY
lineEndY = np.array(position) + lineLength * directionY
yAxisNode.AddControlPoint(lineStartY)
yAxisNode.AddControlPoint(lineEndY)

# Set the 'y axis' line color to blue
yAxisNode.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)
yAxisNode.GetDisplayNode().SetColor(0.0, 0.0, 1.0)

```
</details>

Depicted are the INB plane and the two new axes

![image](https://github.com/user-attachments/assets/044df3d4-75d2-4d77-9cf9-bc20acf5254a)



### Creating point X via AA FHP
The code creates a line called "AA FHP" in turquoise along the INB which is parallel to the FHP and bisects point AA - this is later needeed to establish point X. 
The next part of the same code snippet creates a new "point X" node defined as the point that falls on nasion-point A plane (aka perpendicular to y axis, parallel to AA FHP ) at height of point AA (bisects it)

<details>
<summary>Code for Point X</summary>
	
``` python
####Making AA FHP####
import slicer
import numpy as np

# Get the nodes for the existing plane "INB", point "lmrks_Stephan", and line "x axis"
planeNode = slicer.util.getNode('INB')
pointNode = slicer.util.getNode('lmrks_Stephan')
xAxisNode = slicer.util.getNode('x axis')

# Get the plane normal and a point on the plane
planeNormal = np.array(planeNode.GetNormal())
planePoint = np.array(planeNode.GetOrigin())

# Get the direction vector of the line "x axis"
xAxisStart = np.array(xAxisNode.GetNthControlPointPosition(0))
xAxisEnd = np.array(xAxisNode.GetNthControlPointPosition(1))
lineDirection = xAxisEnd - xAxisStart
lineDirection /= np.linalg.norm(lineDirection)  # Normalize the direction vector

# Get the position of the point in "lmrks_Stephan" at position 7
hardTissuePoint = np.array(pointNode.GetNthControlPointPosition(7))

# Define the start and end points of the new line "AA FHP" to bisect the lmrks_Stephan point
newLineStart = hardTissuePoint - lineDirection * 100  # Half of 200mm
newLineEnd = hardTissuePoint + lineDirection * 100  # Half of 200mm

# Project the start and end points onto the "INB" plane
def project_point_onto_plane(point, plane_point, plane_normal):
    point_to_plane = point - plane_point
    distance = np.dot(point_to_plane, plane_normal)
    projected_point = point - distance * plane_normal
    return projected_point

newLineStart = project_point_onto_plane(newLineStart, planePoint, planeNormal)
newLineEnd = project_point_onto_plane(newLineEnd, planePoint, planeNormal)

# Create the new line "AA FHP"
newLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'AA FHP')
newLineNode.AddControlPoint(newLineStart)
newLineNode.AddControlPoint(newLineEnd)

# Set the color of the new line to turquoise
displayNode = newLineNode.GetDisplayNode()
displayNode.SetSelectedColor(0, 1, 1)  # RGB for turquoise

print("New line 'AA FHP' created successfully on the 'INB' plane, bisecting the point in 'lmrks_Stephan' at position 7, parallel to the 'x axis', with a length of 200mm and color turquoise.")


import slicer
import numpy as np

# Get the nodes for the existing points and lines
hardTissueNode = slicer.util.getNode('lmrks_Stephan')  # Main node containing multiple control points
aaFhpNode = slicer.util.getNode('AA FHP')

# Get the positions of the control points for the new line "n-point A)"
startPoint = np.array(hardTissueNode.GetNthControlPointPosition(0))
endPoint = np.array(hardTissueNode.GetNthControlPointPosition(6))

# Calculate the direction vector and elongate it to 200 mm
directionVector = endPoint - startPoint
directionVector = directionVector / np.linalg.norm(directionVector) * 200

# Calculate the new end point for the elongated line
elongatedEndPoint = startPoint + directionVector

# Create a new line node called "n-point A)"
nPointANode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'n-point A)')
nPointANode.AddControlPoint(startPoint)
nPointANode.AddControlPoint(elongatedEndPoint)

# Get the direction vector and a point on the "AA FHP" line
aaFhpStart = np.array(aaFhpNode.GetNthControlPointPosition(0))
aaFhpEnd = np.array(aaFhpNode.GetNthControlPointPosition(1))
aaFhpDirection = aaFhpEnd - aaFhpStart

# Get the direction vector and a point on the "n-point A)" line
nPointAStart = startPoint
nPointAEnd = elongatedEndPoint
nPointADirection = nPointAEnd - nPointAStart

# Solve for the intersection point
# We need to find t and s such that:
# aaFhpStart + t * aaFhpDirection = nPointAStart + s * nPointADirection

# Set up the system of linear equations
A = np.array([aaFhpDirection, -nPointADirection]).T
b = nPointAStart - aaFhpStart

# Solve for t and s
t, s = np.linalg.lstsq(A, b, rcond=None)[0]

# Calculate the intersection point
intersectionPoint = aaFhpStart + t * aaFhpDirection

# Create a new node called "Point X" at the intersection point
pointXNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'Point X')
pointXNode.AddControlPoint(intersectionPoint)

print("New node 'Point X' created successfully at the intersection of 'AA FHP' and 'n-point A)'.")

```
</details>

![image](https://github.com/user-attachments/assets/b32dfaef-65af-451d-b264-98ff0d62aaf5)

Depicted are the new point X node at the intersection of the AA FHP and the nasion-point A line (red) and the turqoise AA FHP line.

### Measuring the nasal bone angle
This angle is described as the **a)** variable in the original study as measured from nasion to rhinion, from Frankfurt horizontal. Based on our previously created lines, this means that the apex of the angle is at the nasion, and the angle is between the anterior end of the x axis (which already bisects the nasion and is parallelll to the FHP) and the rhinion.

<details>
<summary>Code for nasal bone angle</summary>
	
``` python
####Nasal bone angle a) ####
import slicer
import numpy as np

# Get the nodes for the existing points and lines
hardTissueNode = slicer.util.getNode('lmrks_Stephan')
xAxisNode = slicer.util.getNode('x axis')

# Get the positions of the control points
apexPoint = np.array(hardTissueNode.GetNthControlPointPosition(0))
firstControlPoint = np.array(xAxisNode.GetNthControlPointPosition(1))
thirdControlPoint = np.array(hardTissueNode.GetNthControlPointPosition(4))

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'A) nasal bone angle')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Second control point (apex)
angleNode.AddControlPoint(thirdControlPoint)  # Third control point

print("New angle 'a) nasal bone angle' created successfully.")
```
</details>

![image](https://github.com/user-attachments/assets/326ec4de-8381-49ce-be96-31f6d4ad71b8)


### Setup for measurement C - LL and LR axes, rhi c) and c)
The following steps prepare to execute  measurement C) in the original study, defined as _distance from rhinion to most posterior point on nasal aperture border, measured perpendicular to nasion/prosthion plane_
The LL and LR axes also help with the "line-instead-plane" process lines by bisecting the most posterior part of the nasal aperture from lateral view on the left and right, perpendicular to AA FHP line and projected on the INB plane – these are for measurement c) later on (both axes are defines as_The shortest (perpendicular) distance between the rhinion and the most posterior point of the nasal aperture from side view_ (LL in the example)) and should be very similar, almost overlapping, therefore only one of them is followed through in the later codes. If the ones in your patient do not overlap, consider doing both sides individually. 

<details>
<summary>Code to create c)</summary>

``` python
###LL and RL axes#####
import slicer
import numpy as np

# Function to project a line onto a plane
def project_line_onto_plane(line, plane):
    plane_origin = np.zeros(3)
    plane_normal = np.zeros(3)
    plane.GetOriginWorld(plane_origin)
    plane.GetNormalWorld(plane_normal)

    projected_points = []
    for i in range(line.GetNumberOfControlPoints()):
        point = np.zeros(3)
        line.GetNthControlPointPositionWorld(i, point)
        distance_from_plane = np.dot(np.subtract(point, plane_origin), plane_normal)
        projected_point = point - plane_normal * distance_from_plane
        projected_points.append(projected_point)

    return projected_points

# Access the points stored in "lmrks_Stephan"
hard_tissue = slicer.util.getNode('lmrks_Stephan')
point_8 = [0.0, 0.0, 0.0]
hard_tissue.GetNthControlPointPosition(8, point_8)
point_9 = [0.0, 0.0, 0.0]
hard_tissue.GetNthControlPointPosition(9, point_9)

# Access the "AA FHP" line points
AA_FHP = slicer.util.getNode('AA FHP')
AA_FHP_point_1 = [0.0, 0.0, 0.0]
AA_FHP.GetNthControlPointPosition(0, AA_FHP_point_1)
AA_FHP_point_2 = [0.0, 0.0, 0.0]
AA_FHP.GetNthControlPointPosition(1, AA_FHP_point_2)

# Calculate the direction vector of the "AA FHP" line
direction_AA_FHP = [
    AA_FHP_point_2[0] - AA_FHP_point_1[0],
    AA_FHP_point_2[1] - AA_FHP_point_1[1],
    AA_FHP_point_2[2] - AA_FHP_point_1[2]
]

# Access the normal vector of the "INB" plane
INB = slicer.util.getNode('INB')
normal_INB = [0.0, 0.0, 0.0]
INB.GetNormal(normal_INB)

# Calculate the cross product to get the perpendicular direction
perpendicular_direction = np.cross(direction_AA_FHP, normal_INB)
perpendicular_direction = perpendicular_direction / np.linalg.norm(perpendicular_direction)  # Normalize

# Scale the perpendicular direction to 100mm (half of 200mm)
scaled_direction = perpendicular_direction * 100

# Create "LL y axis"
LL_y_axis = slicer.vtkMRMLMarkupsLineNode()
LL_y_axis.SetName('LL y axis')
slicer.mrmlScene.AddNode(LL_y_axis)
LL_y_axis.AddControlPoint(
    point_8[0] - scaled_direction[0],
    point_8[1] - scaled_direction[1],
    point_8[2] - scaled_direction[2]
)  # Start point
LL_y_axis.AddControlPoint(
    point_8[0] + scaled_direction[0],
    point_8[1] + scaled_direction[1],
    point_8[2] + scaled_direction[2]
)  # End point

# Create "RL y axis"
RL_y_axis = slicer.vtkMRMLMarkupsLineNode()
RL_y_axis.SetName('RL y axis')
slicer.mrmlScene.AddNode(RL_y_axis)
RL_y_axis.AddControlPoint(
    point_9[0] - scaled_direction[0],
    point_9[1] - scaled_direction[1],
    point_9[2] - scaled_direction[2]
)  # Start point
RL_y_axis.AddControlPoint(
    point_9[0] + scaled_direction[0],
    point_9[1] + scaled_direction[1],
    point_9[2] + scaled_direction[2]
)  # End point

# Project 'LL y axis' onto 'INB' plane
projected_points_ll = project_line_onto_plane(LL_y_axis, INB)

# Update the 'LL y axis' line with the projected points
LL_y_axis.RemoveAllControlPoints()
for point in projected_points_ll:
    LL_y_axis.AddControlPoint(point)

# Set the color of the 'LL y axis' line to green
LL_y_axis.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)
LL_y_axis.GetDisplayNode().SetColor(0.0, 1.0, 0.0)

# Project 'RL y axis' onto 'INB' plane
projected_points_rl = project_line_onto_plane(RL_y_axis, INB)

# Update the 'RL y axis' line with the projected points
RL_y_axis.RemoveAllControlPoints()
for point in projected_points_rl:
    RL_y_axis.AddControlPoint(point)

# Set the color of the 'RL y axis' line to orange
RL_y_axis.GetDisplayNode().SetSelectedColor(1.0, 0.5, 0.0)
RL_y_axis.GetDisplayNode().SetColor(1.0, 0.5, 0.0)


#### rhi C####
import slicer
import numpy as np

# Function to project a point onto a plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point_to_origin = np.subtract(point, plane_origin)
    distance_from_plane = np.dot(point_to_origin, plane_normal)
    projected_point = np.subtract(point, plane_normal * distance_from_plane)
    return projected_point

# Access the points stored in "lmrks_Stephan"
hard_tissue = slicer.util.getNode('lmrks_Stephan')
point_4 = [0.0, 0.0, 0.0]
hard_tissue.GetNthControlPointPosition(4, point_4)

# Access the "LL y axis" line points
LL_y_axis = slicer.util.getNode('LL y axis')
LL_y_axis_point_1 = [0.0, 0.0, 0.0]
LL_y_axis.GetNthControlPointPosition(0, LL_y_axis_point_1)
LL_y_axis_point_2 = [0.0, 0.0, 0.0]
LL_y_axis.GetNthControlPointPosition(1, LL_y_axis_point_2)

# Calculate the direction vector of the "LL y axis" line
direction_LL_y_axis = np.subtract(LL_y_axis_point_2, LL_y_axis_point_1)
direction_LL_y_axis = direction_LL_y_axis / np.linalg.norm(direction_LL_y_axis)  # Normalize

# Access the "INB" plane
INB = slicer.util.getNode('INB')
plane_origin = np.zeros(3)
plane_normal = np.zeros(3)
INB.GetOriginWorld(plane_origin)
INB.GetNormalWorld(plane_normal)

# Project the point stored in "lmrks_Stephan" at position 4 onto the "INB" plane
projected_point_4 = project_point_onto_plane(point_4, plane_origin, plane_normal)

# Calculate the start and end points of the new line "c) rhi"
start_point = np.subtract(projected_point_4, direction_LL_y_axis * 100)
end_point = np.add(projected_point_4, direction_LL_y_axis * 100)

# Create "c) rhi" line
c_rhi = slicer.vtkMRMLMarkupsLineNode()
c_rhi.SetName('c) rhi')
slicer.mrmlScene.AddNode(c_rhi)
c_rhi.AddControlPoint(start_point)
c_rhi.AddControlPoint(end_point)

# Set the color of the "c) rhi" line to pink
c_rhi.GetDisplayNode().SetSelectedColor(1.0, 0.0, 1.0)
c_rhi.GetDisplayNode().SetColor(1.0, 0.0, 1.0)

##### measurement C)####
import slicer
import numpy as np

# Function to project a point onto a plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point_to_origin = np.subtract(point, plane_origin)
    distance_from_plane = np.dot(point_to_origin, plane_normal)
    projected_point = np.subtract(point, plane_normal * distance_from_plane)
    return projected_point

# Function to calculate the closest points between two lines at a specific level
def closest_points_between_lines_at_level(line1, line2, level_point):
    point1 = np.array([0.0, 0.0, 0.0])
    point2 = np.array([0.0, 0.0, 0.0])
    line1.GetNthControlPointPosition(0, point1)
    line1.GetNthControlPointPosition(1, point2)
    direction1 = point2 - point1

    point3 = np.array([0.0, 0.0, 0.0])
    point4 = np.array([0.0, 0.0, 0.0])
    line2.GetNthControlPointPosition(0, point3)
    line2.GetNthControlPointPosition(1, point4)
    direction2 = point4 - point3

    # Calculate the vector between the two lines
    vector_between_lines = point3 - point1

    # Calculate the cross product of the direction vectors
    cross_product = np.cross(direction1, direction2)
    cross_product_norm = np.linalg.norm(cross_product)

    # Calculate the points on each line that are closest to the level point
    t1 = np.dot(level_point - point1, direction1) / np.dot(direction1, direction1)
    closest_point_line1 = point1 + t1 * direction1

    t2 = np.dot(level_point - point3, direction2) / np.dot(direction2, direction2)
    closest_point_line2 = point3 + t2 * direction2

    return closest_point_line1, closest_point_line2

# Get the 'lmrks_Stephan' node
hardTissueNode = slicer.util.getNode('lmrks_Stephan')

# Get the position of the fourth point in 'lmrks_Stephan'
position4 = [0.0, 0.0, 0.0]
hardTissueNode.GetNthControlPointPosition(4, position4)

# Get the 'c) rhi' line node
cRhiLineNode = slicer.util.getNode('c) rhi')

# Get the 'LL y axis' line node
llYAxisNode = slicer.util.getNode('LL y axis')

# Calculate the closest points between 'c) rhi' and 'LL y axis' at the level of 'lmrks_Stephan' position 4
closest_point_c_rhi, closest_point_ll_y_axis = closest_points_between_lines_at_level(cRhiLineNode, llYAxisNode, position4)

# Create a new line node for 'C)'
cLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'C)')
cLineNode.AddControlPoint(closest_point_c_rhi)
cLineNode.AddControlPoint(closest_point_ll_y_axis)

# Set the 'C)' line color to depict the shortest distance
cLineNode.GetDisplayNode().SetSelectedColor(1.0, 0.0, 0.0)  # Red color
cLineNode.GetDisplayNode().SetColor(1.0, 0.0, 0.0)

```
</details>

Depicted are the RL and LL landmarks, note the proximity of the orange (RL y axis) and neon green (LL y axis) lines

  ![image](https://github.com/user-attachments/assets/acfe63ee-d9dd-416f-8bae-1401dad05846)
  
See how "rhi c)" bisects the rhinion and is parallell to the LL y  axis

![image](https://github.com/user-attachments/assets/01540185-7601-4eac-859a-17b16f070969)

Measurement C is shown in red

![image](https://github.com/user-attachments/assets/14b0fcce-8a85-42e4-9f1a-74eb30003022)



### Setting up lines "for b-ac" and "for b-LL" to create measurement B)
Line “for b-ac” is a line perpendicular to AA FHP which bisects the acanthion; line “for b – LL” is a line perpendicular to AA FHP which bisects the LL point and is projected onto the “INB” plane. Line B should appear in magenta and represents the shortest distance between the lines.

<details>
<summary>Code to create b)</summary>
``` python
import slicer
import numpy as np
# Get the 'lmrks_Stephan' node
hardTissueNode = slicer.util.getNode('lmrks_Stephan')
# Get the position of the fifth point in 'lmrks_Stephan'
position = [0.0, 0.0, 0.0]
hardTissueNode.GetNthControlPointPosition(5, position)
# Get the 'AA FHP' line node
aaFhpLineNode = slicer.util.getNode('AA FHP')
# Get the positions of the control points of 'AA FHP'
point1 = [0.0, 0.0, 0.0]
point2 = [0.0, 0.0, 0.0]
aaFhpLineNode.GetNthControlPointPosition(0, point1)
aaFhpLineNode.GetNthControlPointPosition(1, point2)
# Calculate the direction vector of 'AA FHP'
directionAA = np.array(point2) - np.array(point1)
directionAA = directionAA / np.linalg.norm(directionAA)  # Normalize the direction vector
# Create a direction vector perpendicular to 'AA FHP'
perpendicularDirection = np.cross(directionAA, [1, 0, 0])
if np.linalg.norm(perpendicularDirection) == 0:  # If the direction is parallel to the x-axis, use a different unit vector
    perpendicularDirection = np.cross(directionAA, [0, 1, 0])
perpendicularDirection = perpendicularDirection / np.linalg.norm(perpendicularDirection)  # Normalize the direction vector
# Create a new line node for 'for b - ac'
newLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'for b - ac')
# Set the 'for b - ac' line to be perpendicular to 'AA FHP' and bisect the 'lmrks_Stephan' node at position 6
lineLength = 100  # Half of the total length (200mm)
lineStart = np.array(position) - lineLength * perpendicularDirection
lineEnd = np.array(position) + lineLength * perpendicularDirection
newLineNode.AddControlPoint(lineStart)
newLineNode.AddControlPoint(lineEnd)
# Set the 'for b - ac' line color to yellow
newLineNode.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)
newLineNode.GetDisplayNode().SetColor(1.0, 1.0, 0.0)
##########################################################
import slicer
import numpy as np
# Get the 'lmrks_Stephan' node
hardTissueNode = slicer.util.getNode('lmrks_Stephan')
if not hardTissueNode:
    raise ValueError("Node 'lmrks_Stephan' not found")
# Get the positions of the eighth and ninth points in 'lmrks_Stephan'
position8 = [0.0, 0.0, 0.0]
position9 = [0.0, 0.0, 0.0]
if hardTissueNode.GetNumberOfControlPoints() > 8:
    hardTissueNode.GetNthControlPointPosition(8, position8)
    hardTissueNode.GetNthControlPointPosition(9, position9)
else:
    raise ValueError("Not enough control points in 'lmrks_Stephan'")
# Calculate the midpoint between positions 8 and 9
midpoint89 = (np.array(position8) + np.array(position9)) / 2
# Get the 'AA FHP' line node
aaFhpLineNode = slicer.util.getNode('AA FHP')
if not aaFhpLineNode:
    raise ValueError("Node 'AA FHP' not found")
# Get the positions of the control points of 'AA FHP'
point1 = [0.0, 0.0, 0.0]
point2 = [0.0, 0.0, 0.0]
if aaFhpLineNode.GetNumberOfControlPoints() > 1:
    aaFhpLineNode.GetNthControlPointPosition(0, point1)
    aaFhpLineNode.GetNthControlPointPosition(1, point2)
else:
    raise ValueError("Not enough control points in 'AA FHP'")
# Calculate the direction vector of 'AA FHP'
directionAA = np.array(point2) - np.array(point1)
directionAA = directionAA / np.linalg.norm(directionAA)  # Normalize the direction vector
# Create a direction vector perpendicular to 'AA FHP'
perpendicularDirection = np.cross(directionAA, [1, 0, 0])
if np.linalg.norm(perpendicularDirection) == 0:  # If the direction is parallel to the x-axis, use a different unit vector
    perpendicularDirection = np.cross(directionAA, [0, 1, 0])
perpendicularDirection = perpendicularDirection / np.linalg.norm(perpendicularDirection)  # Normalize the direction vector
# Create a new line node for 'for b - LL'
newLineNodeLL = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'for b - LL')
# Set the 'for b - LL' line to be perpendicular to 'AA FHP' and bisect the midpoint between positions 8 and 9
lineLength = 100  # Half of the total length (200mm)
lineStartLL = midpoint89 - lineLength * perpendicularDirection
lineEndLL = midpoint89 + lineLength * perpendicularDirection
newLineNodeLL.AddControlPoint(lineStartLL)
newLineNodeLL.AddControlPoint(lineEndLL)
# Set the 'for b - LL' line color to yellow
newLineNodeLL.GetDisplayNode().SetSelectedColor(1.0, 1.0, 0.0)
newLineNodeLL.GetDisplayNode().SetColor(1.0, 1.0, 0.0)
# Create a new line node for 'RL-LL'
newLineNodeRL_LL = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'RL-LL')
# Set the 'RL-LL' line to connect positions 8 and 9
newLineNodeRL_LL.AddControlPoint(position8)
newLineNodeRL_LL.AddControlPoint(position9)
# Set the 'RL-LL' line color to blue
newLineNodeRL_LL.GetDisplayNode().SetSelectedColor(0.0, 0.0, 1.0)
newLineNodeRL_LL.GetDisplayNode().SetColor(0.0, 0.0, 1.0)
# Create a new fiducial node for 'mid LL/RL'
midpointFiducial = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'mid LL/RL')
# Add the midpoint between positions 8 and 9 as a fiducial point
midpointFiducial.AddControlPoint(midpoint89)
# Set the fiducial color to green
midpointFiducial.GetDisplayNode().SetSelectedColor(0.0, 1.0, 0.0)
midpointFiducial.GetDisplayNode().SetColor(0.0, 1.0, 0.0)

#############################################

import slicer
import numpy as np
#Function to project a point onto a plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point_to_origin = np.subtract(point, plane_origin)
    distance_from_plane = np.dot(point_to_origin, plane_normal)
    projected_point = np.subtract(point, plane_normal * distance_from_plane)
    return projected_point
#Function to calculate the closest points between two lines at a specific level
def closest_points_between_lines_at_level(line1, line2, level_point):
    point1 = np.array([0.0, 0.0, 0.0])
    point2 = np.array([0.0, 0.0, 0.0])
    line1.GetNthControlPointPosition(0, point1)
    line1.GetNthControlPointPosition(1, point2)
    direction1 = point2 - point1

    point3 = np.array([0.0, 0.0, 0.0])
    point4 = np.array([0.0, 0.0, 0.0])
    line2.GetNthControlPointPosition(0, point3)
    line2.GetNthControlPointPosition(1, point4)
    direction2 = point4 - point3

    # Calculate the vector between the two lines
    vector_between_lines = point3 - point1

    # Calculate the cross product of the direction vectors
    cross_product = np.cross(direction1, direction2)
    cross_product_norm = np.linalg.norm(cross_product)

    # Calculate the points on each line that are closest to the level point
    t1 = np.dot(level_point - point1, direction1) / np.dot(direction1, direction1)
    closest_point_line1 = point1 + t1 * direction1

    t2 = np.dot(level_point - point3, direction2) / np.dot(direction2, direction2)
    closest_point_line2 = point3 + t2 * direction2

    return closest_point_line1, closest_point_line2

#Get the 'lmrks_Stephan' node
hardTissueNode = slicer.util.getNode('lmrks_Stephan')

#Get the position of the seventh point in 'lmrks_Stephan'
position7 = [0.0, 0.0, 0.0]
hardTissueNode.GetNthControlPointPosition(7, position7)

#Get the 'for b - ac' line node
forBAcLineNode = slicer.util.getNode('for b - ac')

#Get the 'for b - LL' line node
forBLLLineNode = slicer.util.getNode('for b - LL')

#Calculate the closest points between 'for b - ac' and 'for b - LL' at the level of 'lmrks_Stephan' position 7
closest_point_for_b_ac, closest_point_for_b_ll = closest_points_between_lines_at_level(forBAcLineNode, forBLLLineNode, position7)

#Create a new line node for 'B)'
bLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'B)')
bLineNode.AddControlPoint(closest_point_for_b_ac)
bLineNode.AddControlPoint(closest_point_for_b_ll)

#Set the 'B)' line color to magenta
bLineNode.GetDisplayNode().SetSelectedColor(1.0, 0.0, 1.0)
bLineNode.GetDisplayNode().SetColor(1.0, 0.0, 1.0)

```
</details>


![image](https://github.com/user-attachments/assets/b70cd603-050c-423f-b31f-364063a410f9)


### Apex for angle D) and the angle
The exact position of the e) angle apex is quite quite difficult to distinguish from the figure provided in the study (Figure 5 in the original) and there is no further explanation as to the definition of the exact position of the apex of the angle. I am providing codes for both instances; therefore consider which one you choose when running the entire code all at once!

The way I see it, there are two options to follow based on the graphic depiction by Stephan et al. 2003: 

<details>
<summary>Option 1</summary>  
 the "base" of the angle is the "FHP AA" line (so we take the anterior end as point 1) AND the apex of angle e) is point X

```python
import slicer
import numpy as np

# Get the nodes for the existing points and lines
hardTissueNode = slicer.util.getNode('lmrks_Stephan')  # Main node containing multiple control points
aaFHPNode = slicer.util.getNode('AA FHP')
XNode = slicer.util.getNode('Point X')

# Get the positions of the control points
firstControlPoint =   np.array(hardTissueNode.GetNthControlPointPosition(5))# First control point ( 'aca')
apexPoint = np.array(XNode.GetNthControlPointPosition(0))  #X
thirdControlPoint = np.array(aaFHPNode.GetNthControlPointPosition(1))   # Third control point

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'D) nasal spine angle - opt 1')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Apex point
angleNode.AddControlPoint(thirdControlPoint)  # Third control point as the ant end of FHP AA
```

Zoomed in image showing the three points of the nasal spine angle for option 1. Note that the model's opacity was reduced to 0.3 for visibility.

![image](https://github.com/user-attachments/assets/8ee8c877-4c5c-455c-92f3-a664006e78e1)

</details>

<details>
<summary>Option 2</summary> 

the "base" of the angle is a new line - bisecting point A and is also parallell to the FHP AND the apex is where the most posterior point of the nasal aperture (in our case, this is the "LL y axis") meets this line

```python
import slicer
import numpy as np

# Get the nodes for the existing plane "INB", point "lmrks_Stephan", and line "x axis"
planeNode = slicer.util.getNode('INB')
pointNode = slicer.util.getNode('lmrks_Stephan')
xAxisNode = slicer.util.getNode('x axis')

# Get the plane normal and a point on the plane
planeNormal = np.array(planeNode.GetNormal())
planePoint = np.array(planeNode.GetOrigin())

# Get the direction vector of the line "x axis"
xAxisStart = np.array(xAxisNode.GetNthControlPointPosition(0))
xAxisEnd = np.array(xAxisNode.GetNthControlPointPosition(1))
lineDirection = xAxisEnd - xAxisStart
lineDirection /= np.linalg.norm(lineDirection)  # Normalize the direction vector

# Get the position of the point in "lmrks_Stephan" at position 6
hardTissuePoint = np.array(pointNode.GetNthControlPointPosition(6))

# Define the start and end points of the new line "A FHP" to bisect the lmrks_Stephan point
newLineStart = hardTissuePoint - lineDirection * 100  # Half of 200mm
newLineEnd = hardTissuePoint + lineDirection * 100  # Half of 200mm

# Project the start and end points onto the "INB" plane
def project_point_onto_plane(point, plane_point, plane_normal):
    point_to_plane = point - plane_point
    distance = np.dot(point_to_plane, plane_normal)
    projected_point = point - distance * plane_normal
    return projected_point

newLineStart = project_point_onto_plane(newLineStart, planePoint, planeNormal)
newLineEnd = project_point_onto_plane(newLineEnd, planePoint, planeNormal)

# Create the new line "A FHP"
newLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'A FHP')
newLineNode.AddControlPoint(newLineStart)
newLineNode.AddControlPoint(newLineEnd)

# Set the color of the new line to hot pink
displayNode = newLineNode.GetDisplayNode()
displayNode.SetSelectedColor(1, 0.41, 0.71)  # RGB for hot pink

print("New line 'A FHP' created successfully on the 'INB' plane, bisecting the point in 'lmrks_Stephan' at position 6, parallel to the 'x axis', with a length of 200mm and color hot pink.")

import slicer
import numpy as np

# Get the nodes for the existing lines "LL y axis" and "A FHP"
llYAxisNode = slicer.util.getNode('LL y axis')
aFhpNode = slicer.util.getNode('A FHP')
hardTissueNode = slicer.util.getNode('lmrks_Stephan')

# Get the direction vector and a point on the "LL y axis" line
llYAxisStart = np.array(llYAxisNode.GetNthControlPointPosition(0))
llYAxisEnd = np.array(llYAxisNode.GetNthControlPointPosition(1))
llYAxisDirection = llYAxisEnd - llYAxisStart

# Get the direction vector and a point on the "A FHP" line
aFhpStart = np.array(aFhpNode.GetNthControlPointPosition(0))
aFhpEnd = np.array(aFhpNode.GetNthControlPointPosition(1))
aFhpDirection = aFhpEnd - aFhpStart

# Solve for the intersection point
# We need to find t and s such that:
# llYAxisStart + t * llYAxisDirection = aFhpStart + s * aFhpDirection

# Set up the system of linear equations
A = np.array([llYAxisDirection, -aFhpDirection]).T
b = aFhpStart - llYAxisStart

# Solve for t and s
t, s = np.linalg.lstsq(A, b, rcond=None)[0]

# Calculate the intersection point
intersectionPoint = llYAxisStart + t * llYAxisDirection

# Create a new node called "LL A FHP intersection" at the intersection point
pointXNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'LL A FHP intersection')
pointXNode.AddControlPoint(intersectionPoint)

# Get the position of the aca point in "lmrks_Stephan" at position 5
acaPoint = np.array(hardTissueNode.GetNthControlPointPosition(5))

# Get the position of the "A FHP" line's coordinate at position 1
aFhpLinePoint1 = np.array(aFhpNode.GetNthControlPointPosition(1))

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'D) nasal spine angle - opt 2')
angleNode.AddControlPoint(acaPoint)         # First control point (aca point)
angleNode.AddControlPoint(intersectionPoint) # Apex point (intersection of LL y axis and A FHP)
angleNode.AddControlPoint(aFhpLinePoint1)   # Third control point (A FHP line's coordinate at position 1)

print("New angle node 'D) nasal spine angle - opt 2' created successfully with apex at the intersection of 'LL y axis' and 'A FHP'.")

```
Zoomed in image showing the three points of the nasal spine angle for option 2. Note that the model's opacity was reduced to 0.3 for visibility.

![image](https://github.com/user-attachments/assets/10c00138-089e-461e-afeb-fe94965e9229)

</details>

There is a third option  based on the graphic s provided by Mala et al. 2016[^8] : 

**IN PROGRESS - Waiting for author's reply**

The script creates 2 parallel lines along the A FHP (line parallel to the FHP at the level of point A) and the aca FHP (line parallel to the FHP at the level of the acanthion), each beginning where the "for b - ac" line intersects them, with the length of the B) measurement doubled. the second arm of the angle is then defined by the anterior endpoint of the new "Mala 2B A FHP" line. The angle will be named "D) nasal spine angle - opt 3"

FYI: you may already have an A FHP line and/or LL A FHP intersection point when creating the angle using the 1st option, but it is integrated into this script in case you do not.

<details>
<summary>Code to create Mala's nasal spine angle - option 3</summary>
	
```python
import slicer
import numpy as np

# Get the nodes for the existing plane "INB", point "lmrks_Stephan", and line "x axis"
planeNode = slicer.util.getNode('INB')
pointNode = slicer.util.getNode('lmrks_Stephan')
xAxisNode = slicer.util.getNode('x axis')

# Get the plane normal and a point on the plane
planeNormal = np.array(planeNode.GetNormal())
planePoint = np.array(planeNode.GetOrigin())

# Get the direction vector of the line "x axis"
xAxisStart = np.array(xAxisNode.GetNthControlPointPosition(0))
xAxisEnd = np.array(xAxisNode.GetNthControlPointPosition(1))
lineDirection = xAxisEnd - xAxisStart
lineDirection /= np.linalg.norm(lineDirection)  # Normalize the direction vector

# Get the position of the point in "lmrks_Stephan" at position 5
hardTissuePoint = np.array(pointNode.GetNthControlPointPosition(5))

# Define the start and end points of the new line "aca FHP" to bisect the lmrks_Stephan point
acaFHPLineStart = hardTissuePoint - lineDirection * 100  # Half of 200mm
acaFHPLineEnd = hardTissuePoint + lineDirection * 100  # Half of 200mm

# Project the start and end points onto the "INB" plane
def project_point_onto_plane(point, plane_point, plane_normal):
    point_to_plane = point - plane_point
    distance = np.dot(point_to_plane, plane_normal)
    projected_point = point - distance * plane_normal
    return projected_point

acaFHPLineStart = project_point_onto_plane(acaFHPLineStart, planePoint, planeNormal)
acaFHPLineEnd = project_point_onto_plane(acaFHPLineEnd, planePoint, planeNormal)

# Create the new line "aca FHP"
acaFHPLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'aca FHP')
acaFHPLineNode.AddControlPoint(acaFHPLineStart)
acaFHPLineNode.AddControlPoint(acaFHPLineEnd)

# Retrieve the display node
displayNode = acaFHPLineNode.GetDisplayNode()

if displayNode:
    displayNode.SetColor(128/255, 0, 128/255)  # Set main color
    displayNode.SetSelectedColor(128/255, 0, 128/255)  # Ensure selected color matches
    displayNode.SetOpacity(1)  # Ensure visibility

    # Force full refresh
    slicer.app.processEvents()
    acaFHPLineNode.Modified()
else:
    print("Error: Display node not found for 'aca FHP'")
	
import slicer
import numpy as np

# Get the nodes for the existing plane "INB", point "lmrks_Stephan", and line "x axis"
planeNode = slicer.util.getNode('INB')
pointNode = slicer.util.getNode('lmrks_Stephan')
xAxisNode = slicer.util.getNode('x axis')

# Get the plane normal and a point on the plane
planeNormal = np.array(planeNode.GetNormal())
planePoint = np.array(planeNode.GetOrigin())

# Get the direction vector of the line "x axis"
xAxisStart = np.array(xAxisNode.GetNthControlPointPosition(0))
xAxisEnd = np.array(xAxisNode.GetNthControlPointPosition(1))
lineDirection = xAxisEnd - xAxisStart
lineDirection /= np.linalg.norm(lineDirection)  # Normalize the direction vector

# Get the position of the point in "lmrks_Stephan" at position 6
hardTissuePoint = np.array(pointNode.GetNthControlPointPosition(6))

# Define the start and end points of the new line "A FHP" to bisect the lmrks_Stephan point
newLineStart = hardTissuePoint - lineDirection * 100  # Half of 200mm
newLineEnd = hardTissuePoint + lineDirection * 100  # Half of 200mm

# Project the start and end points onto the "INB" plane
def project_point_onto_plane(point, plane_point, plane_normal):
    point_to_plane = point - plane_point
    distance = np.dot(point_to_plane, plane_normal)
    projected_point = point - distance * plane_normal
    return projected_point

newLineStart = project_point_onto_plane(newLineStart, planePoint, planeNormal)
newLineEnd = project_point_onto_plane(newLineEnd, planePoint, planeNormal)

# Create the new line "A FHP"
newLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'A FHP')
newLineNode.AddControlPoint(newLineStart)
newLineNode.AddControlPoint(newLineEnd)

# Set the color of the new line to hot pink
displayNode = newLineNode.GetDisplayNode()
displayNode.SetSelectedColor(1, 0.41, 0.71)  # RGB for hot pink

import slicer

# Get the point from "lmrks_Stephan" in position 5
point = slicer.util.getNode('lmrks_Stephan').GetNthControlPointPosition(5)

# Get the line "aca FHP"
line_aca_fhp = slicer.util.getNode('aca FHP')

# Calculate the direction vector of "aca FHP"
start_point_aca_fhp = [0, 0, 0]
end_point_aca_fhp = [0, 0, 0]
line_aca_fhp.GetNthControlPointPosition(0, start_point_aca_fhp)
line_aca_fhp.GetNthControlPointPosition(1, end_point_aca_fhp)
direction_vector_aca_fhp = [end_point_aca_fhp[i] - start_point_aca_fhp[i] for i in range(3)]

# Normalize the direction vector
length_direction_vector_aca_fhp = sum([direction_vector_aca_fhp[i] ** 2 for i in range(3)]) ** 0.5
direction_vector_aca_fhp = [direction_vector_aca_fhp[i] / length_direction_vector_aca_fhp for i in range(3)]

# Calculate the length of "B)"
line_b = slicer.util.getNode('B)')
start_point_b = [0, 0, 0]
end_point_b = [0, 0, 0]
line_b.GetNthControlPointPosition(0, start_point_b)
line_b.GetNthControlPointPosition(1, end_point_b)
length_b = sum([(end_point_b[i] - start_point_b[i]) ** 2 for i in range(3)]) ** 0.5

# Calculate the new end point for "Mala 2B aca FHP"
new_end_point = [point[i] + direction_vector_aca_fhp[i] * (2 * length_b) for i in range(3)]

# Create the new line "Mala 2B aca FHP"
new_line = slicer.vtkMRMLMarkupsLineNode()
new_line.SetName("Mala 2B aca FHP")
new_line.AddControlPoint(point)
new_line.AddControlPoint(new_end_point)
slicer.mrmlScene.AddNode(new_line)

print("New line 'Mala 2B aca FHP' created successfully.")


import slicer
import numpy as np

# Function to find the intersection point of two lines
def find_intersection(line1, line2):
    start1 = np.array(line1.GetNthControlPointPosition(0))
    end1 = np.array(line1.GetNthControlPointPosition(1))
    start2 = np.array(line2.GetNthControlPointPosition(0))
    end2 = np.array(line2.GetNthControlPointPosition(1))
    
    # Calculate direction vectors
    dir1 = end1 - start1
    dir2 = end2 - start2
    
    # Calculate the intersection point (assuming lines are coplanar and intersect)
    A = np.array([dir1, -dir2]).T
    b = start2 - start1
    t = np.linalg.lstsq(A, b, rcond=None)[0][0]
    intersection = start1 + t * dir1
    
    return intersection.tolist()

# Get the lines "A FHP" and "for b - ac"
line_a_fhp = slicer.util.getNode('A FHP')
line_for_b_ac = slicer.util.getNode('for b - ac')

# Find the intersection point of "A FHP" and "for b - ac"
intersection_point = find_intersection(line_a_fhp, line_for_b_ac)

# Get the "lmrks_Stephan" node
lmrks_stephan = slicer.util.getNode('lmrks_Stephan')

# Add the intersection point to the end of the list and name it "A FHP - for b - ac intersection"
lmrks_stephan.AddControlPoint(intersection_point)
lmrks_stephan.SetNthControlPointLabel(lmrks_stephan.GetNumberOfControlPoints() - 1, "A FHP - for b - ac intersection")

print("Intersection point added to 'lmrks_Stephan' as 'A FHP - for b - ac intersection'.")


import slicer

# Get the intersection point from "lmrks_Stephan" in position 10
intersection_point = slicer.util.getNode('lmrks_Stephan').GetNthControlPointPosition(10)

# Get the line "A FHP"
line_a_fhp = slicer.util.getNode('A FHP')

# Calculate the direction vector of "A FHP"
start_point_a_fhp = [0, 0, 0]
end_point_a_fhp = [0, 0, 0]
line_a_fhp.GetNthControlPointPosition(0, start_point_a_fhp)
line_a_fhp.GetNthControlPointPosition(1, end_point_a_fhp)
direction_vector_a_fhp = [end_point_a_fhp[i] - start_point_a_fhp[i] for i in range(3)]

# Normalize the direction vector
length_direction_vector_a_fhp = sum([direction_vector_a_fhp[i] ** 2 for i in range(3)]) ** 0.5
direction_vector_a_fhp = [direction_vector_a_fhp[i] / length_direction_vector_a_fhp for i in range(3)]

# Calculate the length of "B)"
line_b = slicer.util.getNode('B)')
start_point_b = [0, 0, 0]
end_point_b = [0, 0, 0]
line_b.GetNthControlPointPosition(0, start_point_b)
line_b.GetNthControlPointPosition(1, end_point_b)
length_b = sum([(end_point_b[i] - start_point_b[i]) ** 2 for i in range(3)]) ** 0.5

# Calculate the new end point for "Mala 2B A FHP"
new_end_point = [intersection_point[i] + direction_vector_a_fhp[i] * (2 * length_b) for i in range(3)]

# Create the new line "Mala 2B A FHP"
new_line = slicer.vtkMRMLMarkupsLineNode()
new_line.SetName("Mala 2B A FHP")
new_line.AddControlPoint(intersection_point)
new_line.AddControlPoint(new_end_point)
slicer.mrmlScene.AddNode(new_line)

print("New line 'Mala 2B A FHP' created successfully.")


import slicer
import numpy as np

# Get the nodes for the existing points and lines
hardTissueNode = slicer.util.getNode('lmrks_Stephan')  # Main node containing multiple control points
acaFHPNode = slicer.util.getNode('aca FHP')
Mala2BAFHPNode = slicer.util.getNode('Mala 2B A FHP')


# Get the positions of the control points
firstControlPoint =   np.array(acaFHPNode.GetNthControlPointPosition(1))# First control point ( 'anterior end of ant aca FHP')
apexPoint = np.array(hardTissueNode.GetNthControlPointPosition(5))  #acanthion
thirdControlPoint = np.array(Mala2BAFHPNode.GetNthControlPointPosition(1))   # Third control point

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'D) nasal spine angle - opt 3')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Apex point
angleNode.AddControlPoint(thirdControlPoint)  # Third control point as the ant end of the line Mala 2B A FHP
```

The two FHP-parallel lines bisecing the acanthion (aca FHP - purple) and orthodontic point A (A FHP - pink)

![image](https://github.com/user-attachments/assets/af936f9d-1a6e-497f-a89c-8e284418fe03)


Finding the intersection point where the "for b - ac" line meets the A FHP line

![image](https://github.com/user-attachments/assets/194750c5-55c6-4f57-852f-7231ba275496)


Creating the two lines with the length of 2 B) 

![image](https://github.com/user-attachments/assets/72f39307-b0ec-4e14-b632-60f368866f2b)


Defining the angle arm as the diagonal of the "rectangle"


![image](https://github.com/user-attachments/assets/a33c84d7-4e73-4b32-9958-0804bf1c5de9)

</details>

### Measurement E)
This measurement is independent from your choice of angle measurements - the distance between nasion and Point X

<details>
<summary>Code to create e)</summary>
```python
import slicer
import numpy as np

#Get the nodes for the existing points
hardTissueNode = slicer.util.getNode('lmrks_Stephan')
pointXNode = slicer.util.getNode('Point X')

#Get the positions of the control points
startPoint = np.array(hardTissueNode.GetNthControlPointPosition(0))
endPoint = np.array(pointXNode.GetNthControlPointPosition(0))

#Create the line node
lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'E)')
lineNode.AddControlPoint(startPoint)  # Start point
lineNode.AddControlPoint(endPoint)    # End point

#Set the color to burgundy
lineNode.GetDisplayNode().SetSelectedColor(0.5, 0.0, 0.13)  # RGB values for burgundy

```
</details>

### Prediction point - pronasale
Stephan et al. 2003 divides the prediction equations by biological sex to predict distances along axes x and y; then find the intersection as the pronasale (soft nose tip). In this section, we apply their original equations for each biological sex to the acquired measurements to predict dimensions (lengths) along the x and y axes predicting the pronasale (soft tissue nose tip) positions. 

<details>
<summary>If female & used option 1 for nasal spine angle</summary>
F(x) = -0.41 * nasal_bone_angle + 0.37 * line_B_value + 49.87

F(y) = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

```python
import slicer
import numpy as np

# Function to calculate the length of a line node
def calculate_line_length(line_node):
    point1 = np.array(line_node.GetNthControlPointPosition(0))
    point2 = np.array(line_node.GetNthControlPointPosition(1))
    length = np.linalg.norm(point1 - point2)
    return length

# Function to get the angle value from an angle node
def get_angle_value(node):
    return node.GetAngleDegrees()

# Function to create a new point in the opposite direction of the x-axis
def create_new_point_opposite_x_axis(start_node, distance):
    start_point = np.array(start_node.GetNthControlPointPosition(0))
    new_point = start_point - np.array([distance, 0, 0])
    return new_point

# Accessing the nodes
nasal_bone_angle_node = slicer.util.getNode('A) nasal bone angle')
line_node_B = slicer.util.getNode('B)')
line_node_C = slicer.util.getNode('C)')
start_node = slicer.util.getNode('lmrks_Stephan')
x_axis_node = slicer.util.getNode('x axis')
y_axis_node = slicer.util.getNode('y axis')
nasal_spine_angle_node = slicer.util.getNode('D) nasal spine angle - opt 1')
line_node_E = slicer.util.getNode('E)')

# Retrieve the values
nasal_bone_angle = get_angle_value(nasal_bone_angle_node)
line_B_value = calculate_line_length(line_node_B)
line_C_value = calculate_line_length(line_node_C)
nasal_spine_angle = get_angle_value(nasal_spine_angle_node)
line_E_value = calculate_line_length(line_node_E)

# Calculate Fx using the given equation
Fx = -0.41 * nasal_bone_angle + 0.37 * line_B_value + 49.87

# Calculate the new point coordinates in the opposite direction
new_point_coordinates = create_new_point_opposite_x_axis(start_node, Fx)

# Calculate y using the given equation
y = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

# Define the starting point
start_point = np.array(start_node.GetNthControlPointPosition(0))

# Get the direction vectors from the x axis and y axis nodes
x_axis_direction = np.array(x_axis_node.GetNthControlPointPosition(1)) - np.array(x_axis_node.GetNthControlPointPosition(0))
x_axis_direction = x_axis_direction / np.linalg.norm(x_axis_direction)

y_axis_direction = np.array(y_axis_node.GetNthControlPointPosition(1)) - np.array(y_axis_node.GetNthControlPointPosition(0))
y_axis_direction = y_axis_direction / np.linalg.norm(y_axis_direction)

# Create "x pred - 1" line parallel to the x axis
x_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x pred - 1')
x_pred_node.AddControlPoint(start_point.tolist())
x_pred_node.AddControlPoint((start_point + Fx * x_axis_direction).tolist())
x_pred_node.GetDisplayNode().SetSelectedColor(0.5, 0, 0.5)  # Set color to purple

# Create "y pred - 1" line parallel to the opposite direction of the y axis
y_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y pred - 1')
y_pred_node.AddControlPoint(start_point.tolist())
y_pred_node.AddControlPoint((start_point - y * y_axis_direction).tolist())
y_pred_node.GetDisplayNode().SetSelectedColor(0.5, 0, 0.5)  # Set color to purple

# Update the scene
slicer.app.processEvents()
```

![image](https://github.com/user-attachments/assets/6383b0c1-d3a5-4bb6-90e1-717c39f0092a)

</details>


<details>
<summary>If female & used option 2 for nasal spine angle</summary>
F(x) = -0.41 * nasal_bone_angle + 0.37 * line_B_value + 49.87

F(y) = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

```python
import slicer
import numpy as np

# Function to calculate the length of a line node
def calculate_line_length(line_node):
    point1 = np.array(line_node.GetNthControlPointPosition(0))
    point2 = np.array(line_node.GetNthControlPointPosition(1))
    length = np.linalg.norm(point1 - point2)
    return length

# Function to get the angle value from an angle node
def get_angle_value(node):
    return node.GetAngleDegrees()

# Function to create a new point in the opposite direction of the x-axis
def create_new_point_opposite_x_axis(start_node, distance):
    start_point = np.array(start_node.GetNthControlPointPosition(0))
    new_point = start_point - np.array([distance, 0, 0])
    return new_point

# Accessing the nodes
nasal_bone_angle_node = slicer.util.getNode('A) nasal bone angle')
line_node_B = slicer.util.getNode('B)')
line_node_C = slicer.util.getNode('C)')
start_node = slicer.util.getNode('lmrks_Stephan')
x_axis_node = slicer.util.getNode('x axis')
y_axis_node = slicer.util.getNode('y axis')
nasal_spine_angle_node = slicer.util.getNode('D) nasal spine angle - opt 2')
line_node_E = slicer.util.getNode('E)')

# Retrieve the values
nasal_bone_angle = get_angle_value(nasal_bone_angle_node)
line_B_value = calculate_line_length(line_node_B)
line_C_value = calculate_line_length(line_node_C)
nasal_spine_angle = get_angle_value(nasal_spine_angle_node)
line_E_value = calculate_line_length(line_node_E)

# Calculate Fx using the given equation
Fx = -0.41 * nasal_bone_angle + 0.37 * line_B_value + 49.87

# Calculate the new point coordinates in the opposite direction
new_point_coordinates = create_new_point_opposite_x_axis(start_node, Fx)

# Calculate y using the given equation
y = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

# Define the starting point
start_point = np.array(start_node.GetNthControlPointPosition(0))

# Get the direction vectors from the x axis and y axis nodes
x_axis_direction = np.array(x_axis_node.GetNthControlPointPosition(1)) - np.array(x_axis_node.GetNthControlPointPosition(0))
x_axis_direction = x_axis_direction / np.linalg.norm(x_axis_direction)

y_axis_direction = np.array(y_axis_node.GetNthControlPointPosition(1)) - np.array(y_axis_node.GetNthControlPointPosition(0))
y_axis_direction = y_axis_direction / np.linalg.norm(y_axis_direction)

# Create "x pred - 2" line parallel to the x axis
x_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x pred - 2')
x_pred_node.AddControlPoint(start_point.tolist())
x_pred_node.AddControlPoint((start_point + Fx * x_axis_direction).tolist())
x_pred_node.GetDisplayNode().SetSelectedColor(0.5, 0, 0.5)  # Set color to purple

# Create "y pred - 2" line parallel to the opposite direction of the y axis
y_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y pred - 2')
y_pred_node.AddControlPoint(start_point.tolist())
y_pred_node.AddControlPoint((start_point - y * y_axis_direction).tolist())
y_pred_node.GetDisplayNode().SetSelectedColor(0.5, 0, 0.5)  # Set color to purple

# Update the scene
slicer.app.processEvents()
```
</details>


![image](https://github.com/user-attachments/assets/d5e039c1-688c-4f43-aef3-4b15681f8662)




<details>
<summary>If female & used option 3 for nasal spine angle</summary>
F(x) = -0.41 * nasal_bone_angle + 0.37 * line_B_value + 49.87
F(y) = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

```python
import slicer
import numpy as np

# Function to calculate the length of a line node
def calculate_line_length(line_node):
    point1 = np.array(line_node.GetNthControlPointPosition(0))
    point2 = np.array(line_node.GetNthControlPointPosition(1))
    length = np.linalg.norm(point1 - point2)
    return length

# Function to get the angle value from an angle node
def get_angle_value(node):
    return node.GetAngleDegrees()

# Function to create a new point in the opposite direction of the x-axis
def create_new_point_opposite_x_axis(start_node, distance):
    start_point = np.array(start_node.GetNthControlPointPosition(0))
    new_point = start_point - np.array([distance, 0, 0])
    return new_point

# Accessing the nodes
nasal_bone_angle_node = slicer.util.getNode('A) nasal bone angle')
line_node_B = slicer.util.getNode('B)')
line_node_C = slicer.util.getNode('C)')
start_node = slicer.util.getNode('lmrks_Stephan')
x_axis_node = slicer.util.getNode('x axis')
y_axis_node = slicer.util.getNode('y axis')
nasal_spine_angle_node = slicer.util.getNode('D) nasal spine angle - opt 3')
line_node_E = slicer.util.getNode('E)')

# Retrieve the values
nasal_bone_angle = get_angle_value(nasal_bone_angle_node)
line_B_value = calculate_line_length(line_node_B)
line_C_value = calculate_line_length(line_node_C)
nasal_spine_angle = get_angle_value(nasal_spine_angle_node)
line_E_value = calculate_line_length(line_node_E)

# Calculate Fx using the given equation
Fx = -0.41 * nasal_bone_angle + 0.37 * line_B_value + 49.87

# Calculate the new point coordinates in the opposite direction
new_point_coordinates = create_new_point_opposite_x_axis(start_node, Fx)

# Calculate y using the given equation
y = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

# Define the starting point
start_point = np.array(start_node.GetNthControlPointPosition(0))

# Get the direction vectors from the x axis and y axis nodes
x_axis_direction = np.array(x_axis_node.GetNthControlPointPosition(1)) - np.array(x_axis_node.GetNthControlPointPosition(0))
x_axis_direction = x_axis_direction / np.linalg.norm(x_axis_direction)

y_axis_direction = np.array(y_axis_node.GetNthControlPointPosition(1)) - np.array(y_axis_node.GetNthControlPointPosition(0))
y_axis_direction = y_axis_direction / np.linalg.norm(y_axis_direction)

# Create "x pred - 3" line parallel to the x axis
x_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x pred - 3')
x_pred_node.AddControlPoint(start_point.tolist())
x_pred_node.AddControlPoint((start_point + Fx * x_axis_direction).tolist())
x_pred_node.GetDisplayNode().SetSelectedColor(0.5, 0, 0.5)  # Set color to purple

# Create "y pred - 3" line parallel to the opposite direction of the y axis
y_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y pred - 3')
y_pred_node.AddControlPoint(start_point.tolist())
y_pred_node.AddControlPoint((start_point - y * y_axis_direction).tolist())
y_pred_node.GetDisplayNode().SetSelectedColor(0.5, 0, 0.5)  # Set color to purple

# Update the scene
slicer.app.processEvents()
```

![image](https://github.com/user-attachments/assets/31d55872-94fd-45c8-86a5-e28d187af423)

</details>



<details>
<summary>If male & used option 1 for D) nasal spine angle</summary>
M(x) = -0.32 * nasal_bone_angle + 0.85 * line_B_value - 0.42 * line_C_value + 49.58
M(y) = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

```python
import slicer
import numpy as np

# Function to calculate the length of a line node
def calculate_line_length(line_node):
    point1 = np.array(line_node.GetNthControlPointPosition(0))
    point2 = np.array(line_node.GetNthControlPointPosition(1))
    length = np.linalg.norm(point1 - point2)
    return length

# Function to get the angle value from an angle node
def get_angle_value(node):
    return node.GetAngleDegrees()

# Function to create a new point in the opposite direction of the x-axis
def create_new_point_opposite_x_axis(start_node, distance):
    start_point = np.array(start_node.GetNthControlPointPosition(0))
    new_point = start_point - np.array([distance, 0, 0])
    return new_point

# Accessing the nodes
nasal_bone_angle_node = slicer.util.getNode('A) nasal bone angle')
line_node_B = slicer.util.getNode('B)')
line_node_C = slicer.util.getNode('C)')
start_node = slicer.util.getNode('lmrks_Stephan')
x_axis_node = slicer.util.getNode('x axis')
y_axis_node = slicer.util.getNode('y axis')
nasal_spine_angle_node = slicer.util.getNode('D) nasal spine angle - opt 1')
line_node_E = slicer.util.getNode('E)')

# Retrieve the values
nasal_bone_angle = get_angle_value(nasal_bone_angle_node)
line_B_value = calculate_line_length(line_node_B)
line_C_value = calculate_line_length(line_node_C)
nasal_spine_angle = get_angle_value(nasal_spine_angle_node)
line_E_value = calculate_line_length(line_node_E)

# Calculate Mx using the given equation
Mx = -0.32 * nasal_bone_angle + 0.85 * line_B_value - 0.42 * line_C_value + 49.58

# Calculate the new point coordinates in the opposite direction
new_point_coordinates = create_new_point_opposite_x_axis(start_node, Mx)

# Calculate y using the given equation
y = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

# Define the starting point
start_point = np.array(start_node.GetNthControlPointPosition(0))

# Get the direction vectors from the x axis and y axis nodes
x_axis_direction = np.array(x_axis_node.GetNthControlPointPosition(1)) - np.array(x_axis_node.GetNthControlPointPosition(0))
x_axis_direction = x_axis_direction / np.linalg.norm(x_axis_direction)

y_axis_direction = np.array(y_axis_node.GetNthControlPointPosition(1)) - np.array(y_axis_node.GetNthControlPointPosition(0))
y_axis_direction = y_axis_direction / np.linalg.norm(y_axis_direction)

# Create "x pred - 1" line parallel to the x axis
x_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x pred - 1')
x_pred_node.AddControlPoint(start_point.tolist())
x_pred_node.AddControlPoint((start_point + Mx * x_axis_direction).tolist())

# Create "y pred - 1" line parallel to the opposite direction of the y axis
y_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y pred - 1')
y_pred_node.AddControlPoint(start_point.tolist())
y_pred_node.AddControlPoint((start_point - y * y_axis_direction).tolist())

# Update the scene
slicer.app.processEvents()
```

![image](https://github.com/user-attachments/assets/2188324f-5f0f-4f67-ba4c-d246cdbf0eba)

</details>


<details>
<summary>If male & used option 2 for D) nasal spine angle</summary>
M(x) = -0.32 * nasal_bone_angle + 0.85 * line_B_value - 0.42 * line_C_value + 49.58
M(y) = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

```python
import slicer
import numpy as np

# Function to calculate the length of a line node
def calculate_line_length(line_node):
    point1 = np.array(line_node.GetNthControlPointPosition(0))
    point2 = np.array(line_node.GetNthControlPointPosition(1))
    length = np.linalg.norm(point1 - point2)
    return length

# Function to get the angle value from an angle node
def get_angle_value(node):
    return node.GetAngleDegrees()

# Function to create a new point in the opposite direction of the x-axis
def create_new_point_opposite_x_axis(start_node, distance):
    start_point = np.array(start_node.GetNthControlPointPosition(0))
    new_point = start_point - np.array([distance, 0, 0])
    return new_point

# Accessing the nodes
nasal_bone_angle_node = slicer.util.getNode('A) nasal bone angle')
line_node_B = slicer.util.getNode('B)')
line_node_C = slicer.util.getNode('C)')
start_node = slicer.util.getNode('lmrks_Stephan')
x_axis_node = slicer.util.getNode('x axis')
y_axis_node = slicer.util.getNode('y axis')
nasal_spine_angle_node = slicer.util.getNode('D) nasal spine angle - opt 2')
line_node_E = slicer.util.getNode('E)')

# Retrieve the values
nasal_bone_angle = get_angle_value(nasal_bone_angle_node)
line_B_value = calculate_line_length(line_node_B)
line_C_value = calculate_line_length(line_node_C)
nasal_spine_angle = get_angle_value(nasal_spine_angle_node)
line_E_value = calculate_line_length(line_node_E)

# Calculate Mx using the given equation
Mx = -0.32 * nasal_bone_angle + 0.85 * line_B_value - 0.42 * line_C_value + 49.58

# Calculate the new point coordinates in the opposite direction
new_point_coordinates = create_new_point_opposite_x_axis(start_node, Mx)

# Calculate y using the given equation
y = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

# Define the starting point
start_point = np.array(start_node.GetNthControlPointPosition(0))

# Get the direction vectors from the x axis and y axis nodes
x_axis_direction = np.array(x_axis_node.GetNthControlPointPosition(1)) - np.array(x_axis_node.GetNthControlPointPosition(0))
x_axis_direction = x_axis_direction / np.linalg.norm(x_axis_direction)

y_axis_direction = np.array(y_axis_node.GetNthControlPointPosition(1)) - np.array(y_axis_node.GetNthControlPointPosition(0))
y_axis_direction = y_axis_direction / np.linalg.norm(y_axis_direction)

# Create "x pred - 2" line parallel to the x axis
x_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x pred - 2')
x_pred_node.AddControlPoint(start_point.tolist())
x_pred_node.AddControlPoint((start_point + Mx * x_axis_direction).tolist())

# Create "y pred - 2" line parallel to the opposite direction of the y axis
y_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y pred - 2')
y_pred_node.AddControlPoint(start_point.tolist())
y_pred_node.AddControlPoint((start_point - y * y_axis_direction).tolist())

# Update the scene
slicer.app.processEvents()
```

![image](https://github.com/user-attachments/assets/9440720f-2b83-4283-ba95-dba18aeea853)


</details>


<details>
<summary>If male & used option 3 for D) nasal spine angle</summary>
M(x) = -0.32 * nasal_bone_angle + 0.85 * line_B_value - 0.42 * line_C_value + 49.58
M(y) = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

```python
import slicer
import numpy as np

# Function to calculate the length of a line node
def calculate_line_length(line_node):
    point1 = np.array(line_node.GetNthControlPointPosition(0))
    point2 = np.array(line_node.GetNthControlPointPosition(1))
    length = np.linalg.norm(point1 - point2)
    return length

# Function to get the angle value from an angle node
def get_angle_value(node):
    return node.GetAngleDegrees()

# Function to create a new point in the opposite direction of the x-axis
def create_new_point_opposite_x_axis(start_node, distance):
    start_point = np.array(start_node.GetNthControlPointPosition(0))
    new_point = start_point - np.array([distance, 0, 0])
    return new_point

# Accessing the nodes
nasal_bone_angle_node = slicer.util.getNode('A) nasal bone angle')
line_node_B = slicer.util.getNode('B)')
line_node_C = slicer.util.getNode('C)')
start_node = slicer.util.getNode('lmrks_Stephan')
x_axis_node = slicer.util.getNode('x axis')
y_axis_node = slicer.util.getNode('y axis')
nasal_spine_angle_node = slicer.util.getNode('D) nasal spine angle - opt 3')
line_node_E = slicer.util.getNode('E)')

# Retrieve the values
nasal_bone_angle = get_angle_value(nasal_bone_angle_node)
line_B_value = calculate_line_length(line_node_B)
line_C_value = calculate_line_length(line_node_C)
nasal_spine_angle = get_angle_value(nasal_spine_angle_node)
line_E_value = calculate_line_length(line_node_E)

# Calculate Mx using the given equation
Mx = -0.32 * nasal_bone_angle + 0.85 * line_B_value - 0.42 * line_C_value + 49.58

# Calculate the new point coordinates in the opposite direction
new_point_coordinates = create_new_point_opposite_x_axis(start_node, Mx)

# Calculate y using the given equation
y = (-0.002 * nasal_spine_angle + 0.83) * line_E_value

# Define the starting point
start_point = np.array(start_node.GetNthControlPointPosition(0))

# Get the direction vectors from the x axis and y axis nodes
x_axis_direction = np.array(x_axis_node.GetNthControlPointPosition(1)) - np.array(x_axis_node.GetNthControlPointPosition(0))
x_axis_direction = x_axis_direction / np.linalg.norm(x_axis_direction)

y_axis_direction = np.array(y_axis_node.GetNthControlPointPosition(1)) - np.array(y_axis_node.GetNthControlPointPosition(0))
y_axis_direction = y_axis_direction / np.linalg.norm(y_axis_direction)

# Create "x pred - 3" line parallel to the x axis
x_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x pred - 3')
x_pred_node.AddControlPoint(start_point.tolist())
x_pred_node.AddControlPoint((start_point + Mx * x_axis_direction).tolist())

# Create "y pred - 3" line parallel to the opposite direction of the y axis
y_pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y pred - 3')
y_pred_node.AddControlPoint(start_point.tolist())
y_pred_node.AddControlPoint((start_point - y * y_axis_direction).tolist())

# Update the scene
slicer.app.processEvents()

```

![image](https://github.com/user-attachments/assets/74a69a75-63b1-4f62-9e06-5042af2c79c3)

</details>


### Error measurements

The following scripts create a line between the real soft tissue pronasale and the predicted one. 
For this to work, download the json file containing this landmark and allocate it before running the codes.  [soft tissue Stephan.mrk.json](https://github.com/user-attachments/files/20149383/soft.tissue.Stephan.mrk.json)


![image](https://github.com/user-attachments/assets/70bd5961-1d59-40e7-a95b-2a9b68236c1a)



These also are split based on the choice of angle measurement into options 1, 2 and 3 - please make sure you use the correct one. 
The colour coding in the resulting lines is as follows: 
 - x para - 1/2/3 and y para - 1/2/3 - green: lines parallel to the axes with the predicted x and y measurements creating the "prediction rectangle"
 - pronasale pred - 1/2/3 - pink: the intersection of the parallels which is the predicted pronasale point
 - pronasale to soft tissue - 1/2/3 - orange: line connecting the manually allocated pronasale and the predicted pronasale, providing the error of prediction in mm

<details>
<summary>Error measurement if option 1 was used for D) nasal spine angle</summary>

```python
import numpy as np
import slicer

# Get the control point from "y pred - 1"
y_pred = slicer.util.getNode('y pred - 1')
control_point = [0, 0, 0]
y_pred.GetNthControlPointPosition(1, control_point)

# Get the direction vector of "x pred - 1"
x_pred = slicer.util.getNode('x pred - 1')
start_point = [0, 0, 0]
end_point = [0, 0, 0]
x_pred.GetNthControlPointPosition(0, start_point)
x_pred.GetNthControlPointPosition(1, end_point)
direction_vector = [end_point[i] - start_point[i] for i in range(3)]

# Normalize the direction vector and reverse it
direction_vector = np.array(direction_vector)
direction_vector = direction_vector / np.linalg.norm(direction_vector)
reversed_direction_vector = -direction_vector

# Calculate the end points of the new line "x para - 1"
length = 150.0  # length in mm
half_length_vector = reversed_direction_vector * (length / 2)
start_point_x_para = control_point + half_length_vector
end_point_x_para = control_point - half_length_vector

# Get the plane "INB"
plane_INB = slicer.util.getNode('INB')
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 0]
plane_INB.GetOrigin(plane_origin)
plane_INB.GetNormal(plane_normal)

# Project points onto the plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point = np.array(point)
    plane_origin = np.array(plane_origin)
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    vector_from_origin = point - plane_origin
    distance_to_plane = np.dot(vector_from_origin, plane_normal)
    projected_point = point - distance_to_plane * plane_normal
    return projected_point

start_point_x_para = project_point_onto_plane(start_point_x_para, plane_origin, plane_normal)
end_point_x_para = project_point_onto_plane(end_point_x_para, plane_origin, plane_normal)

# Create the new line "x para - 1"
x_para = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x para - 1')
x_para.AddControlPoint(start_point_x_para)
x_para.AddControlPoint(end_point_x_para)

# Set the color to forest green
x_para.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)  # RGB values for forest green



import numpy as np
import slicer

# Get the control point from "x pred - 1"
x_pred = slicer.util.getNode('x pred - 1')
control_point = [0, 0, 0]
x_pred.GetNthControlPointPosition(1, control_point)

# Get the direction vector of "y pred - 1"
y_pred = slicer.util.getNode('y pred - 1')
start_point = [0, 0, 0]
end_point = [0, 0, 0]
y_pred.GetNthControlPointPosition(0, start_point)
y_pred.GetNthControlPointPosition(1, end_point)
direction_vector = [end_point[i] - start_point[i] for i in range(3)]

# Normalize the direction vector and reverse it
direction_vector = np.array(direction_vector)
direction_vector = direction_vector / np.linalg.norm(direction_vector)
reversed_direction_vector = -direction_vector

# Calculate the end points of the new line "y para - 1"
length = 150.0  # length in mm
half_length_vector = reversed_direction_vector * (length / 2)
start_point_y_para = control_point + half_length_vector
end_point_y_para = control_point - half_length_vector

# Get the plane "INB"
plane_INB = slicer.util.getNode('INB')
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 0]
plane_INB.GetOrigin(plane_origin)
plane_INB.GetNormal(plane_normal)

# Project points onto the plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point = np.array(point)
    plane_origin = np.array(plane_origin)
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    vector_from_origin = point - plane_origin
    distance_to_plane = np.dot(vector_from_origin, plane_normal)
    projected_point = point - distance_to_plane * plane_normal
    return projected_point

start_point_y_para = project_point_onto_plane(start_point_y_para, plane_origin, plane_normal)
end_point_y_para = project_point_onto_plane(end_point_y_para, plane_origin, plane_normal)

# Create the new line "y para - 1"
y_para = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y para - 1')
y_para.AddControlPoint(start_point_y_para)
y_para.AddControlPoint(end_point_y_para)

# Set the color to forest green
y_para.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)  # RGB values for forest green


import numpy as np
import slicer

# Function to find the intersection of two lines
def line_intersection(p1, p2, p3, p4):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    p4 = np.array(p4)
    
    # Line vectors
    v1 = p2 - p1
    v2 = p4 - p3
    
    # Cross product to find the intersection
    cross_v1_v2 = np.cross(v1, v2)
    cross_p3_p1_v2 = np.cross(p3 - p1, v2)
    
    if np.linalg.norm(cross_v1_v2) == 0:
        raise ValueError("Lines do not intersect or are collinear")
    
    t = np.dot(cross_p3_p1_v2, cross_v1_v2) / np.linalg.norm(cross_v1_v2)**2
    intersection = p1 + t * v1
    
    return intersection

# Get the control points of "x para - 1"
x_para = slicer.util.getNode('x para - 1')
x_start = [0, 0, 0]
x_end = [0, 0, 0]
x_para.GetNthControlPointPosition(0, x_start)
x_para.GetNthControlPointPosition(1, x_end)

# Get the control points of "y para - 1"
y_para = slicer.util.getNode('y para - 1')
y_start = [0, 0, 0]
y_end = [0, 0, 0]
y_para.GetNthControlPointPosition(0, y_start)
y_para.GetNthControlPointPosition(1, y_end)

# Find the intersection point
intersection_point = line_intersection(x_start, x_end, y_start, y_end)

# Create a new fiducial node for the intersection point
pronasale_pred = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pronasale pred - 1')
pronasale_pred.AddControlPoint(intersection_point)

# Set the color to bright pink
pronasale_pred.GetDisplayNode().SetSelectedColor(1.0, 0.08, 0.58)  # RGB values for bright pink


import slicer

# Get the control point from "pronasale pred - 1"
pronasale_pred = slicer.util.getNode('pronasale pred - 1')
pronasale_point = [0, 0, 0]
pronasale_pred.GetNthControlPointPosition(0, pronasale_point)

# Get the control point from "soft tissue Stephan"
soft_tissue = slicer.util.getNode('soft_tissue_Stephan')
soft_tissue_point = [0, 0, 0]
soft_tissue.GetNthControlPointPosition(0, soft_tissue_point)

# Create the new line
line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pronasale to soft tissue - 1')
line_node.AddControlPoint(pronasale_point)
line_node.AddControlPoint(soft_tissue_point)

# Set the color to orange
line_node.GetDisplayNode().SetSelectedColor(1.0, 0.65, 0.0)  # RGB values for orange

```

![image](https://github.com/user-attachments/assets/7dbb1dbf-b317-476f-847b-0b7d3281dcdf)

</details>



<details>
<summary>Error measurement if option 2 was used for D) nasal spine angle</summary>

```python

import numpy as np
import slicer

# Get the control point from "y pred - 2"
y_pred = slicer.util.getNode('y pred - 2')
control_point = [0, 0, 0]
y_pred.GetNthControlPointPosition(1, control_point)

# Get the direction vector of "x pred - 2"
x_pred = slicer.util.getNode('x pred - 2')
start_point = [0, 0, 0]
end_point = [0, 0, 0]
x_pred.GetNthControlPointPosition(0, start_point)
x_pred.GetNthControlPointPosition(1, end_point)
direction_vector = [end_point[i] - start_point[i] for i in range(3)]

# Normalize the direction vector and reverse it
direction_vector = np.array(direction_vector)
direction_vector = direction_vector / np.linalg.norm(direction_vector)
reversed_direction_vector = -direction_vector

# Calculate the end points of the new line "x para - 2"
length = 150.0  # length in mm
half_length_vector = reversed_direction_vector * (length / 2)
start_point_x_para = control_point + half_length_vector
end_point_x_para = control_point - half_length_vector

# Get the plane "INB"
plane_INB = slicer.util.getNode('INB')
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 0]
plane_INB.GetOrigin(plane_origin)
plane_INB.GetNormal(plane_normal)

# Project points onto the plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point = np.array(point)
    plane_origin = np.array(plane_origin)
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    vector_from_origin = point - plane_origin
    distance_to_plane = np.dot(vector_from_origin, plane_normal)
    projected_point = point - distance_to_plane * plane_normal
    return projected_point

start_point_x_para = project_point_onto_plane(start_point_x_para, plane_origin, plane_normal)
end_point_x_para = project_point_onto_plane(end_point_x_para, plane_origin, plane_normal)

# Create the new line "x para - 2"
x_para = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x para - 2')
x_para.AddControlPoint(start_point_x_para)
x_para.AddControlPoint(end_point_x_para)

# Set the color to forest green
x_para.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)  # RGB values for forest green



import numpy as np
import slicer

# Get the control point from "x pred - 2"
x_pred = slicer.util.getNode('x pred - 2')
control_point = [0, 0, 0]
x_pred.GetNthControlPointPosition(1, control_point)

# Get the direction vector of "y pred - 2"
y_pred = slicer.util.getNode('y pred - 2')
start_point = [0, 0, 0]
end_point = [0, 0, 0]
y_pred.GetNthControlPointPosition(0, start_point)
y_pred.GetNthControlPointPosition(1, end_point)
direction_vector = [end_point[i] - start_point[i] for i in range(3)]

# Normalize the direction vector and reverse it
direction_vector = np.array(direction_vector)
direction_vector = direction_vector / np.linalg.norm(direction_vector)
reversed_direction_vector = -direction_vector

# Calculate the end points of the new line "y para - 2"
length = 150.0  # length in mm
half_length_vector = reversed_direction_vector * (length / 2)
start_point_y_para = control_point + half_length_vector
end_point_y_para = control_point - half_length_vector

# Get the plane "INB"
plane_INB = slicer.util.getNode('INB')
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 0]
plane_INB.GetOrigin(plane_origin)
plane_INB.GetNormal(plane_normal)

# Project points onto the plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point = np.array(point)
    plane_origin = np.array(plane_origin)
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    vector_from_origin = point - plane_origin
    distance_to_plane = np.dot(vector_from_origin, plane_normal)
    projected_point = point - distance_to_plane * plane_normal
    return projected_point

start_point_y_para = project_point_onto_plane(start_point_y_para, plane_origin, plane_normal)
end_point_y_para = project_point_onto_plane(end_point_y_para, plane_origin, plane_normal)

# Create the new line "y para - 2"
y_para = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y para - 2')
y_para.AddControlPoint(start_point_y_para)
y_para.AddControlPoint(end_point_y_para)

# Set the color to forest green
y_para.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)  # RGB values for forest green


import numpy as np
import slicer

# Function to find the intersection of two lines
def line_intersection(p1, p2, p3, p4):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    p4 = np.array(p4)
    
    # Line vectors
    v1 = p2 - p1
    v2 = p4 - p3
    
    # Cross product to find the intersection
    cross_v1_v2 = np.cross(v1, v2)
    cross_p3_p1_v2 = np.cross(p3 - p1, v2)
    
    if np.linalg.norm(cross_v1_v2) == 0:
        raise ValueError("Lines do not intersect or are collinear")
    
    t = np.dot(cross_p3_p1_v2, cross_v1_v2) / np.linalg.norm(cross_v1_v2)**2
    intersection = p1 + t * v1
    
    return intersection

# Get the control points of "x para - 2"
x_para = slicer.util.getNode('x para - 2')
x_start = [0, 0, 0]
x_end = [0, 0, 0]
x_para.GetNthControlPointPosition(0, x_start)
x_para.GetNthControlPointPosition(1, x_end)

# Get the control points of "y para - 2"
y_para = slicer.util.getNode('y para - 2')
y_start = [0, 0, 0]
y_end = [0, 0, 0]
y_para.GetNthControlPointPosition(0, y_start)
y_para.GetNthControlPointPosition(1, y_end)

# Find the intersection point
intersection_point = line_intersection(x_start, x_end, y_start, y_end)

# Create a new fiducial node for the intersection point
pronasale_pred = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pronasale pred - 2')
pronasale_pred.AddControlPoint(intersection_point)

# Set the color to bright pink
pronasale_pred.GetDisplayNode().SetSelectedColor(1.0, 0.08, 0.58)  # RGB values for bright pink


import slicer

# Get the control point from "pronasale pred - 2"
pronasale_pred = slicer.util.getNode('pronasale pred - 2')
pronasale_point = [0, 0, 0]
pronasale_pred.GetNthControlPointPosition(0, pronasale_point)

# Get the control point from "soft tissue Stephan"
soft_tissue = slicer.util.getNode('soft_tissue_Stephan')
soft_tissue_point = [0, 0, 0]
soft_tissue.GetNthControlPointPosition(0, soft_tissue_point)

# Create the new line
line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pronasale to soft tissue - 2')
line_node.AddControlPoint(pronasale_point)
line_node.AddControlPoint(soft_tissue_point)

# Set the color to orange
line_node.GetDisplayNode().SetSelectedColor(1.0, 0.65, 0.0)  # RGB values for orange

```
![image](https://github.com/user-attachments/assets/db4493b9-145b-47a9-85dd-6f39250e1871)

</details>




<details>
<summary>Error measurement if option 3 was used for D) nasal spine angle</summary>

```python

import numpy as np
import slicer

# Get the control point from "y pred - 3"
y_pred = slicer.util.getNode('y pred - 3')
control_point = [0, 0, 0]
y_pred.GetNthControlPointPosition(1, control_point)

# Get the direction vector of "x pred - 3"
x_pred = slicer.util.getNode('x pred - 3')
start_point = [0, 0, 0]
end_point = [0, 0, 0]
x_pred.GetNthControlPointPosition(0, start_point)
x_pred.GetNthControlPointPosition(1, end_point)
direction_vector = [end_point[i] - start_point[i] for i in range(3)]

# Normalize the direction vector and reverse it
direction_vector = np.array(direction_vector)
direction_vector = direction_vector / np.linalg.norm(direction_vector)
reversed_direction_vector = -direction_vector

# Calculate the end points of the new line "x para - 3"
length = 150.0  # length in mm
half_length_vector = reversed_direction_vector * (length / 2)
start_point_x_para = control_point + half_length_vector
end_point_x_para = control_point - half_length_vector

# Get the plane "INB"
plane_INB = slicer.util.getNode('INB')
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 0]
plane_INB.GetOrigin(plane_origin)
plane_INB.GetNormal(plane_normal)

# Project points onto the plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point = np.array(point)
    plane_origin = np.array(plane_origin)
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    vector_from_origin = point - plane_origin
    distance_to_plane = np.dot(vector_from_origin, plane_normal)
    projected_point = point - distance_to_plane * plane_normal
    return projected_point

start_point_x_para = project_point_onto_plane(start_point_x_para, plane_origin, plane_normal)
end_point_x_para = project_point_onto_plane(end_point_x_para, plane_origin, plane_normal)

# Create the new line "x para - 3"
x_para = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'x para - 3')
x_para.AddControlPoint(start_point_x_para)
x_para.AddControlPoint(end_point_x_para)

# Set the color to forest green
x_para.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)  # RGB values for forest green



import numpy as np
import slicer

# Get the control point from "x pred - 3"
x_pred = slicer.util.getNode('x pred - 3')
control_point = [0, 0, 0]
x_pred.GetNthControlPointPosition(1, control_point)

# Get the direction vector of "y pred - 3"
y_pred = slicer.util.getNode('y pred - 3')
start_point = [0, 0, 0]
end_point = [0, 0, 0]
y_pred.GetNthControlPointPosition(0, start_point)
y_pred.GetNthControlPointPosition(1, end_point)
direction_vector = [end_point[i] - start_point[i] for i in range(3)]

# Normalize the direction vector and reverse it
direction_vector = np.array(direction_vector)
direction_vector = direction_vector / np.linalg.norm(direction_vector)
reversed_direction_vector = -direction_vector

# Calculate the end points of the new line "y para - 3"
length = 150.0  # length in mm
half_length_vector = reversed_direction_vector * (length / 2)
start_point_y_para = control_point + half_length_vector
end_point_y_para = control_point - half_length_vector

# Get the plane "INB"
plane_INB = slicer.util.getNode('INB')
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 0]
plane_INB.GetOrigin(plane_origin)
plane_INB.GetNormal(plane_normal)

# Project points onto the plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point = np.array(point)
    plane_origin = np.array(plane_origin)
    plane_normal = np.array(plane_normal)
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    vector_from_origin = point - plane_origin
    distance_to_plane = np.dot(vector_from_origin, plane_normal)
    projected_point = point - distance_to_plane * plane_normal
    return projected_point

start_point_y_para = project_point_onto_plane(start_point_y_para, plane_origin, plane_normal)
end_point_y_para = project_point_onto_plane(end_point_y_para, plane_origin, plane_normal)

# Create the new line "y para - 2"
y_para = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'y para - 3')
y_para.AddControlPoint(start_point_y_para)
y_para.AddControlPoint(end_point_y_para)

# Set the color to forest green
y_para.GetDisplayNode().SetSelectedColor(0.13, 0.55, 0.13)  # RGB values for forest green


import numpy as np
import slicer

# Function to find the intersection of two lines
def line_intersection(p1, p2, p3, p4):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    p4 = np.array(p4)
    
    # Line vectors
    v1 = p2 - p1
    v2 = p4 - p3
    
    # Cross product to find the intersection
    cross_v1_v2 = np.cross(v1, v2)
    cross_p3_p1_v2 = np.cross(p3 - p1, v2)
    
    if np.linalg.norm(cross_v1_v2) == 0:
        raise ValueError("Lines do not intersect or are collinear")
    
    t = np.dot(cross_p3_p1_v2, cross_v1_v2) / np.linalg.norm(cross_v1_v2)**2
    intersection = p1 + t * v1
    
    return intersection

# Get the control points of "x para - 3"
x_para = slicer.util.getNode('x para - 3')
x_start = [0, 0, 0]
x_end = [0, 0, 0]
x_para.GetNthControlPointPosition(0, x_start)
x_para.GetNthControlPointPosition(1, x_end)

# Get the control points of "y para - 3"
y_para = slicer.util.getNode('y para - 3')
y_start = [0, 0, 0]
y_end = [0, 0, 0]
y_para.GetNthControlPointPosition(0, y_start)
y_para.GetNthControlPointPosition(1, y_end)

# Find the intersection point
intersection_point = line_intersection(x_start, x_end, y_start, y_end)

# Create a new fiducial node for the intersection point
pronasale_pred = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pronasale pred - 3')
pronasale_pred.AddControlPoint(intersection_point)

# Set the color to bright pink
pronasale_pred.GetDisplayNode().SetSelectedColor(1.0, 0.08, 0.58)  # RGB values for bright pink


import slicer

# Get the control point from "pronasale pred - 3"
pronasale_pred = slicer.util.getNode('pronasale pred - 3')
pronasale_point = [0, 0, 0]
pronasale_pred.GetNthControlPointPosition(0, pronasale_point)

# Get the control point from "soft tissue Stephan"
soft_tissue = slicer.util.getNode('soft_tissue_Stephan')
soft_tissue_point = [0, 0, 0]
soft_tissue.GetNthControlPointPosition(0, soft_tissue_point)

# Create the new line
line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pronasale to soft tissue - 3')
line_node.AddControlPoint(pronasale_point)
line_node.AddControlPoint(soft_tissue_point)

# Set the color to orange
line_node.GetDisplayNode().SetSelectedColor(1.0, 0.65, 0.0)  # RGB values for orange

````
![image](https://github.com/user-attachments/assets/7e51007b-af5a-446a-bf08-7900a116f9db)

</details>

### Output
To copy all measurements to the clipboard, follow this [guide](https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/basics/Start%20here%20/004_Copy%20measurements%20to%20clipboard.md)

In the example, we will show the output of the scenario where the biological sex is known and all angle D) definitions are carried out to test which one is most precise in prediction. 
The codes do not include the biological sex in the output, so make sure you note it in your data collection table. 
We copied the linear measurements first, then the angles: 

| Patient ID              | Axis/Detail                     | Value                     | Notes/Comments |
|------------------------------------------|----------------------------------|---------------------------|----------------|
| (unknown)                                | x axis                          | 199.99999999999997        |  NOT a measurement              |
| (unknown)                                | y axis                          | 199.99999999999997        |   NOT a measurement              |
| (unknown)                                | AA FHP                          | 199.99491973323728        |  NOT a measurement               |
| (unknown)                                | n-point A)                      | 200.00000000000003        |                |
| (unknown)                                | LL y axis                       | 199.99999999999997        |   NOT a measurement              |
| (unknown)                                | RL y axis                       | 200.00000000000003        |   NOT a measurement              |
| (unknown)                                | c) rhi                          | 200.00000000000003        |      NOT a measurement           |
| (unknown)                                | C)                              | 16.780557104417564        |                |
| (unknown)                                | for b - ac                      | 199.99999999999997        |   NOT a measurement              |
| (unknown)                                | for b - LL                      | 199.99999999999997        |    NOT a measurement             |
| (unknown)                                | RL-LL                           | 16.411239690454           |   NOT a measurement              |
| (unknown)                                | B)                              | 6.174772055952712         |                |
| (unknown)                                | A FHP                           | 199.99491973323728        |  NOT a measurement               |
| (unknown)                                | E)                              | 52.17057002558945         |                |
| (unknown)                                | aca FHP                         | 199.99491973323728        |    NOT a measurement             |
| (unknown)                                | A FHP                           | 199.99491973323728        |    NOT a measurement             |
| (unknown)                                | Mala 2B aca FHP                 | 12.349544111905423        |     NOT a measurement            |
| (unknown)                                | Mala 2B A FHP                   | 12.349544111905422        |    NOT a measurement             |
| (unknown)                                | x pred - 1                      | 27.753974269365074        |                |
| (unknown)                                | y pred - 1                      | 38.607058178783475        |                |
| (unknown)                                | x pred - 2                      | 27.753974269365074        |                |
| (unknown)                                | y pred - 2                      | 40.41476232734055         |                |
| (unknown)                                | x pred - 3                      | 27.753974269365074        |                |
| (unknown)                                | y pred - 3                      | 41.69080778370853         |                |
| (unknown)                                | x para - 1                      | 149.99618979992795        |    NOT a measurement             |
| (unknown)                                | y para - 1                      | 149.99999999999997        |    NOT a measurement             |
| (unknown)                                | pronasale to soft tissue - 1    | 7.312906198376119         |                |
| (unknown)                                | x para - 2                      | 149.99618979992795        |   NOT a measurement              |
| (unknown)                                | y para - 2                      | 150.00000000000003        |   NOT a measurement              |
| (unknown)                                | pronasale to soft tissue - 2    | 6.146937792548341         |                |
| (unknown)                                | x para - 3                      | 149.99618979992795        |  NOT a measurement               |
| (unknown)                                | y para - 3                      | 149.99999999999997        |     NOT a measurement            |
| (unknown)                                | pronasale to soft tissue - 3    | 5.5354982411580185        |                |
| (unknown)                                | A) nasal bone angle             | 62.58358748231047         |                |
| (unknown)                                | D) nasal spine angle - opt 1    | 44.991984371199365        |                |
| (unknown)                                | D) nasal spine angle - opt 2    | 27.66704286039727         |                |
| (unknown)                                | D) nasal spine angle - opt 3    | 15.437490300955561        |                |

> [!WARNING]
> DO NOT use pseudo or not true measurements in data analysis. Anything marked with "NOT a measurement" is programmatically established for a certain length for reference axes, therefore are not representing the measurement accuracy of the method!


## Bibliography: 

[^1]:  [Slicer Script Repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
[^2]:  Stephan, C.N., Henneberg, M. and Sampson, W. (2003), Predicting nose projection and pronasale position in facial approximation: A test of published methods and proposal of new guidelines. Am. J. Phys. Anthropol., 122: 240-250. https://doi.org/10.1002/ajpa.10300
[^3]: Gerasimov M. 1971. The face ﬁnder. London: Hutchinson & Co.
[^4]:Krogman WM. 1962. The human skeleton in forensic medicine.Springﬁeld, IL: Charles C. Thomas
[^5]: Prokopec M, Ubelaker DH. 2002. Reconstructing the shape of the nose according to the skull. Forensic Sci Commun 4. p 1– 4 (https://archives.fbi.gov/archives/about-us/lab/forensic-science-communications/fsc/jan2002/prokopec.htm)
[^6]: George RM. 1987. The lateral craniographic method of facial reconstruction. J Forensic Sci 32:1305–1330.
[^7]: Rynn, C., Wilkinson, C.M. & Peters, H.L. Prediction of nasal morphology from the skull. Forensic Sci Med Pathol 6, 20–34 (2010). https://doi.org/10.1007/s12024-009-9124-6
[^8]: Mala PZ. Pronasale position: an appraisal of two recently proposed methods for predicting nasal projection in facial reconstruction. J Forensic Sci. 2013 Jul;58(4):957-63. doi: 10.1111/1556-4029.12128. Epub 2013 May 21. PMID: 23692276.
[^9]: Caple, J. and C. N. Stephan (2016). "A standardized nomenclature for craniofacial and facial anthropometry." Int J Legal Med 130(3): 863-879.
