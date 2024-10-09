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


Rectangle {
    id: container

    color: EaStyle.Colors.chartBackground

    EaCharts.QtCharts1dMeasVsCalc {
        id: chartView

        // property var experimentDataBlocksNoMeas: Globals.Proxies.main.experiment.dataBlocksNoMeas
        // onExperimentDataBlocksNoMeasChanged: {
        //     if (Globals.Proxies.experimentMainParam('_diffrn_radiation', 'type').value === 'cwl') {
        //         axisX.title = '2θ (degree)'
        //     } else if (Globals.Proxies.experimentMainParam('_diffrn_radiation', 'type').value === 'tof') {
        //         axisX.title = 'TOF (µs)'
        //     } else {
        //         axisX.title = ''
        //     }
        // }

        anchors.topMargin: EaStyle.Sizes.toolButtonHeight - EaStyle.Sizes.fontPixelSize - 1

        useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d
        
        axisX.title: "X-axis"
        axisX.min: 0// Globals.Proxies.rangeValue('xMin')
        axisX.max: 10//Globals.Proxies.rangeValue('xMax')
        axisX.minAfterReset: 0//Globals.Proxies.rangeValue('xMin')
        axisX.maxAfterReset: 10//Globals.Proxies.rangeValue('xMax')
        //axisX.onRangeChanged: if (Globals.Proxies.main.project.created) saveImgTimer.restart()

        axisY.title: "Y-axis"
        axisY.min: 0//Globals.Proxies.rangeValue('yMin')
        axisY.max: 10//Globals.Proxies.rangeValue('yMax')
        axisY.minAfterReset: 0//Globals.Proxies.rangeValue('yMin')
        axisY.maxAfterReset: 10//Globals.Proxies.rangeValue('yMax')
        //axisY.onRangeChanged: if (Globals.Proxies.main.project.created) saveImgTimer.restart()

//        measSerie.pointsVisible: true

//        measSerie.onHovered: (point, state) => showMainTooltip(chartView, point, state)
//        bkgSerie.onHovered: (point, state) => showMainTooltip(chartView, point, state)

//        // Calculated curve
//        LineSeries {
//            id: calcSerie
//
//            axisX: mainChart.axisX
//            axisY: mainChart.axisY
//
//            useOpenGL: mainChart.useOpenGL
//
//            color: calcSerieColor
//            width: 2
//
//            onHovered: (point, state) => showMainTooltip(mainChart, point, state)
//        }

        // Tool buttons
        Row {
            id: toolButtons

            x: chartView.plotArea.x + chartView.plotArea.width - width
            y: chartView.plotArea.y - height - EaStyle.Sizes.fontPixelSize

            spacing: 0.25 * EaStyle.Sizes.fontPixelSize

            EaElements.TabButton {
                checked: Globals.Variables.showLegendOnExperimentPage
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "align-left"
                ToolTip.text: Globals.Variables.showLegendOnExperimentPage ?
                                  qsTr("Hide legend") :
                                  qsTr("Show legend")
                onClicked: Globals.Variables.showLegendOnExperimentPage = checked
            }

            EaElements.TabButton {
                checked: chartView.allowHover
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "comment-alt"
                ToolTip.text: qsTr("Show coordinates tooltip on hover")
                onClicked: chartView.allowHover = !chartView.allowHover
            }

            Item { height: 1; width: 0.5 * EaStyle.Sizes.fontPixelSize }  // spacer

            EaElements.TabButton {
                checked: !chartView.allowZoom
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "arrows-alt"
                ToolTip.text: qsTr("Enable pan")
                onClicked: chartView.allowZoom = !chartView.allowZoom
            }

            EaElements.TabButton {
                checked: chartView.allowZoom
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "expand"
                ToolTip.text: qsTr("Enable box zoom")
                onClicked: chartView.allowZoom = !chartView.allowZoom
            }

            EaElements.TabButton {
                checkable: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "backspace"
                ToolTip.text: qsTr("Reset axes")
                onClicked: chartView.resetAxes()
            }

        }
        // Tool buttons

        // Legend
        Rectangle {
            visible: Globals.Variables.showLegendOnExperimentPage

            x: chartView.plotArea.x + chartView.plotArea.width - width - EaStyle.Sizes.fontPixelSize
            y: chartView.plotArea.y + EaStyle.Sizes.fontPixelSize
            width: childrenRect.width
            height: childrenRect.height

            color: EaStyle.Colors.mainContentBackgroundHalfTransparent
            border.color: EaStyle.Colors.chartGridLine

            Column {
                leftPadding: EaStyle.Sizes.fontPixelSize
                rightPadding: EaStyle.Sizes.fontPixelSize
                topPadding: EaStyle.Sizes.fontPixelSize * 0.5
                bottomPadding: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    text: '━  I (sample)'
                    color: chartView.calcSerie.color
                }
//                EaElements.Label {
//                    text: '─  Ibkg (background)'
//                    color: chartView.bkgSerie.color
//                }
            }
        }
        // Legend

        // ToolTips
        EaElements.ToolTip {
            id: dataToolTip

            arrowLength: 0
            textFormat: Text.RichText
        }
        // ToolTips

        // Data is set in python backend

        Component.onCompleted: {
            Globals.References.pages.sample.mainContent.modelView = chartView
            Globals.BackendWrapper.plottingSetQtChartsSerieRef('samplePage',
                                                                'calcSerie',
                                                                 chartView.calcSerie)
//            Globals.BackendWrapper.plotting.setQtChartsSerieRef('samplePage',
//#                                                              'bkgSerie',
//                                                              chartView.bkgSerie)
        }

    }

    Timer {
        id: saveImgTimer

        interval: 5000
        onTriggered: saveImg()
    }

    // Logic

    function showMainTooltip(chart, point, state) {
        if (!chartView.allowHover) {
            return
        }
        const pos = chart.mapToPosition(Qt.point(point.x, point.y))
        dataToolTip.x = pos.x
        dataToolTip.y = pos.y
        dataToolTip.text = `<p align="left">x: ${point.x.toFixed(2)}<br\>y: ${point.y.toFixed(2)}</p>`
        dataToolTip.parent = chart
        dataToolTip.visible = state
    }

    // function saveImg() {
    //     if (Globals.BackendWrapper.project.location) {
    //         const experimentCurrenIndex = Globals.BackendWrapper..experiment.currentIndex
    //         const cifFileName =Globals.BackendWrapper.project.dataBlock.loops._experiment[experimentCurrenIndex].cif_file_name.value
    //         let split = cifFileName.split('.')
    //         split.pop()
    //         const baseFileName = split.join(".")
    //         const suffix = EaStyle.Colors.isDarkPalette ? '_dark' : '_light'
    //         const imgFileName = baseFileName + suffix + '.png'
    //         const path = Globals.BackendWrapper.project.location + '/' +
    //                   Globals.BackendWrapper.project.dirNames.experiments + '/' +
    //                    imgFileName
    //         container.grabToImage(function(result) {
    //             result.saveToFile(path)
    //         })
    //     }
    // }

}

