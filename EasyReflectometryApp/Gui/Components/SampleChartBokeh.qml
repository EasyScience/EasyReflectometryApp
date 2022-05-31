import QtQuick 2.13

import easyApp.Gui.Style 1.0 as EaStyle

import Gui.Components 1.0 as ExComponents
import Gui.Globals 1.0 as ExGlobals

ExComponents.BaseBokeh {
    calculatedData: ExGlobals.Constants.proxy.plotting1d.bokehPureDataObj
    sldData: ExGlobals.Constants.proxy.plotting1d.bokehSampleSldDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj
    sldPlotRanges: ExGlobals.Constants.proxy.plotting1d.sampleSldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: ExGlobals.Constants.proxy.simulation.yMainAxisTitle
    xSldAxisTitle: "z (Å)"
    ySldAxisTitle: "SLD (10⁻⁶Å⁻²)"
    
    calculatedLineColor: ExGlobals.Constants.proxy.model.modelColor
    sldLineColor: ExGlobals.Constants.proxy.model.modelColor

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}

