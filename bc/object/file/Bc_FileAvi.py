# Пользовательский файл для интерфейса
from .Bc_FileDvi import Bc_FileDvi
from core.empty.CardFileView import CardFileView
from core.base.BaseAvi import BaseAvi

class Bc_FileAvi(Bc_FileDvi):
    @classmethod
    def list(cls, **kwargs):
        #Создаём экземпляр вложенного класса List
        instance = cls.List()
        
        # Устанавливаем атрибуты из kwargs
        for key, value in kwargs.items():
            setattr(instance, key, value)
    
        return instance

    class List(Bc_FileDvi.DviList):
        showAttr = ['sCaption', 'sSuffix']
        def openCh(self, master):
            yield Bc_FileAvi.CardFileView()


    class LookUp(Bc_FileDvi.DviLookUp):
        pass

    class CardFileView(CardFileView, BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return await self.thisApi().getRealPath(self.getAttr('super$id'))
