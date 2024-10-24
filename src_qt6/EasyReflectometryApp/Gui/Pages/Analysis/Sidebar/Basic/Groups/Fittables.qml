// SPDX-FileCopyrightText: 2023 EasyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyDiffraction project <https://github.com/easyscience/EasyDiffraction>

import QtQuick
import QtQuick.Controls
import QtCharts

import EasyApp.Gui.Logic as EaLogic
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaElements.GroupBox {
    //title: qsTr("Parameters")
    collapsible: false
    last: true

    Column {
        property int selectedParamIndex: -1
        onSelectedParamIndexChanged: {
            updateSliderLimits()
            updateSliderValue()
        }

        property string selectedColor: EaStyle.Colors.themeForegroundHovered

        spacing: EaStyle.Sizes.fontPixelSize

        // Filter parameters widget
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            // Filter criteria
            EaElements.TextField {
                id: filterCriteriaField

                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

                placeholderText: qsTr("Filter criteria")

                onTextChanged: {
                    nameFilterSelector.currentIndex = nameFilterSelector.indexOfValue(text)
                    Globals.Proxies.main.fittables.nameFilterCriteria = text
                }
            }
            // Filter criteria

            // Filter by name
            EaElements.ComboBox {
                id: nameFilterSelector

                topInset: 0
                bottomInset: 0

                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

                valueRole: "value"
                textRole: "text"

                displayText: currentIndex === -1 ?
                                qsTr("Filter by name") :
                                currentText.replace('&nbsp;◦ ', '')

                model: [
                    { value: "", text: `All names (${Globals.Proxies.main.fittables.modelParamsCount + Globals.Proxies.main.fittables.experimentParamsCount})` },
                    { value: "model", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>layer-group </font>Model (${Globals.Proxies.main.fittables.modelParamsCount})` },
                    { value: "cell", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>cube </font>Unit cell` },
                    { value: "atom_site", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>atom </font>Atom sites` },
                    { value: "fract", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>map-marker-alt </font>Atomic coordinates` },
                    { value: "occupancy", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>fill </font>Atomic occupancies` },
                    { value: "B_iso", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>arrows-alt </font>Atomic displacement` },
                    { value: "experiment", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>microscope </font>Experiment (${Globals.Proxies.main.fittables.experimentParamsCount})` },
                    { value: "resolution", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>shapes </font>Peak shape` },
                    { value: "asymmetry", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>balance-scale-left </font>Peak asymmetry` },
                    { value: "background", text: `<font color='${EaStyle.Colors.themeForegroundMinor}' face='${EaStyle.Fonts.iconsFamily}'>wave-square </font>Background` }
                ]

                onActivated: filterCriteriaField.text = currentValue
            }
            // Filter by name

            // Filter by variability
            EaElements.ComboBox {
                id: variabilityFilterSelector

                property int lastIndex: -1

                topInset: 0
                bottomInset: 0

                width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

                displayText: currentIndex === -1 ? qsTr("Filter by variability") : currentText

                valueRole: "value"
                textRole: "text"

                model: [
                    { value: 'all', text: `All parameters (${Globals.Proxies.main.fittables.freeParamsCount +
                                                        Globals.Proxies.main.fittables.fixedParamsCount})` },
                    { value: 'free', text: `Free parameters (${Globals.Proxies.main.fittables.freeParamsCount})` },
                    { value: 'fixed', text: `Fixed parameters (${Globals.Proxies.main.fittables.fixedParamsCount})` }
                ]
                onModelChanged: currentIndex = lastIndex

                onActivated: {
                    lastIndex = currentIndex
                    Globals.Proxies.main.fittables.variabilityFilterCriteria = currentValue
                }
            }
            // Filter by variability

        }
        // Filter parameters widget

        // Table
        EaComponents.TableView {
            id: tableView

            property var currentValueTextInput: null

            defaultInfoText: qsTr("No parameters found")

            maxRowCountShow: 7 +
                            Math.trunc((applicationWindow.height - EaStyle.Sizes.appWindowMinimumHeight) /
                                        EaStyle.Sizes.tableRowHeight)
            // Table model
            // We only use the length of the model object defined in backend logic and
            // directly access that model in every row using the TableView index property.
            model: Globals.Proxies.main_fittables_data.length
            // Table model

            Component.onCompleted: selectedParamIndex = 0

            // Header row
            header: EaComponents.TableViewHeader {
                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.5
                    //text: qsTr("No.")
                }

                EaComponents.TableViewLabel {
                    flexibleWidth: true
                    horizontalAlignment: Text.AlignLeft
                    color: EaStyle.Colors.themeForegroundMinor
                    text: qsTr("name")
                }

                EaComponents.TableViewLabel {
                    id: valueLabel
                    width: EaStyle.Sizes.fontPixelSize * 4.5
                    horizontalAlignment: Text.AlignRight
                    color: EaStyle.Colors.themeForegroundMinor
                    text: qsTr("value")
                }

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 2.0
                    horizontalAlignment: Text.AlignLeft
                    //text: qsTr("units")
                }

                EaComponents.TableViewLabel {
                    width: valueLabel.width
                    horizontalAlignment: Text.AlignRight
                    color: EaStyle.Colors.themeForegroundMinor
                    text: qsTr("error")
                }

                EaComponents.TableViewLabel {
                    width: valueLabel.width
                    horizontalAlignment: Text.AlignRight
                    color: EaStyle.Colors.themeForegroundMinor
                    text: qsTr("min")
                }

                EaComponents.TableViewLabel {
                    width: valueLabel.width
                    horizontalAlignment: Text.AlignRight
                    color: EaStyle.Colors.themeForegroundMinor
                    text: qsTr("max")
                }

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 3.0
                    color: EaStyle.Colors.themeForegroundMinor
                    text: qsTr("vary")
                }
            }
            // Header row

            // Table content row
            delegate: EaComponents.TableViewDelegate {
                enabled: !Globals.Proxies.main.fitting.isFittingNow

                property bool isCurrentItem: ListView.isCurrentItem
                property var item: Globals.Proxies.main_fittables_data[index]

                mouseArea.onPressed: selectedParamIndex = tableView.currentIndex

                onIsCurrentItemChanged: {
                    if (tableView.currentValueTextInput != valueColumn) {
                    tableView.currentValueTextInput = valueColumn
                    }
                }

                EaComponents.TableViewLabel {
                    text: index + 1
                    color: EaStyle.Colors.themeForegroundMinor
                }

                EaComponents.TableViewLabel {
                    width: EaStyle.Sizes.fontPixelSize * 5
                    text: Globals.Proxies.paramName(item, EaGlobals.Vars.paramNameFormat)
                    textFormat: EaGlobals.Vars.paramNameFormat === EaGlobals.Vars.PlainShortWithLabels ||
                                EaGlobals.Vars.paramNameFormat === EaGlobals.Vars.PlainFullWithLabels ?
                                    Text.PlainText :
                                    Text.RichText
                    //clip: true
                    elide: Text.ElideMiddle  // NEED FIX: Doesn't work with textFormat: Text.RichText
                    ToolTip.text: textFormat === Text.PlainText ? text : ''
                }

                EaComponents.TableViewParameter {
                    id: valueColumn
                    selected: //index === tableView.currentIndex ||
                            index === selectedParamIndex
                    fit: item.fit
                    text: item.error === 0 ?
                            EaLogic.Utils.toDefaultPrecision(item.value) :
                            Globals.Proxies.main.backendHelpers.toStdDevSmalestPrecision(item.value, item.error).value
                    onEditingFinished: {
                        focus = false
                        console.debug('')
                        console.debug("*** Editing (manual) 'value' field of fittable on Analysis page ***")
                        Globals.Proxies.main.fittables.editSilently(item.blockType,
                                                                    item.blockIdx,
                                                                    item.category,
                                                                    item.rowIndex ?? -1,
                                                                    item.name,
                                                                    'value',
                                                                    text)
                        updateSliderLimits()
                        slider.value = Globals.Proxies.main_fittables_data[selectedParamIndex].value

                    }
                }

                EaComponents.TableViewLabel {
                    text: item.units
                    color: EaStyle.Colors.themeForegroundMinor
                }

                EaComponents.TableViewLabel {
                    elide: Text.ElideNone
                    text: item.error === 0 ?
                            '' :
                            Globals.Proxies.main.backendHelpers.toStdDevSmalestPrecision(item.value, item.error).std_dev
                }

                EaComponents.TableViewParameter {
                    minored: true
                    text: EaLogic.Utils.toDefaultPrecision(item.min).replace('Infinity', 'inf')
                    onEditingFinished: {
                        focus = false
                        console.debug('')
                        console.debug("*** Editing 'min' field of fittable on Analysis page ***")
                        const value = (text === '' ? '-inf' : text)
                        Globals.Proxies.main.fittables.editSilently(item.blockType,
                                                                    item.blockIdx,
                                                                    item.category,
                                                                    item.rowIndex ?? -1,
                                                                    item.name,
                                                                    'min',
                                                                    value)
                    }
                }

                EaComponents.TableViewParameter {
                    minored: true
                    text: EaLogic.Utils.toDefaultPrecision(item.max).replace('Infinity', 'inf')
                    onEditingFinished: {
                        focus = false
                        console.debug('')
                        console.debug("*** Editing 'max' field of fittable on Analysis page ***")
                        const value = (text === '' ? 'inf' : text)
                        Globals.Proxies.main.fittables.editSilently(item.blockType,
                                                                    item.blockIdx,
                                                                    item.category,
                                                                    item.rowIndex ?? -1,
                                                                    item.name,
                                                                    'max',
                                                                    value)
                    }
                }

                EaComponents.TableViewCheckBox {
                    id: fitColumn
                    enabled: Globals.Proxies.main.experiment.defined
                    checked: item.fit
                    onToggled: {
                        console.debug('')
                        console.debug("*** Editing 'fit' field of fittable on Analysis page ***")
                        Globals.Proxies.main.fittables.editSilently(item.blockType,
                                                                    item.blockIdx,
                                                                    item.category,
                                                                    item.rowIndex ?? -1,
                                                                    item.name,
                                                                    'fit',
                                                                    checked)
                    }
                }
            }
            // Table content row
        }
        // Table

        // Parameter change slider
        Row {
            visible: Globals.Proxies.main_fittables_data.length

            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.TextField {
                readOnly: true
                width: EaStyle.Sizes.fontPixelSize * 6
                //text: EaLogic.Utils.toDefaultPrecision(slider.from)
                //text: EaLogic.Utils.toErrSinglePrecision(slider.from, Globals.Proxies.main_fittables_data[selectedParamIndex].error)
                text: {
                    const value = Globals.Proxies.main_fittables_data[selectedParamIndex].value
                    const error = Globals.Proxies.main_fittables_data[selectedParamIndex].error
                    //return EaLogic.Utils.toErrSinglePrecision(value, error).length <= 8 ?
                    //            EaLogic.Utils.toErrSinglePrecision(slider.from, error) :
                    //            EaLogic.Utils.toDefaultPrecision(slider.from)
                    return error === 0 ?
                                EaLogic.Utils.toDefaultPrecision(slider.from) :
                                Globals.Proxies.main.backendHelpers.toStdDevSmalestPrecision(slider.from, error).value
                }
            }

            EaElements.Slider {
                id: slider

                enabled: !Globals.Proxies.main.fitting.isFittingNow
                width: tableView.width - EaStyle.Sizes.fontPixelSize * 14

                stepSize: (to - from) / 20
                snapMode: Slider.SnapAlways

                toolTipText: {
                    const value = Globals.Proxies.main_fittables_data[selectedParamIndex].value
                    const error = Globals.Proxies.main_fittables_data[selectedParamIndex].error
                    //return EaLogic.Utils.toErrSinglePrecision(value, error).length <= 8 ?
                    //            EaLogic.Utils.toErrSinglePrecision(value, error) :
                    //            EaLogic.Utils.toDefaultPrecision(value)
                    return error === 0 ?
                                EaLogic.Utils.toDefaultPrecision(value) :
                                Globals.Proxies.main.backendHelpers.toStdDevSmalestPrecision(value, error).value
                }

                onMoved: {
                        console.debug('')
                        console.debug("*** Editing (slider) 'value' field of fittable on Analysis page ***")
                        const item = Globals.Proxies.main_fittables_data[selectedParamIndex]
                        Globals.Proxies.main.fittables.editSilently(item.blockType,
                                                                    item.blockIdx,
                                                                    item.category,
                                                                    item.rowIndex ?? -1,
                                                                    item.name,
                                                                    'value',
                                                                    value.toString())
                }

                onPressedChanged: {
                    if (!pressed) {
                        updateSliderLimits()
                    }
                }
            }

            EaElements.TextField {
                readOnly: true
                width: EaStyle.Sizes.fontPixelSize * 6
                //text: EaLogic.Utils.toDefaultPrecision(slider.to)
                //text: EaLogic.Utils.toErrSinglePrecision(slider.to, Globals.Proxies.main_fittables_data[selectedParamIndex].error)
                text: {
                    const value = Globals.Proxies.main_fittables_data[selectedParamIndex].value
                    const error = Globals.Proxies.main_fittables_data[selectedParamIndex].error
                    //return EaLogic.Utils.toErrSinglePrecision(value, error).length <= 8 ?
                    //            EaLogic.Utils.toErrSinglePrecision(slider.to, error) :
                    //            EaLogic.Utils.toDefaultPrecision(slider.to)
                    return error === 0 ?
                                EaLogic.Utils.toDefaultPrecision(slider.to) :
                                Globals.Proxies.main.backendHelpers.toStdDevSmalestPrecision(slider.to, error).value
                }
            }

        }
        // Slider

        // Move delay timer

        /*
        Timer {
            id: moveDelayTimer
            interval: 0 //50
            onTriggered: {
                if (tableView.currentValueTextInput.text !== slider.value.toFixed(4)) {
                    //enableOpenGL()
                    tableView.currentValueTextInput.text = slider.value.toFixed(4)
                    tableView.currentValueTextInput.editingFinished()
                    //disableOpenGL()
                }
            }
        }
        */

        // Use OpenGL on slider move only

        Timer {
            id: disableOpenGLTimer
            interval: 1500
            onTriggered: disableOpenGLFromTimer()
        }

        // Logic

        function updateSliderValue() {
            const value = Globals.Proxies.main_fittables_data[selectedParamIndex].value
            slider.value = EaLogic.Utils.toDefaultPrecision(value)
        }

        function updateSliderLimits() {
            const from = Globals.Proxies.main_fittables_data[selectedParamIndex].from
            const to = Globals.Proxies.main_fittables_data[selectedParamIndex].to
            slider.from = EaLogic.Utils.toDefaultPrecision(from)
            slider.to = EaLogic.Utils.toDefaultPrecision(to)
        }

        function enableOpenGL() {
            if (Globals.Proxies.main.plotting.currentLib1d === 'QtCharts') {
                Globals.Refs.app.experimentPage.plotView.useOpenGL = true
                //Globals.Refs.app.modelPage.plotView.useOpenGL = true
                Globals.Refs.app.analysisPage.plotView.useAnimation = false
                Globals.Refs.app.analysisPage.plotView.useOpenGL = true
            }
        }

        function disableOpenGL() {
            if (Globals.Proxies.main.plotting.currentLib1d === 'QtCharts') {
                ////Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie.pointsReplaced()
                disableOpenGLTimer.restart()
            }
        }

        function disableOpenGLFromTimer() {
            Globals.Refs.app.experimentPage.plotView.useOpenGL = false
            //Globals.Refs.app.modelPage.plotView.useOpenGL = false
            ////Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie.pointsReplaced()
            ///console.error(Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie)
            Globals.Refs.app.analysisPage.plotView.useAnimation = true
            Globals.Refs.app.analysisPage.plotView.useOpenGL = false
        }
    }
}