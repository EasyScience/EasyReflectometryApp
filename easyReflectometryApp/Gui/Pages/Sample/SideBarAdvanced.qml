import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Analysis conditions")
        //enabled: true
        //collapsible: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.CheckBox {
                checked: false
                text: qsTr("Polarisation")
                ToolTip.text: qsTr("Checking this box will activate polarisation/magnetisation")
                onCheckedChanged: ExGlobals.Constants.proxy.usePolarisation = checked
            }

        }

    }

    EaElements.GroupBox {
        title: qsTr("Model simulation range")
        //enabled: true
        //collapsible: false

        ExComponents.SampleSimulationSetup {}
    }

    EaElements.GroupBox {
        title: qsTr("Chart")
        //enabled: true
        //collapsible: false
        last: true

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.CheckBox {
                checked: ExGlobals.Constants.proxy.plotting1d.sldXDataReversed
                text: qsTr("Reverse SLD z axis")
                //ToolTip.text: qsTr("Checking this box will activate polarisation/magnetisation")
                onCheckedChanged: ExGlobals.Constants.proxy.plotting1d.reverseSldXData()
            }

        }

    }

}
