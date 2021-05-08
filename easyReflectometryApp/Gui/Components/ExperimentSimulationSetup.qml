import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    // Min
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ-min:")
    }
    EaElements.Parameter {
        id: xMin
        enabled: !ExGlobals.Constants.proxy.experimentLoaded
        width: textFieldWidth()
        units: "deg"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.simulationParametersAsObj.x_min, 3)
        onEditingFinished: updateParameters()
    }

    // Max
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ-max:")
    }
    EaElements.Parameter {
        id: xMax
        enabled: !ExGlobals.Constants.proxy.experimentLoaded
        width: textFieldWidth()
        units: "deg"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.simulationParametersAsObj.x_max, 3)
        onEditingFinished: updateParameters()
    }

    // Step
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("2θ-step:")
    }
    EaElements.Parameter {
        id: xStep
        enabled: !ExGlobals.Constants.proxy.experimentLoaded
        width: textFieldWidth()
        units: "deg"
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.simulationParametersAsObj.x_step, 3)
        onEditingFinished: updateParameters()
    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 5 - textFieldWidth() * 3) / 3
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 7.0
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
