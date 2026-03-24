import flet as ft

from .FormFlet import BaseForm
from core.package.Core_ImageManagerPkg import Core_ImageManagerPkg
from core.package.Core_AsynRunPkg import asyncRun
from core.Core_Store import store



class CardFileView(BaseForm):
    async def onRefreshExt(self):
        return ''
    
    async def _getAttr(self):
        return ''

    def _refresh(self, isUpdate:bool=True):
        self.__uploadFile()
        if isUpdate: store.page.update()

    def __uploadFile(self):
        self.visibleMainForm(False)
        self.img.src = asyncRun(Core_ImageManagerPkg().loadFile(asyncRun(self.onRefresh())))
        self.visibleMainForm(True)
        
    def visibleMainForm(self, value:bool):
        self.img.visible = value
        self.loadInd.visible = not value
        store.page.update()

    def createMainForm(self):
        self.loadInd = ft.CupertinoActivityIndicator(expand=True, radius=50, color=ft.Colors.RED_400, animating=True)
        self.img = ft.Image(src=None, expand=True, visible=False)
        return ft.Column(controls=[
            ft.Container(content=self.loadInd, expand=True)
            , ft.Container(content=self.img, expand=True)
            ]
            , alignment=ft.MainAxisAlignment.CENTER           # <--- Центр по вертикали
            , horizontal_alignment=ft.MainAxisAlignment.CENTER)