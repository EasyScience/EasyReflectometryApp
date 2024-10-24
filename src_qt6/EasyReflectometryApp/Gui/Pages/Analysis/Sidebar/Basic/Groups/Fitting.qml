// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupBox {
    //title: qsTr("Fitting")
    collapsible: false

    Column {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: Globals.Proxies.main.experiment.defined
            wide: true

            fontIcon: Globals.Proxies.main.fitting.isFittingNow ? 'stop-circle' : 'play-circle'
            text: Globals.Proxies.main.fitting.isFittingNow ? qsTr('Cancel fitting') : qsTr('Start fitting')

            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                Globals.Proxies.main.fitting.startStop()
            }

            Component.onCompleted: Globals.Refs.app.analysisPage.startFittingButton = this

            Loader { source: "../Popups/FitStatusDialog.qml" }
        }

    }
}
