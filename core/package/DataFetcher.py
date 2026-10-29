import re

from core.DB.Turso import ASQL
from core.empty.obj import EmptyObj


class DataFetcher:
    """Класс для унификации получения данных через onRefresh"""

    def __init__(self, class_):
        from core.empty.pub import EmptyPub

        self.class_: EmptyPub = class_
        self._obj_res = None
        self._data:list[EmptyObj] = []
        self._attr = []
        self._dataExt = []
        self._attrExt = []
        self._old_data = []

    def getColumns(self):
        return self._attr + self._attrExt

    def getColumnsExt(self):
        return self._attrExt

    def getData(self):
        if len(self._dataExt) > 0:
            return list(d.getDict(isNotNone=False) | dE for d, dE in zip(self._data, self._dataExt))
        return list(d.getDict(isNotNone=False) for d in self._data)

    def getDateExt(self):
        return self._dataExt

    def refresh(self):
        self.refreshRes = self.class_.onRefresh()
        if self.refreshRes:
            if isinstance(self.refreshRes, str):
                self._data, self._attr = self._str(self.refreshRes)
            elif isinstance(self.refreshRes, list):
                print("list")
            else:
                self._obj(self.refreshRes)

    def refreshItem(self):
        refreshExtRes = self.class_.onRefreshExt()
        self._dataExt, self._attrExt = self._str(refreshExtRes, isExt=True)

    def _str(self, res, isExt:bool=False):
        data = []
        attr = []
        if res != "" and res != None:
            sqlAndParam = self._getSqlAndParam(res)
            resSQL = ASQL(*sqlAndParam)
            if not isExt:
                self._attrExt = list(i for i in resSQL['columns'] if i not in resSQL['data'][0].keys())
                for i in resSQL["data"]:
                    data.append(self.class_.thisLogic()._createObj(i))
                    self._dataExt.append({i:resSQL['data'][0][i] for i in self._attrExt})
            else:
                data = resSQL["data"]
            attr = resSQL["columns"]
        return data, attr

    def _getSqlAndParam(self, res, data: dict = None) -> tuple[str, list]:
        paternFind = r":([^ \s)]*)"
        par = [
            self.class_.getAttr(i) if data is None else data[i]
            for i in re.findall(paternFind, res)
        ]
        sql = re.sub(paternFind, "?", res)
        return (sql, par)

    def _list(self, res):
        pass

    def _obj(self, res: EmptyObj):
        self._data = [res]
        self._attr = list(self._data[0].getDict(isNotNone=False).keys())
        self.refreshItem()
