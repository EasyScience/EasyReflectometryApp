import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents
import easyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Q range of interest")
    visible: Globals.BackendWrapper.experimentExperimentalData
    Row {
        spacing: EaStyle.Sizes.fontPixelSize * 0.5

        EaComponents.TableViewLabel{
            text: qsTr("q-min:")
            horizontalAlignment: Text.AlignRight
            width: labelWidth()
        }
        EaElements.Parameter {
            enabled: Globals.BackendWrapper.experimentExperimentalData
            width: textFieldWidth()
            units: "Å<sup>-1</sup>"
            text: Globals.BackendWrapper.experimentQMin.toFixed(3)
            onEditingFinished: Globals.BackendWrapper.experimentSetQMin(text)
        }

        EaComponents.TableViewLabel{
            text: qsTr("q-max:")
            horizontalAlignment: Text.AlignRight
            width: labelWidth()
        }
        EaElements.Parameter {
            enabled: Globals.BackendWrapper.experimentExperimentalData
            width: textFieldWidth()
            units: "Å<sup>-1</sup>"
            text: Globals.BackendWrapper.experimentQMax.toFixed(3)
            onEditingFinished: Globals.BackendWrapper.experimentSetQMax(text)
        }

        EaComponents.TableViewLabel{
            text: qsTr("q-res:")
            horizontalAlignment: Text.AlignRight
            width: labelWidth()
        }
        EaElements.Parameter {
            enabled: Globals.BackendWrapper.experimentExperimentalData
            width: textFieldWidth()
            text: Globals.BackendWrapper.experimentQResolution
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

