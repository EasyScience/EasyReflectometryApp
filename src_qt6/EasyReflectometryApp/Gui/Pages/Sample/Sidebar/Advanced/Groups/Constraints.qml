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

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * 0.5
        Column {

            EaElements.Label {
                enabled: false
                text: qsTr("Numeric or Parameter-Parameter constraint")
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
                    displayText: currentIndex === -1 ? "Select dependent parameter" : currentText
                    model: Globals.BackendWrapper.sampleParameterNames
                    onCurrentIndexChanged: {
                        independentPar.model = Globals.BackendWrapper.sampleParameterNames
                        independentPar.model[currentIndex] = 'Dependent parameter'
                        independentPar.currentIndex = -1
                    }
                }

                EaElements.ComboBox {
                    id: relationalOperator
                    width: 47
                    currentIndex: 0
                    font.family: EaStyle.Fonts.iconsFamily
                    model: Globals.BackendWrapper.sampleRelationOperators
                }

                Item { height: 1; width: 1 }
                Item { height: 1; width: 1 }

                EaElements.ComboBox {
                    id: independentPar
                    width: dependentPar.width
                    currentIndex: -1
                    displayText: currentIndex === -1 ? "Numeric constrain or select independent parameter" : currentText
                    model: Globals.BackendWrapper.sampleParameterNames
                    onCurrentIndexChanged: {
                        dependentPar.model = Globals.BackendWrapper.sampleParameterNames
                        if (currentIndex === -1){
                            displayText: "Numeric constrain or select independent parameter"
                            arithmeticOperator.model = Globals.BackendWrapper.sampleArithmicOperators.slice(0,1)  // no arithmetic operators
                        }
                        else{
                            arithmeticOperator.model = Globals.BackendWrapper.sampleArithmicOperators.slice(1) // allow all arithmetic operators
                            dependentPar.model[currentIndex] = 'Independent parameter'
                        //arithmeticOperator.currentIndex = 0
                        }
                    }
                }

                EaElements.ComboBox {
                    id: arithmeticOperator
                    width: relationalOperator.width
                    currentIndex: 0
                    font.family: EaStyle.Fonts.iconsFamily
                    model: arithmeticOperator.model = Globals.BackendWrapper.sampleArithmicOperators.slice(0,1)
                }

                EaElements.TextField {
                    id: value
                    width: 65
                    horizontalAlignment: Text.AlignRight
                    text: "1.0000"
                }

                EaElements.SideBarButton {
                    id: addConstraint
                    enabled: ( dependentPar.currentIndex !== -1 && independentPar.currentIndex !== -1 && independentPar.currentIndex !== dependentPar.currentIndex )
                    width: 35
                    fontIcon: "plus-circle"
                    ToolTip.text: qsTr("Add constraint between two parameters")
                    onClicked: {
                        Globals.BackendWrapper.sampleAddConstraint(
                            dependentPar.currentIndex,
                            relationalOperator.currentText.replace("\uf52c", "=").replace("\uf531", ">").replace("\uf536", "<"),
                            value.text,
                            arithmeticOperator.currentText.replace("\uf00d", "*").replace("\uf529", "/").replace("\uf067", "+").replace("\uf068", "-"),
                            independentPar.currentIndex
                        )
                        independentPar.currentIndex = -1
                        dependentPar.currentIndex = -1
                        relationalOperator.currentIndex = 0
                        arithmeticOperator.currentIndex = 0
                    }
                }
            }
        }
    }
}
    
