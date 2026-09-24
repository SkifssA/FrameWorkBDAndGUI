import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, 
    QLineEdit, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

class AddItemDialog(QDialog):
    """Модальное окно для ввода данных"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        self.setFixedSize(300, 150)
        
        # Создаем элементы интерфейса
        layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Отмена")
        
        # Подключаем сигналы
        self.ok_btn.clicked.connect(self.accept_data)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Хранилище для результата
        self.result_name = ""

    def accept_data(self):
        """Проверяем данные и закрываем окно с кодом Accepted"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым!")
            return
            
        self.result_name = name
        self.accept() # Закрываем окно и возвращаем QDialog.DialogCode.Accepted

    def get_name(self):
        return self.result_name


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример с модальным окном")
        self.setGeometry(100, 100, 600, 400)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Таблица для отображения данных
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Имя"])
        main_layout.addWidget(self.table)
        
        # Кнопка добавления
        add_btn = QPushButton("Добавить запись")
        add_btn.clicked.connect(self.open_add_dialog)
        main_layout.addWidget(add_btn)
        
        self.current_id = 1

    def open_add_dialog(self):
        """Открывает модальное окно и обрабатывает результат"""
        dialog = AddItemDialog()
        
        # exec() блокирует выполнение до закрытия окна
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_name()
            self.add_row_to_table(name)
            
    def add_row_to_table(self, name):
        """Добавляет новую строку в таблицу"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(self.current_id)))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.current_id += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())