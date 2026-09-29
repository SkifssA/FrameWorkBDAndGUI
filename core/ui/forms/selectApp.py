from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QScrollArea, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal

# Импорты твоих утилит остаются прежними
from core import ACTIONDISPATCHER
from core.package.FileManager import FileManagerPkg
from core.package.AsynRun import asyncRun
from core.ui.theme import Fonts


class AppCard(QFrame):
    """
    Визуальный блок (карточка) приложения.
    Отвечает только за внешний вид и сигнал «открыть».
    Никаких обращений к родительским окнам — только Qt-сигналы.

    Стилизация — через objectName-селекторы #AppCard/#AppCardTitle/...
    из глобальной темы (core/ui/theme.py). Локальных цветов здесь нет.
    """
    openRequested = pyqtSignal(dict)

    def __init__(self, data):
        super().__init__()
        self.data = data

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setObjectName("AppCard")  # стилизуется GLOBAL_QSS

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 1. Левая часть: название и описание
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        title_label = QLabel(data['name'])
        title_label.setFont(Fonts.H2)
        title_label.setObjectName("AppCardTitle")

        desc_text = data.get('description', 'Модуль системы')
        desc_label = QLabel(desc_text)
        desc_label.setFont(Fonts.MUTED)
        desc_label.setObjectName("AppCardDesc")

        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)

        # 2. Правая часть: кнопка
        btn_open = QPushButton("Открыть")
        btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open.setFixedSize(100, 36)
        btn_open.setObjectName("OpenButton")

        # Карточка не знает о главном окне — она только испускает сигнал.
        btn_open.clicked.connect(lambda checked, d=data: self.openRequested.emit(d))

        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(btn_open)


class SelectApp(QWidget):
    """Экран выбора модулей. Внешний вид — из глобальной темы."""

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Шапка страницы
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(40, 36, 40, 12)
        header_layout.setSpacing(6)

        title = QLabel("Доступные модули")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Выберите модуль для работы")
        subtitle.setObjectName("PageSubtitle")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск модуля…")
        self.search.setObjectName("SearchBox")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self._filterCards)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addSpacing(8)
        header_layout.addWidget(self.search)
        root.addWidget(header)

        # Прокручиваемый список карточек
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.apps_container = QVBoxLayout(container)
        self.apps_container.setContentsMargins(40, 12, 40, 40)
        self.apps_container.setSpacing(12)
        self.apps_container.addStretch()  # список прижат к верху

        scroll.setWidget(container)
        root.addWidget(scroll, stretch=1)

        self._cards: list[AppCard] = []

        # --- ЛОГИКА ЗАГРУЗКИ ---
        listApp = asyncRun(FileManagerPkg.ReadFile("project.yaml"))

        for app in listApp['modules']:
            if asyncRun(FileManagerPkg.Exists(f"module/{app}/config/app.json")):
                data = asyncRun(FileManagerPkg.ReadFile(f"module/{app}/config/app.json"))
                if (data.get('name', None) is not None):
                    card = AppCard(data)
                    # Единая точка навигации: карточка ничего не знает об окне,
                    # переключением центрального виджета занимается этот экран.
                    card.openRequested.connect(self._openModule)
                    self.apps_container.addWidget(card)
                    self._cards.append(card)

    # ------------------------------------------------------------------
    # Фильтр карточек по тексту поиска
    # ------------------------------------------------------------------
    def _filterCards(self, text: str):
        needle = text.strip().lower()
        for card in self._cards:
            name = card.data.get('name', '').lower()
            desc = card.data.get('description', '').lower()
            card.setVisible((not needle) or needle in name or needle in desc)

    def _openModule(self, data):
        """Открывает главное меню модуля и делает его центральным виджетом окна."""
        from core.fabric.Form import FormConstruct
        mainWin = self.window()
        self.mainMenu = self.openMainMenuModule(data)
        FormConstruct.mainMenu = self.mainMenu
        mainWin.setCentralWidget(self.mainMenu)

    def openMainMenuModule(self, data):
        module_name = f"{data['nameMainScreen']}Avi.Default"
        return ACTIONDISPATCHER.action(module_name, kattr={'mainWin': self.window()})
