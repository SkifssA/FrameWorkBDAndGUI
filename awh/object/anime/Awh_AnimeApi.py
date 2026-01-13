# Пользовательский файл для логики
from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj

class Awh_AnimeApi(Awh_AnimeDpi):
    async def register(self, data):
        w = await self.findByMnemocode(data['url'])
        if w is not None:
            return w
        obj = await self.insert()
        obj.bReleased = data['released']
        obj.sCaption = data['name']
        obj.nSeries = data['series']
        obj.sUrl = data['url']
        await self.update(obj)
        return obj.id
