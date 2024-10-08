import QtQuick 2.13

import easyApp.Gui.Style 1.0 as EaStyle

import Gui.Components as Components
import Gui.Globals as Globals

Components.BaseBokeh {
    calculatedData: Globals.Constants.proxy.plotting1d.pureDataObj
    sldData: Globals.Constants.proxy.plotting1d.sampleSldDataObj

    plotRanges: Globals.Constants.proxy.plotting1d.analysisPlotRangesObj
    sldPlotRanges: Globals.Constants.proxy.plotting1d.sampleSldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: Globals.Constants.proxy.simulation.yMainAxisTitle
    xSldAxisTitle: "z (Å)"
    ySldAxisTitle: "SLD (10⁻⁶Å⁻²)"
    
    calculatedLineColor: Globals.Constants.proxy.model.modelColor
    sldLineColor: Globals.Constants.proxy.model.modelColor

    Component.onCompleted: Globals.References.plotting.graph1d = this
}

