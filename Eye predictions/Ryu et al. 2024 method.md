# The Ryu et al. (2024)[^2] method 

The following guide is constructed by the available original study by Ryu et al. (2024)[^2].

The original method was carried out on post-mortem CTs on a population of 171 Korean adults. It devised multple linear regressions to place the most anterior point of the eyeball in 3 dimensions in relation to the bony orbit, with slightly different definitions for orbital breadth and height. 

## Table of Contents

> [!WARNING]
> The sample CT (CBCT PreDentalSurgery) used in the screenshots of this guide does not have all the features (bregma) that are to be landmarked. Please refer to the illustrations in the guide for correct placement. In addition, due to the CT being taken pre-surgery for an underbite, the error rate shown in the guide is probably not representative if implemented on a population without pathologies.



## Landmarks in this guide: 

| Position in code | Position in file | Name in file | Landmark | Definition | defined by | tissue type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | 1 | n | Nasion | The junction of the internasal suture with the nasofrontal suture | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 1 | 2 | pr | Prosthion | The lowermost point of the intermaxillary suture between the central incisors of the maxilla. | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 2 | 3 | auL | Auriculare (left) | On the LEFT zygomatic root, vertically above the center of the external auditory meatus | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 3 | 4 | auR | Auriculare (right) | On the RIGHT zygomatic root, vertically above the center of the external auditory meatus | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 4 | 5 | mid_au | Auriculare Midpoint | The midpoint in the 3D coordinates of both AU | Ryu et al. 2024 [^2] | hard |
| 5 | 6 | orL | Orbitale (left) | The lowest point on the LEFT orbital rim | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 6 | 7 | orR | Orbitale (right) | The lowest point on the RIGHT orbital rim | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 7 | 8 | b | Bregma | Where the sagittal and coronal sutures meet | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 8 | 9 | g | Glabella | Most projecting anterior median point on lower edge of the frontal bone, on the brow ridge, in between the superciliary arches and above the nasal root. | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 9 | 10 | lat_orL | Lateral Orbitale (left) | Most lateral point on the left orbital rim | Ryu et al. 2024 [^2] | hard |
| 10 | 11 | lat_orR | Lateral Orbitale (right) | Most lateral point on the RIGHT orbital rim | Ryu et al. 2024 [^2] | hard |
| 11 | 12 | dL | Median Orbitale (left) | The point where the LEFT anterior lacrimal ridge meets frontonasal suture(=dacryion) | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 12 | 13 | dR | Median Orbitale (right) | The point where the RIGHT anterior lacrimal ridge meets frontonasal suture | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 13 | 14 | skL | Supra Orbitale (left) | The most upper point on the LEFT orbital rim | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 14 | 15 | skR | Supra Orbitale (right) | The most upper point on the RIGHT orbital rim | Martin, 1928 [^3]; Knussmann, 1988 [^4] | hard |
| 15 | 16 | 🟦ocpR | Optic Canal Point (right) | Uppermost point of the RIGHT optic nerve canal | Ryu et al. 2024 [^2] | soft |
| 16 | 17 | 🟦ocpL | Optic Canal Point (left) | Uppermost point of the LEFT optic nerve canal | Ryu et al. 2024 [^2] | soft |
| 17 | 18 | 🟦lcL | Lens Centre (left) | The center of gravity of the left lens (sic!)- geometric mean | Ryu et al. 2024 [^2] | soft |
| 18 | 19 | 🟦lcR | Lens Centre (right) | The center of gravity of the right lens (sic!)- geometric mean | Ryu et al. 2024 [^2] | soft |
| 19 | 20 | 🟦laL | Lens Anterior (left) | The most anterior point of the LEFT lens | Ryu et al. 2024 [^2] | soft |
| 20 | 21 | 🟦laR | Lens Anterior (right) | The most anterior point of the RIGHT lens | Ryu et al. 2024 [^2] | soft |
| 21 | 22 | 🟦lpL | Lens Posterior (left) | The most posterior point of the LEFT lens | Ryu et al. 2024 [^2] | soft |
| 22 | 23 | 🟦lpR | Lens Posterior (right) | The most posterior point of the RIGHT lens | Ryu et al. 2024 [^2] | soft |
| 23 | 24 | 🟦osL | Globe Superior (left) | The uppermost point of the LEFT eyeball | Guyomarc'h, 2012 [^5] | soft |
| 24 | 25 | 🟦osR | Globe Superior (right) | The uppermost point of the RIGHTeyeball | Guyomarc'h, 2012 [^5] | soft |
| 25 | 26 | 🟦oiL | Globe Inferior (left) | The lowest point of the LEFT eyeball | Guyomarc'h, 2012 [^5] | soft |
| 26 | 27 | 🟦oiR | Globe Inferior (right) | The lowest point of the RIGHT eyeball | Guyomarc'h, 2012 [^5] | soft |
| 27 | 28 | 🟦opL | Globe Lateral (left) | The most lateral point of the LEFT eyeball | Guyomarc'h, 2012 [^5] | soft |
| 28 | 29 | 🟦opR | Globe Lateral (right) | The most lateral point of the RIGHT eyeball | Guyomarc'h, 2012 [^5] | soft |
| 29 | 30 | 🟦omL | Globe Medial (left) | The most medial mole (sic!) of the LEFT eyeball. | Ryu et al. 2024 [^2] | soft |
| 30 | 31 | 🟦omR | Globe Medial (right) | The most medial mole (sic!) of the RIGHT eyeball. | Ryu et al. 2024 [^2] | soft |
| 31 | 32 | 🟦oaL | Cornea (left) | The most anterior point of the LEFT eyeball | originally undefined! | soft |
| 32 | 33 | 🟦oaR | Cornea (right) | The most anterior point of the RIGHT eyeball | originally undefined! | soft |
| 33 | 34 | 🟦pL | if available, left pupulare | IF DISTINGUISHABLE, Centre of the LEFT pupil | ADDITIONAL | soft |
| 34 | 35 | 🟦pR | if available, right pupulare | IF DISTINGUISHABLE, Centre of the RIGHT pupil | ADDITIONAL | soft |
| 35 | 36 | 🟦gcL | left globe centre | calculated programmatically | originally undefined! | soft |
| 36 | 37 | 🟦gcR | right globe centre | calculated programmatically | originally undefined! | soft |

> [!IMPORTANT]
> The landmarks with the 🟦 symbol are for reproducing the entire method for validation and not essential to place for applying the eyeball placement for facial approximation.

Illustration of the method: 


> [!WARNING]
> Before you proceed, please make sure you completed the following steps: 

- [ ] The scan has to be re-aligned in the FHP
- [ ] Hard tissue landmarks from the [hard tissue landmark file]([Ryu_hard_tissue.mrk.json](https://github.com/user-attachments/files/27120614/Ryu_hard_tissue.mrk.json); except for the mis-auriculare have to be allocated

<img width="906" height="1026" alt="image" src="https://github.com/user-attachments/assets/19d34a4f-641b-4b5e-a051-ea154bc24ac0" />

Aiding code to place mid-auriculare
<details>
<summary>mid-au calculation</summary>

	
```python
import slicer
import numpy as np

def update_mid_auriculare_midpoint():
    """
    Calculates the midpoint between 'auL' and 'auR' from a loaded fiducial node
    and updates the position of the 'mid_au' landmark within that same node.
    """
    
    # --- 1. Configuration ---
    # The name of your fiducial list node in the Slicer scene.
    # This should match the name of the file you loaded.
    fiducials_node_name = "Ryu_hard_tissue" 
    
    # --- 2. Get the Landmark Node ---
    try:
        landmarks_node = slicer.util.getNode(fiducials_node_name)
    except slicer.util.MRMLNodeNotFoundException:
        slicer.util.errorDisplay(
            f"Landmark node '{fiducials_node_name}' not found. "
            "Please load your 'Ryu_hard_tissue.mrk.json' file first."
        )
        return

    # --- 3. Get Auriculare Positions ---
    auL_pos, auR_pos = None, None
    for i in range(landmarks_node.GetNumberOfControlPoints()):
        label = landmarks_node.GetNthControlPointLabel(i)
        pos = np.zeros(3)
        landmarks_node.GetNthControlPointPosition(i, pos)
        if label == "auL":
            auL_pos = pos
        elif label == "auR":
            auR_pos = pos

    # Check if both landmarks were found
    if auL_pos is None or auR_pos is None:
        slicer.util.errorDisplay("Could not find 'auL' and/or 'auR' in the landmark node.")
        return

    # --- 4. Calculate the Correct Midpoint ---
    correct_mid_au_pos = (auL_pos + auR_pos) / 2.0
    
    # --- 5. Find and Update the 'mid_au' Landmark ---
    mid_au_index = -1
    for i in range(landmarks_node.GetNumberOfControlPoints()):
        if landmarks_node.GetNthControlPointLabel(i) == "mid_au":
            mid_au_index = i
            break
            
    if mid_au_index != -1:
        # Update the position of the existing 'mid_au' point
        landmarks_node.SetNthControlPointPosition(mid_au_index, correct_mid_au_pos)
        slicer.util.infoDisplay(
            f"Successfully updated 'mid_au' landmark to its correct position: {correct_mid_au_pos}"
        )
    else:
        # If 'mid_au' doesn't exist for some reason, add it
        landmarks_node.AddControlPoint(correct_mid_au_pos, "mid_au")
        slicer.util.warningDisplay("The 'mid_au' landmark was not found, so a new one has been added at the correct position.")
        
# --- Run the function ---
update_mid_auriculare_midpoint()
```

</details>



Example of scene when hard tissue landmarks are allocated


### Main Planes

Ryu et al. (2024)[^2] defined 3 anatomical planes as reference for the further steps in their method: The Frankfort Horizontal plane, the sagittal and frontal planes.  The following code will execute the creation of the 3 planes; just copy and paste it in the Python console, then press enter. 

| Plane |  Definition |
| :--- | :--- |
| Median sagittal plane | Plane passing through 3 landmarks, Nasion, prosthion, auriculare midpoint |
| Orbitale transverse plane | Plane passing through 2 landmarks, orbitale left and auriculare midpoint and orthogonal to the medial sagittal plane |
| Coronal plane | Plane passing through 1 landmark, bregma and orthogonal to the median sagittal and orbitale transverse planes |

<img width="923" height="908" alt="image" src="https://github.com/user-attachments/assets/4607a058-99dc-4cb7-9b19-5240ebfc54b0" />

Example screenshot of the scene after creating the three main reference planes (note that the plane "sizes" were adjusted for visual purposes, they are technically infinite)


<details>
<summary>Main planes code</summary>

	
```python
import slicer
import numpy as np

print("="*60)
print("Running Step 1: Create Main Anatomical Planes (Corrected)")
print("="*60)

def unit(v):
    n = np.linalg.norm(v)
    if n < 1e-9: raise ValueError("Cannot normalize zero-length vector")
    return v / n

def get_landmark(node, label):
    for i in range(node.GetNumberOfControlPoints()):
        if node.GetNthControlPointLabel(i) == label:
            p = np.zeros(3); node.GetNthControlPointPositionWorld(i, p)
            return p
    raise ValueError(f"Landmark '{label}' not found.")

def get_or_create(cls, name):
    n = slicer.mrmlScene.GetFirstNodeByName(name)
    if not n: n = slicer.mrmlScene.AddNewNodeByClass(cls, name)
    return n

def style_plane(plane, color, opacity=0.8):
    d = plane.GetDisplayNode() or plane.CreateDefaultDisplayNodes()
    d.SetColor(color); d.SetSelectedColor(color); d.SetOpacity(opacity); d.SetVisibility(True)

try:
    hard_node = slicer.util.getNode("Ryu_hard_tissue")

    # --- THIS IS THE KEY FIX: Define vectors robustly from landmarks first ---
    auR, auL, n = get_landmark(hard_node, 'auR'), get_landmark(hard_node, 'auL'), get_landmark(hard_node, 'n')
    vec_right = unit(auR - auL)
    vec_anterior_initial = unit(n - (auR + auL) / 2.0)
    vec_anterior = unit(vec_anterior_initial - np.dot(vec_anterior_initial, vec_right) * vec_right) # Orthogonalize
    vec_superior = unit(np.cross(vec_right, vec_anterior)) # Guarantees a right-handed system

    print(f"Corrected vec_superior: {np.round(vec_superior, 2)}")
    print(f"Corrected vec_right:    {np.round(vec_right, 2)}")
    print(f"Corrected vec_anterior: {np.round(vec_anterior, 2)}")

    # Create planes from these corrected vectors
    midsag_plane = get_or_create("vtkMRMLMarkupsPlaneNode", "Median Sagittal Plane (Trial)")
    midsag_plane.SetOrigin(get_landmark(hard_node, 'n')); midsag_plane.SetNormal(vec_right)
    style_plane(midsag_plane, [0.2, 0.8, 0.2])

    orbital_plane = get_or_create("vtkMRMLMarkupsPlaneNode", "Orbitale Transverse Plane (Trial)")
    orbital_plane.SetOrigin(get_landmark(hard_node, 'orL')); orbital_plane.SetNormal(vec_superior)
    style_plane(orbital_plane, [0.8, 0.2, 0.2])

    coronal_plane = get_or_create("vtkMRMLMarkupsPlaneNode", "Coronal Plane (Trial)")
    coronal_plane.SetOrigin(get_landmark(hard_node, 'b')); coronal_plane.SetNormal(vec_anterior)
    style_plane(coronal_plane, [0.2, 0.2, 0.8])

    print("\nStep 1 complete. Main anatomical planes created with correct orientation.")

except Exception as e:
    slicer.util.errorDisplay(f"An error occurred in Step 1: {e}")

```

</details>


### Marginal lines and planes

Now that the "blueprint" planes are present, the guiding lines and marginal planes bisecting the most extreme landmarks can be programmatically created. These are both techinically infinite, but  the guiding lines will be uniformly 75 mm to visualise them - please note that these are NOT measurements. 
Below are the definitions of all the lines/planes created via the code below:

| Line | Landmark to Bisect | Definition | Plane for Reference | Direction | Defined by |
|------|--------------------|------------|---------------------|-----------|-------------|
| guiding_SOM_L/R | skL/R | superior orbital margin on the left/right | parallel to Orbitale transverse plane | laterally | Stephan, 2008[^5] |
| guiding_MOM_L/R | dL/R | medial orbital margin on the left/right | parallel to Median sagittal plane | superoinferiorly | Stephan, 2008[^5] |
| guiding_LOM_L | lat_orL | lateral-most point on the lateral orbital margin on the left | parallel to Median sagittal plane | superoinferiorly | Stephan, 2008[^5] |
| guiding_LOM_R | lat_orR | lateral-most point on the lateral orbital margin on the right | parallel to Median sagittal plane | superoinferiorly | Ryu et al 2024[^2] |
| guiding_IOM_L/R | orL/R | inferior-most point on the infraorbital margin (orbitale) on the left/right | parallel to Orbitale transverse plane | laterally | Stephan, 2008[^5] |

| Plane | Landmark to Bisect | Definition | Plane for Reference | Direction | Defined by |
|-------|--------------------|------------|---------------------|-----------|-------------|
| marginal_SOM_L/R | skL/R | superior orbital marginal plane on the left/right | parallel to Orbitale transverse plane | superoinferiorly | Stephan, 2008[^5] |
| marginal_MOM_L/R | dL/R | medial orbital marginal plane on the left/right | parallel to Median sagittal plane | laterally | Stephan, 2008[^5] |
| marginal_LOM_L | lat_orL | lateral-most point on the lateral orbital marginal plane on the left | parallel to Median sagittal plane | laterally | Stephan, 2008[^5] |
| marginal_LOM_R | lat_orR | lateral-most point on the lateral orbital marginal plane on the right | parallel to Median sagittal plane | laterally | Ryu et al 2024[^2] |
| marginal_IOM_L/R | orL/R | inferior-most point on the infraorbital marginal plane (orbitale) on the left/right | parallel to Orbitale transverse plane | superoinferiorly | Stephan, 2008[^5] |

* note that the directionalities are opposite for planes and lines!

<img width="947" height="791" alt="image" src="https://github.com/user-attachments/assets/f806980f-b5ea-4bab-93af-7817b06f0ef8" />


Screenshot after the code below was run, all other lines/planes/landmarks were hidden from visibility.


<details>	
<summary> Marginal planes and guiding lines code </summary>

```python
import slicer
import numpy as np

print("="*60)
print("Running Step 2: Create Marginal Planes and Guiding Lines")
print("="*60)

def unit(v):
    n = np.linalg.norm(v); return v / n if n > 1e-9 else v

def get_landmark(node, label):
    for i in range(node.GetNumberOfControlPoints()):
        if node.GetNthControlPointLabel(i) == label:
            p = np.zeros(3); node.GetNthControlPointPositionWorld(i, p)
            return p
    raise ValueError(f"Landmark '{label}' not found.")

def get_or_create(cls, name):
    n = slicer.mrmlScene.GetFirstNodeByName(name)
    if not n: n = slicer.mrmlScene.AddNewNodeByClass(cls, name)
    if "Line" in cls: n.RemoveAllControlPoints()
    return n

def style_line(line, color):
    d = line.GetDisplayNode() or line.CreateDefaultDisplayNodes()
    d.SetColor(color); d.SetSelectedColor(color); d.SetVisibility(True)

def style_plane(plane, color, opacity=0.8):
    d = plane.GetDisplayNode() or plane.CreateDefaultDisplayNodes()
    d.SetColor(color); d.SetSelectedColor(color); d.SetOpacity(opacity); d.SetVisibility(True)

def make_line(name, p0, p1, color):
    ln = get_or_create("vtkMRMLMarkupsLineNode", name)
    ln.AddControlPoint(p0); ln.AddControlPoint(p1)
    ln.GetMeasurement("length").SetEnabled(True)
    style_line(ln, color)

try:
    hard_node = slicer.util.getNode("Ryu_hard_tissue")
    
    # Get vectors from the correctly oriented main planes
    vec_superior = np.array(slicer.util.getNode("Orbitale Transverse Plane (Trial)").GetNormal())
    vec_right = np.array(slicer.util.getNode("Median Sagittal Plane (Trial)").GetNormal())

    # Create marginal geometry
    defs = [
        ("SOM", "sk", vec_superior, vec_right), ("IOM", "or", vec_superior, vec_right),
        ("MOM", "d", vec_right, vec_superior), ("LOM", "lat_or", vec_right, vec_superior)
    ]
    for base, lm_prefix, plane_n, line_dir in defs:
        for s in ["L", "R"]:
            p = get_landmark(hard_node, f"{lm_prefix}{s}")
            c = [1,0.7,0.2] if s=="L" else [0.2,0.7,1] # Orange for Left, Purple for Right
            pl = get_or_create("vtkMRMLMarkupsPlaneNode", f"marginal_{base}_{s}")
            pl.SetOrigin(p); pl.SetNormal(plane_n); style_plane(pl, c)
            make_line(f"guiding_{base}_{s}", p - line_dir*37.5, p + line_dir*37.5, c)

    print("\nStep 2 complete. Marginal planes and guiding lines created.")

except Exception as e:
    slicer.util.errorDisplay(f"An error occurred in Step 2: {e}")


```

</details>


### Applying the regressions of Guyomarc'h et al. (2012)[^2]
Guyomarc'h et al. (2012)[^2] devised regressions to predict the position of the oa (oculare anterior), which they converted into proportions of the OBB and OBH. Although their research did not differentiate beftween the sides for the regressions, they reported significant differences between the bony orbits, therefore the regressions in the code are side-specific. When running the code, expect a pop-up window of a graphic user interface (GUI) which asks you to download an artificial eye model for a male or female. The current study did not differentiate between the biological sexes, but some do, hence the option. All eye models were adjusted to the average size of a human eyeball, 24mm in diameter. You'll have to choose the left and right eyes individually - so clicking the "Download and Place Eyeball" twice, but choosing the other side from the dropdown menu. 

<img width="1393" height="786" alt="image" src="https://github.com/user-attachments/assets/dbe41aab-09e6-4d7e-80cb-ca305e33c9a7" />

Expect this additional window on the right. 

<img width="658" height="288" alt="image" src="https://github.com/user-attachments/assets/547c0cef-daab-4144-a003-433f58fd51ae" />

Illustrating the drop-down menu


Summary of the lengths and directions of the regressions adjusted for side-specific coding: 

| Direction of eyeball | Left orbit | Right orbit |
| :--- | :--- | :--- |
| Superoinferior | 44.1% of OBH from skL | 44.1% of OBH from skR |
| Mediolateral | 57.6% of OBB from dL | 57.6% of OBB from dR |
| Anteroposterior | 51.3% of OBH from dlomL | 51.3% of OBH from dlomR |


<details>	
<summary> Eye model placement code </summary>
	
```python


```

</details>


<img width="874" height="1125" alt="image" src="https://github.com/user-attachments/assets/b3ade752-6d3c-49c7-924f-3c833081cf0b" />

View after placing both eyeballs


### Validating the original study
If you wanted to use this this tool for an approximation, you're done!

Additionally, we can compare the predicted and the actual eyeball positions via landmarks, by placing the soft tissue landmarks denoted with a blue square in the previous section "Landmarks in this study". 
You can download them [here](https://github.com/user-attachments/files/26708232/true_eyeball.mrk.json). 
Once you placed the "ground truth" landmarks (called true_eyeball.lmrk.json) onto the scan (you'll likely have to use the red/green/yellow windows for a more precise placement), you can run the code below. 

It will create two comparison tables: (1) for comparing length measurements between the "artificial" eyeball model and the true eyeball that were measured by Guyomarc'h et al. (2012)[^2] in the original studt to create the regressions; (2) for measuring the distance between the true vs artificial eyeball landmarks. 

(1) 
| Landmark from `true_eyeball.mrk.json` (scan) | Landmark from artificial eyeball | Error Measurement Name |
| :--- | :--- | :--- |
| true_oaR | oaR | oaR_error |
| true_oaL | oaL | oaL_error |
| true_opR | opR | opR_error |
| true_opL | opL | opL_error |
| true_osR | osR | osR_error |
| true_osL | osL | osL_error |
| true_oiR | oiR | oiR_error |
| true_oiL | oiL | oiL_error |
| true_omL | omL | omL_error |
| true_omR | omR | omR_error |
| true_olL | olL | olL_error |
| true_olR | olR | olR_error |
| true_pL | pL | pL_error |
| true_pR | pR | pR_error |

(2) 
| Line Name | Definition |
| :--- | :--- |
| true_DLOM-R-oaR | perpendicular (shortest) distance between DLOM_R line and true_oaR (right eyeball projection) |
| true_DLOM-L-oaL | perpendicular (shortest) distance between DLOM_L line and true_oaL (left eyeball projection) |
| true_SOM_L-oaL | perpendicular (shortest) distance between SOM_L line and true_oaL |
| true_IOM_L-oaL | perpendicular (shortest) distance between IOM_L line and true_oaL |
| true_LOM_L-oaL | perpendicular (shortest) distance between LOM_L line and true_oaL |
| true_MOM_L-oaL | perpendicular (shortest) distance between MOM_L line and true_oaL |
| true_SOM_R-oaR | perpendicular (shortest) distance between SOM_R line and true_oaR |
| true_IOM_R-oaR | perpendicular (shortest) distance between IOM_R line and true_oaR |
| true_LOM_R-oaR | perpendicular (shortest) distance between LOM_R line and true_oaR |
| true_MOM_R-oaR | perpendicular (shortest) distance between MOM_R line and true_oaR |
| pred_DLOM-R-oaR | perpendicular (shortest) distance between DLOM_R line and oaR |
| pred_DLOM-L-oaL | perpendicular (shortest) distance between DLOM_L line and oaL |
| pred_SOM_L-oaL | perpendicular (shortest) distance between SOM_L line and oaL |
| pred_IOM_L-oaL | perpendicular (shortest) distance between IOM_L line and oaL |
| pred_LOM_L-oaL | perpendicular (shortest) distance between LOM_L line and oaL |
| pred_MOM_L-oaL | perpendicular (shortest) distance between MOM_L line and oaL |
| pred_SOM_R-oaR | perpendicular (shortest) distance between SOM_R line and oaR |
| pred_IOM_R-oaR | perpendicular (shortest) distance between IOM_R line and oaR |
| pred_LOM_R-oaR | perpendicular (shortest) distance between LOM_R line and oaR |
| pred_MOM_R-oaR | perpendicular (shortest) distance between MOM_R line and oaR |



<details>	
<summary> Eye model placement code </summary>
	
```python

```

</details>


<img width="871" height="693" alt="{7586E9C8-BB6E-4B46-B2AA-4EE8F046E0DF}" src="https://github.com/user-attachments/assets/327f841e-fc60-4ef5-927f-65ed6b9582e7" />


In addition, the code will print some information on the console, something like this: 

```python

```



### Output
To copy all the linear measurements to clipboard, use the method described in [this guide](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/004_Copying%20measurements%20to%20Clipboard.md). 

> [!IMPORTANT]
> It is very important that you do not treat the pre-programmed lines with set length as measurements in your statistical analysis, therefore there is an example below. 

| ID | line node name | length in mm | Note |
| :--- | :--- | :--- | :--- |
| (none) | L orbit bisecting line | 100 | ❌ - not a real measurement |

* IDs will return none or unknown if your data was anonymised appropriately



## Bibliography

[^1]: [Slicer Script Repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
[^2]: Ryu, J. Y., et al. (2024). "Developing an eyeball positioning method in the eye orbit for craniofacial identification in Korean population." Scientific Reports 14(1).
[^3]: Martin, R. (1928). Lehrbuch der Anthropologie in systematischer Darstellung: mit besonderer Berücksichtigung der anthropologischen Methoden ; für Studierende, Ärzte und Forschungsreisendechichte, Morphologische Methoden. Jena, Gustav Fisher.
[^4]: Knussmann, R. (1988). Anthropologie: Handbuch der vergleichenden Biologie des Menschen, G. Fischer.
[^5]: Guyomarc'h, P., et al. (2012). "Anatomical placement of the human eyeball in the orbit--validation using CT scans of living adults and prediction for facial approximation." J Forensic Sci 57(5): 1271–1275.

[^5]: Stephan, C. N. and P. L. Davidson (2008). "The placement of the human eyeball and canthi in craniofacial identification." Journal of Forensic Sciences 53(3): 612–619.
[^6]: Guyomarc'h, P., et al. (2012). "Anatomical Placement of the Human Eyeball in the Orbit-Validation Using CT Scans of Living Adults and Prediction for Facial Approximation." Journal of Forensic Sciences 57(5): 1271–1275.
