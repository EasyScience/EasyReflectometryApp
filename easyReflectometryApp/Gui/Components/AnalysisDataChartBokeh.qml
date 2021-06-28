import QtQuick 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    sldData: ExGlobals.Constants.proxy.plotting1d.bokehSldDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj
    sldPlotRanges: ExGlobals.Constants.proxy.plotting1d.sldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: {
        let title = 'R(q)calc'
        if (hasMeasuredData) title = 'R(q)meas, R(q)calc'
        return title
    }
    xSldAxisTitle: "z (Å)"
    ySldAxisTitle: "SLD (10⁻⁶Å⁻²)"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

