__author__ = ["github.com/AndrewSazonov", "github.com/arm61"]
__version__ = '0.0.1'

from typing import List
import os
import sys
import glob
import site
import PySide2
import shiboken2
import refnx
import refl1d
import periodictable
import easyCore
import easyApp
import EasyReflectometry
import Functions
import Config
from PyInstaller.__main__ import run as pyInstallerMain

CONFIG = Config.Config()


def appIcon() -> str:
    """
    :return: definition of the app icon path
    """
    icon_dir = os.path.join(*CONFIG['ci']['app']['icon']['dir'])
    icon_name = CONFIG['ci']['app']['icon']['file_name']
    icon_ext = CONFIG['ci']['app']['icon']['file_ext'][CONFIG.os]
    icon_path = os.path.join(CONFIG.package_name, icon_dir, f'{icon_name}{icon_ext}')
    icon_path = os.path.abspath(icon_path)
    return f'--icon={icon_path}'


def excludedModules() -> List[str]:
    """
    :return: list of modules to exclude from frozen app.
    """
    os_independent = CONFIG['ci']['pyinstaller']['auto_exclude']['all']
    os_dependent = CONFIG['ci']['pyinstaller']['auto_exclude'][CONFIG.os]
    formatted = []
    for module_name in os_independent:
        formatted.append('--exclude-module')
        formatted.append(module_name)
    for module_name in os_dependent:
        formatted.append('--exclude-module')
        formatted.append(module_name)
    return formatted


def addedData() -> List[str]:
    """
    :return: list of add-data commands for PyInstaller.
    """
    data = [{
        'from': CONFIG.package_name,
        'to': CONFIG.package_name
    }, {
        'from': refnx.__path__[0],
        'to': 'refnx'
    }, {
        'from': refl1d.__path__[0],
        'to': 'refl1d'
    }, {
        'from': periodictable.__path__[0],
        'to': 'periodictable'
    }, {
        'from': easyCore.__path__[0],
        'to': 'easyCore'
    }, {
        'from': EasyReflectometry.__path__[0],
        'to': 'EasyReflectometryLib'
    }, {
        'from': easyApp.__path__[0],
        'to': 'easyApp'
    }, {
        'from': 'utils.py',
        'to': '.'
    }, {
        'from': 'pyproject.toml',
        'to': '.'
    }]
    # Add other missing libs
    missing_other_libraries = CONFIG['ci']['pyinstaller']['missing_other_libraries'][
        CONFIG.os]
    if missing_other_libraries:
        for lib_file in missing_other_libraries:
            data.append({'from': lib_file, 'to': '.'})
    # Use the last element, since on certain conda installations
    # we get more than one entry
    site_packages_path = site.getsitepackages()[-1]
    missing_calculator_libs = CONFIG['ci']['pyinstaller']['missing_calculator_libs'][
        CONFIG.os]
    if missing_calculator_libs:
        for lib_name in missing_calculator_libs:
            lib_path = os.path.join(site_packages_path, lib_name)
            data.append({'from': lib_path, 'to': lib_name})
    # Format for pyinstaller
    separator = CONFIG['ci']['pyinstaller']['separator'][CONFIG.os]
    formatted = []
    for element in data:
        formatted.append(f'--add-data={element["from"]}{separator}{element["to"]}')
    return formatted


def copyMissingLibs():
    """
    Copies the missing libraries, specifically those for PySide2.
    """
    missing_files = CONFIG['ci']['pyinstaller']['missing_pyside2_files'][CONFIG.os]
    if len(missing_files) == 0:
        Functions.printNeutralMessage(f'No missing PySide2 libraries for {CONFIG.os}')
        return
    try:
        message = 'copy missing PySide2 libraries'
        pyside2_path = PySide2.__path__[0]
        shiboken2_path = shiboken2.__path__[0]
        for file_name in missing_files:
            file_path = os.path.join(shiboken2_path, file_name)
            for file_path in glob.glob(file_path):  # for cases with '*' in the lib name
                Functions.copyFile(file_path, pyside2_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def copyMissingPlugins():
    """
    Copies missing plugins for PySide2.
    """
    missing_plugins = CONFIG['ci']['pyinstaller']['missing_pyside2_plugins'][CONFIG.os]
    if len(missing_plugins) == 0:
        Functions.printNeutralMessage(f'No missing PySide2 plugins for {CONFIG.os}')
        return
    try:
        message = 'copy missing PySide2 plugins'
        pyside2_path = PySide2.__path__[0]
        app_plugins_path = os.path.join(CONFIG.dist_dir, CONFIG.app_name, 'PySide2',
                                        'plugins')
        for relative_dir_path in missing_plugins:
            src_dir_name = os.path.basename(relative_dir_path)
            src_dir_path = os.path.join(pyside2_path, relative_dir_path)
            dst_dir_path = os.path.join(app_plugins_path, src_dir_name)
            Functions.copyDir(src_dir_path, dst_dir_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def excludeFiles():
    """
    Removes files to be excluded from the installer.
    """
    file_names = CONFIG['ci']['pyinstaller']['manual_exclude']
    if len(file_names) == 0:
        Functions.printNeutralMessage(f'No libraries to be excluded for {CONFIG.os}')
        return
    try:
        message = 'exclude files'
        for file_name in file_names:
            dir_suffix = CONFIG['ci']['pyinstaller']['dir_suffix'][CONFIG.os]
            content_suffix = CONFIG['ci']['pyinstaller']['content_suffix'][CONFIG.os]
            freezed_app_path = os.path.join(CONFIG.dist_dir,
                                            f'{CONFIG.app_name}{dir_suffix}',
                                            f'{content_suffix}')
            file_path = os.path.join(freezed_app_path, file_name)
            for file_path in glob.glob(file_path):  # for cases with '*' in the lib name
                Functions.removeFile(file_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def runPyInstaller():
    """
    Constructs and runs the pyInstallerMain.
    """
    try:
        message = 'freeze app'
        main_py_path = os.path.join(CONFIG.package_name, 'main.py')
        pyInstallerMain([
            # Application main file
            main_py_path,
            # Name to assign to the bundled app and spec file
            # (default: first script’s basename)
            f'--name={CONFIG.app_name}',
            # LEVEL may be one of DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO)
            '--log-level', 'WARN',
            # Replace output directory (default: SPECPATH/dist/SPECNAME)
            # without asking for confirmation
            '--noconfirm',
            # Clean PyInstaller cache and remove temporary files before building
            '--clean',
            # Windows and Mac OS X: do not provide a console window for standard i/o
            '--windowed',
            # Create a one-folder bundle containing an executable (default)
            '--onedir',
            # Folder to store the generated spec file (default: current directory)
            # '--specpath', workDirPath(),
            # Where to put the bundled app (default: ./dist)
            '--distpath', CONFIG.dist_dir,
            # Where to put all the temporary work files,
            # .log, .pyz and etc. (default: ./build)
            '--workpath', CONFIG.build_dir,
            *excludedModules(),
            *addedData(),
            appIcon()
        ])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    copyMissingLibs()
    copyMissingPlugins()
    runPyInstaller()
    excludeFiles()
