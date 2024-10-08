# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

#import argparse
#import orjson
#import os
#import pathlib
#import sys
#import decimal
#import importlib.util
import numpy as np
from uncertainties import ufloat

#from PySide6.QtCore import Qt, QObject, QCoreApplication, QUrl, Signal, Slot, Property
#from PySide6.QtGui import QStyleHints
from PySide6.QtWidgets import QApplication

#from EasyApp.Logic.Logging import console


# class EasyAppLoader:

#     @staticmethod
#     def terminateIfNotFound():
#         easyAppSpec = importlib.util.find_spec("EasyApp")
#         if easyAppSpec is not None:
#             return

#         print('No EasyApp specs found')
#         sys.exit(1)


# class PersistentSettingsHandler:

#     def __init__(self):
#         self.path = self.getPath()

#     def getPath(self):
#         appName = QCoreApplication.instance().applicationName()
#         homeDirPath = pathlib.Path.home()
#         name = 'settings.ini'
#         path = str(homeDirPath.joinpath(f'.{appName}', name))
#         console.info(f'Persistent settings: {path}')
#         return path


# class ResourcePaths:

#     def __init__(self):
#         self.mainQml = 'Gui/main.qml'  # Current app main.qml file
#         self.splashScreenQml = 'Gui/Components/SplashScreen.qml'  # Splash screen .qml file
#         self.imports = []  # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
#         self.setPaths()

#     def setPaths(self):
#         try:
#             import resources
#             self.mainQml = f'qrc:/{self.mainQml}'
#             self.splashScreenQml = f'qrc:/{self.splashScreenQml}'
#             self.imports.append('qrc:/')
#             resourcesPath = resources.__file__
#             console.info(f'Resources: {resourcesPath}')
#         except ImportError:
#             self.imports.append('.')
#             console.debug('No python resources (rc) file found')

#         import EasyApp
#         easyAppPath = os.path.abspath(EasyApp.__path__[0])
#         self.imports.append(os.path.join(easyAppPath, '..'))
#         console.info(f'EasyApp module: {easyAppPath}')


# class CommandLineArguments:

#     def __new__(cls):
#         parser = argparse.ArgumentParser()

#         parser.add_argument(
#             '-t',
#             '--testmode',
#             action='store_true',
#             help='run the application in test mode: run tests, take screenshots and exit the application'
#         )

#         return parser.parse_args()


# class EnvironmentVariables:

#     @staticmethod
#     def set():
#         # see https://doc.qt.io/qt-6/qtquick3d-requirements.html
#         #os.environ['QSG_RHI_BACKEND'] = 'opengl'  # Requests the specific RHI backend. For QtCharts XYSeries useOpenGL
#         os.environ['QT_RHI_SHADER_DEBUG'] = '1'    # Enables the graphics API implementation's debug
#         os.environ['QSG_INFO'] = '1'               # Printing system information when initializing the Qt Quick scene graph
#         # misc
#         #qsetenv("QT_QPA_PLATFORM", "windows:darkmode=[1|2]")
#         #os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=[1|2]'
#         #os.environ['QT_MESSAGE_PATTERN'] = "\033[32m%{time h:mm:ss.zzz}%{if-category}\033[32m %{category}:%{endif} %{if-debug}\033[34m%{function}%{endif}%{if-warning}\033[31m%{backtrace depth=3}%{endif}%{if-critical}\033[31m%{backtrace depth=3}%{endif}%{if-fatal}\033[31m%{backtrace depth=3}%{endif}\033[0m %{message}"


# class WebEngine:

#     @staticmethod
#     def initialize():
#         try:
#             from PySide6.QtWebEngineQuick import QtWebEngineQuick
#         except ModuleNotFoundError:
#             console.debug('No module named "PySide6.QtWebEngineQuick" is found')
#             pass
#         else:
#             QtWebEngineQuick.initialize()

#     @staticmethod
#     def runJavaScriptWithoutCallback(webEngine, script):
#         callback = None
#         webEngine.runJavaScript(script, callback)


class IO:

    @staticmethod
    def generalizePath(fpath: str) -> str:
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        return fpath  # NEED FIX: Check on different platforms
        # filename = urlparse(fpath).path
        # if not sys.platform.startswith("win"):
        #     return filename
        # if filename[0] == '/':
        #     filename = filename[1:].replace('/', os.path.sep)
        # return filename

    @staticmethod
    def formatMsg(type, *args):
        types = {'main': '*', 'sub': '  -'}
        mark = types[type]
        widths = [22,21,20,10]
        widths[0] -= len(mark)
        msgs = []
        for idx, arg in enumerate(args):
            msgs.append(f'{arg:<{widths[idx]}}')
        msg = ' ▌ '.join(msgs)
        msg = f'{mark} {msg}'
        return msg

    @staticmethod
    def toStdDevSmalestPrecision(value, std_dev):
        if std_dev > 1:
            value_str = f'{round(value)}'
            std_dev_str = f'{round(std_dev)}'
            value_with_std_dev_str = f'{value_str}({std_dev_str})'
        else:
            precision = 1
            std_dev_decimals = precision - int(np.floor(np.log10(std_dev) + 1))
            std_dev = round(std_dev, std_dev_decimals)
            std_dev_str = f'{std_dev:.{std_dev_decimals}f}'
            value = round(value, std_dev_decimals)
            value_str = f'{value:.{std_dev_decimals}f}'
            clipped_std_dev = int(round(std_dev * 10**std_dev_decimals))
            value_with_std_dev_str = f'{value_str}({clipped_std_dev})'
        return value_str, std_dev_str, value_with_std_dev_str

    @staticmethod
    def toStdDevSmalestPrecision_OLD(value, std_dev):
        if std_dev < 10:
            fmt = '.1u'
        else:
            fmt = 'u'
        value_str, std_dev_str = f'{ufloat(value, std_dev):{fmt}}'.split('+/-')
        value_with_std_dev_str = f'{ufloat(value, std_dev):{fmt}S}'
        return value_str, std_dev_str, value_with_std_dev_str

    def value_with_error_WEB(val, err, precision=2):
        """String with value and error in parenthesis with the number of digits given by precision."""
        # Number of digits in the error
        err_decimals = precision - int(np.floor(np.log10(err) + 1))
        # Output error with a "precision" number of significant digits
        err_out = round(err, err_decimals)
        # Removes leading zeros for fractional errors
        if err_out < 1:
            err_out = int(round(err_out * 10**err_decimals))
            err_format = 0
        else:
            err_format = int(np.clip(err_decimals, 0, np.inf))

        # Format the value to have the same significant digits as the error
        val_out = round(val, err_decimals)
        val_format = int(np.clip(err_decimals, 0, np.inf))

        return f'{val_out:.{val_format}f}({err_out:.{err_format}f})'

      
# class Converter:

#     @staticmethod
#     def jsStrToPyBool(value):
#         if value == 'true':
#             return True
#         elif value == 'false':
#             return False
#         else:
#             #console.debug(f'Input value "{value}" is not supported. It should either be "true" or "false".')
#             pass

#     @staticmethod
#     def dictToJson(obj):
#         # Dump to json
#         dumpOption = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
#         jsonBytes = orjson.dumps(obj, option=dumpOption)
#         json = jsonBytes.decode()
#         return json
#         #if not formatted:
#         #    return jsonStr
#         ## Format to have arrays shown in one line. Can orjson do this?
#         #formatOptions = jsbeautifier.default_options()
#         #formatOptions.indent_size = 2
#         #formattedJsonStr = jsbeautifier.beautify(jsonStr, formatOptions)
#         #return formattedJsonStr


class Application(QApplication):  # QGuiApplication crashes when using in combination with QtCharts
    def __init__(self, sysArgv):
        super(Application, self).__init__(sysArgv)
        self.setApplicationName('EasyReflectometry')
        self.setOrganizationName('EasyScience')
        self.setOrganizationDomain('easyscience.software')


# class ColorSchemeHandler(QObject):
#     systemColorSchemeChanged = Signal()

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._styleHints = QApplication.instance().styleHints()
#         self.schemes = { Qt.ColorScheme.Unknown: 0,
#                          Qt.ColorScheme.Light: 1,
#                          Qt.ColorScheme.Dark: 2 }
#         self._systemColorScheme = self.schemes[self._styleHints.colorScheme()]
#         console.debug(f"Initial system color scheme: {self._systemColorScheme} (0 - unknown, 1 - light, 2 - dark)")
#         self._styleHints.colorSchemeChanged.connect(self.onSystemColorSchemeChanged)

#     @Property(int, notify=systemColorSchemeChanged)
#     def systemColorScheme(self):
#         return self._systemColorScheme

#     def onSystemColorSchemeChanged(self):
#         console.debug(f"Previous system color scheme: {self._systemColorScheme}")
#         self._systemColorScheme = self.schemes[self._styleHints.colorScheme()]
#         console.debug(f"New system color scheme: {self._systemColorScheme}")
#         self.systemColorSchemeChanged.emit()


# class BackendHelpers(QObject):

#     def __init__(self, parent=None):
#         super().__init__(parent)

#     @Slot(str, result=str)
#     def urlToLocalFile(self, url: str):
#         fpath = QUrl(url).toLocalFile()
#         return fpath

#     @Slot(str, result=str)
#     def localFileToUrl(self, fpath: str):
#         url = QUrl.fromLocalFile(fpath).toString()
#         return url

#     @Slot(int)
#     def exitApp(self, exitCode):
#         console.debug(f'Force exiting application with code {exitCode}')
#         os._exit(exitCode)

#     @Slot(str, result=bool)
#     def fileExists(self, path):
#         exists = pathlib.Path(path).is_file()
#         #if exists:
#         #    console.debug(f'File {path} exists')
#         #else:
#         #    console.debug(f"File {path} doesn't exist")
#         return exists

#     @Slot('QVariant', result=str)
#     def listToUri(self, fpathParts):
#         fpathParts = fpathParts.toVariant()
#         fpath = os.path.join(*fpathParts)
#         if fpath[:2] == ':/':  # qrc format
#             return 'qrc' + fpath
#         exists = pathlib.Path(fpath).is_file()
#         if not exists:
#             return ''
#         furi = pathlib.Path(fpath).as_uri()
#         if sys.platform.startswith("win") and furi[0] == '/':
#             furi = furi[1:].replace('/', os.path.sep)
#         return furi

#     #@Slot(float, int, result=str)
#     #def toPrecision(self, x, n):
#     #    return str(decimal.Context(prec=n).create_decimal_from_float(x))

#     #@Slot(float, float, int, result=str)
#     #def toOtherPrecision(self, x, s, n):
#     #    xStr = f'{x}'
#     #    sStr = self.toPrecision(s, n)
#     #    return str(decimal.Decimal(xStr).quantize(decimal.Decimal(sStr)))

#     @Slot(float, float, result='QVariant')
#     def toStdDevSmalestPrecision(self, value, std_dev):
#         value_str, std_dev_str, _ = IO.toStdDevSmalestPrecision(value, std_dev)
#         return {'value': value_str, 'std_dev': std_dev_str}


# class PyProxyWorker(QObject):
#     createdAndMovedToMainThread = Signal()

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.proxy = None

#     def createAndMoveToMainThread(self):
#         from Logic.PyProxy import PyProxy
#         #time.sleep(0.5)
#         #console.debug('Slept for 0.5s to allow splash screen to start')
#         #mainThread = QCoreApplication.instance().thread()
#         mainThread = QApplication.instance().thread()
#         console.debug(f'Main thread id:{id(mainThread)} found')
#         self.proxy = PyProxy()
#         console.debug(f'PyProxy object id:{id(self.proxy)} created')
#         self.proxy.moveToThread(mainThread)
#         console.debug(f'PyProxy object id:{id(self.proxy)} moved to main thread id:{id(self.proxy.thread())}')
#         self.createdAndMovedToMainThread.emit()


# class TranslationsHandler(QObject):

#     def __init__(self, engine, parent=None):
#         from EasyApp.Logic.Translate import Translator

#         super().__init__(parent)
#         self.translator = Translator(QApplication.instance(),
#                                      engine,
#                                      self.translationsPath(),
#                                      self.languages())

#     def translationsPath(self):  # NEED FIX: read from pyproject.toml
#         translationsPath = 'Gui/Resources/Translations'
#         translationsPath = os.path.join(*translationsPath.split('/'))
#         console.debug(f'Translations path: {translationsPath}')
#         return translationsPath

#     def languages(self):  # NEED FIX: read from pyproject.toml
#         languages = [ { 'code': 'en', 'name': 'English' },
#                       { 'code': 'fr', 'name': 'Française' },
#                       { 'code': 'de', 'name': 'Deutsch' },
#                       { 'code': 'es', 'name': 'Español' },
#                       { 'code': 'it', 'name': 'Italiano' },
#                       { 'code': 'da', 'name': 'Dansk' },
#                       { 'code': 'sv', 'name': 'Svenska' },
#                       { 'code': 'pl', 'name': 'Polski' },
#                       { 'code': 'ru', 'name': 'Русский' } ]
#         console.debug(f'Languages: {[lang["code"] for lang in languages]}')
#         return languages
