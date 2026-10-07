from core.DB.Turso import ASQL
from core.dataClass.tabDataClass import tabShema

SERVICE_COLUMNS = ('id', 'gid', 'sHeadLine', 'sMnemoCode')


class TabManager:
    """Менеджер накатки схем таблиц (DDL из *.odb.json).

    Вход/выход — dataclass tabShema из core.fabric.dataClass.tabDataClass.
    """

    async def execute_pending(self, data: tabShema):
        if not await self._exist_tab(data):
            await data.execute_pending()
        elif x := (await self._exist_collumn(data)):
            lAttrInDB = list(i['name'] for i in x['data'] if i['name'] not in SERVICE_COLUMNS)
            lAttrInOdb = list(i.name for i in data.attr)
            if (lAttrInDB != lAttrInOdb):
                min = lAttrInDB if len(lAttrInDB) < len(lAttrInOdb) else lAttrInOdb
                data.isNew = True
                data.minListAttr = min
                await data.execute_pending()

    async def _exist_tab(self, data: tabShema):
        return await ASQL("SELECT * FROM sqlite_sequence WHERE name = ?;", (data.name, ))

    async def _exist_collumn(self, data: tabShema):
        return await ASQL("SELECT * FROM pragma_table_info(?);", (data.name, ))


TabsManager = TabManager()