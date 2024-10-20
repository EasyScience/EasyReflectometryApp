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
// -- Should implement setters for properties that are writable, onChanged breaks the link to the property.

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

    readonly property string projectName: activeBackend.project.name
    function projectSetName(value) { activeBackend.project.setName(value) } 
    readonly property string projectDescription: activeBackend.project.description
    function projectSetDescription(value) { activeBackend.project.setDescription(value) } 
    readonly property string projectLocation: activeBackend.project.location
    function projectSetLocation(value) { activeBackend.project.setLocation(value) } 

    function projectCreate() { activeBackend.project.create() }
    function projectReset() { activeBackend.project.reset() }
    function projectSave() { activeBackend.project.save() }
    function projectLoad(value) { activeBackend.project.load(value) }


    ///////////////
    // Sample page
    ///////////////

    // Material
    readonly property var sampleMaterials: activeBackend.sample.materials
    readonly property var sampleMaterialNames: activeBackend.sample.materialNames

//    readonly property int sampleCurrentMaterialIndex: activeBackend.sample.currentMaterialIndex
    function sampleSetCurrentMaterialIndex(value) { activeBackend.sample.setCurrentMaterialIndex(value) }

    function sampleSetCurrentMaterialName(value) { activeBackend.sample.setCurrentMaterialName(value) }
    function sampleSetCurrentMaterialSld(value) { activeBackend.sample.setCurrentMaterialSld(value) } 
    function sampleSetCurrentMaterialISld(value) { activeBackend.sample.setCurrentMaterialISld(value) }
    function sampleRemoveMaterial(value) { activeBackend.sample.removeMaterial(value) }
    function sampleAddNewMaterial() { activeBackend.sample.addNewMaterial() }
    function sampleDuplicateSelectedMaterial() { activeBackend.sample.duplicateSelectedMaterial() }
    function sampleMoveSelectedMaterialUp() { activeBackend.sample.moveSelectedMaterialUp() }
    function sampleMoveSelectedMaterialDown() { activeBackend.sample.moveSelectedMaterialDown() }

    // Model
    readonly property var sampleModels: activeBackend.sample.models
    readonly property string sampleCurrentModelName: activeBackend.sample.currentModelName

//    readonly property int sampleCurrentModelIndex: activeBackend.sample.currentModelIndex
    function sampleSetCurrentModelIndex(value) { activeBackend.sample.setCurrentModelIndex(value) }

    function sampleSetCurrentModelName(value) { activeBackend.sample.setCurrentModelName(value) }
    function sampleRemoveModel(value) { activeBackend.sample.removeModel(value) }
    function sampleAddNewModel() { activeBackend.sample.addNewModel() }
    function sampleDuplicateSelectedModel() { activeBackend.sample.duplicateSelectedModel() }
    function sampleMoveSelectedModelUp() { activeBackend.sample.moveSelectedModelUp() }
    function sampleMoveSelectedModelDown() { activeBackend.sample.moveSelectedModelDown() }

    // Sample
    readonly property var sampleAssemblies: activeBackend.sample.assemblies
    readonly property string sampleCurrentAssemblyName: activeBackend.sample.currentAssemblyName
    readonly property string sampleCurrentAssemblyType: activeBackend.sample.currentAssemblyType

//    readonly property int sampleCurrentAssemblyIndex: activeBackend.sample.currentAssemblyIndex
    function sampleSetCurrentAssemblyIndex(value) { activeBackend.sample.setCurrentAssemblyIndex(value) }

    function sampleSetCurrentAssemblyName(value) { activeBackend.sample.setCurrentAssemblyName(value) }
    function sampleSetCurrentAssemblyType(value) { activeBackend.sample.setCurrentAssemblyType(value) }
    function sampleRemoveAssembly(value) { activeBackend.sample.removeAssembly(value) }
    function sampleAddNewAssembly() { activeBackend.sample.addNewAssembly() }
    function sampleDuplicateSelectedAssembly() { activeBackend.sample.duplicateSelectedAssembly() }
    function sampleMoveSelectedAssemblyUp() { activeBackend.sample.moveSelectedAssemblyUp() }
    function sampleMoveSelectedAssemblyDown() { activeBackend.sample.moveSelectedAssemblyDown() }

    // Assembly specific methods
    readonly property int sampleCurrentAssemblyRepeatedLayerReptitions: activeBackend.sample.currentAssemblyRepeatedLayerReptitions
    function sampleSetCurrentAssemblyConstrainAPM(value) { activeBackend.sample.setCurrentAssemblyConstrainAPM(value) }
    function sampleSetCurrentAssemblyConformalRoughness(value) { activeBackend.sample.setCurrentAssemblyConformalRoughness(value) }
    function sampleSetCurrentAssemblyRepeatedLayerReptitions(value) { activeBackend.sample.setCurrentAssemblyRepeatedLayerReptitions(value) }

    // Layer
    readonly property var sampleLayers: activeBackend.sample.layers
    readonly property string sampleCurrentLayerName: activeBackend.sample.currentLayerName

//    readonly property int sampleCurrentLayerIndex: activeBackend.sample.currentLayerIndex
    function sampleSetCurrentLayerIndex(value) { activeBackend.sample.setCurrentLayerIndex(value) }

    function sampleRemoveLayer(value) { activeBackend.sample.removeLayer(value) }
    function sampleAddNewLayer() { activeBackend.sample.addNewLayer() }
    function sampleDuplicateSelectedLayer() { activeBackend.sample.duplicateSelectedLayer() }
    function sampleMoveSelectedLayerUp() { activeBackend.sample.moveSelectedLayerUp() }
    function sampleMoveSelectedLayerDown() { activeBackend.sample.moveSelectedLayerDown() }

    function sampleSetCurrentLayerFormula(value) { activeBackend.sample.setCurrentLayerFormula(value) }
    function sampleSetCurrentLayerMaterial(value) { activeBackend.sample.setCurrentLayerMaterial(value) }
    function sampleSetCurrentLayerSolvent(value) { activeBackend.sample.setCurrentLayerSolvent(value) }
    function sampleSetCurrentLayerThickness(value) { activeBackend.sample.setCurrentLayerThickness(value) }
    function sampleSetCurrentLayerRoughness(value) { activeBackend.sample.setCurrentLayerRoughness(value) }
    function sampleSetCurrentLayerAPM(value) { activeBackend.sample.setCurrentLayerAPM(value) }
    function sampleSetCurrentLayerSolvation(value) { activeBackend.sample.setCurrentLayerSolvation(value) }

    ///////////////
    // Analysis page
    ///////////////
    readonly property bool analysisIsFitFinished: activeBackend.analysis.isFitFinished


    ///////////////
    // Summary page
    ///////////////
    readonly property bool summaryCreated: activeBackend.report.created
    readonly property string summaryAsHtml: activeBackend.report.asHtml

    ///////////////
    // Plotting
    ///////////////

     function plottingSetQtChartsReflectometrySerieRef(value1, value2, value3) { activeBackend.plotting.setQtChartsReflectometrySerieRef(value1, value2, value3) }
     function plottingSetQtChartsSldSerieRef(value1, value2, value3) { activeBackend.plotting.setQtChartsSldSerieRef(value1, value2, value3) }

}
