import QtQuick 2.14
import QtQuick.Controls 2.14

import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Instrumental parameters")
    visible: Globals.BackendWrapper.experimentExperimentalData
    collapsed: true
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaComponents.TableViewLabel{
            text: qsTr("Scaling:")
            horizontalAlignment: Text.AlignRight
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
        }
        EaElements.Parameter {
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            text: Globals.BackendWrapper.experimentScaling.toFixed(3)
            onEditingFinished: Globals.BackendWrapper.experimentSetScaling(text)
            enabled: Globals.BackendWrapper.experimentExperimentalData
        }

        EaComponents.TableViewLabel{
            text: qsTr("Background:")
            horizontalAlignment: Text.AlignRight
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
        }
        EaElements.Parameter {
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            text: Globals.BackendWrapper.experimentBackground.toFixed(2)
            onEditingFinished: Globals.BackendWrapper.experimentSetBackground(text)
            enabled: Globals.BackendWrapper.experimentExperimentalData
        }

        EaComponents.TableViewLabel{
            text: qsTr("Resolution:")
            horizontalAlignment: Text.AlignRight
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
        }
        EaElements.Parameter {
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            units: "%"
            text: Globals.BackendWrapper.experimentResolution
            enabled: Globals.BackendWrapper.experimentExperimentalData && Globals.BackendWrapper.experimentResolution !== "-"
            onEditingFinished: Globals.BackendWrapper.experimentSetResolution(text)
        }
    }
}
