import flet as ft

class Column(ft.Column):
    def add(self, content):
        self.controls.append(content)
        if (len(self.controls) > 0):
            self.visible = True