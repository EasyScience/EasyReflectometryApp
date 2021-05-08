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
    //id: phasesTable

    defaultInfoText: qsTr("No Experiments Loaded")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.experimentDataAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 27.9
            headerText: "Label"
            text: model.label
            onEditingFinished: ExGlobals.Constants.proxy.setCurrentExperimentDatasetName(text)
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            //backgroundColor: model.color ? model.color : "transparent"
            backgroundColor: EaStyle.Colors.chartForegrounds[0]
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this dataset")
            onClicked: {
                ExGlobals.Constants.proxy.experimentLoaded = false
                ExGlobals.Constants.proxy.experimentSkipped = true
                ExGlobals.Constants.proxy.removeExperiment()
            }
        }

    }

}
