# Installation

To make the installation of easyReflectometry as easy as possible, we prepare packaged releases for three major operating systems: 

- [Windows](https://github.com/easyScience/easyReflectometryApp/releases/download/v0.0.2-beta.1/easyReflectometry_Windows_x86-32_v0.0.2-beta.1.zip)
- [macOS](https://github.com/easyScience/easyReflectometryApp/releases/download/v0.0.2-beta.1/easyReflectometry_macOS_x86-64_v0.0.2-beta.1.zip) (built on 10.15)
- [Linux](https://github.com/easyScience/easyReflectometryApp/releases/download/v0.0.2-beta.1/easyReflectometry_Linux_x86-64_v0.0.2-beta.1.zip) (built on Ubuntu-20.04)

If the relevant easyReflectometry installation does not work on your system, then please try installation from source. 

## Installation from source

1. Install [**Poetry**](https://python-poetry.org/docs/) isolated from the rest of your system (recommended)
  ```
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  ```
2. Clone **easyReflectometryApp** repo from GitHub
  ```
  git clone https://github.com/easyScience/easyReflectometryApp
  ```
3. Go to **easyReflectometryApp** directory
4. Create virtual environment for **easyReflectometryApp** and install its dependences using **poetry** 
  ```
  poetry install
  ```  
5. Launch **easyReflectometry** application using **poetry**
  ```
  poetry run easyReflectometry
  ```

It is also possible to install [poetry within a conda](https://anaconda.org/conda-forge/poetry) environment [if you really need to](https://xkcd.com/1987/), but this is not recommended.