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
        return (await self.find(text, 'div', class_='entity__title mb-4')).find('h1').get_text()
    
    async def __getGenre(self, text)->list:
        return (i.get_text() for i in (await self.find(text, 'div', class_='entity-field__genres')).find_all('a'))
    
    async def __getSeries(self, text)->str:
        w = (await self.findAll(text, 'div', class_='g-col-7 g-col-sm-12 g-col-md-8 g-col-lg-9 g-col-xl-9 text-break'))
        if w[1].get_text().isdigit():
            return w[1].get_text()
        return w[2].get_text()
    
    async def __getUrlImg(self, text)->str:
        return (await self.find(text, 'img', class_='image__img rounded', title= self.d['name'])).get('src')

    def __convSeriesInInt(self, series:str):
        if series.isdigit():
            return int(series)
        else:
            w = series[series.find('/')+1:].strip()
            if w.isalnum():
                return int(w)
            else:
                return 0
            