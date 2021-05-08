import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {


    EaElements.GroupBox {
        title: qsTr("Analysis conditions")
        enabled: true
        collapsible: false

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

    /*EaElements.GroupBox {
        title: qsTr("Bonds")
        enabled: ExGlobals.Constants.proxy.samplesPresent
        collapsed: false

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            // Show bonds
            EaElements.CheckBox {
                text: qsTr("Polarisation")
                onCheckedChanged: ExGlobals.Constants.proxy.showBonds = checked
                Component.onCompleted: checked = ExGlobals.Constants.proxy.showBonds
            }

            // Spacer
            EaElements.Label {
                width: EaStyle.Sizes.fontPixelSize * 2.5
            }

            // Min distance
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                text: qsTr("Min distance:")
            }
            EaElements.Parameter {
                enabled: false
                anchors.verticalCenter: parent.verticalCenter
                width: 75
                Component.onCompleted: text = 0
            }

            // Spacer
            EaElements.Label {
                width: EaStyle.Sizes.fontPixelSize * 3.0
            }

            // Max distance
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                text: qsTr("Max distance:")
            }
            EaElements.Parameter {
                anchors.verticalCenter: parent.verticalCenter
                width: 75
                onEditingFinished: ExGlobals.Constants.proxy.bondsMaxDistance = text
                Component.onCompleted: text = ExGlobals.Constants.proxy.bondsMaxDistance
            }

        }

    }*/
    

}
