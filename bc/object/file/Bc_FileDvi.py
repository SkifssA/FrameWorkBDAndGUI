# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .Bc_FileApi import Bc_FileApi, Bc_FileObj

class Bc_FileDvi(BaseAvi):
    thisApi = Bc_FileApi
    class DviList(BaseAvi.DefaultList):
        showAttr = ['gidScr', 'sCaption', 'sSuffix', 'sPath']
        selection = Selection('Bc_File')
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

        async def thisApi(self)->Bc_FileApi:
            return super().thisApi()

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return """
            SELECT t.id
                  ,t.sHeadLine 
            FROM Bc_File AS t
            """
