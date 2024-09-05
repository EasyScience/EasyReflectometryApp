import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
import "../Assemblies" as Assemblies


EaElements.GroupColumn {
    Row {
        spacing: EaStyle.Sizes.fontPixelSize * 0.5

        // This integer defines how many repetitions of the layer structure should be
        // used.
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 2.1
            ToolTip.text: qsTr("To create some repeating multilayer structure")
            text: qsTr("Number of repetitions:")
        }
        EaElements.SpinBox {
            id: repsSpinBox
            editable: true
            from: 1
            to: 9999
            value: ExGlobals.Constants.proxy.model.currentItemsRepetitions
            onValueChanged: {
                ExGlobals.Constants.proxy.model.currentItemsRepetitions = value
            }
        }
    }
    Assemblies.MultiLayer{}
}
