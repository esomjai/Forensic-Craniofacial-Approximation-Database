``` python

import numpy as np
import slicer
import qt
import vtk
import urllib.request
import tempfile
import os

class PurkaitSinghGUI(qt.QWidget):
        def createStep4_FSTTChoices(self):
            widget = qt.QWidget()
            layout = qt.QVBoxLayout(widget)
            layout.setSpacing(15)

            title = qt.QLabel("Step 4: Set Facial Soft Tissue Thickness (FSTT) Values")
            title.setStyleSheet("font-weight: bold; font-size: 16px;")
            layout.addWidget(title)

            desc = qt.QLabel(
                "Set the FSTT values for subnasale (sn') and nasion (n'). You can choose male, female, or non-sex-specific values.\n"
                "Non-sex-specific FSTT is always available as an option for prediction, but is not tied to a specific regression equation.\n"
                "All FSTT options will be available for all predictions, and the FSTT used for each prediction will be shown in the results."
            )
            desc.setWordWrap(True)
            layout.addWidget(desc)

            # FSTT for sn'
            snGroup = qt.QGroupBox("FSTT for Subnasale (sn')")
            snLayout = qt.QVBoxLayout(snGroup)
            snExplanation = qt.QLabel(
                "The FSTT at subnasale (sn') is used to predict the soft tissue position from the hard tissue landmark 'subspinale (ss)'.\n"
                "Male: 11.61±1.6mm (Purkait & Singh 2024)\n"
                "Female: 10.27±10.62mm (Purkait & Singh 2024)\n"
                "Not sex-specific: 13.5±3.5mm (Hona et al. 2024)"
            )
            snExplanation.setWordWrap(True)
            snExplanation.setStyleSheet("font-style: italic; color: #555;")
            snLayout.addWidget(snExplanation)

            snSexLayout = qt.QHBoxLayout()
            self.snMaleCheckbox = qt.QCheckBox("Male")
            self.snFemaleCheckbox = qt.QCheckBox("Female")
            self.snNonSexCheckbox = qt.QCheckBox("Not sex-specific")
            self.snMaleCheckbox.setChecked(True)
            self.snMaleCheckbox.toggled.connect(self.onSnSexChanged)
            self.snFemaleCheckbox.toggled.connect(self.onSnSexChanged)
            self.snNonSexCheckbox.toggled.connect(self.onSnSexChanged)
            snSexLayout.addWidget(self.snMaleCheckbox)
            snSexLayout.addWidget(self.snFemaleCheckbox)
            snSexLayout.addWidget(self.snNonSexCheckbox)
            snSexLayout.addStretch()
            snLayout.addLayout(snSexLayout)

            # Sliders for sn'
            self.snMaleSlider = qt.QSlider(qt.Qt.Horizontal)
            self.snMaleSlider.setRange(0, 100)
            self.snMaleSlider.setValue(50)
            self.snMaleSlider.valueChanged.connect(self.onSnMaleSliderChanged)
            self.snMaleLabel = qt.QLabel("FSTT sn' (Male): 11.61 mm")
            self.snMaleLabel.setStyleSheet("font-weight: bold;")
            snLayout.addWidget(self.snMaleLabel)
            snLayout.addWidget(self.snMaleSlider)
            self.snMaleRangeLabel = qt.QLabel("Range: -SD (10.01 mm) ← Mean (11.61 mm) → +SD (13.21 mm) [Adjustable beyond limits]")
            self.snMaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
            snLayout.addWidget(self.snMaleRangeLabel)

            self.snFemaleSlider = qt.QSlider(qt.Qt.Horizontal)
            self.snFemaleSlider.setRange(0, 100)
            self.snFemaleSlider.setValue(50)
            self.snFemaleSlider.valueChanged.connect(self.onSnFemaleSliderChanged)
            self.snFemaleSlider.setVisible(False)
            self.snFemaleLabel = qt.QLabel("FSTT sn' (Female): 10.27 mm")
            self.snFemaleLabel.setStyleSheet("font-weight: bold;")
            self.snFemaleLabel.setVisible(False)
            snLayout.addWidget(self.snFemaleLabel)
            snLayout.addWidget(self.snFemaleSlider)

            self.snFemaleRangeLabel = qt.QLabel("Range: -SD (-0.35 mm) ← Mean (10.27 mm) → +SD (20.89 mm) [Adjustable beyond limits]")
            self.snFemaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
            self.snFemaleRangeLabel.setVisible(False)
            snLayout.addWidget(self.snFemaleRangeLabel)

            self.snNonSexSlider = qt.QSlider(qt.Qt.Horizontal)
            self.snNonSexSlider.setRange(0, 100)
            self.snNonSexSlider.setValue(50)
            self.snNonSexSlider.valueChanged.connect(self.onSnNonSexSliderChanged)
            self.snNonSexSlider.setVisible(False)
            self.snNonSexLabel = qt.QLabel("FSTT sn' (Non-sex-specific): 13.5 mm")
            self.snNonSexLabel.setStyleSheet("font-weight: bold;")
            self.snNonSexLabel.setVisible(False)
            snLayout.addWidget(self.snNonSexLabel)
            snLayout.addWidget(self.snNonSexSlider)

            self.snNonSexRangeLabel = qt.QLabel("Range: -SD (10.0 mm) ← Mean (13.5 mm) → +SD (17.0 mm) [Adjustable beyond limits]")
            self.snNonSexRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
            self.snNonSexRangeLabel.setVisible(False)
            snLayout.addWidget(self.snNonSexRangeLabel)

            layout.addWidget(snGroup)

            # FSTT for n'
            nGroup = qt.QGroupBox("FSTT for Nasion (n')")
            nLayout = qt.QVBoxLayout(nGroup)
            nExplanation = qt.QLabel(
                "The FSTT at nasion (n') is used to predict the soft tissue position from the hard tissue landmark 'nasion (n)'.\n"
                "Male: 5.02±0.99mm (Purkait & Singh 2024)\n"
                "Female: 3.97±0.92mm (Purkait & Singh 2024)\n"
                "Not sex-specific: 6.0±1.5mm (Hona et al. 2024)"
            )
            nExplanation.setWordWrap(True)
            nExplanation.setStyleSheet("font-style: italic; color: #555;")
            nLayout.addWidget(nExplanation)

            nSexLayout = qt.QHBoxLayout()
            self.nMaleCheckbox = qt.QCheckBox("Male")
            self.nFemaleCheckbox = qt.QCheckBox("Female")
            self.nNonSexCheckbox = qt.QCheckBox("Not sex-specific")
            self.nMaleCheckbox.setChecked(True)
            self.nMaleCheckbox.toggled.connect(self.onNSexChanged)
            self.nFemaleCheckbox.toggled.connect(self.onNSexChanged)
            self.nNonSexCheckbox.toggled.connect(self.onNSexChanged)
            nSexLayout.addWidget(self.nMaleCheckbox)
            nSexLayout.addWidget(self.nFemaleCheckbox)
            nSexLayout.addWidget(self.nNonSexCheckbox)
            nSexLayout.addStretch()
            nLayout.addLayout(nSexLayout)

            self.nMaleSlider = qt.QSlider(qt.Qt.Horizontal)
            self.nMaleSlider.setRange(0, 100)
            self.nMaleSlider.setValue(50)
            self.nMaleSlider.valueChanged.connect(self.onNMaleSliderChanged)
            self.nMaleLabel = qt.QLabel("FSTT n' (Male): 5.02 mm")
            self.nMaleLabel.setStyleSheet("font-weight: bold;")
            nLayout.addWidget(self.nMaleLabel)
            nLayout.addWidget(self.nMaleSlider)

            self.nMaleRangeLabel = qt.QLabel("Range: -SD (4.03 mm) ← Mean (5.02 mm) → +SD (6.01 mm) [Adjustable beyond limits]")
            self.nMaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
            nLayout.addWidget(self.nMaleRangeLabel)

            self.nFemaleSlider = qt.QSlider(qt.Qt.Horizontal)
            self.nFemaleSlider.setRange(0, 100)
            self.nFemaleSlider.setValue(50)
            self.nFemaleSlider.valueChanged.connect(self.onNFemaleSliderChanged)
            self.nFemaleSlider.setVisible(False)
            self.nFemaleLabel = qt.QLabel("FSTT n' (Female): 3.97 mm")
            self.nFemaleLabel.setStyleSheet("font-weight: bold;")
            self.nFemaleLabel.setVisible(False)
            nLayout.addWidget(self.nFemaleLabel)
            nLayout.addWidget(self.nFemaleSlider)

            self.nFemaleRangeLabel = qt.QLabel("Range: -SD (3.05 mm) ← Mean (3.97 mm) → +SD (4.89 mm) [Adjustable beyond limits]")
            self.nFemaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
            self.nFemaleRangeLabel.setVisible(False)
            nLayout.addWidget(self.nFemaleRangeLabel)

            self.nNonSexSlider = qt.QSlider(qt.Qt.Horizontal)
            self.nNonSexSlider.setRange(0, 100)
            self.nNonSexSlider.setValue(50)
            self.nNonSexSlider.valueChanged.connect(self.onNNonSexSliderChanged)
            self.nNonSexSlider.setVisible(False)
            self.nNonSexLabel = qt.QLabel("FSTT n' (Non-sex-specific): 6.0 mm")
            self.nNonSexLabel.setStyleSheet("font-weight: bold;")
            self.nNonSexLabel.setVisible(False)
            nLayout.addWidget(self.nNonSexLabel)
            nLayout.addWidget(self.nNonSexSlider)

            self.nNonSexRangeLabel = qt.QLabel("Range: -SD (4.5 mm) ← Mean (6.0 mm) → +SD (7.5 mm) [Adjustable beyond limits]")
            self.nNonSexRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
            self.nNonSexRangeLabel.setVisible(False)
            nLayout.addWidget(self.nNonSexRangeLabel)

            layout.addWidget(nGroup)

            self.stepStack.addWidget(widget)

    
    def onDownloadHardTissue(self):
        try:
            self.downloadStatusLabel.setText("⏳ Downloading hard tissue landmarks...")
            slicer.app.processEvents()
            
            url = "https://github.com/user-attachments/files/21217369/PS_hard_tissue.mrk. json"
            temp_file = os.path.join(tempfile. gettempdir(), "PS_hard_tissue.mrk.json")
            
            urllib.request.urlretrieve(url, temp_file)
            success = slicer.util.loadMarkups(temp_file)
            
            if success:
                self.hardTissueNode = slicer.util.getNode("PS_hard_tissue")
                self.hardTissueSelector.setCurrentNode(self.hardTissueNode)
                
                self.downloadStatusLabel.setText("✅ Hard tissue landmarks downloaded and loaded successfully!")
                self.step1StatusLabel.setText("Status: ✅ Hard tissue landmarks ready!")
                self.step1StatusLabel.setStyleSheet("color: green; font-weight: bold;")
                slicer.util.showStatusMessage("Hard tissue landmarks loaded!", 3000)
            else:
                raise Exception("Failed to load file")
                
        except Exception as e:
            self.downloadStatusLabel.setText("❌ Error:  {0}".format(str(e)))
            slicer.util.errorDisplay("Failed to download hard tissue landmarks: {0}".format(str(e)))
    
    def onDownloadSoftTissue(self):
        try:
            self.downloadStatusLabel.setText("⏳ Downloading soft tissue landmarks...")
            slicer.app.processEvents()
            
            url = "https://github.com/user-attachments/files/21217705/PS_soft_tissue.mrk.json"
            temp_file = os.path.join(tempfile.gettempdir(), "PS_soft_tissue.mrk.json")
            
            urllib.request.urlretrieve(url, temp_file)
            success = slicer.util.loadMarkups(temp_file)
            
            if success: 
                self.softTissueNode = slicer.util. getNode("PS_soft_tissue")
                if hasattr(self, 'softTissueSelector'):
                    self.softTissueSelector.setCurrentNode(self.softTissueNode)
                
                self.downloadStatusLabel.setText("✅ Soft tissue landmarks downloaded and loaded successfully!")
                slicer.util.showStatusMessage("Soft tissue landmarks loaded!", 3000)
            else:
                raise Exception("Failed to load file")
                
        except Exception as e:
            self.downloadStatusLabel.setText("❌ Error: {0}".format(str(e)))
            slicer.util.errorDisplay("Failed to download soft tissue landmarks: {0}".format(str(e)))
    
    def createStep2_PlaneSetup(self):
        widget = qt. QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 2: Setup Reference Planes")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        mspGroup = qt.QGroupBox("Midsagittal Plane (MSP)")
        mspLayout = qt.QVBoxLayout(mspGroup)
        
        mspDesc = qt.QLabel("Create MSP using best-fit through:  nasion, rhinion, subspinale, and ANS.")
        mspDesc.setWordWrap(True)
        mspLayout.addWidget(mspDesc)
        
        self.createMSPButton = qt.QPushButton("Create MSP from Landmarks")
        self.createMSPButton.clicked.connect(self.onCreateMSP)
        mspLayout.addWidget(self.createMSPButton)
        
        layout. addWidget(mspGroup)
        
        fhpGroup = qt.QGroupBox("Frankfurt Horizontal Plane (FHP)")
        fhpLayout = qt.QVBoxLayout(fhpGroup)
        
        fhpDesc = qt.QLabel("Please ensure you have created your FHP before proceeding.")
        fhpDesc.setWordWrap(True)
        fhpLayout.addWidget(fhpDesc)
        
        self.fhpSelector = slicer.qMRMLNodeComboBox()
        self.fhpSelector.nodeTypes = ["vtkMRMLMarkupsPlaneNode"]
        self.fhpSelector.setMRMLScene(slicer. mrmlScene)
        self.fhpSelector.noneEnabled = True
        self.fhpSelector.selectNodeUponCreation = True
        self.fhpSelector. currentNodeChanged.connect(self.onFHPSelected)
        
        fhpFormLayout = qt.QFormLayout()
        fhpFormLayout. addRow("FHP Plane:", self.fhpSelector)
        fhpLayout.addLayout(fhpFormLayout)
        
        layout. addWidget(fhpGroup)
        
        self.step2StatusLabel = qt.QLabel("Status: Please create MSP and select FHP.")
        self.step2StatusLabel.setWordWrap(True)
        layout.addWidget(self.step2StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep3_Measurements(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 3: Create Hard Tissue Measurements")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "This will create all guide lines and measurements needed for prediction.\n\n"
            "Please set the facial soft tissue thickness (FSTT) values for predictions:"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # ============= FSTT for sn' =============
        snGroup = qt.QGroupBox("FSTT for Subnasale (sn')")
        snLayout = qt.QVBoxLayout(snGroup)

        snExplanation = qt.QLabel(
            "The FSTT at subnasale (sn') is used to predict the soft tissue position from the hard tissue landmark 'subspinale (ss)'.\n"
            "Values: Male = 11.61±1.6mm (Purkait & Singh 2024), Female = 10.27±10.62mm (Purkait & Singh 2024), "
            "Not sex-specific = 13.5±3.5mm (Hona et al. 2024)"
        )
        snExplanation.setWordWrap(True)
        snExplanation.setStyleSheet("font-style: italic; color: #555;")
        snLayout.addWidget(snExplanation)

        # Tickboxes for sn'
        snSexLayout = qt.QHBoxLayout()
        self.snMaleCheckbox = qt.QCheckBox("Male")
        self.snFemaleCheckbox = qt.QCheckBox("Female")
        self.snNonSexCheckbox = qt.QCheckBox("Not sex-specific")
        self.snMaleCheckbox.setChecked(True)
        self.snMaleCheckbox.toggled.connect(self.onSnSexChanged)
        self.snFemaleCheckbox.toggled.connect(self.onSnSexChanged)
        self.snNonSexCheckbox.toggled.connect(self.onSnSexChanged)
        snSexLayout.addWidget(self.snMaleCheckbox)
        snSexLayout.addWidget(self.snFemaleCheckbox)
        snSexLayout.addWidget(self.snNonSexCheckbox)
        snSexLayout.addStretch()
        snLayout.addLayout(snSexLayout)

        # Slider for sn' (Male)
        self.snMaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.snMaleSlider.setRange(0, 100)
        self.snMaleSlider.setValue(50)
        self.snMaleSlider.valueChanged.connect(self.onSnMaleSliderChanged)

        self.snMaleLabel = qt.QLabel("FSTT sn' (Male): 11.61 mm")
        self.snMaleLabel.setStyleSheet("font-weight: bold;")
        snLayout.addWidget(self.snMaleLabel)
        snLayout.addWidget(self.snMaleSlider)

        self.snMaleRangeLabel = qt.QLabel("Range: -SD (10.01 mm) ← Mean (11.61 mm) → +SD (13.21 mm) [Adjustable beyond limits]")
        self.snMaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        snLayout.addWidget(self.snMaleRangeLabel)

        # Slider for sn' (Female)
        self.snFemaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.snFemaleSlider.setRange(0, 100)
        self.snFemaleSlider.setValue(50)
        self.snFemaleSlider.valueChanged.connect(self.onSnFemaleSliderChanged)
        self.snFemaleSlider.setVisible(False)

        self.snFemaleLabel = qt.QLabel("FSTT sn' (Female): 10.27 mm")
        self.snFemaleLabel.setStyleSheet("font-weight: bold;")
        self.snFemaleLabel.setVisible(False)
        snLayout.addWidget(self.snFemaleLabel)
        snLayout.addWidget(self.snFemaleSlider)

        self.snFemaleRangeLabel = qt.QLabel("Range: -SD (-0.35 mm) ← Mean (10.27 mm) → +SD (20.89 mm) [Adjustable beyond limits]")
        self.snFemaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.snFemaleRangeLabel.setVisible(False)
        snLayout.addWidget(self.snFemaleRangeLabel)

        # Slider for sn' (Non-sex-specific)
        self.snNonSexSlider = qt.QSlider(qt.Qt.Horizontal)
        self.snNonSexSlider.setRange(0, 100)
        self.snNonSexSlider.setValue(50)
        self.snNonSexSlider.valueChanged.connect(self.onSnNonSexSliderChanged)
        self.snNonSexSlider.setVisible(False)

        self.snNonSexLabel = qt.QLabel("FSTT sn' (Non-sex-specific): 13.50 mm")
        self.snNonSexLabel.setStyleSheet("font-weight: bold;")
        self.snNonSexLabel.setVisible(False)
        snLayout.addWidget(self.snNonSexLabel)
        snLayout.addWidget(self.snNonSexSlider)

        self.snNonSexRangeLabel = qt.QLabel("Range: -SD (10.0 mm) ← Mean (13.5 mm) → +SD (17.0 mm) [Adjustable beyond limits]")
        self.snNonSexRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.snNonSexRangeLabel.setVisible(False)
        snLayout.addWidget(self.snNonSexRangeLabel)

        layout.addWidget(snGroup)

        # ============= FSTT for n' =============
        nGroup = qt.QGroupBox("FSTT for Nasion (n')")
        nLayout = qt.QVBoxLayout(nGroup)

        nExplanation = qt.QLabel(
            "The FSTT at nasion (n') is used to predict the soft tissue position from the hard tissue landmark 'nasion (n)'.\n"
            "Values: Male = 5.02±0.99mm (Purkait & Singh 2024), Female = 3.97±0.92mm (Purkait & Singh 2024), "
            "Not sex-specific = 6.0±1.5mm (Hona et al. 2024)"
        )
        nExplanation.setWordWrap(True)
        nExplanation.setStyleSheet("font-style: italic; color: #555;")
        nLayout.addWidget(nExplanation)

        # Tickboxes for n'
        nSexLayout = qt.QHBoxLayout()
        self.nMaleCheckbox = qt.QCheckBox("Male")
        self.nFemaleCheckbox = qt.QCheckBox("Female")
        self.nNonSexCheckbox = qt.QCheckBox("Not sex-specific")
        self.nMaleCheckbox.setChecked(True)
        self.nMaleCheckbox.toggled.connect(self.onNSexChanged)
        self.nFemaleCheckbox.toggled.connect(self.onNSexChanged)
        self.nNonSexCheckbox.toggled.connect(self.onNSexChanged)
        nSexLayout.addWidget(self.nMaleCheckbox)
        nSexLayout.addWidget(self.nFemaleCheckbox)
        nSexLayout.addWidget(self.nNonSexCheckbox)
        nSexLayout.addStretch()
        nLayout.addLayout(nSexLayout)

        # Slider for n' (Male)
        self.nMaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.nMaleSlider.setRange(0, 100)
        self.nMaleSlider.setValue(50)
        self.nMaleSlider.valueChanged.connect(self.onNMaleSliderChanged)

        self.nMaleLabel = qt.QLabel("FSTT n' (Male): 5.02 mm")
        self.nMaleLabel.setStyleSheet("font-weight: bold;")
        nLayout.addWidget(self.nMaleLabel)
        nLayout.addWidget(self.nMaleSlider)

        self.nMaleRangeLabel = qt.QLabel("Range: -SD (4.03 mm) ← Mean (5.02 mm) → +SD (6.01 mm) [Adjustable beyond limits]")
        self.nMaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        nLayout.addWidget(self.nMaleRangeLabel)

        # Slider for n' (Female)
        self.nFemaleSlider = qt.QSlider(qt.Qt.Horizontal)
        self.nFemaleSlider.setRange(0, 100)
        self.nFemaleSlider.setValue(50)
        self.nFemaleSlider.valueChanged.connect(self.onNFemaleSliderChanged)
        self.nFemaleSlider.setVisible(False)

        self.nFemaleLabel = qt.QLabel("FSTT n' (Female): 3.97 mm")
        self.nFemaleLabel.setStyleSheet("font-weight: bold;")
        self.nFemaleLabel.setVisible(False)
        nLayout.addWidget(self.nFemaleLabel)
        nLayout.addWidget(self.nFemaleSlider)

        self.nFemaleRangeLabel = qt.QLabel("Range: -SD (3.05 mm) ← Mean (3.97 mm) → +SD (4.89 mm) [Adjustable beyond limits]")
        self.nFemaleRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.nFemaleRangeLabel.setVisible(False)
        nLayout.addWidget(self.nFemaleRangeLabel)

        # Slider for n' (Non-sex-specific)
        self.nNonSexSlider = qt.QSlider(qt.Qt.Horizontal)
        self.nNonSexSlider.setRange(0, 100)
        self.nNonSexSlider.setValue(50)
        self.nNonSexSlider.valueChanged.connect(self.onNNonSexSliderChanged)
        self.nNonSexSlider.setVisible(False)

        self.nNonSexLabel = qt.QLabel("FSTT n' (Non-sex-specific): 6.00 mm")
        self.nNonSexLabel.setStyleSheet("font-weight: bold;")
        self.nNonSexLabel.setVisible(False)
        nLayout.addWidget(self.nNonSexLabel)
        nLayout.addWidget(self.nNonSexSlider)

        self.nNonSexRangeLabel = qt.QLabel("Range: -SD (4.5 mm) ← Mean (6.0 mm) → +SD (7.5 mm) [Adjustable beyond limits]")
        self.nNonSexRangeLabel.setStyleSheet("font-size: 9pt; color: #666;")
        self.nNonSexRangeLabel.setVisible(False)
        nLayout.addWidget(self.nNonSexRangeLabel)

        layout.addWidget(nGroup)

        # ============= CREATE BUTTON =============
        self.createMeasurementsButton = qt.QPushButton("Create All Measurements")
        self.createMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px; font-weight: bold;"
        )
        self.createMeasurementsButton.clicked.connect(self.onCreateMeasurements)
        layout.addWidget(self.createMeasurementsButton)
        
        self.step3StatusLabel = qt.QLabel("Status: Ready to create measurements.")
        self.step3StatusLabel.setWordWrap(True)
        layout.addWidget(self.step3StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

    def createStep4_Prediction(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 4: Predict Pronasale and Nasion Tip")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "Select the biological sex and visualization options, then run the prediction.\n\n"
            "Note: If you used 'Not sex-specific' FSTT values in Step 3, you must choose which "
            "prediction equation (Male or Female) to use below, as there are no sex-neutral equations available."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        sexGroup = qt.QGroupBox("Prediction Equations to Use")
        sexLayout = qt.QVBoxLayout(sexGroup)
        
        sexButtonLayout = qt.QHBoxLayout()
        self.maleRadio = qt.QRadioButton("Male")
        self.femaleRadio = qt.QRadioButton("Female")
        self.bothRadio = qt.QRadioButton("Both (for comparison)")
        self.maleRadio.setChecked(True)
        
        sexButtonLayout.addWidget(self.maleRadio)
        sexButtonLayout.addWidget(self.femaleRadio)
        sexButtonLayout.addWidget(self.bothRadio)
        sexButtonLayout.addStretch()
        sexLayout.addLayout(sexButtonLayout)
        
        noteLabel = qt.QLabel(
            "<i>These equations are used to predict pronasale (prn) and nasion tip (nt) positions. "
            "They are independent of the FSTT values chosen in Step 3.</i>"
        )
        noteLabel.setWordWrap(True)
        noteLabel.setStyleSheet("color: #666; font-size: 10pt;")
        sexLayout.addWidget(noteLabel)
        
        layout.addWidget(sexGroup)
        
        self.showLinesCheckbox = qt.QCheckBox("Show visualization lines")
        self.showLinesCheckbox.setChecked(True)
        layout.addWidget(self.showLinesCheckbox)
        
        self.predictButton = qt.QPushButton("Run Predictions (Pronasale & Nasion Tip)")
        self.predictButton.setStyleSheet(
            "background-color: #e74c3c; color: white; padding: 10px; font-weight: bold;"
        )
        self.predictButton.clicked.connect(self.onRunPrediction)
        layout.addWidget(self.predictButton)
        
        self.step4StatusLabel = qt.QLabel("Status: Ready to predict.")
        self.step4StatusLabel.setWordWrap(True)
        layout.addWidget(self.step4StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)

        
    def createStep5_Validation(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 5: Validation & Additional Measurements (Optional)")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        desc = qt.QLabel(
            "If you have ground truth soft tissue landmarks, you can calculate prediction errors "
            "and create additional measurements from the paper."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        self.softTissueSelector = slicer.qMRMLNodeComboBox()
        self.softTissueSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.softTissueSelector.setMRMLScene(slicer.mrmlScene)
        self.softTissueSelector.noneEnabled = True
        self.softTissueSelector.selectNodeUponCreation = True
        self.softTissueSelector.currentNodeChanged.connect(self.onSoftTissueSelected)
        
        formLayout = qt.QFormLayout()
        formLayout.addRow("Soft Tissue Landmarks:", self.softTissueSelector)
        layout.addLayout(formLayout)
        
        self.additionalMeasurementsButton = qt.QPushButton("📏 Create All Additional Measurements")
        self.additionalMeasurementsButton.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px; font-weight: bold;"
        )
        self.additionalMeasurementsButton. clicked.connect(self.onCreateAdditionalMeasurements)
        layout.addWidget(self.additionalMeasurementsButton)
        
        self.calculateErrorButton = qt.QPushButton("📊 Calculate Prediction Errors")
        self.calculateErrorButton.setStyleSheet(
            "background-color: #9b59b6; color: white; padding: 8px; font-weight: bold;"
        )
        self.calculateErrorButton. clicked.connect(self.onCalculateErrors)
        layout.addWidget(self.calculateErrorButton)
        
        self.step5StatusLabel = qt.QLabel("Status: Optional step.")
        self.step5StatusLabel.setWordWrap(True)
        layout.addWidget(self.step5StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    
    def createStep6_Results(self):
        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = qt.QLabel("Step 6: Results & Export")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        measurementsLabel = qt.QLabel("<b>📏 Measurements (Distances & Angles)</b>")
        measurementsLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(measurementsLabel)
        
        instructionsLabel = qt.QLabel(
            "Prediction errors are <span style='background-color: #ffffcc;'>highlighted in yellow</span>."
        )
        instructionsLabel.setWordWrap(True)
        layout.addWidget(instructionsLabel)
        
        self.measurementsTable = qt.QTableWidget()
        self.measurementsTable. setColumnCount(3)
        self.measurementsTable.setHorizontalHeaderLabels(["Measurement", "Value", "Unit"])
        self.measurementsTable.horizontalHeader().setStretchLastSection(False)
        self.measurementsTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView. Stretch)
        self.measurementsTable.setMinimumHeight(250)
        self.measurementsTable.setAlternatingRowColors(True)
        layout.addWidget(self.measurementsTable)
        
        coordinatesLabel = qt.QLabel("<b>📍 Coordinates Comparison (Predicted vs True)</b>")
        coordinatesLabel.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(coordinatesLabel)
        
        coordDesc = qt.QLabel("3D positions in space (RAS coordinate system:  Right, Anterior, Superior)")
        coordDesc.setWordWrap(True)
        layout.addWidget(coordDesc)
        
        self.coordinatesTable = qt.QTableWidget()
        self.coordinatesTable.setColumnCount(8)
        self.coordinatesTable.setHorizontalHeaderLabels([
            "Landmark", 
            "Predicted X", "Predicted Y", "Predicted Z",
            "True X", "True Y", "True Z",
            "3D Error (mm)"
        ])
        self.coordinatesTable.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self.coordinatesTable. setMinimumHeight(150)
        self.coordinatesTable.setAlternatingRowColors(True)
        layout.addWidget(self.coordinatesTable)
        
        buttonLayout = qt.QHBoxLayout()
        
        self.copyMeasurementsButton = qt. QPushButton("📋 Copy Measurements")
        self.copyMeasurementsButton.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px; font-weight: bold;"
        )
        self.copyMeasurementsButton.setToolTip("Copy measurements table to clipboard")
        self.copyMeasurementsButton.clicked.connect(self.onCopyMeasurements)
        buttonLayout.addWidget(self.copyMeasurementsButton)
        
        self.copyCoordinatesButton = qt.QPushButton("📋 Copy Coordinates")
        self.copyCoordinatesButton.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px; font-weight: bold;"
        )
        self.copyCoordinatesButton. setToolTip("Copy coordinates table to clipboard")
        self.copyCoordinatesButton.clicked.connect(self.onCopyCoordinates)
        buttonLayout.addWidget(self.copyCoordinatesButton)
        
        self.finishButton = qt.QPushButton("Finish")
        self.finishButton.clicked.connect(lambda: self.close())
        buttonLayout.addWidget(self.finishButton)
        
        layout.addLayout(buttonLayout)
        
        self.step6StatusLabel = qt.QLabel("Status: Review results above.")
        self.step6StatusLabel.setWordWrap(True)
        layout.addWidget(self.step6StatusLabel)
        
        layout.addStretch(1)
        self.stepStack.addWidget(widget)
    


    # ==================== SLIDER HELPER METHODS ====================

    def onSnSexChanged(self):
        """Handle sn' sex checkbox changes"""
        maleChecked = self.snMaleCheckbox.isChecked()
        femaleChecked = self.snFemaleCheckbox.isChecked()
        nonSexChecked = self.snNonSexCheckbox.isChecked()
        
        # Show/hide male slider
        self.snMaleSlider.setVisible(maleChecked)
        self.snMaleLabel.setVisible(maleChecked)
        self.snMaleRangeLabel.setVisible(maleChecked)
        
        # Show/hide female slider
        self.snFemaleSlider.setVisible(femaleChecked)
        self.snFemaleLabel.setVisible(femaleChecked)
        self.snFemaleRangeLabel.setVisible(femaleChecked)
        
        # Show/hide non-sex-specific slider
        self.snNonSexSlider.setVisible(nonSexChecked)
        self.snNonSexLabel.setVisible(nonSexChecked)
        self.snNonSexRangeLabel.setVisible(nonSexChecked)

    def onNSexChanged(self):
        """Handle n' sex checkbox changes"""
        maleChecked = self.nMaleCheckbox.isChecked()
        femaleChecked = self.nFemaleCheckbox.isChecked()
        nonSexChecked = self.nNonSexCheckbox.isChecked()
        
        # Show/hide male slider
        self.nMaleSlider.setVisible(maleChecked)
        self.nMaleLabel.setVisible(maleChecked)
        self.nMaleRangeLabel.setVisible(maleChecked)
        
        # Show/hide female slider
        self.nFemaleSlider.setVisible(femaleChecked)
        self.nFemaleLabel.setVisible(femaleChecked)
        self.nFemaleRangeLabel.setVisible(femaleChecked)
        
        # Show/hide non-sex-specific slider
        self.nNonSexSlider.setVisible(nonSexChecked)
        self.nNonSexLabel.setVisible(nonSexChecked)
        self.nNonSexRangeLabel.setVisible(nonSexChecked)

    def onSnMaleSliderChanged(self, value):
        """Update sn' male FSTT value based on slider"""
        mean = 11.61
        sd = 1.6
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.snMaleLabel.setText("FSTT sn' (Male): {:.2f} mm".format(fstt_value))

    def onSnFemaleSliderChanged(self, value):
        """Update sn' female FSTT value based on slider"""
        mean = 10.27
        sd = 10.62
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.snFemaleLabel.setText("FSTT sn' (Female): {:.2f} mm".format(fstt_value))

    def onSnNonSexSliderChanged(self, value):
        """Update sn' non-sex-specific FSTT value based on slider"""
        mean = 13.5
        sd = 3.5
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.snNonSexLabel.setText("FSTT sn' (Non-sex-specific): {:.2f} mm".format(fstt_value))

    def onNMaleSliderChanged(self, value):
        """Update n' male FSTT value based on slider"""
        mean = 5.02
        sd = 0.99
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.nMaleLabel.setText("FSTT n' (Male): {:.2f} mm".format(fstt_value))

    def onNFemaleSliderChanged(self, value):
        """Update n' female FSTT value based on slider"""
        mean = 3.97
        sd = 0.92
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.nFemaleLabel.setText("FSTT n' (Female): {:.2f} mm".format(fstt_value))

    def onNNonSexSliderChanged(self, value):
        """Update n' non-sex-specific FSTT value based on slider"""
        mean = 6.0
        sd = 1.5
        fstt_value = mean + ((value - 50) / 25.0) * sd
        self.nNonSexLabel.setText("FSTT n' (Non-sex-specific): {:.2f} mm".format(fstt_value))

    def getSnFSTT(self):
        """Get the current sn' FSTT value(s) based on checkboxes"""
        values = {}
        
        if self.snMaleCheckbox.isChecked():
            mean = 11.61
            sd = 1.6
            slider_value = self.snMaleSlider.value
            values['male'] = mean + ((slider_value - 50) / 25.0) * sd
        
        if self.snFemaleCheckbox.isChecked():
            mean = 10.27
            sd = 10.62
            slider_value = self.snFemaleSlider.value
            values['female'] = mean + ((slider_value - 50) / 25.0) * sd
        
        if self.snNonSexCheckbox.isChecked():
            mean = 13.5
            sd = 3.5
            slider_value = self.snNonSexSlider.value
            values['nonsex'] = mean + ((slider_value - 50) / 25.0) * sd
        
        return values

    def getNFSTT(self):
        """Get the current n' FSTT value(s) based on checkboxes"""
        values = {}
        
        if self.nMaleCheckbox.isChecked():
            mean = 5.02
            sd = 0.99
            slider_value = self.nMaleSlider.value
            values['male'] = mean + ((slider_value - 50) / 25.0) * sd
        
        if self.nFemaleCheckbox.isChecked():
            mean = 3.97
            sd = 0.92
            slider_value = self.nFemaleSlider.value
            values['female'] = mean + ((slider_value - 50) / 25.0) * sd
        
        if self.nNonSexCheckbox.isChecked():
            mean = 6.0
            sd = 1.5
            slider_value = self.nNonSexSlider.value
            values['nonsex'] = mean + ((slider_value - 50) / 25.0) * sd
        
        return values
    
    def findCircleIntersections(self, center1, radius1, center2, radius2):
        """
        Find intersection points of two circles in 3D space.
        For 3D, we need to constrain to the plane containing both centers and perpendicular to MSP.
        Returns the two intersection points (or one if circles are tangent, or None if no intersection)
        """
        d = np.linalg.norm(center2 - center1)
        
        # Check if circles intersect
        if d > radius1 + radius2:  # Circles too far apart
            print("Warning: Circles don't intersect (too far). Distance: {:.2f}, Sum of radii: {:.2f}".format(d, radius1 + radius2))
            return None
        if d < abs(radius1 - radius2):  # One circle inside the other
            print("Warning: One circle is inside the other")
            return None
        if d == 0 and radius1 == radius2:  # Same circle
            print("Warning: Circles are identical")
            return None
        
        # Calculate the intersection points
        # Point P on the line between centers
        a = (radius1**2 - radius2**2 + d**2) / (2 * d)
        h = np.sqrt(radius1**2 - a**2)
        
        # Direction from center1 to center2
        direction = (center2 - center1) / d
        
        # Point P (on line between centers)
        P = center1 + a * direction
        
        # We need a perpendicular direction to find the two intersection points
        # Get MSP normal to constrain the solution
        if self.mspNode:
            msp_origin, msp_normal = self.getPlaneData(self.mspNode)
            # Perpendicular direction in the plane perpendicular to line center1-center2
            # and considering MSP orientation
            perp = np.cross(direction, msp_normal)
            perp = perp / np.linalg.norm(perp)
        else:
            # Fallback: use arbitrary perpendicular
            if abs(direction[2]) < 0.9:
                perp = np.array([0, 0, 1])
            else:
                perp = np.array([1, 0, 0])
            perp = np.cross(direction, perp)
            perp = perp / np.linalg.norm(perp)
        
        # Two intersection points
        intersection1 = P + h * perp
        intersection2 = P - h * perp
        
        return intersection1, intersection2

    def selectBestNtIntersection(self, intersection1, intersection2, n_soft):
        """
        Select the best nt intersection point.
        Choose the one that is more INFERIOR (lower Z value in RAS) and more ANTERIOR (higher Y)
        The nasion tip should be below the nasion, not above it.
        """
        if intersection1 is None:
            return None
        
        if intersection2 is None:
            return intersection1
        
        # In RAS coordinates:
        # - Anterior is positive Y (we want this)
        # - Superior is positive Z (we want NEGATIVE/lower for inferior)
        
        # Primary criterion: Choose the more inferior point (lower Z = downward)
        # Secondary criterion: If similar Z, choose more anterior (higher Y)
        
        z_diff = abs(intersection1[2] - intersection2[2])
        
        if z_diff > 1.0:  # Significant Z difference (> 1mm)
            # Choose the LOWER point (more inferior/downward)
            if intersection1[2] < intersection2[2]:
                print("Selected intersection 1 (more inferior): Z={0:.2f}".format(intersection1[2]))
                return intersection1
            else:
                print("Selected intersection 2 (more inferior): Z={0:.2f}".format(intersection2[2]))
                return intersection2
        else:
            # Z values are similar, use anterior position as tiebreaker
            if intersection1[1] > intersection2[1]:  # Y coordinate (anterior)
                print("Selected intersection 1 (more anterior): Y={0:.2f}, Z={1:.2f}".format(intersection1[1], intersection1[2]))
                return intersection1
            else:
                print("Selected intersection 2 (more anterior): Y={0:.2f}, Z={1:.2f}".format(intersection2[1], intersection2[2]))
                return intersection2

    def syncWithScene(self):
        """ENHANCED: Smart auto-detection with multiple name variations"""
        # Hard tissue detection
        possible_hard_names = ["PS_hard_tissue", "hard_tissue", "Hard_tissue", "hard", "Hard Tissue", "HardTissue"]
        for name in possible_hard_names: 
            node = slicer.util.getFirstNodeByName(name)
            if node:
                self.hardTissueNode = node
                self.hardTissueSelector.setCurrentNode(node)
                print("✅ Auto-detected hard tissue:  '{0}'".format(name))
                break
        
        # MSP detection
        possible_msp_names = ["MSP", "msp", "Midsagittal", "midsagittal", "Mid-Sagittal", "mid-sagittal"]
        for name in possible_msp_names: 
            node = slicer. util.getFirstNodeByName(name)
            if node: 
                self.mspNode = node
                print("✅ Auto-detected MSP: '{0}'".format(name))
                break
        
        # FHP detection - ENHANCED with more variations
        possible_fhp_names = ["FHP", "fhp", "Frankfurt", "frankfurt", "Frankfort", "frankfort", "FH", "fh", "Frankfurt Horizontal", "frankfurt horizontal"]
        for name in possible_fhp_names:
            node = slicer.util.getFirstNodeByName(name)
            if node: 
                self.fhpNode = node
                self.fhpSelector.setCurrentNode(node)
                print("✅ Auto-detected FHP: '{0}'".format(name))
                break
        
        # Soft tissue detection
        possible_soft_names = ["PS_soft_tissue", "soft_tissue", "Soft_tissue", "soft", "Soft Tissue", "SoftTissue"]
        for name in possible_soft_names: 
            node = slicer.util.getFirstNodeByName(name)
            if node:
                self.softTissueNode = node
                if hasattr(self, 'softTissueSelector'):
                    self.softTissueSelector. setCurrentNode(node)
                print("✅ Auto-detected soft tissue: '{0}'".format(name))
                break
    
    def showDetectionSummary(self):
        """Show a summary of what was auto-detected"""
        detected = []
        
        if self.hardTissueNode:
            detected.append("✅ Hard tissue landmarks")
        if self.mspNode:
            detected.append("✅ MSP plane")
        if self.fhpNode:
            detected.append("✅ FHP plane")
        if self.softTissueNode:
            detected.append("✅ Soft tissue landmarks")
        
        if detected: 
            summary = "Auto-detected nodes:\n" + "\n".join(detected)
            print("\n" + "="*50)
            print(summary)
            print("="*50 + "\n")
            slicer.util.showStatusMessage("Auto-detection complete! Check Python console for details.", 3000)
            
            # Update status labels
            if self.hardTissueNode:
                self.step1StatusLabel.setText("Status: ✅ Hard tissue detected!")
                self.step1StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            if self.currentStep == 1:
                self.updateStep2Status()
        else:
            print("No existing nodes detected.  Please load or create landmarks.")
    
    # ==================== HELPER METHODS ====================
    
    def getPoint(self, node, index):
        point = [0, 0, 0]
        node.GetNthControlPointPosition(index, point)
        return np.array(point)
    
    def getPointByLabel(self, node, label):
        for i in range(node.GetNumberOfControlPoints()):
            if node. GetNthControlPointLabel(i) == label:
                return self.getPoint(node, i)
        raise ValueError("Point '{0}' not found". format(label))
    
    def getPlaneData(self, planeNode):
        if 'Plane' in planeNode.GetClassName():
            origin = [0, 0, 0]
            normal = [0, 0, 0]
            planeNode.GetOrigin(origin)
            planeNode.GetNormal(normal)
            return np.array(origin), np.array(normal)
        else:
            raise ValueError("Node is not a plane")
    
    def createLine(self, p1, p2, name, color=[1.0, 1.0, 1.0], selected_color=[1.0, 0.5, 0.0], thickness=0.25):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        lineNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsLineNode', name)
        lineNode.AddControlPoint(p1.tolist())
        lineNode.AddControlPoint(p2.tolist())
        
        displayNode = lineNode.GetDisplayNode()
        if displayNode:
            displayNode. SetColor(*color)
            displayNode.SetSelectedColor(*selected_color)
            displayNode.SetLineThickness(thickness)
            displayNode.SetGlyphScale(1.8)
        
        return lineNode
    
    def getLineLength(self, lineNode):
        start = [0, 0, 0]
        end = [0, 0, 0]
        lineNode.GetNthControlPointPosition(0, start)
        lineNode.GetNthControlPointPosition(1, end)
        return np.linalg.norm(np.array(end) - np.array(start))
    
    def storeMeasurement(self, name, value, unit="mm", is_summary=False):
        self.all_measurements[name] = {
            "value": value,
            "unit": unit,
            "is_summary": is_summary
        }
    
    def storeCoordinate(self, landmark_name, predicted_coords, true_coords=None):
        self.all_coordinates[landmark_name] = {
            "predicted":  predicted_coords,
            "true": true_coords
        }
    
    def onHardTissueSelected(self, node):
        if node: 
            self.hardTissueNode = node
            self.step1StatusLabel.setText("Status: ✅ Selected '{0}'. ".format(node.GetName()))
            self.step1StatusLabel.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.hardTissueNode = None
            self.step1StatusLabel.setText("Status: Download landmarks or select 'PS_hard_tissue' node.")
            self.step1StatusLabel.setStyleSheet("")
    
    def onFHPSelected(self, node):
        """ENHANCED: Smart FHP selection with status updates"""
        if node: 
            self.fhpNode = node
            print("✅ FHP selected: '{0}'".format(node.GetName()))
            self.updateStep2Status()
            
            # Check if both planes are ready
            if self.mspNode: 
                slicer.util.showStatusMessage("✅ Both planes ready!  You can proceed to Step 3.", 3000)
        else:
            self.fhpNode = None
            self.updateStep2Status()
    
    def onSoftTissueSelected(self, node):
        if node:
            self.softTissueNode = node
            self.step5StatusLabel.setText("Status: ✅ Selected '{0}'.". format(node.GetName()))
            self.step5StatusLabel. setStyleSheet("color: green; font-weight: bold;")
        else:
            self.softTissueNode = None
            self.step5StatusLabel.setText("Status: Optional step.")
            self.step5StatusLabel.setStyleSheet("")
    
    def updateStep2Status(self):
        """ENHANCED: Color-coded status messages"""
        if self.mspNode and self.fhpNode:
            self.step2StatusLabel.setText("Status: ✅ MSP and FHP ready!  Click 'Next' to continue.")
            self.step2StatusLabel.setStyleSheet("color: green; font-weight: bold;")
        elif self.mspNode:
            self.step2StatusLabel.setText("Status: MSP created.  ⚠️ Please select FHP plane.")
            self.step2StatusLabel.setStyleSheet("color: orange; font-weight: bold;")
        elif self.fhpNode:
            self.step2StatusLabel.setText("Status: FHP selected. ⚠️ Please create MSP.")
            self.step2StatusLabel.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.step2StatusLabel.setText("Status: ❌ Please create MSP and select FHP.")
            self.step2StatusLabel.setStyleSheet("color: red; font-weight:  bold;")
    
    def onCreateMSP(self):
        try:
            if not self.hardTissueNode:
                raise ValueError("Please select hard tissue landmarks first.")
            
            self.step2StatusLabel.setText("Status: Creating MSP...")
            self.step2StatusLabel.setStyleSheet("color: blue;")
            slicer.app.processEvents()
            
            points = []
            for i in range(4):
                points.append(self.getPoint(self.hardTissueNode, i))
            points = np.array(points)
            
            centroid = np.mean(points, axis=0)
            pts_centered = points - centroid
            U, S, Vt = np.linalg.svd(pts_centered)
            normal = Vt[2, :]
            
            existing = slicer.util.getFirstNodeByName('MSP')
            if existing: 
                slicer.mrmlScene.RemoveNode(existing)
            
            self.mspNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsPlaneNode', 'MSP')
            self.mspNode.SetOriginWorld(centroid)
            self.mspNode. SetNormalWorld(normal)
            
            self.updateStep2Status()
            slicer.util.showStatusMessage("✅ MSP created successfully!", 3000)
            print("✅ MSP created from landmarks")
            
        except Exception as e:
            self.step2StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step2StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create MSP:  {0}".format(str(e)))
    
    def onCreateMeasurements(self):
        try:
            if not all([self.hardTissueNode, self.mspNode, self.fhpNode]):
                raise ValueError("Please complete previous steps first.")
            
            self.step3StatusLabel.setText("Status: Creating measurements...")
            slicer.app.processEvents()
            
            msp_origin, msp_normal = self.getPlaneData(self.mspNode)
            fhp_origin, fhp_normal = self.getPlaneData(self.fhpNode)
            
            line_direction = np.cross(msp_normal, fhp_normal)
            line_direction = line_direction / np.linalg. norm(line_direction)
            
            length = 70.0
            half_vec = 0.5 * length * line_direction
            fhp_start = msp_origin - half_vec
            fhp_end = msp_origin + half_vec
            
            self.createLine(fhp_start, fhp_end, 'FHP guide', [1.0, 1.0, 1.0], [1.0, 0.0, 0.0])
            
            guide_names = ['st n guide', 'st rhi guide', 'st sn guide']
            guide_colors = {
                'st n guide': ([1.0, 1.0, 1.0], [0.0, 1.0, 0.0]),
                'st rhi guide':  ([1.0, 1.0, 1.0], [0.0, 0.0, 1.0]),
                'st sn guide': ([1.0, 1.0, 1.0], [1.0, 1.0, 0.0])
            }
            
            for i, name in enumerate(guide_names):
                landmark_pos = self.getPoint(self.hardTissueNode, i)
                start = landmark_pos - half_vec
                end = landmark_pos + half_vec
                self.createLine(start, end, name, *guide_colors[name])
            
            pred_FSTT_sn = slicer.util.getFirstNodeByName('pred_FSTT_sn')
            if pred_FSTT_sn:
                slicer.mrmlScene.RemoveNode(pred_FSTT_sn)
            self.pred_FSTT_sn = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', 'pred_FSTT_sn')
            
            # Get sn' FSTT values - use male by default if available
            sn_fstt_values = self.getSnFSTT()
            if 'male' in sn_fstt_values:
                sn_thickness = sn_fstt_values['male']
            elif 'female' in sn_fstt_values:
                sn_thickness = sn_fstt_values['female']
            else:
                sn_thickness = 13.5  # Default fallback
                        
            st_sn_guide = slicer.util.getNode('st sn guide')
            sn_guide_start = self.getPoint(st_sn_guide, 0)
            sn_guide_end = self.getPoint(st_sn_guide, 1)
            
            guide_vec = sn_guide_end - sn_guide_start
            guide_unit_vec = guide_vec / np. linalg.norm(guide_vec)
            guide_unit_vec = -guide_unit_vec
            
            ss_point = self.getPoint(self.hardTissueNode, 2)
            pred_sn_position = ss_point + guide_unit_vec * sn_thickness
            
            self.pred_FSTT_sn.AddControlPoint(pred_sn_position.tolist(), "sn'_FSTT")
            
            displayNode = self.pred_FSTT_sn.GetDisplayNode()
            if displayNode: 
                displayNode.SetColor(0.0, 0.8, 0.0)
                displayNode.SetSelectedColor(1.0, 0.0, 0.0)
                displayNode.SetGlyphScale(1.8)
                displayNode.SetTextScale(3.0)
                displayNode.SetSliceProjection(True)
            
            # ============= NEW: Predict n' (nasion) points =============
            n_fstt_values = self.getNFSTT()

            # Create prediction nodes for each selected sex/type
            for sex_key, n_thickness in n_fstt_values.items():
                # Get the st n guide line
                st_n_guide = slicer.util.getNode('st n guide')
                n_guide_start = self.getPoint(st_n_guide, 0)
                n_guide_end = self.getPoint(st_n_guide, 1)
                
                # Direction along the guide (anterior direction)
                n_guide_vec = n_guide_end - n_guide_start
                n_guide_unit_vec = n_guide_vec / np.linalg.norm(n_guide_vec)
                
                # Get nasion point
                n_point = self.getPoint(self.hardTissueNode, 0)
                
                # Predict n' by moving anteriorly from nasion
                pred_n_position = n_point + n_guide_unit_vec * n_thickness
                
                # Store in appropriate prediction node
                pred_node_name = 'pred_soft_tissue_{0}'.format(sex_key)
                pred_node = slicer.util.getFirstNodeByName(pred_node_name)
                if not pred_node:
                    pred_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', pred_node_name)
                
                # Add n' prediction
                pred_node.AddControlPoint(pred_n_position.tolist(), "n'_FSTT_{0}".format(sex_key))
                
                # Set colors
                displayNode = pred_node.GetDisplayNode()
                if displayNode:
                    if sex_key == "male":
                        displayNode.SetColor(0.0, 0.0, 0.8)
                        displayNode.SetSelectedColor(0.0, 0.0, 1.0)
                    elif sex_key == "female":
                        displayNode.SetColor(0.0, 0.8, 0.0)
                        displayNode.SetSelectedColor(0.0, 1.0, 0.0)
                    else:  # nonsex
                        displayNode.SetColor(0.8, 0.0, 0.8)
                        displayNode.SetSelectedColor(1.0, 0.0, 1.0)
                    
                    displayNode.SetGlyphScale(1.8)
                    displayNode.SetTextScale(3.0)
                    displayNode.SetSliceProjection(True)
                
                # Store measurement
                self.storeMeasurement("Predicted n' FSTT ({0})".format(sex_key), n_thickness, "mm")
                self.storeCoordinate("n' ({0})".format(sex_key), pred_n_position)

            n_point = self.getPoint(self.hardTissueNode, 0)
            self.createLine(n_point, pred_sn_position, 'n to sn FSTT', [1.0, 1.0, 1.0], [0.5, 0.5, 0.0])

            n_to_sn_dist = np.linalg.norm(pred_sn_position - n_point)
            self.storeMeasurement("n to sn FSTT", n_to_sn_dist)
            
            n_point = self.getPoint(self.hardTissueNode, 0)
            self.createLine(n_point, pred_sn_position, 'n to sn FSTT', [1.0, 1.0, 1.0], [0.5, 0.5, 0.0])
            
            n_to_sn_dist = np.linalg.norm(pred_sn_position - n_point)
            self.storeMeasurement("n to sn FSTT", n_to_sn_dist)
            
            ab_start = self.getPoint(self.hardTissueNode, 4)
            ab_end = self.getPoint(self.hardTissueNode, 5)
            ab_line = self.createLine(ab_start, ab_end, 'AB', [1.0, 1.0, 1.0], [1.0, 0.0, 1.0])
            self.storeMeasurement("AB", self.getLineLength(ab_line))
            
            cd_start = self.getPoint(self.hardTissueNode, 6)
            cd_end = self.getPoint(self.hardTissueNode, 7)
            cd_line = self.createLine(cd_start, cd_end, 'CD', [1.0, 1.0, 1.0], [0.0, 1.0, 1.0])
            self.storeMeasurement("CD", self.getLineLength(cd_line))
            
            baseline_start = self.getPoint(self.hardTissueNode, 0)
            baseline_end = self.getPoint(self.hardTissueNode, 3)
            baseline_line = self.createLine(baseline_start, baseline_end, 'baseline', [1.0, 1.0, 1.0], [1.0, 0.5, 0.0])
            self.storeMeasurement("baseline", self.getLineLength(baseline_line))
            
            n_to_rhi_start = self.getPoint(self.hardTissueNode, 0)
            n_to_rhi_end = self.getPoint(self.hardTissueNode, 1)
            n_to_rhi_line = self.createLine(n_to_rhi_start, n_to_rhi_end, 'n to rhi', [1.0, 1.0, 1.0], [0.5, 0.0, 0.5])
            self.storeMeasurement("n to rhi", self.getLineLength(n_to_rhi_line))
            
            rhi_point = self.getPoint(self.hardTissueNode, 1)
            baseline_vec = baseline_end - baseline_start
            line_unit_vec = baseline_vec / np.linalg.norm(baseline_vec)
            
            v = rhi_point - baseline_start
            proj_length = np.dot(v, line_unit_vec)
            closest_point = baseline_start + proj_length * line_unit_vec
            
            rhi_to_baseline_line = self.createLine(rhi_point, closest_point, 'rhi to baseline', [1.0, 1.0, 1.0], [0.7, 0.3, 0.3])
            self.storeMeasurement("rhi to baseline", self.getLineLength(rhi_to_baseline_line))
            
            self.step3StatusLabel.setText("Status: ✅ All measurements created successfully!")
            self.step3StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            slicer.util.showStatusMessage("Measurements created!", 3000)
            
            self.updateResultsTables()
            
        except Exception as e:
            self.step3StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step3StatusLabel. setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create measurements: {0}".format(str(e)))
    
    def onRunPrediction(self):
        try:
            if self.bothRadio.isChecked():
                self.step4StatusLabel.setText("Status: Running predictions for both sexes...")
                slicer. app.processEvents()
                self.runSinglePrediction("male")
                self.runSinglePrediction("female")
                self.step4StatusLabel.setText("Status: ✅ Predictions completed for both sexes!")
                self.step4StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            elif self.maleRadio.isChecked():
                self.step4StatusLabel.setText("Status: Running male prediction...")
                slicer. app.processEvents()
                self.runSinglePrediction("male")
                self.step4StatusLabel.setText("Status: ✅ Male prediction completed!")
                self.step4StatusLabel. setStyleSheet("color: green; font-weight: bold;")
            else:
                self.step4StatusLabel.setText("Status: Running female prediction...")
                slicer.app.processEvents()
                self.runSinglePrediction("female")
                self.step4StatusLabel.setText("Status: ✅ Female prediction completed!")
                self.step4StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            slicer.util.showStatusMessage("Prediction complete!", 3000)
            self.updateResultsTables()
            
        except Exception as e:
            self.step4StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step4StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer. util.errorDisplay("Failed to predict: {0}".format(str(e)))
    
    def runSinglePrediction(self, sex, sn_fstt, n_fstt, sn_fstt_label, n_fstt_label):
        """
        Run a single prediction for a given sex and FSTT values.
        The FSTT label is used to record which FSTT was used for each prediction.
        Implements geometric and regression logic as in the .md file.
        """
        # 1. Get all required nodes and points
        hardTissueNode = self.hardTissueNode or slicer.util.getNode('PS_hard_tissue')
        mspNode = self.mspNode or slicer.util.getNode('MSP')
        fhpNode = self.fhpNode or slicer.util.getNode('FHP')
        def getpt(label):
            return self.getPointByLabel(hardTissueNode, label)
        n = getpt('n')
        rhi = getpt('rhi')
        ss = getpt('ss')
        ans = getpt('ANS')
        def getLineEnds(name):
            node = slicer.util.getNode(name)
            p1 = [0,0,0]; p2 = [0,0,0]
            node.GetNthControlPointPosition(0, p1)
            node.GetNthControlPointPosition(1, p2)
            return np.array(p1), np.array(p2)
        baseline_start, baseline_end = getLineEnds('baseline')
        n2rhi_start, n2rhi_end = getLineEnds('n to rhi')
        rhi2base_start, rhi2base_end = getLineEnds('rhi to baseline')
        baseline_len = np.linalg.norm(baseline_end - baseline_start)
        n2rhi_len = np.linalg.norm(n2rhi_end - n2rhi_start)
        rhi2base_len = np.linalg.norm(rhi2base_end - rhi2base_start)
        if sex == 'male':
            prn_dist = 19.544 + 0.299 * rhi2base_len
            nt_dist = 31.76 + 1.009 * n2rhi_len
            bony_nss = 4.385 + 0.988 * baseline_len
        else:
            prn_dist = 15.056 + 0.622 * rhi2base_len
            nt_dist = 33.23 + 0.768 * n2rhi_len
            bony_nss = 7.673 + 0.909 * baseline_len
        msp_origin = np.array(mspNode.GetOrigin())
        msp_normal = np.array(mspNode.GetNormal())
        sn_pred = ss + sn_fstt * msp_normal / np.linalg.norm(msp_normal)
        self.storeCoordinate(f"sn'_pred_{sex}_{sn_fstt_label}", sn_pred.tolist(), fstt_label=sn_fstt_label)
        n_pred = n + n_fstt * msp_normal / np.linalg.norm(msp_normal)
        self.storeCoordinate(f"n'_pred_{sex}_{n_fstt_label}", n_pred.tolist(), fstt_label=n_fstt_label)
        prn_pred = baseline_start + prn_dist * msp_normal / np.linalg.norm(msp_normal)
        self.storeCoordinate(f"prn_pred_{sex}_{sn_fstt_label}_{n_fstt_label}", prn_pred.tolist(), fstt_label=f"sn:{sn_fstt_label}, n:{n_fstt_label}")
        def sphere_intersection(c1, r1, c2, r2):
            d = np.linalg.norm(c2 - c1)
            if d > r1 + r2:
                return None, None
            a = (r1**2 - r2**2 + d**2) / (2*d)
            h = np.sqrt(max(0, r1**2 - a**2))
            p2 = c1 + a * (c2 - c1) / d
            if np.allclose(c1, c2):
                return None, None
            v = c2 - c1
            if not np.allclose(v[0], 0):
                perp = np.array([-v[1], v[0], 0])
            else:
                perp = np.array([0, -v[2], v[1]])
            perp = perp / np.linalg.norm(perp)
            i1 = p2 + h * perp
            i2 = p2 - h * perp
            return i1, i2
        nt1, nt2 = sphere_intersection(n, bony_nss, n_pred, nt_dist)
        if nt1 is not None and nt2 is not None:
            nt_pred = nt1 if nt1[1] > nt2[1] else nt2
            self.storeCoordinate(f"nt_pred_{sex}_{sn_fstt_label}_{n_fstt_label}", nt_pred.tolist(), fstt_label=f"sn:{sn_fstt_label}, n:{n_fstt_label}")
    
    def onCreateAdditionalMeasurements(self):
        try:
            if not self.softTissueNode:
                raise ValueError("Please select soft tissue landmarks first (PS_soft_tissue).")
            
            if not self.hardTissueNode:
                raise ValueError("Hard tissue landmarks not found.")
            
            self.step5StatusLabel.setText("Status: Creating additional measurements...")
            slicer.app.processEvents()
            
            baselineNode = slicer.util.getFirstNodeByName("baseline")
            if baselineNode:
                baseline_start = np.zeros(3)
                baseline_end = np.zeros(3)
                baselineNode.GetNthControlPointPosition(0, baseline_start)
                baselineNode.GetNthControlPointPosition(1, baseline_end)
                baseline_dir = (baseline_end - baseline_start)
                baseline_dir = baseline_dir / np.linalg.norm(baseline_dir)
            else:
                n_soft = self.getPointByLabel(self.softTissueNode, "n'")
                baseline_dir = np.array([1.0, 0.0, 0.0])
                baseline_start = n_soft. copy()
                baseline_end = n_soft + baseline_dir * 100.0
                baselineNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "baseline")
                baselineNode.AddControlPoint(baseline_start.tolist())
                baselineNode.AddControlPoint(baseline_end.tolist())
            
            n_hard = self.getPointByLabel(self.hardTissueNode, "n")
            n_soft = self.getPointByLabel(self.softTissueNode, "n'")
            nn_dist = self.createMeasurementLine("n-n'", n_hard, n_soft)
            self.storeMeasurement("n-n'", nn_dist)
            
            rhi_hard = self.getPointByLabel(self.hardTissueNode, "rhi")
            rhi_soft = self.getPointByLabel(self.softTissueNode, "rhi'")
            rhi_dist = self.createMeasurementLine("rhi-rhi'", rhi_hard, rhi_soft)
            self.storeMeasurement("rhi-rhi'", rhi_dist)
            
            sn = self.getPointByLabel(self.softTissueNode, "sn'")
            
            alL = self.getPointByLabel(self.softTissueNode, "X1(alL)")
            alR = self.getPointByLabel(self.softTissueNode, "X2(alR)")
            al_dist = self.createMeasurementLine("al-al", alL, alR)
            self.storeMeasurement("al-al", al_dist)
            
            nbL = self.getPointByLabel(self.softTissueNode, "Y1(nbL)")
            nbR = self.getPointByLabel(self.softTissueNode, "Y2(nbR)")
            nb_dist = self.createMeasurementLine("nb-nb", nbL, nbR)
            self.storeMeasurement("nb-nb", nb_dist)
            
            P, Q, xy_dist = self.shortestDistanceBetweenLines(alL, alR, nbL, nbR)
            self.createMeasurementLine("X-Y", P, Q)
            self.storeMeasurement("X-Y", xy_dist)
            
            nt = self.getPointByLabel(self.softTissueNode, "nt")
            n_nt_dist = self.createMeasurementLine("soft n-nt", n_soft, nt)
            self.storeMeasurement("soft n-nt", n_nt_dist)
            
            prn = self.getPointByLabel(self.softTissueNode, "prn")
            prn_proj = baseline_start + np.dot(prn - baseline_start, baseline_dir) * baseline_dir
            prn_perp_dist = self.createMeasurementLine("prn perp baseline", prn, prn_proj)
            self.storeMeasurement("prn perp baseline", prn_perp_dist)
            
            rhi_prn_sn_angle = self.createAngle("soft rhi'-prn-sn'", rhi_soft, prn, sn)
            self.storeMeasurement("soft rhi'-prn-sn'", rhi_prn_sn_angle, "degrees")
            
            prn_sn_nt_angle = self.createAngle("prn-sn'-nt", prn, sn, nt)
            self.storeMeasurement("prn-sn'-nt", prn_sn_nt_angle, "degrees")
            
            al_prn_al_angle = self.createAngle("al-prn-al", alL, prn, alR)
            self.storeMeasurement("al-prn-al", al_prn_al_angle, "degrees")
            
            self.step5StatusLabel.setText("Status: ✅ All additional measurements created successfully!")
            self.step5StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            slicer.util.showStatusMessage("Additional measurements complete!", 3000)
            
            self.updateResultsTables()
            
        except Exception as e:
            self.step5StatusLabel.setText("Status: ❌ Error - {0}". format(str(e)))
            self.step5StatusLabel.setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to create additional measurements: {0}".format(str(e)))
    
    def createMeasurementLine(self, name, point1, point2):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        line_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", name)
        line_node.AddControlPoint(point1.tolist())
        line_node.AddControlPoint(point2.tolist())
        display_node = line_node.GetDisplayNode()
        if display_node:
            display_node. SetTextScale(3.0)
        return np.linalg.norm(point2 - point1)
    
    def createAngle(self, name, point1, apex, point2):
        existing = slicer.util.getFirstNodeByName(name)
        if existing:
            slicer.mrmlScene.RemoveNode(existing)
        
        angle_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsAngleNode", name)
        angle_node.AddControlPoint(point1.tolist())
        angle_node.AddControlPoint(apex.tolist())
        angle_node.AddControlPoint(point2.tolist())
        display_node = angle_node. GetDisplayNode()
        if display_node:
            display_node.SetTextScale(3.0)
        return angle_node. GetAngleDegrees()
    
    def shortestDistanceBetweenLines(self, p1, p2, q1, q2):
        v = p2 - p1
        u = q2 - q1
        w0 = p1 - q1
        
        a = np.dot(v, v)
        b = np.dot(v, u)
        c = np.dot(u, u)
        d = np.dot(v, w0)
        e = np.dot(u, w0)
        
        denom = a * c - b * b
        
        if abs(denom) < 1e-6:
            t = np.dot(v, w0) / a if a > 0 else 0
            t = max(0, min(1, t))
            closest_on_line1 = p1 + t * v
            s = 0.5
            closest_on_line2 = q1 + s * u
            distance = np.linalg.norm(closest_on_line2 - closest_on_line1)
            return closest_on_line1.astype(float), closest_on_line2.astype(float), distance
        
        s = (b * e - c * d) / denom
        t = (a * e - b * d) / denom
        
        s = max(0, min(1, s))
        t = max(0, min(1, t))
        
        P = p1 + s * v
        Q = q1 + t * u
        distance = np.linalg.norm(P - Q)
        
        return P.astype(float), Q.astype(float), distance
    
    def onCalculateErrors(self):
        try:
            if not self.softTissueNode:
                raise ValueError("Please select soft tissue landmarks first.")
            
            self.step5StatusLabel.setText("Status: Calculating errors...")
            slicer.app.processEvents()
            
            pred_male = slicer.util.getFirstNodeByName('pred_soft_tissue_male')
            pred_female = slicer.util.getFirstNodeByName('pred_soft_tissue_female')
            
            if not pred_male and not pred_female:
                raise ValueError("No predictions found. Please run Step 4 first.")
            
            errors = []
            
                # ========== PRONASALE ERRORS ==========
            try:
                true_prn = self.getPointByLabel(self.softTissueNode, "prn")
                
                if pred_male:
                    pred_prn_male = self.getPointByLabel(pred_male, "pred_prn_male")
                    self.createLine(pred_prn_male, true_prn, "error_prn_male", [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
                    error_dist = np.linalg.norm(pred_prn_male - true_prn)
                    errors.append("Male pronasale error: {0:.2f} mm".format(error_dist))
                    self.storeMeasurement("ERROR: Pronasale (male)", error_dist, "mm", is_summary=True)
                    
                    if "Pronasale (male)" in self.all_coordinates:
                        self.all_coordinates["Pronasale (male)"]["true"] = true_prn
                
                if pred_female: 
                    pred_prn_female = self.getPointByLabel(pred_female, "pred_prn_female")
                    self.createLine(pred_prn_female, true_prn, "error_prn_female", [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
                    error_dist = np.linalg.norm(pred_prn_female - true_prn)
                    errors.append("Female pronasale error: {0:.2f} mm".format(error_dist))
                    self.storeMeasurement("ERROR: Pronasale (female)", error_dist, "mm", is_summary=True)
                    
                    if "Pronasale (female)" in self.all_coordinates:
                        self.all_coordinates["Pronasale (female)"]["true"] = true_prn
            except ValueError:
                print("⚠️ True pronasale (prn) landmark not found")
            
            # ========== SUBNASALE (sn') FSTT ERRORS ==========
            if self.pred_FSTT_sn: 
                try:
                    pred_sn_fstt = self.getPointByLabel(self.pred_FSTT_sn, "sn'_FSTT")
                    true_sn = self.getPointByLabel(self.softTissueNode, "sn'")
                    self.createLine(pred_sn_fstt, true_sn, "error_FSTT_sn", [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 0.2)
                    error_dist = np.linalg.norm(pred_sn_fstt - true_sn)
                    errors.append("FSTT sn' error: {0:.2f} mm".format(error_dist))
                    self.storeMeasurement("ERROR: FSTT sn'", error_dist, "mm", is_summary=True)
                    self.storeCoordinate("Subnasale (FSTT)", pred_sn_fstt, true_sn)
                except ValueError:
                    print("⚠️ True subnasale (sn') landmark not found")

            # ========== NASION (n') FSTT ERRORS ==========
            try:
                true_n_soft = self.getPointByLabel(self.softTissueNode, "n'")
                
                # Check each prediction node for n' predictions
                for sex in ['male', 'female', 'nonsex']:
                    pred_node_name = 'pred_soft_tissue_{0}'.format(sex)
                    pred_node = slicer.util.getFirstNodeByName(pred_node_name)
                    
                    if pred_node:
                        # Find predicted n' FSTT
                        for i in range(pred_node.GetNumberOfControlPoints()):
                            label = pred_node.GetNthControlPointLabel(i)
                            if "n'_FSTT" in label:
                                pred_n_soft = self.getPoint(pred_node, i)
                                n_error = np.linalg.norm(pred_n_soft - true_n_soft)
                                
                                self.storeMeasurement("ERROR: n' FSTT ({0})".format(sex), n_error, "mm", is_summary=True)
                                
                                # Update the stored coordinate with true value
                                coord_key = "n' ({0})".format(sex)
                                if coord_key in self.all_coordinates:
                                    self.all_coordinates[coord_key]["true"] = true_n_soft
                                
                                errors.append("n' FSTT error ({0}): {1:.2f} mm".format(sex, n_error))
                                print("✅ n' error for {0}: {1:.2f} mm".format(sex, n_error))
                                break
            except ValueError:
                print("⚠️ True nasion soft tissue (n') landmark not found")

            # ========== NASION TIP (nt) ERRORS ==========
            try:
                true_nt = self.getPointByLabel(self.softTissueNode, "nt")
                
                for sex in ['male', 'female']:
                    pred_node_name = 'pred_soft_tissue_{0}'.format(sex)
                    pred_node = slicer.util.getFirstNodeByName(pred_node_name)
                    
                    if pred_node:
                        # Find predicted nt
                        for i in range(pred_node.GetNumberOfControlPoints()):
                            label = pred_node.GetNthControlPointLabel(i)
                            if 'pred_nt' in label:
                                pred_nt = self.getPoint(pred_node, i)
                                nt_error = np.linalg.norm(pred_nt - true_nt)
                                
                                self.storeMeasurement("ERROR: nt ({0})".format(sex), nt_error, "mm", is_summary=True)
                                
                                # Update coordinate with true value
                                coord_key = "nt ({0})".format(sex)
                                if coord_key in self.all_coordinates:
                                    self.all_coordinates[coord_key]["true"] = true_nt
                                
                                errors.append("nt error ({0}): {1:.2f} mm".format(sex, nt_error))
                                print("✅ nt error for {0}: {1:.2f} mm".format(sex, nt_error))
                                break
            except ValueError:
                print("⚠️ True nasion tip (nt) landmark not found")
            
            self.step5StatusLabel.setText("Status: ✅ Errors calculated!")
            self.step5StatusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            self.updateResultsTables()

            if errors:
                msg = qt.QMessageBox()
                msg.setIcon(qt.QMessageBox.Information)
                msg.setText("Prediction Errors Calculated")
                msg.setInformativeText("\n".join(errors))
                msg.setWindowTitle("Validation Results")
                msg.exec_()
            else:
                slicer.util.messageBox("No errors could be calculated. Check that true landmarks exist.")
            
            
        except Exception as e:
            self.step5StatusLabel.setText("Status: ❌ Error - {0}".format(str(e)))
            self.step5StatusLabel. setStyleSheet("color: red; font-weight: bold;")
            slicer.util.errorDisplay("Failed to calculate errors: {0}".format(str(e)))
    
    def updateResultsTables(self):
        self.updateMeasurementsTable()
        self.updateCoordinatesTable()
    
    def updateMeasurementsTable(self):
        self.measurementsTable.setRowCount(len(self.all_measurements))
        
        row = 0
        for name, data in sorted(self.all_measurements.items()):
            name_item = qt.QTableWidgetItem(name)
            name_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            value_item = qt.QTableWidgetItem("{0:.2f}".format(data["value"]))
            value_item.setFlags(qt.Qt. ItemIsEnabled | qt.Qt. ItemIsSelectable)
            
            unit_item = qt.QTableWidgetItem(data["unit"])
            unit_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            
            if data. get("is_summary", False):
                yellow = qt.QColor(255, 255, 200)
                name_item.setBackground(yellow)
                value_item.setBackground(yellow)
                unit_item.setBackground(yellow)
                
                font = qt.QFont()
                font.setBold(True)
                name_item.setFont(font)
                value_item.setFont(font)
                unit_item. setFont(font)
            
            self.measurementsTable. setItem(row, 0, name_item)
            self.measurementsTable.setItem(row, 1, value_item)
            self.measurementsTable.setItem(row, 2, unit_item)
            
            row += 1
        
        self.measurementsTable.resizeColumnsToContents()
    
    def updateCoordinatesTable(self):
        self.coordinatesTable.setRowCount(len(self.all_coordinates))
        
        row = 0
        for landmark_name, coords in sorted(self.all_coordinates.items()):
            name_item = qt.QTableWidgetItem(landmark_name)
            name_item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            self.coordinatesTable.setItem(row, 0, name_item)
            
            pred_coords = coords["predicted"]
            true_coords = coords. get("true", None)
            
            for col, val in enumerate([pred_coords[0], pred_coords[1], pred_coords[2]]):
                item = qt.QTableWidgetItem("{0:.2f}".format(val))
                item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
                self.coordinatesTable.setItem(row, col + 1, item)
            
            if true_coords is not None:
                for col, val in enumerate([true_coords[0], true_coords[1], true_coords[2]]):
                    item = qt.QTableWidgetItem("{0:.2f}".format(val))
                    item.setFlags(qt. Qt.ItemIsEnabled | qt. Qt.ItemIsSelectable)
                    item.setBackground(qt.QColor(220, 255, 220))
                    self.coordinatesTable.setItem(row, col + 4, item)
                
                error_3d = np.linalg.norm(pred_coords - true_coords)
                error_item = qt.QTableWidgetItem("{0:.2f}".format(error_3d))
                error_item.setFlags(qt. Qt.ItemIsEnabled | qt. Qt.ItemIsSelectable)
                error_item.setBackground(qt. QColor(255, 220, 220))
                font = qt.QFont()
                font.setBold(True)
                error_item.setFont(font)
                self.coordinatesTable.setItem(row, 7, error_item)
            else:
                for col in range(4, 8):
                    item = qt.QTableWidgetItem("N/A")
                    item. setFlags(qt.Qt.ItemIsEnabled)
                    self.coordinatesTable.setItem(row, col, item)
            
            row += 1
        
        self.coordinatesTable.resizeColumnsToContents()
    
    def onCopyMeasurements(self):
        try:
            if not self.all_measurements:
                slicer.util.warningDisplay("No measurements available to copy.  Please run the prediction and measurements first.")
                return
            
            export_text = "Measurement\tValue\tUnit\n"
            
            for name, data in sorted(self.all_measurements.items()):
                value_str = "{0:.2f}".format(data["value"])
                export_text += "{0}\t{1}\t{2}\n". format(name, value_str, data["unit"])
            
            qt.QApplication.clipboard().setText(export_text)
            
            self.step6StatusLabel.setText("Status: ✅ Measurements copied to clipboard!  Ready to paste into Excel.")
            slicer.util.showStatusMessage("Measurements copied!", 3000)
            
        except Exception as e:
            slicer.util.errorDisplay("Failed to copy measurements: {0}".format(str(e)))
    
    def onCopyCoordinates(self):
        """Copy coordinates table to clipboard"""
        try: 
            if not self.all_coordinates:
                slicer.util.warningDisplay("No coordinates available to copy. Please run the prediction first.")
                return
            
            # Create tab-separated values (TSV) format with headers
            export_text = "Landmark\tPredicted X\tPredicted Y\tPredicted Z\tTrue X\tTrue Y\tTrue Z\t3D Error (mm)\n"
            
            for landmark_name, coords in sorted(self.all_coordinates.items()):
                pred = coords["predicted"]
                true_coords = coords.get("true", None)
                
                if true_coords is not None: 
                    # Calculate 3D error
                    error_3d = np.linalg.norm(pred - true_coords)
                    # Format each value separately to avoid format specifier issues
                    export_text += "{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6:.2f}\t{7:.2f}\n".format(
                        landmark_name,
                        float(pred[0]), float(pred[1]), float(pred[2]),
                        float(true_coords[0]), float(true_coords[1]), float(true_coords[2]),
                        float(error_3d)
                    )
                else:
                    # No true coordinates available
                    export_text += "{0}\t{1:.2f}\t{2:.2f}\t{3:.2f}\tN/A\tN/A\tN/A\tN/A\n".format(
                        landmark_name,
                        float(pred[0]), float(pred[1]), float(pred[2])
                    )
            
            # Copy to clipboard
            qt.QApplication.clipboard().setText(export_text)
            
            # Show success message
            self.step6StatusLabel.setText("Status: ✅ Coordinates copied to clipboard! Ready to paste into Excel.")
            slicer.util.showStatusMessage("Coordinates copied!", 3000)
            
        except Exception as e: 
            import traceback
            traceback.print_exc()
            slicer.util.errorDisplay("Failed to copy coordinates: {0}".format(str(e)))
    
    def onPrevButtonClicked(self):
        if self.currentStep > 0:
            self.currentStep -= 1
            self.updateStepUI()
    
    def onNextButtonClicked(self):
        if self.currentStep < self.stepStack.count - 1:
            self.currentStep += 1
            self.updateStepUI()
    
    def updateStepUI(self):
        self.stepStack.setCurrentIndex(self.currentStep)
        self.stepLabel.setText("Step {0}/{1}".format(self.currentStep + 1, self.stepStack.count))
        self.prevButton.setEnabled(self.currentStep > 0)
        self.nextButton.setEnabled(self.currentStep < self.stepStack.count - 1)


# Create and show the widget
widget = PurkaitSinghGUI()
widget.show()
