import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Crystal system")
        }

        EaElements.ComboBox {
            id: crystalSystemSelector
            width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize * 2
            model: ExGlobals.Constants.proxy.crystalSystemList
            currentIndex: indexOfValue(ExGlobals.Constants.proxy.currentCrystalSystem)
            onActivated: ExGlobals.Constants.proxy.currentCrystalSystem = currentText
        }
    }

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Space group")
        }

        EaElements.ComboBox {
            width: crystalSystemSelector.width
            model: ExGlobals.Constants.proxy.formattedSpaceGroupList
            currentIndex: ExGlobals.Constants.proxy.currentSpaceGroup
            onActivated: ExGlobals.Constants.proxy.currentSpaceGroup = currentIndex
        }
    }

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Setting")
        }

        EaElements.ComboBox {
            width: crystalSystemSelector.width + EaStyle.Sizes.fontPixelSize * 4.0
            model: ExGlobals.Constants.proxy.formattedSpaceGroupSettingList
            currentIndex: ExGlobals.Constants.proxy.currentSpaceGroupSetting
            onActivated: ExGlobals.Constants.proxy.currentSpaceGroupSetting = currentIndex
        }
    }
}
