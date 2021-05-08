pragma Singleton

import QtQuick 2.13

QtObject {
    // Debug mode
    property bool isDebugMode: typeof _pyQmlProxyObj === "undefined"

    // Initial application components accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool samplePageEnabled: isDebugMode ? true : false

    // Workflow states
    property bool needsSave: true // while waiting for a proper undo/redo flag

    // //////////
    // HTML parts
    // //////////
    property string analysisChartHeadScript: ""
    property string analysisChartHeadStyle: ""
    property string analysisChartHtml: ""
    property string reportHtml: ""

    //property string reportFilePath: ""

    // //////////////////////////
    // References to GUI elements
    // //////////////////////////

    // Application bar
    property var appBarCentralTabs

    // Application bar tab buttons
    property var homeTabButton
    property var projectTabButton
    property var sampleTabButton
    property var experimentTabButton
    property var analysisTabButton
    property var summaryTabButton

    // Sidebar controls tab buttons
    property var analysisBasicControlsTabButton
    property var analysisAdvancedControlsTabButton

    // Main application window
    property var showSaveDialog : false
    property var projectPageMainContent
    property var samplePageMainContent
    property var experimentPageMainContent
    property var analysisPageMainContent
    property var summaryPageMainContent

    // Application bar tool buttons
    property var preferencesButton

    // Main content and sidebar buttons
    property var aboutButton
    property var onlineDocumentationButton
    property var getInTouchButton
    property var startButton
    property var createProjectButton
    property var openProjectButton
    property var continueWithoutProjectButton
    property var loadExampleProjectButton
    property var setNewSampleManuallyButton
    property var appendNewAtomButton
    property var continueWithoutExperimentDataButton
    property var startFittingButton
    property var exportReportButton

    // Dialog buttons
    property var preferencesOkButton
    property var refinementResultsOkButton
    property var saveConfirmationOkButton

    // Sidebar group boxes
    property var structuralPhasesGroup
    property var symmetryGroup
    property var atomsGroup
    property var adpsGroup
    property var experimentalDataGroup
    property var associatedPhasesGroup
    property var parametersGroup
    property var exportReportGroup

    // Sidebar elements
    property var cellLengthALabel

    // Tab buttons
    property var phaseCifTab
    property var experimentTableTab
    property var experimentCifTab
    property var calculationCifTab

    // Checkboxes
    property var enableToolTipsCheckBox
    property var enableUserGuidesCheckBox
    property var fitCellACheckBox
    property var fitZeroShiftCheckBox
    property var fitScaleCheckBox
    property var fitResolutionUValue
    property var fitResolutionVValue
    property var fitResolutionWValue
    property var fitResolutionYValue

    // Comboboxes
    property var themeSelector
    property var calculatorSelector
    property var parametersFilterTypeSelector

    // Tables
    property var phasesTable
    property var parametersTable
    property int currentPhaseIndex: -1
    property int currentAtomIndex: -1

    // Slider
    property string currentParameterId
    property real currentParameterValue

    // Analysis tab settings
    property bool showLegend: false
    property bool iconifiedNames: true

    // Plotting
    property var bokehStructureChart
    property var analysisChart
    property var analysisImageSource
    property var structureImageSource
    property var showBondsButton
    property var showLabelsButton
    property var projectionTypeButton
    property var xProjectionButton
    property var yProjectionButton
    property var zProjectionButton
    property var defaultViewButton

    // Summary
    property var reportWebView

    // User guides
    property var userGuidesLastDisableButton
    property var userGuidesNextButtons: [[], [], [], [], [], []]
    property var userGuidesTextList: [[], [], [], [], [], []]

}
