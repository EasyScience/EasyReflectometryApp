pragma Singleton

import QtQuick

import Backends as Backends

// Wrapper to external backend API to expose properties and methods to the QML GUI.
// Backend implementations are located in the Backends folder.
// Serves to decouple the GUI code from the backend code.
// - In GUI code, backend properties and methods MUST be accessed through this object.
// - The backend is instantiated at runtime based on the availability of the PyBackend class.
// - A flat structure is used.
// -- Enable QT Creator to show the properties in the editor (code completion and rightclick follow).
// -- Location of property in backend should be encoded in the name. 

QtObject {

    ///////////////
    // Active backend
    ///////////////
    // Instantiate MockBackend if PyBackend is not defined otherwise use PyBackend
    // The PyBackend class will be defined if exposed from main.py
    readonly property var activeBackend: {
        if (typeof Backends.PyBackend == 'undefined') {
            console.debug('MOCK backend is in use')
            return Backends.MockBackend
        } else {
            console.debug('PYTHON backend proxy is in use')
            return Backends.PyBackend
        }
    }

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

    property string projectName: activeBackend.project.name
    onProjectNameChanged: activeBackend.project.name = projectName
    property string projectDescription: activeBackend.project.description
    onProjectDescriptionChanged: activeBackend.project.description = projectDescription
    property string projectLocation: activeBackend.project.location
    onProjectLocationChanged: activeBackend.project.location = projectLocation

    function projectCreate() { activeBackend.project.create() }
    function projectReset() { activeBackend.project.reset() }
    function projectSave() { activeBackend.project.save() }
    function projectLoad(value) { activeBackend.project.load(value) }

    ///////////////
    // Summary page
    ///////////////
    readonly property bool summaryCreated: activeBackend.report.created
    readonly property string summaryAsHtml: activeBackend.report.asHtml

}
