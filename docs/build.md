# Development Env

The EasyReflectometry project consists of two packages; an application and a library. 
To develop effectively for EasyReflectometry, we work on the `develop` branch of both and then periodically merge to `master` when a release is made. 

With this in mind, the best way to build a development environment for EasyReflectometry is as follows. 

```console
$ mamba create -y -n easy_refl python=3.9
$ mamba activate easy_refl
$ git clone git@github.com:easyScience/EasyReflectometryLib.git
$ cd EasyReflectometryLib
$ git checkout develop
$ pip install -e .
$ cd ../
```

Then, to that you are working with your local version of `EasyReflectometryLib`, you want to change line 35 of the `EasyReflectometryApp` `pyproject.toml` file from

```toml
'EasyReflectometryLib @ git+https://github.com/easyScience/EasyReflectometryLib.git@develop',
```

to use the directory where you have cloned `EasyReflectometryLib`, i.e.

```toml
'EasyReflectometryLib @ file:///path/to/EasyReflectometryLib',
```

With this modification in place, you should then be able to install `EasyReflectometryApp`

```console
$ git clone git@github.com:easyScience/EasyReflectometryApp.git
$ cd EasyReflectometryApp
$ git checkout develop
$ pip install -e .
```

Note, that the use of `mamba` is a personal choice, if you prefer building Python environments with `pyenv` that should also work. 
This will build, in-place, versions of both the application and the library. 
The application can then be run (from within the appropriate Python environment) with the following. 

```console
$ EasyReflectometry
```

## Additional requirements

Some additional requirements exist that are operating system specific. 

### Linux

```console
sudo apt install libxcb-xinerama0
```
