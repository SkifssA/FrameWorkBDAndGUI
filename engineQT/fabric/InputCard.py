from engineQT.type.Event import SetterEvent

from engineQT.ui.inputs import inputType, Base as BaseInput, CheckBox
from engineQT.ui.widget.inputandlable import InputandLable 

class InputCardConstruct:
    def __init__(self, formParent):
        from engineQT.ui.forms.card import Card
        self.formParent:Card = formParent
        self._editors:dict[str, BaseInput] = {}
        self._InputandLable:dict[str, InputandLable] = {}

    def getEditor(self, name)->BaseInput:
        return self._editors[name]

    def getNameAllEditor(self):
        return tuple(self._editors.keys())

    def createInput(self, name, value, dataAttr:dict = None):
        data = dataAttr or self.formParent.metaInfo['attr'].get(name, {})
        self._editors[name] = inputType[data.get('edit', 'edit')](data)
        self._editors[name].setEnabled(not data.get('isReadOnly', False) and self.formParent.isReadOnlyForm)
        self._editors[name].setValue(value)
        self._editors[name].setParent(self.formParent)
        self._editors[name].regSetter(lambda: self.formParent._set_value_avi(name, SetterEvent(self._editors[name])))

        self._InputandLable[name] = InputandLable(data.get('caption', name), self._editors[name]) 
        self.formParent._layout.addWidget(self._InputandLable[name])
        self._InputandLable[name].setVisible(data.get('isVisible', True))