import QtQuick 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Components 1.0 as ExComponents
import Gui.Globals 1.0 as ExGlobals

ExComponents.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.measuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.calculatedDataObj
    sldData: ExGlobals.Constants.proxy.plotting1d.analysisSldDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj
    sldPlotRanges: ExGlobals.Constants.proxy.plotting1d.analysisSldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: ExGlobals.Constants.proxy.simulation.yMainAxisTitle
    xSldAxisTitle: "z (Å)"
    ySldAxisTitle: "SLD (10⁻⁶Å⁻²)"

    calculatedLineColor: ExGlobals.Constants.proxy.data.experimentColor
    sldLineColor: ExGlobals.Constants.proxy.data.experimentColor
    measuredLineColor: ExGlobals.Constants.proxy.data.experimentColor
    measuredAreaColor: ExGlobals.Constants.proxy.data.experimentColor

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

