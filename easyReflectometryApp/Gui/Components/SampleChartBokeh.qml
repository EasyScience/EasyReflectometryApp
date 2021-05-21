import QtQuick 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    sldData: ExGlobals.Constants.proxy.plotting1d.bokehSldDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: {
        let title = 'R(q)calc'
        if (hasMeasuredData) title = 'R(q)meas, R(q)calc'
        return title
    }
    xSldAxisTitle: "SLD x axis title"
    ySldAxisTitle: "SLD y axis title"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}
