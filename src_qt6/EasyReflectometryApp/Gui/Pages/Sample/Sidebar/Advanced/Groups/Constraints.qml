import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQml.XmlListModel

import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents
import easyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals

EaElements.GroupBox {
    title: qsTr("Sample constraints")
    enabled: true
    last: false

//    ExComponents.AnalysisConstraints {}

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * 0.5

        // Type 1 START
        // Column {

        //     EaElements.Label {
        //         enabled: false
        //         text: qsTr("Type 1")
        //     }

        //     Grid {
        //         columns: 4
        //         columnSpacing: EaStyle.Sizes.fontPixelSize * 0.5
        //         rowSpacing: EaStyle.Sizes.fontPixelSize * 0.5
        //         anchors.horizontalCenter: parent.horizontalCenter
        //         verticalItemAlignment: Grid.AlignVCenter

        //         EaElements.ComboBox {
        //             id: dependentPar2
        //             width: 359
        //             currentIndex: -1
        //             displayText: currentIndex === -1 ? "Select parameter" : currentText
        //             // textFormat: ExGlobals.Variables.iconifiedNames ? Text.RichText : Text.PlainText
        //             // elide: Text.ElideMiddle
        //             textRole: ExGlobals.Variables.iconifiedNames ? "iconified_label" : "label"
        //             model: XmlListModel {
        //                 xml: ExGlobals.Constants.proxy.parameter.parametersAsXml
        //                 query: "/root/item"
        //                 XmlRole { name: "label"; query: "label/string()" }
        //                 onXmlChanged: dependentParCurrentIndex2 = dependentPar2.currentIndex
        //             }
        //             onCurrentIndexChanged: {
        //                 if (dependentPar2.currentIndex === -1 && model.count > 0)
        //                     dependentPar2.currentIndex = dependentParCurrentIndex2
        //             }
        //         }

        //         EaElements.ComboBox {
        //             id: relationalOperator2
        //             width: 47
        //             currentIndex: 0
        //             //model: [">", "<"]
        //             font.family: EaStyle.Fonts.iconsFamily
        //             model: XmlListModel {
        //                 xml: "<root><item><operator>&gt;</operator><icon>\uf531</icon></item><item><operator>&lt;</operator><icon>\uf536</icon></item></root>"
        //                 query: "/root/item"
        //                 XmlRole { name: "icon"; query: "icon/string()" }
        //             }
        //         }

        //         EaElements.TextField {
        //             id: value2
        //             width: 65
        //             horizontalAlignment: Text.AlignRight
        //             text: "1.0000"
        //         }

        //         EaElements.SideBarButton {
        //             id: addConstraint2
        //             width: 35
        //             fontIcon: "plus-circle"
        //             ToolTip.text: qsTr("Add numeric constraint for single parameter")
        //             onClicked: {
        //                 ExGlobals.Constants.proxy.fitter.addConstraint(
        //                            dependentPar2.currentIndex,
        //                            relationalOperator2.currentText.replace("\uf531", ">").replace("\uf536", "<"),
        //                            value2.text,
        //                            "",
        //                            -1
        //                            )
        //             }
        //         }
        //     }
        // }
        // Type 1 END

        // Type 2 START
        Column {

            EaElements.Label {
                enabled: false
                text: qsTr("Parameter-Parameter Constraints")
            }

            Grid {
                columns: 4
                columnSpacing: EaStyle.Sizes.fontPixelSize * 0.5
                rowSpacing: EaStyle.Sizes.fontPixelSize * 0.5
                verticalItemAlignment: Grid.AlignVCenter

                EaElements.ComboBox {
                    id: dependentPar
                    width: 359
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    // textFormat: ExGlobals.Variables.iconifiedNames ? Text.RichText : Text.PlainText
                    // elide: Text.ElideMiddle
                    textRole: ExGlobals.Variables.iconifiedNames ? "iconified_label" : "label"
                    model: XmlListModel {
//                        xml: ExGlobals.Constants.proxy.parameter.parametersAsXml
                        query: "/data/item"
//                        XmlRole { name: "label"; query: "label/string()" }
//                        onXmlChanged: dependentParCurrentIndex = dependentPar.currentIndex
                    }
                    onCurrentIndexChanged: {
                        //print(currentText)
                        if (dependentPar.currentIndex === -1 && model.count > 0)
                            dependentPar.currentIndex = dependentParCurrentIndex
                    }
                }

                EaElements.ComboBox {
                    id: relationalOperator
                    width: 47
                    currentIndex: 0
                    font.family: EaStyle.Fonts.iconsFamily
                    //model: ["=", ">", "<"]
                    model: XmlListModel {
 //                       xml: "<root><item><operator>=</operator><icon>\uf52c</icon></item><item><operator>&gt;</operator><icon>\uf531</icon></item><item><operator>&lt;</operator><icon>\uf536</icon></item></root>"
                        query: "/root/item"
//                        XmlRole { name: "icon"; query: "icon/string()" }
                    }
                }

                Item { height: 1; width: 1 }
                Item { height: 1; width: 1 }

                EaElements.ComboBox {
                    id: independentPar
                    width: dependentPar.width
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Select parameter" : currentText
                    // textFormat: ExGlobals.Variables.iconifiedNames ? Text.RichText : Text.PlainText
                    // elide: Text.ElideMiddle
                    textRole: ExGlobals.Variables.iconifiedNames ? "iconified_label" : "label"
                    model: XmlListModel {
//                        xml: ExGlobals.Constants.proxy.parameter.parametersAsXml
                        query: "/data/item"
//                        XmlRole { name: "label"; query: "label/string()" }
                        // XmlRole { name: "iconified_label"; query: "iconified_label_with_index/string()" }
//                        onXmlChanged: independentParCurrentIndex = independentPar.currentIndex
                    }
                    onCurrentIndexChanged: {
                        if (independentPar.currentIndex === -1 && model.count > 0)
                            independentPar.currentIndex = independentParCurrentIndex
                    }
                }

                EaElements.ComboBox {
                    id: arithmeticOperator
                    width: relationalOperator.width
                    currentIndex: 0
                    font.family: EaStyle.Fonts.iconsFamily
                    //model: ["", "*", "/", "+", "-"]
                    //model: ["\uf00d", "\uf529", "\uf067", "\uf068"]
                    model: XmlListModel {
//                        xml: "<root><item><operator>*</operator><icon>\uf00d</icon></item><item><operator>/</operator><icon>\uf529</icon></item><item><operator>+</operator><icon>\uf067</icon></item><item><operator>-</operator><icon>\uf068</icon></item></root>"
                        query: "/root/item"
//                        XmlRole { name: "icon"; query: "icon/string()" }
                    }
                }

                EaElements.TextField {
                    id: value
                    width: 65
                    horizontalAlignment: Text.AlignRight
                    text: "1.0000"
                }

                EaElements.SideBarButton {
                    id: addConstraint
                    width: 35
                    fontIcon: "plus-circle"
                    ToolTip.text: qsTr("Add constraint between two parameters")
                    onClicked: {
                        ExGlobals.Constants.proxy.parameter.addConstraint(
                                    dependentPar.currentIndex,
                                    relationalOperator.currentText.replace("\uf52c", "=").replace("\uf531", ">").replace("\uf536", "<"),
                                    value.text,
                                    arithmeticOperator.currentText.replace("\uf00d", "*").replace("\uf529", "/").replace("\uf067", "+").replace("\uf068", "-"),
                                    independentPar.currentIndex
                                    )
                    }
                }
            }
        }
        // Type 2 END

    }
}
    
