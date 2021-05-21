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
        id: xMin
        enabled: !ExGlobals.Constants.proxy.experimentLoaded
        width: elementWidth()
        anchors.verticalCenter: parent.verticalCenter
        units: ""
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.simulationParametersAsObj.x_min, 3)
        onEditingFinished: updateParameters()
    }

    // Logic

    function elementWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 4) / 4
    }

    function updateParameters() {
        const json = {
            "x_min": parseFloat(xMin.text),
            "x_max": parseFloat(xMax.text),
            "x_step": parseFloat(xStep.text)
        }
        ExGlobals.Constants.proxy.simulationParametersAsObj = JSON.stringify(json)
    }
}
