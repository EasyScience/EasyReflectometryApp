# Installation

To make the installation of EasyReflectometry as easy as possible, we prepare packaged releases for three major operating systems: 

- [Windows](https://github.com/easyScience/EasyReflectometryApp/releases/download/v0.0.10-beta/EasyReflectometry_Windows_x86-32_v0.0.10-beta.exe)
- [macOS](https://github.com/easyScience/EasyReflectometryApp/releases/download/v0.0.10-beta/EasyReflectometry_macOS_x86-64_v0.0.10-beta.zip) (built on 10.15)
- [Linux](https://github.com/easyScience/EasyReflectometryApp/releases/download/v0.0.10-beta/EasyReflectometry_Linux_x86-64_v0.0.10-beta.zip) (built on Ubuntu-20.04)

If the relevant EasyReflectometry installation does not work on your system, then please try installation from source. 

## Installation from source

1. Install [**Poetry**](https://python-poetry.org/docs/) isolated from the rest of your system (recommended)
  ```
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  ```
2. Clone **EasyReflectometryApp** repo from GitHub
  ```
  git clone https://github.com/easyScience/EasyReflectometryApp
  ```
3. Go to **EasyReflectometryApp** directory
4. Create virtual environment for **EasyReflectometryApp** and install it and its dependences using **pip** 
  ```
  pip install .
  ```  
5. Launch **EasyReflectometry** application using **poetry**
  ```
  python EasyReflectometryApp/main.py
  ```

It is also possible to install [poetry within a conda](https://anaconda.org/conda-forge/poetry) environment [if you really need to](https://xkcd.com/1987/), but this is not recommended.
