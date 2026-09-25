import asyncio
import os

from libsql_client import create_client

from core.package.FileManager import FileManagerPkg

class DbManager:
    _pathConfig = 'core/config/config.json'
    _initialized = False
    url = None
    auth_token = None

    async def setConf(self):
        """Параметры БД: сначала переменные окружения, потом config.json.

        Токен НЕ должен лежать в git. Задайте один раз:
            $env:TURSO_URL / TURSO_AUTH_TOKEN   (Windows PowerShell)
            export TURSO_URL=... TURSO_AUTH_TOKEN=...   (Linux/macOS)
        """
        if not self._initialized:
            conf = (await FileManagerPkg.ReadFile(self._pathConfig))['database']
            self.url = os.environ.get('TURSO_URL') or conf.get('url')
            self.auth_token = os.environ.get('TURSO_AUTH_TOKEN') or conf.get('auth_token')
            self._initialized = True

    async def ATSQL(self, SQLstr: str, parameters=None):
        await self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        async with create_client(url=self.url, auth_token=self.auth_token) as db:
            if 'insert'.upper() in SQLstr.upper():
                SQLstr += " RETURNING id"
            print(' '.join(SQLstr.replace('\n', ' ').strip().split()), parameters or [])
            c = await db.execute(SQLstr, parameters or [])
            if c.rows != []:
                d = c.rows[0][0]
            else:
                d = None
            return d
            
    async def ASQL(self, SQLstr: str, parameters=None) -> dict[str, list]:
        await self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        async with create_client(url=self.url, auth_token=self.auth_token) as db:
            try:
                print(' '.join(SQLstr.replace('\n', ' ').strip().split()), parameters or [])
                result = await db.execute(SQLstr, parameters or [])
                return {'columns': list(result.columns), 'data': [dict(zip(result.columns, row)) for row in result.rows]}
            except:
                return {'columns': [], 'data': []}

    async def _ensure_initialized(self):
        """Гарантирует что конфигурация загружена"""
        if not self._initialized:
            await self.setConf()

    def rebaseParameters(self, parameters):
        parameters = list(parameters or [])
        from .. import Gid
        for x, i in enumerate(parameters):
            if type(i) == Gid:
                parameters[x] = i.get()
        return parameters

DbManagerPkg = DbManager()

# УДАЛИТЕ ЭТУ СТРОКУ:
# asyncio.run(DbManagerPkg.setConf())

ATSQL = DbManagerPkg.ATSQL
ASQL = DbManagerPkg.ASQL