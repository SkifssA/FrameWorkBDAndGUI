from engine.package import ASQL

from modules.core.createClass.createTab.class_for_tab import Tab
from modules.core.object.class_.Core_ClassApi import Core_ClassApi

class TabManager:
    async def execute_pending(self, data: Tab):
        if not await self._exist_tab(data):              
            data.execute_pending()
            Core_ClassApi().register(data.name, data.caption)
        elif x:=(await self._exist_collumn(data)):
            lAttrInDB = list(i['name'] for i in x if not i['name'] in ('id', 'gid', 'sHeadLine', 'sMnemoCode'))
            lAttrInOdb = list(i.name for i in data.attr)
            if (lAttrInDB != lAttrInOdb):
                min = lAttrInDB if len(lAttrInDB) < len(lAttrInOdb) else lAttrInOdb
                data.isNew(min)
                data.execute_pending()

    async def _exist_tab(self, data:Tab):
        if x:=Core_ClassApi().findByMnemocode(data.name):
            return x
        else:
            return await ASQL("SELECT * FROM sqlite_sequence WHERE name = ?;", (data.name, ))
    
    async def _exist_collumn(self, data:Tab):
        return await ASQL("SELECT * FROM pragma_table_info(?);", (data.name, ))


TabsManager = TabManager()