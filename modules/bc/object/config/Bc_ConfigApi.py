# Пользовательский файл для логики
from .Bc_ConfigDpi import Bc_ConfigDpi, Bc_ConfigObj
from engine.package import ASQL

class Bc_ConfigApi(Bc_ConfigDpi):
    async def registerByModule(self, sModule, sCaprionSetting, sValue):
        obj = self.getByMnemocode(f'{sModule} {sCaprionSetting}')
        if obj is None:
            obj = self.insert()
            self.setsModule(obj, sModule)
            self.setsCaprionSetting(obj, sCaprionSetting)
        obj.sValue = sValue
        self.update(obj)
        return obj
    
    async def getValueByModule(self, sModule, sCaprionSetting):
        id = await self._findByAttr('sModule || \'.\' || sCaprionSetting', f'{sModule}.{sCaprionSetting}')
        return (self.load(id)).sValue
        
