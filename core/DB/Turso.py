import re
from libsql_client import create_client

from core.package.FileManager import FileManagerPkg

_RE_FIRST_KEYWORD = re.compile(
    r"^\s*(?:--[^\n]*\n|\s|/\*.*?\*/)*([A-Za-z]+)",
    re.DOTALL,
)


def _firstKeyword(SQLstr: str) -> str:
    """Возвращает ключевое слово, с которого начинается запрос ('insert', 'select', ...)."""
    m = _RE_FIRST_KEYWORD.match(SQLstr)
    return m.group(1).lower() if m else ''

class DbManager:
    _pathConfig = 'core/config/config.json'
    _initialized = False
    url = None
    auth_token = None

    async def setConf(self):
        if not self._initialized:
            conf = await FileManagerPkg.ReadFile(self._pathConfig)
            # config.json не хранится в git (секреты) — шаблон: config.example.json
            if not isinstance(conf, dict) or 'database' not in conf:
                raise FileNotFoundError(
                    "Не найден core/config/config.json. "
                    "Скопируйте core/config/config.example.json в core/config/config.json "
                    "и укажите url и auth_token базы данных."
                )
            conf = conf['database']
            self.url = conf['url']
            self.auth_token = conf['auth_token']
            self._initialized = True

    async def ATSQL(self, SQLstr: str, parameters=None):
        await self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        async with create_client(url=self.url, auth_token=self.auth_token) as db:
            if _firstKeyword(SQLstr) == 'insert' and 'returning' not in SQLstr.lower():
                SQLstr += " RETURNING id"
            print(' '.join(SQLstr.replace('\n', ' ').strip().split()), parameters or [])
            c = await db.execute(SQLstr, parameters or [])
            if c.rows:
                d = c.rows[0][0]
            else:
                d = None
            return d
            
    async def ASQL(self, SQLstr: str, parameters=None) -> dict[str, list]:
        await self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        async with create_client(url=self.url, auth_token=self.auth_token) as db:
            print(' '.join(SQLstr.replace('\n', ' ').strip().split()), parameters or [])
            result = await db.execute(SQLstr, parameters or [])
            return {'columns': list(result.columns), 'data': [dict(zip(result.columns, row)) for row in result.rows]}

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

ATSQL = DbManagerPkg.ATSQL
ASQL = DbManagerPkg.ASQL