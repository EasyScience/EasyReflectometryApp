__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

from random import random

from PySide2.QtCore import QPointF
from PySide2.QtCharts import QtCharts


class StatusModel:
    def __init__(self, paren=None):
        super().__init__(parent)

    def updateSeries(self):
        """
        Generates new data and updates the GUI ChartView LineSeries.
        """
        if not self._lowerSeriesRefs or not self._upperSeriesRefs:
            return

        lowerSeries = self._dataObj.get_lowerXY()
        upperSeries = self._dataObj.get_upperXY()

        for seriesRef in self._lowerSeriesRefs:
            seriesRef.replace(lowerSeries)
        for seriesRef in self._upperSeriesRefs:
            seriesRef.replace(upperSeries)

    def updateData(self, dataObj):
        """
        Update ...
        """
        self._dataObj = dataObj
        self.updateSeries()

    def addLowerSeriesRef(self, seriesRef):
        """
        Sets series to be a reference to the GUI ChartView LineSeries.
        """
        self._lowerSeriesRefs.append(seriesRef)

    def addUpperSeriesRef(self, seriesRef):
        """
        Sets series to be a reference to the GUI ChartView LineSeries.
        """
        self._upperSeriesRefs.append(seriesRef)


class CalculatedDataModel:
    def __init__(self, dataObj=None):
        self._seriesRef = None
        self._dataObj = dataObj

    def updateSeries(self):
        """
        Generates new data and updates the GUI ChartView LineSeries.
        """
        if self._seriesRef is None:
            return

        series = self._dataObj.get_fit_XY()
        self._seriesRef.replace(series)

    def updateData(self, dataObj):
        """
        Update ...
        """
        self._dataObj = dataObj
        self.updateSeries()

    def setSeriesRef(self, seriesRef):
        """
        Sets series to be a reference to the GUI ChartView LineSeries.
        """
        self._seriesRef = seriesRef
