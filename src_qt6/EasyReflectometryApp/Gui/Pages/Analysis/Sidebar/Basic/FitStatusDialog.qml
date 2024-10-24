// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.Dialog {
    id: dialog

    visible: Globals.Proxies.main.status.fitStatus
    title: qsTr("Fit status")
    standardButtons: Dialog.Ok

    Component.onCompleted: Globals.Refs.app.analysisPage.fitStatusDialogOkButton = okButtonRef()

    EaElements.Label {
        text: {
            if (Globals.Proxies.main.status.fitStatus === 'Success') {
                return 'Optimization finished successfully.'
            } else if (Globals.Proxies.main.status.fitStatus === 'Failure') {
                return 'Optimization failed.'
            } else if (Globals.Proxies.main.status.fitStatus === 'Aborted') {
                return 'Optimization aborted.'
            } else if (Globals.Proxies.main.status.fitStatus === 'No free params') {
                return 'Nothing to vary. Allow some parameters to be free.'
            } else {
                return ''
            }
        }
    }

    // Logic

    function okButtonRef() {
        const buttons = dialog.footer.contentModel.children
        for (let i in buttons) {
            const button = buttons[i]
            if (button.text === 'OK') {
                return button
            }
        }
        return null
    }
}
