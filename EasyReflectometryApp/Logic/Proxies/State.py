__author__ = 'github.com/arm61'

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import np
from easyCore.Utils.io.xml import XMLSerializer


class StateProxy(QObject):

    stateChanged = Signal(bool)
    statusInfoChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._status_model = None
        self._state_changed = False

        self.stateChanged.connect(self._onStateChanged)
        self.parent._calculator_proxy.calculatorChanged.connect(self.statusInfoChanged)
        self.parent._minimizer_proxy.currentMinimizerChanged.connect(
            self.statusInfoChanged)
        self.parent._minimizer_proxy.currentMinimizerMethodChanged.connect(
            self.statusInfoChanged)

    # # #
    # Setters and getters
    # # #

    @Property(bool, notify=stateChanged)
    def stateHasChanged(self):
        return self._state_changed

    @stateHasChanged.setter
    def stateHasChanged(self, changed: bool):
        if self._state_changed == changed:
            return
        self._state_changed = changed
        self.stateChanged.emit(changed)

    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        obj = {
            "calculation":
            self.parent._interface.current_interface_name,
            "minimization":
            f'{self.parent._fitter_proxy.eFitter.easy_f.current_engine.name} ({self.parent._minimizer_proxy._current_minimizer_method_name})'
        }
        self._status_model = obj
        return obj

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [{
            "label": "Calculation",
            "value": self.parent._interface.current_interface_name
        }, {
            "label":
            "Minimization",
            "value":
            f'{self.parent._fitter_proxy.eFitter.easy_f.current_engine.name} ({self.parent._minimizer_proxy._current_minimizer_method_name})'
        }]
        # xml = dicttoxml(model, attr_type=False)
        # xml = xml.decode()
        xml = XMLSerializer().encode({"item":model}, data_only=True)
        return xml

    # # #
    # Actions
    # # #

    def _onStateChanged(self, changed=True):
        self.stateHasChanged = changed

    # # #
    # Slots
    # # #

    @Slot()
    def resetState(self):
        self.parent._project_proxy.resetProject()
        self.parent._material_proxy.resetMaterial()
        self.parent._model_proxy.resetModel()
        self.parent._data_proxy.resetData()
        self.parent._undoredo_proxy.resetUndoRedoStack()
        self.parent._simulation_proxy.resetSimulation()
        self.parent._plotting_1d_proxy._setMeasuredDataArrays(np.empty(0), np.empty(0))
        self.parent._model_proxy.modelChanged.emit()
        self.parent.sampleChanged.emit()
        self.stateChanged.emit(False)