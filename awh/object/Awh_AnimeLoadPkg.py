from core.package import Core_AiohttpPkg

class Awh_AnimeLoadPkg(Core_AiohttpPkg):
    async def getData(self, urlAnime: str):
        d = {}
        async with self.get(urlAnime) as response:
            text = await response.text()
            d['name'] = await self.__getName(text)
            d['genre'] = await self.__getGenre(text)
        return d
    
    async def __getName(self, text):
        return (await self.find(text, 'div', class_='anime-title')).find('h1').get_text()
    
    async def __getGenre(self, text):
        d = []
        for i in (await self.find(text, 'dd', class_='col-6 col-sm-8 mb-1 overflow-h')).find_all('a'):
            d.append(i.get_text())
        return d