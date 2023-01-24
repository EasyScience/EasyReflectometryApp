
# Continuous integration

## Building

The aim of building the application and library is to create an accessible, either via PyPI, `snap`, or an executable installer, the EasyReflectometry application and library.

### `EasyReflectometryLib`

Based on [ADR0002](./adrs/adr0002), the only expected method of installation for the Python library is via PyPI (or some other `pip` compatible approach). 
Therefore, the building of `EasyReflectometryLib` is achieved through relatively standard Github actions for pushing built Python modules to PyPI.
This is achieved though common approaches, discussed in [this PyPA documentation](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/), specifically the Github action defined in the [`python-publish.yml` workflow](https://github.com/easyScience/EasyReflectometryLib/blob/main/.github/workflows/python-publish.yml). 

### `EasyReflectometryApp`

