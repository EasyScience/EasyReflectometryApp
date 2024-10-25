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

    visible: Globals.BackendWrapper.analysisMinimizerStatus
    title: qsTr("Fit status")
    standardButtons: Dialog.Ok

    Component.onCompleted: Globals.References.pages.analysis.sidebar.basic.popups.fitStatusDialogOkButton = okButtonRef()

    EaElements.Label {
        text: {
            if ( Globals.BackendWrapper.analysisMinimizerStatus === 'Success') {
                return 'Optimization finished successfully.'
            } else if (Globals.BackendWrapper.analysisMinimizerStatus === 'Failure') {
                return 'Optimization failed.'
            } else if (Globals.BackendWrapper.analysisMinimizerStatus  === 'Aborted') {
                return 'Optimization aborted.'
            } else if (Globals.BackendWrapper.analysisMinimizerStatus  === 'No free params') {
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
