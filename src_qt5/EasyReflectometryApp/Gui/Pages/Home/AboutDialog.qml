import QtQuick 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.AboutDialog {
    visible: EaGlobals.Variables.showAppAboutDialog
    onClosed: EaGlobals.Variables.showAppAboutDialog = false

    appIconPath: ExGlobals.Constants.appLogo
    appUrl: ExGlobals.Constants.appUrl

    appPrefixName: ExGlobals.Constants.appPrefixName
    appSuffixName: ExGlobals.Constants.appSuffixName
    appVersion: ExGlobals.Constants.appVersion
    appDate: ExGlobals.Constants.appDate

    commit: ExGlobals.Constants.commit
    commitUrl: ExGlobals.Constants.commitUrl

    branch: ExGlobals.Constants.branch
    branchUrl: ExGlobals.Constants.branchUrl

    eulaUrl: ExGlobals.Constants.eulaUrl
    oslUrl: ExGlobals.Constants.oslUrl

    description: ExGlobals.Constants.description

    essIconPath: ExGlobals.Constants.essLogo
}
