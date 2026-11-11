from libsql_client import create_client_sync  # Синхронный клиент

from core.package.FileManager import FileManagerPkg
from core.context import PATH_CONFIG
from core.package.loggingConfig import get_logger

log = get_logger('core.db')

class DbManager:
    _initialized = False
    url = None
    auth_token = None

    def __init__(self):
        self.db = None

    def setConf(self):
        if not self._initialized:
            conf = FileManagerPkg.ReadFile(PATH_CONFIG)
            conf = conf["database"]
            self.url = conf["url"]
            self.auth_token = conf["auth_token"]
            self._initialized = True

    def ATSQL(self, SQLstr: str, parameters=None):
        self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        log.debug("%s %s", " ".join(SQLstr.replace("\n", " ").strip().split()), parameters)
        c = self.db.execute(SQLstr, parameters)
        if c.rows:
            d = c.rows[0][0]
        else:
            d = None
        return d

    def ASQL(self, SQLstr: str, parameters=None) -> dict[str, list]:
        self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        
        log.debug("%s %s", " ".join(SQLstr.replace("\n", " ").strip().split()), parameters)
        result = self.db.execute(SQLstr, parameters)
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
