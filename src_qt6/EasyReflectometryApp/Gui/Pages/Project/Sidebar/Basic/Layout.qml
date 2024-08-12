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

}
