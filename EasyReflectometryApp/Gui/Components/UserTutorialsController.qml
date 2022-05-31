import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaElements.RemoteController {
    id: rc

    property bool isPreparationToFitDone: false
    property bool isFitSuccessfullyDone: typeof ExGlobals.Constants.proxy.fitter.fitResults.success !== 'undefined' &&
                                         ExGlobals.Constants.proxy.fitter.isFitFinished

    visible: false
    audioDir: Qt.resolvedUrl("../../Resources/Audio")
    //audioEnabled: false

    Timer {
        id: quitAppTimer

        interval: 1000
        onTriggered: {
            print("* closing app")
            Qt.quit()
        }
    }

    Timer {
        id: runTestTutorialTimer

        interval: 1000
        onTriggered: {
            startScreenRecording()
            runAppInterfaceTutorial()
            //runDataFittingTutorial()
            //runDataSimulationTutorial()
            stopScreenRecording()
        }
    }

    Timer {
        id: finishFittingTutorialTimer

        running: isPreparationToFitDone && isFitSuccessfullyDone
        interval: 1000
        onTriggered: {
            finishDataFittingTutorial()
            if (EaGlobals.Variables.isTestMode) {
                stopScreenRecording()
            }
        }
    }

    Component.onCompleted: {
        if (EaGlobals.Variables.isTestMode) {
            print('*** TEST MODE ***')
            runTestTutorialTimer.start()
        }
    }

    // Logic

    function startScreenRecording() {
        const frame_rect = {
            left: window.x,
            top: window.y,
            width: window.width,
            height: window.height
        }
        const margin_rect = {
            left: 3 * EaStyle.Sizes.fontPixelSize,
            top: 3 * EaStyle.Sizes.fontPixelSize,
            right: 3 * EaStyle.Sizes.fontPixelSize,
            bottom: 3 * EaStyle.Sizes.fontPixelSize
        }
        ExGlobals.Constants.proxy.screenRecorder.startRecording(frame_rect, margin_rect)
    }

    function stopScreenRecording() {
        ExGlobals.Constants.proxy.screenRecorder.stopRecording()
        quitAppTimer.start()
    }

    function playPageUserGuides(pageIndex) {
        const buttons = ExGlobals.Variables.userGuidesNextButtons[pageIndex]
        const textList = ExGlobals.Variables.userGuidesTextList[pageIndex]
        const waitingMultiplier = 40
        for (let i = 0; i < buttons.length; ++i) {
            //rc.say(textList[i])
            rc.wait(textList[i].length * waitingMultiplier)
            if (i !== buttons.length - 1) {
                rc.mouseClick(buttons[i])
            }
        }
    }

    function beforeRunTutorial() {
        rc.visible = true
        rc.posToCenter()
        rc.wait(2000)
        rc.showPointer()
    }

    function afterRunTutorial() {
        rc.hidePointer()
        //rc.say("Thank you for using easy diffraction.")
        rc.wait(1000)
        rc.visible = false
    }

    // Tutorials

    function runAppInterfaceTutorial() {
        print("* run app interface tutorial")

        beforeRunTutorial()

        // General
        rc.mouseClick(ExGlobals.Variables.preferencesButton)
        rc.mouseClick(ExGlobals.Variables.enableUserGuidesCheckBox)
        rc.mouseClick(ExGlobals.Variables.preferencesOkButton)

        afterRunTutorial()
    }

    function runAppInterfaceTutorial_original() {
        print("* run app interface tutorial")

        beforeRunTutorial()

        // General
        rc.mouseClick(ExGlobals.Variables.preferencesButton)
        rc.mouseClick(ExGlobals.Variables.enableUserGuidesCheckBox)
        rc.mouseClick(ExGlobals.Variables.preferencesOkButton)

        // Home page
        playPageUserGuides(EaGlobals.Variables.HomePageIndex)
        rc.mouseClick(ExGlobals.Variables.startButton)

        // Project page
        playPageUserGuides(EaGlobals.Variables.ProjectPageIndex)
        rc.mouseClick(ExGlobals.Variables.loadExampleProjectButton)
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)

        // Sample page
        playPageUserGuides(EaGlobals.Variables.SamplePageIndex)
        rc.mouseClick(ExGlobals.Variables.experimentTabButton)

        // Experiment page
        playPageUserGuides(EaGlobals.Variables.ExperimentPageIndex)
        rc.mouseClick(ExGlobals.Variables.analysisTabButton)

        // Analysis page
        playPageUserGuides(EaGlobals.Variables.AnalysisPageIndex)
        rc.mouseClick(ExGlobals.Variables.summaryTabButton)

        // Summary page
        playPageUserGuides(EaGlobals.Variables.SummaryPageIndex)
        rc.mouseClick(ExGlobals.Variables.userGuidesLastDisableButton)

        afterRunTutorial()
    }

    function runDataSimulationTutorial() {
        print("* run data simulation tutorial")

        const was_tool_tips_checked = ExGlobals.Variables.enableToolTipsCheckBox.checked
        let x_pos = undefined
        let y_pos = undefined

        beforeRunTutorial()

        // App preferences

        rc.say("Application preferences can be accessed quickly from the application toolbar.")
        rc.mouseClick(ExGlobals.Variables.preferencesButton)

        rc.mouseClick(ExGlobals.Variables.themeSelector)
        y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        if (!was_tool_tips_checked) {
            rc.mouseClick(ExGlobals.Variables.enableToolTipsCheckBox)
            rc.wait(500)
        }

        rc.mouseClick(ExGlobals.Variables.preferencesOkButton)

        // Home Tab

        rc.say("To start working with easy diffraction, just click start button.")
        rc.mouseClick(ExGlobals.Variables.startButton)

        // Project Tab

        //rc.say("Here, you can create a new project.")
        //rc.mouseClick(ExGlobals.Variables.createProjectButton)

        rc.say("Now, you can continue without creating a project.")
        rc.mouseClick(ExGlobals.Variables.continueWithoutProjectButton)

        // Sample Tab

        rc.say("Use application toolbar to switch to the sample description page.")
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)

        rc.say("You can set new phase from file or manually.")
        rc.mouseClick(ExGlobals.Variables.setNewSampleManuallyButton)

        rc.say("Now, you can change the symmetry and cell parameters.")
        rc.mouseClick(ExGlobals.Variables.symmetryGroup, 15)
        x_pos = typeof ExGlobals.Variables.cellLengthALabel !== 'undefined' ?
                    ExGlobals.Variables.cellLengthALabel.width :
                    0
        rc.mouseClick(ExGlobals.Variables.cellLengthALabel, x_pos)
        rc.hidePointer()
        //rc.keyClick(Qt.Key_Right)
        //rc.keyClick(Qt.Key_Right)
        rc.deleteCharacters(6)
        rc.typeText("7.00")
        rc.keyClick(Qt.Key_Enter) // DOESN'T WORK ON CI XVFB ?
        rc.showPointer()

        rc.say("Append or remove new atoms.")
        rc.mouseClick(ExGlobals.Variables.atomsGroup, 15)
        rc.mouseClick(ExGlobals.Variables.appendNewAtomButton)

        rc.say("To change the structure view parameters use the toolbar buttons.")
        rc.mouseClick(ExGlobals.Variables.xProjectionButton)
        rc.mouseClick(ExGlobals.Variables.showBondsButton)
        rc.mouseClick(ExGlobals.Variables.showBondsButton)
        rc.mouseClick(ExGlobals.Variables.showLabelsButton)
        rc.mouseClick(ExGlobals.Variables.showLabelsButton)
        rc.mouseClick(ExGlobals.Variables.projectionTypeButton)
        rc.mouseClick(ExGlobals.Variables.projectionTypeButton)
        rc.mouseClick(ExGlobals.Variables.yProjectionButton)
        rc.mouseClick(ExGlobals.Variables.zProjectionButton)
        rc.mouseClick(ExGlobals.Variables.defaultViewButton)

        rc.wait(1000)

        // Experiment Tab

        rc.say("When the sample is fully described, use application toolbar to switch to the experiment description page.")
        rc.mouseClick(ExGlobals.Variables.experimentTabButton)

        rc.say("If you don't have experimental data, just click continue without experiment button to enable analysis page and some parameters needed for simulation.")
        rc.mouseClick(ExGlobals.Variables.continueWithoutExperimentDataButton)

        // Analysis Tab

        rc.say("Now, you can switch to the analysis page to see and control the simulated diffraction pattern.")
        rc.mouseClick(ExGlobals.Variables.analysisTabButton)
        rc.wait(1000)
        rc.say("In the advanced controls, you can choose between different calculation engines.")
        rc.mouseClick(ExGlobals.Variables.analysisAdvancedControlsTabButton)
        // CFML
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        x_pos = undefined
        y_pos = EaStyle.Sizes.comboBoxHeight * 1.5
        rc.mouseClick(ExGlobals.Variables.calculatorSelector, x_pos, y_pos)
        rc.wait(1000)
        // GSAS-II
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        x_pos = undefined
        y_pos = EaStyle.Sizes.comboBoxHeight * 2.5
        rc.mouseClick(ExGlobals.Variables.calculatorSelector, x_pos, y_pos)
        rc.wait(1000)
        // CrysPy
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        rc.mouseClick(ExGlobals.Variables.calculatorSelector)
        rc.mouseClick(ExGlobals.Variables.analysisBasicControlsTabButton)

        // Summary Tab

        rc.say("Now, you can see the interactive report generated on the summary page and export it in different formats.")
        rc.mouseClick(ExGlobals.Variables.summaryTabButton)
        rc.wait(1000)
        //rc.pointerMove(ExGlobals.Variables.reportWebView)
        //rc.mouseMove(ExGlobals.Variables.reportWebView)
        //rc.mouseWheel(ExGlobals.Variables.reportWebView)
        //rc.wait(1000)

        // Restore app preferences

        rc.mouseClick(ExGlobals.Variables.preferencesButton)

        rc.mouseClick(ExGlobals.Variables.themeSelector)
        y_pos = !EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        if (!was_tool_tips_checked) {
            rc.mouseClick(ExGlobals.Variables.enableToolTipsCheckBox)
            rc.wait(500)
        }

        rc.mouseClick(ExGlobals.Variables.preferencesOkButton)

        afterRunTutorial()
    }

    function runDataFittingTutorial() {
        print("* run data fitting tutorial")

        isPreparationToFitDone = false

        let x_pos = undefined
        let y_pos = EaStyle.Sizes.comboBoxHeight * 2.5

        beforeRunTutorial()

        // Home Tab
        rc.mouseClick(ExGlobals.Variables.startButton)

        // Project Tab
        rc.mouseClick(ExGlobals.Variables.loadExampleProjectButton)
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)

        // Sample page
        rc.mouseClick(ExGlobals.Variables.experimentTabButton)

        // Experiment page
        rc.mouseClick(ExGlobals.Variables.analysisTabButton)

        // Analysis page
        rc.mouseClick(ExGlobals.Variables.fitCellACheckBox)
        rc.mouseClick(ExGlobals.Variables.parametersFilterTypeSelector)
        rc.mouseClick(ExGlobals.Variables.parametersFilterTypeSelector, x_pos, y_pos)
        rc.mouseClick(ExGlobals.Variables.fitZeroShiftCheckBox)
        rc.mouseClick(ExGlobals.Variables.fitScaleCheckBox)
        x_pos = typeof ExGlobals.Variables.fitResolutionYValue !== 'undefined' ?
                    ExGlobals.Variables.fitResolutionYValue.width :
                    0
        rc.mouseClick(ExGlobals.Variables.fitResolutionYValue, x_pos)
        rc.deleteCharacters(4)
        rc.typeText("0961")
        rc.keyClick(Qt.Key_Enter) // DOESN'T WORK ON CI XVFB ?
        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.startFittingButton)

        isPreparationToFitDone = true

        print("* fitting started")
    }

    function finishDataFittingTutorial() {
        print("* fitting finished")

        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.refinementResultsOkButton)
        rc.mouseClick(ExGlobals.Variables.summaryTabButton)

        // Summary page
        rc.mouseClick(ExGlobals.Variables.exportReportButton)
        rc.mouseClick(ExGlobals.Variables.saveConfirmationOkButton)

        afterRunTutorial()
    }

}
