import re

from engine.base.obj import BaseObj
from engine.package.AsynRunPkg import asyncRun
from engine.package.DbManagerPkg import ASQL_Dict, ASQL
from engine.form.Base import Base

class Rect:
    """Класс для привода onRefresh к одному формату"""
    def __init__(self, class_:Base):
        self.class_ = class_
        self.data = []
        self.attr = []
        self.dataExt = []
        self.attrExt = []
        
    def getAttr(self):
        return self.attr + self.attrExt
    
    def getData(self):
        if len(self.dataExt) > 0:
            return list(d | dE for d, dE in zip(self.data, self.dataExt))
        return self.data

    def refresh(self):
        refreshRes = self.class_.onRefresh()
        if isinstance(refreshRes, str):
            self.data, self.attr = self._str(refreshRes)
        elif isinstance(refreshRes, list):
            print('list')
        else:
            self._obj(refreshRes)

    def refreshItem(self):
        refreshExtRes = self.class_.onRefreshExt()
        self.dataExt, self.attrExt = self._str(refreshExtRes, True)

    def _str(self, res, isExt:bool=False):
        data = []
        if (self.class_.getAttr('id') is None and isExt):
           for i in self.data:
            sqlAndParam = self._getSqlAndParam(res, i)
            data.append(asyncRun(ASQL(*sqlAndParam))[0])
        else: 
            sqlAndParam = self._getSqlAndParam(res)
            resSQL = asyncRun(ASQL_Dict(*sqlAndParam))
            data = resSQL['data']
            attr = resSQL['columns']
        return data, attr

    def _getSqlAndParam(self, res, data:dict=None)->tuple[str, list]:
        paternFind = r':([^ \s]*)'
        par = [self.class_.getAttr(i) if data is None else data[i] for i in re.findall(paternFind, res)]
        sql = re.sub(paternFind, '?', res)
        return (sql, par)

    def _list(self, res):
        pass

    def _obj(self, res:BaseObj):
        self.data = [res.__dict__.copy()]
        self.attr = list(self.data[0].keys())
        sqlAndParam = self._getSqlAndParam(self.class_.onRefreshExt(), self.data[0])
        extData = asyncRun(ASQL(*sqlAndParam))['data'][0]
        for nameAttr in extData:
            self.data[0][nameAttr] = extData[nameAttr]
            self.attr.append(nameAttr)
        