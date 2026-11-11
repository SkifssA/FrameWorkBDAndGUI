from core.DB import ASQL
from core.dataClass.tabDataClass import tabSchema
from core.module.sc.object.cls.Sc_ClsLogic import Sc_ClsLogic

SERVICE_COLUMNS = ("id", "sHeadLine", "sMnemoCode", "gid")


class TabManager:
    """Менеджер накатки схем таблиц (DDL из *.odb.json).

    Вход/выход — dataclass tabSchema из core.fabric.dataClass.tabDataClass.
    """

    def execute_pending(self, data: tabSchema):
        if not self._exist_tab(data):
            data.execute_pending()
        elif x := (self._exist_collumn(data)):
            lAttrInDB = list(
                i["name"] for i in x["data"] if i["name"] not in SERVICE_COLUMNS
            )
            lAttrInOdb = list(i.name for i in data.attr)
            if lAttrInDB != lAttrInOdb:
                min = lAttrInDB if len(lAttrInDB) < len(lAttrInOdb) else lAttrInOdb
                data.isNew = True
                data.minListAttr = min
                data.execute_pending()

        Sc_ClsLogic().register(data.name, data.caption)

    def _exist_tab(self, data: tabSchema):
        return ASQL("SELECT name FROM sqlite_master WHERE type='table' AND name = ?;", (data.name,))['data'] != []

    def _exist_collumn(self, data: tabSchema):
        return ASQL("SELECT * FROM pragma_table_info(?);", (data.name,))


TabsManager = TabManager()
