import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.XmlListModel 2.13

// import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
// import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
// import Gui.Components 1.0 as ExComponents
// import Gui.Pages.Sample 1.0 as ExSample
import Gui.Pages.Sample.Layers 1.0 as ExLayers

EaElements.GroupBox {
    id: repeatingMultilayerGroup
    title: qsTr(ExGlobals.Constants.proxy.model.currentItemsName + " editor")
    enabled: (itemsTable.model.count > 0) ? true : false //When a layer is selected
    collapsible: false
    last: true
    Row {
        // visible: (currentItemsType == 'Repeating Multi-layer') ? true : false
        spacing: EaStyle.Sizes.fontPixelSize * 0.5

        // This integer defines how many repetitions of the layer structure should be
        // used.
        EaComponents.TableViewLabel{
            horizontalAlignment: Text.AlignRight
            width: labelWidth() * 2.1
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

    ExLayers.MultilayerTable{
        id: layersTable
    }

    ExLayers.MultilayerRow{
        id: layersRow
    }

    // Row {
    //     spacing: EaStyle.Sizes.fontPixelSize

    //     EaElements.SideBarButton {
    //         width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
    //         enabled: true
    //         fontIcon: "plus-circle"
    //         text: qsTr("Add layer")
    //         onClicked: ExGlobals.Constants.proxy.model.addNewLayers()
    //     }

    //     EaElements.SideBarButton {
    //         width: (EaStyle.Sizes.sideBarContentWidth - (2 * (EaStyle.Sizes.tableRowHeight + EaStyle.Sizes.fontPixelSize)) - EaStyle.Sizes.fontPixelSize) / 2
    //         enabled: (layersTable.model.count > 0) ? true : false //when item is selected
    //         fontIcon: "clone"
    //         text: qsTr("Duplicate layer")
    //         onClicked: ExGlobals.Constants.proxy.model.duplicateSelectedLayers()
    //     }

    //     EaElements.SideBarButton {
    //         width: EaStyle.Sizes.tableRowHeight
    //         enabled: (layersTable.model.count > 0 && layersTable.currentIndex != 0) ? true : false//When item is selected
    //         fontIcon: "arrow-up"
    //         ToolTip.text: qsTr("Move layer up")
    //         onClicked: ExGlobals.Constants.proxy.model.moveSelectedLayersUp()
    //     }

    //     EaElements.SideBarButton {
    //         width: EaStyle.Sizes.tableRowHeight
    //         enabled: (layersTable.model.count > 0 && layersTable.currentIndex + 1 != layersTable.model.count) ? true : false
    //         fontIcon: "arrow-down"
    //         ToolTip.text: qsTr("Move layer down")
    //         onClicked: ExGlobals.Constants.proxy.model.moveSelectedLayersDown()
    //     }
    // }
}