from PySide2.QtCore import QObject, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco


class MinimizerProxy(QObject):

    dummySignal = Signal()
    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.parent._fitter_proxy.eFitter.available_methods(
        )[0]
        self.currentMinimizerChanged.connect(self._onCurrentMinimizerChanged)

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=dummySignal)
    def minimizerNames(self):
        return self.parent._fitter_proxy.eFitter.available_engines

    @Property(int, notify=currentMinimizerChanged)
    def currentMinimizerIndex(self):
        current_name = self.parent._fitter_proxy.eFitter.current_engine.name
        return self.minimizerNames.index(current_name)

    @currentMinimizerIndex.setter
    @property_stack_deco('Minimizer change')
    def currentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex == new_index:
            return
        new_name = self.minimizerNames[new_index]
        self.parent._fitter_proxy.eFitter.switch_engine(new_name)
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

    @Property('QVariant', notify=currentMinimizerChanged)
    def minimizerMethodNames(self):
        current_minimizer = self.minimizerNames[self.currentMinimizerIndex]
        tested_methods = {
            'lmfit': ['leastsq', 'powell', 'cobyla'],
            'bumps': ['newton', 'lm', 'de'],
            'DFO_LS': ['leastsq']
        }
        return tested_methods[current_minimizer]

    # # #
    # Actions
    # # #

    def _onCurrentMinimizerChanged(self):
        idx = 0
        minimizer_name = self.parent._fitter_proxy.eFitter.current_engine.name
        if minimizer_name == 'lmfit':
            idx = self.minimizerMethodNames.index('leastsq')
        elif minimizer_name == 'bumps':
            idx = self.minimizerMethodNames.index('lm')
        if -1 < idx != self._current_minimizer_method_index:
            # Bypass the property as it would be added to the stack.
            self._current_minimizer_method_index = idx
            self._current_minimizer_method_name = self.minimizerMethodNames[idx]
            self.currentMinimizerMethodChanged.emit()
