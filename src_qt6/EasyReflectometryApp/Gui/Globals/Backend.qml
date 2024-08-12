pragma Singleton

import QtQuick

import Backend.Mock as MockBackend


// If the backend_proxy_py object is created in main.py and exposed to qml, it is used as
// realBackendPy to access the necessary backend properties and methods. Otherwise, the mock
// proxy defined in MockBackend/Backend.qml with hardcoded data is used.
// The assumption here is that the real backend proxy and the mock proxy have the same API.

QtObject {

    ///////////////
    // Backend proxy
    ///////////////

    readonly property var mockBackendQml: MockBackend.Backend

    readonly property var realBackendPy: typeof backend_proxy_py !== 'undefined' &&
                                              backend_proxy_py !== null ?
                                                  backend_proxy_py :
                                                  undefined

    // This property is used to access the backend proxy object from GUI components.
    // Sets Backend to realBackendPy if this property is defined, otherwise sets it to
    // mockBackendQml
    readonly property var backend: realBackendPy ?? mockBackendQml

    /////////////
    // Status bar
    /////////////

    readonly property var status: QtObject {
        readonly property string project: backend.status.project
        readonly property string phaseCount: backend.status.phaseCount
        readonly property string experimentsCount: backend.status.experimentsCount
        readonly property string calculator: backend.status.calculator
        readonly property string minimizer: backend.status.minimizer
        readonly property string variables: backend.status.variables
    }

    ///////////////
    // Home page
    ///////////////

    readonly property var home: QtObject {
        readonly property string versionNumber: backend.home.version.number
        readonly property string versionDate: backend.home.version.date
        readonly property string homepageUrl: backend.home.urls.homepage
        readonly property string issuesUrl: backend.home.urls.issues
        readonly property string licenseUrl: backend.home.urls.license
        readonly property string documentationUrl: backend.home.urls.documentation
        readonly property string dependenciesUrl: backend.home.urls.dependencies
    }

    ///////////////
    // Project page
    ///////////////

    readonly property var project: QtObject {
        readonly property bool created: backend.project.created
        readonly property var info: backend.project.info

        function create() { backend.project.create() }
        function save() { backend.project.save() }
    }

    ///////////////
    // Summary page
    ///////////////

    readonly property var summary: QtObject {
        readonly property bool created: backend.report.created
        readonly property string asHtml: backend.report.asHtml
    }

}
