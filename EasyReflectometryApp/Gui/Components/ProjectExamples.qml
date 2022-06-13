import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: tableView

    defaultInfoText: qsTr("No Examples Available")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.projectExamplesAsXml
        query: "/root/item"

        XmlRole { name: "name"; query: "name/string()" }
        XmlRole { name: "description"; query: "description/string()" }
        XmlRole { name: "path"; query: "path/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: indexColumn

            width: EaStyle.Sizes.fontPixelSize * 2.5

            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            width: tableView.width
                   - indexColumn.width
                   - descriptionColumn.width
                   - uploadColumn.width
                   - EaStyle.Sizes.tableColumnSpacing * 3
                   - EaStyle.Sizes.borderThickness

            horizontalAlignment: Text.AlignLeft

            headerText: "Name"
            text: model.name
        }

        EaComponents.TableViewLabel {
            id: descriptionColumn

            width: EaStyle.Sizes.fontPixelSize * 25

            horizontalAlignment: Text.AlignLeft

            headerText: "Description"
            text: model.description
        }

        EaComponents.TableViewButton {
            id: uploadColumn

            fontIcon: "upload"
            ToolTip.text: qsTr("Load this example")

            onClicked: {
                const fileUrl = Qt.resolvedUrl(model.path)
                ExGlobals.Constants.proxy.loadExampleProject(fileUrl)

                ExGlobals.Variables.samplePageEnabled = true
                ExGlobals.Variables.experimentPageEnabled = true
            }

            Component.onCompleted: {
                if (model.name === 'PbSO4') {
                    ExGlobals.Variables.loadExampleProjectButton = this
                }
            }
        }
    }

}
