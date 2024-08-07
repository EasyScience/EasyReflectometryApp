// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


EaComponents.TableView {

    id: tableView

    showHeader: false
    tallRows: true
    maxRowCountShow: 6

    defaultInfoText: qsTr('No examples available')

    model: Globals.BackendProxy.project.examples

    // header
    header: EaComponents.TableViewHeader {
        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
        }

        EaComponents.TableViewLabel {
            flexibleWidth: true
            horizontalAlignment: Text.AlignLeft
            text: qsTr('name / description')
        }
    }
    // header

    // delegate
    delegate: EaComponents.TableViewDelegate {
        mouseArea.onPressed: {
            const filePath = tableView.model[index].path
            console.debug(`Loading example: ${filePath}`)
        }

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewTwoRowsAdvancedLabel {
            fontIcon: 'archive'
            text: tableView.model[index].name
            minorText: tableView.model[index].description
            ToolTip.text: tableView.model[index].description
        }
    }
    // delegate

}
