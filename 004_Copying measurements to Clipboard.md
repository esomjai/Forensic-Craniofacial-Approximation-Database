## Content Summary
- [When is this step relevant?](#when-is-this-step-relevant)
- [What does the code do and what’s the output?](#what-does-the-code-do-and-whats-the-output)
- [Code to copy linear measurements](#code-to-copy-linear-measurements)
- [Code to copy angle measurements](#code-to-copy-angle-measurements)

### When is this step relevant?
This will be important when all your measurements are done in the environment and you need to collate them. 

Unfortunately, there are only options for copying one type of measurement and ALL of them at one time, but if there are pseudo-measurements (I call the additional lines that actually not measure anything, but are connecting structures, or are used intermediately for other measurements), these will be highlighted and mentioned in the tutorial. 

### What does the code do and what’s the output?
There will be two codes provided in this guide, one of them is specifically for linear and the other is for angle measurements. These codes copy ALL linear or ALL angle measurements present in the environment that you created in the **Markup**s module to the clipboard, with the patient ID, the name of the measurement and its numerical value. The default measurements are in mm and degrees. 

The code snippets create shortcuts that need to be re-established every time you close Slicer – Repository of the official 3D Slicer site has an option to save the function. 

Then, when pressing the buttons for the shortcut, a pop-up message will tell you how many measurements were copied as a conformation for you that the code worked. Now, you can go to your Excel worksheet and paste the values. 

Initially, it will look something like this:

(unknown) | sellions | 13.00624
-- | -- | --
(unknown) | SN line | 300
(unknown) | height of apertura piriformis rhi-aca | 37.81184
(unknown) | 2 INB proj | 37.80521
(unknown) | height of the bony nose nas-aca | 53.58975
(unknown) | 3 INB proj | 53.58588
(unknown) | P parallel | 200
(unknown) | P parallel proj | 199.9997
(unknown) | rhi parallel | 200
(unknown) | rhi parallel proj | 199.9997
(unknown) | 5 P max proj | 14.30314
(unknown) | 7 height of rhinion | 16.57942
(unknown) | 6 prominence of rhinion in relation to the n-aca plane | 8.777521
(unknown) | 4 P max | 8.010799
(unknown) | 9 angle between plane n-aca and rhi-aca plane | 13.37417

The first column will show a lot of “unknown” – this may be due to the Patient ID missing/anonymised or entered in the wrong column at the CT scan acquisition. I usually replace these with the ID of the individual in the study I am replicating – good for record keeping as well in case a participant wishes to withdraw from the research for any reason.

The second column will be the “given name” – this is something you either do manually, or is included in certain types of code to identify which measurement you took. 

The third column is the measurement made in Slicer based on the coordinates in mm up to 5 decimal places. 

The measurements in italics are examples of pseudo/secondary measurements where their length was programmed as it is not relevant or they take part in establishing another, relevant measurement. These will always be mentioned and flagged it the tutorials to prevent confusion and hyperinflating data.  

### Code to copy linear measurements

```python
def createMeasurements():
  for nodeName in []:
    lineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", nodeName)
    lineNode.CreateDefaultDisplayNodes()
    dn = lineNode.GetDisplayNode()
    # Use crosshair glyph to allow more accurate point placement
    dn.SetGlyphTypeFromString("CrossDot2D")
    # Hide measurement result while markup up
    lineNode.GetMeasurement('length').SetEnabled(False)

shortcut1 = qt.QShortcut(slicer.util.mainWindow())
shortcut1.setKey(qt.QKeySequence("Ctrl+n"))
shortcut1.connect('activated()', createMeasurements)

def copyLineMeasurementsToClipboard():
  measurements = []
  # Collect all line measurements from the scene
  lineNodes = getNodesByClass('vtkMRMLMarkupsLineNode')
  for lineNode in lineNodes:
    if lineNode.GetNumberOfDefinedControlPoints() < 2:
      # incomplete line, skip it
      continue
    # Get node filename that the length was measured on
    try:
      volumeNode = slicer.mrmlScene.GetNodeByID(lineNode.GetNthControlPointAssociatedNodeID(0))
      imagePath = volumeNode.GetStorageNode().GetFileName()
    except:
      imagePath = '(unknown)'
    # Get line node n
    measurementName = lineNode.GetName()
    # Get length measurement
    lineNode.GetMeasurement('length').SetEnabled(True)
    length = str(lineNode.GetMeasurement('length').GetValue())
    # Add fields to results
    measurements.append('\t'.join([imagePath, measurementName, length]))
  # Copy all measurements to clipboard (to be pasted into Excel)
  outputText = "\n".join(measurements) + "\n"
  slicer.app.clipboard().setText(outputText)
  slicer.util.delayDisplay(f"Copied {len(measurements)} length measurements to the clipboard.")

2 = qt.QShortcut(slicer.util.mainWindow())
shortcut2.setKey(qt.QKeySequence("Ctrl+m"))
shortcut2.connect('activated()', copyLineMeasurementsToClipboard)
```

###  Code to copy angle measurements

After copy+pasting this into the python console in Slicer and pressing Enter, the shortcut Ctrl+T should result in a pop-up message stating the number of measurements copied.


```python
def copyAngleMeasurementsToClipboard():
  measurements = []
  # Collect all line measurements from the scene
  angleNodes = getNodesByClass('vtkMRMLMarkupsAngleNode')
  for angleNode in angleNodes:
    if angleNode.GetNumberOfDefinedControlPoints() < 3:
      # incomplete line, skip it
      continue
    # Get node filename that the length was measured on
    try:
      volumeNode = slicer.mrmlScene.GetNodeByID(angleNode.GetNthControlPointAssociatedNodeID(0))
      imagePath = volumeNode.GetStorageNode().GetFileName()
    except:
      imagePath = '(unknown)'
    # Get angle node n
    measurementName = angleNode.GetName()
    # Get angle measurement
    angleNode.GetMeasurement('angle').SetEnabled(True)
    angle = str(angleNode.GetMeasurement('angle').GetValue())
    # Add fields to results
    measurements.append('\t'.join([imagePath, measurementName, angle]))
  # Copy all measurements to clipboard (to be pasted into Excel)
  outputText = "\n".join(measurements) + "\n"
  slicer.app.clipboard().setText(outputText)
  slicer.util.delayDisplay(f"Copied {len(measurements)} angle measurements to the clipboard.")

shortcut2 = qt.QShortcut(slicer.util.mainWindow())
shortcut2.setKey(qt.QKeySequence("Ctrl+t"))
shortcut2.connect( 'activated()', copyAngleMeasurementsToClipboard)
```



