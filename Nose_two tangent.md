# The Two Tangent Method by Gerasimow, 1955


Limitations occur in describing this method in detail as his works are available in English only partially, these are (i) the published translations from German (Gerassimow, 1968; Gerasimov, 1971) and the (ii) unpublished Tshernezky translation later used for the development of the Manchester protocol (Wilkinson, 2004; Stephan and Ullrich, 2011; Stephan and Ullrich, 2015). 

The method followed here is the one described by Gatliff (1984), as the interpretation by Stephan (2003) was later scrutinised by Rynn and Wilkinson (2006) and Rynn et al. (2012). 

The summarised theory is that the tip of the soft nose (pronasale) can be predicted by where two tangents meet: (a) the tangent running between the nasion to rhinion OR the line following the bony nose shape in profile view and (b) the tangent aligning with the anterior 1/3rd of the nasal spine OR following its direction as an arrow.

To achieve this, we will 

1. [Establish an INB plane (Rynn et al. 2012) as the cut plane to establish a standard profile view](#inb-plane)
2. [Make a profile view](#profile-view-model) along the INB plane by cutting the Bone model
3. [Draw or code the two tangents](#establishing-the-tangents) and programmatically ensure they are aligned in the INB plane
4. [Elongate the aligned tangents](#elongating-the-tangents) to find their meeting point - the soft nose tip _pronasale_
5. Optionally, connect the predicted nose tip and the actual nose tip for [error rate](#error-rate) (you can also compare the coordinates instead)

Landmarks in this guide: 
| Position in code | Position in file | Name in file | Landmark name | Definition                                                                                                                     | Defined by            |
|------------------|------------------|--------------|---------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| 0                | 1                | nasion       | nasion        | Intersection of the nasofrontal sutures in the median plane                                                                    | Rynn et al. 2010      |
| 1                | 2                | inion        | inion         | Median point between the apices of the superior nuchal lines and at the base of the external occipital protuberance (not the tip of the protuberance) | Rynn et al. 2010      |
| 2                | 3                | bregma       | bregma        | Where the sagittal and coronal sutures meet. Impossible to determine in juvenile skulls with anterior fontanelle, or with complete suture obliteration | Rynn et al. 2010      |
| 3                | 4                | rhinion      | rhinion       | Most rostral (end) point on the internasal suture.                                                                            | Rynn et al. 2010      |
| 4                | 5                | acanthion    | acanthion     | Most anterior tip of the anterior nasal spine                                                                                 | Rynn et al. 2010      |
| 5                | 6                | pronasale    | pronasale     | The most anteriorly protruded point of the apex nasi. In the case of a bifid nose, the more protruding tip is chosen           | Caple and Stephan 2016|

[Gerasimow landmarks.mrk.json](https://github.com/user-attachments/files/19151390/Gerasimow.landmarks.mrk.json)

Illustration of the method: 

> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

[ ] The scan has to be re-aligned in the FHP
[ ] You should have a Bone and Skin model via segmentation (explained later)



### INB plane

To help with the side profile, we will establish the “INB” plane as defined by Rynn et al. 2010. 

> a midsagittal plane (INB) which bisected the inion, nasion and bregma

by downloading markups file for this method: 
[Gerasimow landmarks.mrk.json](https://github.com/user-attachments/files/19151283/Gerasimow.landmarks.mrk.json), allocating the first three landmarks (nasion, inion, bregma) and copying and pasting the following code: 

```python
#INB plane#

import numpy as np
import slicer

# Get the points from the "hard tissue" node
hardTissueNode = slicer.util.getNode('Gerasimow landmarks')
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

![NIB lmrks allocated](https://github.com/user-attachments/assets/584631f2-598e-4cdf-8f09-ef4f7bc798ff)
View after only the first 3 landmarks are allocated correctly
![INB as is](https://github.com/user-attachments/assets/50f064e9-2267-4135-90b3-3518bf718fe9)
The generated INB plane view

![enlraged plane](https://github.com/user-attachments/assets/77feb12a-cc3b-438d-9f53-5a4193aed721)
INB extended via the toggles (dots)

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

> [!IMPORTANT]
> On the example screenshots, the "full model" is named "Skin-cropped" and "Bone-cropped" - this is because the example Brain CT still had the headrest in the segmentation as an artefact, so I removed that

Make sure you create your cut model with the settings on the screenshot to cut the Bone model at the INB Plane: 

[ ] - Make sure the source volume is the full model of the Bone
[ ] - Choose INB as the plane node
[ ] - Operation type should be **Intersection**
[ ] - You MUST chose the **Create new model as...** from the drop-down menu and type in the custom name with the **bone** prefix - otherwise you'll override your existing models
[ ] - DO NOT FORGET TO CLICK APPLY

    ![image](https://github.com/user-attachments/assets/e4fc0f15-acfe-41d4-854c-354188e4f7b0)

[ ] - Check if this was executed by finding your 2 new models under the "Models" module
With these settings, the Model list will be the following: 
    ![image](https://github.com/user-attachments/assets/2e2fcaab-2716-49e4-a3e7-c34bc4df30bd)


And you should have the following individual views (excluding/hiding the original full models for demonstration purposes):
![cropped cranium](https://github.com/user-attachments/assets/4de15a97-9b76-4fb7-94b1-294d7eaaab35)

You can now allocate the remainder of the landmarks on either model - they should appear on ALL of them. 


### Establishing the tangents
Re-orient the view of either your left-bone model to see its right side OR your right-bone model to see its left side to look inside the cranium: 

You'll have two options to establish the first tangent: 
1) Draw a line by hand via “Markups”>”+Line” along the anterior 1/3rd of the nasal bones in side profile view and name it “tangent1” by double clicking on the name.
![image](https://github.com/user-attachments/assets/3bc8fbe5-4b0c-4ce9-b81f-bcb866b60e63)

2) Or if you’d like the first tangent to be the direction from nasion to rhinion, use the code “tangent1”

![image](https://github.com/user-attachments/assets/27edb95e-5669-40c7-bfda-333a8d772e4f)

```python
F=getNode('Gerasimow landmarks')  
#opens up the collection of point you stored in the markup file#
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     
#number is the number on list of saved points#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(3)
L.AddControlPoint(secondPoint)
L.SetName('tangent1')     
#name of your measurements#

```

Then draw a second line in the general direction of where the acanthion is pointing (like an arrow) and name it “tangent2”. Do not worry if it is slanted drastically to the opposite side – the next code snippet will correct that. 
![image](https://github.com/user-attachments/assets/9ac99a96-4a61-4316-ae92-27b3e44836ee)


Now, use the **tangents to INB** code  that projects the lines to the INB and ensures that tangent 2 bisects the acanthion. 

```python
###Tangents to INB###

import slicer
import numpy as np

# Retrieve the INB plane
INB_plane = slicer.util.getNode('INB')

# Retrieve the point from hard tissue
hard_tissue = slicer.util.getNode('Gerasimow landmarks')
point = hard_tissue.GetNthControlPointPosition(4)

# Function to project a point onto a plane
def project_point_onto_plane(point, plane_origin, plane_normal):
    point_vector = np.array(point) - np.array(plane_origin)
    distance = np.dot(point_vector, plane_normal)
    projected_point = np.array(point) - distance * np.array(plane_normal)
    return projected_point

# Retrieve tangent1 and tangent2
tangent1 = slicer.util.getNode('tangent1')
tangent2 = slicer.util.getNode('tangent2')

# Project tangent1 and tangent2 onto the INB plane
plane_origin = INB_plane.GetOrigin()
plane_normal = INB_plane.GetNormal()

tangent1_start = tangent1.GetNthControlPointPosition(0)
tangent1_end = tangent1.GetNthControlPointPosition(1)
tangent1_start_projected = project_point_onto_plane(tangent1_start, plane_origin, plane_normal)
tangent1_end_projected = project_point_onto_plane(tangent1_end, plane_origin, plane_normal)

tangent2_start = tangent2.GetNthControlPointPosition(0)
tangent2_end = tangent2.GetNthControlPointPosition(1)
tangent2_start_projected = project_point_onto_plane(tangent2_start, plane_origin, plane_normal)
tangent2_end_projected = project_point_onto_plane(tangent2_end, plane_origin, plane_normal)

# Update tangent1 and tangent2 with projected points
tangent1.SetNthControlPointPosition(0, *tangent1_start_projected)
tangent1.SetNthControlPointPosition(1, *tangent1_end_projected)
tangent2.SetNthControlPointPosition(0, *tangent2_start_projected)
tangent2.SetNthControlPointPosition(1, *tangent2_end_projected)

# Adjust tangent2 to bisect the point
midpoint = (np.array(tangent2_start_projected) + np.array(tangent2_end_projected)) / 2
bisect_vector = np.array(point) - midpoint
new_tangent2_end = midpoint + bisect_vector

tangent2.SetNthControlPointPosition(1, *new_tangent2_end)
```
### Elongating the tangents
The lines are now both present but may appear very short due to the projection if you used the whole skull to allocate these tangents. Even if they look reasonably long, they probably won't meet yet. 
After this, copy and paste the script “prn pred” that elongates both tangents until they meet, creating a new node list (and node) as pred prn (predicted pronasale). 

```python

###prn pred###
import slicer
import numpy as np

# Function to calculate the direction vector of a line
def calculate_direction_vector(start, end):
    return np.array(end) - np.array(start)

# Function to find the intersection point of two lines
def find_intersection_point(line1_start, line1_dir, line2_start, line2_dir):
    # Solve for t1 and t2 where line1_start + t1 * line1_dir = line2_start + t2 * line2_dir
    A = np.array([line1_dir, -line2_dir]).T
    b = np.array(line2_start) - np.array(line1_start)
    t = np.linalg.lstsq(A, b, rcond=None)[0]
    intersection_point = line1_start + t[0] * line1_dir
    return intersection_point

# Retrieve tangent1 and tangent2
tangent1 = slicer.util.getNode('tangent1')
tangent2 = slicer.util.getNode('tangent2')

# Get the start and end points of tangent1 and tangent2
tangent1_start = np.array(tangent1.GetNthControlPointPosition(0))
tangent1_end = np.array(tangent1.GetNthControlPointPosition(1))
tangent2_start = np.array(tangent2.GetNthControlPointPosition(0))
tangent2_end = np.array(tangent2.GetNthControlPointPosition(1))

# Calculate the direction vectors
tangent1_dir = calculate_direction_vector(tangent1_start, tangent1_end)
tangent2_dir = calculate_direction_vector(tangent2_start, tangent2_end)

# Find the intersection point
intersection_point = find_intersection_point(tangent1_start, tangent1_dir, tangent2_start, tangent2_dir)

# Create a new markups node called "prn pred"
prn_pred = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'prn pred')
prn_pred.AddControlPoint(intersection_point)

# Extend tangent1 and tangent2 beyond the intersection point
extension_length = 10  # Adjust this value as needed

new_tangent1_end = intersection_point + extension_length * tangent1_dir / np.linalg.norm(tangent1_dir)
new_tangent2_end = intersection_point + extension_length * tangent2_dir / np.linalg.norm(tangent2_dir)

tangent1.SetNthControlPointPosition(1, *new_tangent1_end)
tangent2.SetNthControlPointPosition(1, *new_tangent2_end)

print(f"Intersection point added to 'prn pred': {intersection_point}")
print(f"New tangent1 end point: {new_tangent1_end}")
print(f"New tangent2 end point: {new_tangent2_end}")
```
### Error rate
As a research question, you can also allocate the original pronasale (included in the _Gerasimow landmarks.lmrk.json_ as the last item) and check the error rate (copy and paste the code "prn error"). 

```python
###prn error####

import slicer
import numpy as np

# Retrieve the points
hard_tissue = slicer.util.getNode('Gerasimow landmarks')
point1 = hard_tissue.GetNthControlPointPosition(5)

prn_pred = slicer.util.getNode('prn pred')
point2 = prn_pred.GetNthControlPointPosition(0)

# Create a new markups line node
line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pred error')
line_node.AddControlPoint(point1)
line_node.AddControlPoint(point2)

# Set the color to burgundy (RGB: 128, 0, 32)
line_node.GetDisplayNode().SetSelectedColor(128/255, 0/255, 32/255)
line_node.GetDisplayNode().SetColor(128/255, 0/255, 32/255)

print(f"New line created between points: {point1} and {point2} with color burgundy")
```
 With every new line, your environment is looking like this: 

![image](https://github.com/user-attachments/assets/2dc4a929-39ec-4bed-916f-fdd49029db2b)

To copy the error measurement, use the method described in [this guide](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/004_Copying%20measurements%20to%20Clipboard.md). 

The output will look like this: 

| (unknown) | tangent1 | 76.67370706918534 |
| (unknown) | tangent2 | 52.81195129766234 | 
| (unknown) | pred error | 16.34060755830103 |

> [!IMPORTANT]
> Only "pred error" is a true measurement, do not use the other measurements as such in your data analysis!!!!




### Bibliography: 

1. [Slicer Script Repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
2. Gerasimov, M. (1955). "Vosstanovlenie lica po cerepu." Akademii Nauk SSSR.
3. Gerassimow, M. (1968). Ich suchte Gesichter. Gutersloh (Germany): C, Bertelsmann Verlag.
4. Gerasimov, M. (1971). The Face Finder. London, Hutchinson.
5. Wilkinson, C. (2004). Forensic Facial Reconstruction. Cambridge, UK, Cambridge University Press.
6. Ullrich, H. and C. N. Stephan (2011). "On Gerasimov’s plastic facial reconstruction technique: new insights to facilitate repeatability." Journal of forensic sciences 56(2): 470-474.
7. Ullrich, H. and C. Stephan (2016). "Mikhail Mikhaylovich Gerasimov’s Authentic Approach to Plastic Facial Reconstruction." Anthropologie (Czech Republic) 54: 97-107.
8. Gatliff, B. P. (1984). "Facial sculpture on the skull for identification." American Journal of Forensic Medicine and Pathology 5(4): 327-332.
9. Stephan, C. N., et al. (2003). "Predicting nose projection and pronasale position in facial approximation: a test of published methods and proposal of new guidelines." American Journal of Physical Anthropology: The Official Publication of the American Association of Physical Anthropologists 122(3): 240-250.
10. Rynn, C. and C. M. Wilkinson (2006). "Appraisal of traditional and recently proposed relationships between the hard and soft dimensions of the nose in profile." American Journal of Physical Anthropology: The Official Publication of the American Association of Physical Anthropologists 130(3): 364-373.
11. Rynn, C., et al. (2012). Relationships between the skull and face. Craniofacial identification. C. W. C. Rynn. Cambridge, Cambridge University Press: 193-202.
12. Caple, J. and C. N. Stephan (2016). "A standardized nomenclature for craniofacial and facial anthropometry." Int J Legal Med 130(3): 863-879.
