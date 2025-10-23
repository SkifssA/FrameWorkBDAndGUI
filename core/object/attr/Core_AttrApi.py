# Пользовательский файл для логики
from .Core_AttrDpi import Core_AttrDpi, Core_AttrObj

class Core_AttrApi(Core_AttrDpi):
    async def register(self, idTab, sName, sType, sCaption, sNameRefTab=None):
        rop = await self._getAllByAttr('sCode', sName)
        if rop:
            rop = rop[0]
        else:
            rop = await super().insert()
            rop.idTab = idTab
            rop.sCaption = sCaption
            rop.sType = sType
            rop.sCode = sName
            rop.sRefClass = sNameRefTab
            await self.update(rop)
        return rop
