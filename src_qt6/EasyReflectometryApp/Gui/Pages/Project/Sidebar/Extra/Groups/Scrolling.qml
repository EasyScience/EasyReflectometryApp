// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import QtQuick

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements


Column {

    property int labelsCount: 50

    spacing: EaStyle.Sizes.fontPixelSize

    Repeater {
        model: labelsCount
        EaElements.Label {
            text: `Label ${index+1} of ${labelsCount}`
        }
    }

}

