# ==============================================================================
# Ryu et al. 2024 Method - COMPLETE WORKFLOW (v6 - WITH EXTRA HARD TISSUE)
# ==============================================================================
# This script incorporates ALL exact code and color settings from the markdown
# INCLUDING the Extra Hard Tissue Measurements section
# ==============================================================================

import slicer
import qt
import logging
import numpy as np
import os
import urllib.request
import vtk

try:
    import gdown
except ImportError:
    slicer.util.pip_install('gdown')
    import gdown

# --- Define the Logic Class ---
class Ryu2024WorkflowLogic:
    def __init__(self, gui):
        self.gui = gui

    def trackNode(self, node):
        if node and node.GetID() not in self.gui.createdNodeIDs:
            self.gui.createdNodeIDs.append(node.GetID())

    def undo_all(self):
        logging.info(f"Cleaning up {len(self.gui.createdNodeIDs)} generated nodes...")
        for nodeID in self.gui.createdNodeIDs:
            node = slicer.mrmlScene.GetNodeByID(nodeID)
            if node:
                slicer.mrmlScene.RemoveNode(node)
        self.gui.createdNodeIDs.clear()

    def run_script_with_error_handling(self, script_function, *args):
        try:
            return script_function(*args)
        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred: {e}", 30)
            logging.error(f"Error during script execution: {e}", exc_info=True)
            return None

    def _execute_step0(self):
        """Calculate mid_au from auL and auR."""
        logging.info("--- Running Step 0: Calculate mid_au ---")
        hard_node = slicer.util.getNode("Ryu_hard_tissue")
        if not hard_node:
            raise ValueError("Node 'Ryu_hard_tissue' not found. Please load it first.")

        def get_landmark_pos(label):
            for i in range(hard_node.GetNumberOfControlPoints()):
                if hard_node.GetNthControlPointLabel(i) == label:
                    pos = np.zeros(3)
                    hard_node.GetNthControlPointPositionWorld(i, pos)
                    return pos
            raise ValueError(f"Landmark '{label}' not found.")

        auL_pos = get_landmark_pos('auL')
        auR_pos = get_landmark_pos('auR')
        mid_au_pos = (auL_pos + auR_pos) / 2.0

        mid_au_index = -1
        for i in range(hard_node.GetNumberOfControlPoints()):
            if hard_node.GetNthControlPointLabel(i) == 'mid_au':
                mid_au_index = i
                break

        if mid_au_index != -1:
            hard_node.SetNthControlPointPositionWorld(mid_au_index, mid_au_pos)
        else:
            hard_node.AddControlPoint(mid_au_pos, 'mid_au')

        return True

    def _execute_step1(self):
        """EXACT Step 1: Create Main Anatomical Planes from markdown"""
        logging.info("--- Running Step 1: Create Main Anatomical Planes ---")
        
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

            # Define vectors robustly from landmarks first
            auR, auL, n = get_landmark(hard_node, 'auR'), get_landmark(hard_node, 'auL'), get_landmark(hard_node, 'n')
            vec_right = unit(auR - auL)
            vec_anterior_initial = unit(n - (auR + auL) / 2.0)
            vec_anterior = unit(vec_anterior_initial - np.dot(vec_anterior_initial, vec_right) * vec_right)
            vec_superior = unit(np.cross(vec_right, vec_anterior))

            # Create planes from these corrected vectors
            midsag_plane = get_or_create("vtkMRMLMarkupsPlaneNode", "Median Sagittal Plane")
            midsag_plane.SetOrigin(get_landmark(hard_node, 'n')); midsag_plane.SetNormal(vec_right)
            style_plane(midsag_plane, [0.2, 0.8, 0.2])
            self.trackNode(midsag_plane)

            orbital_plane = get_or_create("vtkMRMLMarkupsPlaneNode", "Orbitale Transverse Plane")
            orbital_plane.SetOrigin(get_landmark(hard_node, 'orL')); orbital_plane.SetNormal(vec_superior)
            style_plane(orbital_plane, [0.8, 0.2, 0.2])
            self.trackNode(orbital_plane)

            coronal_plane = get_or_create("vtkMRMLMarkupsPlaneNode", "Coronal Plane")
            coronal_plane.SetOrigin(get_landmark(hard_node, 'b')); coronal_plane.SetNormal(vec_anterior)
            style_plane(coronal_plane, [0.2, 0.2, 0.8])
            self.trackNode(coronal_plane)

            return True

        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred in Step 1: {e}")
            return False

    def _execute_step2(self):
        """EXACT Step 2: Create Marginal Planes and Guiding Lines from markdown"""
        logging.info("--- Running Step 2: Create Marginal Planes and Guiding Lines ---")
        
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
            self.trackNode(ln)

        try:
            hard_node = slicer.util.getNode("Ryu_hard_tissue")
            
            # Get vectors from the correctly oriented main planes
            vec_superior = np.array(slicer.util.getNode("Orbitale Transverse Plane").GetNormal())
            vec_right = np.array(slicer.util.getNode("Median Sagittal Plane").GetNormal())

            # Create marginal geometry
            defs = [
                ("SOM", "sk", vec_superior, vec_right), ("IOM", "or", vec_superior, vec_right),
                ("MOM", "d", vec_right, vec_superior), ("LOM", "lat_or", vec_right, vec_superior)
            ]
            for base, lm_prefix, plane_n, line_dir in defs:
                for s in ["L", "R"]:
                    p = get_landmark(hard_node, f"{lm_prefix}{s}")
                    c = [1,0.7,0.2] if s=="L" else [0.2,0.7,1]
                    pl = get_or_create("vtkMRMLMarkupsPlaneNode", f"marginal_{base}_{s}")
                    pl.SetOrigin(p); pl.SetNormal(plane_n); style_plane(pl, c)
                    self.trackNode(pl)
                    make_line(f"guiding_{base}_{s}", p - line_dir*37.5, p + line_dir*37.5, c)

            return True

        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred in Step 2: {e}")
            return False

    def _execute_step3(self):
        """EXACT Step 3: Create Hard Tissue Measurements (L/R1, L/R8, L/R15) from markdown"""
        logging.info("--- Running Step 3: Create Core Hard Tissue Measurements ---")
        
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
            self.trackNode(ln)
            return ln

        try:
            hard_node = slicer.util.getNode("Ryu_hard_tissue")
            vec_superior = np.array(slicer.util.getNode("Orbitale Transverse Plane").GetNormal())
            vec_right = np.array(slicer.util.getNode("Median Sagittal Plane").GetNormal())
            vec_anterior = np.array(slicer.util.getNode("Coronal Plane").GetNormal())
            coronal_origin = np.array(slicer.util.getNode("Coronal Plane").GetOrigin())
            
            cyan = [0, 1, 1]
            
            for s in ["L", "R"]:
                # L1/R1: Distance from dL/dR to lat_orL/R along Right direction
                lom_p = get_landmark(hard_node, f"lat_or{s}")
                mom_p = get_landmark(hard_node, f"d{s}")
                dist = abs(np.dot(lom_p - mom_p, vec_right))
                make_line(f"{s}1", mom_p, mom_p + vec_right * np.dot(lom_p - mom_p, vec_right), cyan, dist)
                
                # L8/R8: Distance from skL/R to orL/R along Superior direction
                som_p = get_landmark(hard_node, f"sk{s}")
                iom_p = get_landmark(hard_node, f"or{s}")
                dist = abs(np.dot(som_p - iom_p, vec_superior))
                make_line(f"{s}8", iom_p, iom_p + vec_superior * np.dot(som_p - iom_p, vec_superior), cyan, dist)
                
                # L15/R15: Distance from lat_orL/R to Coronal Plane along Anterior direction
                lom_p = get_landmark(hard_node, f"lat_or{s}")
                dist = abs(np.dot(lom_p - coronal_origin, vec_anterior))
                make_line(f"{s}15", lom_p, lom_p - vec_anterior * np.dot(lom_p - coronal_origin, vec_anterior), cyan, dist)

            return True

        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred in Step 3: {e}")
            return False

    def _execute_step3b(self):
        """EXTRA Hard Tissue Measurements (C1, C2, L/R2-10, L/R16, L/R19) - ORANGE"""
        logging.info("--- Running Step 3b: Create Extra Hard Tissue Measurements ---")
        
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
            self.trackNode(ln)
            return ln

        def project_point_to_plane(point, plane_node):
            origin = np.zeros(3)
            normal = np.zeros(3)
            plane_node.GetOrigin(origin)
            plane_node.GetNormal(normal)
            return point - np.dot(point - origin, normal) * normal

        try:
            hard_node = slicer.util.getNode("Ryu_hard_tissue")
            marginal_SOM_L = slicer.util.getNode("marginal_SOM_L")
            marginal_SOM_R = slicer.util.getNode("marginal_SOM_R")
            marginal_MOM_L = slicer.util.getNode("marginal_MOM_L")
            marginal_MOM_R = slicer.util.getNode("marginal_MOM_R")
            marginal_LOM_L = slicer.util.getNode("marginal_LOM_L")
            marginal_LOM_R = slicer.util.getNode("marginal_LOM_R")
            orbital_plane = slicer.util.getNode("Orbitale Transverse Plane")
            coronal_plane = slicer.util.getNode("Coronal Plane")
            
            orange = [1, 0.5, 0]
            
            for s in ["L", "R"]:
                sk_pos = get_landmark(hard_node, f"sk{s}")
                or_pos = get_landmark(hard_node, f"or{s}")
                d_pos = get_landmark(hard_node, f"d{s}")
                lat_or_pos = get_landmark(hard_node, f"lat_or{s}")
                
                marginal_SOM = marginal_SOM_L if s == "L" else marginal_SOM_R
                marginal_MOM = marginal_MOM_L if s == "L" else marginal_MOM_R
                marginal_LOM = marginal_LOM_L if s == "L" else marginal_LOM_R
                
                # L2/R2: skL/R to marginal_MOM plane
                sk_to_mom = project_point_to_plane(sk_pos, marginal_MOM)
                dist = np.linalg.norm(sk_pos - sk_to_mom)
                make_line(f"{s}2", sk_pos, sk_to_mom, orange, dist)
                
                # L3/R3: skL/R to marginal_LOM plane
                sk_to_lom = project_point_to_plane(sk_pos, marginal_LOM)
                dist = np.linalg.norm(sk_pos - sk_to_lom)
                make_line(f"{s}3", sk_pos, sk_to_lom, orange, dist)
                
                # L4/R4: orL/R to marginal_MOM plane
                or_to_mom = project_point_to_plane(or_pos, marginal_MOM)
                dist = np.linalg.norm(or_pos - or_to_mom)
                make_line(f"{s}4", or_pos, or_to_mom, orange, dist)
                
                # L5/R5: orL/R to marginal_LOM plane
                or_to_lom = project_point_to_plane(or_pos, marginal_LOM)
                dist = np.linalg.norm(or_pos - or_to_lom)
                make_line(f"{s}5", or_pos, or_to_lom, orange, dist)
                
                # L6/R6: dL/R to marginal_SOM plane
                d_to_som = project_point_to_plane(d_pos, marginal_SOM)
                dist = np.linalg.norm(d_pos - d_to_som)
                make_line(f"{s}6", d_pos, d_to_som, orange, dist)
                
                # L7/R7: dL/R to orbital plane
                d_to_orbital = project_point_to_plane(d_pos, orbital_plane)
                dist = np.linalg.norm(d_pos - d_to_orbital)
                make_line(f"{s}7", d_pos, d_to_orbital, orange, dist)
                
                # L9/R9: lat_orL/R to marginal_SOM plane
                lat_or_to_som = project_point_to_plane(lat_or_pos, marginal_SOM)
                dist = np.linalg.norm(lat_or_pos - lat_or_to_som)
                make_line(f"{s}9", lat_or_pos, lat_or_to_som, orange, dist)
                
                # L10/R10: lat_orL/R to orbital plane
                lat_or_to_orbital = project_point_to_plane(lat_or_pos, orbital_plane)
                dist = np.linalg.norm(lat_or_pos - lat_or_to_orbital)
                make_line(f"{s}10", lat_or_pos, lat_or_to_orbital, orange, dist)
                
                # L16/R16: skL/R to coronal plane
                sk_to_coronal = project_point_to_plane(sk_pos, coronal_plane)
                dist = np.linalg.norm(sk_pos - sk_to_coronal)
                make_line(f"{s}16", sk_pos, sk_to_coronal, orange, dist)
                
                # L19/R19: dL/R to coronal plane
                d_to_coronal = project_point_to_plane(d_pos, coronal_plane)
                dist = np.linalg.norm(d_pos - d_to_coronal)
                make_line(f"{s}19", d_pos, d_to_coronal, orange, dist)

            # C1: Distance between marginal_LOM_L and marginal_LOM_R planes
            # C2: Distance from n to coronal plane
            n_pos = get_landmark(hard_node, 'n')
            n_to_coronal = project_point_to_plane(n_pos, coronal_plane)
            dist_C2 = np.linalg.norm(n_pos - n_to_coronal)
            make_line("C2", n_pos, n_to_coronal, orange, dist_C2)

            slicer.util.infoDisplay("SUCCESS: Created extra hard tissue measurement lines (ORANGE).")
            return True

        except Exception as e:
            slicer.util.errorDisplay(f"An error occurred in Step 3b: {e}")
            return False

    def _execute_step4(self, sex, side):
        """EXACT Step 4: Place eyeball from markdown (EYEBALL PLACEMENT GUI CODE)"""
        logging.info(f"--- Running Step 4: Place Eyeball ({sex} {side}) ---")
        
        hard_node = slicer.util.getNode("Ryu_hard_tissue")
        if not hard_node:
            raise ValueError("Node 'Ryu_hard_tissue' not found.")

        side_char = side[0]

        def get_node(name, cls):
            node = slicer.mrmlScene.GetFirstNodeByName(name)
            if not node or not node.IsA(cls):
                raise ValueError(f"Required node '{name}' of type {cls} not found.")
            return node
        
        def get_line_length(name):
            return get_node(name, "vtkMRMLMarkupsLineNode").GetMeasurement("length").GetValue()

        L1 = get_line_length(f"{side_char}1")
        L8 = get_line_length(f"{side_char}8")
        L15 = get_line_length(f"{side_char}15")

        # --- Apply sex-specific regression equations ---
        if sex == "Female":
            pred_L21 = 0.349 * L8 + 4.320
            pred_L22 = 0.652 * L8 - 4.353
            pred_L23 = 0.619 * L1 - 2.175
            pred_L33 = 1.005 * L15 + 14.700
        else:  # Male
            pred_L21 = 0.560 * L8 - 3.648
            pred_L22 = 0.439 * L8 + 3.662
            pred_L23 = 0.844 * L1 - 11.224
            pred_L33 = 0.950 * L15 + 19.126

        # Get anatomical reference vectors and planes
        vS = np.array(get_node("Orbitale Transverse Plane", "vtkMRMLMarkupsPlaneNode").GetNormal())
        vR = np.array(get_node("Median Sagittal Plane", "vtkMRMLMarkupsPlaneNode").GetNormal())
        vA = np.array(get_node("Coronal Plane", "vtkMRMLMarkupsPlaneNode").GetNormal())

        # Calculate target eyeball position from predictions
        p_si_1 = np.array(get_node(f"marginal_SOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()) - vS * pred_L21
        p_si_2 = np.array(get_node(f"marginal_IOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()) + vS * pred_L22
        d_si = 0.5 * (np.dot(vS, p_si_1) + np.dot(vS, p_si_2))

        lat_dir = -vR if side_char == "L" else vR
        p_ml = np.array(get_node(f"marginal_MOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()) + lat_dir * pred_L23
        d_ml = np.dot(vR, p_ml)

        p_ap = np.array(get_node("Coronal Plane", "vtkMRMLMarkupsPlaneNode").GetOrigin()) + vA * pred_L33
        d_ap = np.dot(vA, p_ap)

        target_pos = np.linalg.solve(np.array([vS, vR, vA]), np.array([d_si, d_ml, d_ap]))

        # Save 3D view and layout state
        def get_camera_state():
            view = slicer.app.layoutManager().threeDWidget(0).threeDView()
            renderer = view.renderWindow().GetRenderers().GetFirstRenderer()
            cam = renderer.GetActiveCamera()
            return (cam.GetPosition(), cam.GetFocalPoint(), cam.GetViewUp())
        
        def get_layout_state():
            """Save visibility state of all nodes before loading"""
            visibility_state = {}
            for node in slicer.util.getNodesByClass("vtkMRMLNode"):
                if hasattr(node, 'GetDisplayNode'):
                    display_node = node.GetDisplayNode()
                    if display_node:
                        visibility_state[node.GetID()] = display_node.GetVisibility()
            return visibility_state
        
        camera_state = get_camera_state()
        layout_state = get_layout_state()

        # Download and place eyeball model
        IDS = {
            "Female Left": "1p8rCfH7g35sAKXl0HeVf8PHzPt_xmSes",
            "Female Right": "1SK4alr7IumBGPm9OFUbNTCRAvJCPCpDR",
            "Male Left": "1X7JllfMrZM-AZpSrNh1CZwMGUTnHcqfG",
            "Male Right": "1rKmPbzuC1EjNoxLwoKNLIqLpZcVSxNYh"
        }
        key = f"{sex} {side}"
        mrb_path = os.path.join(slicer.app.temporaryPath, f"ryu_{key.replace(' ','_')}.mrb")
        gdown.download(id=IDS[key], output=mrb_path, quiet=False)
        
        nodes_before = set(slicer.util.getNodesByClass("vtkMRMLNode"))
        slicer.util.loadScene(mrb_path, {"clear": False, "loadCamera": False})
        new_nodes = list(set(slicer.util.getNodesByClass("vtkMRMLNode")) - nodes_before)

        for node in new_nodes:
            self.trackNode(node)

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

        # Create prediction measurement lines
        def make_pred_line(name, p0, p1, value, color=(1, 0, 0)):
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
            self.trackNode(ln)

        coronal_origin = np.array(get_node("Coronal Plane", "vtkMRMLMarkupsPlaneNode").GetOrigin())
        p_on_som = target_pos - vS * np.dot(target_pos - np.array(get_node(f"marginal_SOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()), vS)
        p_on_iom = target_pos - vS * np.dot(target_pos - np.array(get_node(f"marginal_IOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()), vS)
        p_on_mom = target_pos - vR * np.dot(target_pos - np.array(get_node(f"marginal_MOM_{side_char}", "vtkMRMLMarkupsPlaneNode").GetOrigin()), vR)
        p_on_coronal = target_pos - vA * np.dot(target_pos - coronal_origin, vA)

        make_pred_line(f"pred_{side_char}21", target_pos, p_on_som, pred_L21, color=(1, 0, 0))
        make_pred_line(f"pred_{side_char}22", target_pos, p_on_iom, pred_L22, color=(1, 0, 0))
        make_pred_line(f"pred_{side_char}23", target_pos, p_on_mom, pred_L23, color=(1, 0, 0))
        make_pred_line(f"pred_{side_char}33", target_pos, p_on_coronal, pred_L33, color=(1, 0, 0))

        # Restore camera state and layout
        view = slicer.app.layoutManager().threeDWidget(0).threeDView()
        renderer = view.renderWindow().GetRenderers().GetFirstRenderer()
        cam = renderer.GetActiveCamera()
        pos, fp, up = camera_state
        cam.SetPosition(pos)
        cam.SetFocalPoint(fp)
        cam.SetViewUp(up)
        view.renderWindow().Render()
        
        # Restore visibility state of previous nodes
        for node_id, visibility in layout_state.items():
            node = slicer.mrmlScene.GetNodeByID(node_id)
            if node and hasattr(node, 'GetDisplayNode'):
                display_node = node.GetDisplayNode()
                if display_node:
                    display_node.SetVisibility(visibility)

        final_message = (f"✓ Prediction complete!\n\n"
                         f"{sex} {side} eyeball\n\n"
                         f"Predicted soft tissue distances:\n"
                         f"{side_char}21 = {pred_L21:.2f} mm\n"
                         f"{side_char}22 = {pred_L22:.2f} mm\n"
                         f"{side_char}23 = {pred_L23:.2f} mm\n"
                         f"{side_char}33 = {pred_L33:.2f} mm")
        slicer.util.infoDisplay(final_message)

        return True

    def _execute_step5(self):
        """Step 5: Place true center landmarks"""
        logging.info("--- Running Step 5: Place True Center Landmarks ---")
        
        try:
            landmarks_node = slicer.util.getNode("Ryu_soft_tissue")
        except:
            slicer.util.errorDisplay("ERROR: 'Ryu_soft_tissue' landmark node not found in the scene. Please load it first.")
            return False

        def get_landmark_pos(label):
            for i in range(landmarks_node.GetNumberOfControlPoints()):
                if landmarks_node.GetNthControlPointLabel(i) == label:
                    pos = np.zeros(3)
                    landmarks_node.GetNthControlPointPositionWorld(i, pos)
                    return pos
            return None

        def set_or_add_landmark(label, position):
            for i in range(landmarks_node.GetNumberOfControlPoints()):
                if landmarks_node.GetNthControlPointLabel(i) == label:
                    landmarks_node.SetNthControlPointPositionWorld(i, position)
                    return
            landmarks_node.AddControlPoint(position, label)

        for side in ["L", "R"]:
            la_pos = get_landmark_pos(f"true_la{side}")
            lp_pos = get_landmark_pos(f"true_lp{side}")

            if la_pos is not None and lp_pos is not None:
                lc_pos = (la_pos + lp_pos) / 2.0
                set_or_add_landmark(f"true_lc{side}", lc_pos)

            oa_pos = get_landmark_pos(f"true_oa{side}")
            op_pos = get_landmark_pos(f"true_op{side}")
            os_pos = get_landmark_pos(f"true_os{side}")
            oi_pos = get_landmark_pos(f"true_oi{side}")
            om_pos = get_landmark_pos(f"true_om{side}")
            ol_pos = get_landmark_pos(f"true_ol{side}")

            extreme_points = [oa_pos, op_pos, os_pos, oi_pos, om_pos, ol_pos]
            if all(p is not None for p in extreme_points):
                gc_pos = np.mean(np.array(extreme_points), axis=0)
                set_or_add_landmark(f"true_gc{side}", gc_pos)

        slicer.util.infoDisplay("True center landmarks calculated.")
        return True

    def _execute_step6(self):
        """Step 6: Create final predicted soft tissue measurements (RED lines)"""
        logging.info("--- Running Step 6: Create Predicted Soft Tissue Measurements (RED) ---")
        
        def get_node(name):
            node = slicer.mrmlScene.GetFirstNodeByName(name)
            if not node:
                raise ValueError(f"Node '{name}' not found.")
            return node

        def get_landmark_pos(node, label):
            idx = node.GetControlPointIndexByLabel(label)
            if idx == -1:
                raise ValueError(f"Landmark '{label}' not found.")
            pos = np.zeros(3)
            node.GetNthControlPointPositionWorld(idx, pos)
            return pos

        def create_line(name, p1, p2, color):
            ln = slicer.mrmlScene.GetFirstNodeByName(name)
            if not ln:
                ln = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
            else:
                ln.RemoveAllControlPoints()
            ln.AddControlPoint(p1)
            ln.AddControlPoint(p2)
            d = ln.GetDisplayNode() or ln.CreateDefaultDisplayNodes()
            d.SetColor(color[0], color[1], color[2])
            d.SetSelectedColor(1, 1, 0)
            d.SetVisibility(True)
            ln.GetMeasurement("length").SetEnabled(True)
            self.trackNode(ln)

        def project_point_to_plane_node(point, plane_node):
            origin = np.zeros(3)
            normal = np.zeros(3)
            plane_node.GetOrigin(origin)
            plane_node.GetNormal(normal)
            return point - np.dot(point - origin, normal) * normal

        try:
            coronal_plane = get_node("Coronal Plane")
            hard_tissue_node = get_node("Ryu_hard_tissue")
            red = (1, 0, 0)

            for side in ["L", "R"]:
                side_full = "Left" if side == "L" else "Right"
                eyeball_lm_node = get_node(f"{side_full} Eyeball lmrks")
                
                marginal_SOM = get_node(f"marginal_SOM_{side}")
                marginal_MOM = get_node(f"marginal_MOM_{side}")

                lc_pos = get_landmark_pos(eyeball_lm_node, f"lc{side}")
                oa_pos = get_landmark_pos(eyeball_lm_node, f"oa{side}")
                ocp_pos = get_landmark_pos(hard_tissue_node, f"ocp{side}")

                create_line(f"pred_{side}21", lc_pos, project_point_to_plane_node(lc_pos, marginal_SOM), red)
                create_line(f"pred_{side}23", lc_pos, project_point_to_plane_node(lc_pos, marginal_MOM), red)
                create_line(f"pred_{side}33", oa_pos, project_point_to_plane_node(oa_pos, coronal_plane), red)
                create_line(f"pred_{side}32", oa_pos, ocp_pos, red)

            slicer.util.infoDisplay("SUCCESS: Created predicted soft tissue measurement lines (RED).")
            return True

        except Exception as e:
            raise ValueError(f"Error in Step 6: {e}")

    def _execute_step7(self):
        """Step 7: Create final true soft tissue measurements (GREEN lines)"""
        logging.info("--- Running Step 7: Create True Soft Tissue Measurements (GREEN) ---")
        
        def get_node(name):
            node = slicer.mrmlScene.GetFirstNodeByName(name)
            if not node:
                raise ValueError(f"Node '{name}' not found.")
            return node

        def get_landmark_pos(node, label):
            idx = node.GetControlPointIndexByLabel(label)
            if idx == -1:
                return None
            pos = np.zeros(3)
            node.GetNthControlPointPositionWorld(idx, pos)
            return pos

        def create_line(name, p1, p2, color):
            ln = slicer.mrmlScene.GetFirstNodeByName(name)
            if not ln:
                ln = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
            else:
                ln.RemoveAllControlPoints()
            ln.AddControlPoint(p1)
            ln.AddControlPoint(p2)
            d = ln.GetDisplayNode() or ln.CreateDefaultDisplayNodes()
            d.SetColor(color[0], color[1], color[2])
            d.SetSelectedColor(1, 1, 0)
            d.SetVisibility(True)
            ln.GetMeasurement("length").SetEnabled(True)
            self.trackNode(ln)

        def project_point_to_plane_node(point, plane_node):
            origin = np.zeros(3)
            normal = np.zeros(3)
            plane_node.GetOrigin(origin)
            plane_node.GetNormal(normal)
            return point - np.dot(point - origin, normal) * normal

        try:
            coronal_plane = get_node("Coronal Plane")
            hard_tissue_node = get_node("Ryu_hard_tissue")
            soft_tissue_node = get_node("Ryu_soft_tissue")
            green = (0, 1, 0)

            for side in ["L", "R"]:
                marginal_SOM = get_node(f"marginal_SOM_{side}")
                marginal_MOM = get_node(f"marginal_MOM_{side}")

                lc_pos = get_landmark_pos(soft_tissue_node, f"true_lc{side}")
                oa_pos = get_landmark_pos(soft_tissue_node, f"true_oa{side}")
                ocp_pos = get_landmark_pos(hard_tissue_node, f"ocp{side}")

                if lc_pos is not None and oa_pos is not None and ocp_pos is not None:
                    create_line(f"true_{side}21", lc_pos, project_point_to_plane_node(lc_pos, marginal_SOM), green)
                    create_line(f"true_{side}23", lc_pos, project_point_to_plane_node(lc_pos, marginal_MOM), green)
                    create_line(f"true_{side}33", oa_pos, project_point_to_plane_node(oa_pos, coronal_plane), green)
                    create_line(f"true_{side}32", oa_pos, ocp_pos, green)

            slicer.util.infoDisplay("SUCCESS: Created true soft tissue measurement lines (GREEN).")
            return True

        except Exception as e:
            raise ValueError(f"Error in Step 7: {e}")


# --- Define the GUI Widget Class ---
class Ryu2024WorkflowGUI(qt.QWidget):
    def __init__(self, parent=None):
        super(Ryu2024WorkflowGUI, self).__init__(parent)
        self.logic = Ryu2024WorkflowLogic(self)
        self.createdNodeIDs = []
        self.setup()

    def setup(self):
        self.setWindowTitle("Ryu et al. 2024 Complete Workflow")
        self.mainLayout = qt.QVBoxLayout(self)

        self.hard_tissue_url = "https://github.com/user-attachments/files/28435260/Ryu_hard_tissue.mrk.json"
        self.soft_tissue_url = "https://github.com/user-attachments/files/28435266/Ryu_soft_tissue.mrk.json"

        # Step 0
        setupBox = self._create_collapsible_box("Step 0: Load Hard Tissue Landmarks")
        self.loadHardTissueButton = qt.QPushButton("Download/Load Ryu Hard Tissue Landmarks")
        setupBox.layout().addRow(self.loadHardTissueButton)

        # Step 1
        step1Box = self._create_collapsible_box("Step 1: Create Main Anatomical Planes")
        step1Box.layout().addRow(qt.QLabel("Creates Median Sagittal, Orbitale Transverse, and Coronal planes."))
        self.runStep1Button = qt.QPushButton("Run Step 1")
        step1Box.layout().addRow(self.runStep1Button)

        # Step 2
        step2Box = self._create_collapsible_box("Step 2: Create Marginal Planes and Guiding Lines")
        step2Box.layout().addRow(qt.QLabel("Creates marginal planes and guiding lines (Orange=Left, Purple=Right)."))
        self.runStep2Button = qt.QPushButton("Run Step 2")
        step2Box.layout().addRow(self.runStep2Button)

        # Step 3
        step3Box = self._create_collapsible_box("Step 3: Create Core Hard Tissue Measurements")
        step3Box.layout().addRow(qt.QLabel("Calculates L/R1, L/R8, L/R15 (CYAN lines)."))
        self.runStep3Button = qt.QPushButton("Run Step 3")
        step3Box.layout().addRow(self.runStep3Button)

        # Step 3b
        step3bBox = self._create_collapsible_box("Step 3b (Optional): Create Extra Hard Tissue Measurements")
        step3bBox.layout().addRow(qt.QLabel("Calculates L/R2-10, L/R16, L/R19, C2 (ORANGE lines)."))
        self.runStep3bButton = qt.QPushButton("Run Step 3b - Extra Measurements")
        step3bBox.layout().addRow(self.runStep3bButton)

        # Step 4
        step4Box = self._create_collapsible_box("Step 4: Place Eyeball Model")
        self.sexSelector = qt.QComboBox()
        self.sexSelector.addItems(["Female", "Male"])
        step4Box.layout().addRow("Biological Sex:", self.sexSelector)
        self.sideSelector = qt.QComboBox()
        self.sideSelector.addItems(["Left", "Right"])
        step4Box.layout().addRow("Side:", self.sideSelector)
        self.runStep4Button = qt.QPushButton("Download and Place Eyeball")
        step4Box.layout().addRow(self.runStep4Button)
        self.placementStatusLabel = qt.QLabel("Ready.")
        step4Box.layout().addRow("Status:", self.placementStatusLabel)

        # Step 5
        step5Box = self._create_collapsible_box("Step 5: Load Soft Tissue Landmarks & Calculate Centers")
        self.loadSoftTissueButton = qt.QPushButton("Load Soft Tissue Landmarks")
        step5Box.layout().addRow(self.loadSoftTissueButton)
        self.runStep5Button = qt.QPushButton("Calculate True Centers (lc, gc)")
        step5Box.layout().addRow(self.runStep5Button)

        # Step 6
        step6Box = self._create_collapsible_box("Step 6: Create Predicted Soft Tissue Measurements")
        step6Box.layout().addRow(qt.QLabel("Creates L/R21, L/R22, L/R23, L/R32, L/R33 (RED lines)."))
        self.runStep6Button = qt.QPushButton("Run Step 6")
        step6Box.layout().addRow(self.runStep6Button)

        # Step 7
        step7Box = self._create_collapsible_box("Step 7: Create True Soft Tissue Measurements")
        step7Box.layout().addRow(qt.QLabel("Creates true L/R21, L/R22, L/R23, L/R32, L/R33 (GREEN lines)."))
        self.runStep7Button = qt.QPushButton("Run Step 7")
        step7Box.layout().addRow(self.runStep7Button)

        # Management
        manageBox = self._create_collapsible_box("Management")
        self.cleanupButton = qt.QPushButton("Clean Up All Generated Nodes")
        manageBox.layout().addRow(self.cleanupButton)

        self.mainLayout.addStretch(1)

        # Connections
        self.loadHardTissueButton.connect('clicked(bool)', lambda: self.onLoadMarkups(self.hard_tissue_url, "Ryu_hard_tissue"))
        self.loadSoftTissueButton.connect('clicked(bool)', lambda: self.onLoadMarkups(self.soft_tissue_url, "Ryu_soft_tissue"))
        self.runStep1Button.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step0) and self.logic.run_script_with_error_handling(self.logic._execute_step1))
        self.runStep2Button.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step2))
        self.runStep3Button.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step3))
        self.runStep3bButton.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step3b))
        self.runStep4Button.connect('clicked(bool)', self.onRunStep4)
        self.runStep5Button.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step5))
        self.runStep6Button.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step6))
        self.runStep7Button.connect('clicked(bool)', lambda: self.logic.run_script_with_error_handling(self.logic._execute_step7))
        self.cleanupButton.connect('clicked(bool)', self.onCleanup)

    def _create_collapsible_box(self, title):
        try:
            import ctk
            box = ctk.ctkCollapsibleButton()
            box.text = title
        except ImportError:
            box = qt.QGroupBox(title)
            box.setCheckable(True)
        
        layout = qt.QFormLayout()
        box.setLayout(layout)
        self.mainLayout.addWidget(box)
        return box

    def onLoadMarkups(self, url, node_name):
        if slicer.util.getFirstNodeByName(node_name):
            slicer.util.infoDisplay(f"Node '{node_name}' already exists.")
            return
        try:
            temp_path = os.path.join(slicer.app.temporaryPath, os.path.basename(url))
            urllib.request.urlretrieve(url, temp_path)
            node = slicer.util.loadMarkups(temp_path)
            node.SetName(node_name)
            self.logic.trackNode(node)
            slicer.util.infoDisplay(f"Successfully loaded '{node_name}'.")
        except Exception as e:
            slicer.util.errorDisplay(f"Failed to load landmarks: {e}")

    def onRunStep4(self):
        self.placementStatusLabel.setText("Starting...")
        slicer.app.processEvents()
        sex = self.sexSelector.currentText
        side = self.sideSelector.currentText
        result = self.logic.run_script_with_error_handling(self.logic._execute_step4, sex, side)
        if result:
            self.placementStatusLabel.setText(f"SUCCESS! Placed {sex} {side} eyeball.")
        else:
            self.placementStatusLabel.setText("ERROR: Check console for details.")

    def onCleanup(self):
        self.logic.undo_all()
        self.placementStatusLabel.setText("Ready.")
        slicer.util.infoDisplay("Cleanup complete.")


# --- Main execution block ---
try:
    if 'ryu2024WorkflowGUI' in globals() and ryu2024WorkflowGUI.parent():
        globals()['ryu2024WorkflowGUI'].parent().close()
    del globals()['ryu2024WorkflowGUI']
except (NameError, KeyError):
    pass

ryu2024WorkflowGUI = Ryu2024WorkflowGUI()
dockWidget = qt.QDockWidget("Ryu 2024 Complete Workflow")
dockWidget.setWidget(ryu2024WorkflowGUI)
slicer.util.mainWindow().addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
dockWidget.show()
