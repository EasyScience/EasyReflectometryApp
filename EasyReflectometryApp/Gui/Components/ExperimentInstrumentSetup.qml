import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    // Zero shift
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Zero shift:")
    }
    EaElements.Parameter {
        width: textFieldWidth()
        units: "deg" //ExGlobals.Constants.proxy.patternParametersAsObj.zero_shift.units
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.patternParametersAsObj.zero_shift.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.patternParametersAsObj.zero_shift["@id"], text)
    }

    // Wavelength
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Wavelength:")
    }
    EaElements.Parameter {
        width: textFieldWidth()
        units: "Å" //ExGlobals.Constants.proxy.instrumentParametersAsObj.wavelength.units
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.instrumentParametersAsObj.wavelength.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.instrumentParametersAsObj.wavelength["@id"], text)
    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 3 - textFieldWidth() * 2) / 2
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 11.0
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }
}
