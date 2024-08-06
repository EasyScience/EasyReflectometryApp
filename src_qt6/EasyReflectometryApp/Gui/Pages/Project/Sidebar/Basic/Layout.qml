// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr('Get started')
        icon: 'rocket'
        collapsed: false

        Loader { source: 'Groups/GetStarted.qml' }
    }

    EaElements.GroupBox {
        title: qsTr('Examples')
        icon: 'database'

        Loader { source: 'Groups/Examples.qml' }
    }

    EaElements.GroupBox {
        title: qsTr('Recent projects')
        icon: 'archive'

        Loader { source: 'Groups/Recent.qml' }
    }

}
