# SPDX-FileCopyrightText: 2024 EasyReflectometryApp contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2024 Contributors to the EasyReflectometryApp project <https://github.com/easyscience/EasyReflectometryApp>

import sys

from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import qInstallMessageHandler

from EasyApp.Logic.Logging import console

from Logic.Py.backend_proxy import BackendProxy

CURRENT_DIR = Path(__file__).parent                                 # path to qml components of the current project
EASYAPP_DIR = CURRENT_DIR / '..' / '..' / '..' / 'EasyApp' / 'src'  # path to qml components of the easyapp module
MAIN_QML = CURRENT_DIR / 'main.qml'                                 # path to the root qml file


if __name__ == '__main__':
    qInstallMessageHandler(console.qmlMessageHandler)
    console.debug('Custom Qt message handler defined')

    app = QGuiApplication(sys.argv)
    console.debug(f'Qt Application created {app}')

    engine = QQmlApplicationEngine()
    console.debug(f'QML application engine created {engine}')

    backend_proxy = BackendProxy()
    engine.rootContext().setContextProperty('backend_proxy_py', backend_proxy)
    console.debug('backend_proxy object exposed to QML as backend_proxy_py')

    engine.addImportPath(EASYAPP_DIR)
    engine.addImportPath(CURRENT_DIR)
    console.debug('Paths added where QML searches for components')

    engine.load(MAIN_QML)
    console.debug('Main QML component loaded')

    console.debug('Application event loop is about to start')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
