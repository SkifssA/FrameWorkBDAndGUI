from core.type.Event import SetterEvent
from core.ui.inputs import inputType, Base as BaseInput

class InputListConstruct:
    def __init__(self, formParent):
        from core.ui.forms.list import List
        self.formParent: List = formParent
        self.loadDataLookUp = {}

    def getInput(self, row, col):
        sysName = self.formParent._getSysNameAttrByCol(col)
        setName = f'set{sysName}'
        if hasattr(self.formParent, setName):
            dataAttr = self.formParent.metaInfo['attr'].get(sysName, {})
            value = self._get_value(row, col)
            
            rect = self.formParent.tablet.visualRect(self.formParent.tablet.model().index(row, col))
            self._current_edit_row = row
            self._current_edit_col = col
            self._sysName = self._get_sysName()    

            self._editor = inputType[dataAttr.get('edit', 'edit')](dataAttr)
            self._editor.active(value, rect, self.formParent.tablet.viewport())
            self._editor.regSetter(lambda: self._all_save())

    def _get_value(self, row, col):
        if (x:=self.formParent.tablet.item(row, col)):
            return x.text()
        elif (chk:=self.formParent._getCheckBox(row, col)):
                return chk.getValue()['value']

    def _get_sysName(self):
        if x:= self.formParent.metaInfo['attr'][self.formParent._getSysNameAttrByCol(self._current_edit_col)].get("attrId"):
            return x
        return self.formParent._getSysNameAttrByCol(self._current_edit_col)

    def _all_save(self):
        if isinstance(self._editor, LookUp):
             self.formParent._setAttr(self.formParent._getSysNameAttrByCol(self._current_edit_col), self._editor.getValue()['user_data'])

        self.formParent._setAttr(self._sysName, self._editor.getValue()['value'])
        self.formParent._set_value_avi(self._sysName, SetterEvent(self._editor))
        
        self._editor.deleteLater()

