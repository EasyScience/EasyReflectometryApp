import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    id: table

    enabled: ExGlobals.Constants.proxy.isFitFinished

    maxRowCountShow: 8
    defaultInfoText: qsTr("No Parameters Found")

    // Table model

    model: XmlListModel {
        id: fitablesModel

        //xml: ExGlobals.Constants.proxy.fitablesListAsXml
        xml: ExGlobals.Constants.proxy.parametersAsXml

        query: "/root/item"

        XmlRole { name: "id"; query: "id/string()" }
        XmlRole { name: "number"; query: "number/number()" }
        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "value"; query: "value/number()" }
        XmlRole { name: "unit"; query: "unit/string()" }
        XmlRole { name: "error"; query: "error/number()" }
        XmlRole { name: "fit"; query: "fit/number()" }

        onStatusChanged: {
            if (status === XmlListModel.Ready) {
                storeCurrentParameter()
            }
        }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numberColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.number
        }

        EaComponents.TableViewLabel {
            id: labelColumn
            horizontalAlignment: Text.AlignLeft
            width: table.width -
                   (parent.children.length - 1) * EaStyle.Sizes.tableColumnSpacing -
                   numberColumn.width -
                   valueColumn.width -
                   unitColumn.width -
                   errorColumn.width -
                   fitColumn.width
            headerText: "Label"
            text: formatLabel(model.index, model.label)
            textFormat: Text.RichText
        }

        EaComponents.TableViewTextInput {
            id: valueColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Value"
            text: model.value.toFixed(4)
            onEditingFinished: editParameterValue(model.id, text)

            Component.onCompleted: {
                if (model.label.endsWith('.resolution_u')) {
                    ExGlobals.Variables.fitResolutionUValue = this
                } else if (model.label.endsWith('.resolution_v')) {
                    ExGlobals.Variables.fitResolutionVValue = this
                } else if (model.label.endsWith('.resolution_w')) {
                    ExGlobals.Variables.fitResolutionWValue = this
                } else if (model.label.endsWith('.resolution_y')) {
                    ExGlobals.Variables.fitResolutionYValue = this
                }
            }
        }

        EaComponents.TableViewLabel {
            id: unitColumn
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 2
            text: model.unit
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewLabel {
            id: errorColumn
            horizontalAlignment: Text.AlignRight
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Error  "
            text: model.error === 0.0 || model.error > 999999 ? "" : model.error.toFixed(4) + "  "
        }

        EaComponents.TableViewCheckBox {
            enabled: ExGlobals.Constants.proxy.experimentLoaded
            id: fitColumn
            headerText: "Fit"
            checked: model.fit
            onCheckedChanged: editParameterFit(model.id, checked)

            Component.onCompleted: {
                if (model.label.endsWith('.length_a'))
                    ExGlobals.Variables.fitCellACheckBox = this
                if (model.label.endsWith('.zero_shift'))
                    ExGlobals.Variables.fitZeroShiftCheckBox = this
                if (model.label.endsWith('.scale'))
                    ExGlobals.Variables.fitScaleCheckBox = this
            }
        }

    }

    onCurrentIndexChanged: storeCurrentParameter()

    // Logic

    function storeCurrentParameter() {
        if (typeof model.get(currentIndex) === "undefined")
            return
        ExGlobals.Variables.currentParameterId = model.get(currentIndex).id
        ExGlobals.Variables.currentParameterValue = model.get(currentIndex).value
    }

    function editParameterValue(id, value) {
        //ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }
    function editParameterFit(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, value)
    }

    function formatLabel(index, label) {
        if (index < 0 || typeof label === "undefined")
            return ""

        const datasetName = ExGlobals.Constants.proxy.experimentDataAsObj[0].name

        // Modify current label
        label = label.replace("Instrument.", `Instrument.${datasetName}.`)
        label = label.replace(".background.", ".")
        label = label.replace("Uiso.Uiso", "Uiso")
        label = label.replace("fract_", "fract.")
        label = label.replace("length_", "length.")
        label = label.replace("angle_", "angle.")
        label = label.replace("resolution_", "resolution.")

        // Current label to list
        let list = label.split(".")
        const last = list.length - 1

        // Modify previous label to list
        let previousLabel = index > 0 ? fitablesModel.get(index - 1).label : ""
        previousLabel = previousLabel.replace("Instrument.", `Instrument.${datasetName}.`)
        previousLabel = previousLabel.replace(".background.", ".")
        previousLabel = previousLabel.replace("Uiso.Uiso", "Uiso")
        previousLabel = previousLabel.replace("fract_", "fract.")
        previousLabel = previousLabel.replace("length_", "length.")
        previousLabel = previousLabel.replace("angle_", "angle.")
        previousLabel = previousLabel.replace("resolution_", "resolution.")

        // Previous label to list
        let previousList = previousLabel.split(".")

        // First element formatting
        //const iconColor = EaStyle.Colors.themeForegroundMinor
        const iconColor = EaStyle.Colors.isDarkTheme ? Qt.darker(EaStyle.Colors.themeForegroundMinor, 1.2) : Qt.lighter(EaStyle.Colors.themeForegroundMinor, 1.2)
        if (list[0] === previousList[0]) {
            if (ExGlobals.Variables.iconifiedNames) {
                list[0] = `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">${list[0]}</font>`
                list[0] = list[0].replace("Phases", "gem").replace("Instrument", "microscope")
            } else {
                list[0] = `<font color=${EaStyle.Colors.themeForegroundMinor}>${list[0]}</font>`
            }
        } else {
            if (ExGlobals.Variables.iconifiedNames) {
                list[0] = `<font face="${EaStyle.Fonts.iconsFamily}">${list[0]}</font>`
                list[0] = list[0].replace("Phases", "gem").replace("Instrument", "microscope")
            } else {
                list[0] = `<font color=${EaStyle.Colors.themeForeground}>${list[0]}</font>`
            }
        }

        // Intermediate elements formatting (excluding first and last)
        for (let i = 1; i < last; ++i) {
            if (list[i] === previousList[i]) {
                list[i] = `<font color=${EaStyle.Colors.themeForegroundMinor}>${list[i]}</font>`
                if (ExGlobals.Variables.iconifiedNames) {
                    list[i] = list[i].replace("lattice", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">cube</font>`)
                    list[i] = list[i].replace("length", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">ruler</font>`)
                    list[i] = list[i].replace("angle", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">less-than</font>`)
                    list[i] = list[i].replace("atoms", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">atom</font>`)
                    list[i] = list[i].replace("adp", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">arrows-alt</font>`)
                    list[i] = list[i].replace("fract", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">map-marker-alt</font>`)
                    list[i] = list[i].replace("resolution", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">grip-lines-vertical</font>`)
                    list[i] = list[i].replace("point_background", `<font color=${iconColor} face="${EaStyle.Fonts.iconsFamily}">wave-square</font>`)
                }
            } else {
                list[i] = `${list[i]}`
                if (ExGlobals.Variables.iconifiedNames) {
                    list[i] = list[i].replace("lattice", `<font face="${EaStyle.Fonts.iconsFamily}">cube</font>`)
                    list[i] = list[i].replace("length", `<font face="${EaStyle.Fonts.iconsFamily}">ruler</font>`)
                    list[i] = list[i].replace("angle", `<font face="${EaStyle.Fonts.iconsFamily}">less-than</font>`)
                    list[i] = list[i].replace("atoms", `<font face="${EaStyle.Fonts.iconsFamily}">atom</font>`)
                    list[i] = list[i].replace("adp", `<font face="${EaStyle.Fonts.iconsFamily}">arrows-alt</font>`)
                    list[i] = list[i].replace("fract", `<font face="${EaStyle.Fonts.iconsFamily}">map-marker-alt</font>`)
                    list[i] = list[i].replace("resolution", `<font face="${EaStyle.Fonts.iconsFamily}">grip-lines-vertical</font>`)
                    list[i] = list[i].replace("point_background", `<font face="${EaStyle.Fonts.iconsFamily}">wave-square</font>`)
                }
            }
        }

        // Last element formatting
        //list[last] = `<font color=${EaStyle.Colors.themeForegroundHovered}>${list[last]}</font>`
        list[last] = `${list[last]}`

        // Back to string
        if (ExGlobals.Variables.iconifiedNames) {
            label = list.join(`&nbsp;&nbsp;`)
        } else {
            label = list.join(`<font color=${EaStyle.Colors.themeForegroundMinor}>.</font>`)
            label = label.replace("fract<font color=#aaaaaa>.", "fract_").replace("<font color=#aaaaaa>fract</font><font color=#aaaaaa>.", "fract_")
            label = label.replace("length<font color=#aaaaaa>.", "length_").replace("<font color=#aaaaaa>length</font><font color=#aaaaaa>.", "length_")
            label = label.replace("angle<font color=#aaaaaa>.", "angle_").replace("<font color=#aaaaaa>angle</font><font color=#aaaaaa>.", "angle_")
        }

        // 180,0_deg to 180.0°
        label = label.replace(",", ".").replace("_deg", "°")

        return label
    }

}

