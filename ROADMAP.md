# Roadmap for EasyReflectometry

This documents the planned roadmap for the EasyReflectometry project (containing both [EasyReflectometryApp]() and [EasyReflectometryLib]()) between now and the start of 2027. 
Certain tasks may depend on other Easy-family projects (in particular EasyCore) which will be be noted, where relevant. 

```mermaid
gantt
    title EasyReflectometry Roadmap Nov 2022-Jan 2027
    dateFormat  YYYY-MM
    axisFormat  %Y-%m
    todaymarker off

    section General
    User experience enhancement :a1, 2022-12, 24w
    Resolution smearing :a2, 2023-04, 8w
    File IO :a3, after a1, 16w
    Video Tutorials :a4, after d3, 16w
    Ready for real users: milestone, m1, after a3, 2min

    section New functionality
    Mixed models :b1, after m1, 20w
    ESS integration :b2, after c2, 20w
    Bayesian analysis :b3, after b2, 30w
    Ready for first ESS instruments :milestone, m2, after b2, 2min
    ESS Start of User Operation :milestone, m3, 2026-11, 2min

    section Hard Condensed Matter
    Magnetism support :c1, after m1, 52w
    Polarisation analysis :c2, after c1, 24w

    section Item Library
    Bilayer item :d1, 2023-01, 8w
    Material gradient :d2, after a2, 8w
    Mixed surfactant layer :d3, after b1, 8w
    Bilayer with embedded protein :d4, after c1, 16w
    Mixed bilayer item :d5, after c2, 8w

```

Above we include a Gannt chart showing the roadmap. 
Each epic in this chart can be correlated with a heading below which details it. 
In time, each epic will be populated with a series of issues relating to the part of the Easy-family of projects that it pertains to.
Issues that are general to EasyReflectometry (i.e. those related to interaction with the userbase) will be defined as EasyReflectometryApp issues.  

## Epics details 

### User experience enhancement

The aim of this epic is to improve the user experience in EasyReflectometry. 
Currently, there are a performance issues and user-unfriendly interfaces that should be improved. 
This has the additional benefit of reducing technical debt. 
This includes work such as improving visualisation and adding code signing. 

<!-- #### EasyReflectometryApp issues

- Transition to model `dicttoxml` functionality from EasyCore
- Project pane visualisation
- Summary pane visualisation
- App signing for all platforms
- Example projects
- Improvements to constraint setting UI
- Visualisation of multiple contrasts simultaneously  -->

### Resolution smearing

Currently, we only support a constant Gaussian $q$-resolution function. 
However, many reflectometry analysis libraries support $q$-dependent Gaussian resolution and even arbitrary function resolutions. 

### FileIO

This epic will enable greater interoperability with other analysis packages and plotting software. 
This includes adding functionality for a ORSO model definition file (to be defined) and the ability to output easily data from EasyReflectometry for plotting in other packages

<!-- - Saving model as a data file
- Saving plots/data with greater user control. This could be done with adding new columns to the .ort file for model reflectometry. -->

### Video tutorials

Short video tutorials to accompany example projects.
These can be hosted on YouTube or similar and linked to from easyreflectometry.org.

### Mixed models

`refnx` has the functionality to produce an [incoherent sum of two different models](https://refnx.readthedocs.io/en/stable/refnx.reflect.html#refnx.reflect.MixedReflectModel). 
This is important in accounting for non-uniform films/surfaces. 

### ESS integration

This means integration with the SciCat data catalogue, such that ESS data can be easily loaded to EasyReflectometry. 
Additionally, it will include the use of `scipp` as a data storage object and `plopp` plotting functionality. 

### Bayesian analysis 

Bayesian sampling methods are becoming a more and more important tool in reflectometry analysis. 
While it may be possible to enable this by outputting models built in EasyReflectometry to `refl1d` or `refnx` Python environments, it would be cleaner to have the functionality available in EasyReflectometry. 
This would involve significant EasyCore work, in addition to the development of an EasyApp pane for sampling visualisaton (also beneficial to a potential EasyQens). 

### Magnetism support 

This will begin with enabling the magnetism functionality available in `refl1d`, concurrent to which the graphical user interface will be designed with input from the relevant user communities. 

### Polarisation analysis 

Enabling the analysis of difference between different spin flipper state

### Bilayer item

Introduces a phospholipid bilayer item to the item library. 

### Material gradient

Introduces a material that describes a gradient (with a couple of different function forms) of one material present in another. 

### Mixed surfactant layer

Using the [mixed model](#mixed-models) functionality, making it possible to define more than one surfactant in a layer. 

### Bilayer with embedded protein

A bilayer item but with some concentration of protein embedded in the layer. 
Initially the protein describe would be basic (linking potentially to the protein-SLD calculator) but in future this could be expanded to include the protein-SLD calculator functionality or data from crystallographic or simulation results. 

### Mixed bilayer item 

Using the [mixed model](#mixed-models) functionality, making it possible to define more than one phospholipid type in a bilayer.  