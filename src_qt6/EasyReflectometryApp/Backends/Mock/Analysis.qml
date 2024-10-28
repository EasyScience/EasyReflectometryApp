pragma Singleton

import QtQuick

QtObject {

    readonly property bool isFitFinished: true
    readonly property var minimizersAvailable: ['minimizer_1', 'minimizer_2', 'minimizer_3']
    readonly property int minimizerCurrentIndex: 0

    readonly property var calculatorsAvailable: ['calculator_1', 'calculator_2', 'calculator_3']
    readonly property int calculatorCurrentIndex: 1

    readonly property var experimentsAvailable: ['experiment_1', 'experiment_2', 'experiment_3']
    readonly property int experimentCurrentIndex: 2

    readonly property string minimizerStatus: undefined  //'Success'
    readonly property double minimizerTolerance: 1.0
    readonly property int minimizerMaxIterations: 2

    readonly property bool fittingRunning: false

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

    //Actions
    function fittingStartStop() {
        console.debug('fittingStartStop')
    }
}
