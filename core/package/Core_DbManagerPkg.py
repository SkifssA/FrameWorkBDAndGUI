import asyncio
from libsql_client import create_client

from .Core_FileManagerPkg import Core_FileManagerPkg

class Core_DbManager:
    _pathConfig = '../config/config.json'

    async def setConf(self):
        conf = await Core_FileManagerPkg.ReadFile(self._pathConfig)
        self.url = conf['url']
        self.auth_token = conf['auth_token']

    async def connect(self):
        self.client = create_client(url=self.url, auth_token=self.auth_token)

    async def ATSQL(self, SQLstr, parameters=None):
        async with create_client(url=self.url, auth_token=self.auth_token) as db:
            if 'insert'.upper() in SQLstr.upper():
                SQLstr += "RETURNING id"
            print(SQLstr, parameters or [])
            c = await db.execute(SQLstr, parameters or [])
            if c.rows != []:
                d = c.rows[0][0]
            else:
                d = None
            return d

    async def ASQL(self, SQLstr, parameters=None):
        async with create_client(url=self.url, auth_token=self.auth_token) as db:
            try:
                print(SQLstr, parameters or [])
                result = await db.execute(SQLstr, parameters or [])
                if result.columns:
                    return [dict(zip(result.columns, row)) for row in result.rows]
            except:
                return []

Core_DbManagerPkg = Core_DbManager()

asyncio.run(Core_DbManagerPkg.setConf())

ATQSL = Core_DbManagerPkg.ATSQL
ASQL = Core_DbManagerPkg.ASQL