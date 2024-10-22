pragma Singleton

import QtQuick

QtObject {
    property double scaling: 1.
    property double background: 2.
    property double resolution: 3.

    property double q_min: 4.
    property double q_max: 5.
    property double q_step: 6.

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

    function setQMin(value) {
        console.debug(`setQMin ${value}`)
    }
    function setQMax(value) {
        console.debug(`setQMax ${value}`)
    }
    function setQStep(value) {
        console.debug(`setQStep ${value}`)
    }

    function load(path) {
        console.debug(`Loading experiment from ${path}`)
    }
}
