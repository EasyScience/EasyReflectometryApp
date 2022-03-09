import json
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property

from easyCore.Utils.UndoRedo import property_stack_deco

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials

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

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_material

        self._materials_as_obj = []
        self._materials_as_xml = ""
        self._materials = self._defaultMaterials()

    # # #
    # Defaults
    # # # 

    def _defaultMaterials(self) -> Materials:
        return Materials(Material.from_pars(0., 0., name='Vacuum'), Material.from_pars(6.335, 0., name='D2O'), Material.from_pars(2.074, 0., name='Si'))

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

    @Property(list, notify=materialsNameChanged)
    def materialsName(self):
        return self._materials.names

    @materialsName.setter
    @property_stack_deco
    def materialsName(self):
        self.parent.parametersChanged.emit() 

    # # # 
    # Actions
    # # # 

    def _onMaterialsChanged(self):
        for i in self.parent._model_proxy._model.structure:
            for j in i.layers:
                j.name = j.material.name + ' Layer'
        self._setMaterialsAsObj()  # 0.025 s
        self._setMaterialsAsXml()  # 0.065 s
        self.parent.stateChanged.emit(True)