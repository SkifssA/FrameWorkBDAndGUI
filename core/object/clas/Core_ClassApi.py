# Пользовательский файл для логики
from .Core_ClassDpi import Core_ClassDpi, Core_ClassObj

class Core_ClassApi(Core_ClassDpi):    
    async def register(self, sName, sCaption):
        rop = await self._getAllByAttr('sCode', sName)
        if rop:
            rop = rop[0]
        else:
            rop = await super().insert()
            rop.sCaption = sCaption
            rop.sCode = sName
            await self.update(rop)
        return rop
        

