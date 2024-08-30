pragma Singleton

import QtQuick

import Backends.Mock as MockBackend


// Wrapper to expose the backend properties and methods to the QML GUI.
// Backend implementations are located in the Backends folder.
// Serves to decouple the GUI code from the backend code.
// - In GUI code, backend properties and methods MUST be accessed through this object.
// - The backend is selected at runtime based on the availability of the backend_py object.
// - The properties are read-only, setter methods are exposed.
// -- To protect the backend from unwanted changes.
// -- To prevent the GUI from breaking the link to the backend property.
// -- To pass a property value from the GUI to the backend one needs to used dedicated set methods.
// - A flat structure is used.
// -- Enable QT Creator to show the properties in the editor (code completion and rightclick follow).
// -- Location of property in backend should be encoded in the name. 

QtObject {

    ///////////////
    // Determine active backend
    ///////////////
    // Sets the active backend to pyBackend if this property is defined
    // otherwise sets it to mockBackend
    readonly property var mockBackend: MockBackend.Backend
    readonly property var pyBackend: typeof backend_py !== 'undefined' && backend_py !== null ? backend_py : undefined
    readonly property var activeBackend: pyBackend ?? mockBackend

    /////////////
    // Status bar
    /////////////
    readonly property string statusProject: activeBackend.status.project
    readonly property string statusPhaseCount: activeBackend.status.phaseCount
    readonly property string statusExperimentsCount: activeBackend.status.experimentsCount
    readonly property string statusCalculator: activeBackend.status.calculator
    readonly property string statusMinimizer: activeBackend.status.minimizer
    readonly property string statusVariables: activeBackend.status.variables

    ///////////////
    // Home page
    ///////////////
    readonly property string homeVersionNumber: activeBackend.home.version.number
    readonly property string homeVersionDate: activeBackend.home.version.date
    readonly property string homeUrlsHomepage: activeBackend.home.urls.homepage
    readonly property string homeUrlsIssues: activeBackend.home.urls.issues
    readonly property string homeUrlsLicense: activeBackend.home.urls.license
    readonly property string homeUrlsDocumentation: activeBackend.home.urls.documentation
    readonly property string homeUrlsDependencies: activeBackend.home.urls.dependencies

    ///////////////
    // Project page
    ///////////////
    readonly property bool projectCreated: activeBackend.project.created
    readonly property string projectCreationDate: activeBackend.project.creationDate
    readonly property string projectName: activeBackend.project.name
    function projectSetName(value) { activeBackend.project.name = value }
    readonly property string projectDescription: activeBackend.project.description
    function projectSetDescription(value) { activeBackend.project.description = value }
    readonly property string projectLocation: activeBackend.project.location
    function projectSetLocation(value) { activeBackend.project.location = value }
    function projectCreate(value) { activeBackend.project.create(value) }
    function projectSave() { activeBackend.project.save() }

    ///////////////
    // Summary page
    ///////////////
    readonly property bool summaryCreated: activeBackend.report.created
    readonly property string summaryAsHtml: activeBackend.report.asHtml

}
