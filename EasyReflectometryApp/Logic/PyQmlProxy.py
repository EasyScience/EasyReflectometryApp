# noqa: E501
from cmath import log
import os
import sys
import pathlib
import datetime
import re
import timeit
import json
from typing import Union
from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCore import QByteArray, QBuffer, QIODevice

from easyCore import np, borg
from easyCore.Objects.Groups import BaseCollection
from easyCore.Objects.Base import BaseObj
from easyCore.Fitting.Fitting import Fitter
from easyCore.Utils.UndoRedo import property_stack_deco

from easyAppLogic.Utils.Utils import generalizePath

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers
from EasyReflectometry.sample.item import MultiLayer, RepeatingMultiLayer
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.interface import InterfaceFactory


from .Project import ProjectProxy
from .Simulation import SimulationProxy
from .Material import MaterialProxy
from .Model import ModelProxy
from .Calculator import CalculatorProxy
from .Parameter import ParameterProxy
from .Data import DataProxy
from .Minimizer import MinimizerProxy
from .UndoRedo import UndoRedoProxy
from .State import StateProxy
from .DataStore import DataSet1D, DataStore
from .Proxies.Plotting1d import Plotting1dProxy
from .Fitter import FitterProxy
from .Fitter import Fitter as ThreadedFitter


class PyQmlProxy(QObject):
    # SIGNALS
    parametersChanged = Signal()
    dummySignal = Signal()
    sampleChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
            
        self._interface = InterfaceFactory()

        ######### proxies #########
        self._project_proxy = ProjectProxy(self)
        self._data_proxy = DataProxy(self)
        self._simulation_proxy = SimulationProxy(self)
        self._material_proxy = MaterialProxy(self)
        self._model_proxy = ModelProxy(self)
        self._calculator_proxy = CalculatorProxy(self)
        self._parameter_proxy = ParameterProxy(self)
        self._fitter_proxy = FitterProxy(self)
        self._minimizer_proxy = MinimizerProxy(self)
        self._plotting_1d_proxy = Plotting1dProxy(self)
        self._state_proxy = StateProxy(self)
        self._undoredo_proxy = UndoRedoProxy(self)

        # Sample Connections
        self.sampleChanged.connect(self._material_proxy._onMaterialsChanged)
        self.sampleChanged.connect(self._model_proxy._onModelChanged)
        self.sampleChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.sampleChanged.connect(self._parameter_proxy._onParametersChanged)

        # Parameter Connections
        self.parametersChanged.connect(self._material_proxy._onMaterialsChanged)
        self.parametersChanged.connect(self._model_proxy._onModelChanged)
        self.parametersChanged.connect(self._simulation_proxy._onSimulationParametersChanged)
        self.parametersChanged.connect(self._parameter_proxy._onParametersChanged)
        self.parametersChanged.connect(self._simulation_proxy._onCalculatedDataChanged)
        self.parametersChanged.connect(self._undoredo_proxy.undoRedoChanged)

        # Screen recorder
        recorder = None
        try:
            from EasyReflectometryApp.Logic.ScreenRecorder import ScreenRecorder
            recorder = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        self._screen_recorder = recorder

    @Property('QVariant', notify=dummySignal)
    def state(self):
        return self._state_proxy
        
    @Property('QVariant', notify=dummySignal)
    def project(self):
        return self._project_proxy
        
    @Property('QVariant', notify=dummySignal)
    def simulation(self):
        return self._simulation_proxy

    @Property('QVariant', notify=dummySignal)
    def material(self):
        return self._material_proxy

    @Property('QVariant', notify=dummySignal)
    def model(self):
        return self._model_proxy

    @Property('QVariant', notify=dummySignal)
    def calculator(self):
        return self._calculator_proxy

    @Property('QVariant', notify=dummySignal)
    def parameter(self):
        return self._parameter_proxy

    @Property('QVariant', notify=dummySignal)
    def data(self):
        return self._data_proxy

    @Property('QVariant', notify=dummySignal)
    def fitter(self):
        return self._fitter_proxy

    @Property('QVariant', notify=dummySignal)
    def minimizer(self):
        return self._minimizer_proxy

    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self._plotting_1d_proxy

    @Property('QVariant', notify=dummySignal)
    def undoredo(self):
        return self._undoredo_proxy

    ####################################################################################################################
    ####################################################################################################################
    # Screen recorder
    ####################################################################################################################
    ####################################################################################################################

    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self._screen_recorder
