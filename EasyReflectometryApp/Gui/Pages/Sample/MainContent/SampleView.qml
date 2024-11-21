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

        anchors.topMargin: EaStyle.Sizes.toolButtonHeight - EaStyle.Sizes.fontPixelSize - 1

        useOpenGL: EaGlobals.Vars.useOpenGL
        
        property double xRange: Globals.BackendWrapper.plottingSampleMaxX - Globals.BackendWrapper.plottingSampleMinX
        axisX.title: "q (Å⁻¹)"
        axisX.min: Globals.BackendWrapper.plottingSampleMinX - xRange * 0.01
        axisX.max: Globals.BackendWrapper.plottingSampleMaxX + xRange * 0.01
        axisX.minAfterReset: Globals.BackendWrapper.plottingSampleMinX - xRange * 0.01
        axisX.maxAfterReset: Globals.BackendWrapper.plottingSampleMaxX + xRange * 0.01

        property double yRange: Globals.BackendWrapper.plottingSampleMaxY - Globals.BackendWrapper.plottingSampleMinY
        axisY.title: "Log10 R(q)"
        axisY.min: Globals.BackendWrapper.plottingSampleMinY - yRange * 0.01
        axisY.max: Globals.BackendWrapper.plottingSampleMaxY + yRange * 0.01
        axisY.minAfterReset: Globals.BackendWrapper.plottingSampleMinY - yRange * 0.01
        axisY.maxAfterReset: Globals.BackendWrapper.plottingSampleMaxY + yRange * 0.01

        calcSerie.onHovered: (point, state) => showMainTooltip(chartView, point, state)

        // Tool buttons
        Row {
            id: toolButtons

            x: chartView.plotArea.x + chartView.plotArea.width - width
            y: chartView.plotArea.y - height - EaStyle.Sizes.fontPixelSize

            spacing: 0.25 * EaStyle.Sizes.fontPixelSize

            EaElements.TabButton {
                checked: Globals.Variables.showLegendOnSamplePage
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "align-left"
                ToolTip.text: Globals.Variables.showLegendOnSamplePage ?
                                  qsTr("Hide legend") :
                                  qsTr("Show legend")
                onClicked: Globals.Variables.showLegendOnSamplePage = checked
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
            }
        }
        // Legend

        EaElements.ToolTip {
            id: dataToolTip

            arrowLength: 0
            textFormat: Text.RichText
        }

        // Data is set in python backend (plotting_1d.py)
        Component.onCompleted: {
            Globals.References.pages.sample.mainContent.sampleView = chartView
            Globals.BackendWrapper.plottingSetQtChartsSerieRef('samplePage',
                                                               'sampleSerie',
                                                               chartView.calcSerie)
            Globals.BackendWrapper.plottingRefreshSample()                                                              
        }

    }

    // Logic
    function showMainTooltip(chart, point, state) {
        if (!chartView.allowHover) {
            return
        }
        const pos = chart.mapToPosition(Qt.point(point.x, point.y))
        dataToolTip.x = pos.x
        dataToolTip.y = pos.y
        dataToolTip.text = `<p align="left">x: ${point.x.toFixed(3)}<br\>y: ${point.y.toFixed(3)}</p>`
        dataToolTip.parent = chart
        dataToolTip.visible = state
    }
}

