# Code for opening the .OBJ file

As soon as the 3D Slicer loaded, copy and paste the script below. The model should load as yellow first, then change into the one texture. 
Sadly, even if we save the scene, it does not automatically re-applies it, so this is the most efficient way of showing participants the bones. No point in saving the scene, but no data is lost. 

```python
import os
import slicer
import vtk
from qt import QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget

class LoadTexturedModelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load Textured Model")
        self.setMinimumWidth(400)
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.infoLabel = QLabel("Pick a folder containing your OBJ, MTL, and texture image.")
        self.mainLayout.addWidget(self.infoLabel)
        
        self.pickFolderButton = QPushButton("Select Model Folder")
        self.mainLayout.addWidget(self.pickFolderButton)
        self.pickFolderButton.clicked.connect(self.pickFolder)
        
        self.statusLabel = QLabel("")
        self.mainLayout.addWidget(self.statusLabel)
        
    def pickFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            self.statusLabel.setText("No folder selected.")
            return
        
        self.statusLabel.setText(f"Loading from:\n{folder}")
        self.loadModelWithTexture(folder)
    
    def loadModelWithTexture(self, folder):
        # Find OBJ file
        obj_files = [f for f in os.listdir(folder) if f.lower().endswith('.obj')]
        if not obj_files:
            self.statusLabel.setText("No OBJ file found in folder.")
            return
        obj_file = obj_files[0]
        obj_path = os.path.join(folder, obj_file)
        
        # Find MTL file
        mtl_files = [f for f in os.listdir(folder) if f.lower().endswith('.mtl')]
        if not mtl_files:
            self.statusLabel.setText("No MTL file found in folder.")
            return
        mtl_file = mtl_files[0]
        mtl_path = os.path.join(folder, mtl_file)
        
        # Parse texture filename from MTL
        texture_filename = None
        with open(mtl_path, "r") as f:
            for line in f:
                if line.strip():
                    if line.strip().startswith("map_Kd"):
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) == 2:
                            texture_filename = parts[1]
                            break
        if not texture_filename:
            self.statusLabel.setText("No texture file referenced in MTL file.")
            return
        texture_path = os.path.join(folder, texture_filename)
        if not os.path.exists(texture_path):
            self.statusLabel.setText(f"Texture file {texture_filename} not found in folder.")
            return
        
        # Load OBJ as model
        model_node = slicer.util.loadModel(obj_path)
        if model_node is None:
            self.statusLabel.setText("Failed to load OBJ model.")
            return
        
        # Load texture as volume node
        vectorVolNode = slicer.util.loadVolume(texture_path)
        if vectorVolNode is None:
            self.statusLabel.setText("Failed to load texture image.")
            return
        
        # Apply texture
        modelDisplayNode = model_node.GetDisplayNode()
        modelDisplayNode.SetBackfaceCulling(0)
        textureImageFlipVert = vtk.vtkImageFlip()
        textureImageFlipVert.SetFilteredAxis(1)
        textureImageFlipVert.SetInputConnection(vectorVolNode.GetImageDataConnection())
        modelDisplayNode.SetTextureImageDataConnection(textureImageFlipVert.GetOutputPort())
        
        self.statusLabel.setText("Model and texture loaded!")

# Create and show the widget in Slicer
try:
    loadWidget.close()
except:
    pass
loadWidget = LoadTexturedModelWidget()
loadWidget.show()
```


CAN YOU TRY THIS ONE?

## How to Use This Script in 3D Slicer
Open 3D Slicer
Press Ctrl+3 to open the Python Interactor
Copy and paste the script above
Press Enter to execute

# Common Issues for Beginners
## File Format Compatibility: Not all texture formats work well with Slicer. JPG and PNG usually work best.

## Path Issues: Make sure your OBJ, MTL, and texture files are all in the same folder.

## Python Console Errors: If you get an error, look at the Python console (Ctrl+3) for more details about what went wrong.

## Qt Imports: Different versions of Slicer may require different Qt import statements.

```python
import os
import slicer
import vtk
from PythonQt import QtWidgets  # This is more reliable in Slicer

class LoadTexturedModelWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load Textured Model")
        self.setMinimumWidth(400)
        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.infoLabel = QtWidgets.QLabel("Pick a folder containing your OBJ, MTL, and texture image.")
        self.mainLayout.addWidget(self.infoLabel)
        
        self.pickFolderButton = QtWidgets.QPushButton("Select Model Folder")
        self.mainLayout.addWidget(self.pickFolderButton)
        self.pickFolderButton.clicked.connect(self.pickFolder)
        
        self.statusLabel = QtWidgets.QLabel("")
        self.mainLayout.addWidget(self.statusLabel)
        
    def pickFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            self.statusLabel.setText("No folder selected.")
            return
        
        self.statusLabel.setText(f"Loading from:\n{folder}")
        self.loadModelWithTexture(folder)
    
    def loadModelWithTexture(self, folder):
        # Find OBJ file
        obj_files = [f for f in os.listdir(folder) if f.lower().endswith('.obj')]
        if not obj_files:
            self.statusLabel.setText("No OBJ file found in folder.")
            return
        obj_file = obj_files[0]
        obj_path = os.path.join(folder, obj_file)
        
        # Find MTL file
        mtl_files = [f for f in os.listdir(folder) if f.lower().endswith('.mtl')]
        if not mtl_files:
            self.statusLabel.setText("No MTL file found in folder.")
            return
        mtl_file = mtl_files[0]
        mtl_path = os.path.join(folder, mtl_file)
        
        # Parse texture filename from MTL
        texture_filename = None
        with open(mtl_path, "r") as f:
            for line in f:
                if line.strip():
                    if line.strip().startswith("map_Kd"):
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) == 2:
                            texture_filename = parts[1]
                            break
        if not texture_filename:
            self.statusLabel.setText("No texture file referenced in MTL file.")
            return
        texture_path = os.path.join(folder, texture_filename)
        if not os.path.exists(texture_path):
            self.statusLabel.setText(f"Texture file {texture_filename} not found in folder.")
            return
        
        # Load OBJ as model
        model_node = slicer.util.loadModel(obj_path)
        if model_node is None:
            self.statusLabel.setText("Failed to load OBJ model.")
            return
            
        # Try different methods to load texture
        try:
            # Method 1: Try to load as volume
            vectorVolNode = slicer.util.loadVolume(texture_path, {"singleFile": True})
            if vectorVolNode:
                # Apply texture
                modelDisplayNode = model_node.GetDisplayNode()
                modelDisplayNode.SetBackfaceCulling(0)
                textureImageFlipVert = vtk.vtkImageFlip()
                textureImageFlipVert.SetFilteredAxis(1)
                textureImageFlipVert.SetInputConnection(vectorVolNode.GetImageDataConnection())
                modelDisplayNode.SetTextureImageDataConnection(textureImageFlipVert.GetOutputPort())
                self.statusLabel.setText("Model and texture loaded!")
            else:
                self.statusLabel.setText("Could not load texture as volume. Try a different format.")
        except Exception as e:
            self.statusLabel.setText(f"Error loading texture: {str(e)}")

# Create and show the widget in Slicer
widget_name = "loadTexturedModelWidget"

# Try to close existing widget if it exists
if hasattr(slicer.modules, widget_name):
    try:
        getattr(slicer.modules, widget_name).close()
    except:
        pass

# Create new widget and store reference
widget = LoadTexturedModelWidget()
setattr(slicer.modules, widget_name, widget)
widget.show()
```
