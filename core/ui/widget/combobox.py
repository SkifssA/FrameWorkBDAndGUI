from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QLabel

class ComboBox(QComboBox):
    def __init__(self, parent = ...):
        super().__init__(parent)
        self.dictHlAndId = {}

    def addItemByData(self, data):
        for i in data['data']:
            self.dictHlAndId[i['id']] = i['sHeadLine']
