import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    EaComponents.TableViewLabel {
        horizontalAlignment: Text.AlignRight
        width: elementWidth()
        text: qsTr("Background Type:")
    }
    EaElements.ComboBox {
        width: elementWidth()
        model: ["Uniform"]
    }

    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: elementWidth()
        text: qsTr("Value:")
    }
    EaElements.Parameter {
        id: bkg
        enabled: true
        width: elementWidth()
        anchors.verticalCenter: parent.verticalCenter
        units: ""
        text: ExGlobals.Constants.proxy.simulation.backgroundAsObj.bkg
        onEditingFinished: updateParameters()
    }

    // Logic

    function elementWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 4) / 4
    }

    function updateParameters() {
        const json = {
            "bkg": parseFloat(bkg.text),
        }
        ExGlobals.Constants.proxy.simulation.backgroundAsObj = JSON.stringify(json)
    }
}
