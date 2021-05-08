<img src="https://easyReflectometry.github.io/images/easyReflectometry-logo.svg" height="80"><img width="15"><img src="https://easyReflectometry.github.io/images/easyReflectometry-text.svg" height="80">

**easyReflectometry** is a scientific software for modelling and analysis of the diffraction data.

## Dev info

[![CI Build][20]][21]

[![Release][30]][31]

[![Downloads][70]][71] [![Lines of code][82]][80] [![Total lines][81]][80] [![Files][83]][80]

[![License][50]][51]

[![w3c][90]][91]

### Download easyReflectometryApp repo
* Open **Terminal** 
* Change the current working directory to the location where you want the **easyReflectometryApp** directory
* Clone **easyReflectometryApp** repo from GitHub using **git**
  ```
  git clone https://github.com/easyScience/easyReflectometryApp
  ```
  
### Install easyReflectometryApp dependencies
* Open **Terminal**
* Install [**Poetry**](https://python-poetry.org/docs/) (Python dependency manager)
  * osx / linux / bashonwindows
    ```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    ```
  * windows powershell
    ```
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
    ```
* Go to **easyReflectometryApp** directory
* Create virtual environment for **easyReflectometryApp** and install its dependences using **poetry** (configuration file: **pyproject.toml**)
  ```
  poetry install
  ```
  
### Launch easyReflectometryApp application
* Open **Terminal**
* Go to **easyReflectometryApp** directory
* Launch **easyReflectometry** application using **poetry**
  ```
  poetry run easyReflectometry
  ```

### Update easyReflectometryApp dependencies
* Open **Terminal**
* Go to **easyReflectometryApp** directory
* Update **easyReflectometryApp** using **poetry** (configuration file: **pyproject.toml**)
  ```
  poetry update
  ```

### Delete easyReflectometryApp
* Delete **easyReflectometryApp** directory
* Uninstall **Poetry**
   * osx / linux / bashonwindows
   ```
   curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_UNINSTALL=1 python
   ```

<!---URLs--->
<!---https://naereen.github.io/badges/--->

<!---CI Build Status--->
[20]: https://github.com/easyScience/easyReflectometryApp/workflows/build%20macOS,%20Linux,%20Windows/badge.svg
[21]: https://github.com/easyScience/easyReflectometryApp/actions?query=workflow%3A%22build+macOS%2C+Linux%2C+Windows%22

<!---Release--->
[30]: https://img.shields.io/github/release/easyScience/easyReflectometryApp.svg
[31]: https://github.com/easyScience/easyReflectometryApp/releases

<!---License--->
[50]: https://img.shields.io/github/license/easyScience/easyReflectometryApp.svg
[51]: https://github.com/easyScience/easyReflectometryApp/blob/master/LICENSE.md

<!---LicenseScan--->
[60]: https://app.fossa.com/api/projects/git%2Bgithub.com%2FeasyScience%easyReflectometryApp.svg?type=shield
[61]: https://app.fossa.com/projects/git%2Bgithub.com%2FeasyScience%easyReflectometryApp?ref=badge_shield

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
