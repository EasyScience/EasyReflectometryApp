## [![CI Build][20]][21] [![Release][30]][31] [![Downloads][70]][71] [![Lines of code][82]][80] [![Total lines][81]][80] [![Files][83]][80] [![License][50]][51]

<img height="80"><img src="./resources/images/er_logo.svg" height="65">

**easyReflectometry** is a scientific software for modelling and analysis of reflectometry data. Currently, **easyReflectometry** covers single contrast measurements of layered structures.

![easyReflectometry Screenshot](./resources/images/er_analysis_dark.png) 

## What is easyReflectometry for?

**easyReflectometry** allows simulation of reflectometry profiles based on layered structures and the refinements of the structural parameters. For refinement, the program uses a number of fitting engines (minimizers).

**easyReflectometry** offers a graphical user interface for the analysis of reflectometry data, build on _external_ reflectometry packages such as [refnx](https://refnx.readthedocs.io/en/latest/). 
This allows **easyReflectometry** to cover different functionality aspects within a signle, intuitive, and user-friendly interface.  
The reflectomety packages are included with the installation so there is no need to download andn compile any additional components. 

## Main features

**easyReflectometry** is open source (currently [GPL v3](LICENSE.md)) and cross-platform, with support for Windows, macOS and Linux (Ubuntu).

The intuitive tabbed interface allows for a clear and defined data modelling and analysis workflow. 
There are also built-in step-by-step user guides and video tutorials for new users.

Current main features of **easyReflectometry**:

- Support for the analysis of a single contrast of reflectometry data
- Creation of materials to be used in structure from scattering length density
- The ability to define repeating multi-layers of materials and refine these structures using [refnx](https://refnx.readthedocs.io/en/latest/). 
- Multiple minimization engines: [lmfit](https://lmfit.github.io/lmfit-py), [bumps](https://github.com/bumps/bumps) and [DFO-LS](https://github.com/numericalalgorithmsgroup/dfols) (including the differential evolution method).
- Interactive HTML and standard PDF report generation.
- Undo/redo for both parameter changes and fitting 
- Saving and loading of projects

Planned improvements / new functionality for **easyReflectometry**:

- The addition of the [bornagain](https://www.bornagainproject.org) and [refl1d](https://refl1d.readthedocs.io/en/latest/) reflectometry packages for reflectometry calculation
- Ability to corefine multiple contrasts of reflectometry data
- Expansion of the flexible _item_ type to include chemical consistent models
- Support for polarised reflectometry measurements
- Reading of q-dependent resolution from a file

## Getting Started

### Downloading

Download the official **easyReflectometry installer v0.0.1-develop** for your operating system:

- [Windows 10 and above, 32-bit](https://github.com/easyScience/easyReflectometryApp/releases/download/develop/easyReflectometry_Windows_x86-32_v0.0.1_develop.zip)
- [macOS 10.15 and above, 64-bit](https://github.com/easyScience/easyReflectometryApp/releases/download/develop/easyReflectometry_macOS_x86-64_v0.0.1_develop.zip)
- [Ubuntu 20.04 and above, 64-bit](https://github.com/easyScience/easyReflectometryApp/releases/download/develop/easyReflectometry_Linux_x86-64_v0.0.1_develop.zip)

### Installing

Run **easyReflectometry installer** and follow the instructions.

macOS: If you see the message _easyReflectometrySetup.app can't be opened because it is from an unidentified developer_, do the following:
In the **Finder**, locate the **easyReflectometry installer app**, then _control-click_ the app icon, then choose _Open_ from the shortcut menu and finally click _Open_.

### Uninstalling

Run **MaintenanceTool** from the **easyReflectometry** installation directory, select _Remove all components_ and follow the instructions.

## Get in touch

<!---For general questions or comments, please contact us at [support@easyReflectometry.org](mailto:support@easyReflectometry.org).--->

For bug reports and feature requests, please use [Issue Tracker](https://github.com/easyScience/easyReflectometryApp/issues) instead.

<!---URLs--->
<!---https://naereen.github.io/badges/--->

<!---CI Build Status--->

[20]: https://img.shields.io/github/workflow/status/easyScience/easyReflectometryApp/build%20macOS,%20Linux,%20Windows/ci
[21]: https://github.com/easyScience/easyReflectometryApp/actions?query=workflow%3A%22build+macOS%2C+Linux%2C+Windows%22

<!---Release--->

[30]: https://img.shields.io/github/release/easyScience/easyReflectometryApp.svg?include_prereleases
[31]: https://github.com/easyScience/easyReflectometryApp/releases

<!---License--->

[50]: https://img.shields.io/github/license/easyScience/easyReflectometryApp.svg
[51]: https://github.com/easyScience/easyReflectometryApp/blob/master/LICENSE.md

<!---LicenseScan--->

[60]: https://app.fossa.com/api/projects/git%2Bgithub.com%2FeasyScience%2FeasyReflectometryApp.svg?type=shield
[61]: https://app.fossa.com/projects/git%2Bgithub.com%2FeasyScience%2FeasyReflectometryApp?ref=badge_shield

<!---Downloads--->

[70]: https://img.shields.io/github/downloads/easyScience/easyReflectometryApp/total.svg
[71]: https://github.com/easyScience/easyReflectometryApp/releases

<!---Code statistics--->

[80]: https://github.com/easyScience/easyReflectometryApp
[81]: https://tokei.rs/b1/github/easyScience/easyReflectometryApp
[82]: https://tokei.rs/b1/github/easyScience/easyReflectometryApp?category=code
[83]: https://tokei.rs/b1/github/easyScience/easyReflectometryApp?category=files

<!---W3C validation--->

[90]: https://img.shields.io/w3c-validation/default?targetUrl=https://easyscience.github.io/easyReflectometryApp
[91]: https://easyscience.github.io/easyReflectometryApp
