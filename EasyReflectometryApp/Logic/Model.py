import json
from struct import Struct
from dicttoxml import dicttoxml

from matplotlib import cm, colors

from PySide2.QtCore import QObject, Signal, Property

from easyCore import np
from easyCore.Utils.UndoRedo import property_stack_deco

from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.item import MultiLayer
from EasyReflectometry.sample.structure import Structure
from EasyReflectometry.experiment.model import Model


class ModelLogic(QObject):

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        

class ModelProxy(QObject):
    
    modelNameChanged = Signal()

    modelAsXmlChanged = Signal()
    modelAsObjChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_model

        self._model_as_obj = []
        self._model_as_xml = ""
        self._model = self._defaultModel(interface=parent._interface)

    # # #
    # Defaults
    # # # 

    def _defaultModel(self, interface=None) -> Model:
        layers = [
            Layer.from_pars(self.parent._material_proxy._materials[0], 0.0, 0.0, name='Vacuum Layer'),
            Layer.from_pars(self.parent._material_proxy._materials[1], 100.0, 3.0, name='D2O Layer'),
            Layer.from_pars(self.parent._material_proxy._materials[2], 0.0, 1.2, name='Si Layer'),
        ]
        items = [
            MultiLayer.from_pars(layers[0], name='Superphase'),
            MultiLayer.from_pars(layers[1], name='D2O Layer'),
            MultiLayer.from_pars(layers[2], name='Subphase')
        ]
        structure = Structure.from_pars(*items)
        model = Model.from_pars(structure, 1, 0, 0, interface=interface)
        model.structure[0].layers[0].thickness.enabled = False
        model.structure[0].layers[0].roughness.enabled = False
        model.structure[-1].layers[-1].thickness.enabled = False
        return model

    # # #
    # Setters and getters
    # # #

    @Property('QVariant', notify=modelAsObjChanged)
    def modelAsObj(self):
        return self._model_as_obj

    def _setModelAsObj(self):
        self._model_as_obj = []
        for i in self._model.structure:
            dictionary = {'name': i.name}
            dictionary['type'] =  i.type
            dictionary['layers'] = [j.as_dict(skip=['interface']) for j in i.layers]
            if 'repetitions' in dictionary.keys():
                dictionary['repetitions'] = i.repetitions.as_dict(skip=['interface'])
            self._model_as_obj.append(dictionary)
        if len(self._model.structure) > 0: 
            self._model_as_obj[0]['layers'][0]['thickness']['value'] = np.nan
            self._model_as_obj[0]['layers'][0]['roughness']['value'] = np.nan
            self._model_as_obj[-1]['layers'][-1]['thickness']['value'] = np.nan
        self.modelAsObjChanged.emit()

    @Property(str, notify=modelAsXmlChanged)
    def modelAsXml(self):
        return self._model_as_xml

    @modelAsXml.setter
    @property_stack_deco
    def modelAsXml(self):
        self.parent.parametersChanged.emit()

    def _setModelAsXml(self):
        self._model_as_xml = dicttoxml(self._model_as_obj).decode()
        self.modelAsXmlChanged.emit()

    # # # 
    # Actions
    # # # 

    def _onModelChanged(self):
        for i in self._model.structure:
            for j in i.layers:
                j.name = j.material.name + ' Layer'
        self._setModelAsObj()
        self._setModelAsXml() 
        self.parent.stateChanged.emit(True)