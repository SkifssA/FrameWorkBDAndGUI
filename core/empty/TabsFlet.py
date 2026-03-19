import flet as ft

class Tabs(ft.Tabs):
    def init2(self, tab_bar:ft.TabBar, tab_view:ft.TabBarView):
        self.tab_view = tab_view
        self.tab_bar = tab_bar
        self.ch = {}

    def add(self, tabBar:ft.Tab, tabView):
        if self.ch.get(tabBar.data['name'], None) is None:
            self.ch[tabBar.data['name']] = len(self.tab_bar.tabs)
            self.tab_bar.tabs.append(tabBar)
            self.tab_view.controls.append(tabView)
            self.length = len(self.tab_bar.tabs)
            if (self.length > 0 and not self.visible):
                self.visible = True
        self.selected_index = self.ch[tabBar.data['name']]

    def popByName(self, name:str):
        self.popByIndex(self.ch.get(name, None))

    def popByIndex(self, index:int):
        if index is not None:
            self.tab_bar.tabs.pop(index)
            self.tab_view.controls.pop(index)
            self.length = len(self.tab_bar.tabs)
            self.ch = {i.data['name']: x for x, i in enumerate(self.tab_bar.tabs)}
            if (self.length < 1 and self.visible):
                self.length = 1
                self.selected_index = 0
                self.visible = False
            else:
                self.selected_index = 0