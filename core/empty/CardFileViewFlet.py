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
        self.mainForm.src = asyncRun(Core_ImageManagerPkg().loadFile(asyncRun(self.onRefresh())))
        if isUpdate: store.page.update()

    def createMainForm(self):
        return ft.Image(src=None, expand=True)