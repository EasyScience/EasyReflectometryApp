import QtQuick 2.13

import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseQtCharts {
    measuredData: ExGlobals.Constants.proxy.plotting1d.qtchartsMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.qtchartsCalculatedDataObj
    differenceData: ExGlobals.Constants.proxy.plotting1d.qtchartsDifferenceDataObj
    braggData: ExGlobals.Constants.proxy.plotting1d.qtchartsBraggDataObj
    backgroundData: ExGlobals.Constants.proxy.plotting1d.qtchartsBackgroundDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj

    xAxisTitle: "2θ (deg)"
    yMainAxisTitle: {
        let title = 'Icalc'
        if (hasMeasuredData) title = 'Imeas, Icalc'
        if (hasBackgroundData) title += ', Ibkg'
        return title
    }
    yDifferenceAxisTitle: "Imeas - Icalc"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}
