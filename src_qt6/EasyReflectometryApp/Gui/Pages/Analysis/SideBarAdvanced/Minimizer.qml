// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupRow {
    property real columnWidth: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 4

    EaElements.ComboBox {
        width: columnWidth
        topInset: minimizerLabel.height
        topPadding: topInset + padding
        model: ['Lmfit']
        EaElements.Label {
            id: minimizerLabel
            text: qsTr("Minimizer")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }

    EaElements.TextField {
        width: columnWidth
        topInset: methodLabel.height
        topPadding: topInset + padding
        horizontalAlignment: TextInput.AlignLeft
        onAccepted: focus = false
        text: Globals.Proxies.main.fitting.minimizerMethod
        onTextEdited: Globals.Proxies.main.fitting.minimizerMethod = text
        EaElements.Label {
            id: methodLabel
            text: qsTr("Method")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }

    EaElements.TextField {
        width: columnWidth
        topInset: toleranceLabel.height
        topPadding: topInset + padding
        horizontalAlignment: TextInput.AlignLeft
        onAccepted: focus = false
        text: Globals.Proxies.main.fitting.minimizerTol
        onTextEdited: Globals.Proxies.main.fitting.minimizerTol = text
        EaElements.Label {
            id: toleranceLabel
            text: qsTr("Tolerance")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }

    EaElements.TextField {
        width: columnWidth
        topInset: maxIterLabel.height
        topPadding: topInset + padding
        horizontalAlignment: TextInput.AlignLeft
        onAccepted: focus = false
        text: Globals.Proxies.main.fitting.minimizerMaxIter
        onTextEdited: Globals.Proxies.main.fitting.minimizerMaxIter = text
        EaElements.Label {
            id: maxIterLabel
            text: qsTr("Max iterations")
            color: EaStyle.Colors.themeForegroundMinor
        }
    }
}
