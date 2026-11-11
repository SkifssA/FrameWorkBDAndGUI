import os
import re
import sqlite3
import threading
from urllib.parse import urlparse, unquote

from core.package.FileManager import FileManagerPkg
from core.context import PATH_CONFIG
from core.package.loggingConfig import get_logger

log = get_logger('core.db')


class DbManager:
    _initialized = False
    url = None
    path = None

    def __init__(self):
        self.db: sqlite3.Connection | None = None
        self._lock = threading.RLock()

    # ---------- конфигурация ----------

    def setConf(self):
        if self._initialized:
            return
        conf = FileManagerPkg.ReadFile(PATH_CONFIG)["database"]
        # поддерживаем и "path": "data/app.db", и старый "url": "file:data/app.db"
        self.url = conf.get("url")
        self.path = conf.get("path") or self._url_to_path(self.url)
        self._initialized = True

    @staticmethod
    def _url_to_path(url: str | None) -> str:
        if not url:
            return "app.db"
        if url.startswith("file:"):
            parsed = urlparse(url)
            # file:relative.db / file:///abs/path.db
            raw = parsed.path or parsed.netloc
            return unquote(raw) or "app.db"
        return url  # обычная строка-путь

    def _ensure_initialized(self):
        if self.db is not None:
            return
        self.setConf()

        directory = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(directory, exist_ok=True)

        self.db = sqlite3.connect(
            self.path,
            check_same_thread=False,   # доступ из разных потоков (под self._lock)
            isolation_level=None,      # ручное управление транзакциями
            timeout=30.0,
        )
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=NORMAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        log.info("SQLite opened: %s", os.path.abspath(self.path))

    # ---------- параметры ----------

    def rebaseParameters(self, parameters):
        if parameters is None:
            return []
        if isinstance(parameters, dict):
            return parameters          # для :name плейсхолдеров
        if isinstance(parameters, (list, tuple)):
            return list(parameters)    # для ? плейсхолдеров
        return [parameters]            # одиночное скалярное значение

    @staticmethod
    def _normalize_sql(SQLstr: str) -> str:
        """libsql-стиль :name работает и в sqlite3, конвертация не нужна."""
        return SQLstr

    @staticmethod
    def _log_sql(SQLstr: str, parameters):
        log.debug("%s %s", " ".join(SQLstr.split()), parameters)

    # ---------- чтение ----------

    def ATSQL(self, SQLstr: str, parameters=None):
        """Первое поле первой строки или None."""
        self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        self._log_sql(SQLstr, parameters)
        with self._lock:
            cur = self.db.execute(SQLstr, parameters)
            row = cur.fetchone()
            return row[0] if row is not None else None

    def ASQL(self, SQLstr: str, parameters=None) -> dict[str, list]:
        self._ensure_initialized()
        parameters = self.rebaseParameters(parameters)
        self._log_sql(SQLstr, parameters)
        with self._lock:
            cur = self.db.execute(SQLstr, parameters)
            columns = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
            return {
                "columns": columns,
                "data": [dict(zip(columns, row)) for row in rows],
            }

    # ---------- запись: много запросов за одно обращение ----------

    def ASQL_batch(self, statements: list) -> list[dict]:
        """
        Все запросы — в одной транзакции, один сброс на диск (fsync).
        Формат элементов:
            "DELETE FROM t"
            ("INSERT INTO t (a,b) VALUES (?,?)", [1, 2])
            ("UPDATE t SET a=:a WHERE id=:id", {"a": 5, "id": 1})
        Либо объект с .sql / .parameters.
        """
        self._ensure_initialized()
        if not statements:
            return []

        prepared = []
        for item in statements:
            if isinstance(item, str):
                sql, params = item, []
            elif isinstance(item, (tuple, list)):
                sql = item[0]
                params = item[1] if len(item) > 1 else []
            elif isinstance(item, dict):
                sql, params = item["sql"], item.get("parameters")
            else:
                sql, params = item.sql, getattr(item, "parameters", None)
            prepared.append((sql, self.rebaseParameters(params)))

        log.debug("Batch: %d statements", len(prepared))
        results = []
        with self._lock:
            try:
                self.db.execute("BEGIN")
                for sql, params in prepared:
                    self._log_sql(sql, params)
                    cur = self.db.execute(sql, params)
                    columns = [d[0] for d in cur.description] if cur.description else []
                    rows = cur.fetchall() if columns else []
                    results.append({
                        "columns": columns,
                        "data": [dict(zip(columns, row)) for row in rows],
                        "rows_affected": cur.rowcount,
                        "last_insert_rowid": cur.lastrowid,
                    })
                self.db.execute("COMMIT")
            except Exception:
                self.db.execute("ROLLBACK")
                log.exception("Batch failed, rolled back")
                raise
        return results

    def ASQL_many(self, SQLstr: str, parameters_list: list) -> int:
        """Один и тот же запрос с множеством наборов параметров."""
        self._ensure_initialized()
        if not parameters_list:
            return 0
        params = [self.rebaseParameters(p) for p in parameters_list]
        log.debug("Many: %s (%d rows)", " ".join(SQLstr.split()), len(params))
        with self._lock:
            try:
                self.db.execute("BEGIN")
                cur = self.db.executemany(SQLstr, params)
                self.db.execute("COMMIT")
                return cur.rowcount
            except Exception:
                self.db.execute("ROLLBACK")
                raise

    def ASQL_script(self, SQL_script: str) -> None:
        """DDL/миграции: несколько команд без параметров."""
        self._ensure_initialized()
        with self._lock:
            self.db.executescript(SQL_script)

    # ---------- сервис ----------

    def close(self):
        with self._lock:
            if self.db is not None:
                self.db.close()
                self.db = None
                log.info("SQLite closed")

    def __enter__(self):
        self._ensure_initialized()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


DbManagerPkg = DbManager()

ATSQL = DbManagerPkg.ATSQL
ASQL = DbManagerPkg.ASQL
ASQL_batch = DbManagerPkg.ASQL_batch
ASQL_many = DbManagerPkg.ASQL_many