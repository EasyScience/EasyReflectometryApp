import QtQuick 2.13
import QtQuick.Controls 2.13
import QtWebEngine 1.10

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Logic 1.0 as EaLogic
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Components 1.0 as ExComponents
import Gui.Logic 1.0 as ExLogic

ExComponents.BasePlot {
    id: plot

    property var chartData: {
        'measured': plot.measuredData,
        'calculated': plot.calculatedData,
        'ranges': plot.plotRanges,
        'sld': plot.sldData,
        'sldRanges': plot.sldPlotRanges,
        'background': plot.backgroundData,

        'hasMeasured': plot.hasMeasuredData,
        'hasCalculated': plot.hasCalculatedData,
        'hasSld': plot.hasSldData,
        'hasPlotRanges': plot.hasPlotRanges,
        'hasSldPlotRanges': plot.hasSldPlotRangesData,
        'hasBackground': plot.hasBackgroundData,
    }

    property var chartSpecs: {
        'chartWidth': plot.chartWidth,
        'mainChartHeight': plot.mainChartHeight,
        'sldChartHeight': plot.sldChartHeight,

        'xMainAxisTitle': plot.xMainAxisTitle,
        'yMainAxisTitle': plot.yMainAxisTitle,
        'xSldAxisTitle': plot.xSldAxisTitle,
        'ySldAxisTitle': plot.ySldAxisTitle,

        'chartBackgroundColor': plot.chartBackgroundColor,
        'chartForegroundColor': plot.chartForegroundColor,
        'chartGridLineColor': plot.chartGridLineColor,
        'chartMinorGridLineColor': plot.chartMinorGridLineColor,

        'measuredLineColor': plot.measuredLineColor,
        'measuredAreaColor': plot.measuredAreaColor,
        'calculatedLineColor': plot.calculatedLineColor,
        'sldLineColor': plot.sldLineColor,
        'backgroundLineColor': plot.backgroundLineColor,

        'measuredLineWidth': plot.measuredLineWidth,
        'calculatedLineWidth': plot.calculatedLineWidth,
        'sldLineWidth': plot.sldLineWidth,
        'backgroundLineWidth': plot.backgroundLineWidth,

        'fontPixelSize': plot.fontPixelSize
    }

    property string html: ExLogic.Plotting.bokehHtml(chartData, chartSpecs)

    WebEngineView {
        id: chartView

        anchors.fill: parent
        anchors.margins: plot.paddings
        anchors.topMargin: plot.paddings - 0.25 * plot.fontPixelSize
        backgroundColor: plot.chartBackgroundColor

        onContextMenuRequested: {
            request.accepted = true
        }
    }

    /////////////////////
    // Chart tool buttons
    /////////////////////

    /*
    Row {
        anchors.top: parent.top
        anchors.right: parent.right

        anchors.topMargin: plot.fontPixelSize
        anchors.rightMargin: plot.fontPixelSize

        spacing: 3

        EaElements.TabButton {
            //checked: mainChart.allowZoom
            autoExclusive: false
            height: plot.chartToolButtonsHeight
            width: plot.chartToolButtonsHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "expand"
            ToolTip.text: qsTr("Box zoom")
            //onClicked: mainChart.allowZoom = !mainChart.allowZoom
        }

        EaElements.TabButton {
            checkable: false
            height: plot.chartToolButtonsHeight
            width: plot.chartToolButtonsHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "sync-alt"
            ToolTip.text: qsTr("Reset")
            //onClicked: mainChart.zoomReset()
            onClicked: chartView.runJavaScript("OnClick()", function(result) {
                console.log(result);
                //var button = document.querySelector(".bk-tool-icon-reset");
                //console.log("!!!!!!!!!!!!!!!!!", button)
                //if (button) {
                //  button.click();
                //}
            });
        }

        EaElements.TabButton {
            //checked: mainChart.allowHover
            autoExclusive: false
            height: plot.chartToolButtonsHeight
            width: plot.chartToolButtonsHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "comment-alt"
            ToolTip.text: qsTr("Hover")
            //onClicked: mainChart.allowHover = !mainChart.allowHover
        }
    }
    */

    onHtmlChanged: {
        //print(html)
        chartView.loadHtml(html)
    }
}
