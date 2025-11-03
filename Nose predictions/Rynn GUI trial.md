```python
# =============================================================================
#
#  Rynn Method - Simplified GUI (Version 52.0 - Perfect Report Format)
#
#  Hello esomjai!
#
#  FINAL VERSION with equation formulas displayed in the report!
#  Example: PA_1_1: pred Rynn PA = 0.83*Y-3.5 = 26.14 mm
#
#  To use: RESTART 3D Slicer, then paste this entire script.
#
# =============================================================================

import os
import vtk
import numpy as np
import qt
import slicer
import urllib.request
import tempfile
import re

# =============================================================================
# REPORT WINDOW
# =============================================================================

class ReportWindow(qt.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculation Report")
        self.setWindowFlag(qt.Qt.WindowStaysOnTopHint, True)
        self.setGeometry(100, 100, 600, 700)
        
        self.main_layout = qt.QVBoxLayout(self)
        self.report_text_edit = qt.QTextEdit()
        self.report_text_edit.setReadOnly(True)
        self.report_text_edit.setFontFamily("Courier")
        self.report_text_edit.setLineWrapMode(qt.QTextEdit.NoWrap)
        
        self.button_layout = qt.QHBoxLayout()
        self.clear_button = qt.QPushButton("Clear Report")
        self.copy_basic_button = qt.QPushButton("Copy Basic Results")
        self.copy_advanced_button = qt.QPushButton("Copy Advanced Results")
        
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.copy_basic_button)
        self.button_layout.addWidget(self.copy_advanced_button)
        
        self.main_layout.addWidget(self.report_text_edit)
        self.main_layout.addLayout(self.button_layout)
        
        self.clear_button.clicked.connect(self.clear_report)
        self.copy_basic_button.clicked.connect(self.copy_basic_results)
        self.copy_advanced_button.clicked.connect(self.copy_advanced_results)

        self.results = {}
        self.clear_report()

    def append_text(self, text_string):
        self.report_text_edit.append(text_string)
        self.report_text_edit.verticalScrollBar().setValue(self.report_text_edit.verticalScrollBar().maximum)

    def store_result(self, category, item_id, measurement, value, unit):
        if category not in self.results: self.results[category] = []
        self.results[category].append({"id": item_id, "measurement": measurement, "value": value, "unit": unit})

    def clear_report(self):
        self.report_text_edit.clear(); self.results.clear(); self.append_text("--- Calculation Report ---\n")

    def _generate_report_string(self, categories_to_include):
        report_lines = ["ID\tMeasurement\tValue\tUnit"]
        for cat in categories_to_include:
            if cat in self.results:
                for item in self.results[cat]:
                    value_str = f"{item['value']:.2f}" if isinstance(item['value'], (float, np.floating)) else str(item['value'])
                    report_lines.append(f"{item['id']}\t{item['measurement']}\t{value_str}\t{item['unit']}")
        return "\n".join(report_lines)

    def copy_basic_results(self):
        categories = ["Base Measurements", "PA", "PV", "pFHP", "ND Radii", "NH Radii", "NL Radii", "Angles", "Basic Errors"]
        report = self._generate_report_string(categories)
        slicer.app.clipboard().setText(report); slicer.util.showStatusMessage("Basic results copied to clipboard.", 3000)

    def copy_advanced_results(self):
        categories = ["Projection Network", "Advanced Errors"]
        report = self._generate_report_string(categories)
        slicer.app.clipboard().setText(report); slicer.util.showStatusMessage("Advanced results copied to clipboard.", 3000)

# =============================================================================
# CAMERA UTILITIES
# =============================================================================

def save_camera_state():
    """Save the current 3D camera state."""
    layoutManager = slicer.app.layoutManager()
    if not layoutManager: return None
    threeDWidget = layoutManager.threeDWidget(0)
    if not threeDWidget: return None
    threeDView = threeDWidget.threeDView()
    if not threeDView: return None
    
    renderer = threeDView.renderWindow().GetRenderers().GetFirstRenderer()
    if not renderer: return None
    camera = renderer.GetActiveCamera()
    if not camera: return None
    
    return {
        'position': camera.GetPosition(),
        'focal_point': camera.GetFocalPoint(),
        'view_up': camera.GetViewUp(),
        'view_angle': camera.GetViewAngle(),
        'clipping_range': camera.GetClippingRange()
    }

def restore_camera_state(camera_state):
    """Restore a previously saved camera state."""
    if not camera_state: return
    
    layoutManager = slicer.app.layoutManager()
    if not layoutManager: return
    threeDWidget = layoutManager.threeDWidget(0)
    if not threeDWidget: return
    threeDView = threeDWidget.threeDView()
    if not threeDView: return
    
    renderer = threeDView.renderWindow().GetRenderers().GetFirstRenderer()
    if not renderer: return
    camera = renderer.GetActiveCamera()
    if not camera: return
    
    camera.SetPosition(camera_state['position'])
    camera.SetFocalPoint(camera_state['focal_point'])
    camera.SetViewUp(camera_state['view_up'])
    camera.SetViewAngle(camera_state['view_angle'])
    camera.SetClippingRange(camera_state['clipping_range'])
    
    threeDView.forceRender()

# =============================================================================
# MAIN LOGIC
# =============================================================================

class RynnMethodLogic:
    def __init__(self):
        self.run_number = self.get_next_run_number()
        self.item_counters = {}
    
    def get_next_run_number(self):
        """Find the next available run number by checking existing nodes."""
        max_run = 0
        for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode"):
            match = re.search(r'_(\d+)_\d+$', node.GetName())
            if match:
                max_run = max(max_run, int(match.group(1)))
        for node in slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode"):
            match = re.search(r'_(\d+)$', node.GetName())
            if match:
                max_run = max(max_run, int(match.group(1)))
        return max_run + 1
    
    def reset_item_counter(self, category):
        """Reset the item counter for a category."""
        self.item_counters[category] = 0
    
    def get_next_item_number(self, category):
        """Get the next item number for a category."""
        if category not in self.item_counters:
            self.item_counters[category] = 0
        self.item_counters[category] += 1
        return self.item_counters[category]
    
    def make_name(self, base_name, use_run_number=False):
        """Create a name, optionally with run number for items from Step 5 onwards."""
        if use_run_number:
            item_num = self.get_next_item_number(base_name)
            return f"{base_name}_{self.run_number}_{item_num}"
        else:
            return base_name
    
    def get_landmark_positions(self, landmark_node, required_landmarks):
        if not landmark_node: raise ValueError("Landmark node is not selected.")
        positions = {landmark_node.GetNthControlPointLabel(i).lower(): np.array(landmark_node.GetNthControlPointPositionWorld(i)) for i in range(landmark_node.GetNumberOfControlPoints())}
        for name in required_landmarks:
            clean_name = name.lower().split(" ")[0]
            if clean_name not in positions and "(if visible)" not in name:
                raise ValueError(f"Required landmark '{name}' not found in the selected node.")
        return positions

    def create_line(self, name, p1, p2, color=(1,1,0), use_run_number=False):
        full_name = self.make_name(name, use_run_number)
        line_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', full_name)
        line_node.AddControlPoint(p1); line_node.AddControlPoint(p2)
        displayNode = line_node.GetDisplayNode()
        if not displayNode: line_node.CreateDefaultDisplayNodes(); displayNode = line_node.GetDisplayNode()
        displayNode.SetColor(color); displayNode.SetSelectedColor(color); displayNode.SetLineThickness(0.5)
        return line_node

    def create_circle(self, name, center, radius, plane_normal, color=(0.2, 0.8, 0.2)):
        full_name = self.make_name(name, use_run_number=True)
        curve_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsClosedCurveNode", full_name)
        curve_node.CreateDefaultDisplayNodes(); display_node = curve_node.GetDisplayNode()
        plane_normal = np.array(plane_normal) / np.linalg.norm(np.array(plane_normal))
        arbitrary_vector = np.array([0, 0, 1]) if not np.allclose(plane_normal, [0, 0, 1]) else np.array([1, 0, 0])
        v1 = np.cross(plane_normal, arbitrary_vector); v1 /= np.linalg.norm(v1)
        v2 = np.cross(plane_normal, v1)
        for i in range(36):
            angle = 2 * np.pi * i / 36
            point = center + radius * (np.cos(angle) * v1 + np.sin(angle) * v2)
            curve_node.AddControlPoint(point)
        display_node.SetColor(color); display_node.SetSelectedColor(color)
        display_node.SetLineThickness(0.5); display_node.SetTextScale(0)
        return curve_node

    def create_reference_planes(self, landmark_node, method):
        def create_plane(name, origin, normal, color):
            plane_node = slicer.util.getFirstNodeByName(name) or slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', name)
            plane_node.SetOrigin(origin); plane_node.SetNormal(normal); plane_node.SetSize(300, 300)
            display_node = plane_node.GetDisplayNode() or plane_node.CreateDefaultDisplayNodes() and plane_node.GetDisplayNode()
            display_node.SetSelectedColor(color)
            return plane_node
        
        camera_state = save_camera_state()
        try:
            if "INB" in method:
                pos = self.get_landmark_positions(landmark_node, ["inion", "nasion", "bregma"])
                v1, v2 = pos['nasion'] - pos['inion'], pos['bregma'] - pos['inion']
                normal = np.cross(v1, v2); normal /= np.linalg.norm(normal)
                profile_plane = create_plane('INB', pos['inion'], normal, (1, 0, 0))
            elif "MSP" in method:
                pos = self.get_landmark_positions(landmark_node, ["nasion", "acanthion", "prosthion", "subspinale"])
                points = np.array(list(pos.values())); center = np.mean(points, axis=0)
                covariance = np.cov(points - center, rowvar=False); _, eigenvectors = np.linalg.eigh(covariance)
                normal = eigenvectors[:, np.argmin(_)]
                profile_plane = create_plane('MSP', center, normal, (1, 0.5, 0))
            else:
                raise ValueError("Invalid method")
            
            pos_np = self.get_landmark_positions(landmark_node, ["nasion", "prosthion"])
            profile_normal = np.array(profile_plane.GetNormal())
            vec_np = pos_np['nasion'] - pos_np['prosthion']
            npp_normal = np.cross(profile_normal, vec_np); npp_normal /= np.linalg.norm(npp_normal)
            create_plane('NPP', pos_np['prosthion'], npp_normal, (0, 1, 0))
            ptp_normal = np.cross(profile_normal, npp_normal); ptp_normal /= np.linalg.norm(ptp_normal)
            create_plane('PTP', pos_np['nasion'], ptp_normal, (0, 0, 1))
        finally:
            restore_camera_state(camera_state)

    def create_axes(self, landmark_node, report_window):
        pos = self.get_landmark_positions(landmark_node, ["nasion", "acanthion", "rhinion", "subspinale"])
        p_nas, p_aca, p_rhi, p_sub = pos['nasion'], pos['acanthion'], pos['rhinion'], pos['subspinale']
        x_len, y_len, z_len = np.linalg.norm(p_nas - p_aca), np.linalg.norm(p_rhi - p_sub), np.linalg.norm(p_nas - p_sub)
        
        camera_state = save_camera_state()
        try:
            self.create_line('X_axis', p_nas, p_aca, (1,0,0), use_run_number=False)
            self.create_line('Y_axis', p_rhi, p_sub, (0,1,0), use_run_number=False)
            self.create_line('Z_axis', p_nas, p_sub, (0,0,1), use_run_number=False)
        finally:
            restore_camera_state(camera_state)
        
        report_window.append_text(f"\n=== Run {self.run_number}: Base Measurements ===")
        report_window.append_text(f"X-axis: {x_len:.2f} mm")
        report_window.append_text(f"Y-axis: {y_len:.2f} mm")
        report_window.append_text(f"Z-axis: {z_len:.2f} mm")
        report_window.store_result("Base Measurements", f"Run{self.run_number}_X", "X-axis", x_len, "mm")
        report_window.store_result("Base Measurements", f"Run{self.run_number}_Y", "Y-axis", y_len, "mm")
        report_window.store_result("Base Measurements", f"Run{self.run_number}_Z", "Z-axis", z_len, "mm")

    def create_network_lines(self, landmark_node, active_profile_plane_name):
        profile_plane = slicer.util.getNode(active_profile_plane_name)
        if not profile_plane: raise ValueError(f"Profile plane '{active_profile_plane_name}' not found.")
        pos = self.get_landmark_positions(landmark_node, ["nasion", "subspinale"])
        profile_normal = np.array(profile_plane.GetNormal())
        horizontal_dir = np.cross(profile_normal, np.array([0,0,1])); horizontal_dir /= np.linalg.norm(horizontal_dir)
        vertical_dir = np.cross(horizontal_dir, profile_normal); vertical_dir /= np.linalg.norm(vertical_dir)
        
        camera_state = save_camera_state()
        try:
            self.create_line("Line_1", pos['nasion'] - horizontal_dir*150, pos['nasion'] + horizontal_dir*150, (1,0.5,0), use_run_number=False)
            self.create_line("Line_2", pos['nasion'] - vertical_dir*150, pos['nasion'] + vertical_dir*150, (1,0.5,0), use_run_number=False)
            self.create_line("Line_3", pos['subspinale'] - horizontal_dir*150, pos['subspinale'] + horizontal_dir*150, (1,0.5,0), use_run_number=False)
        finally:
            restore_camera_state(camera_state)

    def calculate_pa(self, landmark_node, equations_to_run, report_window):
        self.reset_item_counter("PA")
        
        y_node = slicer.util.getNode("Y_axis")
        l1_node = slicer.util.getNode("Line_1")
        if not y_node or not l1_node: raise ValueError("Y-axis or Line_1 missing.")
        
        p1, p2 = np.zeros(3), np.zeros(3)
        y_node.GetNthControlPointPositionWorld(0, p1); y_node.GetNthControlPointPositionWorld(1, p2)
        y_len = np.linalg.norm(p2 - p1)
        
        start_pos = self.get_landmark_positions(landmark_node, ["nasion"])["nasion"]
        l1_node.GetNthControlPointPositionWorld(0, p1); l1_node.GetNthControlPointPositionWorld(1, p2)
        direction = (p1 - p2) / np.linalg.norm(p1 - p2)
        ptp_node = slicer.util.getNode('PTP')
        if ptp_node and np.dot(direction, start_pos - np.array(ptp_node.GetOrigin())) > 0: direction *= -1
        
        report_window.append_text(f"\n=== Run {self.run_number}: PA ===")
        camera_state = save_camera_state()
        try:
            for eq in equations_to_run:
                eq_map = {
                    "pred Rynn PA": (0.83, y_len, -3.5, "0.83*Y-3.5"),
                    "pred Sarilita M PA": (0.57, y_len, 2.33, "0.57*Y+2.33"),
                    "pred Bulut F PA": (0.681, y_len, 2.711, "0.681*Y+2.711"),
                    "pred Bulut M PA": (0.776, y_len, -0.481, "0.776*Y-0.481")
                }
                coeff, var_len, const, eq_str = eq_map[eq]
                length = coeff * var_len + const
                line_node = self.create_line("PA", start_pos, start_pos + direction * length, (0.85,0.7,0), use_run_number=True)
                # THIS IS THE FIX: Show equation name = formula = result
                report_window.append_text(f"{line_node.GetName()}: {eq} = {eq_str} = {length:.2f} mm")
                report_window.store_result("PA", line_node.GetName(), eq, length, "mm")
        finally:
            restore_camera_state(camera_state)

    def calculate_pv(self, pa_line_name, pv_equations_to_run, report_window):
        self.reset_item_counter("PV")
        
        x_node = slicer.util.getNode("X_axis")
        l2_node = slicer.util.getNode("Line_2")
        pa_node = slicer.util.getNode(pa_line_name)
        if not all([x_node, l2_node, pa_node]): raise ValueError("Required nodes missing.")
        
        p1, p2 = np.zeros(3), np.zeros(3)
        x_node.GetNthControlPointPositionWorld(0, p1); x_node.GetNthControlPointPositionWorld(1, p2)
        x_len = np.linalg.norm(p2 - p1)
        
        l2_node.GetNthControlPointPositionWorld(0, p1); l2_node.GetNthControlPointPositionWorld(1, p2)
        direction = (p2 - p1) / np.linalg.norm(p2 - p1)
        if direction[2] > 0: direction *= -1
        
        pa_end_pos = np.array(pa_node.GetNthControlPointPositionWorld(1))
        pred_node_name = f"soft_tissue_pred_{self.run_number}"
        pred_node = slicer.util.getFirstNodeByName(pred_node_name) or slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", pred_node_name)
        
        report_window.append_text(f"\n=== Run {self.run_number}: PV (from {pa_line_name}) ===")
        camera_state = save_camera_state()
        try:
            for eq_name in pv_equations_to_run:
                eq_map = {
                    "pred Rynn PV": (0.9, x_len, -2, "0.9*X-2"),
                    "pred Sarilita M PV": (0.88, x_len, 0.68, "0.88*X+0.68"),
                    "pred Bulut F PV": (0.779, x_len, 5.501, "0.779*X+5.501"),
                    "pred Bulut M PV": (0.954, x_len, -3.53, "0.954*X-3.53")
                }
                coeff, var_len, const, eq_str = eq_map[eq_name]
                length = coeff * var_len + const
                final_pos = pa_end_pos + direction * length
                
                line_node = self.create_line("PV", pa_end_pos, final_pos, color=(0.2, 0.8, 0.2), use_run_number=True)
                point_label = f"pronasale_{line_node.GetName()}"
                pred_node.AddControlPoint(final_pos, point_label)
                
                # THIS IS THE FIX: Show equation name = formula = result
                report_window.append_text(f"{line_node.GetName()}: {eq_name} = {eq_str} = {length:.2f} mm")
                report_window.store_result("PV", line_node.GetName(), eq_name, length, "mm")
        finally:
            restore_camera_state(camera_state)

    def calculate_pfhp(self, landmark_node, equations_to_run, report_window):
        self.reset_item_counter("pFHP")
        
        y_node = slicer.util.getNode("Y_axis")
        l3_node = slicer.util.getNode("Line_3")
        if not y_node or not l3_node: raise ValueError("Y-axis or Line_3 missing.")
        
        p1,p2 = np.zeros(3),np.zeros(3)
        y_node.GetNthControlPointPositionWorld(0,p1); y_node.GetNthControlPointPositionWorld(1,p2)
        y_len = np.linalg.norm(p2-p1)
        
        l3_node.GetNthControlPointPositionWorld(0,p1); l3_node.GetNthControlPointPositionWorld(1,p2)
        direction = (p2 - p1) / np.linalg.norm(p2-p1)
        subsp = self.get_landmark_positions(landmark_node, ["subspinale"])["subspinale"]
        if np.dot(direction, subsp - p1) > 0: direction *= -1
        
        report_window.append_text(f"\n=== Run {self.run_number}: pFHP ===")
        camera_state = save_camera_state()
        try:
            for eq in equations_to_run:
                eq_map = {
                    "pred Rynn pFHP": (0.93, y_len, -6, "0.93*Y-6"),
                    "pred Sarilita M pFHP": (0.58, y_len, 4.55, "0.58*Y+4.55"),
                    "pred Bulut F pFHP": (0.775, y_len, 1.161, "0.775*Y+1.161"),
                    "pred Bulut M pFHP": (0.777, y_len, 0.518, "0.777*Y+0.518")
                }
                coeff, var_len, const, eq_str = eq_map[eq]
                length = coeff * var_len + const
                line_node = self.create_line("pFHP", subsp, subsp + direction * length, (0.9,0.4,0.1), use_run_number=True)
                # THIS IS THE FIX: Show equation name = formula = result
                report_window.append_text(f"{line_node.GetName()}: {eq} = {eq_str} = {length:.2f} mm")
                report_window.store_result("pFHP", line_node.GetName(), eq, length, "mm")
        finally:
            restore_camera_state(camera_state)

    def calculate_sn(self, center_point_index, nd_equation, pfhp_line_name, active_profile_plane_name, report_window):
        self.reset_item_counter("ND_circle")
        
        pred_node = slicer.util.getFirstNodeByName(f"soft_tissue_pred_{self.run_number}")
        y_node = slicer.util.getNode("Y_axis")
        z_node = slicer.util.getNode("Z_axis")
        plane = slicer.util.getNode(active_profile_plane_name)
        line_node = slicer.util.getNode(pfhp_line_name)
        if not all([pred_node, y_node, z_node, plane, line_node]): raise ValueError("Required nodes missing.")
        
        center_label, center_pos = pred_node.GetNthControlPointLabel(center_point_index), np.array(pred_node.GetNthControlPointPositionWorld(center_point_index))
        p1,p2 = np.zeros(3),np.zeros(3)
        y_node.GetNthControlPointPositionWorld(0,p1); y_node.GetNthControlPointPositionWorld(1,p2); y_len=np.linalg.norm(p2-p1)
        z_node.GetNthControlPointPositionWorld(0,p1); z_node.GetNthControlPointPositionWorld(1,p2); z_len=np.linalg.norm(p2-p1)
        
        eq_map = {
            "pred Rynn F ND": (0.5, y_len, 1.5, "0.5*Y+1.5"),
            "pred Rynn M ND": (0.4, y_len, 5, "0.4*Y+5"),
            "pred Sarilita M ND": (0.22, z_len, 4.02, "0.22*Z+4.02"),
            "pred Sarilita F ND": (0.29, y_len, 6.24, "0.29*Y+6.24"),
            "pred Bulut F ND": (0.423, y_len, 5.169, "0.423*Y+5.169"),
            "pred Bulut M ND": (0.386, y_len, 6.587, "0.386*Y+6.587")
        }
        coeff, var_len, const, eq_str = eq_map[nd_equation]
        radius = coeff * var_len + const
        
        report_window.append_text(f"\n=== Run {self.run_number}: sn (ND circle) ===")
        report_window.append_text(f"Center: {center_label}, Line: {pfhp_line_name}")
        # THIS IS THE FIX: Show equation name = formula = result
        report_window.append_text(f"{nd_equation} = {eq_str} = {radius:.2f} mm")
        report_window.store_result("ND Radii", f"Run{self.run_number}_{nd_equation}", "Radius", radius, "mm")
        
        plane_n = np.array(plane.GetNormal())
        camera_state = save_camera_state()
        try:
            self.create_circle("ND_circle", center_pos, radius, plane_n)
        finally:
            restore_camera_state(camera_state)
        
        u=np.cross(plane_n,[0,0,1] if not np.allclose(plane_n,[0,0,1]) else [1,0,0]); u/=np.linalg.norm(u); v=np.cross(u,plane_n)
        lp0,lp1=np.array(line_node.GetNthControlPointPositionWorld(0)),np.array(line_node.GetNthControlPointPositionWorld(1))
        p0_plane=np.array([np.dot(lp0-center_pos,u),np.dot(lp0-center_pos,v)])
        p1_plane=np.array([np.dot(lp1-center_pos,u),np.dot(lp1-center_pos,v)])
        dp = p1_plane - p0_plane; a = np.dot(dp,dp); b = 2*np.dot(p0_plane,dp); c = np.dot(p0_plane,p0_plane) - radius**2
        discriminant = b**2 - 4*a*c
        if discriminant < 0: raise ValueError("No intersection found.")
        t_values = [(-b + np.sqrt(discriminant))/(2*a), (-b - np.sqrt(discriminant))/(2*a)]
        intersections = [lp0 + t*(lp1-lp0) for t in t_values if 0 <= t <= 1]
        if not intersections: raise ValueError("Intersection outside line segment.")
        
        final_label = f"subnasale_{self.run_number}"
        pred_node.AddControlPoint(intersections[0], final_label)
        report_window.append_text(f"Created: {final_label}")

    def calculate_nasion(self, nh_center_point_index, nh_equation, nl_center_point_index, nl_equation, active_profile_plane_name, report_window):
        self.reset_item_counter("NH_circle")
        self.reset_item_counter("NL_circle")
        
        pred_node = slicer.util.getFirstNodeByName(f"soft_tissue_pred_{self.run_number}")
        x_node = slicer.util.getNode("X_axis")
        z_node = slicer.util.getNode("Z_axis")
        plane = slicer.util.getNode(active_profile_plane_name)
        if not all([pred_node, x_node, z_node, plane]): raise ValueError("Required nodes missing.")
        
        nh_label, nh_center_pos = pred_node.GetNthControlPointLabel(nh_center_point_index), np.array(pred_node.GetNthControlPointPositionWorld(nh_center_point_index))
        nl_label, nl_center_pos = pred_node.GetNthControlPointLabel(nl_center_point_index), np.array(pred_node.GetNthControlPointPositionWorld(nl_center_point_index))
        p1,p2=np.zeros(3),np.zeros(3)
        x_node.GetNthControlPointPositionWorld(0,p1); x_node.GetNthControlPointPositionWorld(1,p2); x_len=np.linalg.norm(p2-p1)
        z_node.GetNthControlPointPositionWorld(0,p1); z_node.GetNthControlPointPositionWorld(1,p2); z_len=np.linalg.norm(p2-p1)
        
        nh_map = {
            "pred Rynn EA M NH": (0.78, z_len, 9.5, "0.78*Z+9.5"),
            "pred Rynn EA F NH": (0.63, z_len, 17, "0.63*Z+17"),
            "pred Sarilita M NH": (0.79, z_len, 3.74, "0.79*Z+3.74"),
            "pred Sarilita F NH": (0.69, x_len, 12.36, "0.69*X+12.36"),
            "pred Bulut F NH": (0.687, z_len, 15.047, "0.687*Z+15.047"),
            "pred Bulut M NH": (0.784, z_len, 9.858, "0.784*Z+9.858")
        }
        nl_map = {
            "pred Rynn EA NL": (0.74, z_len, 3.5, "0.74*Z+3.5"),
            "pred Sarilita F NL": (0.71, z_len, 6.624, "0.71*Z+6.624"),
            "pred Sarilita M NL": (0.807, z_len, 0.764, "0.807*Z+0.764"),
            "pred Bulut M NL": (0.66, x_len, 7.77, "0.66*X+7.77")
        }
        
        nh_coeff, nh_var, nh_const, nh_eq_str = nh_map[nh_equation]
        nl_coeff, nl_var, nl_const, nl_eq_str = nl_map[nl_equation]
        nh_radius, nl_radius = nh_coeff * nh_var + nh_const, nl_coeff * nl_var + nl_const
        
        report_window.append_text(f"\n=== Run {self.run_number}: Nasion ===")
        # THIS IS THE FIX: Show equation name = formula = result
        report_window.append_text(f"NH: {nh_equation} = {nh_eq_str} = {nh_radius:.2f} mm")
        report_window.append_text(f"NL: {nl_equation} = {nl_eq_str} = {nl_radius:.2f} mm")
        report_window.store_result("NH Radii", f"Run{self.run_number}_{nh_equation}", "Radius", nh_radius, "mm")
        report_window.store_result("NL Radii", f"Run{self.run_number}_{nl_equation}", "Radius", nl_radius, "mm")
        
        plane_n = np.array(plane.GetNormal())
        camera_state = save_camera_state()
        try:
            self.create_circle("NH_circle", nh_center_pos, nh_radius, plane_n, color=(1,0,0))
            self.create_circle("NL_circle", nl_center_pos, nl_radius, plane_n, color=(0,0,1))
        finally:
            restore_camera_state(camera_state)
        
        c1,r1,c2,r2=nh_center_pos,nh_radius,nl_center_pos,nl_radius
        d_vec=c1-c2; d=np.linalg.norm(d_vec)
        if d > r1+r2 or d < abs(r1-r2) or d==0: raise ValueError("Circles do not intersect.")
        a=(r1**2-r2**2+d**2)/(2*d); h=np.sqrt(max(0,r1**2-a**2)); p2_intersect=c1+a*(c2-c1)/d
        v=np.cross(d_vec,plane_n); v/=np.linalg.norm(v); intersections=[p2_intersect+h*v, p2_intersect-h*v]
        
        l1_node = slicer.util.getNode("Line_1")
        l1p0,l1p1=np.array(l1_node.GetNthControlPointPositionWorld(0)), np.array(l1_node.GetNthControlPointPositionWorld(1))
        def dist_to_line(pt,p0,p1):
            line_vec=p1-p0; point_vec=pt-p0; line_len=np.linalg.norm(line_vec)
            proj=np.dot(point_vec,line_vec/line_len)
            if proj<0: return np.linalg.norm(pt-p0)
            if proj>line_len: return np.linalg.norm(pt-p1)
            return np.linalg.norm(pt - (p0 + proj*(line_vec/line_len)))
        closest_pt=min(intersections, key=lambda pt: dist_to_line(pt,l1p0,l1p1))
        
        label=f"nasion_{self.run_number}"
        pred_node.AddControlPoint(closest_pt, label)
        report_window.append_text(f"Created: {label}")
# =============================================================================
# PART 2: GUI - Steps 2-10 and Main Window
# =============================================================================

class StepWidget(qt.QWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(parent)
        self.logic = logic
        self.data = data
        self.main_gui = main_gui
        self.mainLayout = qt.QVBoxLayout(self)
        title_label = qt.QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.mainLayout.addWidget(title_label, 0, qt.Qt.AlignHCenter)
    def onEnterStep(self): pass
    def get_landmark_node(self):
        return self.main_gui.get_selected_landmark_node()

class Step2_LandmarkSetup(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        
        self.downloadHardButton = qt.QPushButton("1. Download Hard Tissue Landmarks")
        self.downloadHardButton.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold; padding: 8px;")
        
        noteLabel = qt.QLabel("<b>2. Place the required hard tissue landmarks on your model.</b>")
        noteLabel.setWordWrap(True); noteLabel.setTextFormat(qt.Qt.RichText)
        
        self.landmarkTable = qt.QTableWidget(7, 1)
        self.landmarkTable.setHorizontalHeaderLabels(["Required Hard Tissue Landmarks"])
        landmarks = ["nasion","inion (if visible)","bregma (if visible)","prosthion","subspinale","rhinion","acanthion"]
        for i, landmark in enumerate(landmarks):
            self.landmarkTable.setItem(i, 0, qt.QTableWidgetItem(landmark))
        self.landmarkTable.horizontalHeader().setStretchLastSection(True)
        self.landmarkTable.verticalHeader().setVisible(False)
        self.landmarkTable.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.landmarkTable.setFixedHeight(self.landmarkTable.verticalHeader().defaultSectionSize * (self.landmarkTable.rowCount + 1))
        
        selectorLayout = qt.QFormLayout()
        self.landmarksSelector = slicer.qMRMLNodeComboBox()
        self.landmarksSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.landmarksSelector.setMRMLScene(slicer.mrmlScene)
        self.landmarksSelector.addEnabled = True
        self.landmarksSelector.removeEnabled = False
        self.landmarksSelector.noneEnabled = True
        selectorLayout.addRow("<b>3. Select Landmark Node:</b>", self.landmarksSelector)
        
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        
        for w in [self.downloadHardButton, noteLabel, self.landmarkTable, self.statusLabel]:
            self.mainLayout.addWidget(w)
        self.mainLayout.addLayout(selectorLayout)
        self.mainLayout.addStretch(1)
        
        self.downloadHardButton.clicked.connect(self.onDownloadHardLandmarks)
        self.attempt_count = 0

    def onEnterStep(self):
        if self.landmarksSelector.currentNode():
            self.statusLabel.setText("✓ Status: Landmark node is already selected.")
            return
        
        self.attempt_count = 0
        self.tryAutoSelect()
    
    def tryAutoSelect(self):
        slicer.app.processEvents()
        qt.QApplication.instance().processEvents()
        
        # Smart search: look for nodes with the required landmarks inside
        required_landmarks = ["nasion", "prosthion", "rhinion", "subspinale", "acanthion"]
        
        for node in slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode'):
            # Check if this node has the required landmarks
            landmark_labels = [node.GetNthControlPointLabel(i).lower() for i in range(node.GetNumberOfControlPoints())]
            matches = sum(1 for req in required_landmarks if any(req in label for label in landmark_labels))
            
            # If it has at least 3 of the required landmarks, it's probably the right one
            if matches >= 3:
                self.landmarksSelector.setCurrentNode(node)
                self.statusLabel.setText(f"✓ Status: Auto-selected '{node.GetName()}' (found {matches} matching landmarks)")
                return
        
        # If not found and we haven't tried too many times, try again
        self.attempt_count += 1
        if self.attempt_count < 5:
            qt.QTimer.singleShot(200 * self.attempt_count, self.tryAutoSelect)
        else:
            self.statusLabel.setText("Status: Please download or manually select the landmark node.")

    def onDownloadHardLandmarks(self):
        self.statusLabel.setText("Status: Downloading...")
        slicer.app.processEvents()
        url = "https://github.com/user-attachments/files/22989769/Rynn_hard_tissue.mrk.json"
        nodeName = "Rynn_hard_tissue"
        try:
            with urllib.request.urlopen(url) as response, tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile:
                tempFile.write(response.read())
                tempFilePath = tempFile.name
            loadedNode = slicer.util.loadMarkups(tempFilePath)
            os.remove(tempFilePath)
            if loadedNode:
                loadedNode.SetName(nodeName)
                slicer.app.processEvents()
                qt.QTimer.singleShot(100, lambda: self.landmarksSelector.setCurrentNode(loadedNode))
                self.statusLabel.setText(f"✓ Status: '{nodeName}' downloaded and selected.")
            else:
                raise IOError("Failed to load landmarks.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step3_PlaneSetup(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        
        desc = qt.QLabel("Choose a method to define the primary profile plane (INB or MSP).")
        desc.setWordWrap(True)
        
        noteLabel = qt.QLabel("<b>📝 Note:</b> The reference planes will be used for all runs. If you want to change from INB to MSP (or vice versa), please save your scene and reload 3D Slicer.")
        noteLabel.setWordWrap(True)
        noteLabel.setStyleSheet("background-color: #FFF3CD; padding: 10px; border-radius: 5px;")
        
        planeChoiceLayout = qt.QFormLayout()
        self.planeChoiceComboBox = qt.QComboBox()
        self.planeChoiceComboBox.addItems(["Select a method...", "INB (Inion-Nasion-Bregma)", "MSP (Midsagittal Best-Fit)"])
        planeChoiceLayout.addRow("Profile Plane Method:", self.planeChoiceComboBox)
        
        self.createPlanesButton = qt.QPushButton("Create All Reference Planes")
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        
        self.mainLayout.addWidget(desc)
        self.mainLayout.addWidget(noteLabel)
        self.mainLayout.addLayout(planeChoiceLayout)
        self.mainLayout.addWidget(self.createPlanesButton)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch(1)
        
        self.createPlanesButton.clicked.connect(self.onCreatePlanes)
    
    def onCreatePlanes(self):
        self.statusLabel.setText("Status: Processing...")
        slicer.app.processEvents()
        try:
            landmark_node = self.get_landmark_node()
            choice = self.planeChoiceComboBox.currentText
            if "Select a method" in choice:
                raise ValueError("Please select a plane creation method.")
            self.logic.create_reference_planes(landmark_node, choice)
            active_plane_name = "INB" if "INB" in choice else "MSP"
            self.statusLabel.setText(f"✓ Status: Created {active_plane_name}, NPP, and PTP planes.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step4_Scaffolding(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        
        axesGroup = qt.QGroupBox("1. Coordinate Axes")
        axesLayout = qt.QVBoxLayout(axesGroup)
        self.createAxesButton = qt.QPushButton("Create X, Y, Z Axes")
        axesLayout.addWidget(self.createAxesButton)
        
        networkGroup = qt.QGroupBox("2. Reference Network")
        networkLayout = qt.QVBoxLayout(networkGroup)
        self.createNetworkButton = qt.QPushButton("Create Network Lines 1, 2, 3")
        networkLayout.addWidget(self.createNetworkButton)
        
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        
        self.mainLayout.addWidget(axesGroup)
        self.mainLayout.addWidget(networkGroup)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch(1)
        
        self.createAxesButton.clicked.connect(self.onCreateAxes)
        self.createNetworkButton.clicked.connect(self.onCreateNetwork)
    
    def onCreateAxes(self):
        self.statusLabel.setText("Status: Creating axes...")
        slicer.app.processEvents()
        try:
            landmark_node = self.get_landmark_node()
            self.logic.create_axes(landmark_node, self.data["report_window"])
            self.statusLabel.setText(f"✓ Status: Axes created for Run {self.logic.run_number}.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")
    
    def onCreateNetwork(self):
        self.statusLabel.setText("Status: Creating network lines...")
        slicer.app.processEvents()
        try:
            landmark_node = self.get_landmark_node()
            active_plane = slicer.util.getFirstNodeByName("INB") or slicer.util.getFirstNodeByName("MSP")
            if not active_plane:
                raise ValueError("Please create Reference Planes in Step 3 first.")
            plane_name = active_plane.GetName()
            self.logic.create_network_lines(landmark_node, plane_name)
            self.statusLabel.setText(f"✓ Status: Network lines created.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step5_PronasaleAnterior(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        self.mainLayout.addWidget(qt.QLabel("Predict the anterior position of the pronasale."))
        table_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%">
            <tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr>
            <tr><td>Rynn 2010</td><td>ANY</td><td>All</td><td>0.83 * Y - 3.5</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Male</td><td>0.57 * Y + 2.33</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Female</td><td>0.681 * Y + 2.711</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Male</td><td>0.776 * Y - 0.481</td></tr>
            </table><br><b>Y</b> = Y-axis length"""
        self.mainLayout.addWidget(qt.QLabel(table_html))
        self.pa_equations = ["pred Rynn PA", "pred Sarilita M PA", "pred Bulut F PA", "pred Bulut M PA"]
        self.pa_checkbox_list = []
        for eq in self.pa_equations:
            checkbox = qt.QCheckBox(eq)
            self.mainLayout.addWidget(checkbox)
            self.pa_checkbox_list.append(checkbox)
        self.calculateButton = qt.QPushButton("Calculate Pronasale Anterior")
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.calculateButton)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch(1)
        self.calculateButton.clicked.connect(self.onCalculatePA)
    
    def onCalculatePA(self):
        self.statusLabel.setText("Status: Calculating...")
        slicer.app.processEvents()
        try:
            landmark_node = self.get_landmark_node()
            chosen = [cb.text for cb in self.pa_checkbox_list if cb.isChecked()]
            if not chosen:
                raise ValueError("Please select at least one equation.")
            self.logic.calculate_pa(landmark_node, chosen, self.data["report_window"])
            self.statusLabel.setText(f"✓ Status: Created {len(chosen)} PA line(s) for Run {self.logic.run_number}.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step6_PronasaleVertical(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        self.mainLayout.addWidget(qt.QLabel("Predict the vertical position of the pronasale."))
        table_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%">
            <tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr>
            <tr><td>Rynn 2010</td><td>ANY</td><td>All</td><td>0.9 * X - 2</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Male</td><td>0.88 * X + 0.68</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Female</td><td>0.779 * X + 5.501</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Male</td><td>0.954 * X - 3.53</td></tr>
            </table><br><b>X</b> = X-axis length"""
        self.mainLayout.addWidget(qt.QLabel(table_html))
        
        self.pa_group = qt.QGroupBox("1. Select PA Line(s) to Use")
        self.mainLayout.addWidget(self.pa_group)
        self.pa_checkbox_list = []
        
        pv_group = qt.QGroupBox("2. Select PV Equation(s)")
        self.mainLayout.addWidget(pv_group)
        pv_layout = qt.QVBoxLayout(pv_group)
        self.pv_equations = ["pred Rynn PV", "pred Sarilita M PV", "pred Bulut F PV", "pred Bulut M PV"]
        self.pv_checkbox_list = []
        for eq in self.pv_equations:
            cb = qt.QCheckBox(eq)
            pv_layout.addWidget(cb)
            self.pv_checkbox_list.append(cb)
        
        self.calculateButton = qt.QPushButton("Calculate Pronasale Vertical")
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.calculateButton)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch(1)
        self.calculateButton.clicked.connect(self.onCalculatePV)
    
    def onEnterStep(self):
        layout = self.pa_group.layout() or qt.QVBoxLayout(self.pa_group)
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        self.pa_checkbox_list.clear()
        
        # Find PA lines for this run
        pa_lines = [n for n in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") if n.GetName().startswith(f"PA_{self.logic.run_number}_")]
        
        if not pa_lines:
            layout.addWidget(qt.QLabel("No PA lines found. Please complete Step 5."))
        else:
            for ln in pa_lines:
                cb = qt.QCheckBox(ln.GetName())
                layout.addWidget(cb)
                self.pa_checkbox_list.append(cb)
            if len(self.pa_checkbox_list) == 1:
                self.pa_checkbox_list[0].setChecked(True)
    
    def onCalculatePV(self):
        self.statusLabel.setText("Status: Calculating...")
        slicer.app.processEvents()
        try:
            chosen_pa_lines = [cb.text for cb in self.pa_checkbox_list if cb.isChecked()]
            chosen_pv_eqs = [cb.text for cb in self.pv_checkbox_list if cb.isChecked()]
            if not chosen_pa_lines or not chosen_pv_eqs:
                raise ValueError("Please select at least one PA line and one PV equation.")
            for pa_line in chosen_pa_lines:
                self.logic.calculate_pv(pa_line, chosen_pv_eqs, self.data["report_window"])
            self.statusLabel.setText(f"✓ Status: Created PV points for Run {self.logic.run_number}.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step7_PFH(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        self.mainLayout.addWidget(qt.QLabel("<b>Select pFHP equation(s)</b>"))
        table_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%">
            <tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr>
            <tr><td>Rynn 2010</td><td>ANY</td><td>All</td><td>0.93 * Y - 6</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Male</td><td>0.58 * Y + 4.55</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Female</td><td>1.161 + 0.775 * Y</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Male</td><td>0.518 + 0.777 * Y</td></tr>
            </table><br><b>Y</b> = Y-axis length"""
        self.mainLayout.addWidget(qt.QLabel(table_html))
        self.pfhp_equations = ["pred Rynn pFHP", "pred Sarilita M pFHP", "pred Bulut F pFHP", "pred Bulut M pFHP"]
        self.pfhp_checkbox_list = []
        for eq in self.pfhp_equations:
            cb = qt.QCheckBox(eq)
            self.mainLayout.addWidget(cb)
            self.pfhp_checkbox_list.append(cb)
        self.calculateButton = qt.QPushButton("Calculate pFHP")
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        self.mainLayout.addWidget(self.calculateButton)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch(1)
        self.calculateButton.clicked.connect(self.onCalculatePFHP)
    
    def onCalculatePFHP(self):
        self.statusLabel.setText("Status: Calculating...")
        slicer.app.processEvents()
        try:
            landmark_node = self.get_landmark_node()
            chosen = [cb.text for cb in self.pfhp_checkbox_list if cb.isChecked()]
            if not chosen:
                raise ValueError("Please select at least one pFHP equation.")
            self.logic.calculate_pfhp(landmark_node, chosen, self.data["report_window"])
            self.statusLabel.setText(f"✓ Status: Created {len(chosen)} pFHP line(s) for Run {self.logic.run_number}.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step8_SoftTissueSN(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        table_html = """<table border="1" cellspacing="0" cellpadding="3" width="100%">
            <tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr>
            <tr><td>Rynn 2010</td><td>ANY</td><td>Female</td><td>0.5 * Y + 1.5</td></tr>
            <tr><td>Rynn 2010</td><td>ANY</td><td>Male</td><td>0.4 * Y + 5</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Female</td><td>0.29 * Y + 6.24</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Male</td><td>0.22 * Z + 4.02</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Female</td><td>0.423 * Y + 5.169</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Male</td><td>0.386 * Y + 6.587</td></tr>
            </table><br><b>Y</b> = Y-axis, <b>Z</b> = Z-axis"""
        self.mainLayout.addWidget(qt.QLabel(table_html))
        
        self.point_group = qt.QGroupBox("1. Choose pronasale pred point")
        self.nd_eq_group = qt.QGroupBox("2. Choose ND radius equation")
        self.line_group = qt.QGroupBox("3. Choose pFHP line")
        
        nd_layout = qt.QVBoxLayout(self.nd_eq_group)
        self.nd_equations = ["pred Rynn F ND", "pred Rynn M ND", "pred Sarilita M ND", "pred Sarilita F ND", "pred Bulut F ND", "pred Bulut M ND"]
        self.nd_eq_buttons = qt.QButtonGroup(self)
        for i, eq in enumerate(self.nd_equations):
            radio = qt.QRadioButton(eq)
            nd_layout.addWidget(radio)
            self.nd_eq_buttons.addButton(radio, i)
        
        self.calculateButton = qt.QPushButton("Create ND Circle and Find Intersection")
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        self.statusLabel.setWordWrap(True)
        
        for w in [self.point_group, self.nd_eq_group, self.line_group, self.calculateButton, self.statusLabel]:
            self.mainLayout.addWidget(w)
        self.mainLayout.addStretch(1)
        self.calculateButton.clicked.connect(self.onCalculateSN)
    
    def _populate_radio_group(self, group_box, items, button_group):
        layout = group_box.layout() or qt.QVBoxLayout(group_box)
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        for button in button_group.buttons():
            button_group.removeButton(button)
        if not items:
            layout.addWidget(qt.QLabel("No items found."))
        else:
            for i, (label, data) in enumerate(items):
                radio = qt.QRadioButton(label)
                layout.addWidget(radio)
                button_group.addButton(radio, data)
            if button_group.buttons():
                button_group.buttons()[0].setChecked(True)
    
    def onEnterStep(self):
        pred_node = slicer.util.getFirstNodeByName(f"soft_tissue_pred_{self.logic.run_number}")
        
        self.pronasale_points_group = qt.QButtonGroup(self)
        pronasale_items = [(pred_node.GetNthControlPointLabel(i), i) for i in range(pred_node.GetNumberOfControlPoints()) if "pronasale" in pred_node.GetNthControlPointLabel(i).lower()] if pred_node else []
        self._populate_radio_group(self.point_group, pronasale_items, self.pronasale_points_group)
        
        self.pfhp_lines_group = qt.QButtonGroup(self)
        pfhp_nodes = [node for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") if node.GetName().startswith(f"pFHP_{self.logic.run_number}_")]
        self.pfhp_line_names = [node.GetName() for node in pfhp_nodes]
        pfhp_items = [(name, i) for i, name in enumerate(self.pfhp_line_names)]
        self._populate_radio_group(self.line_group, pfhp_items, self.pfhp_lines_group)
    
    def onCalculateSN(self):
        self.statusLabel.setText("Status: Calculating...")
        slicer.app.processEvents()
        try:
            active_plane = slicer.util.getFirstNodeByName("INB") or slicer.util.getFirstNodeByName("MSP")
            if not active_plane:
                raise ValueError("Please create Reference Planes in Step 3 first.")
            plane_name = active_plane.GetName()
            
            center_point_index = self.pronasale_points_group.checkedId()
            nd_equation_index = self.nd_eq_buttons.checkedId()
            pfhp_line_index = self.pfhp_lines_group.checkedId()
            
            if -1 in [center_point_index, nd_equation_index, pfhp_line_index]:
                raise ValueError("Please make a selection in all three sections.")
            
            self.logic.calculate_sn(center_point_index, self.nd_equations[nd_equation_index], self.pfhp_line_names[pfhp_line_index], plane_name, self.data["report_window"])
            self.statusLabel.setText(f"✓ Status: Created sn point for Run {self.logic.run_number}.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step9_Nasion(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        
        nh_table_html = """<b>NH (Nasal Height) Equations</b><table border="1" cellspacing="0" cellpadding="3" width="100%">
            <tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr>
            <tr><td>Rynn 2010</td><td>European American</td><td>Male</td><td>0.78*Z+9.5</td></tr>
            <tr><td>Rynn 2010</td><td>European American</td><td>Female</td><td>0.63*Z+17</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Male</td><td>0.79*Z+3.74</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Female</td><td>0.69*X+12.36</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Female</td><td>0.687*Z+15.047</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Male</td><td>0.784*Z+9.858</td></tr>
            </table>"""
        
        nl_table_html = """<b>NL (Nasal Length) Equations</b><table border="1" cellspacing="0" cellpadding="3" width="100%">
            <tr><th>Literature</th><th>Ancestry</th><th>Sex</th><th>Equation</th></tr>
            <tr><td>Rynn 2010</td><td>European American</td><td>ANY</td><td>0.74*Z+3.5</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Female</td><td>0.71*Z+6.624</td></tr>
            <tr><td>Sarilita 2018</td><td>Indonesian</td><td>Male</td><td>0.807*Z+0.764</td></tr>
            <tr><td>Bulut 2019</td><td>Turkish</td><td>Male</td><td>0.66*X+7.77</td></tr>
            </table><br><b>X</b> = X-axis, <b>Z</b> = Z-axis"""
        
        self.nh_group = qt.QGroupBox("1. Choose NH center ('sn' point)")
        self.nh_eq_group = qt.QGroupBox("2. Choose NH equation")
        nh_eq_layout = qt.QVBoxLayout(self.nh_eq_group)
        nh_eq_layout.addWidget(qt.QLabel(nh_table_html))
        
        self.nl_group = qt.QGroupBox("3. Choose NL center ('pronasale' point)")
        self.nl_eq_group = qt.QGroupBox("4. Choose NL equation")
        nl_eq_layout = qt.QVBoxLayout(self.nl_eq_group)
        nl_eq_layout.addWidget(qt.QLabel(nl_table_html))
        
        self.nh_equations = ["pred Rynn EA M NH", "pred Rynn EA F NH", "pred Sarilita M NH", "pred Sarilita F NH", "pred Bulut F NH", "pred Bulut M NH"]
        self.nh_eq_buttons = self._add_buttons_to_group(nh_eq_layout, self.nh_equations)
        
        self.nl_equations = ["pred Rynn EA NL", "pred Sarilita F NL", "pred Sarilita M NL", "pred Bulut M NL"]
        self.nl_eq_buttons = self._add_buttons_to_group(nl_eq_layout, self.nl_equations)
        
        self.calculateButton = qt.QPushButton("Draw Circles and Predict Nasion")
        self.statusLabel = qt.QLabel("Status: Waiting for user.")
        
        for w in [self.nh_group, self.nh_eq_group, self.nl_group, self.nl_eq_group, self.calculateButton, self.statusLabel]:
            self.mainLayout.addWidget(w)
        self.mainLayout.addStretch(1)
        self.calculateButton.clicked.connect(self.onCalculateNasion)
    
    def _add_buttons_to_group(self, layout, equations):
        button_group = qt.QButtonGroup(self)
        for i, eq in enumerate(equations):
            radio = qt.QRadioButton(eq)
            layout.addWidget(radio)
            button_group.addButton(radio, i)
        return button_group
    
    def _populate_radio_group(self, group_box, items, button_group):
        layout = group_box.layout() or qt.QVBoxLayout(group_box)
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
        for button in button_group.buttons():
            button_group.removeButton(button)
        if not items:
            layout.addWidget(qt.QLabel("No items found."))
        else:
            for i, (label, data) in enumerate(items):
                radio = qt.QRadioButton(label)
                layout.addWidget(radio)
                button_group.addButton(radio, data)
            if button_group.buttons():
                button_group.buttons()[0].setChecked(True)
    
    def onEnterStep(self):
        pred_node = slicer.util.getFirstNodeByName(f"soft_tissue_pred_{self.logic.run_number}")
        
        self.nh_center_points_group = qt.QButtonGroup(self)
        nh_items = [(pred_node.GetNthControlPointLabel(i), i) for i in range(pred_node.GetNumberOfControlPoints()) if "subnasale" in pred_node.GetNthControlPointLabel(i).lower()] if pred_node else []
        self._populate_radio_group(self.nh_group, nh_items, self.nh_center_points_group)
        
        self.nl_center_points_group = qt.QButtonGroup(self)
        nl_items = [(pred_node.GetNthControlPointLabel(i), i) for i in range(pred_node.GetNumberOfControlPoints()) if "pronasale" in pred_node.GetNthControlPointLabel(i).lower()] if pred_node else []
        self._populate_radio_group(self.nl_group, nl_items, self.nl_center_points_group)
    
    def onCalculateNasion(self):
        self.statusLabel.setText("Status: Calculating...")
        slicer.app.processEvents()
        try:
            active_plane = slicer.util.getFirstNodeByName("INB") or slicer.util.getFirstNodeByName("MSP")
            if not active_plane:
                raise ValueError("Please create Reference Planes in Step 3 first.")
            plane_name = active_plane.GetName()
            
            nh_center_idx = self.nh_center_points_group.checkedId()
            nh_eq_idx = self.nh_eq_buttons.checkedId()
            nl_center_idx = self.nl_center_points_group.checkedId()
            nl_eq_idx = self.nl_eq_buttons.checkedId()
            
            if -1 in [nh_center_idx, nh_eq_idx, nl_center_idx, nl_eq_idx]:
                raise ValueError("Please make a selection in all four sections.")
            
            self.logic.calculate_nasion(nh_center_idx, self.nh_equations[nh_eq_idx], nl_center_idx, self.nl_equations[nl_eq_idx], plane_name, self.data["report_window"])
            self.statusLabel.setText(f"✓ Status: Created nasion point for Run {self.logic.run_number}.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")

class Step10_Analysis(StepWidget):
    def __init__(self, title, logic, data, main_gui, parent=None):
        super().__init__(title, logic, data, main_gui, parent)
        
        # Run Again section
        run_again_group = qt.QGroupBox("🔄 Start a New Run")
        run_again_layout = qt.QVBoxLayout(run_again_group)
        
        info_label = qt.QLabel("Click below to start a new run with different equations. Your current geometry will stay visible so you can compare!")
        info_label.setWordWrap(True)
        run_again_layout.addWidget(info_label)
        
        note_label = qt.QLabel("<b>📝 Note:</b> All runs use the same reference planes (INB/MSP). To change planes, save your scene and reload 3D Slicer.")
        note_label.setWordWrap(True)
        note_label.setStyleSheet("background-color: #FFF3CD; padding: 10px; border-radius: 5px;")
        run_again_layout.addWidget(note_label)
        
        self.runAgainButton = qt.QPushButton("▶ Run Again (Start New Run)")
        self.runAgainButton.setStyleSheet("background-color: #28A745; color: white; font-weight: bold; padding: 10px;")
        run_again_layout.addWidget(self.runAgainButton)
        
        # Analysis section
        compare_group = qt.QGroupBox("📊 Analysis Tools")
        compare_layout = qt.QVBoxLayout(compare_group)
        
        self.softNodeStatusLabel = qt.QLabel("Status:")
        self.softNodeStatusLabel.setWordWrap(True)
        compare_layout.addWidget(self.softNodeStatusLabel)
        
        self.downloadSoftButton = qt.QPushButton("Download 'Rynn_soft_tissue' Landmarks")
        self.downloadSoftButton.setStyleSheet("background-color: #007BFF; color: white;")
        compare_layout.addWidget(self.downloadSoftButton)
        
        self.basicCompareButton = qt.QPushButton("Run Basic Comparison (Errors & Angles)")
        self.projectionButton = qt.QPushButton("Create Rynn Projection Network")
        self.advancedCompareButton = qt.QPushButton("Run Advanced Network Analysis")
        compare_layout.addWidget(self.basicCompareButton)
        compare_layout.addWidget(self.projectionButton)
        compare_layout.addWidget(self.advancedCompareButton)
        
        # Report section
        cleanup_group = qt.QGroupBox("📋 Report & View")
        cleanup_layout = qt.QVBoxLayout(cleanup_group)
        self.toggleReportButton = qt.QPushButton("Show/Hide Calculation Report")
        self.toggleHelpersButton = qt.QPushButton("Toggle All Geometry Visibility")
        cleanup_layout.addWidget(self.toggleReportButton)
        cleanup_layout.addWidget(self.toggleHelpersButton)
        
        self.statusLabel = qt.QLabel(f"✓ Status: Run {self.logic.run_number} complete!")
        self.statusLabel.setWordWrap(True)
        
        self.mainLayout.addWidget(run_again_group)
        self.mainLayout.addWidget(compare_group)
        self.mainLayout.addWidget(cleanup_group)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch(1)
        
        self.runAgainButton.clicked.connect(self.onRunAgain)
        self.downloadSoftButton.clicked.connect(self.onDownloadSoftLandmarks)
        self.basicCompareButton.clicked.connect(self.onBasicCompare)
        self.projectionButton.clicked.connect(self.onRunProjection)
        self.advancedCompareButton.clicked.connect(self.onAdvancedCompare)
        self.toggleReportButton.clicked.connect(self.onToggleReport)
        self.toggleHelpersButton.clicked.connect(self.onToggleHelpers)
    
    def onEnterStep(self):
        found_node = slicer.util.getFirstNodeByName(self.data["soft_tissue_node_name"])
        if found_node:
            self.softNodeStatusLabel.setText(f"✓ <b>Info:</b> Found soft tissue node: <b>'{found_node.GetName()}'</b>.")
        else:
            self.softNodeStatusLabel.setText("<b>Action Needed:</b> No soft tissue node found. Please download one.")
        
        self.advancedCompareButton.enabled = bool(slicer.util.getFirstNodeByName("n-pt1R"))
        self.statusLabel.setText(f"✓ Status: Run {self.logic.run_number} complete!")
    
    def onRunAgain(self):
        # Increment run number
        self.logic.run_number += 1
        self.logic.item_counters = {}
        
        # Update the main GUI's run label
        self.main_gui.updateRunLabel()
        
        # Show message
        msg = qt.QMessageBox()
        msg.setIcon(qt.QMessageBox.Information)
        msg.setText(f"Starting Run {self.logic.run_number}!")
        msg.setInformativeText("Your previous run's geometry will stay visible so you can compare.\n\nClick OK to jump to Step 5 (PA calculation).")
        msg.setWindowTitle("New Run Started")
        msg.setStandardButtons(qt.QMessageBox.Ok)
        msg.exec_()
        
        # Jump to Step 5 (PA - index 4)
        self.main_gui.currentStep = 4
        self.main_gui.update_ui()
        
        # Add to report
        self.data["report_window"].append_text(f"\n\n{'='*60}")
        self.data["report_window"].append_text(f"STARTING NEW RUN {self.logic.run_number}")
        self.data["report_window"].append_text(f"{'='*60}")
    
    def onDownloadSoftLandmarks(self):
        self.statusLabel.setText("Status: Downloading...")
        slicer.app.processEvents()
        
        # Smart naming: find a unique name if Rynn_soft_tissue already exists
        base_name = self.data["soft_tissue_node_name"]
        nodeName = base_name
        counter = 2
        
        # Check if the name already exists, if so, add a number
        while slicer.util.getFirstNodeByName(nodeName):
            nodeName = f"{base_name}_{counter}"
            counter += 1
        
        try:
            with urllib.request.urlopen("https://github.com/user-attachments/files/22989771/Rynn_soft_tissue.mrk.json") as response, tempfile.NamedTemporaryFile(delete=False, suffix='.mrk.json', mode='wb') as tempFile:
                tempFile.write(response.read())
                tempFilePath = tempFile.name
            
            loadedNode = slicer.util.loadMarkups(tempFilePath)
            os.remove(tempFilePath)
            
            if loadedNode:
                loadedNode.SetName(nodeName)
                if nodeName != base_name:
                    self.statusLabel.setText(f"✓ Status: Downloaded as '{nodeName}' (original already exists).")
                else:
                    self.statusLabel.setText(f"✓ Status: '{nodeName}' downloaded.")
                self.onEnterStep()
            else:
                raise IOError("Failed to load landmarks.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")
    
    def _create_or_update_angle(self, name, p1, p2, p3, color, report_window):
        angle_node = slicer.util.getFirstNodeByName(name) or slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsAngleNode', name)
        angle_node.GetDisplayNode().SetColor(color)
        angle_node.RemoveAllControlPoints()
        angle_node.AddControlPoint(p1)
        angle_node.AddControlPoint(p2)
        angle_node.AddControlPoint(p3)
        angle_deg = angle_node.GetAngleDegrees()
        report_window.store_result("Angles", name, "Angle", angle_deg, "degrees")
    
    def onBasicCompare(self):
        self.statusLabel.setText("Status: Running Basic Comparison...")
        slicer.app.processEvents()
        try:
            pred_node = slicer.util.getNode(f"soft_tissue_pred_{self.logic.run_number}")
            soft_node = slicer.util.getNode(self.data["soft_tissue_node_name"])
            if not pred_node or not soft_node:
                raise ValueError(f"Nodes not found.")
            
            for node in [n for n in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") if n.GetName().startswith("error_")]:
                slicer.mrmlScene.RemoveNode(node)
            
            angles_created, error_lines_created = 0, 0
            
            pred_points = {"nasion": None, "pronasale": None, "subnasale": None}
            for i in range(pred_node.GetNumberOfControlPoints()):
                label, pos = pred_node.GetNthControlPointLabel(i), np.array(pred_node.GetNthControlPointPositionWorld(i))
                if "nasion" in label.lower():
                    pred_points["nasion"] = pos
                if "pronasale" in label.lower():
                    pred_points["pronasale"] = pos
                if "subnasale" in label.lower():
                    pred_points["subnasale"] = pos
            
            if all(v is not None for v in pred_points.values()):
                self._create_or_update_angle(f"Predicted_Nasal_Angle_Run{self.logic.run_number}", pred_points["nasion"], pred_points["pronasale"], pred_points["subnasale"], (1,1,0), self.data["report_window"])
                angles_created += 1
            
            true_positions = {"nasion": None, "pronasale": None, "subnasale": None}
            for i in range(soft_node.GetNumberOfControlPoints()):
                label, pos = soft_node.GetNthControlPointLabel(i).lower(), np.array(soft_node.GetNthControlPointPositionWorld(i))
                if "nasion" in label:
                    true_positions["nasion"] = pos
                if "pronasale" in label:
                    true_positions["pronasale"] = pos
                if "subnasale" in label:
                    true_positions["subnasale"] = pos
            
            if all(v is not None for v in true_positions.values()):
                self._create_or_update_angle("True_Nasal_Angle", true_positions["nasion"], true_positions["pronasale"], true_positions["subnasale"], (0,1,1), self.data["report_window"])
                angles_created += 1
            
            for i in range(pred_node.GetNumberOfControlPoints()):
                pred_label, pred_pos = pred_node.GetNthControlPointLabel(i), np.array(pred_node.GetNthControlPointPositionWorld(i))
                soft_key = "nasion" if "nasion" in pred_label.lower() else "subnasale" if "subnasale" in pred_label.lower() else "pronasale" if "pronasale" in pred_label.lower() else None
                if soft_key and true_positions.get(soft_key) is not None:
                    error_dist = np.linalg.norm(pred_pos - true_positions[soft_key])
                    self.logic.create_line(f"error_{pred_label}", pred_pos, true_positions[soft_key], color=(1,0,0), use_run_number=False)
                    error_lines_created += 1
                    self.data["report_window"].store_result("Basic Errors", pred_label, "Error Distance", error_dist, "mm")
            
            self.statusLabel.setText(f"✓ Status: Created {error_lines_created} error lines, {angles_created} angles.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")
    
    def onRunProjection(self):
        self.statusLabel.setText("Status: Running projection network...")
        slicer.app.processEvents()
        try:
            hard_node, soft_node = self.get_landmark_node(), slicer.util.getNode(self.data["soft_tissue_node_name"])
            if not soft_node:
                raise ValueError(f"Soft tissue node not found.")
            
            for node in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode"):
                if node.GetName().startswith("n-pt") or " lat" in node.GetName() or " ant" in node.GetName() or " vert" in node.GetName() or node.GetName() in ["MAW", "MNW"]:
                    slicer.mrmlScene.RemoveNode(node)
            self.data['report_window'].results.pop("Projection Network", None)
            
            nasion_pos = self.logic.get_landmark_positions(hard_node, ["nasion"])["nasion"]
            point_map = {"pt1R": 3, "pt1L": 4, "pt2R": 5, "pt2L": 6, "pt3R": 7, "pt3L": 8, "pt4R": 9, "pt4L": 10, "pt5R": 11, "pt5L": 12, "pt6R": 13, "pt6L": 14, "pt7R": 15, "pt7L": 16, "pt8R": 17, "pt8L": 18}
            
            for name, index in point_map.items():
                soft_pos = np.array(soft_node.GetNthControlPointPositionWorld(index))
                line_node = self.logic.create_line(f"n-{name}", nasion_pos, soft_pos, color=(0.5, 0.5, 0.5), use_run_number=False)
                self.data['report_window'].store_result("Projection Network", line_node.GetName(), "Length", line_node.GetLineLengthWorld(), "mm")
                
                for plane_name_part in ["NPP", "PTP", "INB", "MSP"]:
                    plane_node = slicer.util.getFirstNodeByName(plane_name_part)
                    if not plane_node:
                        continue
                    suffix_map = {"NPP": "lat", "PTP": "ant", "INB": "vert", "MSP": "vert"}
                    suffix, color = suffix_map[plane_node.GetName()], plane_node.GetDisplayNode().GetColor()
                    plane_origin, plane_normal = np.array(plane_node.GetOrigin()), np.array(plane_node.GetNormal())
                    
                    def project(p):
                        return p - np.dot(p - plane_origin, plane_normal) * plane_normal
                    
                    line_node_proj = self.logic.create_line(f"{name} {suffix}", project(nasion_pos), project(soft_pos), color, use_run_number=False)
                    self.data['report_window'].store_result("Projection Network", line_node_proj.GetName(), "Length", line_node_proj.GetLineLengthWorld(), "mm")
            
            self.logic.create_line("MAW", self.logic.get_landmark_positions(hard_node, ["XL"])["xl"], self.logic.get_landmark_positions(hard_node, ["XR"])["xr"], (1,0,1), use_run_number=False)
            self.logic.create_line("MNW", self.logic.get_landmark_positions(soft_node, ["pt6r"])["pt6r"], self.logic.get_landmark_positions(soft_node, ["pt6l"])["pt6l"], (1,0,1), use_run_number=False)
            self.statusLabel.setText(f"✓ Status: Projection Network created successfully.")
            self.onEnterStep()
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")
    
    def onAdvancedCompare(self):
        self.statusLabel.setText("Status: Running Advanced Analysis...")
        slicer.app.processEvents()
        try:
            hard_node, soft_node = self.get_landmark_node(), slicer.util.getNode(self.data["soft_tissue_node_name"])
            if not soft_node:
                raise ValueError("Soft tissue node not found.")
            
            for node in [n for n in slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") if n.GetName().startswith("adv_error_") or n.GetName() == "Shortest_MNW-MAW"]:
                slicer.mrmlScene.RemoveNode(node)
            self.data['report_window'].results.pop("Advanced Errors", None)
            
            print("\n--- Advanced Analysis Report ---")
            pairs = [("pt5L", 12, "CL", 7, (1,0,0)), ("pt5R", 11, "CR", 8, (1,0,0)), ("pt7L", 16, "LL", 11, (0.13,0.55,0.13)), ("pt7R", 15, "LR", 12, (0.13,0.55,0.13)), ("pt4L", 10, "XL", 9, (0.13,0.55,0.13)), ("pt4R", 9, "XR", 10, (0.13,0.55,0.13))]
            
            for soft_label, soft_idx, hard_label_text, hard_idx, color in pairs:
                soft_pos, hard_pos = np.array(soft_node.GetNthControlPointPositionWorld(soft_idx)), np.array(hard_node.GetNthControlPointPositionWorld(hard_idx))
                line_name = f"adv_error_{soft_label}-{hard_label_text}"
                self.logic.create_line(line_name, hard_pos, soft_pos, color, use_run_number=False)
                displacement_len = np.linalg.norm(soft_pos - hard_pos)
                print(f"{line_name}: {displacement_len:.2f} mm")
                self.data['report_window'].store_result("Advanced Errors", line_name, "Length", displacement_len, "mm")
            
            mnw, maw = slicer.util.getNode("MNW"), slicer.util.getNode("MAW")
            if mnw and maw:
                p0,p1,q0,q1=np.array(mnw.GetNthControlPointPositionWorld(0)),np.array(mnw.GetNthControlPointPositionWorld(1)),np.array(maw.GetNthControlPointPositionWorld(0)),np.array(maw.GetNthControlPointPositionWorld(1))
                u,v,w=p1-p0,q1-q0,p0-q0
                a,b,c,d,e=np.dot(u,u),np.dot(u,v),np.dot(v,v),np.dot(u,w),np.dot(v,w)
                den=a*c-b*b
                sc,tc = ((b*e-c*d)/den,(a*e-b*d)/den) if den!=0 else (0,np.dot(-w,v)/c if c!=0 else 0)
                pa, pb = p0+sc*u, q0+tc*v
                dist = np.linalg.norm(pa - pb)
                self.logic.create_line("Shortest_MNW-MAW",pa,pb,color=(0.13,0.55,0.13), use_run_number=False)
                print(f"Shortest MNW-MAW: {dist:.2f} mm")
                self.data['report_window'].store_result("Advanced Errors", "Shortest_MNW-MAW", "Distance", dist, "mm")
            
            self.statusLabel.setText(f"✓ Status: Advanced analysis complete.")
        except Exception as e:
            self.statusLabel.setText(f"Status: Error! {e}")
    
    def onToggleHelpers(self):
        nodes = (slicer.util.getNodesByClass("vtkMRMLMarkupsPlaneNode") + 
                slicer.util.getNodesByClass("vtkMRMLMarkupsClosedCurveNode") + 
                slicer.util.getNodesByClass("vtkMRMLMarkupsLineNode") + 
                slicer.util.getNodesByClass("vtkMRMLMarkupsAngleNode"))
        if not nodes:
            self.statusLabel.setText("Status: No geometry found.")
            return
        first_node = next((n for n in nodes if n and n.GetDisplayNode()), None)
        if not first_node:
            return
        new_visibility = not first_node.GetDisplayNode().GetVisibility()
        for node in nodes:
            if node and node.GetDisplayNode():
                node.GetDisplayNode().SetVisibility(new_visibility)
        self.statusLabel.setText(f"Status: Geometry is now {'visible' if new_visibility else 'hidden'}.")
    
    def onToggleReport(self):
        if self.data["report_window"].isVisible():
            self.data["report_window"].hide()
        else:
            self.data["report_window"].show()

# =============================================================================
# MAIN GUI
# =============================================================================

class RynnMethodSimplifiedGUI(qt.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(qt.Qt.WindowStaysOnTopHint, True)
        self.setWindowTitle("Rynn (2010) Method - Simplified")
        self.setObjectName("RynnMethodSimplifiedGUI")
        
        self.mainLayout = qt.QVBoxLayout(self)
        self.logic = RynnMethodLogic()
        self.report_window = ReportWindow()
        self.data = {"report_window": self.report_window, "soft_tissue_node_name": "Rynn_soft_tissue"}
        
        # Add run number indicator
        self.run_label = qt.QLabel(f"<b>Current Run: {self.logic.run_number}</b>")
        self.run_label.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; font-size: 14px;")
        self.run_label.setAlignment(qt.Qt.AlignCenter)
        self.mainLayout.addWidget(self.run_label)
        
        self.step_widgets = []
        self.stepStack = qt.QStackedWidget()
        self.mainLayout.addWidget(self.stepStack)
        self.create_all_steps()
        self.setup_navigation()
        self.currentStep = 0
        self.update_ui()
    
    def updateRunLabel(self):
        """Update the run label when run number changes."""
        self.run_label.setText(f"<b>Current Run: {self.logic.run_number}</b>")
    
    def create_all_steps(self):
        steps_to_add = [
            ("Step 1: Welcome", StepWidget),
            ("Step 2: Landmark Setup", Step2_LandmarkSetup),
            ("Step 3: Plane Setup", Step3_PlaneSetup),
            ("Step 4: Scaffolding", Step4_Scaffolding),
            ("Step 5: Pronasale Anterior", Step5_PronasaleAnterior),
            ("Step 6: Pronasale Vertical", Step6_PronasaleVertical),
            ("Step 7: pFHP", Step7_PFH),
            ("Step 8: Soft Tissue sn", Step8_SoftTissueSN),
            ("Step 9: Nasion Prediction", Step9_Nasion),
            ("Step 10: Complete", Step10_Analysis)
        ]
        for title, TStep in steps_to_add:
            step_widget = TStep(title, self.logic, self.data, self)
            self.step_widgets.append(step_widget)
            self.stepStack.addWidget(step_widget)
    
    def get_selected_landmark_node(self):
        step2_widget = self.step_widgets[1]
        landmark_node = step2_widget.landmarksSelector.currentNode()
        if not landmark_node:
                        raise ValueError("Please select a Landmark Node in Step 2 first.")
        return landmark_node
    
    def setup_navigation(self):
        nav_widget = qt.QWidget()
        nav_layout = qt.QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        
        self.prevButton = qt.QPushButton("Previous")
        self.prevButton.clicked.connect(self.on_prev_button_clicked)
        
        self.stepLabel = qt.QLabel("")
        self.stepLabel.setAlignment(qt.Qt.AlignCenter)
        self.stepLabel.setStyleSheet("font-weight: bold;")
        
        self.nextButton = qt.QPushButton("Next")
        self.nextButton.clicked.connect(self.on_next_button_clicked)
        
        nav_layout.addWidget(self.prevButton)
        nav_layout.addStretch(1)
        nav_layout.addWidget(self.stepLabel)
        nav_layout.addStretch(1)
        nav_layout.addWidget(self.nextButton)
        
        self.mainLayout.addWidget(nav_widget)
    
    def update_ui(self):
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText(f"Step {self.currentStep + 1} / {self.stepStack.count}")
        is_last_step = (self.currentStep == self.stepStack.count - 1)
        self.nextButton.setText("Finish" if is_last_step else "Next")
        self.prevButton.setEnabled(self.currentStep > 0)
        self.step_widgets[self.currentStep].onEnterStep()
    
    def on_prev_button_clicked(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.update_ui()
    
    def on_next_button_clicked(self):
        if self.currentStep == self.stepStack.count - 1:
            self.report_window.close()
            self.close()
        else:
            self.currentStep += 1
            self.update_ui()

# =============================================================================
# ENTRY POINT - This starts everything!
# =============================================================================

try:
    if 'rynnGui' in globals() and rynnGui is not None:
        if hasattr(rynnGui, 'report_window') and rynnGui.report_window is not None:
            rynnGui.report_window.close()
        rynnGui.close()
        rynnGui = None
except (NameError, AttributeError):
    pass

rynnGui = RynnMethodSimplifiedGUI()
rynnGui.show()
print(f"\n✅ Rynn Method GUI loaded successfully!")
print(f"✅ Current run number: {rynnGui.logic.run_number}")
print(f"✅ Ready to go!")
print(f"✅ Report will show: PA_1_1: pred Rynn PA = 0.83*Y-3.5 = 26.14 mm")

```
