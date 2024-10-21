import numpy as np
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Property

from EasyApp.Logic.Logging import console

from easyreflectometry import Project as ProjectLib
from easyreflectometry.data import DataSet1D

from .helpers import IO 


PLOT_BACKEND = 'QtCharts'

class Plotting1d(QObject):
    currentLib1dChanged = Signal()
    useAcceleration1dChanged = Signal()
    chartRefsChanged = Signal()
#    chartRangesChanged = Signal()
    sldChartRangesChanged = Signal()
    sampleChartRangesChanged = Signal()

    def __init__(self, project_lib: ProjectLib, parent=None):
        super().__init__(parent)
        self._project_lib = project_lib
        self._proxy = parent
        self._currentLib1d = 'QtCharts'
        self._useAcceleration1d = True
        self._model_index = 0
        self._chartRefs = {

            'QtCharts': {
#                'experimentPage': {
#                    'measSerie': None,  # QtCharts.QXYSeries,
#                    'bkgSerie': None,  # QtCharts.QXYSeries
#                },
                'samplePage': {
                    'sampleSerie': None,
                    'sldSerie': None,
                },
#                'analysisPage': {
#                    'measSerie': None,  # QtCharts.QXYSeries,
#                    'bkgSerie': None,  # QtCharts.QXYSeries,
#                }
            }
        }

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

    # Frontend/Backend public properties

    @Property(float, notify=sampleChartRangesChanged)
    def sampleMaxX(self):
        return self.sample_data.x.max()

    @Property(float, notify=sampleChartRangesChanged)
    def sampleMinX(self):
        return self.sample_data.x.min()
    
    @Property(float, notify=sampleChartRangesChanged)
    def sampleMaxY(self):
        return np.log10(self.sample_data.y.max())

    @Property(float, notify=sampleChartRangesChanged)
    def sampleMinY(self):
        return np.log10(self.sample_data.y.min())
    
    @Property(float, notify=sldChartRangesChanged)
    def sldMaxX(self):
        return self.sld_data.x.max()

    @Property(float, notify=sldChartRangesChanged)
    def sldMinX(self):
        return self.sld_data.x.min()
    
    @Property(float, notify=sldChartRangesChanged)
    def sldMaxY(self):
        return self.sld_data.y.max()

    @Property(float, notify=sldChartRangesChanged)
    def sldMinY(self):
        return self.sld_data.y.min()

    @Property(str, notify=currentLib1dChanged)
    def currentLib1d(self):
        return self._currentLib1d

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

    @Property('QVariant', notify=chartRefsChanged)
    def chartRefs(self):
        return self._chartRefs

    # Frontend/Backend public methods

    @Slot(int)
    def setModelIndex(self, value: int) -> None:
        self._model_index = value

    @Slot(str, str, 'QVariant')
    def setQtChartsReflectometrySerieRef(self, page:str, serie:str, ref: QObject):
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))
        self.drawCalculatedOnSampleChart()
        self.chartRefsChanged.emit()

    @Slot(str, str, 'QVariant')
    def setQtChartsSldSerieRef(self, page:str, serie:str, ref: QObject):
        self._chartRefs['QtCharts'][page][serie] = ref
        console.debug(IO.formatMsg('sub', f'{serie} on {page}: {ref}'))
        self.drawCalculatedOnSldChart()
        self.chartRefsChanged.emit()

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

    # QtCharts: Sample

    def qtchartsReplaceCalculatedOnSampleChartAndRedraw(self):
        sampleSerie = self._chartRefs['QtCharts']['samplePage']['sampleSerie']
        sampleSerie.clear()
        nr_points = 0
        for point in self.sample_data.data_points():
            sampleSerie.append(point[0], np.log10(point[1]))
            nr_points = nr_points + 1
        console.debug(IO.formatMsg('sub', 'Calc curve', f'{nr_points} points', 'on sample page', 'replaced'))

    def qtchartsReplaceCalculatedOnSldChartAndRedraw(self):
        sldSerie = self._chartRefs['QtCharts']['samplePage']['sldSerie']
        sldSerie.clear()
        nr_points = 0
        for point in self.sld_data.data_points():
            sldSerie.append(point[0], point[1])
            nr_points = nr_points + 1
        console.debug(IO.formatMsg('sub', 'Sld curve', f'{nr_points} points', 'on sample page', 'replaced'))
