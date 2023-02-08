pragma Singleton

import QtQuick 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import Gui.Logic 1.0 as ExLogic

QtObject {
    readonly property var proxy: typeof _pyQmlProxyObj !== "undefined" && _pyQmlProxyObj !== null ? _pyQmlProxyObj : new ExLogic.PyQmlProxy.PyQmlProxy()
    readonly property bool remote: typeof EaGlobals.Variables.projectConfig.ci.app.info !== 'undefined'

    readonly property string appName: EaGlobals.Variables.projectConfig.project.name
    readonly property string appPrefixName: "Easy"
    readonly property string appSuffixName: appName.replace(appPrefixName, "")

    readonly property string appLogo: logo('App.svg')
    readonly property string appUrl: EaGlobals.Variables.projectConfig.project.urls.homepage
    readonly property string appGit: EaGlobals.Variables.projectConfig.project.urls.documentation

    readonly property string appVersion: EaGlobals.Variables.projectConfig.project.version
    readonly property string appDate: remote ? EaGlobals.Variables.projectConfig.ci.git.build_date : new Date().toISOString().slice(0,10)

    readonly property string commit: remote ? EaGlobals.Variables.projectConfig.ci.git.commit_sha_short : ''
    readonly property string commitUrl: remote ? EaGlobals.Variables.projectConfig.ci.git.commit_url : ''

    readonly property string branch: remote ? EaGlobals.Variables.projectConfig.ci.git.branch_name : ''
    readonly property string branchUrl: remote ? EaGlobals.Variables.projectConfig.git.branch_url : ''

    readonly property string eulaUrl: githubRawContent(branch, 'LICENSE.md')
    readonly property string oslUrl: githubRawContent(branch, 'DEPENDENCIES.md')

    readonly property string description:
`${appName} is a scientific software for
modelling and analysis of 
neutron and x-ray reflecometry data.

${appName} is build by ESS DMSC in
Copenhagen, Denmark.`

    readonly property string essLogo: logo('ESSlogo.png')

    // Logic

    function logo(file) {
        return Qt.resolvedUrl(`../Resources/Logo/${file}`)
    }

    function githubRawContent(branch, file) {
        return `https://raw.githubusercontent.com/easyScience/EasyReflectometryApp/${branch}/${file}`
    }
}
