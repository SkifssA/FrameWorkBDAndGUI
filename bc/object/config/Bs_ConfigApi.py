# Пользовательский файл для логики
from .Bs_ConfigDpi import Bs_ConfigDpi, Bs_ConfigObj
from core.package import ASQL

class Bs_ConfigApi(Bs_ConfigDpi):
    async def insertByModule(self, sModule, sCaprionSetting, sValue):
        rop = await self.insert()
        rop.sModule = sModule
        rop.sCaprionSetting = sCaprionSetting
        rop.sValue = sValue
        await self.update(rop)
        return rop
    
    async def getValueByModule(self, sModule, sCaprionSetting):
        id = await self._findByAttr('sModule || \'.\' || sCaprionSetting', f'{sModule}.{sCaprionSetting}')
        return (await self.load(id)).sValue
        
