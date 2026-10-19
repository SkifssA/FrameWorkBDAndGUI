from .bilderBase import BilderBase


# {setter}
class BilderDvi(BilderBase):
    temp = """# Системный файл для интерфейса
from .{name}Logic import {name}Logic, {name}Obj
from core.sdk import EmptyPub, SetterEvent, Setter

class {name}Dvi(EmptyPub):
    thisLogic = {name}Logic

    class DviDefault(EmptyPub.Default):
        def structuredQuery(self):
            return \"\"\"{sqlList}\"\"\"

        def onRefreshExt(self):
            return \"\"\"{sqlListExt}\"\"\"

        def thisLogic(self)->{name}Logic:
            return super().thisLogic()

        {setter}
        
    class DviList(DviDefault, EmptyPub.List):...

    class DviCard(DviDefault, EmptyPub.Card):...

    class DviLookUp:
        def onRefresh(self):
            return \"\"\"
            SELECT t.id
                ,t.sHeadLine 
            FROM {name} AS t
            \"\"\"
"""
    suffixFile = "Dvi.py"

    def __init__(self, data):
        super().__init__(data)
        w = self.__getSqlList()
        self.dictData["setter"] = self.__getSetters()
        self.dictData["sqlList"] = w[0]
        self.dictData["sqlListExt"] = w[1]

    def __getSetters(self):
        def getSetterStr(nameAttr, tempSet):
            setHead = "def set{nameAttr}(self, event:SetterEvent): ".format(
                nameAttr=nameAttr
            )
            return tempSet.format(nameAttr=nameAttr, setHead=setHead)

        tempSet = "@Setter\n        {setHead}self.thisLogic().set{nameAttr}(self.thisObj(), event.value); self.afterSetter('{nameAttr}')"
        listTepmSet = []

        for attr in self.data.attr:
            listTepmSet.append(getSetterStr(attr.name, tempSet))

            if attr.editType == "lookUp":
                listTepmSet.append(getSetterStr(attr.name + "HL", tempSet))

        return f"\n{self.tabSpace * 2}".join(listTepmSet)

    def __getSqlList(self) -> str:
        nameTabl = self.data.name
        dataAttr = self.data.attr
        sqlstr = {"int": 1, "attr": ["t.id"], "join": []}
        for attr in dataAttr:
            sqlstr["attr"].append(f"t.{attr.name}")
            if attr.refTab:
                sqlstr["attr"].append(f"t{sqlstr['int']}.sHeadLine as {attr.name}HL")
                sqlstr["join"].append(
                    f"LEFT JOIN {attr.refTab} t{sqlstr['int']} ON t{sqlstr['int']}.id = t.{attr.name}"
                )
                sqlstr["int"] += 1

        getSel = f",\n{self.tabSpace * 3}".join(
            f":{i[i.rfind('.') + 1 :]} as {i[i.rfind('.') + 1 :]}"
            for i in sqlstr["join"]
        )
        getExt = f",\n{self.tabSpace * 5}".join(
            i for i in sqlstr["attr"] if i.endswith("HL")
        )
        return [
            f"""
                SELECT {f",\n{self.tabSpace * 5}".join(sqlstr["attr"])}
                FROM {nameTabl} AS t
                    {f"\n{self.tabSpace * 5}".join(sqlstr["join"])}
                """,
            f"""
                with t as ( select 
                    :id as id{"," if getSel != "" else ""}
                    {getSel}
                )
                select
                    t.id{"," if getExt != "" else ""}
                  {getExt}
                from t
                    {f"\n{self.tabSpace * 3}".join(sqlstr["join"])}
                """,
        ]
