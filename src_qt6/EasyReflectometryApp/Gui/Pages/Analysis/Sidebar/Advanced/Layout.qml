// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import "./Groups" as Groups


EaComponents.SideBarColumn {

    Groups.ParamNames {}
/*
    EaElements.GroupBox {
        title: qsTr("Parameter names")
        icon: "paint-brush"
        collapsed: false

        Loader { source: 'SideBarAdvanced/ParamNames.qml' }
    }
*/
    Groups.Calculator {}
/*
    EaElements.GroupBox {
        title: qsTr("Calculation engine")
        icon: 'calculator'

        Loader { source: 'SideBarAdvanced/Calculator.qml' }
    }
*/
    Groups.Minimizer {}
/*
    EaElements.GroupBox {
        title: qsTr("Minimization engine")
        icon: 'level-down-alt'

        Loader { source: 'SideBarAdvanced/Minimizer.qml' }
    }
    */
}
