"""Базовый класс формы приложения.

Ответственности слоя (шаблон Template Method):
- Base строит «каркас» формы: тулбар, сплиттер, дочерние группы форм.
- Наследники реализуют только «хуки»: onRefresh / _createMainFrameWidget / getChilders.

Правила, которые здесь соблюдаются:
1. Никаких дублей объявлений хуков — каждый хук объявлен ровно один раз.
2. Порядок инициализации фиксирован: kwargs -> инфраструктура -> каркас UI.
3. Состояние дочерних групп хранится локально (не в магических словарях),
   общение с наследниками идёт через явно объявленные хуки.
"""

from typing import Any, Optional, TypedDict

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter

from core import Metadata
from core.package.Rect import Rect
from core.ui.widget.menubar import OperUIBuilder, OperRegistry
from core.ui.widget.groupForm import GroupForm
from core.type.Event import SetterEvent

LEFT = 'left'
RIGHT = 'right'


class Config(TypedDict, total=False):
    """Параметры, которые можно передать форме через FormConstruct.param()."""
    locat: str
    isUpdate: bool
    isCh: bool


class Base(QWidget):
    """Каркас всех форм модулей."""

    #: показывать ли тулбар формы (наследники могут отключить классовым флагом)
    IsToolBar = True

    def __init__(self, **kwargs):
        super().__init__()

        # 1. Внешние параметры (Config и всё, что передал модуль).
        for key, value in kwargs.items():
            setattr(self, key, value)

        # 2. Инфраструктура формы.
        self.registry = OperRegistry()
        self.oper = OperUIBuilder(self.registry)
        self.metaInfo = Metadata.get(self)
        self.Rect = Rect(self)
        self.formParent = None
        self.caption = self.metaInfo.get('caption', 'НАЗВАНИЯ НЕТ')
        self.toolbar = None

        # 3. Каркас UI.
        layout = QVBoxLayout(self)
        if self.IsToolBar and self.metaInfo.get('isVisibleToolBar', True):
            self._refreshToolBar()
            layout.addWidget(self.toolbar)
        else:
            self.registry.register(self)

        splitter = QSplitter(self)
        # У QSplitter нет setHandleSize — ширина «ручек» задаётся через QSS
        # (в теме: QSplitter::handle { background/min-size }), поэтому здесь
        # только отключаем схлопывание дочерних панелей.
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)

        children = {LEFT: [], RIGHT: []}
        for childer in self.getChilders() or []:
            # form.open() мутирует конструктор (clsForm заменяется экземпляром),
            # поэтому locat читаем ДО открытия.
            children[childer.locat].append(childer)

        self._addChildrenGroup(children[LEFT], splitter)
        splitter.addWidget(self._createMainFrameWidget())
        self._addChildrenGroup(children[RIGHT], splitter)

    # ------------------------------------------------------------------
    # Публичное API
    # ------------------------------------------------------------------

    def getForOpen(self) -> tuple['Base', str]:
        """Что вернуть родителю (главному окну) для вставки формы во вкладку."""
        return (self, self.caption)

    # ------------------------------------------------------------------
    # Хуки для наследников (переопределяются, но не вызываются снаружи)
    # ------------------------------------------------------------------

    def getChilders(self) -> list:
        """Дочерние формы-конструкторы, расставляемые по краям сплиттера."""
        return []

    def onRefresh(self):
        """Источник данных формы (используется Rect.refresh())."""
        return {}

    def _createMainFrameWidget(self) -> QWidget:
        raise NotImplementedError

    def _onRefresh(self):
        pass

    def _getAttr(self, sysName: str) -> Optional[Any]:
        return None

    def checwork(self):
        """Хук актуализации состояния тулбара/кнопок после изменений."""
        pass

    # ------------------------------------------------------------------
    # Внутренние механизмы
    # ------------------------------------------------------------------

    def _addChildrenGroup(self, forms: list, splitter: QSplitter) -> None:
        """Создаёт GroupForm из дочерних форм и добавляет её в сплиттер.

        Формы, у которых задан callback, не встраиваются как панели — они
        открываются один раз сразу после сборки каркаса (например, модалка).
        """
        plain = [f for f in forms if getattr(f, 'callback', None) is None]
        deferred = [f for f in forms if getattr(f, 'callback', None) is not None]
        if plain:
            group = GroupForm(self)
            group.setObjectName("SidePanel")  # боковая панель стилизуется темой
            splitter.addWidget(group)
            for form in plain:
                child = form.open()
                child.formParent = self
                group.addWidget(child)
        for form in deferred:
            result = form.open()
            if result is not None and hasattr(result, 'formParent'):
                result.formParent = self
            form.callback(result)

    def refreshCh(self):
        """Обновляет все дочерние группы форм."""
        for group in self.findChildren(GroupForm):
            group.refreshCh()

    def _set_value_avi(self, attrName: str, setter: SetterEvent) -> None:
        """Вызывает сеттер атрибута `set<attrName>`, если он определён."""
        setName = f'set{attrName}'
        if hasattr(self, setName):
            getattr(self, setName)(setter)

    def _refreshToolBar(self) -> None:
        self.registry.register(self)
        self.toolbar = self.oper.build_toolbar(self.toolbar)
