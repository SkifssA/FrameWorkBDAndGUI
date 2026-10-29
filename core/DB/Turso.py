import re
from libsql_client import create_client_sync  # Синхронный клиент

from core.package.FileManager import FileManagerPkg

_RE_FIRST_KEYWORD = re.compile(
    r"^\s*(?:--[^\n]*\n|\s|/\*.*?\*/)*([A-Za-z]+)",
    re.DOTALL,
)


def _firstKeyword(SQLstr: str) -> str:
    """Возвращает ключевое слово, с которого начинается запрос ('insert', 'select', ...)."""
    m = _RE_FIRST_KEYWORD.match(SQLstr)
    return m.group(1).lower() if m else ""


class DbManager:
    _pathConfig = "core/config/config.json"
    _initialized = False
    url = None
    auth_token = None

    def __init__(self):
        self.db = None

    def setConf(self):
        if not self._initialized:
            conf = FileManagerPkg.ReadFile(self._pathConfig)
            conf = conf["database"]
            self.url = conf["url"]
            self.auth_token = conf["auth_token"]
            self._initialized = True

    def ATSQL(self, SQLstr: str, parameters=None):
        self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        print(" ".join(SQLstr.replace("\n", " ").strip().split()), parameters or [])
        c = self.db.execute(SQLstr, parameters or [])
        if c.rows:
            d = c.rows[0][0]
        else:
            d = None
        return d

    def ASQL(self, SQLstr: str, parameters=None) -> dict[str, list]:
        self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        print(" ".join(SQLstr.replace("\n", " ").strip().split()), parameters or [])
        result = self.db.execute(SQLstr, parameters or [])
        return {
            "columns": list(result.columns),
            "data": [dict(zip(result.columns, row)) for row in result.rows],
        }

    def _ensure_initialized(self):
        """Гарантирует что конфигурация загружена"""
        if not self._initialized:
            self.setConf()
            self.db = create_client_sync(url=self.url, auth_token=self.auth_token)

    def rebaseParameters(self, parameters):
        parameters = list(parameters or [])
        return parameters


DbManagerPkg = DbManager()

ATSQL = DbManagerPkg.ATSQL
ASQL = DbManagerPkg.ASQL
