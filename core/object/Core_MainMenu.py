import dearpygui.dearpygui as dpg

from ..package import Core_FileManagerPkg, ATQSL
from ..base.BaseOper import SetOper
from ..base.BaseMainMenu import mainMenu
from ..object.clas.Core_ClassAvi import Core_ClassAvi
from ..object.attr.Core_AttrAvi import Core_AttrAvi

class Core_MainMenu(mainMenu):

    @SetOper(label='Классы')
    def mm_class(self): pass

    @SetOper(label='Классы', headOper='mm_class', order=10)
    async def classAvi(self):
        await Core_ClassAvi().List().open()

    @SetOper(label='Атрибуты', headOper='mm_class', order=20)
    async def attrAvi(self):
        await Core_AttrAvi().List().open()