// SPDX-FileCopyrightText: 2024 EasyApp contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2024 Contributors to the EasyApp project <https://github.com/easyscience/EasyApp>

import QtQuick

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.AboutDialog {

    visible: EaGlobals.Vars.showAppAboutDialog
    onClosed: EaGlobals.Vars.showAppAboutDialog = false

    appIconPath: Globals.ApplicationInfo.about.icon
    appUrl: Globals.ApplicationInfo.about.homePageUrl

    appPrefixName: Globals.ApplicationInfo.about.namePrefixForLogo
    appSuffixName: Globals.ApplicationInfo.about.nameSuffixForLogo
    appVersion: Globals.ApplicationInfo.about.version
    appDate: Globals.ApplicationInfo.about.date

    eulaUrl: Globals.ApplicationInfo.about.licenseUrl
    oslUrl: Globals.ApplicationInfo.about.dependenciesUrl

    description: Globals.ApplicationInfo.about.description
    developerIcons: Globals.ApplicationInfo.about.developerIcons
    developerYearsFrom: Globals.ApplicationInfo.about.developerYearsFrom
    developerYearsTo: Globals.ApplicationInfo.about.developerYearsTo

}
