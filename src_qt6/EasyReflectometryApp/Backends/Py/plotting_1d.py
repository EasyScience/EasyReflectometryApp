# SPDX-FileCopyrightText: 2023 EasyDiffraction contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import numpy as np
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QImage
# from PySide6.QtGui import QBrush
#from PySide6 import QtCharts

from EasyApp.Logic.Logging import console

from easyreflectometry import Project as ProjectLib
from easyreflectometry.data import DataSet1D

#from .helpers import Converter
from .helpers import IO 
#from .helpers importWebEngine


#_LIBS_1D = ['QtCharts', 'Plotly']

PLOT_BACKEND = 'QtCharts'

class Plotting1d(QObject):
    currentLib1dChanged = Signal()
    useAcceleration1dChanged = Signal()
    chartRefsChanged = Signal()
    chartRangesChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._project_lib = project_lib
        self._proxy = parent
        self._currentLib1d = 'QtCharts'
        self._useAcceleration1d = True
        self._model_index = 0
        self._chartRanges = {}
        self._chartRefs = {
            # 'Plotly': {
            #     'experimentPage': None,
            #     'modelPage': None,
            #     'analysisPage': None
            # },
            'QtCharts': {
#                'experimentPage': {
#                    'measSerie': None,  # QtCharts.QXYSeries,
#                    'bkgSerie': None,  # QtCharts.QXYSeries
#                },
                'samplePage': {
                    'sampleSerie': None,  # QtCharts.QXYSeries,
                    'sldSerie': None,
#                    'braggSerie': None,  # QtCharts.QXYSeries
                },
#                'analysisPage': {
#                    'measSerie': None,  # QtCharts.QXYSeries,
#                    'bkgSerie': None,  # QtCharts.QXYSeries,
#                    'totalCalcSerie': None,  # QtCharts.QXYSeries,
#                    'residSerie': None,  # QtCharts.QXYSeries,
#                    'braggSeries': {}  # QtCharts.QXYSeries
#                }
            }
        }

    # Frontend/Backend public properties

    @Property(str, notify=currentLib1dChanged)
    def currentLib1d(self):
        return self._currentLib1d

    @property
    def sample_data(self) -> DataSet1D:
        try:
            sample_data = self._project_lib.sample_data_for_model_at_index()
        except IndexError:
            sample_data = DataSet1D(
                name='Sample Data empty',
                    x=np.empty(0),
                    y=np.empty(0),
            )
        return sample_data

    @property
    def sld_data(self) -> DataSet1D:
        try:
            sld_data = self._project_lib.sld_data_for_model_at_index()
        except IndexError:
            sld_data = DataSet1D(
                name='Sample Data empty',
                    x=np.empty(0),
                    y=np.empty(0),
            )
        return sld_data

    @currentLib1d.setter
    def currentLib1d(self, newValue):
        if self._currentLib1d == newValue:
            return
        self._currentLib1d = newValue
        self.currentLib1dChanged.emit()

    @Property(bool, notify=useAcceleration1dChanged)
    def useAcceleration1d(self):
        return self._useAcceleration1d

    @useAcceleration1d.setter
    def useAcceleration1d(self, newValue):
        if self._useAcceleration1d == newValue:
            return
        self._useAcceleration1d = newValue
        self.useAcceleration1dChanged.emit()

    @Property('QVariant', notify=chartRangesChanged)
    def chartRanges(self):
        return self._chartRanges

    @Property('QVariant', notify=chartRefsChanged)
    def chartRefs(self):
        return self._chartRefs

    # Frontend/Backend public methods

    @Slot(int)
    def setModelIndex(self, value: int) -> None:
        self._model_index = value

    @Slot(str, str, 'QVariant')
    def setQtChartsReflectometrySerieRef(self, page:str, serie:str, ref: QObject):
        #if self._chartRefs['QtCharts'][page][serie] == ref:
        #    return
#        if ref.objectName():  # braggSeries
#            self._chartRefs['QtCharts'][page][serie][ref.objectName()] = ref
#            console.debug(IO.formatMsg('sub', f'{serie} with name {ref.objectName()} on {page}: {ref}'))
#        else:  # other series
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))
        self.drawCalculatedOnSampleChart()
        self.chartRefsChanged.emit()

    @Slot(str, str, 'QVariant')
    def setQtChartsSldSerieRef(self, page:str, serie:str, ref: QObject):
        #if self._chartRefs['QtCharts'][page][serie] == ref:
        #    return
#        if ref.objectName():  # braggSeries
#            self._chartRefs['QtCharts'][page][serie][ref.objectName()] = ref
#            console.debug(IO.formatMsg('sub', f'{serie} with name {ref.objectName()} on {page}: {ref}'))
#        else:  # other series
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))
        self.drawCalculatedOnSldChart()
        self.chartRefsChanged.emit()
    # @Slot(str, 'QVariant')
    # def setPlotlyChartRef(self, page, ref):
    #     if self._chartRefs['Plotly'][page] == ref:
    #         return
    #     self._chartRefs['Plotly'][page] = ref
    #     self.chartRefsChanged.emit()

    # @Slot(int, str, result='QBrush')
    # def verticalLine(self, size, color):
    #     width = size
    #     height = size
    #     textureImage = QImage(width, height, QImage.Format_ARGB32)
    #     # Transparent background
    #     for row in range(height):
    #         for column in range(width):
    #             textureImage.setPixelColor(column, row, Qt.transparent)
    #     # Vertical line
    #     for row in range(height):
    #         column = int(width/2)
    #         textureImage.setPixelColor(column, row, color)
    #     brush = QBrush()
    #     brush.setTextureImage(textureImage)
    #     return brush


    # Backend public methods

    def refreshSamplePage(self):
        self.drawCalculatedOnSampleChart()
        self.drawCalculatedOnSldChart()

    # Sample

    def drawCalculatedOnSampleChart(self):
        if PLOT_BACKEND == 'QtCharts':
            self.qtchartsReplaceCalculatedOnSampleChartAndRedraw()

    def drawCalculatedOnSldChart(self):
        if PLOT_BACKEND == 'QtCharts':
            self.qtchartsReplaceCalculatedOnSldChartAndRedraw()
    # Experiment

    # def drawMeasuredOnExperimentChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceMeasuredOnExperimentChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     self.plotlyReplaceXOnExperimentChart()
    #     #     self.plotlyReplaceMeasuredYOnExperimentChart()
    #     #     self.plotlyRedrawExperimentChart()

    # def drawBackgroundOnExperimentChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceBackgroundOnExperimentChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     pass

    # # Analysis

    # def drawMeasuredOnAnalysisChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceMeasuredOnAnalysisChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     self.plotlyReplaceXOnAnalysisChart()
    #     #     self.plotlyReplaceMeasuredYOnAnalysisChart()

    # def drawBackgroundOnAnalysisChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceBackgroundOnAnalysisChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     pass

    # def drawCalculatedOnAnalysisChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceTotalCalculatedOnAnalysisChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     self.plotlyReplaceTotalCalculatedYOnAnalysisChartAndRedraw()

    # def drawResidualOnAnalysisChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceResidualOnAnalysisChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     pass

    # def drawBraggOnAnalysisChart(self):
    #     lib = self._proxy.plotting.currentLib1d
    #     if lib == 'QtCharts':
    #         self.qtchartsReplaceBraggOnAnalysisChartAndRedraw()
    #     # elif lib == 'Plotly':
    #     #     pass

    # Backend private methods

    # QtCharts: Sample

    def qtchartsReplaceCalculatedOnSampleChartAndRedraw(self):
#        index = self._project_lib.samp.currentIndex
#         try:
#             sample_data = self._project_lib.sample_data_for_model_at_index()
# #            xArray = self._project_lib._xArrays[self._model_index]
# #            yCalcArray = self._project_lib._yCalcArrays[self._model_index]
#         except IndexError:
#             sample_data = DataSet1D(
#                 name='Sample Data empty',
#                     x=np.empty(0),
#                     y=np.empty(0),
#             )
        sampleSerie = self._chartRefs['QtCharts']['samplePage']['sampleSerie']
        sampleSerie.clear()
        nr_points = 0
        for point in self.sample_data.data_points():
            sampleSerie.append(point[0], np.log10(point[1]))
            nr_points = nr_points + 1
        console.debug(IO.formatMsg('sub', 'Calc curve', f'{nr_points} points', 'on sample page', 'replaced'))

    def qtchartsReplaceCalculatedOnSldChartAndRedraw(self):
#        index = self._project_lib.samp.currentIndex
#         try:
#             sample_data = self._project_lib.sld_data_for_model_at_index()
# #            xArray = self._project_lib._xArrays[self._model_index]
# #            yCalcArray = self._project_lib._yCalcArrays[self._model_index]
#         except IndexError:
#             sample_data = DataSet1D(
#                 name='Sample Data empty',
#                     x=np.empty(0),
#                     y=np.empty(0),
#             )
        sldSerie = self._chartRefs['QtCharts']['samplePage']['sldSerie']
        sldSerie.clear()
        nr_points = 0
        for point in self.sld_data.data_points():
            sldSerie.append(point[0], point[1])
            nr_points = nr_points + 1
        console.debug(IO.formatMsg('sub', 'Sld curve', f'{nr_points} points', 'on sample page', 'replaced'))

    # # QtCharts: Experiment

    # def qtchartsReplaceMeasuredOnExperimentChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xArray = self._proxy.experiment._xArrays[index]
    #         yMeasArray = self._proxy.experiment._yMeasArrays[index]
    #     except IndexError:
    #         xArray = np.empty(0)
    #         yMeasArray = np.empty(0)
    #     measSerie = self._chartRefs['QtCharts']['experimentPage']['measSerie']
    #     measSerie.replaceNp(xArray, yMeasArray)
    #     console.debug(IO.formatMsg('sub', 'Meas curve', f'{xArray.size} points', 'on experiment page', 'replaced'))

    # def qtchartsReplaceBackgroundOnExperimentChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xArray = self._proxy.experiment._xArrays[index]
    #         yBkgArray = self._proxy.experiment._yBkgArrays[index]
    #     except IndexError:
    #         xArray = np.empty(0)
    #         yBkgArray = np.empty(0)
    #     bkgSerie = self._chartRefs['QtCharts']['experimentPage']['bkgSerie']
    #     bkgSerie.replaceNp(xArray, yBkgArray)
    #     console.debug(IO.formatMsg('sub', 'Bkg curve', f'{xArray.size} points', 'on experiment page', 'replaced'))

    # # QtCharts: Analysis

    # def qtchartsReplaceMeasuredOnAnalysisChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xArray = self._proxy.experiment._xArrays[index]
    #         yMeasArray = self._proxy.experiment._yMeasArrays[index]
    #     except IndexError:
    #         xArray = np.empty(0)
    #         yMeasArray = np.empty(0)
    #     measSerie = self._chartRefs['QtCharts']['analysisPage']['measSerie']
    #     measSerie.replaceNp(xArray, yMeasArray)
    #     console.debug(IO.formatMsg('sub', 'Meas curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    # def qtchartsReplaceBackgroundOnAnalysisChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xArray = self._proxy.experiment._xArrays[index]
    #         yBkgArray = self._proxy.experiment._yBkgArrays[index]
    #     except IndexError:
    #         xArray = np.empty(0)
    #         yBkgArray = np.empty(0)
    #     bkgSerie = self._chartRefs['QtCharts']['analysisPage']['bkgSerie']
    #     bkgSerie.replaceNp(xArray, yBkgArray)
    #     console.debug(IO.formatMsg('sub', 'Bkg curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    # def qtchartsReplaceTotalCalculatedOnAnalysisChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xArray = self._proxy.experiment._xArrays[index]
    #         yCalcTotalArray = self._proxy.experiment._yCalcTotalArrays[index]
    #     except IndexError:
    #         xArray = np.empty(0)
    #         yCalcTotalArray = np.empty(0)
    #     calcSerie = self._chartRefs['QtCharts']['analysisPage']['totalCalcSerie']
    #     calcSerie.replaceNp(xArray, yCalcTotalArray)
    #     console.debug(IO.formatMsg('sub', 'Calc (total) curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    # def qtchartsReplaceResidualOnAnalysisChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xArray = self._proxy.experiment._xArrays[index]
    #         yResidArray = self._proxy.experiment._yResidArrays[index]
    #     except IndexError:
    #         xArray = np.empty(0)
    #         yResidArray = np.empty(0)
    #     residSerie = self._chartRefs['QtCharts']['analysisPage']['residSerie']
    #     residSerie.replaceNp(xArray, yResidArray)
    #     console.debug(IO.formatMsg('sub', 'Resid curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    # def qtchartsReplaceBraggOnAnalysisChartAndRedraw(self):
    #     index = self._proxy.experiment.currentIndex
    #     try:
    #         xBraggDict = self._proxy.experiment._xBraggDicts[index]
    #         for phaseIdx, phaseName in enumerate(xBraggDict):
    #             xBraggArray = xBraggDict[phaseName]
    #             yBraggArray = np.full_like(xBraggArray, -phaseIdx * 0.5)
    #             braggSerie = self._chartRefs['QtCharts']['analysisPage']['braggSeries'][phaseName]
    #             braggSerie.replaceNp(xBraggArray, yBraggArray)
    #             console.debug(IO.formatMsg('sub', f'Bragg peaks {phaseName}', f'{xBraggArray.size} points', 'on analysis page', 'replaced'))
    #     except IndexError:
    #         pass





    # # Plotly: Experiment

    # def plotlyReplaceXOnExperimentChart(self):
    #     index = self._proxy.experiment.currentIndex
    #     xArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         xArray = self._proxy.experiment._xArrays[index]
    #     arrayStr = Converter.dictToJson(xArray)
    #     script = f'setXData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['experimentPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyReplaceMeasuredYOnExperimentChart(self):
    #     index = self._proxy.experiment.currentIndex
    #     yMeasArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         yMeasArray = self._proxy.experiment._yMeasArrays[index]
    #     arrayStr = Converter.dictToJson(yMeasArray)
    #     script = f'setMeasuredYData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['experimentPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyRedrawExperimentChart(self):
    #     chart = self._chartRefs['Plotly']['experimentPage']
    #     script = 'redrawPlot()'
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # # Plotly: Model

    # def plotlyReplaceXOnModelChart(self):
    #     index = self._proxy.experiment.currentIndex
    #     xArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         xArray = self._proxy.experiment._xArrays[index]
    #     arrayStr = Converter.dictToJson(xArray)
    #     script = f'setXData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['modelPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyReplaceCalculatedYOnModelChart(self):
    #     index = self._proxy.model.currentIndex
    #     yCalcArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         yCalcArray = self._proxy.model._yCalcArrays[index]
    #     arrayStr = Converter.dictToJson(yCalcArray)
    #     script = f'setCalculatedYData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['modelPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyRedrawModelChart(self):
    #     chart = self._chartRefs['Plotly']['modelPage']
    #     script = 'redrawPlot()'
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyReplaceCalculatedYOnModelChartAndRedraw(self):
    #     chart = self._chartRefs['Plotly']['modelPage']
    #     array = self._proxy.model.calculated[self._proxy.model.currentIndex]['yArray']
    #     arrayStr = Converter.dictToJson(array)
    #     script = f'redrawPlotWithNewCalculatedYJson({{ y:[{arrayStr}] }})'
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # # Plotly: Analysis

    # def plotlyReplaceXOnAnalysisChart(self):
    #     index = self._proxy.experiment.currentIndex
    #     xArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         xArray = self._proxy.experiment._xArrays[index]
    #     arrayStr = Converter.dictToJson(xArray)
    #     script = f'setXData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['analysisPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyReplaceMeasuredYOnAnalysisChart(self):
    #     index = self._proxy.experiment.currentIndex
    #     yMeasArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         yMeasArray = self._proxy.experiment._yMeasArrays[index]
    #     arrayStr = Converter.dictToJson(yMeasArray)
    #     script = f'setMeasuredYData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['analysisPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyReplaceTotalCalculatedYOnAnalysisChart(self):
    #     index = self._proxy.experiment.currentIndex
    #     yTotalCalcArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         yTotalCalcArray = self._proxy.analysis._yCalcTotal
    #     arrayStr = Converter.dictToJson(yTotalCalcArray)
    #     script = f'setCalculatedYData({arrayStr})'
    #     chart = self._chartRefs['Plotly']['analysisPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyRedrawAnalysisChart(self):
    #     chart = self._chartRefs['Plotly']['analysisPage']
    #     script = 'redrawPlot()'
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)

    # def plotlyReplaceTotalCalculatedYOnAnalysisChartAndRedraw(self):
    #     if not self._proxy.analysis.defined:
    #         return
    #     index = self._proxy.experiment.currentIndex
    #     yTotalCalcArray = np.empty(0)
    #     if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
    #         yTotalCalcArray = self._proxy.analysis._yCalcTotal
    #     arrayStr = Converter.dictToJson(yTotalCalcArray)
    #     script = f'redrawPlotWithNewCalculatedYJson({{ y:[{arrayStr}] }})'
    #     chart = self._chartRefs['Plotly']['analysisPage']
    #     WebEngine.runJavaScriptWithoutCallback(chart, script)
