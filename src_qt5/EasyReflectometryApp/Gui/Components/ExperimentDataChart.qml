import QtQuick 2.13

import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Components 1.0 as ExComponents
import Gui.Globals 1.0 as ExGlobals

ExComponents.BaseBokeh {
    measuredData: ExGlobals.Constants.proxy.plotting1d.measuredDataObj
    backgroundData: ExGlobals.Constants.proxy.plotting1d.backgroundDataObj
    scaleData: ExGlobals.Constants.proxy.plotting1d.scaleDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.experimentPlotRangesObj
    sldPlotRanges: ExGlobals.Constants.proxy.plotting1d.sldPlotRangesObj

    xMainAxisTitle: "q (Å⁻¹)"
    yMainAxisTitle: ExGlobals.Constants.proxy.simulation.yMainAxisTitle

    measuredLineColor: ExGlobals.Constants.proxy.data.experimentColor
    measuredAreaColor: ExGlobals.Constants.proxy.data.experimentColor
}

