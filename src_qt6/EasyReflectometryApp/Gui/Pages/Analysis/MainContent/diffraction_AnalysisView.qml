// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls
import QtCharts

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


Column {
    id: container

    property alias measSerie: measSerie
    property alias bkgSerie: bkgSerie
    property alias calcSerie: calcSerie
    property alias residSerie: residSerie

    property var phaseNames: {
        if (typeof Globals.Proxies.main.experiment.dataBlocksNoMeas[
                    Globals.Proxies.main.experiment.currentIndex].loops._pd_phase_block !== 'undefined') {
            return Globals.Proxies.main.experiment.dataBlocksNoMeas[
                Globals.Proxies.main.experiment.currentIndex].loops._pd_phase_block.map(
                phase => phase.id.value)
        } else if (typeof Globals.Proxies.main.experiment.dataBlocksNoMeas[
                       Globals.Proxies.main.experiment.currentIndex].loops._exptl_crystal !== 'undefined') {
            return Globals.Proxies.main.experiment.dataBlocksNoMeas[
                        Globals.Proxies.main.experiment.currentIndex].loops._exptl_crystal.map(
                        phase => phase.id.value)
        } else {
            //console.error('No phase names found')
            return []
        }
    }

    property string calcSerieColor: EaStyle.Colors.chartForegrounds[0]

    property int extraMargin: -12
    property real residualToMainChartHeightRatio: 0.3
    property real mainChartHeightCoeff: 1 - residualToMainChartHeightRatio

    property bool useOpenGL: Globals.Proxies.main.fitting.isFittingNow ?
                                 true :
                                 EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    Column {
        width: parent.width
        height: parent.height - 3 * EaStyle.Sizes.fontPixelSize + 2

        ///////////////////////////////////////////
        // Main chart container: Imeas, Icalc, Ibkg
        ///////////////////////////////////////////

        Item {
            width: parent.width
            height: parent.height * mainChartHeightCoeff -
                    braggChart.parent.height * 0.5

            EaCharts.QtCharts1dBase {
                id: mainChart

                property var experimentDataBlocksNoMeas: Globals.Proxies.main.experiment.dataBlocksNoMeas
                onExperimentDataBlocksNoMeasChanged: {
                    if (Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd') {
                        if (Globals.Proxies.experimentMainParam('_diffrn_radiation', 'type').value === 'cwl') {
                            axisX.title = '2θ (degree)'
                        } else if (Globals.Proxies.experimentMainParam('_diffrn_radiation', 'type').value === 'tof') {
                            axisX.title = 'TOF (µs)'
                        } else {
                            axisX.title = ''
                        }
                    } else if (Globals.Proxies.experimentMainParam('_sample', 'type').value === 'sg') {
                        axisX.title = 'sinθ/λ (Å⁻¹)'
                    } else {
                        axisX.title = ''
                    }
                }

                anchors.topMargin: EaStyle.Sizes.toolButtonHeight - EaStyle.Sizes.fontPixelSize - 1
                anchors.bottomMargin: -12 - EaStyle.Sizes.fontPixelSize

                useOpenGL: container.useOpenGL

                axisX.titleVisible: false
                axisX.labelsVisible: false
                axisX.min: Globals.Proxies.rangeValue('xMin')
                axisX.max: Globals.Proxies.rangeValue('xMax')
                axisX.minAfterReset: Globals.Proxies.rangeValue('xMin')
                axisX.maxAfterReset: Globals.Proxies.rangeValue('xMax')
                axisX.onRangeChanged: alignAllCharts()

                axisY.title: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd' ?
                                 "Imeas, Icalc, Ibkg" :
                                 "Imeas, Icalc"
                axisY.min: Globals.Proxies.rangeValue('yMin')
                axisY.max: Globals.Proxies.rangeValue('yMax')
                axisY.minAfterReset: Globals.Proxies.rangeValue('yMin')
                axisY.maxAfterReset: Globals.Proxies.rangeValue('yMax')
                axisY.onRangeChanged: adjustResidualChartRangeY()

                backgroundColor: "transparent"
                plotAreaColor: "transparent"

                // Measured points
                /*
                ScatterSeries {
                    id: measSerie

                    axisX: mainChart.axisX
                    axisY: mainChart.axisY

                    useOpenGL: mainChart.useOpenGL

                    markerSize: 5
                    borderWidth: 1
                    color: EaStyle.Colors.chartForegroundsExtra[2]
                    borderColor: this.color
                }
                */
                LineSeries {
                    id: measSerie

                    axisX: mainChart.axisX
                    axisY: mainChart.axisY

                    //useOpenGL: mainChart.useOpenGL

                    color: EaStyle.Colors.chartForegroundsExtra[2]
                    width: 2

                    //style: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd' ?
                    //           Qt.SolidLine :
                    //           Qt.NoPen
                    pointsVisible: true

                    onHovered: (point, state) => showMainTooltip(mainChart, point, state)
                }

                // Background curve
                LineSeries {
                    id: bkgSerie

                    axisX: mainChart.axisX
                    axisY: mainChart.axisY

                    //useOpenGL: mainChart.useOpenGL

                    color: EaStyle.Colors.chartForegrounds[1]
                    width: 1

                    onHovered: (point, state) => showMainTooltip(mainChart, point, state)
                }

                // Calculated curve
                LineSeries {
                    id: calcSerie

                    axisX: mainChart.axisX
                    axisY: mainChart.axisY

                    //useOpenGL: mainChart.useOpenGL

                    color: calcSerieColor
                    width: 2

                    //style: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd' ?
                    //           Qt.SolidLine :
                    //           Qt.NoPen
                    //pointsVisible: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd' ?
                    //                   false :
                    //                   true

                    onHovered: (point, state) => showMainTooltip(mainChart, point, state)
                }

                // Tool buttons
                Row {
                    id: toolButtons

                    x: mainChart.plotArea.x + mainChart.plotArea.width - width
                    y: mainChart.plotArea.y - height - EaStyle.Sizes.fontPixelSize

                    spacing: 0.25 * EaStyle.Sizes.fontPixelSize

                    EaElements.TabButton {
                        checked: Globals.Vars.showLegendOnAnalysisPage
                        autoExclusive: false
                        height: EaStyle.Sizes.toolButtonHeight
                        width: EaStyle.Sizes.toolButtonHeight
                        borderColor: EaStyle.Colors.chartAxis
                        fontIcon: "align-left"
                        ToolTip.text: Globals.Vars.showLegendOnAnalysisPage ?
                                          qsTr("Hide legend") :
                                          qsTr("Show legend")
                        onClicked: Globals.Vars.showLegendOnAnalysisPage = checked
                    }

                    EaElements.TabButton {
                        checked: mainChart.allowHover
                        autoExclusive: false
                        height: EaStyle.Sizes.toolButtonHeight
                        width: EaStyle.Sizes.toolButtonHeight
                        borderColor: EaStyle.Colors.chartAxis
                        fontIcon: "comment-alt"
                        ToolTip.text: qsTr("Show coordinates tooltip on hover")
                        onClicked: mainChart.allowHover = !mainChart.allowHover
                    }

                    Item { height: 1; width: 0.5 * EaStyle.Sizes.fontPixelSize }  // spacer

                    EaElements.TabButton {
                        checked: !mainChart.allowZoom
                        autoExclusive: false
                        height: EaStyle.Sizes.toolButtonHeight
                        width: EaStyle.Sizes.toolButtonHeight
                        borderColor: EaStyle.Colors.chartAxis
                        fontIcon: "arrows-alt"
                        ToolTip.text: qsTr("Enable pan")
                        onClicked: mainChart.allowZoom = !mainChart.allowZoom
                    }

                    EaElements.TabButton {
                        checked: mainChart.allowZoom
                        autoExclusive: false
                        height: EaStyle.Sizes.toolButtonHeight
                        width: EaStyle.Sizes.toolButtonHeight
                        borderColor: EaStyle.Colors.chartAxis
                        fontIcon: "expand"
                        ToolTip.text: qsTr("Enable box zoom")
                        onClicked: mainChart.allowZoom = !mainChart.allowZoom
                    }

                    EaElements.TabButton {
                        checkable: false
                        height: EaStyle.Sizes.toolButtonHeight
                        width: EaStyle.Sizes.toolButtonHeight
                        borderColor: EaStyle.Colors.chartAxis
                        fontIcon: "backspace"
                        ToolTip.text: qsTr("Reset axes")
                        onClicked: mainChart.resetAxes()
                    }

                }
                // Tool buttons
            }
        }

        //////////////////////////////////////
        // Bragg peaks chart container: Bragg
        //////////////////////////////////////

        Item {
            z: -1
            width: parent.width
            height: (0.5 + 1.5 * phaseNames.length) * EaStyle.Sizes.fontPixelSize


            /////onHeightChanged: console.info(`================== ${height} - ${phaseNames.length}`)
            //visible: false

            EaCharts.QtCharts1dBase {
                id: braggChart

                anchors.topMargin: -12 - EaStyle.Sizes.fontPixelSize * 1.5
                anchors.bottomMargin: -12 - EaStyle.Sizes.fontPixelSize * 1.5

                useOpenGL: container.useOpenGL

                axisX.min: mainChart.axisX.min
                axisX.max: mainChart.axisX.max
                axisX.titleVisible: false
                axisX.labelsVisible: false

                axisY.min: -0.5 * phaseNames.length
                axisY.max: 0.5
                axisY.titleVisible: false
                axisY.labelsVisible: false
                axisY.tickCount: 2

                backgroundColor: "transparent"
                plotAreaColor: "transparent"

                //onSeriesAdded: { console.error(series) }

                /*
                ScatterSeries {
                    id: braggSerie

                    axisX: braggChart.axisX
                    axisY: braggChart.axisY

                    //useOpenGL: braggChart.useOpenGL

                    brush: Globals.Proxies.main.plotting.verticalLine(
                               1.5 * EaStyle.Sizes.fontPixelSize,
                               EaStyle.Colors.chartForegroundsExtra[0])
                    borderWidth: 0.001
                    borderColor: 'transparent'

                    Component.onCompleted: console.error(this)
                }
                */
            }
        }

        //////////////////////////////////////////
        // Residual chart container: Imeas - Icalc
        //////////////////////////////////////////

        Item {
            width: parent.width
            height: parent.height * residualToMainChartHeightRatio -
                    braggChart.parent.height * 0.5

            EaCharts.QtCharts1dBase {
                id: residualChart

                anchors.topMargin: -12 - EaStyle.Sizes.fontPixelSize

                useOpenGL: container.useOpenGL

                axisX.min: mainChart.axisX.min
                axisX.max: mainChart.axisX.max
                axisX.titleVisible: false
                axisX.labelsVisible: false

                axisY.min: Globals.Proxies.main.plotting.chartRanges.yMin
                axisY.max: Globals.Proxies.main.plotting.chartRanges.yMax
                axisY.tickType: ValueAxis.TicksFixed
                axisY.tickCount: 3
                axisY.title: 'Imeas - Icalc'

                backgroundColor: "transparent"
                plotAreaColor: "transparent"

                LineSeries {
                    id: residSerie

                    axisX: residualChart.axisX
                    axisY: residualChart.axisY

                    //useOpenGL: residualChart.useOpenGL

                    color: EaStyle.Colors.chartForegrounds[2]

                    onHovered: (point, state) => showMainTooltip(residualChart, point, state)
                }
            }
        }
    }

    /////////////////////////
    // X-axis chart container
    /////////////////////////

    Item {
        z: -1
        width: parent.width
        height: container.height
        parent: container.parent

        EaCharts.QtCharts1dBase {
            id: xAxisChart

            axisX.title: mainChart.axisX.title
            axisX.min: mainChart.axisX.min
            axisX.max: mainChart.axisX.max
            axisX.lineVisible: false
            axisX.gridVisible: false

            axisY.titleVisible: false
            axisY.labelsVisible: false
            axisY.visible: false

            LineSeries {
                axisX: xAxisChart.axisX
                axisY: xAxisChart.axisY

                Component.onCompleted: initialChartsSetupTimer.start()

                Timer {
                    id: initialChartsSetupTimer
                    interval: 50
                    onTriggered: {
                        alignAllCharts()
                        adjustResidualChartRangeY()
                    }
                }
            }
        }
    }

    /////////
    // Legend
    /////////

    Rectangle {
        visible: Globals.Vars.showLegendOnAnalysisPage
        parent: container.parent

        x: mainChart.plotArea.x + mainChart.plotArea.width - width - 12 - EaStyle.Sizes.fontPixelSize
        y: mainChart.plotArea.y - 12 + EaStyle.Sizes.fontPixelSize + mainChart.anchors.topMargin + EaStyle.Sizes.fontPixelSize - 1
        width: childrenRect.width
        height: childrenRect.height

        color: EaStyle.Colors.mainContentBackgroundHalfTransparent
        border.color: EaStyle.Colors.chartGridLine

        Column {
            id: legendColumn

            leftPadding: EaStyle.Sizes.fontPixelSize
            rightPadding: EaStyle.Sizes.fontPixelSize
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            bottomPadding: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                text: '━  Measured (Imeas)'
                color: measSerie.color
            }
            EaElements.Label {
                text: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd' ?
                          '━  Total calculated (Icalc)' :
                          '━  Calculated (Icalc)'
                color: calcSerie.color
            }
            EaElements.Label {
                visible: Globals.Proxies.experimentMainParam('_sample', 'type').value === 'pd'
                text: '─  Background (Ibkg)'
                color: bkgSerie.color
            }
            EaElements.Label {
                text: '━  Residual (Imeas - Icalc)'
                color: residSerie.color
            }
            /*
            EaElements.Label {
                text: '│  Ibragg (Bragg peaks)'
                color: EaStyle.Colors.chartForegroundsExtra[0] //braggSerie.color
            }
            */
        }
    }

    ///////////
    // ToolTips
    ///////////

    EaElements.ToolTip {
        id: dataToolTip

        arrowLength: 0
        textFormat: Text.RichText
    }

    // Save references to chart series to be accessible from Python for updating data
    Component.onCompleted: {
        Globals.Refs.app.analysisPage.plotView = this
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'measSerie',
                                                          this.measSerie)
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'bkgSerie',
                                                          this.bkgSerie)
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'totalCalcSerie',
                                                          this.calcSerie)
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'residSerie',
                                                          this.residSerie)
        //Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
        //                                                  'braggSerie',
        //                                                  this.braggSerie)
        createBraggSeries()

        Globals.Proxies.main.analysis.defined = true
    }

    // Logic

    function residualChartMeanY() {
        return 0
    }

    function residualChartHalfRangeY() {
        if (mainChart.plotArea.height === 0) {
            return 0.5
        }

        const mainChartRangeY = mainChart.axisY.max - mainChart.axisY.min
        const residualToMainChartHeightRatio = residualChart.plotArea.height / mainChart.plotArea.height
        const residualChartRangeY = mainChartRangeY * residualToMainChartHeightRatio
        return 0.5 * residualChartRangeY
    }

    function adjustResidualChartRangeY() {
        residualChart.axisY.min = residualChartMeanY() - residualChartHalfRangeY()
        residualChart.axisY.max = residualChartMeanY() + residualChartHalfRangeY()
        console.debug('Residual chart Y-range has been adjusted')
    }

    function alignAllCharts() {
        xAxisChart.plotArea.width -= mainChart.plotArea.x - xAxisChart.plotArea.x
        xAxisChart.plotArea.x = mainChart.plotArea.x
        residualChart.plotArea.width = xAxisChart.plotArea.width
        residualChart.plotArea.x = mainChart.plotArea.x
        braggChart.plotArea.width = xAxisChart.plotArea.width
        braggChart.plotArea.x = mainChart.plotArea.x
        mainChart.plotArea.width = xAxisChart.plotArea.width
        console.debug('All charts have been aligned')
    }

    function showMainTooltip(chart, point, state) {
        if (!mainChart.allowHover) {
            return
        }
        const pos = chart.mapToPosition(Qt.point(point.x, point.y))
        dataToolTip.x = pos.x
        dataToolTip.y = pos.y
        dataToolTip.text = `<p align="left">x: ${point.x.toFixed(2)}<br\>y: ${point.y.toFixed(2)}</p>`
        dataToolTip.parent = chart
        dataToolTip.visible = state
    }

    function createBraggSeries() {
        for (const phaseIdx in phaseNames) {
            const phaseName = phaseNames[phaseIdx]
            const serie = braggChart.createSeries(ChartView.SeriesTypeScatter,
                                                  phaseName,
                                                  braggChart.axisX,
                                                  braggChart.axisY)
            const markerSize = //serie.useOpenGL ?
                                 //5 :  // don't work here... :(
                                 1.5 * EaStyle.Sizes.fontPixelSize
            serie.useOpenGL = braggChart.useOpenGL
            //serie.useOpenGL = Globals.Proxies.main.fitting.isFittingNow
            serie.brush = Globals.Proxies.main.plotting.verticalLine(
                       markerSize,
                       EaStyle.Colors.models[phaseIdx])
            serie.borderWidth = 0.001
            serie.borderColor = 'transparent'
            //serie.markerShape = ScatterSeries.MarkerShapeRectangle
            serie.markerSize = serie.useOpenGL ?
                        0 :
                        markerSize

            Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                              'braggSeries',
                                                              serie)

            const legendItem = Qt.createQmlObject('import EasyApp.Gui.Elements as EaElements; EaElements.Label {}', legendColumn)
            const textFont = `'${EaStyle.Fonts.fontFamily}'`
            const iconFont = `'${EaStyle.Fonts.iconsFamily}'`
            const textColor = `'${EaStyle.Colors.models[phaseIdx]}'`
            const iconColor = `'${EaStyle.Colors.models[phaseIdx]}'`
            const textHtmlStart = `<font color=${textColor} face=${textFont}>│&nbsp;&nbsp;Bragg peaks</font>`
            const iconHtml =      `<font color=${iconColor} face=${iconFont}>layer-group</font>`
            const textHtmlEnd =   `<font color=${textColor} face=${textFont}>${phaseName}</font>`
            legendItem.text = `${textHtmlStart} ${iconHtml} ${textHtmlEnd}`
            legendItem.textFormat = Text.RichText
        }
    }

}
