pragma Singleton

import QtQuick

import Backend.Mock as MockBackend


// If the backend_py object is created in main.py and exposed to qml, it is used as
// realBackendPy to access the necessary backend properties and methods. Otherwise, the mock
// proxy defined in MockBackend/Backend.qml with hardcoded data is used.
// The assumption here is that the real backend proxy and the mock proxy have the same API.

QtObject {

    ///////////////
    // Backend proxy
    ///////////////

    readonly property var mockBackend: MockBackend.Backend

    readonly property var pyBackend: typeof backend_py !== 'undefined' && backend_py !== null ? backend_py : undefined

    // This property is used to access the backend proxy object from GUI components.
    // Sets Backend to pyBackend if this property is defined, otherwise sets it to
    // mockBackend
    readonly property var backend: pyBackend ?? mockBackend

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
        readonly property string urlsHomepage: backend.home.urls.homepage
        readonly property string urlsIssues: backend.home.urls.issues
        readonly property string urlsLicense: backend.home.urls.license
        readonly property string urlsDocumentation: backend.home.urls.documentation
        readonly property string urlsDependencies: backend.home.urls.dependencies
    }

    ///////////////
    // Project page
    ///////////////

    readonly property var project: QtObject {
        readonly property bool created: backend.project.created
        readonly property string creationDate: backend.project.creationDate

        readonly property string name: backend.project.name
        function setName(new_value) { backend.project.name = new_value }
        readonly property string description: backend.project.description
        function setDescription(new_value) { backend.project.description = new_value }
        readonly property string location: backend.project.location
        function setLocation(new_value) { backend.project.location = new_value }

        function create(project_path) { backend.project.create(project_path) }
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
