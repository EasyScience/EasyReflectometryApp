import os
import sys
import pathlib
import platform
import argparse
import darkdetect

# PySide
from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import Qt
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView  # to call hook-PySide2.QtWebEngineWidgets.py

# easyScience
import EasyReflectometryApp
import toml
import easyApp
from easyscience.fitting import available_minimizers
# from easyApp.Logic.Maintenance import Updater
# from easyApp.Logic.Translate import Translator
from EasyReflectometryApp.Logic.PyQmlProxy import PyQmlProxy

# Global vars
def proj():
    project_fname = 'pyproject.toml'
    try:
        return toml.load(os.path.join(os.path.split(__file__)[0], project_fname))
    except FileNotFoundError:
        up_directory = os.path.join(os.path.split(__file__)[0], '..') 
        return toml.load(os.path.join(up_directory, project_fname)) 

CONFIG = proj()


class App(QApplication):
    def __init__(self, sys_argv):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # DOESN'T WORK?!, USE SCRIPT INSTEAD
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
        super(App, self).__init__(sys_argv)

def main():
    print(available_minimizers.installed_packages)
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logtofile', action='store_true',
                        help='enable logging in the file EasyReflectometry.log in the system directory tmp instead of the terminal')
    parser.add_argument('-t', '--testmode', action='store_true',
                    help='run the application in test mode: run the tutorial, record a video and exit the application')
    args = parser.parse_args()
    if args.logtofile:
        from easyApp.Logic import Logging

    # Paths
    project_name = CONFIG['project']['name'] + 'App'
    current_path = EasyReflectometryApp.__path__[0]
    
    package_path = os.path.join(current_path, f'{project_name}')
    if not os.path.exists(package_path):
        package_path = current_path

    main_qml_path = QUrl.fromLocalFile(os.path.join(package_path, 'Gui', 'main.qml'))
    gui_path = str(QUrl.fromLocalFile(package_path).toString())
    app_icon_path = os.path.join(package_path, 'Gui', 'Resources', 'Logo', 'App.png')
    easyApp_path = os.path.join(easyApp.__path__[0], '..')

    home_path = pathlib.Path.home()
    settings_path = str(home_path.joinpath(f'.{project_name}', 'settings.ini'))

    # QtWebEngine
    QtWebEngine.initialize()

    # Application
    app = App(sys.argv)
    app.setApplicationName(CONFIG['project']['name'])
    app.setApplicationVersion(CONFIG['project']['version'])
    app.setOrganizationName(CONFIG['project']['name'])
    app.setOrganizationDomain(CONFIG['project']['name'])
    app.setWindowIcon(QIcon(app_icon_path))

    # QML application engine
    engine = QQmlApplicationEngine()

    # Python objects to be exposed to QML
    py_qml_proxy_obj = PyQmlProxy()

    # Expose the Python objects to QML
    engine.rootContext().setContextProperty('_pyQmlProxyObj', py_qml_proxy_obj)
    engine.rootContext().setContextProperty('_settingsPath', settings_path)
    engine.rootContext().setContextProperty('_projectConfig', CONFIG)
    engine.rootContext().setContextProperty('_isTestMode', args.testmode)
    try:
        isDark = darkdetect.isDark()
    except FileNotFoundError:
        isDark = False
    engine.rootContext().setContextProperty('_isSystemThemeDark', isDark)

    # Register types to be instantiated in QML
    # qmlRegisterType(Updater, 'easyApp.Logic.Maintenance', 1, 0, 'Updater')

    # Add paths to search for installed modules
    engine.addImportPath(easyApp_path)
    engine.addImportPath(gui_path)

    # Load the root QML file
    engine.load(main_qml_path)

    # Customize app window titlebar
    if platform.system() == "Darwin":
        import ctypes, objc, Cocoa

        # Root application window
        root_obj = engine.rootObjects()
        if not root_obj:
            sys.exit(-1)
        root_window = root_obj[0]

        ptr = int(root_window.winId())
        view = objc.objc_object(c_void_p=ctypes.c_void_p(ptr))
        window = view._.window

        window.setStyleMask_(window.styleMask() | Cocoa.NSFullSizeContentViewWindowMask)
        window.setTitlebarAppearsTransparent_(True)
        window.setTitleVisibility_(Cocoa.NSWindowTitleHidden)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
