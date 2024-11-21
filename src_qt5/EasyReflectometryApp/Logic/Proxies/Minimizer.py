__author__ = 'github.com/arm61'

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal
from PySide2.QtCore import Property

from easyscience.global_object.undo_redo import property_stack_deco
from easyscience.fitting import AvailableMinimizers

class MinimizerProxy(QObject):

    dummySignal = Signal()
    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._current_minimizer = AvailableMinimizers.LMFit_leastsq
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)
        self._current_minimizer_method_index = self.currentMinimizerIndex
        self._current_minimizer_method_name = self._current_minimizer.name

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return [minimizer.name for minimizer in AvailableMinimizers]

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        current_name = self.parent._fitter_proxy.eFitter.easy_f.minimizer.name
        return self.minimizerNames.index(current_name)

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex == new_index:
            return
        new_name = self.minimizerNames[new_index]
        self.parent._fitter_proxy.eFitter.easy_f.switch_minimizer(new_name)
        self.currentMinimizerChanged.emit()

    @Property(int, notify=currentMinimizerMethodChanged)
    def currentMinimizerMethodIndex(self):
        return self._current_minimizer_method_index

    @currentMinimizerMethodIndex.setter
    @property_stack_deco('Minimizer method change')
    def currentMinimizerMethodIndex(self, new_index: int):
        if self._current_minimizer_method_index == new_index:
            return
        self._current_minimizer_method_index = new_index
        self._current_minimizer_method_name = self.minimizerMethodNames[new_index]
        self.currentMinimizerMethodChanged.emit()

    # # #
    # Actions
    # # #

    def _onCurrentMinimizerChanged(self):
        idx = self.currentMinimizerIndex
        if idx != self._current_minimizer_method_index:
            # Bypass the property as it would be added to the stack.
            self._current_minimizer_method_index = idx
            self._current_minimizer_method_name = self._current_minimizer.name
            self.currentMinimizerMethodChanged.emit()