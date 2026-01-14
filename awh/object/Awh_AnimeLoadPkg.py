from core.package import Core_AiohttpPkg

class Awh_AnimeLoadPkg(Core_AiohttpPkg):
    async def getData(self, urlAnime: str):
        self.d = {}
        async with self.get(urlAnime) as response:
            text = await response.text()
            series = await self.__getSeries(text)

            self.d['name'] = await self.__getName(text)
            self.d['genre'] = await self.__getGenre(text)
            self.d['urlImg'] = await self.__getUrlImg(text)
            self.d['released'] = int(series.find('/') == -1)
            self.d['series'] = self.__convSeriesInInt(series)
            self.d['url'] = urlAnime
            print(self.d)
        return self.d
    
    async def __getName(self, text)->str:
        return (await self.find(text, 'div', class_='anime-title')).find('h1').get_text()
    
    async def __getGenre(self, text)->list:
        d = []
        for i in (await self.find(text, 'dd', class_='col-6 col-sm-8 mb-1 overflow-h')).find_all('a'):
            d.append(i.get_text())
        return d
    
    async def __getSeries(self, text)->str:
        return (await self.findAll(text, 'dd', class_='col-6 col-sm-8 mb-1'))[1].get_text()
    
    async def __getUrlImg(self, text)->str:
        return (await self.find(text, 'img', title= self.d['name'])).get('src')

    def __convSeriesInInt(self, series:str):
        if series.find('/') == -1:
            return int(series)
        else:
            w = series[series.find('/')+1:]
            if w.strip().isalpha():
                return int(w)
            else:
                return 0
            