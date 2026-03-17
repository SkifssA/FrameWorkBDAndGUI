from ..package.Core_DbManagerPkg import ATQSL, ASQL
from . import asynRun
from .Type import Gid

class BaseApi:
    _idClass = None
    _classObj = None
    _all_instances = {}

    def asyncRun(self, coroutine):
        return asynRun.asyncRun(coroutine)

    async def idClass(self):
        id = await ASQL(f'select t.id from Core_Class t where t.sMnemoCode = ?', (self._getNameClass(),))
        return id[0]['id']

    async def getCaptionAttrClass(self)->list:
        r = await self._sqlMetaColumns('sCaption, sCode')
        return r
    
    async def _sqlMetaColumns(self, columns:str):
        return await ASQL(f"select {columns} from Core_Attr t where t.idTab = ? and t.sCode <> 'id'", (await self.idClass(),))

    async def _findDataBase(self, attr:str, value):
        if value is not None:
            w = await ASQL(f'SELECT * FROM {self._getNameClass()} WHERE {attr} = ?', [value,])
        else:
            w = await ASQL(f'SELECT * FROM {self._getNameClass()} WHERE {attr} IS NULL')
        return w
    
    async def getAll(self):
        return await ASQL(f'SELECT * FROM {self._getNameClass()}')
    
    async def _getAllByAttr(self, attr:str, value)->list|None:
        w = await self._findDataBase(attr, value)
        if not w:  # covers both [] and None
            return None
        results = []
        for i in w:
            results.append(self._createRop(i))
        return results

    async def _findAllByAttr(self, attr:str, value)->list[int]|None:
        w = await self._findDataBase(attr, value)
        return list(i['id'] for i in w) if w!=[] else None

    async def _findByAttr(self, attr: str, value):
        w = await self._findAllByAttr(attr, value)
        return w[0] if w is not None else w
    
    async def findByMnemocode(self, value)->int:
        return await self._findByAttr('sMnemoCode', value=value)

    def _getDataRop(self, rop)->dict:
        return rop.__dict__.copy()

    def calcHeadLine(self, rop):
        return ' '
    
    def calcMnemoCode(self, rop):
        return ' '

    async def insert(self):
        t = self._getNameClass()
        rop = self._classObj()
        rop.id = await ATQSL(f"INSERT INTO {t} (id) VALUES (NULL)")
        return rop
    
    async def update(self, rop):
        value = self._getDataRop(rop)
        keys = [k for k in value.keys() if k != 'id']
        value['gid'] = Gid(f'{await self.idClass()}/{rop.id}')
        value['sHeadLine'] = self.calcHeadLine(rop)
        value['sMnemoCode'] = self.calcMnemoCode(rop)
        keys = [k for k in value.keys() if k != 'id']
        await ATQSL(f"UPDATE {self._getNameClass()} SET {' = ?, '.join(keys)} = ? WHERE id = ?", tuple(value[i] for i in keys) + (rop.id,))
        
    async def delete(self, rop):
        return await self._deleteById(rop.id)
        
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

    async def load(self, id):
        try:
            if id is not None:
                t = self._getNameClass()
                data = await ASQL(f"SELECT * FROM {t} WHERE id = ?", [id])
                return self._createRop(data=data[0])
        except IndexError:
            pass



    