import QtQuick 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Components 1.0 as ExComponents
import Gui.Globals 1.0 as ExGlobals

ExComponents.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.bokehMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehCalculatedDataObj
    sldData: ExGlobals.Constants.proxy.plotting1d.bokehAnalysisSldDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj
    sldPlotRanges: ExGlobals.Constants.proxy.plotting1d.analysisSldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: ExGlobals.Constants.proxy.simulation.yMainAxisTitle
    xSldAxisTitle: "z (Å)"
    ySldAxisTitle: "SLD (10⁻⁶Å⁻²)"

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

