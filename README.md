# Forensic Craniofacial Approximation Database
Often comparisons of the theoretical and anatomical basis, data collection methods, reliability and success rates, as well as details of the sample population used to establish these guides cannot be readily made due to their heterogeneity, leaving them to interpret these recommendations and assess their limitations.
To improve repeatibility of forensic craniofacial approximation methods, this project aims to “translate” well-known techniques into the world of medical imaging and Python with the help of the open-source programme, 3D Slicer. Please visit their official website for  more information and free download.

All methodology was developed on [NMDID](https://nmdid.unm.edu/welcome)[^1] post-mortem CTs (Edgar, HJH; Daneshvari Berry, S; Moes, E; Adolphi, NL; Bridges, P; Nolte, KB (2020). New Mexico Decedent Image Database. Office of the Medical Investigator, University of New Mexico. doi.org/10.25827/5s8c-n515.)  but are shown in the guides using the Sample Data by 3D Slicer which is openly accessible.

If this is your first time working with Slicer, please start in the "Start here" folder and First Steps.md file.

When noticing any errors, please contact me!

This is a work in progress repository, so take everything with a pinch of salt :)

> [!IMPORTANT]
> Please note that these guidelines are the researcher’s interpretation of the cited literature. If you notice any errors or have any questions, please do not hesitate to get in touch at [e.m.somjai@dundee.ac.uk](mailto:e.m.somjai@dundee.ac.uk). 

For most protocols, the first step is the re-orientation of the scan in the Frankfort Horizontal Plane (FHP), so that navigating the models become easier. 
  - For a step-by-step tutorial,  please visit [this page](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/002_Realign%20CT%20in%20the%20standard%20FHP.md)
  - For the .json file and code only, go to [this release](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/tree/001_CodeForFHPAlignment))
If you choose to do a segmentation, follow the tutorial at [ROI vs Segmentation](https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/003_Roi%20vs%20Segmentation.md)

Do not forget to re-visit the [tutorial] (https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/blob/basics/004_Copying%20measurements%20to%20Clipboard.md) or [code]  (https://github.com/esomjai/ForensicCraniofacialApproximationDatabase/releases/tag/CopyMeasurementsToClipboard) for copying measurements to the clipboard

Currently available methodologies for nose approximation and their original papers are: 

Method name | Method reference | Step-by-step explanation | Graphic User Interface
-- | -- | -- | --
Two Tangent | Gerasimow, 1955 | (link)[https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/0b9f33b72407d2e59e15148d74327f73cfa04910/Nose%20predictions/Gerasimow-MaltaisLapointe%20Two%20tangent%20method.md] | (link)[https://github.com/esomjai/Forensic-Craniofacial-Approximation-Database/blob/0b9f33b72407d2e59e15148d74327f73cfa04910/Nose%20predictions/Gerasimow%20Maltais-LaPointe%20GUI.md]
Compound | Macho, 1956 | 10.1520/JFS11917J |
Threefold ANS | Krogman & Iscan, 1986 | 0-398-08878-0 |
Aesthetic Method | Prokopec & Ubelaker, 2002 | [link](https://archives.fbi.gov/archives/about-us/lab/forensic-science-communications/fsc/jan2002/prokopec.htm)
Stephan's method | Stephan et al. 2003 | [10.1002/ajpa.10300](https://doi.org/10.1002/ajpa.10300)
Rynn method | Rynn et al. 2012 | 
Utsuno method | Utsuno et al. 2016 | 199.9997
Davy-Jow | Davy-Jow et al., 2012 | 200
(unknown) | rhi parallel proj | 199.9997
(unknown) | 5 P max proj | 14.30314
(unknown) | 7 height of rhinion | 16.57942
(unknown) | 6 prominence of rhinion in relation to the n-aca plane | 8.777521
(unknown) | 4 P max | 8.010799
(unknown) | 9 angle between plane n-aca and rhi-aca plane | 13.37417









[^1]: Edgar, HJH; Daneshvari Berry, S; Moes, E; Adolphi, NL; Bridges, P; Nolte, KB (2020). New Mexico Decedent Image Database. Office of the Medical Investigator, University of New Mexico. doi.org/10.25827/5s8c-n515.
