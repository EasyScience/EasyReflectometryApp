// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtCore

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


Column {

    property string projectLocation: Globals.BackendProxy.project.info.location +
                                     EaLogic.Utils.osPathSep() +
                                     'summary'

    spacing: EaStyle.Sizes.fontPixelSize

    // Name field + format selector
    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        // Name field
        EaElements.TextField {
            id: nameField
            width: saveButton.width - formatField.width - parent.spacing
            topInset: nameLabel.height
            topPadding: topInset + padding
            horizontalAlignment: TextInput.AlignLeft
            placeholderText: qsTr('Enter summary file name here')
            Component.onCompleted: text = 'summary'
            EaElements.Label {
                id: nameLabel
                text: qsTr('Name')
            }
        }
        // Name field

        // Format selector
        EaElements.ComboBox {
            id: formatField
            topInset: formatLabel.height
            topPadding: topInset + padding
            width: EaStyle.Sizes.fontPixelSize * 10
            textRole: 'text'
            valueRole: 'value'
            model: [
                { value: 'html', text: qsTr('HTML') }
            ]
            EaElements.Label {
                id: formatLabel
                text: qsTr('Format')
            }
        }
        // Format selector
    }
    // Name field + format selector

    // Location field
    EaElements.TextField {
        id: reportLocationField
        width: saveButton.width
        topInset: locationLabel.height
        topPadding: topInset + padding
        rightPadding: chooseButton.width
        horizontalAlignment: TextInput.AlignLeft
        placeholderText: qsTr('Enter report location here')
        Component.onCompleted: text = projectLocation

        EaElements.Label {
            id: locationLabel
            text: qsTr('Location')
        }

        EaElements.ToolButton {
            id: chooseButton
            anchors.right: parent.right
            topPadding: parent.topPadding
            showBackground: false
            fontIcon: 'folder-open'
            ToolTip.text: qsTr('Choose report parent directory')
            onClicked: reportParentDirDialog.open()
        }
    }
    // Location field

    // Save button
    EaElements.SideBarButton {
        id: saveButton
        wide: true
        fontIcon: 'download'
        text: qsTr('Save')
    }
    // Save button

}
