import QtQuick 2.14
import QtQuick.Controls 2.14

import easyAppGui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    visible: false

    title: qsTr("Save Changes")

    EaElements.Label {
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("The project has not been saved. Do you want to exit?")
    }

    footer: EaElements.DialogButtonBox {
        EaElements.Button {
            text: qsTr("Save and exit")
            onClicked: {
                ExGlobals.Constants.proxy.saveProject()
                Qt.quit()
            }
        }

        EaElements.Button {
            text: qsTr("Exit without saving")
            onClicked: Qt.quit()
        }
    }
}

