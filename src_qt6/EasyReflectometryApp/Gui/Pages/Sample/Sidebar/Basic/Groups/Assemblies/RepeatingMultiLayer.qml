

        Row {
            visible: (currentItemsType == 'Repeating Multi-layer') ? true : false
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            // This integer defines how many repetitions of the layer structure should be
            // used.
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                width: labelWidth() * 2.1
                ToolTip.text: qsTr("To create some repeating multilayer structure")
                text: qsTr("Number of repetitions:")
            }
            EaElements.SpinBox {
                id: repsSpinBox
                editable: true
                from: 1
                to: 9999
                value: ExGlobals.Constants.proxy.model.currentItemsRepetitions 
                onValueChanged: {
                    ExGlobals.Constants.proxy.model.currentItemsRepetitions = value
                }
            }
        }