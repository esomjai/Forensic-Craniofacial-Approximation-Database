## Are you trying out multiple methods?

When there is overlap between the landmarks in different methods, it is tedious to re-allocate the same ones - not to mention, introducing possible inconsistencies. 

When using this GUI, you can export the coordinates of already existing landmarks into the "New" method's coordinates - so i f you had nasion at 0,0,0, in method1; and you have methosd2's landmark ALSO in the scene, the script compares the two for identical landmarks and copies the landmark coordinates from method1 to method2 - saving time for you.



```python
import json
import re
import numpy as np
import qt
import slicer

# Schema for landmark recognition
SCHEMA_JSON = r'''{"schemaVersion":"1.0.0","landmarks":[{"id":"HT-1","canonicalName":"Nasion","tissueType":"hard","aka":["nasion","N","n"]},{"id":"HT-2","canonicalName":"Inion","tissueType":"hard","aka":["inion"]},{"id":"HT-3","canonicalName":"Bregma","tissueType":"hard","aka":["bregma"]},{"id":"HT-4","canonicalName":"Prosthion","tissueType":"hard","aka":["prosthion","pr"]},{"id":"HT-5","canonicalName":"Subspinale","tissueType":"hard","aka":["subspinale","ss","point A"]},{"id":"HT-6","canonicalName":"Rhinion","tissueType":"hard","aka":["rhinion","R","rhi"]},{"id":"HT-7","canonicalName":"Acanthion / Anterior Nasal Spine","tissueType":"hard","aka":["acanthion","AC","ANS","ns","a"]},{"id":"HT-8","canonicalName":"Orbitale Left","tissueType":"hard","aka":["O_L"]},{"id":"HT-9","canonicalName":"Orbitale Right","tissueType":"hard","aka":["O_R"]},{"id":"HT-10","canonicalName":"Inferior Nasal Concha Left","tissueType":"hard","aka":["IC_L"]},{"id":"HT-11","canonicalName":"Inferior Nasal Concha Right","tissueType":"hard","aka":["IC_R"]},{"id":"HT-12","canonicalName":"Hard Tissue Alare Left","tissueType":"hard","aka":["A_L","alL","B (PA_L)"]},{"id":"HT-13","canonicalName":"Hard Tissue Alare Right","tissueType":"hard","aka":["A_R","alR","A (PA_R)"]},{"id":"HT-14","canonicalName":"Left Posterior Piriform Aperture Border","tissueType":"hard","aka":["NAG_L"]},{"id":"HT-15","canonicalName":"Right Posterior Piriform Aperture Border","tissueType":"hard","aka":["NAG_R"]},{"id":"HT-16","canonicalName":"Left Nasal Aperture Inferior","tissueType":"hard","aka":["NAI_L","LL","D (PAB_L)"]},{"id":"HT-17","canonicalName":"Right Nasal Aperture Inferior","tissueType":"hard","aka":["NAI_R","RL","C (PAB_R)"]},{"id":"HT-18","canonicalName":"Left Zygion","tissueType":"hard","aka":["zy_L"]},{"id":"HT-19","canonicalName":"Right Zygion","tissueType":"hard","aka":["zy_R"]},{"id":"HT-20","canonicalName":"Left Ectomolare","tissueType":"hard","aka":["ecm_L"]},{"id":"HT-21","canonicalName":"Right Ectomolare","tissueType":"hard","aka":["ecm_R"]},{"id":"HT-22","canonicalName":"Left Infraorbital Foramen","tissueType":"hard","aka":["iof_L"]},{"id":"HT-23","canonicalName":"Right Infraorbital Foramen","tissueType":"hard","aka":["iof_R"]},{"id":"HT-25","canonicalName":"Vomer-Maxillary Junction","tissueType":"hard","aka":["VMJ"]},{"id":"ST-1","canonicalName":"Soft Tissue Nasion","tissueType":"soft","aka":["soft nasion","n'","soft tissue nasion"]},{"id":"ST-2","canonicalName":"Subnasale","tissueType":"soft","aka":["subnasale","SN","sn'"]},{"id":"ST-3","canonicalName":"Pronasale","tissueType":"soft","aka":["pronasale","PN","prn","pn'"]},{"id":"ST-4","canonicalName":"Selion / Sellion","tissueType":"soft","aka":["S","se'"]},{"id":"ST-5","canonicalName":"Left Alar Groove / Curvature Superior","tissueType":"soft","aka":["ACS_L","als'L"]},{"id":"ST-6","canonicalName":"Right Alar Groove / Curvature Superior","tissueType":"soft","aka":["ACS_R","als'R"]},{"id":"ST-7","canonicalName":"Left Alar Groove / Curvature Posterior","tissueType":"soft","aka":["ACP_L","alp'L"]},{"id":"ST-8","canonicalName":"Right Alar Groove / Curvature Posterior","tissueType":"soft","aka":["ACP_R","alp'R"]},{"id":"ST-9","canonicalName":"Left Alare (Soft Tissue)","tissueType":"soft","aka":["NA_L","X1(alL)","al'L"]},{"id":"ST-10","canonicalName":"Right Alare (Soft Tissue)","tissueType":"soft","aka":["NA_R","X2(alR)","al'R"]},{"id":"ST-11","canonicalName":"Left Alar Groove / Curvature Inferior","tissueType":"soft","aka":["ACI_L","ali'L"]},{"id":"ST-12","canonicalName":"Right Alar Groove / Curvature Inferior","tissueType":"soft","aka":["ACI_R","ali'R"]},{"id":"ST-13","canonicalName":"Soft Tissue Rhinion","tissueType":"soft","aka":["rhi'"]},{"id":"ST-14","canonicalName":"Nasal Tip Inferior","tissueType":"soft","aka":["nt"]},{"id":"ST-15","canonicalName":"Left Nasal Base Attachment","tissueType":"soft","aka":["Y1(nbL)"]},{"id":"ST-16","canonicalName":"Right Nasal Base Attachment","tissueType":"soft","aka":["Y2(nbR)"]}]}'''

def _normalize_label(label):
    """Normalize a label for comparison."""
    if label is None:
        return ""
    s = str(label).lower().strip()
    s = s.replace("left", "_l").replace("right", "_r")
    s = s.replace("'", "").replace("`", "")
    s = re.sub(r"[^a-z0-9_]+", "", s)
    s = s.replace("__", "_")
    return s

class LandmarkMergerTool(qt.QDialog):
    """
    Landmark Merger Tool - Standalone window with exit button and improved styling.
    """
    
    def __init__(self, parent=None):
        super(LandmarkMergerTool, self).__init__(parent)
        self.setWindowTitle("Landmark Merger Tool")
        self.setMinimumSize(850, 650)
        self.setMaximumSize(1200, 800)
        self.setModal(False)
        
        # Set window flags to make it a proper window
        self.setWindowFlags(qt.Qt.Window | qt.Qt.WindowCloseButtonHint | qt.Qt.WindowMinimizeButtonHint)
        
        # Apply dark/light theme based on system
        self._applyTheme()
        
        self.schema = json.loads(SCHEMA_JSON)
        self.landmarkById = {lm["id"]: lm for lm in self.schema["landmarks"]}
        
        # Build alias index
        self._buildAliasIndex()
        
        # Storage for comparison results
        self.matches = []
        
        self._buildUI()
        
    def _applyTheme(self):
        """Apply a clean modern theme."""
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #d0d7de;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                border-radius: 5px;
                padding: 6px 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.7;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 1px solid #d0d7de;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QComboBox {
                padding: 4px;
                border: 1px solid #d0d7de;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
        """)
    
    def _buildAliasIndex(self):
        """Build the alias-to-landmark mapping."""
        self.aliasToLandmarkIdsExact = {}
        self.aliasToLandmarkIdsNormalized = {}
        for lm in self.schema["landmarks"]:
            values = [lm["canonicalName"]] + lm.get("aka", [])
            for v in values:
                if str(v) not in self.aliasToLandmarkIdsExact:
                    self.aliasToLandmarkIdsExact[str(v)] = []
                self.aliasToLandmarkIdsExact[str(v)].append(lm["id"])
                
                norm_v = _normalize_label(v)
                if norm_v not in self.aliasToLandmarkIdsNormalized:
                    self.aliasToLandmarkIdsNormalized[norm_v] = []
                self.aliasToLandmarkIdsNormalized[norm_v].append(lm["id"])
    
    def _buildUI(self):
        """Build the user interface with standalone window styling."""
        # Main layout
        mainLayout = qt.QVBoxLayout(self)
        mainLayout.setSpacing(10)
        mainLayout.setContentsMargins(15, 15, 15, 15)
        
        # Header with title
        headerLayout = qt.QHBoxLayout()
        
        # Title with icon
        titleLabel = qt.QLabel("🔬 Landmark Merger Tool")
        titleLabel.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 3px;
        """)
        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch()
        
        mainLayout.addLayout(headerLayout)
        
        # Description with better formatting
        descBox = qt.QGroupBox()
        descLayout = qt.QVBoxLayout(descBox)
        descLayout.setContentsMargins(10, 5, 10, 5)
        
        desc = qt.QLabel(
            "Compare two landmark files and selectively import coordinates from one to another.\n"
            "Useful for merging landmarks from previous analyses with new sets."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #555555;
            font-size: 12px;
            background-color: #f8f9fa;
            padding: 6px;
            border-radius: 4px;
        """)
        descLayout.addWidget(desc)
        mainLayout.addWidget(descBox)
        
        # File selection section
        filesBox = qt.QGroupBox("📂 Select Landmark Files to Compare")
        filesLayout = qt.QFormLayout(filesBox)
        filesLayout.setSpacing(6)
        filesLayout.setContentsMargins(10, 15, 10, 10)
        
        # Source file
        self.sourceSelector = slicer.qMRMLNodeComboBox()
        self.sourceSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.sourceSelector.noneEnabled = True
        self.sourceSelector.addEnabled = False
        self.sourceSelector.removeEnabled = False
        self.sourceSelector.setMRMLScene(slicer.mrmlScene)
        self.sourceSelector.setToolTip("Select the source landmark file (coordinates will be imported FROM this file)")
        self.sourceSelector.setMinimumHeight(25)
        
        # Target file
        self.targetSelector = slicer.qMRMLNodeComboBox()
        self.targetSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.targetSelector.noneEnabled = True
        self.targetSelector.addEnabled = False
        self.targetSelector.removeEnabled = False
        self.targetSelector.setMRMLScene(slicer.mrmlScene)
        self.targetSelector.setToolTip("Select the target landmark file (coordinates will be imported TO this file)")
        self.targetSelector.setMinimumHeight(25)
        
        filesLayout.addRow("📤 Source (Import FROM):", self.sourceSelector)
        filesLayout.addRow("📥 Target (Import TO):", self.targetSelector)
        
        mainLayout.addWidget(filesBox)
        
        # Compare button
        btnLayout = qt.QHBoxLayout()
        btnLayout.setContentsMargins(0, 3, 0, 3)
        
        self.compareBtn = qt.QPushButton("🔍 Compare Landmarks")
        self.compareBtn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px 25px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.compareBtn.setMinimumHeight(32)
        self.compareBtn.clicked.connect(self.compareLandmarks)
        
        btnLayout.addStretch()
        btnLayout.addWidget(self.compareBtn)
        btnLayout.addStretch()
        mainLayout.addLayout(btnLayout)
        
        # Results table section
        resultsBox = qt.QGroupBox("📋 Matching Landmarks")
        resultsLayout = qt.QVBoxLayout(resultsBox)
        resultsLayout.setContentsMargins(10, 15, 10, 10)
        
        # Instructions
        instr = qt.QLabel(
            "✓ Check the box to import coordinates from the Source file\n"
            "✗ Uncheck to keep the Target file's coordinates"
        )
        instr.setWordWrap(True)
        instr.setStyleSheet("""
            color: #555555;
            background-color: #f8f9fa;
            padding: 5px;
            border-radius: 4px;
            font-size: 11px;
        """)
        resultsLayout.addWidget(instr)
        
        # Results table - make it compact
        self.resultsTable = qt.QTableWidget()
        self.resultsTable.setColumnCount(6)
        self.resultsTable.setHorizontalHeaderLabels([
            "Use Source", "ID", "Canonical Name", 
            "Source Label", "Target Label", "Status"
        ])
        self.resultsTable.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)
        self.resultsTable.verticalHeader().setVisible(False)
        self.resultsTable.setMinimumHeight(200)
        self.resultsTable.setMaximumHeight(400)
        self.resultsTable.setAlternatingRowColors(True)
        
        # Set column widths
        self.resultsTable.setColumnWidth(0, 70)
        self.resultsTable.setColumnWidth(1, 80)
        self.resultsTable.setColumnWidth(2, 180)
        self.resultsTable.setColumnWidth(3, 130)
        self.resultsTable.setColumnWidth(4, 130)
        self.resultsTable.setColumnWidth(5, 90)
        
        resultsLayout.addWidget(self.resultsTable)
        mainLayout.addWidget(resultsBox)
        
        # Action buttons
        actionLayout = qt.QHBoxLayout()
        actionLayout.setSpacing(8)
        
        self.selectAllBtn = qt.QPushButton("✅ Select All")
        self.selectAllBtn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.selectAllBtn.clicked.connect(self.selectAll)
        
        self.selectNoneBtn = qt.QPushButton("❌ Select None")
        self.selectNoneBtn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.selectNoneBtn.clicked.connect(self.selectNone)
        
        self.applyBtn = qt.QPushButton("📥 Apply Selected Changes")
        self.applyBtn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                padding: 8px 25px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #ecf0f1;
            }
        """)
        self.applyBtn.clicked.connect(self.applyChanges)
        self.applyBtn.setEnabled(False)
        self.applyBtn.setMinimumHeight(32)
        
        actionLayout.addWidget(self.selectAllBtn)
        actionLayout.addWidget(self.selectNoneBtn)
        actionLayout.addStretch(1)
        actionLayout.addWidget(self.applyBtn)
        mainLayout.addLayout(actionLayout)
        
        # Delete source file button (optional)
        deleteLayout = qt.QHBoxLayout()
        deleteLayout.setContentsMargins(0, 2, 0, 2)
        
        self.deleteBtn = qt.QPushButton("🗑️ Delete Source File (Optional)")
        self.deleteBtn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #ecf0f1;
            }
        """)
        self.deleteBtn.clicked.connect(self.deleteSourceFile)
        self.deleteBtn.setEnabled(False)
        self.deleteBtn.setMinimumHeight(28)
        
        deleteLayout.addStretch()
        deleteLayout.addWidget(self.deleteBtn)
        mainLayout.addLayout(deleteLayout)
        
        # Status bar
        self.status = qt.QLabel("🔹 Ready - Select two landmark files and click 'Compare Landmarks'")
        self.status.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                padding: 6px;
                border-radius: 4px;
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        self.status.setMinimumHeight(28)
        mainLayout.addWidget(self.status)
        
        # Footer with version info
        footerLayout = qt.QHBoxLayout()
        footerLayout.setContentsMargins(0, 2, 0, 0)
        
        footer = qt.QLabel("Landmark Merger Tool v1.0 | 3D Slicer compatible")
        footer.setStyleSheet("""
            color: #7f8c8d;
            font-size: 10px;
            padding: 3px;
        """)
        footerLayout.addWidget(footer)
        footerLayout.addStretch()
        mainLayout.addLayout(footerLayout)
        
    def _collectNodeLabels(self, node):
        """Collect all labels from a landmark node."""
        labels = []
        if not node:
            return labels
        for i in range(node.GetNumberOfControlPoints()):
            labels.append((i, node.GetNthControlPointLabel(i)))
        return labels
    
    def _findLandmarkId(self, label):
        """Find the landmark ID for a given label using the schema."""
        # First try exact match
        if label in self.aliasToLandmarkIdsExact:
            ids = self.aliasToLandmarkIdsExact[label]
            if len(ids) == 1:
                return ids[0]
        
        # Then try normalized match
        norm = _normalize_label(label)
        if norm in self.aliasToLandmarkIdsNormalized:
            ids = self.aliasToLandmarkIdsNormalized[norm]
            if len(ids) == 1:
                return ids[0]
        
        return None
    
    def _getSourceLandmarkIds(self, sourceNode):
        """Get all landmark IDs present in the source node."""
        sourceIds = set()
        if sourceNode:
            for i in range(sourceNode.GetNumberOfControlPoints()):
                label = sourceNode.GetNthControlPointLabel(i)
                lm_id = self._findLandmarkId(label)
                if lm_id:
                    sourceIds.add(lm_id)
        return sourceIds
    
    def _getTargetLandmarkIds(self, targetNode):
        """Get all landmark IDs present in the target node."""
        targetIds = set()
        if targetNode:
            for i in range(targetNode.GetNumberOfControlPoints()):
                label = targetNode.GetNthControlPointLabel(i)
                lm_id = self._findLandmarkId(label)
                if lm_id:
                    targetIds.add(lm_id)
        return targetIds
    
    def _getUnmatchedTargetLandmarks(self, sourceNode, targetNode):
        """
        Get list of landmark IDs that are present in target but NOT in source.
        These landmarks will NOT be updated (no source coordinates to import from).
        """
        sourceIds = self._getSourceLandmarkIds(sourceNode)
        targetIds = self._getTargetLandmarkIds(targetNode)
        unmatchedIds = targetIds - sourceIds
        unmatchedLandmarks = []
        for lm_id in sorted(unmatchedIds):
            unmatchedLandmarks.append({
                'id': lm_id,
                'canonicalName': self.landmarkById[lm_id]['canonicalName'],
                'tissueType': self.landmarkById[lm_id]['tissueType']
            })
        return unmatchedLandmarks
    
    def compareLandmarks(self):
        """Compare landmarks between source and target files."""
        sourceNode = self.sourceSelector.currentNode()
        targetNode = self.targetSelector.currentNode()
        
        if not sourceNode or not targetNode:
            self._setStatus("❌ Error: Please select both source and target landmark files", "error")
            return
        
        if sourceNode == targetNode:
            self._setStatus("❌ Error: Source and target files must be different", "error")
            return
        
        # Collect labels from both nodes
        sourceLabels = self._collectNodeLabels(sourceNode)
        targetLabels = self._collectNodeLabels(targetNode)
        
        if not sourceLabels:
            self._setStatus("❌ Error: Source file has no landmarks", "error")
            return
        
        if not targetLabels:
            self._setStatus("❌ Error: Target file has no landmarks", "error")
            return
        
        # Find matches
        self.matches = []
        
        for sourceIdx, sourceLabel in sourceLabels:
            # Try to match this label to a landmark ID
            sourceLandmarkId = self._findLandmarkId(sourceLabel)
            
            if sourceLandmarkId:
                canonicalName = self.landmarkById[sourceLandmarkId]["canonicalName"]
                
                # Look for matching landmark in target
                targetIdx = None
                targetLabel = None
                
                # First try to find exact landmark ID match
                for tIdx, tLabel in targetLabels:
                    tLandmarkId = self._findLandmarkId(tLabel)
                    if tLandmarkId == sourceLandmarkId:
                        targetIdx = tIdx
                        targetLabel = tLabel
                        break
                
                # If no exact match, try to find a label that maps to the same canonical name
                if targetIdx is None:
                    for tIdx, tLabel in targetLabels:
                        tLandmarkId = self._findLandmarkId(tLabel)
                        if tLandmarkId and self.landmarkById[tLandmarkId]["canonicalName"] == canonicalName:
                            targetIdx = tIdx
                            targetLabel = tLabel
                            break
                
                if targetIdx is not None:
                    # Found a match - store the source and target indices for coordinate transfer
                    self.matches.append({
                        'landmark_id': sourceLandmarkId,
                        'canonical_name': canonicalName,
                        'source_idx': sourceIdx,
                        'source_label': sourceLabel,
                        'target_idx': targetIdx,
                        'target_label': targetLabel,
                        'use_source': True  # Default to using source coordinates
                    })
        
        # Sort matches by canonical name
        self.matches.sort(key=lambda x: x['canonical_name'])
        
        # Update the table
        self._updateTable()
        
        # Show unmatched target landmarks notification (landmarks in target but not in source)
        self._showUnmatchedTargetNotification(sourceNode, targetNode)
        
        # Update status
        if self.matches:
            self._setStatus("✅ Found " + str(len(self.matches)) + " matching landmarks. Select which coordinates to import.", "success")
            self.applyBtn.setEnabled(True)
            self.deleteBtn.setEnabled(True)
        else:
            self._setStatus("⚠️ No matching landmarks found between the two files", "warning")
            self.applyBtn.setEnabled(False)
            self.deleteBtn.setEnabled(False)
    
    def _setStatus(self, message, status_type="info"):
        """Set the status bar with appropriate styling."""
        styles = {
            "info": "background-color:#ecf0f1; padding:6px; border-radius:4px; color:#2c3e50; font-weight:bold; font-size:12px;",
            "success": "background-color:#e8f8f5; padding:6px; border-radius:4px; color:#1a7a5a; font-weight:bold; font-size:12px;",
            "error": "background-color:#fde8e8; padding:6px; border-radius:4px; color:#c0392b; font-weight:bold; font-size:12px;",
            "warning": "background-color:#fef9e7; padding:6px; border-radius:4px; color:#b7950b; font-weight:bold; font-size:12px;"
        }
        self.status.setText(message)
        self.status.setStyleSheet(styles.get(status_type, styles["info"]))
    
    def _showUnmatchedTargetNotification(self, sourceNode, targetNode):
        """
        Show a notification about landmarks that are in target but NOT in source.
        These landmarks will NOT be updated during the merge.
        """
        unmatchedLandmarks = self._getUnmatchedTargetLandmarks(sourceNode, targetNode)
        
        if unmatchedLandmarks:
            # Group by tissue type
            hard_unmatched = [lm for lm in unmatchedLandmarks if lm['tissueType'] == 'hard']
            soft_unmatched = [lm for lm in unmatchedLandmarks if lm['tissueType'] == 'soft']
            
            # Create message
            msg = "📋 LANDMARKS IN TARGET BUT NOT IN SOURCE\n"
            msg += "=" * 65 + "\n\n"
            msg += "The following landmarks exist in the TARGET file but are NOT present in the SOURCE file.\n"
            msg += "They will NOT be updated during the merge (no source coordinates available).\n\n"
            
            if hard_unmatched:
                msg += "🔷 HARD TISSUE LANDMARKS (" + str(len(hard_unmatched)) + "):\n"
                for lm in hard_unmatched:
                    msg += "  • " + lm['id'] + ": " + lm['canonicalName'] + "\n"
                msg += "\n"
            
            if soft_unmatched:
                msg += "🔶 SOFT TISSUE LANDMARKS (" + str(len(soft_unmatched)) + "):\n"
                for lm in soft_unmatched:
                    msg += "  • " + lm['id'] + ": " + lm['canonicalName'] + "\n"
                msg += "\n"
            
            msg += "Total landmarks that will NOT be updated: " + str(len(unmatchedLandmarks))
            
            # Show the message in a dialog
            msgBox = qt.QMessageBox(self)
            msgBox.setWindowTitle("Landmarks Not to be Updated")
            msgBox.setText(msg)
            msgBox.setIcon(qt.QMessageBox.Information)
            msgBox.setStandardButtons(qt.QMessageBox.Ok)
            msgBox.setSizeGripEnabled(True)
            msgBox.exec_()
            
            # Also update status
            self._setStatus("ℹ️ " + str(len(unmatchedLandmarks)) + " target landmarks have no source match - will NOT be updated", "info")
        else:
            # All target landmarks have matches in source
            targetIds = self._getTargetLandmarkIds(targetNode)
            if targetIds:
                msgBox = qt.QMessageBox(self)
                msgBox.setWindowTitle("Complete Match!")
                msgBox.setText("✅ All target landmarks have matches in the source file!\n\n"
                              "All " + str(len(targetIds)) + " landmarks from the target file\n"
                              "have corresponding landmarks in the source file.\n\n"
                              "They can all be updated with source coordinates.")
                msgBox.setIcon(qt.QMessageBox.Information)
                msgBox.setStandardButtons(qt.QMessageBox.Ok)
                msgBox.exec_()
                
                self._setStatus("✅ All target landmarks have source matches", "success")
    
    def _updateTable(self):
        """Update the results table with current matches."""
        self.resultsTable.setRowCount(len(self.matches))
        
        for row, match in enumerate(self.matches):
            # Checkbox cell - Use Source
            checkbox = qt.QCheckBox()
            checkbox.setChecked(match['use_source'])
            checkbox.stateChanged.connect(lambda state, r=row: self._onCheckboxChanged(r, state))
            self.resultsTable.setCellWidget(row, 0, checkbox)
            
            # Landmark ID
            item = qt.QTableWidgetItem(match['landmark_id'])
            item.setTextAlignment(qt.Qt.AlignCenter)
            self.resultsTable.setItem(row, 1, item)
            
            # Canonical Name
            item = qt.QTableWidgetItem(match['canonical_name'])
            self.resultsTable.setItem(row, 2, item)
            
            # Source Label
            item = qt.QTableWidgetItem(match['source_label'])
            self.resultsTable.setItem(row, 3, item)
            
            # Target Label
            item = qt.QTableWidgetItem(match['target_label'])
            self.resultsTable.setItem(row, 4, item)
            
            # Status
            status = "✓ OK"
            statusColor = "#27ae60"
            sourceNode = self.sourceSelector.currentNode()
            targetNode = self.targetSelector.currentNode()
            if sourceNode and targetNode:
                try:
                    sourcePos = sourceNode.GetNthControlPointPosition(match['source_idx'])
                    targetPos = targetNode.GetNthControlPointPosition(match['target_idx'])
                    if np.isnan(sourcePos[0]) or np.isnan(targetPos[0]):
                        status = "⚠ Missing"
                        statusColor = "#e67e22"
                    elif np.allclose(sourcePos, targetPos, rtol=1e-5, atol=1e-5):
                        status = "✓ Identical"
                        statusColor = "#3498db"
                    else:
                        status = "✓ Different"
                        statusColor = "#27ae60"
                except:
                    status = "✗ Error"
                    statusColor = "#e74c3c"
            
            item = qt.QTableWidgetItem(status)
            item.setTextAlignment(qt.Qt.AlignCenter)
            item.setForeground(qt.QColor(statusColor))
            self.resultsTable.setItem(row, 5, item)
    
    def _onCheckboxChanged(self, row, state):
        """Handle checkbox state change."""
        if row < len(self.matches):
            self.matches[row]['use_source'] = (state == qt.Qt.Checked)
    
    def selectAll(self):
        """Select all checkboxes."""
        for row in range(self.resultsTable.rowCount()):
            checkbox = self.resultsTable.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(True)
                self.matches[row]['use_source'] = True
    
    def selectNone(self):
        """Deselect all checkboxes."""
        for row in range(self.resultsTable.rowCount()):
            checkbox = self.resultsTable.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(False)
                self.matches[row]['use_source'] = False
    
    def _isNodeLocked(self, node):
        """Check if a node is locked (compatible with different Slicer versions)."""
        try:
            return node.locked
        except AttributeError:
            try:
                return node.IsLocked()
            except AttributeError:
                return False
    
    def _setNodeLocked(self, node, locked):
        """Set node locked state (compatible with different Slicer versions)."""
        try:
            node.locked = locked
        except AttributeError:
            try:
                if locked:
                    node.Lock()
                else:
                    node.Unlock()
            except AttributeError:
                pass
    
    def deleteSourceFile(self):
        """Optional: Delete the source landmark file."""
        sourceNode = self.sourceSelector.currentNode()
        if not sourceNode:
            return
        
        # Confirm deletion
        reply = qt.QMessageBox.question(
            self,
            "Delete Source File?",
            "Are you sure you want to delete the source landmark file?\n\n"
            "File: " + sourceNode.GetName() + "\n\n"
            "This action cannot be undone.",
            qt.QMessageBox.Yes | qt.QMessageBox.No
        )
        
        if reply == qt.QMessageBox.Yes:
            try:
                scene = slicer.mrmlScene
                scene.RemoveNode(sourceNode)
                self._setStatus("🗑️ Source file deleted: " + sourceNode.GetName(), "info")
                self.sourceSelector.setCurrentNode(None)
                self.deleteBtn.setEnabled(False)
                self.applyBtn.setEnabled(False)
                self.matches = []
                self.resultsTable.setRowCount(0)
            except Exception as e:
                self._setStatus("❌ Error deleting file: " + str(e), "error")
    
    def applyChanges(self):
        """Apply the selected coordinate changes - ONLY updates RAS coordinates, preserves everything else."""
        sourceNode = self.sourceSelector.currentNode()
        targetNode = self.targetSelector.currentNode()
        
        if not sourceNode or not targetNode:
            self._setStatus("❌ Error: Source or target node not available", "error")
            return
        
        if not self.matches:
            self._setStatus("⚠️ No matches to apply", "warning")
            return
        
        # Check if we can modify the target node
        if self._isNodeLocked(targetNode):
            reply = qt.QMessageBox.question(
                self,
                "Node Locked",
                "The target landmark file is locked. Do you want to unlock it to apply changes?",
                qt.QMessageBox.Yes | qt.QMessageBox.No
            )
            if reply == qt.QMessageBox.Yes:
                self._setNodeLocked(targetNode, False)
            else:
                self._setStatus("⚠️ Operation cancelled - target file is locked", "warning")
                return
        
        # Apply changes - ONLY update coordinates, preserve everything else
        changesApplied = 0
        changesSkipped = 0
        updatedLandmarks = []
        skippedLandmarks = []
        
        # Store original target state for verification
        originalTargetCount = targetNode.GetNumberOfControlPoints()
        originalTargetLabels = []
        for i in range(originalTargetCount):
            originalTargetLabels.append(targetNode.GetNthControlPointLabel(i))
        
        for match in self.matches:
            if match['use_source']:
                try:
                    # Get source position
                    sourcePos = sourceNode.GetNthControlPointPosition(match['source_idx'])
                    
                    # Check if source position is valid
                    if np.isnan(sourcePos[0]) or np.isnan(sourcePos[1]) or np.isnan(sourcePos[2]):
                        changesSkipped += 1
                        skippedLandmarks.append(match['canonical_name'] + " (invalid source position)")
                        continue
                    
                    # Get current target position
                    targetPos = targetNode.GetNthControlPointPosition(match['target_idx'])
                    
                    # Check if coordinates are already the same
                    if np.allclose(sourcePos, targetPos, rtol=1e-5, atol=1e-5):
                        changesSkipped += 1
                        skippedLandmarks.append(match['canonical_name'] + " (already identical)")
                        continue
                    
                    # ONLY update the RAS coordinates - preserve label, description, etc.
                    targetNode.SetNthControlPointPosition(match['target_idx'], sourcePos[0], sourcePos[1], sourcePos[2])
                    
                    changesApplied += 1
                    updatedLandmarks.append(match['canonical_name'])
                    
                except Exception as e:
                    self._setStatus("❌ Error applying change for " + match['canonical_name'] + ": " + str(e), "error")
                    return
        
        # Verify target file integrity - number of points should not change
        finalTargetCount = targetNode.GetNumberOfControlPoints()
        if finalTargetCount != originalTargetCount:
            self._setStatus("❌ Error: Target file point count changed! This should not happen.", "error")
            return
        
        # Update the table and status
        self._updateTable()
        
        # Show landmarks that are in target but not in source (unmatched)
        unmatchedLandmarks = self._getUnmatchedTargetLandmarks(sourceNode, targetNode)
        
        # Create summary message
        summary = "📊 MERGE COMPLETE\n"
        summary += "=" * 65 + "\n\n"
        
        if changesApplied > 0:
            summary += "✅ Successfully updated coordinates for " + str(changesApplied) + " landmark(s):\n"
            for name in updatedLandmarks:
                summary += "  ✓ " + name + " (coordinates updated)\n"
            summary += "\n"
        else:
            summary += "ℹ️ No coordinates were updated.\n\n"
        
        if changesSkipped > 0:
            summary += "⏭️ Skipped " + str(changesSkipped) + " landmark(s):\n"
            for skip in skippedLandmarks:
                summary += "  • " + skip + "\n"
            summary += "\n"
        
        # Report landmarks that are in target but NOT in source (won't be updated)
        if unmatchedLandmarks:
            summary += "📋 LANDMARKS IN TARGET BUT NOT IN SOURCE (" + str(len(unmatchedLandmarks)) + "):\n"
            summary += "   These landmarks exist in target but not in source.\n"
            summary += "   They were NOT updated (no source coordinates available).\n\n"
            hard_unmatched = [lm for lm in unmatchedLandmarks if lm['tissueType'] == 'hard']
            soft_unmatched = [lm for lm in unmatchedLandmarks if lm['tissueType'] == 'soft']
            
            if hard_unmatched:
                summary += "  🔷 Hard tissue:\n"
                for lm in hard_unmatched:
                    summary += "    • " + lm['id'] + ": " + lm['canonicalName'] + "\n"
            
            if soft_unmatched:
                summary += "  🔶 Soft tissue:\n"
                for lm in soft_unmatched:
                    summary += "    • " + lm['id'] + ": " + lm['canonicalName'] + "\n"
        else:
            targetIds = self._getTargetLandmarkIds(targetNode)
            if targetIds:
                summary += "🎉 ALL " + str(len(targetIds)) + " target landmarks have matches in the source file!\n"
                summary += "   All available landmarks have been updated."
        
        summary += "\n\n📌 Note: Only RAS coordinates were updated. All labels, descriptions, and "
        summary += "point count remain unchanged. No landmarks were duplicated or renamed."
        
        # Add option to delete source file
        summary += "\n\n💡 Tip: You can now delete the source file using the 'Delete Source File' button below."
        
        # Show the summary dialog
        msgBox = qt.QMessageBox(self)
        msgBox.setWindowTitle("Merge Summary")
        msgBox.setText(summary)
        msgBox.setIcon(qt.QMessageBox.Warning if unmatchedLandmarks else qt.QMessageBox.Information)
        msgBox.setStandardButtons(qt.QMessageBox.Ok)
        msgBox.setSizeGripEnabled(True)
        msgBox.exec_()
        
        # Update status
        if changesApplied > 0:
            self._setStatus("✅ Updated coordinates for " + str(changesApplied) + " landmark(s). " + 
                          str(len(unmatchedLandmarks)) + " target landmarks have no source match.", "success")
            self.deleteBtn.setEnabled(True)
        else:
            self._setStatus("ℹ️ No coordinates were updated. " + str(len(unmatchedLandmarks)) + " target landmarks have no source match.", "warning")
            self.deleteBtn.setEnabled(True)
    
    def closeEvent(self, event):
        """Handle close event."""
        event.accept()

# Function to launch the tool
def launchLandmarkMerger():
    """Launch the Landmark Merger Tool as a standalone window."""
    # Check if there's already an instance
    for widget in qt.QApplication.topLevelWidgets():
        if isinstance(widget, LandmarkMergerTool):
            widget.raise_()
            widget.activateWindow()
            widget.show()
            return widget
    
    # Create new instance
    merger = LandmarkMergerTool(slicer.util.mainWindow())
    merger.show()
    return merger

# Launch the tool as a standalone window
merger = launchLandmarkMerger()


```
