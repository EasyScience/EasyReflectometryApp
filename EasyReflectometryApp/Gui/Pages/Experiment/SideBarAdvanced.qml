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
            checked: ExGlobals.Constants.proxy.plotting1d.xAxisType
            text: qsTr("Logarithmic q-axis")
            ToolTip.text: qsTr("Checking this box will make the q-axis logarithmic")
            onToggled: ExGlobals.Constants.proxy.plotting1d.changeXAxisType()
        }

        EaElements.CheckBox {
            topPadding: 0
            checked: ExGlobals.Constants.proxy.simulation.plotRQ4
            text: qsTr("Show R(q)q⁴")
            onToggled: ExGlobals.Constants.proxy.simulation.setPlotRQ4()
        }

        EaElements.CheckBox {
            topPadding: 0
            checked: ExGlobals.Constants.proxy.plotting1d.scaleShown
            text: qsTr("Show scale level")
            onToggled: ExGlobals.Constants.proxy.plotting1d.flipScaleShown()
        }

        EaElements.CheckBox {
            topPadding: 0
            checked: ExGlobals.Constants.proxy.plotting1d.bkgShown
            text: qsTr("Show background level")
            onToggled: ExGlobals.Constants.proxy.plotting1d.flipBkgShown()
        }
    }

}
