import re

from core.DB.Turso import ASQL
from core.empty.obj import EmptyObj


class DataFetcher:
    """Класс для унификации получения данных через onRefresh"""

    def __init__(self, class_):
        from core.empty.pub import EmptyPub

        self.class_: EmptyPub = class_
        self._data = []
        self._attr = []
        self._dataExt = []
        self._attrExt = []

    def getAttr(self):
        return self._attr + self._attrExt

    def getAttrExt(self):
        return self._attrExt

    def getData(self):
        if len(self._dataExt) > 0:
            return list(d | dE for d, dE in zip(self._data, self._dataExt))
        return self._data

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
        self._dataExt, self._attrExt = self._str(refreshExtRes)

    def _str(self, res):
        data = []
        attr = []
        if res != "" and res != None:
            sqlAndParam = self._getSqlAndParam(res)
            resSQL = ASQL(*sqlAndParam)
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
        self._data = [res.getDict(isNotNone=False)]
        self._attr = list(self._data[0].keys())
        self.refreshItem()
