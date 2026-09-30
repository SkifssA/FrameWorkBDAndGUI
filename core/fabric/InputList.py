from core.type.Event import SetterEvent
from core.ui.inputs import LineEdit, LookUp

class InputListConstruct:
    def __init__(self, formParent):
        from core.ui.forms.list import List
        self.formParent: List = formParent
        self.loadDataLookUp = {}
        self.dictInput = {
            'check': self._setCheck,
            'lookUp': self._getLookUp,
            'edit': self._getEdit
        }

    def getInput(self, row, col):
        sysName = self.formParent._getSysNameAttrByCol(col)
        setName = f'set{sysName}'
        if hasattr(self.formParent, setName):
            dataAttr = self.formParent.metaInfo['attr'].get(sysName, {})
            value = self._get_value(row, col)
            
            rect = self.formParent.tablet.visualRect(self.formParent.tablet.model().index(row, col))
            self._current_edit_row = row
            self._current_edit_col = col

            self.dictInput[dataAttr.get('edit', 'edit')](sysName, dataAttr, value, rect)

    def _get_value(self, row, col):
        if (x:=self.formParent.tablet.item(row, col)):
            return x.text()
        else:
            if (chk:=self.formParent._getCheckBox(row, col)):
                return chk.getValue()['value']

    def _setCheck(self, sysName, dataAttr, value, rect):
        if (chk:=self.formParent._getCheckBox(self._current_edit_row, self._current_edit_col)):
            chk.setValue(not value)
            self.formParent._set_value_avi(sysName, SetterEvent(chk))

    def _getLookUp(self, sysName, dataAttr, value, rect):
        self._editor = LookUp(dataAttr)

        self._editor.setValue(str(value))
        
        # 4. Позиционируем над ячейкой (через viewport!)
        self._editor.setParent(self.formParent.tablet.viewport())
        self._editor.setGeometry(rect)
        self._editor._editor.showPopup()  # Сразу открываем список!
        self._editor.setFocus()

        self._editor.regSetter(lambda: self._save_combo_edit(self._current_edit_row, self._current_edit_col))

    def _save_combo_edit(self, row, col):
        """Сохраняем выбранное значение комбобокса в ячейку"""
        if hasattr(self, '_editor') and self._editor:
            value = self._editor.getValue()
            new_user_data = value['user_data']
            sysName = self.formParent._getSysNameAttrByCol(col)
            colId = self.formParent.systemName[self.formParent.metaInfo['attr'][sysName].get("attrId")]
            self._set_item_value(row, colId, new_user_data)
            self.formParent._set_value_avi(sysName, SetterEvent(self._editor))

            new_text = value['value']
            self._all_save(row, col, new_text)

    def _getEdit(self, sysName, dataAttr, value, rect):
        self._editor = LineEdit(dataAttr)
        self._editor.setValue(value)

        # Инлайн-редактор в таблице: выделяем акцентной рамкой (токены темы)
        from core.ui.theme import C
        self._editor.setStyleSheet(
            f"background: {C.CARD}; border: 1px solid {C.ACCENT}; border-radius: 6px; padding: 2px;"
        )
        
        self._editor.setGeometry(rect)
        self._editor.setParent(self.formParent.tablet.viewport())  # Важно! viewport, не сама таблица
        self._editor.show()
        self._editor._editor.setFocus()
        self._editor._editor.selectAll()
        self._editor.setFocus()

        self._editor.regSetter(lambda *a: self._save_edit(self._current_edit_row, self._current_edit_col))

    def _save_edit(self, row, col):
        """Сохраняем значение и убираем редактор"""
        if hasattr(self, '_editor') and self._editor:
            sysName = self.formParent._getSysNameAttrByCol(col)
            new_value = self._editor.getValue()['value']
            self.formParent._set_value_avi(sysName, SetterEvent(self._editor))

            self._all_save(row, col, new_value)

    def _all_save(self, row, col, new_value):
        self._set_item_value(row, col, new_value)
        
        self._editor.deleteLater()
        self._editor = None
        self._current_edit_row = None
        self._current_edit_col = None

    def _set_item_value(self, row, col, new_value):
        item = self.formParent.tablet.item(row, col)
        if item:
            item.setText(str(new_value))
