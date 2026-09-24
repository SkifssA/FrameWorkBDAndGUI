from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Импорты твоих утилит остаются прежними
from core.package.ActionDispatcher import ActionDispatcherPkg
from core.package.FileManager import FileManagerPkg
from core.package.AsynRun import asyncRun 

class AppCard(QFrame):
    """
    Визуальный блок (карточка) приложения.
    Отвечает только за внешний вид.
    """
    def __init__(self, data, parent_widget):
        super().__init__()
        self.data = data
        
        # Настройка внешнего вида карточки
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setObjectName("AppCard") # Для CSS стилизации
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 1. Левая часть: Название и описание (если есть)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        title_label = QLabel(data['name'])
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")
        
        # Если в json есть description, покажем его серым цветом
        desc_text = data.get('description', 'Модуль системы')
        desc_label = QLabel(desc_text)
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setStyleSheet("color: #AAAAAA;")
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)
        
        # 2. Правая часть: Кнопка
        btn_open = QPushButton("Открыть")
        btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open.setFixedSize(100, 36)
        btn_open.setObjectName("OpenButton")
        
        # Связываем клик с логикой родителя (как было раньше)
        # Используем lambda, чтобы передать данные именно этого блока
        btn_open.clicked.connect(lambda checked, d=data: parent_widget.parent().setCentralWidget(parent_widget.openMainMenuModule(d)))

        layout.addLayout(info_layout)
        layout.addStretch() # Растягиваем пространство, чтобы кнопка прижалась вправо
        layout.addWidget(btn_open)

    # Метод для применения стилей (можно вынести в общий CSS)
    def get_stylesheet():
        return """
            #AppCard {
                background-color: #2B2B2B;
                border: 1px solid #3E3E3E;
                border-radius: 8px;
            }
            #AppCard:hover {
                border: 1px solid #5A5A5A;
                background-color: #323232;
            }
            #OpenButton {
                background-color: #3700B3; /* Акцентный цвет (фиолетовый/синий) */
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            #OpenButton:hover {
                background-color: #6200EE;
            }
            #OpenButton:pressed {
                background-color: #2a008a;
            }
        """


class SelectApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Основной вертикальный лейаут
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40) # Большие отступы по краям
        main_layout.setSpacing(15) # Расстояние между карточками

        # Заголовок страницы
        header_label = QLabel("Доступные модули")
        header_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Light))
        header_label.setStyleSheet("color: #E0E0E0; margin-bottom: 10px;")
        main_layout.addWidget(header_label)

        # Контейнер для списка приложений (чтобы они шли друг за другом красиво)
        self.apps_container = QVBoxLayout()
        self.apps_container.setSpacing(12)
        
        main_layout.addLayout(self.apps_container)
        main_layout.addStretch() # Чтобы список прижался к верху, если приложений мало

        # --- ЛОГИКА ЗАГРУЗКИ (БЕЗ ИЗМЕНЕНИЙ) ---
        listApp = asyncRun(FileManagerPkg.ReadFile("../../project.yaml"))
        
        for app in listApp['modules']:
            if asyncRun(FileManagerPkg.Exists(f"../../module/{app}/config/app.json")):
                data = asyncRun(FileManagerPkg.ReadFile(f"../../module/{app}/config/app.json"))
                if (data.get('name', None) is not None):
                    # Создаем красивую карточку вместо старого createBlocApp
                    card = AppCard(data, self)
                    self.apps_container.addWidget(card)

        # Применяем стили ко всем карточкам сразу (или можно внутри AppCard)
        self.setStyleSheet(AppCard.get_stylesheet())

    # Твоя оригинальная функция открытия (не тронута)
    def openMainMenuModule(self, data):
        module_name = f"{data['nameMainScreen']}Avi.Default"
        return ActionDispatcherPkg().action(module_name, kattr={'mainWin': self.parent()})