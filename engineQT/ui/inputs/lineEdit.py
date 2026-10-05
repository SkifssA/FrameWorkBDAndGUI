from PyQt6.QtWidgets import QLineEdit, QApplication
from PyQt6.QtCore import Qt, QEvent, QObject
from engineQT.ui.inputs.base import Base

class LineEdit(Base):        
    def createInput(self):
        self._editor = QLineEdit()
        self._editor.setFrame(False)
        self._app_filter = None

    def regSetter(self, fun):
        from engineQT.ui.forms.card import Card
        self.fun = fun

        if self._app_filter is None and isinstance(self.parent(), Card):
            self._app_filter = ClickFocusFilter(self._editor, fun)
            QApplication.instance().installEventFilter(self._app_filter)

        self._editor.editingFinished.connect(lambda *a: fun())

    def setValue(self, value:str):
        if value:
            self._editor.setText(str(value))

    def getValue(self):
        return {
            'value': self._editor.text()
            , 'user_data': None
        }

    def active(self, value, viewport):
        super().active(value, viewport)
        from core.ui.theme import C
        self.setStyleSheet(
            f"background: {C.CARD}; border: 1px solid {C.ACCENT}; border-radius: 6px; padding: 2px;"
        )
        
        self.show()
        self._editor.selectAll()


class ClickFocusFilter(QObject):
    """Глобальный фильтр для снятия фокуса при клике вне виджета"""
    
    def __init__(self, target_widget, callback):
        super().__init__()
        self._target = target_widget
        self._callback = callback
        self._was_editing = False
        
        # Отслеживаем, когда виджет получает фокус
        self._target.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        # Отслеживаем фокус на целевом виджете
        if obj == self._target:
            if event.type() == QEvent.Type.FocusIn:
                self._was_editing = True
            elif event.type() == QEvent.Type.FocusOut:
                if self._was_editing and self._callback:
                    self._callback()
                self._was_editing = False
        
        # Перехватываем все клики мыши в приложении
        if event.type() == QEvent.Type.MouseButtonPress:
            if self._target.hasFocus():
                # Проверяем, был ли клик по самому виджету или его детям
                widget_under_click = QApplication.widgetAt(event.globalPosition().toPoint())
                
                # Если клик НЕ по нашему виджету и его дочерним элементам
                if widget_under_click != self._target and not self._target.isAncestorOf(widget_under_click):
                    self._target.clearFocus()
                    # Фокус снимется, сработает FocusOut → вызовется callback
        
        return False  # Не блокируем события