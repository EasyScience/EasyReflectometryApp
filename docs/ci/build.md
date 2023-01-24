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