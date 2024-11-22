# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import importlib
import Functions, Config


CONFIG = Config.Config()


def pythonLibLocation():
    if len(sys.argv) > 1:
        return os.path.join(sys.argv[1], 'lib')
    return '@rpath'


def pythonDylib():
    python_dylib_file = {
        # 'macos': 'Python',
        'macos': 'libpython3.7m.dylib',
        'ubuntu': 'libpython3.7m.so.1.0',
        'windows': None
    }[CONFIG.os]
    return None if python_dylib_file is None else os.path.join(pythonLibLocation(), python_dylib_file)


def crysfmlPythonDylib():
    d = {
        #'macos': '/Library/Frameworks/Python.framework/Versions/3.7/Python',
        'macos': '/usr/local/Cellar/python@3.7/3.7.9/Frameworks/Python.framework/Versions/3.7/lib/libpython3.7m.dylib',
        'ubuntu': 'libpython3.7m.so.1.0',
        'windows': None
    }
    return d[CONFIG.os]


def rpath():
    d = {
        'macos': '@executable_path',
        'ubuntu': './libsLinux/lib',
        'windows': None
    }
    return d[CONFIG.os]


#def crysfmlRpath():
#    d = {
#        'macos': '/opt/intel//compilers_and_libraries_2020.2.258/mac/compiler/lib',
#        'ubuntu': None,
#        'windows': None
#    }
#    return d[CONFIG.os]


def crysfmlSoFile():
    lib = CONFIG['ci']['pyinstaller']['libs'][CONFIG.os]
    lib_path = importlib.import_module(lib).__path__[0]
    so_location = os.path.join(lib_path, 'CFML_api')
    so_file = {
        'macos': 'crysfml_api.so',
        'ubuntu': 'crysfml_api.so',
        'windows': None
    }[CONFIG.os]
    return None if so_file is None else os.path.join(so_location, so_file)


def relinkCrysfml():
    if CONFIG.os == 'windows':
        Functions.printNeutralMessage(f'No CrysFML relinking is needed for platform {CONFIG.os}')
        return

    Functions.printNeutralMessage(f"pythonLibLocation: {pythonLibLocation()}")
    Functions.printNeutralMessage(f"crysfmlPythonDylib: {crysfmlPythonDylib()}")
    Functions.printNeutralMessage(f"pythonDylib: {pythonDylib()}")
    #Functions.printNeutralMessage(f"crysfmlRpath: {crysfmlRpath()}")
    Functions.printNeutralMessage(f"rpath: {rpath()}")
    Functions.printNeutralMessage(f"crysfmlSoFile: {crysfmlSoFile()}")

    try:
        message = f'relink CrysFML from default Python dylib for platform {CONFIG.os}'
        if CONFIG.os == 'macos':
            Functions.run('otool', '-l', crysfmlSoFile())
            Functions.run('otool', '-L', crysfmlSoFile())
            #Functions.run('install_name_tool', '-rpath', crysfmlRpath(), rpath(), crysfmlSoFile())
            ##Functions.run('install_name_tool', '-add_rpath', rpath(), crysfmlSoFile())
            ##Functions.run('install_name_tool', '-add_rpath', pythonLibLocation(), crysfmlSoFile())
            Functions.run('install_name_tool', '-change', crysfmlPythonDylib(), pythonDylib(), crysfmlSoFile())
            Functions.run('otool', '-l', crysfmlSoFile())
            Functions.run('otool', '-L', crysfmlSoFile())
        elif CONFIG.os == '---ubuntu':
            Functions.run('sudo', 'apt-get', 'update', '-y')
            Functions.run('sudo', 'apt-get', 'install', '-y', 'patchelf')
            Functions.run('sudo', 'apt-get', 'install', '-y', 'chrpath')
            # Python lib
            Functions.run('chrpath', '--list', crysfmlSoFile())
            Functions.run('patchelf', '--set-rpath', rpath(), crysfmlSoFile())
            #Functions.run('patchelf', '--replace-needed', crysfmlPythonDylib(), pythonDylib(), crysfmlSoFile())
            # Intel fortran libs
            # Instead of LD_LIBRARY_PATH...
            #import libsLinux
            #lib_path = os.path.join(list(libsLinux.__path__)[0], 'lib')
            #libs = ['libifcoremt.so.5', 'libifport.so.5', 'libimf.so', 'libintlc.so.5', 'libsvml.so']
            #for lib in libs:
            #    Functions.run('patchelf', '--replace-needed', lib, os.path.join(lib_path, lib), crysfmlSoFile())
            # https://nehckl0.medium.com/creating-relocatable-linux-executables-by-setting-rpath-with-origin-45de573a2e98
            # https://github.com/microsoft/ShaderConductor/issues/52
            # https://unix.stackexchange.com/questions/479421/how-to-link-to-a-shared-library-with-a-relative-path
        else:
            Functions.printFailMessage(f'Platform {CONFIG.os} is unsupported')
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    relinkCrysfml()
