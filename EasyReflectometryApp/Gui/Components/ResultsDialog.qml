import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    id: dialog

    property bool gotResults: typeof ExGlobals.Constants.proxy.fitter.fitResults.nvarys !== 'undefined' &&
                              ExGlobals.Constants.proxy.fitter.isFitFinished

    title: qsTr("Refinement Results")

    standardButtons: Dialog.Ok

    Component.onCompleted: setPreferencesOkButton()

    Column {
        EaElements.Label {
            text: gotResults
                  ? `Success: ${ExGlobals.Constants.proxy.fitter.fitResults.success}`
                  : `Fitting cancelled`
        }

        EaElements.Label {
            enabled: gotResults
            text: gotResults
                  ? `Num. refined parameters: ${ExGlobals.Constants.proxy.fitter.fitResults.nvarys}`
                  : ""
        }

        EaElements.Label {
            enabled: gotResults
            text: gotResults
                  ? `Goodness-of-fit: ${ExGlobals.Constants.proxy.fitter.fitResults.GOF.toFixed(2)}`
                  : ""
        }
    }

    // Logic

    function setPreferencesOkButton() {
        const buttons = dialog.footer.contentModel.children
        for (let i in buttons) {
            const button = buttons[i]
            if (button.text === 'OK') {
                ExGlobals.Variables.refinementResultsOkButton = button
                return
            }
        }
    }
}

