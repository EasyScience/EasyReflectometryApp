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

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phasesAsXml
        query: `/root/item[${phaseIndex}]/atoms/data/item`

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "adpType"; query: "adp/adp_type/value/string()" }
        XmlRole { name: "adpIso"; query: `adp/adp_class/Uiso/value/number()` }
        XmlRole { name: "adpAni11"; query: "adp_ani_11/number()" }
        XmlRole { name: "adpAni22"; query: "adp_ani_22/number()" }
        XmlRole { name: "adpAni33"; query: "adp_ani_33/number()" }
        XmlRole { name: "adpAni12"; query: "adp_ani_12/number()" }
        XmlRole { name: "adpAni13"; query: "adp_ani_13/number()" }
        XmlRole { name: "adpAni23"; query: "adp_ani_23/number()" }

        XmlRole { name: "adpIsoId"; query: "adp/adp_class/Uiso/key[4]/string()" }
        XmlRole { name: "adpAni11Id"; query: "adp_ani_11/key[4]/string()" }
        XmlRole { name: "adpAni22Id"; query: "adp_ani_22/key[4]/string()" }
        XmlRole { name: "adpAni33Id"; query: "adp_ani_33/key[4]/string()" }
        XmlRole { name: "adpAni12Id"; query: "adp_ani_12/key[4]/string()" }
        XmlRole { name: "adpAni13Id"; query: "adp_ani_13/key[4]/string()" }
        XmlRole { name: "adpAni23Id"; query: "adp_ani_23/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelAdpType: model.adpType

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            id: adpAtomLabel
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.fontPixelSize * 3.8
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewComboBox {
            enabled: false
            width: adpAtomLabel.width * 1.2
            headerText: "Type"
            model: ["Uiso", "Uani", "Biso", "Bani"]
            //currentIndex: model.indexOf(modelAdpType)
            Component.onCompleted: currentIndex = model.indexOf(modelAdpType)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Iso"
            text: EaLogic.Utils.toFixed(model.adpIso)
            onEditingFinished: editParameterValue(model.adpIsoId, text)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Ani11"
            text: EaLogic.Utils.toFixed(model.adpAni11)
            onEditingFinished: editParameterValue(model.adpAniId11, text)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Ani22"
            text: EaLogic.Utils.toFixed(model.adpAni22)
            onEditingFinished: editParameterValue(model.adpAniId22, text)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Ani33"
            text: EaLogic.Utils.toFixed(model.adpAni33)
            onEditingFinished: editParameterValue(model.adpAniId33, text)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Ani12"
            text: EaLogic.Utils.toFixed(model.adpAni12)
            onEditingFinished: editParameterValue(model.adpAniId12, text)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Ani13"
            text: EaLogic.Utils.toFixed(model.adpAni13)
            onEditingFinished: editParameterValue(model.adpAniId13, text)
        }

        EaComponents.TableViewTextInput {
            width: adpAtomLabel.width
            headerText: "Ani23"
            text: EaLogic.Utils.toFixed(model.adpAni23)
            onEditingFinished: editParameterValue(model.adpAniId23, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.editParameter(id, parseFloat(value))
    }

}
