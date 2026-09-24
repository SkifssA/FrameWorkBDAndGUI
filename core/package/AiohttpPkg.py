import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup, Tag
from typing import Union


class AiohttpPkg:
    _domen = None
    _nameCSRFToken = None
    _url = None
    def __init__(self):
        self.session = None
        self.info = {}

    async def init(self):
        self.session = aiohttp.ClientSession()
        return self

    def _getHeaders(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    
    async def _reSearch(self, pattern, text):
        match = await asyncio.to_thread(re.search, pattern, text)
        return match.group(1) if match else None
    
    def get(self, nameUrl, headers=None):
        fullUrl = self.GetUrl(nameUrl)
        if fullUrl is None:
            fullUrl = nameUrl
        h = self._getHeaders() if headers is None else headers
        return self.session.get(fullUrl, headers=h)
    
    def post(self, nameUrl, data):
        fullUrl = self.GetUrl(nameUrl)
        return self.session.post(fullUrl, data=data, headers=self._getHeaders())
    
    def GetUrl(self, nameUrl):
        try:
            w = (self._domen + self._url[nameUrl]).format(**self.info)
            return w
        except:
            return nameUrl
         
    async def _getCSRFToken(self):
        async with self.get('login') as response:
            text = await response.text()
            pattern = r'{0}" value="([^"]+)"'.format(self._nameCSRFToken)
            match = await self._reSearch(pattern, text)

            if not match:
                raise Exception("Не удалось найти logintoken на странице входа!")
            
            return match

    async def Login(self, login, password, withCSRFToken=False):
        payload = {
            'username': login,
            'password': password
        }

        if withCSRFToken:
            payload[self._nameCSRFToken] = await self._getCSRFToken()

        async with self.post('login', data=payload) as response:
            if response.status == 200:
                text = await response.text()
                text = text.lower()
            # Можно проверить, есть ли в ответе признак успешного входа
                if "Выход".lower() in text and "Домашняя страница".lower() in text:
                    print("Вход выполенен успешно")
                else:
                    print("Вход не удался — проверьте логин/пароль")
            else:
                print("Ошибка входа:", response.status_code)
        
    async def findAll(self, content: Union[str, BeautifulSoup, Tag], tag, **kargm):
        if isinstance(content, str):
            soup = BeautifulSoup(content, 'html.parser')
        elif isinstance(content, (BeautifulSoup, Tag)):
            soup = content  # и BeautifulSoup, и Tag имеют .find_all()
        else:
            raise TypeError("content must be str, BeautifulSoup, or Tag")
        return await asyncio.to_thread(soup.find_all, tag, **kargm)
    
    async def find(self, content: Union[str, BeautifulSoup, Tag], tag, **kargm):
        if isinstance(content, str):
            soup = BeautifulSoup(content, 'html.parser')
        elif isinstance(content, (BeautifulSoup, Tag)):
            soup = content  # и BeautifulSoup, и Tag имеют .find_all()
        else:
            raise TypeError("content must be str, BeautifulSoup, or Tag")
        return await asyncio.to_thread(soup.find, tag, **kargm)
        
    async def close(self):
        if self.session:
            await self.session.close()