import json
from struct import Struct
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property

from easyCore import np
from easyCore.Utils.UndoRedo import property_stack_deco


class CalculatorLogic(QObject):

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        

class CalculatorProxy(QObject):
    
    dummySignal = Signal()
    calculatorChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_model

        self.calculatorChanged.connect(self._onCurrentCalculatorChanged)

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=dummySignal)
    def calculatorNames(self):
        return self.logic._interface.available_interfaces

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
        self.parent.fitter.initialize(self.parent._model_proxy._model, self.logic._interface.fit_func)
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
    