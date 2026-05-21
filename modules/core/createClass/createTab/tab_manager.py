from engine.package import ASQL

from modules.core.createClass.createTab.class_for_tab import Tab
from modules.core.object.class_.Core_ClassApi import Core_ClassApi

class TabManager:
    async def execute_pending(self, data: Tab):
        if not await self._exist_tab(data):
            await ASQL(data.getSQL())
            Core_ClassApi().register(data.name, data.caption)

    async def _exist_tab(self, data:Tab):
        if x:=Core_ClassApi().findByMnemocode(data.name):
            return x
        else:
            return await ASQL("SELECT * FROM sqlite_sequence WHERE name = ?;", (data.name, ))
    
    async def _exist_collumn(self, data:Tab):
        return await ASQL("SELECT * FROM pragma_table_info(?);", (data.name, ))


TabsManager = TabManager()