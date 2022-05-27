import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: dataTable

    defaultInfoText: qsTr("No Experiments Loaded")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.data.experimentDataAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
        XmlRole { name: "color"; query: "color/string()" }
        XmlRole { name: "model_index"; query: "model_index/number()" }
        XmlRole { name: "resolution"; query: "resolution/number()" }
        XmlRole { name: "background"; query: "background/number()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property var dataModel: model

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 7
            headerText: "Label"
            text: model.label
            onEditingFinished: ExGlobals.Constants.proxy.data.setCurrentExperimentDatasetName(text)
        }

        EaComponents.TableViewComboBox {
            id: modelAccess
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 7
            headerText: "Model"
            model: ExGlobals.Constants.proxy.model.modelList
            onActivated: {
                ExGlobals.Constants.proxy.data.setCurrentExperimentDatasetModel(currentIndex)
            }
            Component.onCompleted: {
                currentIndex = dataModel.model_index
            }
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 6
            headerText: "Resolution/%"
            text: model.resolution
            onEditingFinished: ExGlobals.Constants.proxy.data.setResolution(text)
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignHCenter
            width: EaStyle.Sizes.fontPixelSize * 6
            headerText: "Background"
            text: model.background.toExponential(3)
            onEditingFinished: ExGlobals.Constants.proxy.data.setBackground(text)
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            //backgroundColor: model.color ? model.color : "transparent"
            backgroundColor: model.color
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this dataset")
            onClicked: {
                ExGlobals.Constants.proxy.data.removeExperiment(dataTable.currentIndex)
            }
        }

    }
    onCurrentIndexChanged: {
        ExGlobals.Constants.proxy.data.currentDataIndex = dataTable.currentIndex
    }

}
