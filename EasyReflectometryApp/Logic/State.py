from dicttoxml import dicttoxml

from PySide2.QtCore import QObject, Signal, Property, Slot


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
        self.parent._minimizer_proxy.currentMinimizerChanged.connect(self.statusInfoChanged)
        self.parent._minimizer_proxy.currentMinimizerMethodChanged.connect(self.statusInfoChanged)

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
            "calculation":  self.parent._interface.current_interface_name,
            "minimization": f'{self.parent._fitter_proxy.eFitter.current_engine.name} ({self.parent._minimizer_proxy._current_minimizer_method_name})'
        }
        self._status_model = obj
        return obj

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        model = [
            {"label": "Calculation", "value": self.parent._interface.current_interface_name},
            {"label": "Minimization",
             "value": f'{self.parent._fitter_proxy.eFitter.current_engine.name} ({self.parent._minimizer_proxy._current_minimizer_method_name})'}
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
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
        pass
        # Need to be reimplemented for EasyReflectometry
        #self._project_info = self._defaultProjectInfo()
        #self.projectCreated = False
        #self.projectInfoChanged.emit()
        #self._project_proxy.project_save_filepath = ""
        #self.removeExperiment()
        #self.removePhase(self._sample.phases[self.currentPhaseIndex].name)
        #self.resetUndoRedoStack()
        #self.stateChanged.emit(False)