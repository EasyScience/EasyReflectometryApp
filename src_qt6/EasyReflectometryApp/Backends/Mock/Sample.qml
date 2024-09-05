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
    readonly property var materialNames: materials.map(function (item) { return item.label })

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
            'label': 'label 1',
            'color': 'red',
        },
        {
            'label': 'label 2',
            'color': 'green'
        },
        {
            'label': 'label 3',
            'color': 'blue'
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
            'label': 'label 1',
            'type': 'Multi-layer'
        },
        {
            'label': 'label 2',
            'type': 'Multi-layer'

        },
        {
            'label': 'label 3',
            'type': 'Multi-layer'
        },
    ]

    function setCurrentAssemblyName(value) {
        console.debug(`setCurrentAssemblyName ${value}`)
    }

    function setCurrentAssemblyType(value) {
        console.debug(`setCurrentAssemblyType ${value}`)
    }

    function removeAssembly(value) {
        console.debug(`removeAssembly ${value}`)
    }

    function addNewAssembly() {
        console.debug(`addNewAssembly`)
    }

    function duplicateSelectedAssembly() {
        console.debug(`duplicateSelectedAssembly ${currentAssemblyIndex}`)
    }

    function moveSelectedAssemblyUp() {
        console.debug(`moveSelectedAssemblyUp ${currentAssemblyIndex}`)
    }

    function moveSelectedAssemblyDown() {
        console.debug(`moveSelectedAssemblyDown ${currentAssemblyIndex}`)
    }

    function setCurrentAssemblyIndex(value) {
        console.debug(`setCurrentAssemblyIndex ${value}`)
    }

    // LAYERS
    property int currentLayerIndex: -1
    property string currentLayerName: 'currentLayerName'

    readonly property var layers: [
        {
            'formula': 'formula 1',
            'material': 'label 1',
            'thickness': '1',
            'thickness_enabled': 'True',
            'roughness': '1',
            'roughness_enabled': 'True',
            'solvation': '1',
            'apm': '1',
            'apm_enabled': 'True',
        },
        {
            'formula': 'formula 2',
            'material': 'label 2',
            'thickness': ' 2',
            'thickness_enabled': 'False',
            'roughness': '2',
            'roughness_enabled': 'False',
            'solvation': '2',
            'apm': '2',
            'apm_enabled': 'False',
        },
        {
            'formula': 'formula 3',
            'material': 'label 3',
            'thickness': '3',
            'thickness_enabled': 'False',
            'roughness': '3',
            'roughness_enabled': 'False',
            'solvation': '3',
            'apm': '3',
            'apm_enabled': 'False',
        },
    ]

    function setCurrentLayerMaterialIndex(value) {
        console.debug(`setCurrentLayerMaterialIndex ${value}`)
    }
}
