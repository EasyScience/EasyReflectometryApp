import json
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property, Slot

from easyCore import borg
from easyCore.Utils.UndoRedo import property_stack_deco

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.materials import Materials

COLOURMAP = cm.get_cmap('Blues', 100)
MIN_SLD = -3
MAX_SLD = 15
        

class MaterialProxy(QObject):
    
    materialsNameChanged = Signal()

    materialsAsXmlChanged = Signal()
    materialsAsObjChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

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
        self.parent._state_proxy.stateChanged.emit(True)

    # # # 
    # Slot
    # # # 

    @Slot()
    def addNewMaterials(self):
        borg.stack.enabled = False
        self._materials.append(Material.from_pars(2.074, 0.000, name=f'Material {len(self._materials)+1}', interface=self.parent._interface))
        borg.stack.enabled = True
        self.materialsNameChanged.emit()
        self.parent.sampleChanged.emit()

    @Slot()
    def duplicateSelectedMaterials(self):
        #if borg.stack.enabled:
        #    borg.stack.beginMacro('Loaded default material')
        borg.stack.enabled = False
        # This is a fix until deepcopy is worked out
        # Manual duplication instead of creating a copy
        to_dup = self._materials[self.parent.currentMaterialsIndex] 
        self._materials.append(Material.from_pars(to_dup.sld.raw_value, to_dup.isld.raw_value, name=to_dup.name))
        borg.stack.enabled = True
        self.materialsNameChanged.emit()
        self.parent.sampleChanged.emit()

    @Slot(str)
    def removeMaterials(self, i: str):
        """
        Remove a material from the materials list.

        :param i: Index of the material
        :type i: str
        """
        if len(self._materials) == 1:
            self._materials = Materials.from_pars()
        else:
            del self._materials[int(i)]
        self.materialsNameChanged.emit()
        self.parent.sampleChanged.emit()

    @Slot(str)
    def setCurrentMaterialsName(self, name):
        """
        Sets the name of the currently selected material.

        :param sld: New name
        :type sld: str
        """
        if self._materials[self.parent.currentMaterialsIndex].name == name:
            return
        self._materials[self.parent.currentMaterialsIndex].name = name
        self.parent.sampleChanged.emit()

    @Slot(str)
    def setCurrentMaterialsSld(self, sld):
        """
        Sets the SLD of the currently selected material.

        :param sld: New SLD value
        :type sld: float
        """
        if self._materials[self.parent.currentMaterialsIndex].sld == sld:
            return
        self._materials[self.parent.currentMaterialsIndex].sld = sld
        self.parent.sampleChanged.emit()
    
    @Slot(str)
    def setCurrentMaterialsISld(self, isld):
        """
        Sets the iSLD of the currently selected material.

        :param sld: New iSLD value
        :type sld: float
        """
        if self._materials[self.parent.currentMaterialsIndex].isld == isld:
            return
        self._materials[self.parent.currentMaterialsIndex].isld = isld
        self.parent.sampleChanged.emit()