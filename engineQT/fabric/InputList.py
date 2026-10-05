from engineQT.type.Event import SetterEvent

from engineQT.ui.inputs import inputType, LookUp, CheckBox

class InputListConstruct:
    def __init__(self, formParent):
        from engineQT.ui.forms.list import List
        self.formParent: List = formParent
        self.row = None
        self.col = None
        self._editor = None

    def openEditor(self, row, col):
        sysName = self.formParent._getSysNameAttrByCol(col)
        setName = f'set{sysName}'
        isReadOnlyAttr = not self.formParent.metaInfo['attr'][sysName].get('isReadOnly', False)
        
        if hasattr(self.formParent, setName) and isReadOnlyAttr and self.formParent.isReadOnlyForm:
            dataAttr = self.formParent.metaInfo['attr'].get(sysName, {})
            value = self._get_value(row, col)
            
            rect = self.formParent.tablet.visualRect(self.formParent.tablet.model().index(row, col))
            self._current_edit_row = row
            self._current_edit_col = col
            self._sysName = self._refAttrName()    

            self._editor = inputType[dataAttr.get('edit', 'edit')](dataAttr)
            self._editor.setGeometry(rect)
            self._editor.active(value, self.formParent.tablet.viewport())
            self._editor.setFocus()
            if isinstance(self._editor, CheckBox):
                self._saveEditor()
            else:
                self._editor.regSetter(lambda: self._saveEditor())

    def _get_value(self, row, col):
        if (x:=self.formParent.tablet.item(row, col)):
            return x.text()
        elif (chk:=self.formParent._getCheckBox(row, col)):
                return chk.getValue()['value']

    def _refAttrName(self):
        if x:= self.formParent.metaInfo['attr'][self.formParent._getSysNameAttrByCol(self._current_edit_col)].get("attrId"):
            return x
        return self.formParent._getSysNameAttrByCol(self._current_edit_col)

    def _saveEditor(self):
        if isinstance(self._editor, LookUp):
             self.formParent._setAttr(self.formParent._getSysNameAttrByCol(self._current_edit_col), self._editor.getValue()['user_data'])

        self.formParent._setAttr(self._sysName, self._editor.getValue()['value'])
        self.formParent._set_value_avi(self._sysName, SetterEvent(self._editor))
        
        self._editor.deleteLater()

