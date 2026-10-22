from dacite import from_dict, Config


from core.dataClass.metaDataClass import metaSchema, attrMetaSchema, filterMetaSchema
from core.dataClass.tabDataClass import (
    tabSchema,
    attrSchema,
    collectionsSchema,
    dbDataSchema,
)
from core.package.FileManager import FileManagerPkg


class MetaInfo:
    def __init__(self):
        self._dictMetaUi = {}
        self._dep = None

    def getMetaTab(self, path) -> tabSchema:
        data = FileManagerPkg.ReadFile(path)
        attrListByData = data.get("attr", [])

        data["attr"] = list(
            from_dict(data_class=attrSchema, data=i) for i in attrListByData
        )
        data["collections"] = list(
            from_dict(data_class=collectionsSchema, data=i)
            for i in data.get("collections", [])
        )

        data["dbData"] = list(
            from_dict(data_class=dbDataSchema, data=i) for i in data.get("dbData", [])
        )

        return from_dict(data_class=tabSchema, data=data)

    def readMeta(self, path):
        datas = FileManagerPkg.ReadFile(path)
        self._dictMetaUi = {}

        if x := datas.get("dep"):
            self._dep = x

        for data in datas.get("repres", []):
            attrGen = lambda x: list(
                from_dict(data_class=attrMetaSchema, data=i) for i in x.get("attr", [])
            )
            data["attr"] = attrGen(data)
            f = []
            for filter in data.get("filter", []):
                filter["attr"] = attrGen(filter)
                f.append(from_dict(data_class=filterMetaSchema, data=filter))
            data["filter"] = f

            self._dictMetaUi[data["name"]] = from_dict(data_class=metaSchema, data=data)

        return self

    def getMetaUI(self) -> dict[str, metaSchema]:
        return self._dictMetaUi

    def getDep(self) -> str:
        return self._dep
