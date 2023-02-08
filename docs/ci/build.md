# Building

The aim of building the application and library is to create an accessible, either via PyPI, `snap`, or an executable installer, the EasyReflectometry application and library.

## `EasyReflectometryLib`

Based on [ADR0002](./adrs/adr0002), the only expected method of installation for the Python library is via PyPI (or some other `pip` compatible approach). 
Therefore, the building of `EasyReflectometryLib` is achieved through relatively standard Github actions for pushing built Python modules to PyPI.
This is achieved though common approaches, discussed in [this PyPA documentation](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/), specifically the Github action defined in the [`python-publish.yml` workflow](https://github.com/easyScience/EasyReflectometryLib/blob/main/.github/workflows/python-publish.yml). 

## `EasyReflectometryApp`

The `EasyReflectometryApp` building continuous integration is much more complex, consisting of three individual processes:

- Pushing the Python package to PyPI, such that it may be installed via `pip`. 
- Building an executable installer, for Windows and macOS. 
- Building a `snap` image, for use with Ubuntu-based Linux distributions.

The first of these, is straightforward to achieve, by the same process as in `EasyReflectometryLib`. 
The second is more complex and requires a multi-step [Github action](https://github.com/easyScience/EasyReflectometryApp/blob/main/.github/workflows/build_executable.yml). 
This action performs the following steps: 

1. A Python environment (currently 3.9) is set up and the [`ci` dependencies](https://github.com/easyScience/EasyReflectometryApp/blob/main/pyproject.toml) are intstalled. 
2. A series of environment variables are set, mostly related to the git state at the time. These are used in the built app to give extra information regarding provenence. 
3. The application bundle is then created and the installers are produced using [PyInstaller](https://pyinstaller.org/en/stable/). 
4. These are installed on the build machines and the application is launched (and then quit), to test if the build is at least in part successful. 
5. The installers are then made available for [testing](#testing) as Github artifacts of the action. 
6. If the build is happening on the `master` branch, the installer is also added to a release.

### Testing

#### Executables

The executables for Windows and macOS can be found in the artifacts of the Github action that ran. 
You can download the relevant execuatable and install this on your machine. 
Test out, locally, that the new functionality works as expected. 

#### `snap` image

To test the `snap` build, download the `.snap` image from the Github artifacts and run the following. 

```console 
snap install --devmode *.snap
```