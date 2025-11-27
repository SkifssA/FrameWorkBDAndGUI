# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_FileApi import Bc_FileApi, Bc_FileObj

class Bc_FileDvi(BaseAvi):
    thisApi = Bc_FileApi

    class DviDefault(BaseAvi.DefaultDefault): 
        showAttr = ['gidScr', 'sCaption', 'sSuffix', 'sPath']
        selection = lambda self: Selection(self.getTag())
        async def onRefresh(self):
            return """
            SELECT t.id,
                   t.gid,
                   t.gidScr,
                   t.sCaption,
                   t.sSuffix,
                   t.sPath
            FROM Bc_File AS t      
            """

        async def thisRop(self)->Bc_FileObj:
            return await super().thisRop()

        def thisApi(self)->Bc_FileApi:
            return super().thisApi()

    class DviList(DviDefault, BaseAvi.DefaultList): pass
        
    class DviDet(DviDefault, BaseAvi.DefaultDet): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bc_File AS t
            """