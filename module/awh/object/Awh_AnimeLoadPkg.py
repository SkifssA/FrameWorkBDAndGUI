class Awh_AnimeLoadPkg:
    async def getData(self, urlAnime: str):
        self.d = {}
        async with self.get(urlAnime) as response:
            text = response.text()
            series = self.__getSeries(text)

            self.d['name'] = self.__getName(text)
            self.d['genre'] = self.__getGenre(text)
            self.d['urlImg'] = self.__getUrlImg(text)
            self.d['released'] = int(series.find('/') == -1)
            self.d['series'] = self.__convSeriesInInt(series)
            self.d['comment'] = self.__comment(text)
            self.d['url'] = urlAnime
        return self.d
    
    async def __getName(self, text)->str:
        return (self.find(text, 'div', class_='entity__title mb-4')).find('h1').get_text()
    
    async def __getGenre(self, text)->list:
        return (i.get_text() for i in (self.find(text, 'div', class_='entity-field__genres')).find_all('a'))
    
    async def __getSeries(self, text)->str:
        w = (self.findAll(text, 'div', class_='g-col-7 g-col-sm-12 g-col-md-8 g-col-lg-9 g-col-xl-9 text-break'))
        if w[1].get_text().isdigit():
            return w[1].get_text()
        return w[2].get_text()
    
    async def __getUrlImg(self, text)->str:
        return (self.find(text, 'img', class_='image__img rounded', alt= self.d['name'])).get('src')

    def __convSeriesInInt(self, series:str):
        if series.isdigit():
            return int(series)
        else:
            w = series[series.find('/')+1:].strip()
            if w.isalnum():
                return int(w)
            else:
                return 0
            
    async def __comment(self, text)->str:
        return (self.find(text, 'div', class_='description')).get_text().strip()
            