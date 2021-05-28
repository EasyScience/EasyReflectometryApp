## [![CI Build][20]][21] [![Release][30]][31] [![Downloads][70]][71] [![Lines of code][82]][80] [![Total lines][81]][80] [![Files][83]][80] [![License][50]][51]

<img height="80"><img src="./resources/images/er_logo.svg" height="65">

**easyReflectometry** is a scientific software for modelling and analysis of diffraction data. Currently, **easyReflectometry** covers classical 1D unpolarized neutron powder diffraction data collected at constant wavelength.

![easyReflectometry Screenshot](./resources/images/er_analysis_dark.png) 

## What is easyReflectometry for?

**easyReflectometry** allows simulation of diffraction patterns based on a structural model and refinement of its parameters. For refinement, the program uses a number of fitting engines (minimizers).

**easyReflectometry** is similar to crystallographic programs like FullProf, Jana, GSAS, ShelX, etc. Unlike these programs **easyReflectometry** is based on _external_ crystallographic libraries such as [CrysPy](https://github.com/ikibalin/cryspy), [CrysFML](https://code.ill.fr/scientific-software/crysfml) and [GSAS-II](https://subversion.xray.aps.anl.gov/trac/pyGSAS). This allows **easyReflectometry** to cover different functionality aspects within a single, intuitive and user-friendly graphical interface. These libraries are included with the installation so there is no need to download and compile any additional components.

## Main features

**easyReflectometry** is open source (currently [GPL v3](LICENSE.md)) and cross-platform, with support for Windows, macOS and Linux (Ubuntu).

The intuitive tabbed interface allows for a clear and defined data modelling and analysis workflow. There are also built-in step-by-step user guides and video tutorials for new users.

Current main features of **easyReflectometry**:

- Support for constant-wavelength 1D unpolarized neutron powder diffraction data.
- Structure refinement (yet unstable) using [CrysPy](https://github.com/ikibalin/cryspy), [CrysFML](https://code.ill.fr/scientific-software/crysfml) and [GSAS-II](https://subversion.xray.aps.anl.gov/trac/pyGSAS).
- Simulations of diffraction pattern using aforementioned libraries.
- Multiple minimization engines: [lmfit](https://lmfit.github.io/lmfit-py), [bumps](https://github.com/bumps/bumps) and [DFO-LS](https://github.com/numericalalgorithmsgroup/dfols).
- Crystal structure visualizer and builder.
- Diffraction pattern viewer, including Bragg peaks and difference curve.
- Live update of calculations on parameters change.
- Input files are in [CIF (Crystallographic Information File)](https://www.iucr.org/resources/cif) format.
- Interactive HTML and standard PDF report generation.
- Undo/redo for both parameter changes and fitting.

Planned improvements / new functionality for **easyReflectometry**:

- Improved refinement.
- Parameter constraints during refinement.
- Loading and simulation of Time-of-Flight data.
- Support for polarized neutron data.
- Magnetic structure refinement.
- Pair distribution function.
- X-ray data analysis.

## Getting Started

### Downloading

Download the official **easyReflectometry installer v0.8.0-beta** for your operating system:

- [Windows 10 and above, 32-bit](https://github.com/easyScience/easyReflectometryApp/releases/download/v0.8.0-beta.1/easyReflectometry_Windows_x86-32_v0.8.0-beta.1.zip)
- [macOS 10.15 and above, 64-bit](https://github.com/easyScience/easyReflectometryApp/releases/download/v0.8.0-beta.1/easyReflectometry_macOS_x86-64_v0.8.0-beta.1.zip)
- [Ubuntu 20.04 and above, 64-bit](https://github.com/easyScience/easyReflectometryApp/releases/download/v0.8.0-beta.1/easyReflectometry_Linux_x86-64_v0.8.0-beta.1.zip)

### Installing

Run **easyReflectometry installer** and follow the instructions.

macOS: If you see the message _easyReflectometrySetup.app can't be opened because it is from an unidentified developer_, do the following:
In the **Finder**, locate the **easyReflectometry installer app**, then _control-click_ the app icon, then choose _Open_ from the shortcut menu and finally click _Open_.

### Uninstalling

Run **MaintenanceTool** from the **easyReflectometry** installation directory, select _Remove all components_ and follow the instructions.

## Get in touch

For general questions or comments, please contact us at [support@easyReflectometry.org](mailto:support@easyReflectometry.org).

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
