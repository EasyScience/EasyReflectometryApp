__author__ = 'github.com/arm61'

from PySide2.QtCore import QObject, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco


class CalculatorProxy(QObject):

    dummySignal = Signal()
    calculatorChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.calculatorChanged.connect(self._onCurrentCalculatorChanged)

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=dummySignal)
    def calculatorNames(self):
        return self.parent._interface.available_interfaces

    @Property(int, notify=calculatorChanged)
    def currentCalculatorIndex(self):
        return self.calculatorNames.index(self.parent._interface.current_interface_name)

    @currentCalculatorIndex.setter
    @property_stack_deco('Calculation engine change')
    def currentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return
        new_name = self.calculatorNames[new_index]
        self.parent._model_proxy._model.switch_interface(new_name)
        self.parent._fitting_proxy.eFitter.initialize(self.parent._model_proxy._model,
                                                      self.parent._interface.fit_func)
        self.calculatorChanged.emit()

    # # #
    # Actions
    # # #

    def _onCurrentCalculatorChanged(self):
        # print("***** _onCurrentCalculatorChanged")
        # data = self.parent._data.simulations
        # data = data[0]  # THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        # data.name = f'{self._interface.current_interface_name} engine'
        # print(data.name)
        self.parent.calculatedDataChanged.emit()
