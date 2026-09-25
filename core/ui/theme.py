"""Единая дизайн-система NecoTab.

Здесь живут ВСЕ визуальные токены (цвета, шрифты, отступы) и глобальная QSS-тема.
Формы не хранят свои цвета — они либо полагаются на apply_theme(app),
либо используют object-name + селекторы из GLOBAL_QSS, либо берут значения
из C / FONTS напрямую.

Правила:
1. Никаких hex-цветов внутри файлов форм — только константы отсюда.
2. Кастомные виджеты помечаются setObjectName(...) и стилизуются в GLOBAL_QSS.
3. Сменить палитру = поменять словарь C (и, при желании, добавить light-версию).
"""



from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QApplication

# Встроенная галочка для checked-состояния чекбоксов.
# 18x18 RGBA PNG (белая галка на прозрачном фоне), зашит как data-URI:
# не нужен внешний файл, и Qt гарантированно рендерит PNG в QSS (с SVG из
# data-URI внутри stylesheet есть проблемы).
_CHECK_PNG_B64 = ("iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAANElEQVR42mNgGAU0A/"
                  "8BgCqGwMDgMYRsg0gyBJ9CklyCy1ayvPMfD6A4PAY+htANG+GZGAC4N7dJs027/AAAAA"
                  "BJRU5ErkJggg==")
CHECK_ICON_URI = "data:image/png;base64," + _CHECK_PNG_B64


class C:
    """Палитра «Midnight Slate»."""
    BG        = "#0F1220"   # фон окна
    SURFACE   = "#171B2E"   # панели, тулбары, сайдбары
    CARD      = "#1D2238"   # карточки, таблицы, поля ввода
    CARD_HOV  = "#242A47"   # hover карточек/строк
    BORDER    = "#2A3050"   # обводки
    BORDER_HV = "#3D4675"   # обводка в hover/focus

    TEXT      = "#E8EAF6"   # основной текст
    MUTED     = "#9AA3C7"   # вторичный текст
    FAINT     = "#6B7399"   # подписи, placeholder

    ACCENT    = "#6C7BF0"   # основной акцент (indigo)
    ACCENT_HV = "#8291FF"
    ACCENT_PR = "#5560C9"
    ON_ACCENT = "#FFFFFF"

    SUCCESS   = "#3DDC97"
    WARNING   = "#FFB74D"
    DANGER    = "#FF6B6B"

    SEL       = "#2B3466"   # выделение строк/опций
    SCROLL    = "#39406B"
    TOOLTIP_BG = "#232A4A"


class Fonts:
    FAMILY = "Segoe UI"
    H1 = QFont(FAMILY, 20, QFont.Weight.Bold)
    H2 = QFont(FAMILY, 13, QFont.Weight.DemiBold)
    BODY = QFont(FAMILY, 10)
    MUTED = QFont(FAMILY, 9)
    BTN = QFont(FAMILY, 10, QFont.Weight.DemiBold)


# ---------------------------------------------------------------------------
# Глобальная тема: покрывает все стандартные Qt-виджеты приложения.
# Вызывается один раз в mainProgram() ДО создания окон.
# ---------------------------------------------------------------------------
GLOBAL_QSS = f"""
QWidget {{
    background-color: {C.BG};
    color: {C.TEXT};
    font-family: "{Fonts.FAMILY}";
    font-size: 10pt;
}}
QMainWindow, QDialog {{ background-color: {C.BG}; }}

/* ---------- базовая типографика ---------- */
QLabel {{ background: transparent; }}
QLabel[role="h1"] {{ font-size: 20pt; font-weight: 700; }}
QLabel[role="h2"] {{ font-size: 13pt; font-weight: 600; }}
QLabel[role="muted"] {{ color: {C.MUTED}; font-size: 9pt; }}

/* ---------- кнопки ---------- */
QPushButton {{
    background-color: {C.CARD};
    color: {C.TEXT};
    border: 1px solid {C.BORDER};
    border-radius: 8px;
    padding: 7px 14px;
    font-weight: 600;
}}
QPushButton:hover {{ background-color: {C.CARD_HOV}; border-color: {C.BORDER_HV}; }}
QPushButton:pressed {{ background-color: {C.BG}; }}
QPushButton:disabled {{ color: {C.FAINT}; border-color: {C.BG}; }}
QPushButton[role="accent"] {{
    background-color: {C.ACCENT}; color: {C.ON_ACCENT}; border: none;
}}
QPushButton[role="accent"]:hover {{ background-color: {C.ACCENT_HV}; }}
QPushButton[role="accent"]:pressed {{ background-color: {C.ACCENT_PR}; }}

/* ---------- поля ввода ---------- */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background-color: {C.CARD};
    border: 1px solid {C.BORDER};
    border-radius: 8px;
    padding: 6px 10px;
    selection-background-color: {C.ACCENT};
}}
QLineEdit:focus, QComboBox:focus {{ border-color: {C.ACCENT}; }}
QLineEdit:disabled, QComboBox:disabled {{ color: {C.FAINT}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    background-color: {C.CARD};
    border: 1px solid {C.BORDER};
    selection-background-color: {C.SEL};
    outline: none;
}}
QTextEdit, QPlainTextEdit {{
    background-color: {C.CARD};
    border: 1px solid {C.BORDER};
    border-radius: 8px;
    padding: 6px;
}}

/* ---------- чекбоксы ---------- */
QCheckBox {{ background: transparent; spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border-radius: 5px;
    border: 1px solid {C.BORDER_HV};
    background-color: {C.BG};
}}
QCheckBox::indicator:hover {{ border-color: {C.ACCENT}; }}
QCheckBox::indicator:checked {{
    background-color: {C.ACCENT};
    border-color: {C.ACCENT};
    image: url({CHECK_ICON_URI});
}}

/* ---------- таблицы ---------- */
QTableWidget, QTableView {{
    background-color: {C.CARD};
    alternate-background-color: {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    gridline-color: transparent;
    selection-background-color: {C.SEL};
    selection-color: {C.TEXT};
}}
QTableWidget::item, QTableView::item {{
    padding: 6px 8px;
    border: none;
}}
QTableWidget::item:selected {{ background-color: {C.SEL}; }}
QHeaderView::section {{
    background-color: {C.SURFACE};
    color: {C.MUTED};
    border: none;
    border-bottom: 2px solid {C.BORDER};
    padding: 8px;
    font-weight: 600;
}}
QTableCornerButton::section {{ background-color: {C.SURFACE}; border: none; }}

/* ---------- вкладки ---------- */
QTabWidget::pane {{ border: 1px solid {C.BORDER}; border-radius: 10px; top: -1px; }}
QTabBar::tab {{
    background: transparent;
    color: {C.MUTED};
    border: none;
    padding: 8px 16px;
    margin-right: 4px;
    border-bottom: 2px solid transparent;
    font-weight: 600;
}}
QTabBar::tab:hover {{ color: {C.TEXT}; }}
QTabBar::tab:selected {{ color: {C.ACCENT_HV}; border-bottom: 2px solid {C.ACCENT}; }}

/* ---------- группы / сплиттеры ---------- */
QGroupBox {{
    background-color: {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 8px;
    font-weight: 600;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; color: {C.MUTED}; }}
QSplitter::handle {{ background-color: {C.BORDER}; width: 6px; height: 6px; border-radius: 3px; }}
QSplitter::handle:hover {{ background-color: {C.ACCENT}; }}

/* ---------- меню / тулбар ---------- */
QMenuBar {{ background-color: {C.SURFACE}; border-bottom: 1px solid {C.BORDER}; }}
QMenuBar::item {{ background: transparent; padding: 6px 12px; border-radius: 6px; }}
QMenuBar::item:selected {{ background-color: {C.SEL}; }}
QMenu {{ background-color: {C.CARD}; border: 1px solid {C.BORDER}; border-radius: 8px; padding: 4px; }}
QMenu::item {{ background: transparent; padding: 6px 24px 6px 12px; border-radius: 6px; }}
QMenu::item:selected {{ background-color: {C.SEL}; }}
QMenu::separator {{ height: 1px; background: {C.BORDER}; margin: 4px 8px; }}
QToolBar {{
    background-color: {C.SURFACE};
    border-bottom: 1px solid {C.BORDER};
    padding: 4px 8px;
    spacing: 6px;
}}
QToolButton {{
    background-color: transparent;
    color: {C.TEXT};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 6px 10px;
    font-weight: 600;
}}
QToolButton:hover {{ background-color: {C.CARD_HOV}; border-color: {C.BORDER}; }}
QToolButton:pressed {{ background-color: {C.BG}; }}
QToolButton:checked {{ background-color: {C.SEL}; border-color: {C.ACCENT}; }}
QStatusBar {{ background-color: {C.SURFACE}; border-top: 1px solid {C.BORDER}; color: {C.MUTED}; }}

/* ---------- скроллбары ---------- */
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {C.SCROLL}; border-radius: 5px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background: {C.BORDER_HV}; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {C.SCROLL}; border-radius: 5px; min-width: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}

/* ---------- tooltips ---------- */
QToolTip {{
    background-color: {C.TOOLTIP_BG};
    color: {C.TEXT};
    border: 1px solid {C.BORDER_HV};
    border-radius: 6px;
    padding: 4px 8px;
}}

/* ================= кастомные компоненты ================= */

/* Карточка приложения на экране выбора модулей */
#AppCard {{
    background-color: {C.CARD};
    border: 1px solid {C.BORDER};
    border-radius: 12px;
}}
#AppCard:hover {{ border-color: {C.ACCENT}; background-color: {C.CARD_HOV}; }}
#AppCardTitle {{ background: transparent; font-size: 13pt; font-weight: 700; }}
#AppCardDesc  {{ background: transparent; color: {C.MUTED}; }}
#OpenButton {{
    background-color: {C.ACCENT};
    color: {C.ON_ACCENT};
    border: none;
    border-radius: 8px;
    font-weight: 700;
}}
#OpenButton:hover {{ background-color: {C.ACCENT_HV}; }}
#OpenButton:pressed {{ background-color: {C.ACCENT_PR}; }}

/* Экран выбора приложений */
#PageTitle {{ background: transparent; font-size: 20pt; font-weight: 700; }}
#PageSubtitle {{ background: transparent; color: {C.MUTED}; font-size: 10pt; }}
#SearchBox {{
    background-color: {C.CARD};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    padding: 8px 12px;
}}
#SearchBox:focus {{ border-color: {C.ACCENT}; }}

/* Боковые группы форм (GroupForm) */
#SidePanel {{ background-color: {C.SURFACE}; border: 1px solid {C.BORDER}; border-radius: 10px; }}

/* Строка «подпись + поле» в Card-форме */
#FieldRow QLabel {{ background: transparent; color: {C.MUTED}; font-weight: 600; }}
"""


def apply_theme(app: QApplication) -> None:
    """Применяет дизайн-систему ко всему приложению. Вызывать один раз."""
    app.setStyle("Fusion")                       # нейтральный базовый стиль
    app.setPalette(_fusion_palette())
    app.setStyleSheet(GLOBAL_QSS)
    default = QFont(Fonts.FAMILY, 10)
    app.setFont(default)


def _fusion_palette():
    from PyQt6.QtGui import QPalette
    p = QPalette()
    bg, card, text, muted = QColor(C.BG), QColor(C.CARD), QColor(C.TEXT), QColor(C.MUTED)
    p.setColor(QPalette.ColorRole.Window, bg)
    p.setColor(QPalette.ColorRole.WindowText, text)
    p.setColor(QPalette.ColorRole.Base, card)
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(C.SURFACE))
    p.setColor(QPalette.ColorRole.Text, text)
    p.setColor(QPalette.ColorRole.Button, QColor(C.SURFACE))
    p.setColor(QPalette.ColorRole.ButtonText, text)
    p.setColor(QPalette.ColorRole.Highlight, QColor(C.ACCENT))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(C.ON_ACCENT))
    p.setColor(QPalette.ColorRole.ToolTipBase, QColor(C.TOOLTIP_BG))
    p.setColor(QPalette.ColorRole.ToolTipText, text)
    p.setColor(QPalette.ColorRole.PlaceholderText, muted)
    p.setColor(QPalette.ColorRole.Link, QColor(C.ACCENT_HV))
    dis = QColor(C.FAINT)
    for role in (QPalette.ColorRole.WindowText, QPalette.ColorRole.Text,
                 QPalette.ColorRole.ButtonText):
        p.setColor(QPalette.ColorGroup.Disabled, role, dis)
    return p
