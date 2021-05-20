import QtQuick 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    differenceData: ExGlobals.Constants.proxy.plotting1d.bokehDifferenceDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj

    xAxisTitle: "q (Å-1)"
    yMainAxisTitle: {
        let title = 'R(q)calc'
        if (hasMeasuredData) title = 'R(q)meas, R(q)calc'
        return title
    }
    yDifferenceAxisTitle: "R(q)meas - R(q)calc"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

