import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Plot")
        //enabled: true
        //collapsible: false
        last: true

        // EaElements.CheckBox {
        //     topPadding: 0
        //     text: qsTr("Show legend")
        //     checked: ExGlobals.Variables.showLegend
        //     onCheckedChanged: ExGlobals.Variables.showLegend = checked
        // }

        EaElements.CheckBox {
            topPadding: 0
            id: rq4
            checked: ExGlobals.Constants.proxy.simulation.plotRQ4
            text: qsTr("Show R(q)q⁴")
            onToggled: ExGlobals.Constants.proxy.simulation.setPlotRQ4()
        }
    }

}
