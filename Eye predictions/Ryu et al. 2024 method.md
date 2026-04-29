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

#### Aiding code to place mid-auriculare
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


### Hard tissue measurements for prediction ONLY
Ryu et al. (2024)[^2]  devised regressions specific for biological sex to predict the position of the oa (oculare anterior/cornea by their terminology) and the lens centre, that depend on a few chosen measurement **L/R1, 8, 15, 20**. Regressions from the bony measurements predict soft tissue dimensions **L/R21,22,23,27 and 33**; which determine the approximated position of the eyeball in 3 dimensions. The following code creates the hard tissue measurement necessary to undertake the prediction, summarised in the table below. 

| Line name | Description |
|----------------|-------------|
| L1 | shortest perpendicular guiding_MOM_L line to guiding_LOM_L line distance |
| R1 | shortest perpendicular guiding_MOM_R line to guiding_LOM_R line distance |
| L8 | shortest perpendicular guiding_SOM_L line to guiding_IOM_L line distance |
| R8 | shortest perpendicular guiding_SOM_R line to guiding_IOM_R line distance |
| L15 | shortest perpendicular Coronal plane-guiding_LOM_L line distance |
| R15 | shortest perpendicular Coronal plane-guiding_LOM_R line distance |
| L20 | shortest perpendicular Coronal plane-guiding_IOM_L line distance |
| R20 | shortest perpendicular Coronal plane-guiding_IOM_R line distance |

<details>	
<summary> Core hard tissue measurment code </summary>
	
```python
import slicer
import numpy as np

print("="*60)
print("Running Step 3: Create Hard Tissue Measurements")
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

def make_line(name, p0, p1, color, value=None):
    ln = get_or_create("vtkMRMLMarkupsLineNode", name)
    ln.AddControlPoint(p0); ln.AddControlPoint(p1)
    ln.GetMeasurement("length").SetEnabled(True)
    if value is not None: ln.GetMeasurement("length").SetValue(value)
    style_line(ln, color)
    return ln

try:
    hard_node = slicer.util.getNode("Ryu_hard_tissue")
    vec_superior = np.array(slicer.util.getNode("Orbitale Transverse Plane (Trial)").GetNormal())
    vec_right = np.array(slicer.util.getNode("Median Sagittal Plane (Trial)").GetNormal())
    vec_anterior = np.array(slicer.util.getNode("Coronal Plane (Trial)").GetNormal())
    
    cyan = [0,1,1]
    
    for s in ["L", "R"]:
        # L1/R1
        lom_p = get_landmark(hard_node, f"lat_or{s}")
        mom_p = get_landmark(hard_node, f"d{s}")
        dist = abs(np.dot(lom_p - mom_p, vec_right))
        make_line(f"{s}1", mom_p, mom_p + vec_right * np.dot(lom_p - mom_p, vec_right), cyan, dist)
        
        # L8/R8
        som_p = get_landmark(hard_node, f"sk{s}")
        iom_p = get_landmark(hard_node, f"or{s}")
        dist = abs(np.dot(som_p - iom_p, vec_superior))
        make_line(f"{s}8", iom_p, iom_p + vec_superior * np.dot(som_p - iom_p, vec_superior), cyan, dist)
        
        # L15/R15
        lom_p = get_landmark(hard_node, f"lat_or{s}")
        coronal_origin = np.array(slicer.util.getNode("Coronal Plane (Trial)").GetOrigin())
        dist = abs(np.dot(lom_p - coronal_origin, vec_anterior))
        make_line(f"{s}15", lom_p, lom_p - vec_anterior * np.dot(lom_p - coronal_origin, vec_anterior), cyan, dist)

        # L20/R20  (shortest perpendicular Coronal plane to IOM point)
        iom_p = get_landmark(hard_node, f"or{s}")
        dist_iom = abs(np.dot(iom_p - coronal_origin, vec_anterior))
        make_line(f"{s}20", iom_p, iom_p - vec_anterior * np.dot(iom_p - coronal_origin, vec_anterior), cyan, dist_iom)
    
    print("\nStep 3 complete. Hard tissue measurement lines created.")
    print("\nSetup is finished. You can now use the GUI for placement.")

except Exception as e:
    slicer.util.errorDisplay(f"An error occurred in Step 3: {e}")

```

</details>

<img width="956" height="765" alt="image" src="https://github.com/user-attachments/assets/78d8dc79-522e-4673-a23d-21eae74c81ce" />

### Eye model placement

Next, the **L/R21,22,23,27 and 33** will be calculated using the hard tissue measurements from the previous step; as published by Ryu et al. (2024)[^2]. These are not visualised before the eyeball placement, but after. When running the code, expect a pop-up window of a graphic user interface (GUI) which asks you to download an artificial eye model for a male or female. The current study did not differentiate between the biological sexes, but some do, hence the option. All eye models were adjusted to the average size of a human eyeball, 24mm in diameter. You'll have to choose the left and right eyes individually - so clicking the "Download and Place Eyeball" twice, but choosing the other side from the dropdown menu. 

| Predictor  | Male equation | Female equation | Predicted soft tissue measurement | Definition of soft tissue measurement |
|----------------------|---------------|-----------------|----------------------------------|----------------------------------------|
| L1 | L23 = 0.844 × L1 - 11.224 | L23 = 0.619 × L1 - 2.175 | L23 |oaL perpendicular distance "inward/laterally" from the MOM_L |
| L8 | L21 = 0.560 × L8 - 3.648 | L21 = 0.349 × L8 + 4.320 | L21 | oaL perpendicular distance "downward" from the SOM_L |
| L8 | L22 = 0.439 × L8 + 3.662 | L22 = 0.652 × L8 - 4.353 | L22 | oaL perpendicular distance "upward" from the IOM_L |
| L15 | L27 = 0.989 × L15 + 11.550 | L27 = 1.007 × L15 + 9.552 | L27 | lcL perpendicular distance "forward/anterior" from the Coronal plane |
| L15 | L33 = 0.950 × L15 + 19.126 | L33 = 1.005 × L15 + 14.700 | L33 | oaL perpendicular distance "forward/anterior" from the Coronal plane |
| L20 | L27 = 0.889 × L20 + 11.756 | L27 = 0.969 × L20 + 5.309 | L27 | lcL perpendicular distance "forward/anterior" from the Coronal plane |
| L20 | L33 = 0.865 × L20 + 18.436 | L33 = 1.028 × L20 + 6.826 | L33 | oaL perpendicular distance "forward/anterior" from the Coronal plane |
| R1 | R23 = 0.734 × R1 - 6.687 | R23 = 0.449 × R1 + 4.505 | R23 | oaR perpendicular distance "inward/laterally" from the MOM_R |
| R8 | R21 = 0.562 × R8 - 3.923 | R21 = 0.407 × R8 + 2.082 | R21 | oaR perpendicular distance "downward" from the SOM_R |
| R8 | R22 = 0.438 × R8 + 3.939 | R22 = 0.593 × R8 - 2.064 | R22 | oaR perpendicular distance "upward" from the IOM_R |
| R15 | R27 = 0.978 × R15 + 12.421 | R27 = 0.951 × R15 + 12.818 | R27 | lcR perpendicular distance "forward/anterior" from the Coronal plane |
| R15 | R33 = 0.954 × R15 + 18.983 | R33 = 0.973 × R15 + 16.707 | R33 | oaR perpendicular distance "forward/anterior" from the Coronal plane |
| R20 | R27 = 0.867 × R20 + 13.012 | R27 = 0.905 × R20 + 9.297 | R27 | lcR perpendicular distance "forward/anterior" from the Coronal plane |
| R20 | R33 = 0.840 × R20 + 19.843 | R33 = 0.985 × R20 + 9.354 | R33 | oaR perpendicular distance "forward/anterior" from the Coronal plane |


When running the code, expect a pop-up window of a graphic user interface (GUI) which asks you to download an artificial eye model for a male or female. The current study did differentiate between the biological sexes hence the option. 
All eye models were adjusted to the average size of a human eyeball, 24mm in diameter. You'll have to choose the left and right eyes individually - so clicking the "Download and Place Eyeball" twice, but choosing the other side from the dropdown menu. 
There is also an option to choose whether you want to use **L/R15 or L/R20 or their average** for calculating **L/R27 and L/R33** - this is beacuse the original authors provided multiple, equally well-performing regressions for these. 

> [!IMPORTANT]
> After the left eyeball is placed, the scene may "jump". No action needed, it should be restored either after the right eye is placed, or simply clicking the "Anterior" direction in the scene view



<img width="500" height="371" alt="image" src="https://github.com/user-attachments/assets/15457804-b8b0-49ba-bf06-1a59701ca3b1" />

Expect this additional window on the right. 



<img src="https://github.com/user-attachments/assets/2bb83f47-0b74-4f42-9518-b0ba570249c9" width="500">  <img src="https://github.com/user-attachments/assets/af98b5fd-e2b3-4df3-88aa-204420ddae5e" width="500">


Expected view for the "jump" and its resolution




<details>	
<summary> Eye model placement code </summary>
	
```python
import slicer
import qt
import numpy as np
import os
import vtk

try:
    import gdown
except ImportError:
    slicer.util.showStatusMessage("Installing 'gdown' package...", 2000)
    slicer.util.pip_install('gdown')
    import gdown

class TrialEyeballPlacementWidget(qt.QWidget):
    def __init__(self, parent=None):
        super(TrialEyeballPlacementWidget, self).__init__(parent)
        self.setup()

    def setup(self):
        self.setLayout(qt.QVBoxLayout())
        
        infoLabel = qt.QLabel("This tool places an eyeball model based on the 'Trial' method geometry.")
        infoLabel.setWordWrap(True)
        self.layout().addWidget(infoLabel)
        
        formLayout = qt.QFormLayout()
        self.sex_combo = qt.QComboBox()
        self.sex_combo.addItems(["Female", "Male"])
        formLayout.addRow("Biological Sex:", self.sex_combo)
        
        self.side_combo = qt.QComboBox()
        self.side_combo.addItems(["Left", "Right"])
        formLayout.addRow("Side:", self.side_combo)
        self.layout().addLayout(formLayout)

        # Prediction method selection (items will be side-specific)
        self.method_group = qt.QGroupBox("Prediction method for soft tissue distances")
        method_layout = qt.QFormLayout(self.method_group)
        
        self.method_L27_label = qt.QLabel("Predict measurement 27 (coronal to lc point):")
        self.method_L33_label = qt.QLabel("Predict measurement 33 (coronal to oa point):")
        self.method_27_combo = qt.QComboBox()
        self.method_33_combo = qt.QComboBox()
        
        method_layout.addRow(self.method_L27_label, self.method_27_combo)
        method_layout.addRow(self.method_L33_label, self.method_33_combo)
        
        self.layout().addWidget(self.method_group)

        self.place_button = qt.QPushButton("Place Eyeball")
        self.place_button.toolTip = "Run the placement based on the selected Sex, Side and prediction methods"
        self.place_button.setStyleSheet("background-color: #A9DFBF; font-weight: bold; padding: 8px;")
        self.layout().addWidget(self.place_button)
        
        self.status_label = qt.QLabel("Ready.")
        self.status_label.setWordWrap(True)
        self.layout().addWidget(self.status_label)
        
        self.layout().addStretch(1)

        # Connections
        self.place_button.clicked.connect(self.run_placement)
        self.side_combo.currentIndexChanged.connect(self.update_prediction_ui)

        # Initial UI update
        self.update_prediction_ui()

    def update_prediction_ui(self):
        """Update labels and combo box items to reflect current side (L or R)."""
        side = self.side_combo.currentText
        side_char = side[0]  # 'L' or 'R'
        
        self.method_L27_label.setText(f"Predict {side_char}27 (coronal to lc point):")
        self.method_L33_label.setText(f"Predict {side_char}33 (coronal to oa point):")
        
        # Store current selection to preserve choice type
        current_27 = self.method_27_combo.currentText
        current_33 = self.method_33_combo.currentText
        
        def get_choice_type(text):
            if text.startswith("Use L") or text.startswith("Use R"):
                return "use_L15" if "L15" in text or "R15" in text else "use_L20"
            return "average"
        
        choice_27 = get_choice_type(current_27) if current_27 else "use_L15"
        choice_33 = get_choice_type(current_33) if current_33 else "use_L15"
        
        new_items = [f"Use {side_char}15", f"Use {side_char}20", f"Average ({side_char}15+{side_char}20)"]
        self.method_27_combo.clear()
        self.method_27_combo.addItems(new_items)
        self.method_33_combo.clear()
        self.method_33_combo.addItems(new_items)
        
        # Restore selection
        self.method_27_combo.setCurrentIndex(0 if choice_27 == "use_L15" else 1 if choice_27 == "use_L20" else 2)
        self.method_33_combo.setCurrentIndex(0 if choice_33 == "use_L15" else 1 if choice_33 == "use_L20" else 2)

    def run_placement(self):
        self.status_label.setText("Starting placement...")
        slicer.app.processEvents()
        
        try:
            SEX = self.sex_combo.currentText
            SIDE = self.side_combo.currentText
            side_char = SIDE[0]
            
            def get_node(name, cls):
                node = slicer.mrmlScene.GetFirstNodeByName(name)
                if not node or not node.IsA(cls):
                    raise ValueError(f"Required node '{name}' of type {cls} not found. Please run the setup script first.")
                return node
            
            def get_line_length(name):
                return get_node(name, "vtkMRMLMarkupsLineNode").GetMeasurement("length").GetValue()

            # Read measurements
            self.status_label.setText(f"1. Reading measurements for {SIDE} side...")
            L1 = get_line_length(f"{side_char}1")
            L8 = get_line_length(f"{side_char}8")
            L15 = get_line_length(f"{side_char}15")
            L20 = get_line_length(f"{side_char}20")

            # L21, L22, L23 from L8 and L1
            if SEX == "Female":
                pred_L21 = 0.349 * L8 + 4.320
                pred_L22 = 0.652 * L8 - 4.353
                pred_L23 = 0.619 * L1 - 2.175
            else:  # Male
                pred_L21 = 0.560 * L8 - 3.648
                pred_L22 = 0.439 * L8 + 3.662
                pred_L23 = 0.844 * L1 - 11.224

            # Predictions from L15 and L20 for 27 and 33
            if SEX == "Female":
                pred27_from_L15 = 1.007 * L15 + 9.552
                pred27_from_L20 = 0.969 * L20 + 5.309
                pred33_from_L15 = 1.005 * L15 + 14.700
                pred33_from_L20 = 1.028 * L20 + 6.826
            else:  # Male
                pred27_from_L15 = 0.989 * L15 + 11.550
                pred27_from_L20 = 0.889 * L20 + 11.756
                pred33_from_L15 = 0.950 * L15 + 19.126
                pred33_from_L20 = 0.865 * L20 + 18.436

            # Apply user method
            method_27_text = self.method_27_combo.currentText
            if "Use R15" in method_27_text or "Use L15" in method_27_text:
                pred27 = pred27_from_L15
            elif "Use R20" in method_27_text or "Use L20" in method_27_text:
                pred27 = pred27_from_L20
            else:
                pred27 = (pred27_from_L15 + pred27_from_L20) / 2.0

            method_33_text = self.method_33_combo.currentText
            if "Use R15" in method_33_text or "Use L15" in method_33_text:
                pred33 = pred33_from_L15
            elif "Use R20" in method_33_text or "Use L20" in method_33_text:
                pred33 = pred33_from_L20
            else:
                pred33 = (pred33_from_L15 + pred33_from_L20) / 2.0

            # Vectors and planes
            vS = np.array(get_node("Orbitale Transverse Plane (Trial)", "vtkMRMLMarkupsPlaneNode").GetNormal())
            vR = np.array(get_node("Median Sagittal Plane (Trial)", "vtkMRMLMarkupsPlaneNode").GetNormal())
            vA = np.array(get_node("Coronal Plane (Trial)", "vtkMRMLMarkupsPlaneNode").GetNormal())

            p_si_1 = np.array(get_node(f"marginal_SOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()) - vS * pred_L21
            p_si_2 = np.array(get_node(f"marginal_IOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()) + vS * pred_L22
            d_si = 0.5 * (np.dot(vS, p_si_1) + np.dot(vS, p_si_2))

            lat_dir = -vR if side_char == "L" else vR
            p_ml = np.array(get_node(f"marginal_MOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()) + lat_dir * pred_L23
            d_ml = np.dot(vR, p_ml)

            p_ap = np.array(get_node("Coronal Plane (Trial)", "vtkMRMLMarkupsPlaneNode").GetOrigin()) + vA * pred33
            d_ap = np.dot(vA, p_ap)

            target_pos = np.linalg.solve(np.array([vS, vR, vA]), np.array([d_si, d_ml, d_ap]))

            # --- Save current camera state ---
            def get_camera_state():
                view = slicer.app.layoutManager().threeDWidget(0).threeDView()
                renderer = view.renderWindow().GetRenderers().GetFirstRenderer()
                cam = renderer.GetActiveCamera()
                return (cam.GetPosition(), cam.GetFocalPoint(), cam.GetViewUp())
            
            camera_state = get_camera_state()

            # Download and place model
            self.status_label.setText("3. Downloading model...")
            IDS = {
                "Female Left": "1k0VSUYA6ZM8ihOS50A69Iah-4SDr4sfu",
                "Female Right": "1boOyC2Z_N0FZT-6F5i3p3ozjJ-8UUUIG",
                "Male Left": "1qpSXWe3c96U0CgxJnUL6-QuSaZfhj6AC",
                "Male Right": "1W-xeGiLqOPitoIWHFOJcjzU5UW7Uyf1s"
            }
            key = f"{SEX} {SIDE}"
            mrb_path = os.path.join(slicer.app.temporaryPath, f"trial_{key.replace(' ','_')}.mrb")
            gdown.download(id=IDS[key], output=mrb_path, quiet=False)
            
            nodes_before = set(slicer.util.getNodesByClass("vtkMRMLNode"))
            slicer.util.loadScene(mrb_path, {"clear": False, "loadCamera": False})
            new_nodes = list(set(slicer.util.getNodesByClass("vtkMRMLNode")) - nodes_before)

            xform_node, oa0_pos = None, None
            for node in new_nodes:
                if node.IsA("vtkMRMLLinearTransformNode"):
                    xform_node = node
                if node.IsA("vtkMRMLMarkupsFiducialNode"):
                    if node.GetControlPointIndexByLabel(f"oa{side_char}") >= 0:
                        p = np.zeros(3)
                        node.GetNthControlPointPositionWorld(node.GetControlPointIndexByLabel(f"oa{side_char}"), p)
                        oa0_pos = p

            if xform_node is None or oa0_pos is None:
                raise ValueError("Could not find model transform or 'oa' landmark.")

            translation = target_pos - oa0_pos
            matrix = vtk.vtkMatrix4x4()
            xform_node.GetMatrixTransformToParent(matrix)
            for i in range(3):
                matrix.SetElement(i, 3, matrix.GetElement(i, 3) + translation[i])
            xform_node.SetMatrixTransformToParent(matrix)

            # Create prediction lines
            def make_pred_line(name, p0, p1, value, color=(0,0,1)):
                ln = slicer.mrmlScene.GetFirstNodeByName(name)
                if not ln:
                    ln = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
                ln.RemoveAllControlPoints()
                ln.AddControlPoint(p0)
                ln.AddControlPoint(p1)
                ln.GetMeasurement("length").SetEnabled(True)
                ln.GetMeasurement("length").SetValue(value)
                d = ln.GetDisplayNode() or ln.CreateDefaultDisplayNodes()
                d.SetColor(color[0], color[1], color[2])
                d.SetSelectedColor(1, 1, 0)
                d.SetVisibility(True)

            coronal_origin = np.array(get_node("Coronal Plane (Trial)", "vtkMRMLMarkupsPlaneNode").GetOrigin())
            p_on_som = target_pos - vS * np.dot(target_pos - np.array(get_node(f"marginal_SOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()), vS)
            p_on_iom = target_pos - vS * np.dot(target_pos - np.array(get_node(f"marginal_IOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()), vS)
            p_on_mom = target_pos - vR * np.dot(target_pos - np.array(get_node(f"marginal_MOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()), vR)
            p_on_coronal = target_pos - vA * np.dot(target_pos - coronal_origin, vA)

            make_pred_line(f"pred_{side_char}21", target_pos, p_on_som, pred_L21)
            make_pred_line(f"pred_{side_char}22", target_pos, p_on_iom, pred_L22)
            make_pred_line(f"pred_{side_char}23", target_pos, p_on_mom, pred_L23)
            make_pred_line(f"pred_{side_char}33", target_pos, p_on_coronal, pred33)
            make_pred_line(f"pred_{side_char}27", target_pos, p_on_coronal, pred27)

            # --- Restore camera state ---
            view = slicer.app.layoutManager().threeDWidget(0).threeDView()
            renderer = view.renderWindow().GetRenderers().GetFirstRenderer()
            cam = renderer.GetActiveCamera()
            pos, fp, up = camera_state
            cam.SetPosition(pos)
            cam.SetFocalPoint(fp)
            cam.SetViewUp(up)
            view.renderWindow().Render()

            final_message = (f"Eyeball placement complete!\n"
                             f"Predicted distances for {SIDE} side:\n"
                             f"{side_char}21 = {pred_L21:.2f} mm\n"
                             f"{side_char}22 = {pred_L22:.2f} mm\n"
                             f"{side_char}23 = {pred_L23:.2f} mm\n"
                             f"{side_char}27 = {pred27:.2f} mm (method: {method_27_text})\n"
                             f"{side_char}33 = {pred33:.2f} mm (method: {method_33_text})")
            self.status_label.setText(final_message)
            slicer.util.infoDisplay(final_message)

        except Exception as e:
            self.status_label.setText(f"ERROR: {e}")
            slicer.util.errorDisplay(f"An error occurred: {e}")
            raise e

# Cleanup and instantiation
try:
    if 'trial_placement_widget' in globals() and trial_placement_widget:
        trial_placement_widget.parent().close()
except NameError:
    pass

trial_placement_widget = TrialEyeballPlacementWidget()
dock_widget = qt.QDockWidget("Trial Eyeball Placement")
dock_widget.setWidget(trial_placement_widget)
slicer.util.mainWindow().addDockWidget(qt.Qt.RightDockWidgetArea, dock_widget)

```

</details>

<img width="868" height="954" alt="image" src="https://github.com/user-attachments/assets/bd3b313c-576a-44f0-a307-7b4f433a331a" />


View after placing both eyeballs


### Validating the original study
If you wanted to use this this tool for an approximation, you're done!

Additionally, we can compare the predicted and the actual eyeball positions via landmarks, by placing the soft tissue landmarks denoted with a blue square in the previous section "Landmarks in this study". 
You can download them [here](https://github.com/user-attachments/files/27196663/Ryu_soft_tissue.mrk.json).

Once you placed the "ground truth" landmarks (called true_eyeball.lmrk.json) onto the scan (you'll likely have to use the red/green/yellow windows for a more precise placement), you can run the code below. 

It will create two comparison tables: (1) for comparing length measurements between the "artificial" eyeball model and the true eyeball that were measured by Guyomarc'h et al. (2012)[^2] in the original studt to create the regressions; (2) for measuring the distance between the true vs artificial eyeball landmarks. 


<details>	
<summary> Additional hard tissue measurements </summary>
	
```python


```

</details>


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
