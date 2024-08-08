pragma Singleton

import QtQuick

import Logic.Mock as MockLogic


// If the backend_proxy_py object is created in main.py and exposed to qml, it is used as
// realBackendProxyPy to access the necessary backend properties and methods. Otherwise, the mock
// proxy defined in MockLogic/BackendProxy.qml with hardcoded data is used.
// The assumption here is that the real backend proxy and the mock proxy have the same API.

QtObject {

    ///////////////
    // Backend proxy
    ///////////////

    readonly property var mockBackendProxyQml: MockLogic.BackendProxy

    readonly property var realBackendProxyPy: typeof backend_proxy_py !== 'undefined' &&
                                              backend_proxy_py !== null ?
                                                  backend_proxy_py :
                                                  undefined

    // This property is used to access the backend proxy object from GUI components.
    // Sets backendProxy to realBackendProxyPy if this property is defined, otherwise sets it to
    // mockBackendProxyQml
    readonly property var backendProxy: realBackendProxyPy ?? mockBackendProxyQml

    /////////////
    // Status bar
    /////////////

    readonly property var status: QtObject {
        readonly property string project: backendProxy.status.project
        readonly property string phaseCount: backendProxy.status.phaseCount
        readonly property string experimentsCount: backendProxy.status.experimentsCount
        readonly property string calculator: backendProxy.status.calculator
        readonly property string minimizer: backendProxy.status.minimizer
        readonly property string variables: backendProxy.status.variables
    }

    ///////////////
    // Home page
    ///////////////

    readonly property var home: QtObject {
        readonly property string versionNumber: backendProxy.home.version.number
        readonly property string versionDate: backendProxy.home.version.date
        readonly property string homepageUrl: backendProxy.home.urls.homepage
        readonly property string issuesUrl: backendProxy.home.urls.issues
        readonly property string licenseUrl: backendProxy.home.urls.license
        readonly property string documentationUrl: backendProxy.home.urls.documentation
        readonly property string dependenciesUrl: backendProxy.home.urls.dependencies
    }

    ///////////////
    // Project page
    ///////////////

    readonly property var project: QtObject {
        readonly property bool created: backendProxy.project.created
        readonly property var info: backendProxy.project.info

        function create() { backendProxy.project.create() }
        function save() { backendProxy.project.save() }
    }

    ///////////////
    // Summary page
    ///////////////

    readonly property var summary: QtObject {
        readonly property bool created: backendProxy.report.created
        readonly property string asHtml: backendProxy.report.asHtml
    }

}
