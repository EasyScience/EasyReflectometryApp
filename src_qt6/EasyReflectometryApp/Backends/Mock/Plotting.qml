pragma Singleton

import QtQuick

QtObject {

    property double sampleMinX: -1.
    property double sampleMaxX: 1.
    property double sampleMinY: -10.
    property double sampleMaxY: 10.
    property double sldMinX: -2.
    property double sldMaxX: 2.
    property double sldMinY: -20.
    property double sldMaxY: 20.
    property double experimentMinX: -2.
    property double experimentMaxX: 2.
    property double experimentMinY: -20.
    property double experimentMaxY: 20.

    function setQtChartsSerieRef(value1, value2, value3) {
        console.debug(`setQtChartsSerieRef ${value1}, ${value2}, ${value3}`)
    }

/*    function setQtChartsReflectometrySerieRef(value1, value2, value3) {
        console.debug(`setQtChartsReflectometrySerieRef ${value1}, ${value2}, ${value3}`)
    }

    function setQtChartsSldSerieRef(value1, value2, value3) {
        console.debug(`setQtChartsSldSerieRef ${value1}, ${value2}, ${value3}`)
    }

    function setQtChartsExperimentSerieRef(value1, value2, value3) {
        console.debug(`setQtChartsSldSerieRef ${value1}, ${value2}, ${value3}`)
    }*/
}
