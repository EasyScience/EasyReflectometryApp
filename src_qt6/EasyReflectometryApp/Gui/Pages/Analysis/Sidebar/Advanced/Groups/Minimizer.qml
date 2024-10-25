// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Minimization method")
    icon: 'level-down-alt'

    EaElements.GroupRow{
//        property real columnWidth: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 4

//        Row{
            EaElements.ComboBox {
                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 4
                topInset: minimizerLabel.height
                topPadding: topInset + padding
                model: Globals.BackendWrapper.analysisMinimizersAvailable
                //model: ['Lmfit']
                EaElements.Label {
                    id: minimizerLabel
                    text: qsTr("Minimizer")
                    color: EaStyle.Colors.themeForegroundMinor
                }
            }
//        }
/*        Row{
        //    spacing: EaStyle.Sizes.fontPixelSize

            EaElements.TextField {
                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 4
                topInset: methodLabel.height
                topPadding: topInset + padding
                horizontalAlignment: TextInput.AlignLeft
                onAccepted: focus = false
                //text: Globals.Proxies.main.fitting.minimizerMethod
                //onTextEdited: Globals.Proxies.main.fitting.minimizerMethod = text
                text: Globals.BackendWrapper.analysisMinimizerCurrent
                onTextEdited: Globals.BackendWrapper.analysisSetMinimizer(text)
                EaElements.Label {
                    id: methodLabel
                    text: qsTr("Method")
                    color: EaStyle.Colors.themeForegroundMinor
                }
            }
        }*/
        EaElements.TextField {
            width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 4
            topInset: toleranceLabel.height
            topPadding: topInset + padding
            horizontalAlignment: TextInput.AlignLeft
            onAccepted: focus = false
            //text: Globals.Proxies.main.fitting.minimizerTol
            //onTextEdited: Globals.Proxies.main.fitting.minimizerTol = text
            text: Globals.BackendWrapper.analysisMinimizerTolerance.toFixed(3)
            onTextEdited: Globals.BackendWrapper.analysisMinimizerSetTolerance(text)
            EaElements.Label {
                id: toleranceLabel
                text: qsTr("Tolerance")
                color: EaStyle.Colors.themeForegroundMinor
            }
        }

        EaElements.TextField {
            width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 4
            topInset: maxIterLabel.height
            topPadding: topInset + padding
            horizontalAlignment: TextInput.AlignLeft
            onAccepted: focus = false
            //text: Globals.Proxies.main.fitting.minimizerMaxIter
            //onTextEdited: Globals.Proxies.main.fitting.minimizerMaxIter = text
            text: Globals.BackendWrapper.analysisMinimizerMaxIterations
            onTextEdited: Globals.Proxies.main.fittingMinimizerMaxIterations(text)
            EaElements.Label {
                id: maxIterLabel
                text: qsTr("Max iterations")
                color: EaStyle.Colors.themeForegroundMinor
            }
        }
    }
}
