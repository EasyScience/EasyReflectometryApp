import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents
import easyAppGui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView { 
    property bool enableDelButton:
        typeof ExGlobals.Constants.proxy.phasesAsObj[ExGlobals.Constants.proxy.currentPhaseIndex] !== 'undefined'
        && ExGlobals.Constants.proxy.phasesAsObj[ExGlobals.Constants.proxy.currentPhaseIndex].atoms.data.length > 1
        ? true
        : false

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: `/root/item[${phaseIndex}]/atoms/data/item`

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "type"; query: "specie/value/string()" }
        //XmlRole { name: "color"; query: "color/string()" }
        XmlRole { name: "x"; query: "fract_x/value/number()" }
        XmlRole { name: "y"; query: "fract_y/value/number()" }
        XmlRole { name: "z"; query: "fract_z/value/number()" }
        XmlRole { name: "occupancy"; query: "occupancy/value/number()" }

        XmlRole { name: "labelId"; query: "label/key[4]/string()" }
        XmlRole { name: "typeId"; query: "specie/key[4]/string()" }
        XmlRole { name: "xId"; query: "fract_x/key[4]/string()" }
        XmlRole { name: "yId"; query: "fract_y/key[4]/string()" }
        XmlRole { name: "zId"; query: "fract_z/key[4]/string()" }
        XmlRole { name: "occupancyId"; query: "occupancy/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelType: model.type

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewTextInput {
            id: atomLabel
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 4.22
            headerText: "Label"
            text: model.label
            onEditingFinished: editDescriptorValue(model.labelId, text)
        }

        /*
        EaComponents.TableViewComboBox {
            width: atomLabel.width
            currentIndex: model.indexOf(modelType)
            headerText: "Atom"
            model: ["Mn", "Fe", "Co", "Ni", "Cu", "Si", "O"]
        }
        */
        EaComponents.TableViewTextInput {
            width: atomLabel.width
            horizontalAlignment: Text.AlignLeft
            headerText: "Atom"
            text: model.type
            onEditingFinished: editDescriptorValue(model.typeId, text)
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "x"
            text: EaLogic.Utils.toFixed(model.x)
            onEditingFinished: editParameterValue(model.xId, text)
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "y"
            text: EaLogic.Utils.toFixed(model.y)
            onEditingFinished: editParameterValue(model.yId, text)
       }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "z"
            text: EaLogic.Utils.toFixed(model.z)
            onEditingFinished: editParameterValue(model.zId, text)
        }

        EaComponents.TableViewTextInput {
            width: atomLabel.width
            headerText: "Occ."
            text: EaLogic.Utils.toFixed(model.occupancy)
            onEditingFinished: editParameterValue(model.occupancyId, text)
        }

        EaComponents.TableViewLabel {
            headerText: "Color"
            backgroundColor: jmolAtomColor(model.type)
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            enabled: enableDelButton
            headerText: "Del." //"\uf2ed"
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this atom")
            onClicked: ExGlobals.Constants.proxy.removeAtom(model.label)
        }

    }

    onCurrentIndexChanged: ExGlobals.Variables.currentAtomIndex = currentIndex

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }

    function editDescriptorValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, value)
    }

    function jmolAtomColor(symbol) {
        const colors = {
            'H'  : '#FFFFFF',
            'He' : '#D9FFFF',
            'Li' : '#CC80FF',
            'Be' : '#C2FF00',
            'B'  : '#FFB5B5',
            'C'  : '#909090',
            'N'  : '#3050F8',
            'O'  : '#FF0D0D',
            'F'  : '#90E050',
            'Ne' : '#B3E3F5',
            'Na' : '#AB5CF2',
            'Mg' : '#8AFF00',
            'Al' : '#BFA6A6',
            'Si' : '#F0C8A0',
            'P'  : '#FF8000',
            'S'  : '#FFFF30',
            'Cl' : '#1FF01F',
            'Ar' : '#80D1E3',
            'K'  : '#8F40D4',
            'Ca' : '#3DFF00',
            'Sc' : '#E6E6E6',
            'Ti' : '#BFC2C7',
            'V'  : '#A6A6AB',
            'Cr' : '#8A99C7',
            'Mn' : '#9C7AC7',
            'Fe' : '#E06633',
            'Co' : '#F090A0',
            'Ni' : '#50D050',
            'Cu' : '#C88033',
            'Zn' : '#7D80B0',
            'Ga' : '#C28F8F',
            'Ge' : '#668F8F',
            'As' : '#BD80E3',
            'Se' : '#FFA100',
            'Br' : '#A62929',
            'Kr' : '#5CB8D1',
            'Rb' : '#702EB0',
            'Sr' : '#00FF00',
            'Y'  : '#94FFFF',
            'Zr' : '#94E0E0',
            'Nb' : '#73C2C9',
            'Mo' : '#54B5B5',
            'Tc' : '#3B9E9E',
            'Ru' : '#248F8F',
            'Rh' : '#0A7D8C',
            'Pd' : '#006985',
            'Ag' : '#C0C0C0',
            'Cd' : '#FFD98F',
            'In' : '#A67573',
            'Sn' : '#668080',
            'Sb' : '#9E63B5',
            'Te' : '#D47A00',
            'I'  : '#940094',
            'Xe' : '#429EB0',
            'Cs' : '#57178F',
            'Ba' : '#00C900',
            'La' : '#70D4FF',
            'Ce' : '#FFFFC7',
            'Pr' : '#D9FFC7',
            'Nd' : '#C7FFC7',
            'Pm' : '#A3FFC7',
            'Sm' : '#8FFFC7',
            'Eu' : '#61FFC7',
            'Gd' : '#45FFC7',
            'Tb' : '#30FFC7',
            'Dy' : '#1FFFC7',
            'Ho' : '#00FF9C',
            'Er' : '#00E675',
            'Tm' : '#00D452',
            'Yb' : '#00BF38',
            'Lu' : '#00AB24',
            'Hf' : '#4DC2FF',
            'Ta' : '#4DA6FF',
            'W'  : '#2194D6',
            'Re' : '#267DAB',
            'Os' : '#266696',
            'Ir' : '#175487',
            'Pt' : '#D0D0E0',
            'Au' : '#FFD123',
            'Hg' : '#B8B8D0',
            'Tl' : '#A6544D',
            'Pb' : '#575961',
            'Bi' : '#9E4FB5',
            'Po' : '#AB5C00',
            'At' : '#754F45',
            'Rn' : '#428296',
            'Fr' : '#420066',
            'Ra' : '#007D00',
            'Ac' : '#70ABFA',
            'Th' : '#00BAFF',
            'Pa' : '#00A1FF',
            'U'  : '#008FFF',
            'Np' : '#0080FF',
            'Pu' : '#006BFF',
            'Am' : '#545CF2',
            'Cm' : '#785CE3',
            'Bk' : '#8A4FE3',
            'Cf' : '#A136D4',
            'Es' : '#B31FD4',
            'Fm' : '#B31FBA',
            'Md' : '#B30DA6',
            'No' : '#BD0D87',
            'Lr' : '#C70066',
            'Rf' : '#CC0059',
            'Db' : '#D1004F',
            'Sg' : '#D90045',
            'Bh' : '#E00038',
            'Hs' : '#E6002E',
            'Mt' : '#EB0026',
            'Ds' : '#000000',
            'Rg' : '#000000',
            'Cn' : '#000000',
            'Nh' : '#000000',
            'Fl' : '#000000',
            'Mc' : '#000000',
            'Lv' : '#000000',
            'Ts' : '#000000',
            'Og' : '#000000'
        }
        if (colors.hasOwnProperty(symbol)) {
            return colors[symbol]
        }
        return 'transparent'
    }

}
