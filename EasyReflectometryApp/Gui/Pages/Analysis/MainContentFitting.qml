import QtQuick 2.13

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Loader {
    source: {
        if (ExGlobals.Constants.proxy.plotting1d.currentLib === 'qtcharts') {
            return ExLogic.Paths.component('AnalysisDataChartQtCharts.qml')
        } else if (ExGlobals.Constants.proxy.plotting1d.currentLib === 'bokeh') {
            return ExLogic.Paths.component('AnalysisDataChartBokeh.qml')
        }
    }
}
