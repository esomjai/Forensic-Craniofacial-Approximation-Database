# Prokopec and Ubelaker, 2002[^2] - The Aesthetic Method

The following guide is constructed by the available original study by [Prokopec and Ubelaker, 2002](https://archives.fbi.gov/archives/about-us/lab/forensic-science-communications/fsc/jan2002/prokopec.htm) and its interpretation by Rynn et al, (2010)[^3].
The original method seems to be done in 2 dimensions on the bony and soft tissue profiles, but Rynn et al. (2010)[^3] also applied it in 3D. This approach is also applied in three dimensions with adjustments to accommodate to such, for example using planes instead of lines and supplementary lines for precision. 

This will be achieved by:

- Creating the [INB plane](#inb-plane), [NP plane](#np-plane) and [PT plane](#pt-plane) as defined by Rynn et al. (2010)
- Using [Maximum nasal width](#maximum-nasal-width) and the rhinion as the reference for equidistant planes
-  Choosing your [number of planes](#choose-a-number-of-planes) 
- Creating [reference lines along the INB](#reference-lines-along-the-inb-and-456-mirror-planes) and 4/5/6 mirror planes
- Establishing and adjusting [reference lines A and B](#reference-lines-a-and-b)
- Creating the mirror points by finding the [intersection points between Line B and the INB intersection lines](#intersection-points-between-line-b-and-the-intersection-lines)
  - Establishing the [optional Line A intersections](#optional-line-a-intersections)
- Placing additional [nasal bone outline landmarks](#nasal-bone-outline-landmarks)
- Placing [soft tissue nose outline landmarks](#soft-tissue-nose-outline-landmarks)
  - Optionally, adjusting these in the profile plane
- Creating the relevant [measurement lines](#measurement-lines)
  - [Nasal bone outline connecting lines](#nasal-bone-outline-connecting-lines)
  - [Their intersections with Line B](#nasal-bone-outline-connecting-lines--their-intersections-with-line-b)
  - [Distances between Line A and nose profile & Line A and nasal aperture](#distances-between-line-a-and-nose-profile--line-a-and-nasal-aperture)
- Understanding the [Output](#output)
- [Extra codes for more ideas](#extra-codes-for-more-ideas)
- [Bibliography](#bibliography)

> [!WARNING]
> The sample CT (CBCT PreDentalSurgery) used in the screenshots of this guide does not have all the features (inion, bregma) that are to be landmarked. Please refer to the illustrations in the guide for correct placement. In addition, due to the CT being taken pre-surgery for an underbite, the error rate shown in the guide is probably not representative if implemented on a population without pathologies.



Landmarks in this guide: 
| Position in code | Position in file | Name in file | Landmark name | Definition                                                                                                                     | Defined by            |
|------------------|------------------|--------------|---------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| 0                | 1                | nasion       | nasion        | Intersection of the nasofrontal sutures in the median plane                                                                    | Rynn et al. 2010[^3]      |
| 1                | 2                | inion        | inion         | Median point between the apices of the superior nuchal lines and at the base of the external occipital protuberance (not the tip of the protuberance) | Rynn et al. 2010[^3]      |
| 2                | 3                | bregma       | bregma        | Where the sagittal and coronal sutures meet. Impossible to determine in juvenile skulls with anterior fontanelle, or with complete suture obliteration | Rynn et al. 2010[^3]      |
| 3                | 4                | prosthion     | prosthion       | Median point between the central incisors on the anterior most margin of the maxillary alveolar rim | Rynn et al. 2010[^3]      |
| 4                | 5                | subspinale      | subspinale       | The deepest point seen in the profile view below the anterior nasal spine (orthodontic point A) | Caple and Stephan 2016 [^6]     |
| 5                | 6                | rhinion   | rhinion   | Most rostral (end) point on the internasal suture.          |  Rynn et al. 2010[^3] |
| 6                | 7                | acanthion    | acanthion     | Most anterior tip of the anterior nasal spine                                                                                 | Rynn et al. 2010[^3]     |





Illustration of the method: 

> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

- [ ] The scan has to be re-aligned in the FHP
- [ ] You should have a Bone and Skin model via segmentation (explained later)
- [ ] Allocate ALL landmarks from the [hard_tissue_PU.mrk.json](https://github.com/user-attachments/files/20212741/hard_tissue_PU.mrk.json)
 file 



### INB plane

To help with the side profile, we will establish the “INB” plane as defined by Rynn et al. 2010[^3]. 

> a midsagittal plane (INB) which bisected the inion, nasion and bregma

by downloading markups file for this method, allocating the landmarks  and copying and pasting the following code: 

```python
#INB plane#

import numpy as np
import slicer

# Get the points from the "hard_tissue_PU" node
hardTissueNode = slicer.util.getNode('hard_tissue_PU')
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
<img src="https://github.com/user-attachments/assets/e651bf90-5d0b-4502-b26a-a53b19de2b9b" width="500">


View of the generated INB 
<img src="https://github.com/user-attachments/assets/5c525822-9a71-4c2b-9b22-18bbd3ef6936" width="500">


INB extended via the toggles (dots)

### NP plane
May be referred to as NPP - nasion-prosthion plane; defined by Rynn as 

> a coronal plane which bisects the nasion and prosthion in lateral view, whilst lying at right angles to INB

To create this plane, use this code: 

```python

#NPP#
import numpy as np
import slicer

# Get the 'INB' plane node
inbPlaneNode = slicer.util.getNode('INB')

# Get the 'hard_tissue_PU' point list node
hardTissueNode = slicer.util.getNode('hard_tissue_PU')

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

print("New plane 'NPP' created successfully.")

```



<img src="https://github.com/user-attachments/assets/a567ed66-7091-4934-87d4-c8b5146509fe" width="500">

Immediate view after the code implemented

You can change the colour of the planes for more contrast (and is good practice when using more planes) by double-clicking on the colour square of the plane in the Markups module and choosing a different one. 
<img src="https://github.com/user-attachments/assets/105f9621-7e04-4dd0-9e9a-74ac920ee7cb" width="500">


This screenshot shows the two different planes (NPP with yellow, INB with purple) after extending the INB
<img src="https://github.com/user-attachments/assets/529fdf50-7a4e-4804-9ac5-501cacae1c9c" width="500">



### PT plane
May be referred to as PTP - Prokopec Transverse plane; defined by Rynn as 

> a transverse plane set at right angles to both the INB plane and the NPP, corresponding with the profile prediction lines used by Prokopec and Ubelaker

To create this plane, use this code: 

```python

#PTP#
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

print("New plane 'PTP' created successfully.")

```
<img src="https://github.com/user-attachments/assets/5da113b9-cd62-4fc9-b723-05df297708b9" width="500">

Expected view with all three planes established and extended. Landmarks hidden for representative purposes. 

### Maximum nasal width

Rynn et al. (2012) refined the original description from Prokopec and Ubelaker (2002) "4 to 6 equidistant planes" to be constrained to in-between the level of the maximum nasal width and rhinion.  

You will need to switch to the "Skin" model or use the toggle to reveal the soft tissue on the scan for this step. 
[Download maximum_nasal_width_MAW.mrk.json](https://github.com/user-attachments/files/20212751/maximum_nasal_width_MAW.mrk.json)
, and drag-and-drop it into the "Markups" environment (click OK on this pop-up - see screenshot below).
<img src="https://github.com/user-attachments/assets/9962ad54-f710-4e19-86a2-71f10450b18d" width="500">


This item will appear on your markups list with "empty endpoints" - that's completely fine, find the 
![image](https://github.com/user-attachments/assets/06ce0f82-0574-4901-a0ab-9e1f0638ec58)
icon in the second line of menu to start placing the points.
<img src="https://github.com/user-attachments/assets/80709e15-2a69-4007-a77f-54af1ee57b7f" width="500">


The goal here is to have a linear measurement from the anterior view at the maximum width of the soft nose. 

<img src="https://github.com/user-attachments/assets/768511bf-3b65-4015-91a3-7f3a7a5c1ed5" width="500">

Now, your "Control Points">"Coordinates" menu should be populated by the two endpoints and a measurement in mm should also show up in the "Node" table. 

![image](https://github.com/user-attachments/assets/65bfd3e0-fa64-44f7-897e-ca8e63718bf1)

((((DIAGRAM)))))



## Choose a number of Planes

Depending on your choosing, run the codes for the 4/5/6 mirror planes - or all three for comparison. 

<details>

<summary>Code for 4 mirror planes</summary>

#### Code for 4 mirror planes
```python
#4 mirror planes#
import slicer
import numpy as np

# Get the PTP plane node
ptpPlaneNode = slicer.util.getNode('PTP')

# Get the MAW measurement position (assuming it's stored in a node)
# Replace 'MAW' with the actual node name or method to get the MAW position
mawNode = slicer.util.getNode('maximum nasal width MAW')
mawPosition = np.array(mawNode.GetNthControlPointPositionWorld(0))  # Adjust index if needed

# Get the PTP plane position and normal
ptpPlanePosition = np.array(ptpPlaneNode.GetOrigin())
ptpPlaneNormal = np.array(ptpPlaneNode.GetNormal())

# Create the new plane "A" at the MAW level
planeA = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'Plane_A')
planeA.SetOrigin(mawPosition)
planeA.SetNormal(ptpPlaneNormal)

# Get the hard_tissue_PU node position
hardTissueNode = slicer.util.getNode('hard_tissue_PU')
rhinionPosition = np.array(hardTissueNode.GetNthControlPointPositionWorld(5))

# Calculate the distance between Plane_A and the rhinion
distance = np.dot(mawPosition - rhinionPosition, ptpPlaneNormal)

# Calculate the positions for the new planes B, C, D
numPlanes = 3
planePositions = [rhinionPosition + (i + 1) * distance / (numPlanes + 1) * ptpPlaneNormal for i in range(numPlanes)]

# Create new planes with names B, C, D
planeNames = ['B', 'C', 'D']
for i, pos in enumerate(planePositions):
    planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', f'Plane_{planeNames[i]}')
    planeNode.SetOrigin(pos)
    planeNode.SetNormal(ptpPlaneNormal)
```
Image if the code for 4 mirror planes is employed:
![image](https://github.com/user-attachments/assets/c684f261-e427-4d4d-8831-17dc7d7e3bbe)


</details>


<details>

<summary>Code for 5 mirror planes</summary>

#### Code for 5 mirror planes
```python
#5 mirror planes#
import slicer
import numpy as np

# Get the PTP plane node
ptpPlaneNode = slicer.util.getNode('PTP')

# Get the MAW measurement position (assuming it's stored in a node)
# Replace 'MAW' with the actual node name or method to get the MAW position
mawNode = slicer.util.getNode('maximum nasal width MAW')
mawPosition = np.array(mawNode.GetNthControlPointPositionWorld(0))  # Adjust index if needed

# Get the PTP plane position and normal
ptpPlanePosition = np.array(ptpPlaneNode.GetOrigin())
ptpPlaneNormal = np.array(ptpPlaneNode.GetNormal())

# Create the new plane "A" at the MAW level
planeA = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'Plane_A')
planeA.SetOrigin(mawPosition)
planeA.SetNormal(ptpPlaneNormal)

# Get the hard_tissue_PU node position
hardTissueNode = slicer.util.getNode('hard_tissue_PU')
rhinionPosition = np.array(hardTissueNode.GetNthControlPointPositionWorld(5))

# Calculate the distance between Plane_A and the rhinion
distance = np.dot(mawPosition - rhinionPosition, ptpPlaneNormal)# Calculate the positions for the new planes B, C, D, E
numPlanes = 4  # Change this to 4 to create 5 planes in total (A, B, C, D, E)
planePositions = [rhinionPosition + (i + 1) * distance / (numPlanes + 1) * ptpPlaneNormal for i in range(numPlanes)]

# Create new planes with names B, C, D, E
planeNames = ['B', 'C', 'D', 'E']
for i, pos in enumerate(planePositions):
    planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', f'Plane_{planeNames[i]}')
    planeNode.SetOrigin(pos)
    planeNode.SetNormal(ptpPlaneNormal)
```

Image if the code for 5 mirror planes is employed: 

![image](https://github.com/user-attachments/assets/ea7b9888-95b6-436c-892d-ada9f77f2a6b)


</details>

<details>

<summary>Code for 6 mirror planes</summary>

#### Code for 6 mirror planes
```python
#6 mirror planes#
import slicer
import numpy as np

# Get the PTP plane node
ptpPlaneNode = slicer.util.getNode('PTP')

# Get the MAW measurement position (assuming it's stored in a node)
mawNode = slicer.util.getNode('maximum nasal width MAW')
mawPosition = np.array(mawNode.GetNthControlPointPositionWorld(0))  # Adjust index if needed

# Get the PTP plane position and normal
ptpPlanePosition = np.array(ptpPlaneNode.GetOrigin())
ptpPlaneNormal = np.array(ptpPlaneNode.GetNormal())

# Create the new plane "A" at the MAW level
planeA = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'Plane_A')
planeA.SetOrigin(mawPosition)
planeA.SetNormal(ptpPlaneNormal)

# Get the hard_tissue_PU node position
hardTissueNode = slicer.util.getNode('hard_tissue_PU')
rhinionPosition = np.array(hardTissueNode.GetNthControlPointPositionWorld(5))

# Calculate the distance between Plane_A and the rhinion
distance = np.dot(mawPosition - rhinionPosition, ptpPlaneNormal)

# Calculate the positions for the new planes B, C, D, E, F
numPlanes = 5  # Change this to 5 to create 6 planes in total (A, B, C, D, E, F)
planeNames = ['B', 'C', 'D', 'E', 'F']
planePositions = [rhinionPosition + (i + 1) * distance / (numPlanes + 1) * ptpPlaneNormal for i in range(numPlanes)]

# Create new planes with names B, C, D, E, F
for i, pos in enumerate(planePositions):
    planeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', f'Plane_{planeNames[i]}')
    planeNode.SetOrigin(pos)
    planeNode.SetNormal(ptpPlaneNormal)
```

Image if the code for 6 mirror planes is employed:
![image](https://github.com/user-attachments/assets/8f635b63-27e2-4857-ae29-1d87db13f103)

</details>


### Reference lines along the INB and 4/5/6 mirror planes

This step establishes the 4/5/6 intersection lines where the individual mirror planes meet the INB plane. 

<details>

<summary>Code for 4 intersection lines </summary>

#### Code for 4 intersection lines of 4 mirror planes
```python
#########making 4 intersection lines along INB and each mirror plane########
	# Function to create intersection line between two planes
def create_intersection_line(planeNode1, planeNode2, lineNodeName):
    # Create a new line node for the intersection line
    intersectionLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', lineNodeName)

    # Get the normal vectors and points on the planes
    normal1 = np.array(planeNode1.GetNormalWorld())
    point1 = np.array(planeNode1.GetOriginWorld())
    normal2 = np.array(planeNode2.GetNormalWorld())
    point2 = np.array(planeNode2.GetOriginWorld())

    # Calculate the direction vector of the intersection line
    direction = np.cross(normal1, normal2)

    # Check if the planes are parallel
    if np.linalg.norm(direction) == 0:
        print(f"The planes {planeNode1.GetName()} and {planeNode2.GetName()} are parallel and do not intersect.")
    else:
        # Calculate a point on the intersection line
        A = np.array([normal1, normal2, direction])
        b = np.array([np.dot(normal1, point1), np.dot(normal2, point2), 0])
        intersection_point = np.linalg.solve(A, b)

        # Define the start and end points of the line, extending further
        extension_factor = 1000  # Adjust this factor as needed
        start_point = intersection_point - extension_factor * direction
        end_point = intersection_point + extension_factor * direction

        # Set the points in the line node
        intersectionLineNode.AddControlPointWorld(start_point)
        intersectionLineNode.AddControlPointWorld(end_point)

        print(f"Extended intersection line {lineNodeName} created successfully.")

# List of plane pairs and corresponding line node names
plane_pairs = [
    ('INB', 'Plane_A', 'INB_A'),
    ('INB', 'Plane_B', 'INB_B'),
    ('INB', 'Plane_C', 'INB_C'),
    ('INB', 'Plane_D', 'INB_D')
]

# Iterate over each pair and create the intersection lines
for plane1, plane2, lineName in plane_pairs:
    planeNode1 = getNode(plane1)
    planeNode2 = getNode(plane2)
    create_intersection_line(planeNode1, planeNode2, lineName)
```

![image](https://github.com/user-attachments/assets/016c35b3-83e6-46ed-8151-ae9d48c79124)


</details>


<details>

<summary>Code for 5 intersection lines </summary>

#### Code for 5 intersection lines of 5 mirror planes
```python
#########making intersection lines along INB and each mirror plane########
# Function to create intersection line between two planes
def create_intersection_line(planeNode1, planeNode2, lineNodeName):
    # Create a new line node for the intersection line
    intersectionLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', lineNodeName)

    # Get the normal vectors and points on the planes
    normal1 = np.array(planeNode1.GetNormalWorld())
    point1 = np.array(planeNode1.GetOriginWorld())
    normal2 = np.array(planeNode2.GetNormalWorld())
    point2 = np.array(planeNode2.GetOriginWorld())

    # Calculate the direction vector of the intersection line
    direction = np.cross(normal1, normal2)

    # Check if the planes are parallel
    if np.linalg.norm(direction) == 0:
        print(f"The planes {planeNode1.GetName()} and {planeNode2.GetName()} are parallel and do not intersect.")
    else:
        # Calculate a point on the intersection line
        A = np.array([normal1, normal2, direction])
        b = np.array([np.dot(normal1, point1), np.dot(normal2, point2), 0])
        intersection_point = np.linalg.solve(A, b)

        # Define the start and end points of the line, extending further
        extension_factor = 1000  # Adjust this factor as needed
        start_point = intersection_point - extension_factor * direction
        end_point = intersection_point + extension_factor * direction

        # Set the points in the line node
        intersectionLineNode.AddControlPointWorld(start_point)
        intersectionLineNode.AddControlPointWorld(end_point)

        print(f"Extended intersection line {lineNodeName} created successfully.")

# List of plane pairs and corresponding line node names
plane_pairs = [
    ('INB', 'Plane_A', 'INB_A'),
    ('INB', 'Plane_B', 'INB_B'),
    ('INB', 'Plane_C', 'INB_C'),
    ('INB', 'Plane_D', 'INB_D'),
    ('INB', 'Plane_E', 'INB_E')  # Add the fifth plane pair here
]

# Iterate over each pair and create the intersection lines
for plane1, plane2, lineName in plane_pairs:
    create_intersection_line(slicer.util.getNode(plane1), slicer.util.getNode(plane2), lineName)
```
Image after the 5 line code is iterated: 
![image](https://github.com/user-attachments/assets/3bc4b9d2-63a3-47ad-9dbe-43a81f2490c3)


</details>

<details>

<summary>Code for 6 intersection lines </summary>

#### Code for 6 intersection lines of 6 mirror planes
```python
#########making intersection lines along INB and each mirror plane########
# Function to create intersection line between two planes
def create_intersection_line(planeNode1, planeNode2, lineNodeName):
    # Create a new line node for the intersection line
    intersectionLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', lineNodeName)

    # Get the normal vectors and points on the planes
    normal1 = np.array(planeNode1.GetNormalWorld())
    point1 = np.array(planeNode1.GetOriginWorld())
    normal2 = np.array(planeNode2.GetNormalWorld())
    point2 = np.array(planeNode2.GetOriginWorld())

    # Calculate the direction vector of the intersection line
    direction = np.cross(normal1, normal2)

    # Check if the planes are parallel
    if np.linalg.norm(direction) == 0:
        print(f"The planes {planeNode1.GetName()} and {planeNode2.GetName()} are parallel and do not intersect.")
    else:
        # Calculate a point on the intersection line
        A = np.array([normal1, normal2, direction])
        b = np.array([np.dot(normal1, point1), np.dot(normal2, point2), 0])
        intersection_point = np.linalg.solve(A, b)

        # Define the start and end points of the line, extending further
        extension_factor = 1000  # Adjust this factor as needed
        start_point = intersection_point - extension_factor * direction
        end_point = intersection_point + extension_factor * direction

        # Set the points in the line node
        intersectionLineNode.AddControlPointWorld(start_point)
        intersectionLineNode.AddControlPointWorld(end_point)

        print(f"Extended intersection line {lineNodeName} created successfully.")

# List of plane pairs and corresponding line node names
plane_pairs = [
    ('INB', 'Plane_A', 'INB_A'),
    ('INB', 'Plane_B', 'INB_B'),
    ('INB', 'Plane_C', 'INB_C'),
    ('INB', 'Plane_D', 'INB_D'),
    ('INB', 'Plane_E', 'INB_E'),
    ('INB', 'Plane_F', 'INB_F')  # Add the sixth plane pair here
]

# Iterate over each pair and create the intersection lines
for plane1, plane2, lineName in plane_pairs:
    create_intersection_line(slicer.util.getNode(plane1), slicer.util.getNode(plane2), lineName)

```
Image after the 6 line code is iterated: 
![image](https://github.com/user-attachments/assets/2feed628-718b-4a3c-a888-fa5e4abe988d)


</details>

### Reference lines A and B
After this, we establish the lines of reference which are perpendicular to the mirror planes– one along the nasion-prosthion and one parallel to the nasion-prosthion bisecting the rhinion by copy-pasting code “reference lines A and B”. We are using thie same code for ALL options (4/5/6 mirror planes)!

```python

###reference lines A and B###
import slicer
import vtk

# Get the "hard_tissue_PU" node
F = slicer.util.getNode('hard_tissue_PU')

# Create the first line node
L_A = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'Line_A')

# Retrieve and add the first point (position 0)
firstPoint = F.GetNthControlPointPositionVector(0)
L_A.AddControlPoint(firstPoint)

# Retrieve and add the second point (position 3)
secondPoint = F.GetNthControlPointPositionVector(3)
L_A.AddControlPoint(secondPoint)

# Retrieve the point at position 5
thirdPoint = F.GetNthControlPointPositionVector(5)

# Calculate the direction vector of the first line
directionVector = vtk.vtkVector3d()
directionVector.SetX(secondPoint.GetX() - firstPoint.GetX())
directionVector.SetY(secondPoint.GetY() - firstPoint.GetY())
directionVector.SetZ(secondPoint.GetZ() - firstPoint.GetZ())

# Create the second line node
L_B = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'Line_B')

# Add the third point (position 5)
L_B.AddControlPoint(thirdPoint)

# Extend the direction vector by a factor (e.g., 2 for doubling the length)
factor = 2
extendedDirectionVector = vtk.vtkVector3d()
extendedDirectionVector.SetX(directionVector.GetX() * factor)
extendedDirectionVector.SetY(directionVector.GetY() * factor)
extendedDirectionVector.SetZ(directionVector.GetZ() * factor)

# Calculate and add the fourth point (extended)
fourthPoint = vtk.vtkVector3d()
fourthPoint.SetX(thirdPoint.GetX() + extendedDirectionVector.GetX())
fourthPoint.SetY(thirdPoint.GetY() + extendedDirectionVector.GetY())
fourthPoint.SetZ(thirdPoint.GetZ() + extendedDirectionVector.GetZ())
L_B.AddControlPoint(fourthPoint)

```
This screenshot shows how these lines should look like after the code, with the "Bone" model or toggled view for hard tissue and every other markup hidden. 
![image](https://github.com/user-attachments/assets/6eb075b7-af7c-4bac-bae0-96a38987eac6)

Now, some manual adjustments are required to proceed: As you can see, Line_B needs to be toggled along itself as it is currently starting at the rhinion and we need it spanning before and after its determining landmarks. To do that, click on the “Line_B” icon in the **Node List** in **Markups** and scroll down to “_Display_ options and click on _Interaction handles_. Enable **Visibility** and **Translation**, then use the red arrow to pull the line upwards without changing its direction:


https://github.com/user-attachments/assets/53d1ad03-793b-43b3-abc6-ef4b172b0f5d



### Intersection points between Line B and the intersection lines

The intersection points (called “mirror points” in the code) of planes A, B, C etc with Line_B will be added by the next code, with hot pink showing them. Choose “B intersection points 4” “B intersection points 5” or “B intersection points 6” according to the number of your planes. Optionally, if you wish to compare the curvature of the bony and soft nasal profile, you can also establish the same intersection points for Line A - scroll down to heading _Intersection points between Line A and intersection lines_ for this extra snippet. 

<details>

<summary>4 plane Line B intersection </summary>

#### Code for Line B intersection points 4 planes

```python
###B intersection points 4####
import numpy as np
import slicer

# Assuming 'Line_B' and 'INB_A', 'INB_B', 'INB_C', 'INB_D' are already defined in the scene
lineNode_B = slicer.util.getNode('Line_B')
lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D']

def get_line_points(lineNode):
    startPoint = np.array([0.0, 0.0, 0.0])
    endPoint = np.array([0.0, 0.0, 0.0])
    lineNode.GetNthControlPointPositionWorld(0, startPoint)
    lineNode.GetNthControlPointPositionWorld(1, endPoint)
    return startPoint, endPoint

def find_line_intersection(line1Node, line2Node):
    # Get points and directions of the lines
    p1, p2 = get_line_points(line1Node)
    d1 = p2 - p1
    q1, q2 = get_line_points(line2Node)
    d2 = q2 - q1

    # Normalize directions
    d1 /= np.linalg.norm(d1)
    d2 /= np.linalg.norm(d2)

    # Calculate intersection
    cross_d1_d2 = np.cross(d1, d2)
    if np.linalg.norm(cross_d1_d2) == 0:
        return None  # Lines are parallel

    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
    intersection_point = p1 + t * d1
    return intersection_point

for i, line_name in enumerate(lines):
    line2Node = slicer.util.getNode(line_name)
    intersection_point = find_line_intersection(lineNode_B, line2Node)
    if intersection_point is not None:
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
        fiducialNode.AddControlPointWorld(intersection_point)
        # Set the color to hot pink (RGB: 255, 105, 180)
        displayNode = fiducialNode.GetDisplayNode()
        displayNode.SetSelectedColor(255/255, 105/255, 180/255)

```

![image](https://github.com/user-attachments/assets/2a6b319b-4054-407f-a245-43b55089599c)

</details>

<details>

<summary>5 plane Line B intersection </summary>

#### Code for Line B intersection points 5 planes

```python
###B intersection points 5####

import numpy as np
import slicer

# Assuming 'Line_B' and 'INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E' are already defined in the scene
lineNode_B = slicer.util.getNode('Line_B')
lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E']

def get_line_points(lineNode):
    startPoint = np.array([0.0, 0.0, 0.0])
    endPoint = np.array([0.0, 0.0, 0.0])
    lineNode.GetNthControlPointPositionWorld(0, startPoint)
    lineNode.GetNthControlPointPositionWorld(1, endPoint)
    return startPoint, endPoint

def find_line_intersection(line1Node, line2Node):
    # Get points and directions of the lines
    p1, p2 = get_line_points(line1Node)
    d1 = p2 - p1
    q1, q2 = get_line_points(line2Node)
    d2 = q2 - q1

    # Normalize directions
    d1 /= np.linalg.norm(d1)
    d2 /= np.linalg.norm(d2)

    # Calculate intersection
    cross_d1_d2 = np.cross(d1, d2)
    if np.linalg.norm(cross_d1_d2) == 0:
        return None  # Lines are parallel

    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
    intersection_point = p1 + t * d1
    return intersection_point

for i, line_name in enumerate(lines):
    line2Node = slicer.util.getNode(line_name)
    intersection_point = find_line_intersection(lineNode_B, line2Node)
    if intersection_point is not None:
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
        fiducialNode.AddControlPointWorld(intersection_point)
        # Set the color to hot pink (RGB: 255, 105, 180)
        displayNode = fiducialNode.GetDisplayNode()
        displayNode.SetSelectedColor(255/255, 105/255, 180/255)

```
![image](https://github.com/user-attachments/assets/b3e7883c-5f12-4f4b-86e3-ce2e35cb5966)

</details>


<details>

<summary>6 plane Line B intersection </summary>

#### Code for Line B intersection points 6 planes
```python
import numpy as np
import slicer

# Assuming 'Line_B' and 'INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F' are already defined in the scene
lineNode_B = slicer.util.getNode('Line_B')
lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']

def get_line_points(lineNode):
    startPoint = np.array([0.0, 0.0, 0.0])
    endPoint = np.array([0.0, 0.0, 0.0])
    lineNode.GetNthControlPointPositionWorld(0, startPoint)
    lineNode.GetNthControlPointPositionWorld(1, endPoint)
    return startPoint, endPoint

def find_line_intersection(line1Node, line2Node):
    # Get points and directions of the lines
    p1, p2 = get_line_points(line1Node)
    d1 = p2 - p1
    q1, q2 = get_line_points(line2Node)
    d2 = q2 - q1

    # Normalize directions
    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
        return None  # Avoid division by zero
    d1 /= np.linalg.norm(d1)
    d2 /= np.linalg.norm(d2)

    # Calculate intersection
    cross_d1_d2 = np.cross(d1, d2)
    if np.linalg.norm(cross_d1_d2) == 0:
        return None  # Lines are parallel

    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
    intersection_point = p1 + t * d1
    return intersection_point

for i, line_name in enumerate(lines):
    line2Node = slicer.util.getNode(line_name)
    if line2Node is None:
        print(f"Node {line_name} not found")
        continue
    intersection_point = find_line_intersection(lineNode_B, line2Node)
    if intersection_point is not None:
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorB_{chr(65 + i)}')
        fiducialNode.AddControlPointWorld(intersection_point)
        # Set the color to hot pink (RGB: 255, 105, 180)
        displayNode = fiducialNode.GetDisplayNode()
        displayNode.SetColor(255/255, 105/255, 180/255)
```
![image](https://github.com/user-attachments/assets/748c6a20-6caa-4419-aad2-ac1483ad3a8e)


##### Optional Line A intersections
</details>

<details>

<summary>4 plane optional Line A intersection points </summary>

### Code for optional Line A intersection points, 4 planes
```python
######Line A intersection for 4 planes############
import numpy as np
import slicer

# Assuming 'Line_A' and 'INB_A', 'INB_B', 'INB_C', 'INB_D' are already defined in the scene
lineNode = slicer.util.getNode('Line_A')
lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D']

def get_line_points(lineNode):
    startPoint = np.array([0.0, 0.0, 0.0])
    endPoint = np.array([0.0, 0.0, 0.0])
    lineNode.GetNthControlPointPositionWorld(0, startPoint)
    lineNode.GetNthControlPointPositionWorld(1, endPoint)
    return startPoint, endPoint

def find_line_intersection(line1Node, line2Node):
    # Get points and directions of the lines
    p1, p2 = get_line_points(line1Node)
    d1 = p2 - p1
    q1, q2 = get_line_points(line2Node)
    d2 = q2 - q1

    # Normalize directions
    d1 /= np.linalg.norm(d1)
    d2 /= np.linalg.norm(d2)

    # Calculate intersection
    cross_d1_d2 = np.cross(d1, d2)
    if np.linalg.norm(cross_d1_d2) == 0:
        return None  # Lines are parallel

    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
    intersection_point = p1 + t * d1
    return intersection_point

for i, line_name in enumerate(lines):
    line2Node = slicer.util.getNode(line_name)
    intersection_point = find_line_intersection(lineNode, line2Node)
    if intersection_point is not None:
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
        fiducialNode.AddControlPointWorld(intersection_point)
        # Set the color to turquoise (RGB: 64, 224, 208)
        displayNode = fiducialNode.GetDisplayNode()
        displayNode.SetSelectedColor(64/255, 224/255, 208/255)
```
Screenshot of both line (A and B) intersection points established on a 4 plane model
![image](https://github.com/user-attachments/assets/050b49d1-eb5d-4684-9949-1fdb6fa73462)

</details>

<details>

<summary>5 plane optional Line A intersection points </summary>

####Code for optional Line A intersections, 5 planes

```python
######Line A intersection for 5 planes############
import numpy as np
import slicer

# Assuming 'Line_A' and 'INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E' are already defined in the scene
lineNode = slicer.util.getNode('Line_A')
lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E']

def find_line_intersection(line1Node, line2Node):
    # Get points and directions of the lines
    p1 = np.array(line1Node.GetLineStartPositionWorld())
    d1 = np.array(line1Node.GetLineEndPositionWorld()) - p1
    p2 = np.array(line2Node.GetLineStartPositionWorld())
    d2 = np.array(line2Node.GetLineEndPositionWorld()) - p2

    # Normalize directions
    d1 /= np.linalg.norm(d1)
    d2 /= np.linalg.norm(d2)

    # Calculate intersection
    cross_d1_d2 = np.cross(d1, d2)
    if np.linalg.norm(cross_d1_d2) == 0:
        print("Lines are parallel")
        return None  # Lines are parallel

    t = np.dot(np.cross((p2 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
    intersection_point = p1 + t * d1
    return intersection_point

for i, line_name in enumerate(lines):
    line2Node = slicer.util.getNode(line_name)
    intersection_point = find_line_intersection(lineNode, line2Node)
     if intersection_point is not None:
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
        fiducialNode.AddControlPointWorld(intersection_point)
        # Set the color to turquoise (RGB: 64, 224, 208)
        displayNode = fiducialNode.GetDisplayNode()
        displayNode.SetSelectedColor(64/255, 224/255, 208/255)
    else:
        print(f"No intersection found for {line_name}")
```
Screenshot of both line (A and B) intersection points established on a 5 plane model
![image](https://github.com/user-attachments/assets/dfeef8b2-2d02-49de-a57e-1dec4c570c0d)

</details>

<details>

<summary>6 plane optional Line A intersection points </summary>

####Code for optional Line A intersection, 6 planes


```python 
######Line A intersection for 6 planes############
import numpy as np
import slicer

# Assuming 'Line_A' and 'INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F' are already defined in the scene
lineNode = slicer.util.getNode('Line_A')
lines = ['INB_A', 'INB_B', 'INB_C', 'INB_D', 'INB_E', 'INB_F']

def get_line_points(lineNode):
    startPoint = np.array([0.0, 0.0, 0.0])
    endPoint = np.array([0.0, 0.0, 0.0])
    lineNode.GetNthControlPointPositionWorld(0, startPoint)
    lineNode.GetNthControlPointPositionWorld(1, endPoint)
    return startPoint, endPoint

def find_line_intersection(line1Node, line2Node):
    # Get points and directions of the lines
    p1, p2 = get_line_points(line1Node)
    d1 = p2 - p1
    q1, q2 = get_line_points(line2Node)
    d2 = q2 - q1

    # Normalize directions
    if np.linalg.norm(d1) == 0 or np.linalg.norm(d2) == 0:
        return None  # Avoid division by zero
    d1 /= np.linalg.norm(d1)
    d2 /= np.linalg.norm(d2)

    # Calculate intersection
    cross_d1_d2 = np.cross(d1, d2)
    if np.linalg.norm(cross_d1_d2) == 0:
        return None  # Lines are parallel

    t = np.dot(np.cross((q1 - p1), d2), cross_d1_d2) / np.linalg.norm(cross_d1_d2)**2
    intersection_point = p1 + t * d1
    return intersection_point

for i, line_name in enumerate(lines):
    line2Node = slicer.util.getNode(line_name)
    if line2Node is None:
        print(f"Node {line_name} not found")
        continue
    intersection_point = find_line_intersection(lineNode, line2Node)
    if intersection_point is not None:
        fiducialNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', f'mirrorA_{chr(65 + i)}')
        fiducialNode.AddControlPointWorld(intersection_point)
        # Set the color to turquoise (RGB: 64, 224, 208)
        displayNode = fiducialNode.GetDisplayNode()
        displayNode.SetSelectedColor(64/255, 224/255, 208/255)

``` 
Screenshot of both line (A and B) intersection points established on a 6 plane model
![image](https://github.com/user-attachments/assets/4d17b458-90b3-4e8c-93a1-038d518ad0c1)

</details>

### Nasal Bone outline landmarks
Then hide these intersection points and additional information until you have ONLY the skull and the 4/5/6 lines along the INB and Plane A, B,C, D visible. These will be called INB_A, INB_B, INB_C and INB_D (additionally, INB_E and INB_F, if you have 5/6 planes). 

![image](https://github.com/user-attachments/assets/977acc5c-2ec5-4b89-b9c0-ac468ced8723)
I added the names on the screenshot, but these structures are the only ones relevant for the next steps.

Download the json files based on the number of planes you're working with: 

- [nasal bone outline 4.mrk.json](https://github.com/user-attachments/files/19318005/nasal.bone.outline.4.mrk.json)
- [nasal bone outline 5.mrk.json](https://github.com/user-attachments/files/19318009/nasal.bone.outline.5.mrk.json)
- [nasal bone outline 6.mrk.json](https://github.com/user-attachments/files/19318010/nasal.bone.outline.6.mrk.json)

Drag-and-drop into the markups environment, click OK, then plane the points manually. Make sure you have the model in the correct orientation, with the Rx points on the right and Lx points on the left. 

Example of the content of the json in the case of 4 planes

| Name | Where to place?   | 
|-----------|------------|
| R1 | where the bony nasal outline meets the first line from superior (INB_B) on the right   | 
| R2 | where the bony nasal outline meets the second line from superior (INB_C) on the right   |
| R3 | where the bony nasal outline meets the third line from superior (INB_D) on the right   | 
| R4 | where the bony nasal outline meets the fourth line from superior (INB_A) on the right   |
| L1 | where the bony nasal outline meets the first line from superior (INB_B) on the left   | 
| L2 | where the bony nasal outline meets the second line from superior INB_C) on the left   |
| L3 | where the bony nasal outline meets the third line from superior (INB_D) on the left   | 
| L4 | where the bony nasal outline meets the fourth line from superior (INB_A) on the left  |


![image](https://github.com/user-attachments/assets/8896ea6b-0a56-4991-9b7e-12e6ffc86912)

### Soft tissue nose outline landmarks

Adjust your view or call on your skin model to see the soft nose profile.
Download the applicable Markup file for your number of planes: 


- [nose profile outline 4.mrk.json](https://github.com/user-attachments/files/19327865/nose.profile.outline.4.mrk.json)
- [nose profile outline 5.mrk.json](https://github.com/user-attachments/files/19327866/nose.profile.outline.5.mrk.json)
- [nose profile outline 6.mrk.json](https://github.com/user-attachments/files/19327871/nose.profile.outline.6.mrk.json)

Example of the content of the json in the case of 4 planes

| Name | Where to place?   | 
|-----------|------------|
| 1 | where the soft nose surface meets the first line from superior (INB_B) in the middle   | 
| 2 | where the soft nose surface  meets the second line from superior (INB_C) in the middle   |
| 3 | where the soft nose surface  meets the third line from superior (INB_D) in the middle   | 
| 4 | where the soft nose surface  meets the fourth line from superior (INB_A) in the middle   |


Drag and drop “nose profile outline4/5/6” into the Markups environment and place the dots 1…4/5/6 along the nasal profile and line intersections. Make sure these meet the lines - a slightly turned view is the most helpful for this. 
Example for the position of the model and placement of points for 4 planes: 
![image](https://github.com/user-attachments/assets/5897c99a-cba1-4d0a-9aaf-8ff7c625375a)

<details>

<summary>Are the labels in the way to place these points?</summary>

### Does your scene look a bit like this?
NB: this is a 5-plane workflow screenshot

<img src="https://github.com/user-attachments/assets/8e74b437-4f9d-4827-9d0d-3ee2544d38b5" width="500">

If you go to Markups, choose your line the label of which in the way (INB_A in the example here), then choose **Display**>_Advanced_, scroll down to **Properties Label** and untick it, it should hide the label from view. 

![image](https://github.com/user-attachments/assets/9ee86616-8d93-4eaa-960b-e8526cebb3d4)

</details>

The reason for handling the soft and hard tissue differently in this case is due to their shapes: the nose has a convex, the nasal orifice has a concave geometry that is harder to measure without any metadata adjustments (to avoid “eyeballing” and interpretative errors and improve reproducibility). Instead, we mark the outline of the nasal aperture on both sides, connect them (R1 ro L1 etc.) and check it they meet the “mirror” line B.


### Measurement lines 
This will be a 3-step process  regardless of how many planes you choose for your process. Copy, paste and run code below for your number of planes
#### Nasal bone outline connecting lines
 1.This step creates the lines between the nasal bone outline points R1-L1, etc. and names them “nasal outline1” etc

<details>

<summary>Code for 4-plane nasal outline lines</summary>

``` python
###  4 nasal outline lines
import slicer

# Get the point list node
pointListNode = slicer.util.getNode('nasal bone outline 4')

# Function to get point coordinates by index
def getPointCoordinatesByIndex(pointListNode, index):
    if index < pointListNode.GetNumberOfControlPoints():
        position = [0.0, 0.0, 0.0]
        pointListNode.GetNthControlPointPosition(index, position)
        return position
    return None

# Add linear markups for each pair of points
pointPairs = [(0, 4), (1, 5), (2, 6), (3, 7)]
for index, pair in enumerate(pointPairs):
    point1 = getPointCoordinatesByIndex(pointListNode, pair[0])
    point2 = getPointCoordinatesByIndex(pointListNode, pair[1])
    
    if point1 is not None and point2 is not None:
        # Check if a node with the same name already exists
        existingNode = slicer.mrmlScene.GetFirstNodeByName(f'nasal outline{index + 1}')
        if existingNode is None:
            # Create a new linear markup node
            lineMarkupNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
            lineMarkupNode.SetName(f'nasal outline{index + 1}')
            
            # Add points to the linear markup
            lineMarkupNode.AddControlPoint(point1)
            lineMarkupNode.AddControlPoint(point2)
            
            # Set the color to baby blue (RGB: 137, 207, 240)
            displayNode = lineMarkupNode.GetDisplayNode()
            displayNode.SetSelectedColor(137/255, 207/255, 240/255)
        else:
            print(f'Node nasal outline{index + 1} already exists.')
    else:
        print(f'Points for indices {pair[0]} or {pair[1]} not found.')
```

<img src="https://github.com/user-attachments/assets/be8c5f36-b083-4f39-bdf9-8b5f6d1e8127" width="500">

</details>

<details>

<summary>Code for 5-plane nasal outline lines</summary>

``` python
###  5 nasal outline lines
import slicer

# Get the point list node
pointListNode = slicer.util.getNode('nasal bone outline 5')

# Function to get point coordinates by index
def getPointCoordinatesByIndex(pointListNode, index):
    if index < pointListNode.GetNumberOfControlPoints():
        position = [0.0, 0.0, 0.0]
        pointListNode.GetNthControlPointPosition(index, position)
        return position
    return None

# Add linear markups for each pair of points
pointPairs = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
for index, pair in enumerate(pointPairs):
    point1 = getPointCoordinatesByIndex(pointListNode, pair[0])
    point2 = getPointCoordinatesByIndex(pointListNode, pair[1])
    
    if point1 is not None and point2 is not None:
        # Check if a node with the same name already exists
        existingNode = slicer.mrmlScene.GetFirstNodeByName(f'nasal outline{index + 1}')
        if existingNode is None:
            # Create a new linear markup node
            lineMarkupNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
            lineMarkupNode.SetName(f'nasal outline{index + 1}')
            
            # Add points to the linear markup
            lineMarkupNode.AddControlPoint(point1)
            lineMarkupNode.AddControlPoint(point2)
            
            # Set the color to baby blue (RGB: 137, 207, 240)
            displayNode = lineMarkupNode.GetDisplayNode()
            displayNode.SetSelectedColor(137/255, 207/255, 240/255)
        else:
            print(f'Node nasal outline{index + 1} already exists.')
    else:
        print(f'Points for indices {pair[0]} or {pair[1]} not found.')
```
![image](https://github.com/user-attachments/assets/5937085a-9e71-4d86-848f-7bde519f8768)

<img src="https://github.com/user-attachments/assets/5937085a-9e71-4d86-848f-7bde519f8768" width="500">

</details>

<details>

<summary>Code for 6-plane nasal outline lines</summary>

``` python
###  6 nasal outline lines
def getPointCoordinatesByIndex(pointListNode, index):
    if index < pointListNode.GetNumberOfControlPoints():
        position = [0.0, 0.0, 0.0]
        pointListNode.GetNthControlPointPosition(index, position)
        return position
    return None

# Add linear markups for each pair of points
pointPairs = [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]
for index, pair in enumerate(pointPairs):
    if pair[0] < pointListNode.GetNumberOfControlPoints() and pair[1] < pointListNode.GetNumberOfControlPoints():
        point1 = getPointCoordinatesByIndex(pointListNode, pair[0])
        point2 = getPointCoordinatesByIndex(pointListNode, pair[1])
        
        if point1 is not None and point2 is not None:
            # Check if a node with the same name already exists
            existingNode = slicer.mrmlScene.GetFirstNodeByName(f'nasal outline{index + 1}')
            if existingNode is None:
                # Create a new linear markup node
                lineMarkupNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
                lineMarkupNode.SetName(f'nasal outline{index + 1}')
                
                # Add points to the linear markup
                lineMarkupNode.AddControlPoint(point1)
                lineMarkupNode.AddControlPoint(point2)
                
                # Set the color to baby blue (RGB: 137, 207, 240)
                displayNode = lineMarkupNode.GetDisplayNode()
                displayNode.SetSelectedColor(137/255, 207/255, 240/255)
            else:
                print(f'Node nasal outline{index + 1} already exists.')
        else:
            print(f'Points for indices {pair[0]} or {pair[1]} not found.')
    else:
        print(f'Indices {pair[0]} or {pair[1]} are out of range.')
```
![image](https://github.com/user-attachments/assets/7cb83356-6e1d-43a2-8b13-ba0973ae15db)

<img src="https://github.com/user-attachments/assets/7cb83356-6e1d-43a2-8b13-ba0973ae15db" width="500"]>

</details>




#### Nasal bone outline connecting lines & their intersections with Line B
 2. This step finds the intersection points of these R-L nasal aperture lines and Line B in magenta, and names them “bone1” etc 

<details>

<summary>Code for 4-plane nasal outline & Line B</summary>

``` python
###  4 planes - nasal outline and Line B

```

<img src="https://github.com/user-attachments/assets/d9f9f43d-acc8-4c64-9aa1-4595069e1caa" width="500">

</details>

<details>

<summary>Code for 5-plane nasal outline & Line B</summary>

``` python
###  5  planes - nasal outline and Line B
import slicer
import numpy as np

def get_line_points(line_node):
    points = []
    for i in range(line_node.GetNumberOfControlPoints()):
        point = [0.0, 0.0, 0.0]
        line_node.GetNthControlPointPosition(i, point)
        points.append(point)
    return points

def find_intersection(line1_points, line2_points):
    p1, p2 = np.array(line1_points[0]), np.array(line1_points[1])
    p3, p4 = np.array(line2_points[0]), np.array(line2_points[1])
    
    d1 = p2 - p1
    d2 = p4 - p3
    
    A = np.array([d1, -d2]).T
    b = p3 - p1
    t, s = np.linalg.lstsq(A, b, rcond=None)[0]
    
    intersection = p1 + t * d1
    return intersection

def create_node(name, position):
    node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', name)
    node.AddControlPoint(position)
    # Set the color to magenta (RGB: 255, 0, 255)
    displayNode = node.GetDisplayNode()
    displayNode.SetSelectedColor(255/255, 0/255, 255/255)

# Get the line nodes from the scene
nasal_outline1 = slicer.util.getNode('nasal outline1')
INB_B = slicer.util.getNode('INB_B')
nasal_outline2 = slicer.util.getNode('nasal outline2')
INB_C = slicer.util.getNode('INB_C')
nasal_outline3 = slicer.util.getNode('nasal outline3')
INB_D = slicer.util.getNode('INB_D')
nasal_outline4 = slicer.util.getNode('nasal outline4')
INB_E = slicer.util.getNode('INB_E')
nasal_outline5 = slicer.util.getNode('nasal outline5')
INB_A = slicer.util.getNode('INB_A')

# Get the points of the lines
nasal_outline1_points = get_line_points(nasal_outline1)
INB_B_points = get_line_points(INB_B)
nasal_outline2_points = get_line_points(nasal_outline2)
INB_C_points = get_line_points(INB_C)
nasal_outline3_points = get_line_points(nasal_outline3)
INB_D_points = get_line_points(INB_D)
nasal_outline4_points = get_line_points(nasal_outline4)
INB_E_points = get_line_points(INB_E)
nasal_outline5_points = get_line_points(nasal_outline5)
INB_A_points = get_line_points(INB_A)

# Find intersections
bone1 = find_intersection(nasal_outline1_points, INB_B_points)
bone2 = find_intersection(nasal_outline2_points, INB_C_points)
bone3 = find_intersection(nasal_outline3_points, INB_D_points)
bone4 = find_intersection(nasal_outline4_points, INB_E_points)
bone5 = find_intersection(nasal_outline5_points, INB_A_points)

# Create new nodes
create_node("bone1", bone1)
create_node("bone2", bone2)
create_node("bone3", bone3)
create_node("bone4", bone4)
create_node("bone5", bone5)
```
![image](https://github.com/user-attachments/assets/1a9695de-af58-4cb0-89c5-1dc7c1b85f2d)

<img src="https://github.com/user-attachments/assets/5937085a-9e71-4d86-848f-7bde519f8768" width="500">

</details>

<details>

<summary>Code for 6-plane nasal outline & Line B</summary>

``` python
###   6 planes - nasal outline and Line B
import slicer
import numpy as np

def get_line_points(line_node):
    points = []
    for i in range(line_node.GetNumberOfControlPoints()):
        point = [0.0, 0.0, 0.0]
        line_node.GetNthControlPointPosition(i, point)
        points.append(point)
    return points

def find_intersection(line1_points, line2_points):
    p1, p2 = np.array(line1_points[0]), np.array(line1_points[1])
    p3, p4 = np.array(line2_points[0]), np.array(line2_points[1])
    
    d1 = p2 - p1
    d2 = p4 - p3
    
    A = np.array([d1, -d2]).T
    b = p3 - p1
    t, s = np.linalg.lstsq(A, b, rcond=None)[0]
    
    intersection = p1 + t * d1
    return intersection

def create_node(name, position):
    node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', name)
    node.AddControlPoint(position)
    # Set the color to magenta (RGB: 255, 0, 255)
    displayNode = node.GetDisplayNode()
    displayNode.SetSelectedColor(255/255, 0/255, 255/255)

# Get the line nodes from the scene
nasal_outline1 = slicer.util.getNode('nasal outline1')
INB_B = slicer.util.getNode('INB_B')
nasal_outline2 = slicer.util.getNode('nasal outline2')
INB_C = slicer.util.getNode('INB_C')
nasal_outline3 = slicer.util.getNode('nasal outline3')
INB_D = slicer.util.getNode('INB_D')
nasal_outline4 = slicer.util.getNode('nasal outline4')
INB_E = slicer.util.getNode('INB_E')
nasal_outline5 = slicer.util.getNode('nasal outline5')
INB_F = slicer.util.getNode('INB_F')
nasal_outline6 = slicer.util.getNode('nasal outline6')
INB_A = slicer.util.getNode('INB_A')

# Get the points of the lines
nasal_outline1_points = get_line_points(nasal_outline1)
INB_B_points = get_line_points(INB_B)
nasal_outline2_points = get_line_points(nasal_outline2)
INB_C_points = get_line_points(INB_C)
nasal_outline3_points = get_line_points(nasal_outline3)
INB_D_points = get_line_points(INB_D)
nasal_outline4_points = get_line_points(nasal_outline4)
INB_E_points = get_line_points(INB_E)
nasal_outline5_points = get_line_points(nasal_outline5)
INB_F_points = get_line_points(INB_F)
nasal_outline6_points = get_line_points(nasal_outline6)
INB_A_points = get_line_points(INB_A)

# Find intersections
bone1 = find_intersection(nasal_outline1_points, INB_B_points)
bone2 = find_intersection(nasal_outline2_points, INB_C_points)
bone3 = find_intersection(nasal_outline3_points, INB_D_points)
bone4 = find_intersection(nasal_outline4_points, INB_E_points)
bone5 = find_intersection(nasal_outline5_points, INB_F_points)
bone6 = find_intersection(nasal_outline6_points, INB_A_points)

# Create new nodes
create_node("bone1", bone1)
create_node("bone2", bone2)
create_node("bone3", bone3)
create_node("bone4", bone4)
create_node("bone5", bone5)
create_node("bone6", bone6)
```

<img src="https://github.com/user-attachments/assets/b9cdbbe0-c6ed-4704-9460-84574975ca0c" width="500"]>

</details>

#### Optional adjusting codes
If you want to programmatically ensure the manually placed midline points points meet the INB_A, B etc lines

<details>

<summary>Adjust midline points on 4 planes</summary>

``` python
```
</details>

<details>

<summary>Adjust midline points on 5 planes</summary>

``` python
```
</details>

<details>

<summary>Adjust midline points on 6 planes</summary>

``` python
import slicer
import numpy as np

def is_point_on_line(line_points, point):
    p1, p2 = np.array(line_points[0]), np.array(line_points[1])
    point = np.array(point)
    line_vec = p2 - p1
    point_vec = point - p1
    cross_product = np.cross(line_vec, point_vec)
    return np.allclose(cross_product, 0)

def adjust_point_to_line(line_points, point):
    p1, p2 = np.array(line_points[0]), np.array(line_points[1])
    point = np.array(point)
    line_vec = p2 - p1
    line_vec_normalized = line_vec / np.linalg.norm(line_vec)
    point_vec = point - p1
    projection_length = np.dot(point_vec, line_vec_normalized)
    adjusted_point = p1 + projection_length * line_vec_normalized
    return adjusted_point.tolist()

# Get the line nodes from the scene
INB_B = slicer.util.getNode('INB_B')
INB_C = slicer.util.getNode('INB_C')
INB_D = slicer.util.getNode('INB_D')
INB_E = slicer.util.getNode('INB_E')
INB_F = slicer.util.getNode('INB_F')
INB_A = slicer.util.getNode('INB_A')

# Get the points of the lines
INB_B_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_C_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_D_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_E_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_F_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_A_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

for i in range(INB_B.GetNumberOfControlPoints()):
    INB_B.GetNthControlPointPosition(i, INB_B_points[i])

for i in range(INB_C.GetNumberOfControlPoints()):
    INB_C.GetNthControlPointPosition(i, INB_C_points[i])

for i in range(INB_D.GetNumberOfControlPoints()):
    INB_D.GetNthControlPointPosition(i, INB_D_points[i])

for i in range(INB_E.GetNumberOfControlPoints()):
    INB_E.GetNthControlPointPosition(i, INB_E_points[i])

for i in range(INB_F.GetNumberOfControlPoints()):
    INB_F.GetNthControlPointPosition(i, INB_F_points[i])

for i in range(INB_A.GetNumberOfControlPoints()):
    INB_A.GetNthControlPointPosition(i, INB_A_points[i])

# Get the bone nodes from the scene
bone1 = slicer.util.getNode('bone1')
bone2 = slicer.util.getNode('bone2')
bone3 = slicer.util.getNode('bone3')
bone4 = slicer.util.getNode('bone4')
bone5 = slicer.util.getNode('bone5')
bone6 = slicer.util.getNode('bone6')

# Get the points of the bones
bone1_point = [0.0, 0.0, 0.0]
bone2_point = [0.0, 0.0, 0.0]
bone3_point = [0.0, 0.0, 0.0]
bone4_point = [0.0, 0.0, 0.0]
bone5_point = [0.0, 0.0, 0.0]
bone6_point = [0.0, 0.0, 0.0]

bone1.GetNthControlPointPosition(0, bone1_point)
bone2.GetNthControlPointPosition(0, bone2_point)
bone3.GetNthControlPointPosition(0, bone3_point)
bone4.GetNthControlPointPosition(0, bone4_point)
bone5.GetNthControlPointPosition(0, bone5_point)
bone6.GetNthControlPointPosition(0, bone6_point)

# Get the nose profile outline node from the scene
nose_profile_outline6 = slicer.util.getNode('nose profile outline 6')

# Get the points of the nose profile outline
nose_profile_outline6_points = [[0.0, 0.0, 0.0] for _ in range(nose_profile_outline6.GetNumberOfControlPoints())]

for i in range(nose_profile_outline6.GetNumberOfControlPoints()):
    nose_profile_outline6.GetNthControlPointPosition(i, nose_profile_outline6_points[i])
import slicer
import numpy as np

def is_point_on_line(line_points, point):
    p1, p2 = np.array(line_points[0]), np.array(line_points[1])
    point = np.array(point)
    line_vec = p2 - p1
    point_vec = point - p1
    cross_product = np.cross(line_vec, point_vec)
    return np.allclose(cross_product, 0)

def adjust_point_to_line(line_points, point):
    p1, p2 = np.array(line_points[0]), np.array(line_points[1])
    point = np.array(point)
    line_vec = p2 - p1
    line_vec_normalized = line_vec / np.linalg.norm(line_vec)
    point_vec = point - p1
    projection_length = np.dot(point_vec, line_vec_normalized)
    adjusted_point = p1 + projection_length * line_vec_normalized
    return adjusted_point.tolist()

# Get the line nodes from the scene
INB_B = slicer.util.getNode('INB_B')
INB_C = slicer.util.getNode('INB_C')
INB_D = slicer.util.getNode('INB_D')
INB_E = slicer.util.getNode('INB_E')
INB_F = slicer.util.getNode('INB_F')
INB_A = slicer.util.getNode('INB_A')

# Get the points of the lines
INB_B_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_C_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_D_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_E_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_F_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
INB_A_points = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

for i in range(INB_B.GetNumberOfControlPoints()):
    INB_B.GetNthControlPointPosition(i, INB_B_points[i])

for i in range(INB_C.GetNumberOfControlPoints()):
    INB_C.GetNthControlPointPosition(i, INB_C_points[i])

for i in range(INB_D.GetNumberOfControlPoints()):
    INB_D.GetNthControlPointPosition(i, INB_D_points[i])

for i in range(INB_E.GetNumberOfControlPoints()):
    INB_E.GetNthControlPointPosition(i, INB_E_points[i])

for i in range(INB_F.GetNumberOfControlPoints()):
    INB_F.GetNthControlPointPosition(i, INB_F_points[i])

for i in range(INB_A.GetNumberOfControlPoints()):
    INB_A.GetNthControlPointPosition(i, INB_A_points[i])

# Get the bone nodes from the scene
bone1 = slicer.util.getNode('bone1')
bone2 = slicer.util.getNode('bone2')
bone3 = slicer.util.getNode('bone3')
bone4 = slicer.util.getNode('bone4')
bone5 = slicer.util.getNode('bone5')
bone6 = slicer.util.getNode('bone6')

# Get the points of the bones
bone1_point = [0.0, 0.0, 0.0]
bone2_point = [0.0, 0.0, 0.0]
bone3_point = [0.0, 0.0, 0.0]
bone4_point = [0.0, 0.0, 0.0]
bone5_point = [0.0, 0.0, 0.0]
bone6_point = [0.0, 0.0, 0.0]

bone1.GetNthControlPointPosition(0, bone1_point)
bone2.GetNthControlPointPosition(0, bone2_point)
bone3.GetNthControlPointPosition(0, bone3_point)
bone4.GetNthControlPointPosition(0, bone4_point)
bone5.GetNthControlPointPosition(0, bone5_point)
bone6.GetNthControlPointPosition(0, bone6_point)

# Get the nose profile outline node from the scene
nose_profile_outline6 = slicer.util.getNode('nose profile outline 6')

# Get the points of the nose profile outline
nose_profile_outline6_points = [[0.0, 0.0, 0.0] for _ in range(nose_profile_outline6.GetNumberOfControlPoints())]

for i in range(nose_profile_outline6.GetNumberOfControlPoints()):
    nose_profile_outline6.GetNthControlPointPosition(i, nose_profile_outline6_points[i])

# Check if points are on the lines and adjust if necessary
if not is_point_on_line(INB_B_points, bone1_point):
    bone1_adjusted = adjust_point_to_line(INB_B_points, bone1_point)
else:
    bone1_adjusted = bone1_point

if not is_point_on_line(INB_B_points, nose_profile_outline6_points[0]):
    nose_profile_outline6_point0_adjusted = adjust_point_to_line(INB_B_points, nose_profile_outline6_points[0])
else:
    nose_profile_outline6_point0_adjusted = nose_profile_outline6_points[0]

if not is_point_on_line(INB_C_points, bone2_point):
    bone2_adjusted = adjust_point_to_line(INB_C_points, bone2_point)
else:
    bone2_adjusted = bone2_point

if not is_point_on_line(INB_C_points, nose_profile_outline6_points[1]):
    nose_profile_outline6_point1_adjusted = adjust_point_to_line(INB_C_points, nose_profile_outline6_points[1])
else:
    nose_profile_outline6_point1_adjusted = nose_profile_outline6_points[1]

if not is_point_on_line(INB_D_points, bone3_point):
    bone3_adjusted = adjust_point_to_line(INB_D_points, bone3_point)
else:
    bone3_adjusted = bone3_point

if not is_point_on_line(INB_D_points, nose_profile_outline6_points[2]):
    nose_profile_outline6_point2_adjusted = adjust_point_to_line(INB_D_points, nose_profile_outline6_points[2])
else:
    nose_profile_outline6_point2_adjusted = nose_profile_outline6_points[2]

if not is_point_on_line(INB_E_points, bone4_point):
    bone4_adjusted = adjust_point_to_line(INB_E_points, bone4_point)
else:
    bone4_adjusted = bone4_point

if not is_point_on_line(INB_E_points, nose_profile_outline6_points[3]):
    nose_profile_outline6_point3_adjusted = adjust_point_to_line(INB_E_points, nose_profile_outline6_points[3])
else:
    nose_profile_outline6_point3_adjusted = nose_profile_outline6_points[3]

if not is_point_on_line(INB_F_points, bone5_point):
    bone5_adjusted = adjust_point_to_line(INB_F_points, bone5_point)
else:
    bone5_adjusted = bone5_point

if not is_point_on_line(INB_F_points, nose_profile_outline6_points[4]):
    nose_profile_outline6_point4_adjusted = adjust_point_to_line(INB_F_points, nose_profile_outline6_points[4])
else:
    nose_profile_outline6_point4_adjusted = nose_profile_outline6_points[4]

if not is_point_on_line(INB_A_points, bone6_point):
    bone6_adjusted = adjust_point_to_line(INB_A_points, bone6_point)
else:
    bone6_adjusted = bone6_point

if not is_point_on_line(INB_A_points, nose_profile_outline6_points[5]):
    nose_profile_outline6_point5_adjusted = adjust_point_to_line(INB_A_points, nose_profile_outline6_points[5])
else:
    nose_profile_outline6_point5_adjusted = nose_profile_outline6_points[5]

# Update the points with the adjusted positions
bone1.SetNthControlPointPosition(0, *bone1_adjusted)
nose_profile_outline6.SetNthControlPointPosition(0, *nose_profile_outline6_point0_adjusted)

bone2.SetNthControlPointPosition(0, *bone2_adjusted)
nose_profile_outline6.SetNthControlPointPosition(1, *nose_profile_outline6_point1_adjusted)

bone3.SetNthControlPointPosition(0, *bone3_adjusted)
nose_profile_outline6.SetNthControlPointPosition(2, *nose_profile_outline6_point2_adjusted)

bone4.SetNthControlPointPosition(0, *bone4_adjusted)
nose_profile_outline6.SetNthControlPointPosition(3, *nose_profile_outline6_point3_adjusted)

bone5.SetNthControlPointPosition(0, *bone5_adjusted)
nose_profile_outline6.SetNthControlPointPosition(4, *nose_profile_outline6_point4_adjusted)

bone6.SetNthControlPointPosition(0, *bone6_adjusted)
nose_profile_outline6.Set
```
</details>


#### Distances between Line A and nose profile & Line A and nasal aperture
 3. This step creates length measurements from the mirror point (Line B) to the a) nose profile (outside portion) coloured in orange and names them “noseprofiletoB1/2/3/4” etc; and b) to the nasal aperture in profile view  (inside portion) coloured lilac and names them “nasalbonetoB1/2/3/4” 


<details>

<summary>Code for 4-plane inside-outside mirror point</summary>

``` python
###  4 planes - inside-outside mirror point
import slicer

def create_linear_measurement(name, start_point, end_point, color):
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(end_point)
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

# Define colors
orange = [1.0, 0.5, 0.0]
lilac = [0.78, 0.64, 0.78]

# Get the nodes from the scene
mirrorB_A = slicer.util.getNode('mirrorB_A')
mirrorB_B = slicer.util.getNode('mirrorB_B')
mirrorB_C = slicer.util.getNode('mirrorB_C')
mirrorB_D = slicer.util.getNode('mirrorB_D')
nose_profile_outline4 = slicer.util.getNode('nose profile outline 4')
bone1 = slicer.util.getNode('bone1')
bone2 = slicer.util.getNode('bone2')
bone3 = slicer.util.getNode('bone3')
bone4 = slicer.util.getNode('bone4')

# Get the points from the nodes
nose_profile_outline4_points = []
for i in range(nose_profile_outline4.GetNumberOfControlPoints()):
    point = [0.0, 0.0, 0.0]
    nose_profile_outline4.GetNthControlPointPosition(i, point)
    nose_profile_outline4_points.append(point)

# Create linear measurements in orange
create_linear_measurement("noseprofiletoB1", mirrorB_B.GetNthControlPointPosition(0), nose_profile_outline4_points[0], orange)
create_linear_measurement("noseprofiletoB2", mirrorB_C.GetNthControlPointPosition(0), nose_profile_outline4_points[1], orange)
create_linear_measurement("noseprofiletoB3", mirrorB_D.GetNthControlPointPosition(0), nose_profile_outline4_points[2], orange)
create_linear_measurement("noseprofiletoB4", mirrorB_A.GetNthControlPointPosition(0), nose_profile_outline4_points[3], orange)

# Create linear measurements in lilac
create_linear_measurement("nasalbonetoB1", mirrorB_B.GetNthControlPointPosition(0), bone1.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB2", mirrorB_C.GetNthControlPointPosition(0), bone2.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB3", mirrorB_D.GetNthControlPointPosition(0), bone3.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB4", mirrorB_A.GetNthControlPointPosition(0), bone4.GetNthControlPointPosition(0), lilac)

```
![image](https://github.com/user-attachments/assets/65e998fb-4b37-42d6-82a2-7d67b4634df5)

<img src="https://github.com/user-attachments/assets/65e998fb-4b37-42d6-82a2-7d67b4634df5" width="500">

</details>

<details>

<summary>Code for 5-plane inside-outside mirror point</summary>

``` python
###   5 planes - inside-outside mirror point
import slicer

def create_linear_measurement(name, start_point, end_point, color):
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(end_point)
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

# Define colors
orange = [1.0, 0.5, 0.0]
lilac = [0.78, 0.64, 0.78]

# Get the nodes from the scene
mirrorB_A = slicer.util.getNode('mirrorB_A')
mirrorB_B = slicer.util.getNode('mirrorB_B')
mirrorB_C = slicer.util.getNode('mirrorB_C')
mirrorB_D = slicer.util.getNode('mirrorB_D')
mirrorB_E = slicer.util.getNode('mirrorB_E')
nose_profile_outline5 = slicer.util.getNode('nose profile outline 5')
bone1 = slicer.util.getNode('bone1')
bone2 = slicer.util.getNode('bone2')
bone3 = slicer.util.getNode('bone3')
bone4 = slicer.util.getNode('bone4')
bone5 = slicer.util.getNode('bone5')

# Get the points from the nodes
nose_profile_outline5_points = []
for i in range(nose_profile_outline5.GetNumberOfControlPoints()):
    point = [0.0, 0.0, 0.0]
    nose_profile_outline5.GetNthControlPointPosition(i, point)
    nose_profile_outline5_points.append(point)

nose_profile_outline5_points = []
for i in range(nose_profile_outline5.GetNumberOfControlPoints()):
    point = [0.0, 0.0, 0.0]
    nose_profile_outline5.GetNthControlPointPosition(i, point)
    nose_profile_outline5_points.append(point)

# Create linear measurements in orange
create_linear_measurement("noseprofiletoB1", mirrorB_B.GetNthControlPointPosition(0), nose_profile_outline5_points[0], orange)
create_linear_measurement("noseprofiletoB2", mirrorB_C.GetNthControlPointPosition(0), nose_profile_outline5_points[1], orange)
create_linear_measurement("noseprofiletoB3", mirrorB_D.GetNthControlPointPosition(0), nose_profile_outline5_points[2], orange)
create_linear_measurement("noseprofiletoB4", mirrorB_E.GetNthControlPointPosition(0), nose_profile_outline5_points[3], orange)
create_linear_measurement("noseprofiletoB5", mirrorB_A.GetNthControlPointPosition(0), nose_profile_outline5_points[4], orange)

# Create linear measurements in lilac
create_linear_measurement("nasalbonetoB1", mirrorB_B.GetNthControlPointPosition(0), bone1.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB2", mirrorB_C.GetNthControlPointPosition(0), bone2.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB3", mirrorB_D.GetNthControlPointPosition(0), bone3.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB4", mirrorB_E.GetNthControlPointPosition(0), bone4.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB5", mirrorB_A.GetNthControlPointPosition(0), bone5.GetNthControlPointPosition(0), lilac)

```


<img src="https://github.com/user-attachments/assets/ae87c073-2b4d-45e5-82cd-149c02cfdf86" width="500">

</details>

<details>

<summary>Code for 6-plane inside-outside mirror point</summary>

``` python
###    6 planes - inside-outside mirror point
import slicer

def create_linear_measurement(name, start_point, end_point, color):
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(end_point)
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

# Define colors
orange = [1.0, 0.5, 0.0]
lilac = [0.78, 0.64, 0.78]

# Get the nodes from the scene
mirrorB_A = slicer.util.getNode('mirrorB_A')
mirrorB_B = slicer.util.getNode('mirrorB_B')
mirrorB_C = slicer.util.getNode('mirrorB_C')
mirrorB_D = slicer.util.getNode('mirrorB_D')
mirrorB_E = slicer.util.getNode('mirrorB_E')
mirrorB_F = slicer.util.getNode('mirrorB_F')
nose_profile_outline6 = slicer.util.getNode('nose profile outline 6')
bone1 = slicer.util.getNode('bone1')
bone2 = slicer.util.getNode('bone2')
bone3 = slicer.util.getNode('bone3')
bone4 = slicer.util.getNode('bone4')
bone5 = slicer.util.getNode('bone5')
bone6 = slicer.util.getNode('bone6')

# Get the points from the nodes
nose_profile_outline6_points = []
for i in range(nose_profile_outline6.GetNumberOfControlPoints()):
    point = [0.0, 0.0, 0.0]
    nose_profile_outline6.GetNthControlPointPosition(i, point)
    nose_profile_outline6_points.append(point)

# Create linear measurements in orange
create_linear_measurement("noseprofiletoB1", mirrorB_B.GetNthControlPointPosition(0), nose_profile_outline6_points[0], orange)
create_linear_measurement("noseprofiletoB2", mirrorB_C.GetNthControlPointPosition(0), nose_profile_outline6_points[1], orange)
create_linear_measurement("noseprofiletoB3", mirrorB_D.GetNthControlPointPosition(0), nose_profile_outline6_points[2], orange)
create_linear_measurement("noseprofiletoB4", mirrorB_E.GetNthControlPointPosition(0), nose_profile_outline6_points[3], orange)
create_linear_measurement("noseprofiletoB5", mirrorB_F.GetNthControlPointPosition(0), nose_profile_outline6_points[4], orange)
create_linear_measurement("noseprofiletoB6", mirrorB_A.GetNthControlPointPosition(0), nose_profile_outline6_points[5], orange)

# Create linear measurements in lilac
create_linear_measurement("nasalbonetoB1", mirrorB_B.GetNthControlPointPosition(0), bone1.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB2", mirrorB_C.GetNthControlPointPosition(0), bone2.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB3", mirrorB_D.GetNthControlPointPosition(0), bone3.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB4", mirrorB_E.GetNthControlPointPosition(0), bone4.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB5", mirrorB_F.GetNthControlPointPosition(0), bone5.GetNthControlPointPosition(0), lilac)
create_linear_measurement("nasalbonetoB6", mirrorB_A.GetNthControlPointPosition(0), bone6.GetNthControlPointPosition(0), lilac)
```

<img src="https://github.com/user-attachments/assets/d64193b0-5db8-4416-94ae-c8e731a9772f" width="500"]>

</details>


### Output
To copy all the linear measurements to clipboard, use the method described in [this guide](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/004_Copying%20measurements%20to%20Clipboard.md). 
To make sense of the output, keep in mind that the guideline method allows for testing whether Line A and B are true mirror planes (ascertain whether the inside and outside is significantly different) and test its predictive ability with or without soft tissue measurements (facial soft tissue thickness) of your choice to add on for the “noseprofiletoB1/2/3/4” measurements anteriorly (be careful about pairing landmarks! - the original paper simply states "(a little more than 2 mm) was added").  Optionally, you can see if the 4/5 or 6 plane methods predict nasal shape better. 

<details>

<summary>Output for 4 planes with optional Line A measurements</summary>

| Unknown             | Parameter               | Value                   |
|---------------------|-------------------------|-------------------------|
| (unknown)           | maximum nasal width MAW | 34.065879845058085      |
| (unknown)           | INB_A                   | 2000.0                  |
| (unknown)           | INB_B                   | 2000.0000000000002      |
| (unknown)           | INB_C                   | 2000.0000000000005      |
| (unknown)           | INB_D                   | 2000.0000000000005      |
| (unknown)           | Line_A                  | 62.419688580150364      |
| (unknown)           | Line_B                  | 124.83937716030069      |
| (unknown)           | nasal outline1          | 24.366736158161636      |
| (unknown)           | nasal outline2          | 26.81613067797216       |
| (unknown)           | nasal outline3          | 27.80868537156018       |
| (unknown)           | nasal outline4          | 17.38024525644104       |
| (unknown)           | noseprofiletoB1         | 5.525673779566004       |
| (unknown)           | noseprofiletoB2         | 9.902626067446901       |
| (unknown)           | noseprofiletoB3         | 16.137793993929815      |
| (unknown)           | noseprofiletoB4         | 17.09598625672042       |
| (unknown)           | nasalbonetoB1           | 15.780117253842183      |
| (unknown)           | nasalbonetoB2           | 16.49542889900834       |
| (unknown)           | nasalbonetoB3           | 20.14246273809071       |
| (unknown)           | nasalbonetoB4           | 17.749331272230933      |


</details>

<details>

<summary>Output for 5 planes with optional Line A measurements</summary>

| Unknown   | Parameter               | Value                   |
|-----------|-------------------------|-------------------------|
| (unknown) | maximum nasal width MAW | 34.065879845058085      |
| (unknown) | INB_A                   | 2000.0                  |
| (unknown) | INB_B                   | 2000.0000000000002      |
| (unknown) | INB_C                   | 2000.0000000000005      |
| (unknown) | INB_D                   | 2000.0000000000005      |
| (unknown) | INB_E                   | 2000.0                  |
| (unknown) | Line_A                  | 62.419688580150364      |
| (unknown) | Line_B                  | 124.83937716030074      |
| (unknown) | nasal outline1          | 23.09624385966932       |
| (unknown) | nasal outline2          | 24.00250437441322       |
| (unknown) | nasal outline3          | 26.580511864794236      |
| (unknown) | nasal outline4          | 26.84200917751933       |
| (unknown) | nasal outline5          | 18.885324552925304      |
| (unknown) | noseprofiletoB1         | 4.77413457704267        |
| (unknown) | noseprofiletoB2         | 7.7728775719345204      |
| (unknown) | noseprofiletoB3         | 12.299803347006584      |
| (unknown) | noseprofiletoB4         | 16.577556239891496      |
| (unknown) | noseprofiletoB5         | 16.893884167296918      |
| (unknown) | nasalbonetoB1           | 15.669179694093904      |
| (unknown) | nasalbonetoB2           | 14.209577753877143      |
| (unknown) | nasalbonetoB3           | 17.574859858633058      |
| (unknown) | nasalbonetoB4           | 20.19372441866758       |
| (unknown) | nasalbonetoB5           | 18.50970755626509       |

</details>

<details>

<summary>Output for 6 planes with optional Line A measurements</summary>

| Unknown   | Parameter               | Value                   |
|-----------|-------------------------|-------------------------|
| (unknown) | maximum nasal width MAW | 34.065879845058085      |
| (unknown) | INB_A                   | 2000.0                  |
| (unknown) | INB_B                   | 2000.0000000000002      |
| (unknown) | INB_C                   | 2000.0000000000002      |
| (unknown) | INB_D                   | 2000.0000000000005      |
| (unknown) | INB_E                   | 2000.0000000000002      |
| (unknown) | INB_F                   | 2000.0                  |
| (unknown) | Line_A                  | 62.419688580150364      |
| (unknown) | Line_B                  | 124.83937716030076      |
| (unknown) | nasal outline1          | 22.560548604784675      |
| (unknown) | nasal outline2          | 24.27440147938001       |
| (unknown) | nasal outline3          | 26.689979253823722      |
| (unknown) | nasal outline4          | 24.491972756379866      |
| (unknown) | nasal outline5          | 26.589433476120288      |
| (unknown) | nasal outline6          | 21.438268607642662      |
| (unknown) | noseprofiletoB1         | 4.3806753382390555      |
| (unknown) | noseprofiletoB2         | 6.863999026673066       |
| (unknown) | noseprofiletoB3         | 10.403738313217593      |
| (unknown) | noseprofiletoB4         | 14.525122003267612      |
| (unknown) | noseprofiletoB5         | 17.048739616886586      |
| (unknown) | noseprofiletoB6         | 16.869754556328157      |
| (unknown) | nasalbonetoB1           | 15.844204074180183      |
| (unknown) | nasalbonetoB2           | 14.607928382721507      |
| (unknown) | nasalbonetoB3           | 16.55600629779354       |
| (unknown) | nasalbonetoB4           | 17.59277552761434       |
| (unknown) | nasalbonetoB5           | 20.59955288417588       |
| (unknown) | nasalbonetoB6           | 19.449551948971035      |

</details>

> [!IMPORTANT]
> INB_A, INB_B, INB_C, INB_D, INB_E, INB_F and Line_A, Line_B are NOT true measurements. They provide guide (Line_A and Line_B); or are programmed to be elongated to 20 cm (INB_A, etc) - DO NOT use them as measurements in your data analysis! Exercise caution with the "nasal outline1..." measurements as these are specific to the bony nose outlet and there are no comparable measurements for the soft nose. 

### Extra codes for more ideas

> [!IMPORTANT]
>Run these BEFORE you copy all linear measurements to clipboard if you want to implement them. Ignore the "pred soft nose outline1" 2 etc numbers - they should be identical to the nasalbonetoB1,2etc measurements. 

If the mirror plane idea has peaked your interest, there is a way to measure the difference (prediction error) between the actual nasal outline points and the predicted nasal outline points (assuming _Line_ B to be the mirror plane and the _nasalbonetoB1,2,3,4,5,6_ the distances between the mirror and the bony outline) which in this case we will define as starting from their respective mirror points and of the same length as their respective _nasalbonetoB1,2,3,4,5,6; creating a predicted soft tissue outline named "pred soft nose outline1" in deep purple and a burgundy line connecting the anterior endpoints of the lines **noseprofiletoB1**,2, etc and **pred soft nose outline2**etc named "pred error1,2etc"

<details>

<summary>Extra error code for 4-plane </summary>

```python
#EXTRA predictor, 4 plane forced mirror and true soft nose outline comparison#####

import slicer
import numpy as np

def get_line_points(line_node):
    points = []
    for i in range(line_node.GetNumberOfControlPoints()):
        point = [0.0, 0.0, 0.0]
        line_node.GetNthControlPointPosition(i, point)
        points.append(point)
    return points

def calculate_length(start_point, end_point):
    return np.linalg.norm(np.array(end_point) - np.array(start_point))

def create_parallel_line(name, start_point, length, reference_line_points, color):
    direction = np.array(reference_line_points[1]) - np.array(reference_line_points[0])
    unit_direction = direction / np.linalg.norm(direction)
    new_end_point = np.array(start_point) + unit_direction * length
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(new_end_point.tolist())
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

def create_distance_measurement(name, start_point, end_point, color):
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(end_point)
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

# Define colors
deep_purple = [0.29, 0.0, 0.51]
burgundy = [0.5, 0.0, 0.13]

# Get the nodes from the scene
mirrorB_A = slicer.util.getNode('mirrorB_A')
mirrorB_B = slicer.util.getNode('mirrorB_B')
mirrorB_C = slicer.util.getNode('mirrorB_C')
mirrorB_D = slicer.util.getNode('mirrorB_D')

noseprofiletoB1 = slicer.util.getNode('noseprofiletoB1')
noseprofiletoB2 = slicer.util.getNode('noseprofiletoB2')
noseprofiletoB3 = slicer.util.getNode('noseprofiletoB3')
noseprofiletoB4 = slicer.util.getNode('noseprofiletoB4')

nasalbonetoB1 = slicer.util.getNode('nasalbonetoB1')
nasalbonetoB2 = slicer.util.getNode('nasalbonetoB2')
nasalbonetoB3 = slicer.util.getNode('nasalbonetoB3')
nasalbonetoB4 = slicer.util.getNode('nasalbonetoB4')

INB_A = slicer.util.getNode('INB_A')
INB_B = slicer.util.getNode('INB_B')
INB_C = slicer.util.getNode('INB_C')
INB_D = slicer.util.getNode('INB_D')

# Get the points of the reference lines
INB_A_points = get_line_points(INB_A)
INB_B_points = get_line_points(INB_B)
INB_C_points = get_line_points(INB_C)
INB_D_points = get_line_points(INB_D)

# Calculate lengths of nasalbonetoB lines
length1 = calculate_length(nasalbonetoB1.GetNthControlPointPosition(0), nasalbonetoB1.GetNthControlPointPosition(1))
length2 = calculate_length(nasalbonetoB2.GetNthControlPointPosition(0), nasalbonetoB2.GetNthControlPointPosition(1))
length3 = calculate_length(nasalbonetoB3.GetNthControlPointPosition(0), nasalbonetoB3.GetNthControlPointPosition(1))
length4 = calculate_length(nasalbonetoB4.GetNthControlPointPosition(0), nasalbonetoB4.GetNthControlPointPosition(1))

# Create new lines with parallel vectors and specified lengths
create_parallel_line("pred soft nose outline1", mirrorB_A.GetNthControlPointPosition(0), length1, INB_A_points, deep_purple)
create_parallel_line("pred soft nose outline2", mirrorB_B.GetNthControlPointPosition(0), length2, INB_B_points, deep_purple)
create_parallel_line("pred soft nose outline3", mirrorB_C.GetNthControlPointPosition(0), length3, INB_C_points, deep_purple)
create_parallel_line("pred soft nose outline4", mirrorB_D.GetNthControlPointPosition(0), length4, INB_D_points, deep_purple)

# Get the new lines from the scene
pred_soft_nose_outline1 = slicer.util.getNode('pred soft nose outline1')
pred_soft_nose_outline2 = slicer.util.getNode('pred soft nose outline2')
pred_soft_nose_outline3 = slicer.util.getNode('pred soft nose outline3')
pred_soft_nose_outline4 = slicer.util.getNode('pred soft nose outline4')

# Create distance measurements in burgundy
create_distance_measurement("pred error1", noseprofiletoB1.GetNthControlPointPosition(1), pred_soft_nose_outline2.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error2", noseprofiletoB2.GetNthControlPointPosition(1), pred_soft_nose_outline3.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error3", noseprofiletoB3.GetNthControlPointPosition(1), pred_soft_nose_outline4.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error4", noseprofiletoB4.GetNthControlPointPosition(1), pred_soft_nose_outline1.GetNthControlPointPosition(1), burgundy)
```

</details>


<details>

<summary>Extra error code for 5-plane </summary>

``` python
#EXTRA predictor, 5 plane forced mirror and true soft nose outline comparison#####
import slicer
import numpy as np

def get_line_points(line_node):
    points = []
    for i in range(line_node.GetNumberOfControlPoints()):
        point = [0.0, 0.0, 0.0]
        line_node.GetNthControlPointPosition(i, point)
        points.append(point)
    return points

def calculate_length(start_point, end_point):
    return np.linalg.norm(np.array(end_point) - np.array(start_point))

def create_parallel_line(name, start_point, length, reference_line_points, color):
    direction = np.array(reference_line_points[1]) - np.array(reference_line_points[0])
    unit_direction = direction / np.linalg.norm(direction)
    new_end_point = np.array(start_point) + unit_direction * length
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(new_end_point.tolist())
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

def create_distance_measurement(name, start_point, end_point, color):
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(end_point)
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

# Define colors
deep_purple = [0.29, 0.0, 0.51]
burgundy = [0.5, 0.0, 0.13]

# Get the nodes from the scene
mirrorB_A = slicer.util.getNode('mirrorB_A')
mirrorB_B = slicer.util.getNode('mirrorB_B')
mirrorB_C = slicer.util.getNode('mirrorB_C')
mirrorB_D = slicer.util.getNode('mirrorB_D')
mirrorB_E = slicer.util.getNode('mirrorB_E')

noseprofiletoB1 = slicer.util.getNode('noseprofiletoB1')
noseprofiletoB2 = slicer.util.getNode('noseprofiletoB2')
noseprofiletoB3 = slicer.util.getNode('noseprofiletoB3')
noseprofiletoB4 = slicer.util.getNode('noseprofiletoB4')
noseprofiletoB5 = slicer.util.getNode('noseprofiletoB5')

nasalbonetoB1 = slicer.util.getNode('nasalbonetoB1')
nasalbonetoB2 = slicer.util.getNode('nasalbonetoB2')
nasalbonetoB3 = slicer.util.getNode('nasalbonetoB3')
nasalbonetoB4 = slicer.util.getNode('nasalbonetoB4')
nasalbonetoB5 = slicer.util.getNode('nasalbonetoB5')

INB_A = slicer.util.getNode('INB_A')
INB_B = slicer.util.getNode('INB_B')
INB_C = slicer.util.getNode('INB_C')
INB_D = slicer.util.getNode('INB_D')
INB_E = slicer.util.getNode('INB_E')

# Get the points of the reference lines
INB_A_points = get_line_points(INB_A)
INB_B_points = get_line_points(INB_B)
INB_C_points = get_line_points(INB_C)
INB_D_points = get_line_points(INB_D)
INB_E_points = get_line_points(INB_E)

# Calculate lengths of nasalbonetoB lines
length1 = calculate_length(nasalbonetoB1.GetNthControlPointPosition(0), nasalbonetoB1.GetNthControlPointPosition(1))
length2 = calculate_length(nasalbonetoB2.GetNthControlPointPosition(0), nasalbonetoB2.GetNthControlPointPosition(1))
length3 = calculate_length(nasalbonetoB3.GetNthControlPointPosition(0), nasalbonetoB3.GetNthControlPointPosition(1))
length4 = calculate_length(nasalbonetoB4.GetNthControlPointPosition(0), nasalbonetoB4.GetNthControlPointPosition(1))
length5 = calculate_length(nasalbonetoB5.GetNthControlPointPosition(0), nasalbonetoB5.GetNthControlPointPosition(1))

# Create new lines with parallel vectors and specified lengths
create_parallel_line("pred soft nose outline1", mirrorB_A.GetNthControlPointPosition(0), length1, INB_A_points, deep_purple)
create_parallel_line("pred soft nose outline2", mirrorB_B.GetNthControlPointPosition(0), length2, INB_B_points, deep_purple)
create_parallel_line("pred soft nose outline3", mirrorB_C.GetNthControlPointPosition(0), length3, INB_C_points, deep_purple)
create_parallel_line("pred soft nose outline4", mirrorB_D.GetNthControlPointPosition(0), length4, INB_D_points, deep_purple)
create_parallel_line("pred soft nose outline5", mirrorB_E.GetNthControlPointPosition(0), length5, INB_E_points, deep_purple)

# Get the new lines from the scene
pred_soft_nose_outline1 = slicer.util.getNode('pred soft nose outline1')
pred_soft_nose_outline2 = slicer.util.getNode('pred soft nose outline2')
pred_soft_nose_outline3 = slicer.util.getNode('pred soft nose outline3')
pred_soft_nose_outline4 = slicer.util.getNode('pred soft nose outline4')
pred_soft_nose_outline5 = slicer.util.getNode('pred soft nose outline5')

# Create distance measurements in burgundy
create_distance_measurement("pred error1", noseprofiletoB1.GetNthControlPointPosition(1), pred_soft_nose_outline2.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error2", noseprofiletoB2.GetNthControlPointPosition(1), pred_soft_nose_outline3.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error3", noseprofiletoB3.GetNthControlPointPosition(1), pred_soft_nose_outline4.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error4", noseprofiletoB4.GetNthControlPointPosition(1), pred_soft_nose_outline5.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error5", noseprofiletoB5.GetNthControlPointPosition(1), pred_soft_nose_outline1.GetNthControlPointPosition(1), burgundy)

```

</details>



<details>

<summary>Extra error code for 6-plane </summary>

``` python
import slicer
import numpy as np

def get_line_points(line_node):
    points = []
    for i in range(line_node.GetNumberOfControlPoints()):
        point = [0.0, 0.0, 0.0]
        line_node.GetNthControlPointPosition(i, point)
        points.append(point)
    return points

def calculate_length(start_point, end_point):
    return np.linalg.norm(np.array(end_point) - np.array(start_point))

def create_parallel_line(name, start_point, length, reference_line_points, color):
    direction = np.array(reference_line_points[1]) - np.array(reference_line_points[0])
    unit_direction = direction / np.linalg.norm(direction)
    new_end_point = np.array(start_point) + unit_direction * length
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(new_end_point.tolist())
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

def create_distance_measurement(name, start_point, end_point, color):
    line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
    line_node.AddControlPoint(start_point)
    line_node.AddControlPoint(end_point)
    display_node = line_node.GetDisplayNode()
    display_node.SetSelectedColor(color)
    display_node.SetColor(color)

# Define colors
deep_purple = [0.29, 0.0, 0.51]
burgundy = [0.5, 0.0, 0.13]

# Get the nodes from the scene
mirrorB_A = slicer.util.getNode('mirrorB_A')
mirrorB_B = slicer.util.getNode('mirrorB_B')
mirrorB_C = slicer.util.getNode('mirrorB_C')
mirrorB_D = slicer.util.getNode('mirrorB_D')
mirrorB_E = slicer.util.getNode('mirrorB_E')
mirrorB_F = slicer.util.getNode('mirrorB_F')

noseprofiletoB1 = slicer.util.getNode('noseprofiletoB1')
noseprofiletoB2 = slicer.util.getNode('noseprofiletoB2')
noseprofiletoB3 = slicer.util.getNode('noseprofiletoB3')
noseprofiletoB4 = slicer.util.getNode('noseprofiletoB4')
noseprofiletoB5 = slicer.util.getNode('noseprofiletoB5')
noseprofiletoB6 = slicer.util.getNode('noseprofiletoB6')

nasalbonetoB1 = slicer.util.getNode('nasalbonetoB1')
nasalbonetoB2 = slicer.util.getNode('nasalbonetoB2')
nasalbonetoB3 = slicer.util.getNode('nasalbonetoB3')
nasalbonetoB4 = slicer.util.getNode('nasalbonetoB4')
nasalbonetoB5 = slicer.util.getNode('nasalbonetoB5')
nasalbonetoB6 = slicer.util.getNode('nasalbonetoB6')

INB_A = slicer.util.getNode('INB_A')
INB_B = slicer.util.getNode('INB_B')
INB_C = slicer.util.getNode('INB_C')
INB_D = slicer.util.getNode('INB_D')
INB_E = slicer.util.getNode('INB_E')
INB_F = slicer.util.getNode('INB_F')

# Get the points of the reference lines
INB_A_points = get_line_points(INB_A)
INB_B_points = get_line_points(INB_B)
INB_C_points = get_line_points(INB_C)
INB_D_points = get_line_points(INB_D)
INB_E_points = get_line_points(INB_E)
INB_F_points = get_line_points(INB_F)

# Calculate lengths of nasalbonetoB lines
length1 = calculate_length(nasalbonetoB1.GetNthControlPointPosition(0), nasalbonetoB1.GetNthControlPointPosition(1))
length2 = calculate_length(nasalbonetoB2.GetNthControlPointPosition(0), nasalbonetoB2.GetNthControlPointPosition(1))
length3 = calculate_length(nasalbonetoB3.GetNthControlPointPosition(0), nasalbonetoB3.GetNthControlPointPosition(1))
length4 = calculate_length(nasalbonetoB4.GetNthControlPointPosition(0), nasalbonetoB4.GetNthControlPointPosition(1))
length5 = calculate_length(nasalbonetoB5.GetNthControlPointPosition(0), nasalbonetoB5.GetNthControlPointPosition(1))
length6 = calculate_length(nasalbonetoB6.GetNthControlPointPosition(0), nasalbonetoB6.GetNthControlPointPosition(1))

# Create new lines with parallel vectors and specified lengths
create_parallel_line("pred soft nose outline1", mirrorB_A.GetNthControlPointPosition(0), length1, INB_A_points, deep_purple)
create_parallel_line("pred soft nose outline2", mirrorB_B.GetNthControlPointPosition(0), length2, INB_B_points, deep_purple)
create_parallel_line("pred soft nose outline3", mirrorB_C.GetNthControlPointPosition(0), length3, INB_C_points, deep_purple)
create_parallel_line("pred soft nose outline4", mirrorB_D.GetNthControlPointPosition(0), length4, INB_D_points, deep_purple)
create_parallel_line("pred soft nose outline5", mirrorB_E.GetNthControlPointPosition(0), length5, INB_E_points, deep_purple)
create_parallel_line("pred soft nose outline6", mirrorB_F.GetNthControlPointPosition(0), length6, INB_F_points, deep_purple)

# Get the new lines from the scene
pred_soft_nose_outline1 = slicer.util.getNode('pred soft nose outline1')
pred_soft_nose_outline2 = slicer.util.getNode('pred soft nose outline2')
pred_soft_nose_outline3 = slicer.util.getNode('pred soft nose outline3')
pred_soft_nose_outline4 = slicer.util.getNode('pred soft nose outline4')
pred_soft_nose_outline5 = slicer.util.getNode('pred soft nose outline5')
pred_soft_nose_outline6 = slicer.util.getNode('pred soft nose outline6')

# Create distance measurements in burgundy
create_distance_measurement("pred error1", noseprofiletoB1.GetNthControlPointPosition(1), pred_soft_nose_outline2.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error2", noseprofiletoB2.GetNthControlPointPosition(1), pred_soft_nose_outline3.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error3", noseprofiletoB3.GetNthControlPointPosition(1), pred_soft_nose_outline4.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error4", noseprofiletoB4.GetNthControlPointPosition(1), pred_soft_nose_outline5.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error5", noseprofiletoB5.GetNthControlPointPosition(1), pred_soft_nose_outline6.GetNthControlPointPosition(1), burgundy)
create_distance_measurement("pred error6", noseprofiletoB6.GetNthControlPointPosition(1), pred_soft_nose_outline1.GetNthControlPointPosition(1), burgundy)
```

</details>




## Bibliography

[^1]: [Slicer Script Repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
[^2]: (https://archives.fbi.gov/archives/about-us/lab/forensic-science-communications/fsc/jan2002/prokopec.htm)
[^3]: Rynn, C., Wilkinson, C.M. & Peters, H.L. (2010) "Prediction of nasal morphology from the skull." Forensic Sci Med Pathol 6, 20–34. https://doi.org/10.1007/s12024-009-9124-6
[^4]: Rynn, C. and C. M. Wilkinson (2006). "Appraisal of traditional and recently proposed relationships between the hard and soft dimensions of the nose in profile." American Journal of Physical Anthropology: The Official Publication of the American Association of Physical Anthropologists 130(3): 364-373.
[^5]: Rynn, C., et al. (2012). Relationships between the skull and face. Craniofacial identification. C. W. C. Rynn. Cambridge, Cambridge University Press: 193-202.
[^6]: Caple, J. and C. N. Stephan (2016). "A standardized nomenclature for craniofacial and facial anthropometry." Int J Legal Med 130(3): 863-879.
