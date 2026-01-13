# Пользовательский файл для логики
from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj

class Awh_AnimeApi(Awh_AnimeDpi):
    async def register(self, data):
        obj = await self.insert()
        obj.bReleased = data['released']
        obj.sCaption = data['name']
        obj.nSeries = data['series']
        await self.update(obj)
