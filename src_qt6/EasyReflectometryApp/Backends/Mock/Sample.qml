pragma Singleton

import QtQuick

QtObject {
    // MATERIALS
    property int currentMaterialIndex: -1

    // Getters
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

    // Setters
    function setCurrentMaterialIndex(value) {
        console.debug(`setCurrentMaterialIndex ${value}`)
    }
    function setCurrentMaterialName(value) {
        console.debug(`setCurrentMaterialName ${value}`)
    }
    function setCurrentMaterialSld(value) {
        console.debug(`setCurrentMaterialSld ${value}`)
    }
    function setCurrentMaterialISld(value) {
        console.debug(`setCurrentMaterialISld ${value}`)
    }
    function setRepeatedLayerReptitions(value) {
        console.debug(`setRepeatedLayerReptitions ${value}`)
    }

    // Table functions
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

    // Getters
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

    // Setters
    function setCurrentModelIndex(value){
        console.debug(`setCurrentModelIndex ${value}`)
    }
    function setCurrentModelName(value) {
        console.debug(`setCurrentModelName ${value}`)
    }

    // Table functions
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
    property bool constrainAPM: false
    property bool conformalRoughness: false
    property int repeatedLayerReptitions: 1

    property string currentAssemblyName: 'currentAssemblyName'
    property string currentAssemblyType: 'Surfactant Layer'


    // Getters
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
            'type': 'Repeating Multi-layer'

        },
        {
            'label': 'label 4',
            'type': 'Surfactant Layer'
        },
    ]

    // Setters
    function setCurrentAssemblyName(value) {
        console.debug(`setCurrentAssemblyName ${value}`)
    }
    function setCurrentAssemblyType(value) {
        console.debug(`setCurrentAssemblyType ${value}`)
    }
    function setCurrentAssemblyIndex(value) {
        currentAssemblyType = assemblies[value].type
        console.debug(`setCurrentAssemblyIndex ${value}`)
    }

    // Table functions
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

    // LAYERS
    property int currentLayerIndex: -1

    property string currentLayerName: 'currentLayerName'

    // Getters
    readonly property var layers: [
        {
            'formula': 'formula 1',
            'material': 'label 1',
            'solvent': 'label 1',
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
            'solvent': 'label 2',
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
            'solvent': 'label 3',
            'thickness': '3',
            'thickness_enabled': 'False',
            'roughness': '3',
            'roughness_enabled': 'False',
            'solvation': '3',
            'apm': '3',
            'apm_enabled': 'False',
        },
    ]

    // Setters
    function setCurrentLayerIndex(value){
        console.debug(`setCurrentLayerIndex ${value}`)
    }
    function setCurrentLayerFormula(value) {
        console.debug(`setCurrentLayerFormula ${value}`)
    }
    function setCurrentLayerMaterial(value) {
        console.debug(`setCurrentLayerMaterialIndex ${value}`)
    }
    function setCurrentLayerSolvent(value) {
        console.debug(`setCurrentLayerSolvent ${value}`)
    }
    function setCurrentLayerThickness(value) {
        console.debug(`setCurrentLayerThickness ${value}`)
    }
    function setCurrentLayerRoughness(value) {
        console.debug(`setCurrentLayerRoughness ${value}`)
    }
    function setCurrentLayerAPM(value) {
        console.debug(`setCurrentLayerAPM ${value}`)
    }
    function setCurrentLayerSolvation(value) {
        console.debug(`setCurrentLayerSolvation ${value}`)
    }

    // Table functions
    function removeLayer(value) {
        console.debug(`removeLayer ${value}`)
    }
    function addNewLayer() {
        console.debug(`addNewLayer`)
    }
    function duplicateSelectedLayer() {
        console.debug(`duplicateSelectedLayer ${currentLayerIndex}`)
    }
    function moveSelectedLayerUp() {
        console.debug(`moveSelectedLayerUp ${currentLayerIndex}`)
    }
    function moveSelectedLayerDown() {
        console.debug(`moveSelectedLayerDown ${currentLayerIndex}`)
    }
}
