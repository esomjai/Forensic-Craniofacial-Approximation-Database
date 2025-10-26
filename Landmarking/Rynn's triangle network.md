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
    projectedPoint = point - distanceToPlane * planeNormal
    return projectedPoint


projectedStartPoint = project_point_onto_plane(startPoint, planeOrigin, planeNormal)
projectedEndPoint = project_point_onto_plane(endPoint, planeOrigin, planeNormal)


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8R ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8R')


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


projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8R vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#####################################################################################
#pt8L#
F=getNode('Rynn_hard_tissue')  
G=getNode('Rynn_soft_tissue') 
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(0)     #nasion#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(18)	#Rynn_soft_tissue point#
L.AddControlPoint(secondPoint)
L.SetName('n-pt8L')

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8L')
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
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8L lat')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(1, 1, 0)  # RGB values for yellow

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8L')

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

projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8L ant')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 1, 0)  # RGB values for green

import numpy as np
import slicer

originalLineNode = slicer.util.getNode('n-pt8L')

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
projectedLineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'pt8L vert')
projectedLineNode.AddControlPoint(projectedStartPoint)
projectedLineNode.AddControlPoint(projectedEndPoint)

projectedLineNode.GetDisplayNode().SetSelectedColor(0, 0, 1)  # RGB values for blue

#Create PLB point by connecting XR and XL, then finding its intersection with the INB#
import slicer
import numpy as np

# 1. Get the fiducial node with landmarks
F = slicer.util.getNode('Rynn_hard_tissue')

# 2. Get the XL and XR points (as numpy arrays)
pointXL = np.array(F.GetNthControlPointPositionVector(10))
pointXR = np.array(F.GetNthControlPointPositionVector(9))

# 3. (Optional) Create the line node "XL-XR" (not strictly needed for intersection math)
# You can create it if you want to check, but you don't need to visualize or keep it
L = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', 'XL-XR')
L.AddControlPoint(pointXL)
L.AddControlPoint(pointXR)

# 4. Get the plane node "INB"
planeNode = slicer.util.getNode("INB")
planeOrigin = np.array(planeNode.GetOrigin())
planeNormal = np.array(planeNode.GetNormal())

# 5. Calculate the intersection point (standard line-plane intersection math)
lineDir = pointXR - pointXL
ndotu = planeNormal.dot(lineDir)
if abs(ndotu) < 1e-6:
    raise Exception("Line and plane are parallel and do not intersect.")

w = pointXL - planeOrigin
si = -planeNormal.dot(w) / ndotu
intersection = pointXL + si * lineDir

# 6. Save the intersection as a new point node "PLB"
plbNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "PLB")
plbNode.AddControlPoint(intersection.tolist())

# 7. (Optional) Remove the temporary "XL-XR" line node so it's not displayed
slicer.mrmlScene.RemoveNode(L)

print("Intersection point 'PLB' created at:", intersection)

###rhinion-PLB(XL/XR)-acanthion angle	soft tissue nasion-pronasale-subnasale angle###
import slicer
import numpy as np

# Get the nodes for the existing points and lines
hardTissueNode = slicer.util.getNode('Rynn_soft_tissue')
PLBnode=slicer.util.getNode('PLB')

# Get the positions of the control points
apexPoint = np.array(hardTissueNode.GetNthControlPointPosition(5))
firstControlPoint = np.array(PLBnode.GetNthControlPointPosition(0))
thirdControlPoint = np.array(hardTissueNode.GetNthControlPointPosition(6))

# Create the angle node
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', 'rhi-PLB-aca')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Second control point (apex)
angleNode.AddControlPoint(thirdControlPoint)  # Third control point

print("New angle 'rhi-PLB-aca' created successfully.")


###original soft tissue nasion-pronasale-subnasale angle###
import slicer
import numpy as np

softTissueNode = slicer.util.getNode('Rynn_soft_tissue')

apexPoint = np.array(softTissueNode.GetNthControlPointPosition(0))
firstControlPoint = np.array(softTissueNode.GetNthControlPointPosition(2))
thirdControlPoint = np.array(softTissueNode.GetNthControlPointPosition(1))

# Manually define the labels for the node name
pn = "pronasale"
sn = "subnasale"
angleNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', f'n-{pn}-{sn}')
angleNode.AddControlPoint(firstControlPoint)  # First control point
angleNode.AddControlPoint(apexPoint)          # Second control point (apex)
angleNode.AddControlPoint(thirdControlPoint)  # Third control point

print(f"New angle 'n-{pn}-{sn}' created successfully.")

F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(9)     #XL#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(10)	#XR#
L.AddControlPoint(secondPoint)
L.SetName('MAW')


G=getNode('Rynn_soft_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = G.GetNthControlPointPositionVector(13)     #pt6R#
L.AddControlPoint(firstPoint)
secondPoint = G.GetNthControlPointPositionVector(14)	#pt6L#
L.AddControlPoint(secondPoint)
L.SetName('MNW')


F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(15)     #LCIL#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(17)	#MCIL#
L.AddControlPoint(secondPoint)
L.SetName('incisor width L')

F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(16)     #LCIR#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(18)	#MCIR#
L.AddControlPoint(secondPoint)
L.SetName('incisor width R')

F=getNode('Rynn_hard_tissue')  
L=slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode')
firstPoint = F.GetNthControlPointPositionVector(13)     #ICR#
L.AddControlPoint(firstPoint)
secondPoint = F.GetNthControlPointPositionVector(14)	#ICL#
L.AddControlPoint(secondPoint)
L.SetName('intercanine width')
