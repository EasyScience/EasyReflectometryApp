import QtQuick 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Logic 1.0 as EaLogic

Rectangle {
    id: container

    property int chartToolButtonsHeight: EaStyle.Sizes.toolButtonHeight
    property int paddings: EaStyle.Sizes.fontPixelSize

    property var measuredData: ({})
    property var calculatedData: ({})
    property var sldData: ({})
    property var backgroundData: ({})
    property var scaleData: ({}) 
    property var plotRanges: ({})
    property var sldPlotRanges: ({})

    property bool hasMeasuredData: typeof measuredData !== 'undefined'
                                   && Object.keys(measuredData).length
                                   && (typeof measuredData.x !== 'undefined'
                                       || typeof measuredData.xy !== 'undefined')
    property bool hasCalculatedData: typeof calculatedData !== 'undefined'
                                     && Object.keys(calculatedData).length
    property bool hasSldData: typeof sldData !== 'undefined'
                                     && Object.keys(sldData).length
    property bool hasBackgroundData: typeof backgroundData !== 'undefined'
                                     && Object.keys(backgroundData).length
    property bool hasScaleData: typeof scaleData !== 'undefined' 
                                && Object.keys(scaleData).length
    property bool hasPlotRangesData: typeof plotRanges !== 'undefined'
                                     && Object.keys(plotRanges).length
    property bool hasSldPlotRangesData: typeof sldPlotRanges !== 'undefined'
                                     && Object.keys(sldPlotRanges).length

    property int chartContainerWidth: container.width
    property int chartContainerHeight: container.height

    property int chartWidth: container.width - 2 * paddings
    property int mainChartHeight: container.height
                                  - 2 * paddings
                                  - sldChartHeight
                                  - chartToolButtonsHeight
    property int sldChartHeight: hasSldData
                                 ? 20 * EaStyle.Sizes.fontPixelSize
                                 : 0

    property string xMainAxisTitle: ''
    property string yMainAxisTitle: ''
    property string xSldAxisTitle: ''
    property string ySldAxisTitle: ''

    property color chartBackgroundColor: EaStyle.Colors.chartPlotAreaBackground
    property color chartForegroundColor: EaStyle.Colors.chartForeground
    property color chartGridLineColor: EaStyle.Colors.chartGridLine
    property color chartMinorGridLineColor: EaStyle.Colors.chartMinorGridLine

    property color measuredLineColor: EaStyle.Colors.chartForegrounds[0]
    property color measuredAreaColor: measuredLineColor
    property color calculatedLineColor: EaStyle.Colors.chartForegrounds[1]
    property color sldLineColor: EaStyle.Colors.chartForegrounds[2]
    property color backgroundLineColor: EaStyle.Colors.chartForegrounds[3]
    property color scaleLineColor: EaStyle.Colors.chartForegrounds[3]

    property int measuredLineWidth: 1
    property int calculatedLineWidth: 2
    property int sldLineWidth: 2
    property int backgroundLineWidth: 1
    property int scaleLineWidth: 1

    property int fontPixelSize: EaStyle.Sizes.fontPixelSize

    color: chartBackgroundColor
}