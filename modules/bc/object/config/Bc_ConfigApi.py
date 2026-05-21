# Пользовательский файл для логики
from .Bc_ConfigDpi import Bc_ConfigDpi, Bc_ConfigObj
from engine.package import ASQL

class Bc_ConfigApi(Bc_ConfigDpi):
    async def insertByModule(self, sModule, sCaprionSetting, sValue):
        rop = self.insert()
        rop.sModule = sModule
        rop.sCaprionSetting = sCaprionSetting
        rop.sValue = sValue
        self.update(rop)
        return rop
    
    async def getValueByModule(self, sModule, sCaprionSetting):
        id = await self._findByAttr('sModule || \'.\' || sCaprionSetting', f'{sModule}.{sCaprionSetting}')
        return (self.load(id)).sValue
        
