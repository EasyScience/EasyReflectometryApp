import json
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco


COLOURMAP = cm.get_cmap('Blues', 100)
MIN_SLD = -3
MAX_SLD = 15


class MaterialLogic(QObject):

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        

class MaterialProxy(QObject):
    
    materialsNameChanged = Signal()

    materialsAsXmlChanged = Signal()
    materialsAsObjChanged = Signal()
    backgroundChanged = Signal()
    resolutionChanged = Signal()
    qRangeChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_material

        self._materials_as_obj = []
        self._materials_as_xml = ""
        self._materials = []

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=materialsAsObjChanged)
    def materialsAsObj(self):
        return self._materials_as_obj

    def _setMaterialsAsObj(self):
        self._materials_as_obj = []
        for i in self._materials:
            dictionary = i.as_dict(skip=['interface'])
            dictionary['color'] = colors.rgb2hex(COLOURMAP((dictionary['sld']['value'] - MIN_SLD) / (MAX_SLD - MIN_SLD)))
            self._materials_as_obj.append(dictionary)
        self.materialsAsObjChanged.emit()

    @Property(str, notify=materialsAsXmlChanged)
    def materialsAsXml(self):
        return self._materials_as_xml

    @materialsAsXml.setter
    @property_stack_deco
    def materialsAsXml(self):
        self.parent.parametersChanged.emit()

    def _setMaterialsAsXml(self):
        self._materials_as_xml = dicttoxml(self._materials_as_obj).decode()
        self.materialsAsXmlChanged.emit()