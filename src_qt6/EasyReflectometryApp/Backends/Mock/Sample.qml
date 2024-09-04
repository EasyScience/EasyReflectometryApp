pragma Singleton

import QtQuick

QtObject {
    // MATERIALS
    property int currentMaterialIndex: -1
    readonly property var materials: [
        {
            'label': 'label 1',
            'sld': '1.23456',
            'isld': '-1.23456'
        },
        {
            'label': 'label 2',
            'sld': '2.34567',
            'isld': '-2.34567'
        },
        {
            'label': 'label 3',
            'sld': '3.45678',
            'isld': '-3.45678'
        },
    ]

    function setCurrentMaterialName(value) {
        console.debug(`setCurrentMaterialName ${value}`)
    }

    function setCurrentMaterialSld(value) {
        console.debug(`setCurrentMaterialSld ${value}`)
    }

    function setCurrentMaterialISld(value) {
        console.debug(`setCurrentMaterialISld ${value}`)
    }

    function removeMaterial(value) {
        console.debug(`removeMaterial ${value}`)
    }

    function addNewMaterial() {
        console.debug(`addNewMaterial`)
    }

    function duplicateSelectedMaterial() {
        console.debug(`duplicateSelectedMaterial ${currentMaterialIndex}`)
    }

    function moveSelectedMaterialUp() {
        console.debug(`moveSelectedMaterialUp ${currentMaterialIndex}`)
    }

    function moveSelectedMaterialDown() {
        console.debug(`moveSelectedMaterialDown ${currentMaterialIndex}`)
    }

    // MODELS
    property int currentModelIndex: -1
    property string currentModelName: 'currentModelName'

    readonly property var models: [
        {
            'color': 'red',
            'label': 'label 1'
        },
        {
            'color': 'green',
            'label': 'label 2'
        },
        {
            'color': 'blue',
            'label': 'label 3'
        },
    ]

    function setCurrentModelName(value) {
        console.debug(`setCurrentModelName ${value}`)
    }


    function removeModel(value) {
        console.debug(`removeModel ${value}`)
    }

    function addNewModel() {
        console.debug(`addNewModel`)
    }

    function duplicateSelectedModel() {
        console.debug(`duplicateSelectedModel ${currentModelIndex}`)
    }

    function moveSelectedModelUp() {
        console.debug(`moveSelectedModelUp ${currentModelIndex}`)
    }

    function moveSelectedModelDown() {
        console.debug(`moveSelectedModelDown ${currentModelIndex}`)
    }

    // ASSEMBLIES
    property int currentAssemblyIndex: -1
    property string currentAssemblyName: 'currentAssemblyName'

    readonly property var assemblies: [
        {
            'color': 'red',
            'label': 'label 1'
        },
        {
            'color': 'green',
            'label': 'label 2'
        },
        {
            'color': 'blue',
            'label': 'label 3'
        },
    ]
}
