pragma Singleton

import QtQuick

QtObject {

    readonly property bool isFitFinished: true
    readonly property var minimizersAvailable: ['minimizer_1', 'minimizer_2', 'minimizer_3']
    readonly property var calculatorsAvailable: ['calculator_1', 'calculator_2', 'calculator_3']
    readonly property var experimentsAvailable: ['experiment_1', 'experiment_2', 'experiment_3']

    readonly property int experimentsCurrentIndex: 0
    readonly property string minimizerStatus: undefined  //'Success'

    readonly property string minimizerCurrent: 'minimizer_1'
    readonly property double minimizerTolerance: 1.0
    readonly property int minimizerMaxIterations: 2

    // Setters
    function setCalculatorCurrentIndex(value) {
        console.debug(`setCalculatorCurrentIndex ${value}`)
    }
    function setExperimentCurrentIndex(value) {
        console.debug(`setExperimentCurrentIndex ${value}`)
    }
    function setMinimizerCurrentIndex(value) {
        console.debug(`setMinimizer ${value}`)
    }

    function setMinimizerTolerance(value) {
        console.debug(`setMinimizerTolerance ${value}`)
    }
    function setMinimizerMaxIterations(value) {
        console.debug(`setMinimizerMaxIterations ${value}`)
    }
}
