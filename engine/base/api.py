from ..package.DbManagerPkg import ATQSL, ASQL
from ..package.AsynRunPkg import asyncRun
from .Type import Gid
from abc import ABC, abstractmethod


likeСache = {}

class BaseApi(ABC):
    _idClass = None
    _classObj = None
    _all_instances = {}

    @abstractmethod
    def calcHeadLine(self, rop)->str: pass
    @abstractmethod
    def calcMnemoCode(self, rop)->str: pass

    def idClass(self):
        if self._idClass is None:
            print(self._getNameClass())
            id = asyncRun(ASQL(f'select t.id from Core_Class t where t.sMnemoCode = ?', (self._getNameClass(),)))
            return id[0]['id']
        else :
            return self._idClass

    async def getCaptionAttrClass(self)->list:
        r = await self._sqlMetaColumns('sCaption, sCode')
        return r
    
    async def _sqlMetaColumns(self, columns:str):
        return await ASQL(f"select {columns} from Core_Attr t where t.idTab = ? and t.sCode <> 'id'", (self.idClass(),))

    async def _findDataBase(self, attr:str, value):
        if value is not None:
            w = await ASQL(f'SELECT * FROM {self._getNameClass()} WHERE {attr} = ?', [value,])
        else:
            w = await ASQL(f'SELECT * FROM {self._getNameClass()} WHERE {attr} IS NULL')
        return w
    
    async def getAll(self):
        return await ASQL(f'SELECT * FROM {self._getNameClass()}')
    
    def _getAllByAttr(self, attr:str, value)->list|None:
        w = asyncRun(self._findDataBase(attr, value))
        if not w:  # covers both [] and None
            return None
        results = []
        for i in w:
            results.append(self._createRop(i))
        return results or []

    async def _findAllByAttr(self, attr:str, value)->list[int]|None:
        w = await self._findDataBase(attr, value)
        return list(i['id'] for i in w) if w!=[] else None

    async def _findByAttr(self, attr: str, value):
        w = await self._findAllByAttr(attr, value)
        return w[0] if w is not None else w
    
    def findByMnemocode(self, value)->int|None:
        return asyncRun(self._findByAttr('sMnemoCode', value=value))
    
    def getByMnemocode(self, value):
        if x:=self.findByMnemocode(value=value):
            return self.load(x)

    def insert(self):
        t = self._getNameClass()
        rop = self._classObj()
        rop.id = asyncRun(ATQSL(f"INSERT INTO {t} (id) VALUES (NULL)"))
        return rop
    
    def update(self, rop):
        value = self._getDataRop(rop)
        keys = [k for k in value.keys() if k != 'id']
        value['gid'] = ''#Gid(f'{self.idClass()}/{rop.id}')
        value['sHeadLine'] = self.calcHeadLine(rop)
        value['sMnemoCode'] = self.calcMnemoCode(rop)
        keys = [k for k in value.keys() if k != 'id']
        asyncRun(ATQSL(f"UPDATE {self._getNameClass()} SET {' = ?, '.join(keys)} = ? WHERE id = ?", tuple(value[i] for i in keys) + (rop.id,)))
        
    def delete(self, rop):
        return asyncRun(self._deleteById(rop.id))
        
    async def _deleteById(self, id):
        t = self._getNameClass()
        return await ATQSL(f"DELETE FROM {t} WHERE id = ?", [id])

    def _createRop(self, data):
        rop = self._classObj()
        value = self._getDataRop(rop)
        ''.startswith
        for k, v in {i:data[i] for i in value.keys()}.items():
            if k.startswith('gid'):
                v = Gid(v)
            setattr(rop, k, v)
        return rop

    def _getDataRop(self, rop)->dict:
        return rop.__dict__.copy()

    def load(self, id):
        try:
            if id is not None:
                t = self._getNameClass()
                if likeСache.get(t, None) is None: likeСache[t] = {}
                if (likeСache[t].get(id, None) is None):
                    data = asyncRun(ASQL(f"SELECT * FROM {t} WHERE id = ?", [id]))
                    likeСache[t][id] = self._createRop(data=data[0])

                return likeСache[t][id]
        except IndexError:
            pass



    