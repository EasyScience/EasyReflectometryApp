import QtQuick

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.AboutDialog {

    visible: EaGlobals.Vars.showAppAboutDialog
    onClosed: EaGlobals.Vars.showAppAboutDialog = false

    appIconPath: Globals.ApplicationInfo.about.icon

    appPrefixName: Globals.ApplicationInfo.about.namePrefixForLogo
    appSuffixName: Globals.ApplicationInfo.about.nameSuffixForLogo
    appVersion: Globals.BackendProxy.home.versionNumber
    appDate: Globals.BackendProxy.home.versionDate

    appUrl: Globals.BackendProxy.home.homepageUrl
    eulaUrl: Globals.BackendProxy.home.licenseUrl
    oslUrl: Globals.BackendProxy.home.dependenciesUrl

    description: Globals.ApplicationInfo.about.description
    developerIcons: Globals.ApplicationInfo.about.developerIcons
    developerYearsFrom: Globals.ApplicationInfo.about.developerYearsFrom
    developerYearsTo: Globals.ApplicationInfo.about.developerYearsTo

}
