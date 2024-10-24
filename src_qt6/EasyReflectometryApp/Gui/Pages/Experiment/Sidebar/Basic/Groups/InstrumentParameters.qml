import QtQuick 2.14
import QtQuick.Controls 2.14

//import easyApp.Gui.Globals as EaGlobals
import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents
//import easyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Instrumental parameters")
//    title: qsTr(Globals.Constants.proxy.data.currentDataName + " instrumental parameters")
//    visible: Globals.Constants.proxy.data.experimentLoaded
    collapsed: true
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            text: qsTr("Scaling:")
        }
        EaElements.Parameter {
            id: xMin
            enabled: true
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            units: ""
            text: Globals.BackendWrapper.experimentScaling.toFixed(3)
            onEditingFinished: Globals.BackendWrapper.experimentSetScaling(text)
        }

        // Max
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            text: qsTr("Background:")
        }
        EaElements.Parameter {
            id: xMax
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            units: ""
            text: Globals.BackendWrapper.experimentBackground.toFixed(2)
            onEditingFinished: Globals.BackendWrapper.experimentSetBackground(text)
        }

        // Step
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            text: qsTr("Resolution:")
        }
        EaElements.Parameter {
            id: xStep
            width: (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
            units: "%"
            text: Globals.BackendWrapper.experimentResolution
            enabled: Globals.BackendWrapper.experimentResolution !== "-"
            onEditingFinished: Globals.BackendWrapper.experimentSetResolution(text)
        }
    }
}
