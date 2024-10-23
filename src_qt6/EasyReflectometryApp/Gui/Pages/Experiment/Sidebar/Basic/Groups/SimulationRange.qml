import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents
import easyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Simulation range")
//    visible: Globals.Constants.proxy.data.experimentSkipped

//    enabled: Globals.Constants.proxy.data.experimentSkipped

    Row {
        spacing: EaStyle.Sizes.fontPixelSize * 0.5

        // Min
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: labelWidth()
            text: qsTr("q-min:")
        }
        EaElements.Parameter {
            id: xMin
//            enabled: !ExGlobals.Constants.proxy.data.experimentLoaded
            width: textFieldWidth()
            units: "Å<sup>-1</sup>"
            text: Globals.BackendWrapper.experimentQMin.toFixed(3)
            onEditingFinished: Globals.BackendWrapper.experimentSetQMin(text)
        }

        // Max
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: labelWidth()
            text: qsTr("q-max:")
        }
        EaElements.Parameter {
            id: xMax
//            enabled: !ExGlobals.Constants.proxy.data.experimentLoaded
            width: textFieldWidth()
            units: "Å<sup>-1</sup>"
            text: Globals.BackendWrapper.experimentQMax.toFixed(3)
            onEditingFinished: Globals.BackendWrapper.experimentSetQMax(text)
        }

        // Step
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: labelWidth()
            text: qsTr("q-step:")
        }
        EaElements.Parameter {
            id: xStep
 //           enabled: !ExGlobals.Constants.proxy.data.experimentLoaded
            width: textFieldWidth()
            units: "Å<sup>-1</sup>"
            text: Globals.BackendWrapper.experimentQElements
            onEditingFinished: Globals.BackendWrapper.experimentSetQElements(text)
        }
    }
    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 5 - textFieldWidth() * 3) / 3
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 7.0
    }
}

