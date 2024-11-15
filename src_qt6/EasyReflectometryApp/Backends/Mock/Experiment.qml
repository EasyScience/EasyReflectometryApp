pragma Singleton

import QtQuick

QtObject {
    property bool experimentalData: true
    property double scaling: 1.
    property double background: 2.
    property string resolution: '3.00'

    // Setters
    function setScaling(value) {
        console.debug(`setScaling ${value}`)
    }
    function setBackground(value) {
        console.debug(`setBackgroun ${value}`)
    }
    function setResolution(value) {
        console.debug(`setResolution ${value}`)
    }

    function load(path) {
        console.debug(`Loading experiment from ${path}`)
    }
}
