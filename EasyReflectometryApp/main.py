# SPDX-FileCopyrightText: 2024 EasyReflectometryApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyReflectometryApp project <https://github.com/easyscience/EasyReflectometryApp>

import sys
from pathlib import Path

from EasyApp.Logic.Logging import console
from PySide6.QtCore import QUrl
from PySide6.QtCore import qInstallMessageHandler
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterSingletonType

try:  # Running from installer
    from EasyReflectometryApp.Backends.Py import PyBackend
    from EasyReflectometryApp.Backends.Py.helpers import Application

    INSTALLER = True
except ImportError:  # Running locally
    from Backends.Py import PyBackend
    from Backends.Py.helpers import Application

    INSTALLER = False

CURRENT_DIR = Path(__file__).parent  # path to qml components of the current project


if __name__ == '__main__':
    qInstallMessageHandler(console.qmlMessageHandler)
    console.debug('Custom Qt message handler defined')

    app = Application(sys.argv)  # Create the QApplication (Not QGuiApplication)
    console.debug(f'Qt Application created {app}')

    engine = QQmlApplicationEngine()
    console.debug(f'QML application engine created {engine}')

    qmlRegisterSingletonType(PyBackend, 'Backends', 1, 0, 'PyBackend')
    console.debug('Backend class is registered to be accessible from QML via the name PyBackend')

    if INSTALLER:
        path_main_qml = QUrl.fromLocalFile(CURRENT_DIR / 'EasyReflectometryApp' / 'Gui' / 'ApplicationWindow.qml')
        engine.addImportPath(QUrl.fromLocalFile(CURRENT_DIR / 'EasyReflectometryApp').toString())
        engine.addImportPath(QUrl.fromLocalFile(CURRENT_DIR / '..' / 'EasyApp' / 'src').toString())
        console.debug('Paths added where QML searches for components')
    else:
        path_main_qml = path_main_qml = CURRENT_DIR / 'Gui' / 'ApplicationWindow.qml'  # Running locally
        engine.addImportPath(CURRENT_DIR)
        engine.addImportPath(CURRENT_DIR / '..' / '..' / 'EasyApp' / 'src')
        console.debug('Paths added where QML searches for components')

    engine.load(path_main_qml)
    console.debug('Main QML component loaded')

    console.debug('Application event loop is about to start')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
