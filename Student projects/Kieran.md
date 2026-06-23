[Right Ramus Breadth.mrk.json](https://github.com/user-attachments/files/29254437/Right.Ramus.Breadth.mrk.json)


[Right Minimum zygomatic thickness.mrk.json](https://github.com/user-attachments/files/29254436/Right.Minimum.zygomatic.thickness.mrk.json)


[Right Maximum zygomatic thickness.mrk.json](https://github.com/user-attachments/files/29254435/Right.Maximum.zygomatic.thickness.mrk.json)


[Left Ramus Breadth.mrk.json](https://github.com/user-attachments/files/29254434/Left.Ramus.Breadth.mrk.json)


[Left Minimum zygomatic thickness.mrk.json](https://github.com/user-attachments/files/29254432/Left.Minimum.zygomatic.thickness.mrk.json)


[Left Maximum zygomatic thickness.mrk.json](https://github.com/user-attachments/files/29254431/Left.Maximum.zygomatic.thickness.mrk.json)


[landmarks.mrk.json](https://github.com/user-attachments/files/29254430/landmarks.mrk.json)

```python
"""
Mandibular and Cranial Measurements GUI for 3D Slicer
Copy-paste this entire script into the 3D Slicer Python Interactor and run.

Workflow (beginner-friendly):
1) Download + load landmarks.json (for landmark placement/measurements)
2) Create empty manual line measurements using your provided .mrk.json templates + descriptions
3) Create automatic linear measurements (label-based)
4) Copy linear measurements OR angle measurements to clipboard using buttons (paste into Excel)

Notes:
- This script assumes the correct fiducial list is found by checking that it contains expected labels,
  so it works even if multiple markups fiducial lists exist in the scene.
"""

import os
import urllib.request
import numpy as np
import vtk
import qt
import slicer

# ============================================================
# URLs (updated with your new file links)
# ============================================================

ANATOMICAL_LANDMARKS_URL = "https://github.com/user-attachments/files/29254430/landmarks.mrk.json"

MANUAL_TEMPLATE_URLS = {
    "L Maximum Zygomatic Thickness": "https://github.com/user-attachments/files/29254431/Left.Maximum.zygomatic.thickness.mrk.json",
    "L Minimum Zygomatic Thickness": "https://github.com/user-attachments/files/29254432/Left.Minimum.zygomatic.thickness.mrk.json",
    "R Maximum Zygomatic Thickness": "https://github.com/user-attachments/files/29254435/Right.Maximum.zygomatic.thickness.mrk.json",
    "R Minimum Zygomatic Thickness": "https://github.com/user-attachments/files/29254436/Right.Minimum.zygomatic.thickness.mrk.json",
    "L Ramus Breadth": "https://github.com/user-attachments/files/29254434/Left.Ramus.Breadth.mrk.json",
    "R Ramus Breadth": "https://github.com/user-attachments/files/29254437/Right.Ramus.Breadth.mrk.json",
}

MANUAL_DESCRIPTIONS = {
    "R Maximum Zygomatic Thickness": "The thickest point of the RIGHT zygomatic arch",
    "R Minimum Zygomatic Thickness": "The narrowest point of the RIGHT zygomatic arch.",
    "L Maximum Zygomatic Thickness": "The thickest point of the LEFT zygomatic arch",
    "L Minimum Zygomatic Thickness": "The narrowest point of the LEFT zygomatic arch.",
    "L Ramus Breadth": "The narrowest point of the LEFT ramus of the mandible.",
    "R Ramus Breadth": "The narrowest point of the RIGHT ramus of the mandible.",
}

# ============================================================
# Helper functions
# ============================================================

def download_file(url, filename):
    tempDir = qt.QStandardPaths.writableLocation(qt.QStandardPaths.TempLocation)
    filepath = os.path.join(tempDir, filename)
    slicer.util.delayDisplay(f"Downloading {filename} ...")
    urllib.request.urlretrieve(url, filepath)
    return filepath

def find_fiducial_node_with_labels(required_labels):
    """Return the first fiducial node that contains ALL required_labels."""
    nodes = slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode")
    for n in nodes:
        labels = set(n.GetNthControlPointLabel(i) for i in range(n.GetNumberOfControlPoints()))
        if all(lbl in labels for lbl in required_labels):
            return n
    return None

def get_landmark_point(markups_node, label):
    idx = markups_node.GetControlPointIndexByLabel(label)
    if idx < 0:
        print(f"Warning: landmark '{label}' not found in node '{markups_node.GetName()}'")
        return None
    return markups_node.GetNthControlPointPositionVector(idx)

# ============================================================
# Step 1: Load anatomical landmarks
# ============================================================

def download_and_load_anatomical_landmarks():
    try:
        path = download_file(ANATOMICAL_LANDMARKS_URL, "landmarks.mrk.json")
        slicer.util.loadMarkups(path)
        slicer.util.delayDisplay("Loaded landmarks.mrk.json. Place/verify landmarks, then create measurements.")
    except Exception as e:
        slicer.util.errorDisplay(f"Failed to download/load landmarks.mrk.json:\n{e}")

# ============================================================
# Step 2: Create empty manual measurement nodes
# ============================================================

def create_empty_manual_measurement_nodes():
    """
    Creates empty manual line measurement nodes using the provided templates
    """
    try:
        manualMeasurements = [
            ("R Maximum Zygomatic Thickness", "The thickest point of the RIGHT zygomatic arch"),
            ("R Minimum Zygomatic Thickness", "The narrowest point of the RIGHT zygomatic arch."),
            ("L Maximum Zygomatic Thickness", "The thickest point of the LEFT zygomatic arch"),
            ("L Minimum Zygomatic Thickness", "The narrowest point of the LEFT zygomatic arch."),
            ("L Ramus Breadth", "The narrowest point of the LEFT ramus of the mandible."),
            ("R Ramus Breadth", "The narrowest point of the RIGHT ramus of the mandible."),
        ]

        # Index existing line nodes by name
        existing = {n.GetName(): n for n in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode")}

        created = 0
        reused = 0

        for name, desc in manualMeasurements:
            lineNode = existing.get(name)
            if not lineNode:
                lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode")
                lineNode.SetName(name)
                created += 1
            else:
                reused += 1

            # Ensure the line is EMPTY (remove any existing control points)
            for i in range(lineNode.GetNumberOfControlPoints() - 1, -1, -1):
                lineNode.RemoveNthControlPoint(i)

            # Set description
            try:
                lineNode.SetDescription(desc)
            except Exception:
                pass

            # Improve usability
            lineNode.CreateDefaultDisplayNodes()
            dn = lineNode.GetDisplayNode()
            if dn:
                dn.SetGlyphTypeFromString("CrossDot2D")
                dn.SetPointLabelsVisibility(False)
                dn.SetPropertiesLabelVisibility(True)

            # Hide measurement result until 2 points are placed
            try:
                lineNode.GetMeasurement("length").SetEnabled(False)
            except Exception:
                pass

        slicer.util.delayDisplay(
            f"Manual measurement line nodes ready.\n"
            f"Created: {created}, already existed: {reused}\n"
            "Now place 2 points on each line in the Markups module."
        )

    except Exception as e:
        slicer.util.errorDisplay(f"Failed to create manual measurement nodes:\n{e}")

# ============================================================
# Step 3: Automatic linear measurements (label-based)
# ============================================================

def create_linear_measurements():
    
    try:
        # First, list all fiducial nodes to help debug
        print("Available fiducial nodes:")
        nodes = slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode")
        for n in nodes:
            print(f"  - {n.GetName()} ({n.GetNumberOfControlPoints()} points)")
            labels = [n.GetNthControlPointLabel(i) for i in range(n.GetNumberOfControlPoints())]
            print(f"    Labels: {labels}")
        
        # Prefer the node named exactly 'landmarks'
        try:
            F = slicer.util.getNode("landmarks")
            print(f"Found node named 'landmarks'")
        except slicer.util.MRMLNodeNotFoundException:
            F = None
            print("No node named 'landmarks' found")

        # Fallback: try to find a fiducial list that looks like the anatomical list
        if not F:
            F = find_fiducial_node_with_labels(["g", "gn", "id", "n", "pr", "zyL", "zyR"])
            if F:
                print(f"Found fallback node: {F.GetName()}")
            else:
                print("No fallback node found")

        if not F:
            slicer.util.errorDisplay(
                "Could not find the anatomical landmarks node.\n"
                "Please load landmarks.mrk.json and make sure the node is named 'landmarks'."
            )
            return

        if F.GetClassName() != "vtkMRMLMarkupsFiducialNode":
            slicer.util.errorDisplay(f"Node 'landmarks' is not a fiducial list (it is {F.GetClassName()}).")
            return

        # Print all available labels in the found node
        print(f"Available labels in {F.GetName()}:")
        labels = [F.GetNthControlPointLabel(i) for i in range(F.GetNumberOfControlPoints())]
        print(f"  {labels}")

        # Updated measurements list based on your specifications
        measurements = [
            # Cranial measurements
            ("Maximum Cranial Length", "g", "op"),
            ("Bizygomatic Breadth", "zyR", "zyL"),
            ("Superior Facial Height", "n", "pr"),
            ("Facial Length", "ba", "pr"),
            ("Basion-bregmatic height", "ba", "b"),
            
            # Palatal
            ("Palatal Length", "ol", "pns"),
            
            # Mandibular measurements
            ("Bicondylar Breadth", "kdlR", "kdlL"),
            ("Muscular process breadth", "krL", "krR"),
            ("Bigonial Breadth", "goR", "goL"),
            ("Anterior Height", "id", "gn"),
            
            # Ramus and condylar measurements
            ("Left Ramus height", "kdsL", "goL"),
            ("Right Ramus height", "kdsR", "goR"),
            ("Left Condylar height", "kdsL", "irbL"),
            ("Right Condylar height", "kdsR", "irbR"),
            
            # Temporal fossa
            ("Intertemporal fossa distance", "itR", "itL"),
            
            # Corpus length measurements
            ("Left Corpus length", "kdpL", "irbL"),
            ("Right Corpus length", "kdpR", "irbR"),
        ]

        created = 0
        skipped = 0
        missing_labels = []

        for name, a, b in measurements:
            p1 = get_landmark_point(F, a)
            p2 = get_landmark_point(F, b)
            if p1 is None or p2 is None:
                skipped += 1
                if p1 is None:
                    missing_labels.append(a)
                if p2 is None:
                    missing_labels.append(b)
                continue

            lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode")
            lineNode.SetName(name)
            lineNode.AddControlPoint(p1)
            lineNode.AddControlPoint(p2)

            try:
                lineNode.GetMeasurement("length").SetEnabled(False)
            except Exception:
                pass

            created += 1

        # Mandibular body length: midpoint(goL, goR) to pog
        goL = get_landmark_point(F, "goL")
        goR = get_landmark_point(F, "goR")
        pog = get_landmark_point(F, "pog")

        if goL is not None and goR is not None and pog is not None:
            midpoint = [
                (goL[0] + goR[0]) / 2,
                (goL[1] + goR[1]) / 2,
                (goL[2] + goR[2]) / 2,
            ]

            # Create midpoint as fiducial (hidden using display node)
            midNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
            midNode.SetName("goR goL midpoint")
            midNode.AddControlPoint(midpoint[0], midpoint[1], midpoint[2])
            # Hide the node using its display node
            midNode.CreateDefaultDisplayNodes()
            displayNode = midNode.GetDisplayNode()
            if displayNode:
                displayNode.SetVisibility(False)

            lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode")
            lineNode.SetName("Mandibular body length")
            lineNode.AddControlPoint(pog)
            lineNode.AddControlPoint(midpoint)
            created += 1
        else:
            skipped += 1
            if goL is None:
                missing_labels.append("goL")
            if goR is None:
                missing_labels.append("goR")
            if pog is None:
                missing_labels.append("pog")

        # Show warning about missing labels
        if missing_labels:
            unique_missing = sorted(set(missing_labels))
            slicer.util.delayDisplay(
                f"Created {created} automatic linear measurement line nodes.\n"
                f"Skipped {skipped} (missing landmarks).\n\n"
                f"Missing landmark labels: {', '.join(unique_missing)}\n"
                f"Please ensure these landmarks are placed in the landmarks node."
            )
        else:
            slicer.util.delayDisplay(
                f"Created {created} automatic linear measurement line nodes.\n"
                f"Skipped {skipped} (missing landmarks)."
            )

    except Exception as e:
        slicer.util.errorDisplay(f"Failed to create linear measurements:\n{e}")

# ============================================================
# Step 4: Copy buttons
# ============================================================

def copy_linear_measurements_to_clipboard():
    try:
        rows = []
        lineNodes = slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode")

        for lineNode in lineNodes:
            if lineNode.GetNumberOfDefinedControlPoints() < 2:
                continue

            try:
                lineNode.GetMeasurement("length").SetEnabled(True)
                length = lineNode.GetMeasurement("length").GetValue()
            except Exception:
                continue

            imagePath = "(unknown)"
            try:
                assocId = lineNode.GetNthControlPointAssociatedNodeID(0)
                volumeNode = slicer.mrmlScene.GetNodeByID(assocId) if assocId else None
                if volumeNode and volumeNode.GetStorageNode():
                    imagePath = volumeNode.GetStorageNode().GetFileName()
            except Exception:
                pass

            rows.append("\t".join([imagePath, lineNode.GetName(), f"{length}"]))

        slicer.app.clipboard().setText("\n".join(rows) + "\n")
        slicer.util.delayDisplay(f"Copied {len(rows)} linear measurements to clipboard.")
    except Exception as e:
        slicer.util.errorDisplay(f"Failed to copy linear measurements:\n{e}")

# ============================================================
# GUI window
# ============================================================

def build_gui():
    global mandibular_cranial_gui_window

    mandibular_cranial_gui_window = qt.QWidget()
    mandibular_cranial_gui_window.setWindowTitle("Mandibular and Cranial Measurements")
    mandibular_cranial_gui_window.setMinimumWidth(860)
    mandibular_cranial_gui_window.setMinimumHeight(920)

    layout = qt.QVBoxLayout(mandibular_cranial_gui_window)

    layout.addWidget(qt.QLabel("<h2>Mandibular and Cranial Measurements</h2>"))
    intro = qt.QLabel(
        "Follow the steps in order. If something is missing, check that the correct landmarks are placed.\n"
        "When finished, use the Copy buttons to paste results into Excel."
    )
    intro.setWordWrap(True)
    layout.addWidget(intro)

    # Step 1
    g1 = qt.QGroupBox("Step 1: Download + load anatomical landmarks (landmarks.mrk.json)")
    g1l = qt.QVBoxLayout(g1)
    b1 = qt.QPushButton("Download + Load landmarks.mrk.json")
    b1.clicked.connect(download_and_load_anatomical_landmarks)
    g1l.addWidget(b1)
    layout.addWidget(g1)

    # Step 2: Manual measurements
    g2 = qt.QGroupBox("Step 2: Create empty manual measurement line nodes")
    g2l = qt.QVBoxLayout(g2)
    
    b_manual = qt.QPushButton("Create empty manual measurement line nodes (with descriptions)")
    b_manual.clicked.connect(create_empty_manual_measurement_nodes)
    g2l.addWidget(b_manual)

    manualText = qt.QLabel(
        "Manual lines to fill (place 2 points each):\n"
        "• R Maximum Zygomatic Thickness\n"
        "• R Minimum Zygomatic Thickness\n"
        "• L Maximum Zygomatic Thickness\n"
        "• L Minimum Zygomatic Thickness\n"
        "• L Ramus Breadth\n"
        "• R Ramus Breadth"
    )
    manualText.setWordWrap(True)
    g2l.addWidget(manualText)
    layout.addWidget(g2)

    # Step 3: Automatic linear measurements
    g3 = qt.QGroupBox("Step 3: Automatic linear measurements")
    g3l = qt.QVBoxLayout(g3)
    b3 = qt.QPushButton("Create automatic linear measurements (lines)")
    b3.clicked.connect(create_linear_measurements)
    g3l.addWidget(b3)

    autoText = qt.QLabel(
        "Automatic measurements created:\n"
        "• Maximum Cranial Length (g-op)\n"
        "• Bizygomatic Breadth (zyR-zyL)\n"
        "• Superior Facial Height (n-pr)\n"
        "• Facial Length (ba-pr)\n"
        "• Basion-bregmatic height (ba-b)\n"
        "• Palatal Length (ol-pns)\n"
        "• Bicondylar Breadth (kdlR-kdlL)\n"
        "• Muscular process breadth (krL-krR)\n"
        "• Bigonial Breadth (goR-goL)\n"
        "• Anterior Height (id-gn)\n"
        "• Left Ramus height (kdsL-goL)\n"
        "• Right Ramus height (kdsR-goR)\n"
        "• Left Condylar height (kdsL-irbL)\n"
        "• Right Condylar height (kdsR-irbR)\n"
        "• Intertemporal fossa distance (itR-itL)\n"
        "• Left Corpus length (kdpL-irbL)\n"
        "• Right Corpus length (kdpR-irbR)\n"
        "• Mandibular body length (midpoint goL-goR to pog)"
    )
    autoText.setWordWrap(True)
    g3l.addWidget(autoText)
    layout.addWidget(g3)

    # Step 4: Copy buttons
    g4 = qt.QGroupBox("Step 4: Copy measurements to clipboard (paste into Excel)")
    g4l = qt.QVBoxLayout(g4)
    row = qt.QHBoxLayout()

    c1 = qt.QPushButton("Copy linear measurements")
    c1.clicked.connect(copy_linear_measurements_to_clipboard)
    row.addWidget(c1)

    g4l.addLayout(row)
    layout.addWidget(g4)

    layout.addStretch(1)
    mandibular_cranial_gui_window.show()

# Run
build_gui()
```


