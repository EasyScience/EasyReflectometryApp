from PySide2.QtCore import QObject, Signal, Property


class StateProxy(QObject):

    stateChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._status_model = None
        self._state_changed = False

        self.stateChanged.connect(self._onStateChanged)

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

    # # # 
    # Actions
    # # #

    def _onStateChanged(self, changed=True):
        self.stateHasChanged = changed