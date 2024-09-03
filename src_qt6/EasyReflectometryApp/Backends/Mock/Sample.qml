pragma Singleton

import QtQuick

QtObject {

    readonly property int currentMaterialIndex: 0
    readonly property var materials: [
        {
            'label': 'label 1',
            'sld': '1.234567',
            'isld': '-1.234567'
        },
        {
            'label': 'label 2',
            'sld': '2.345678',
            'isld': '-2.345678'
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
        console.debug(`duplicateSelectedMaterial`)
    }

    function moveSelectedMaterialUp() {
        console.debug(`moveSelectedMaterialUp`)
    }

    function moveSelectedMaterialDown() {
        console.debug(`moveSelectedMaterialDown`)
    }

}