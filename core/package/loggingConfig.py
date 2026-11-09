import logging
import os

from core.package.FileManager import FileManagerPkg
from core.context import PATH_CONFIG

DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

# Короткие имена групп -> префиксы логгеров проекта.
# Логгер в модуле должен называться "necotab.<группа>.<что-то>",
# тогда уровень группы применяется ко всей ветке.
LOGGER_GROUPS = {
    "core": "necotab.core",
    "db": "necotab.db",
    "webapp": "necotab.webapp",
    "module": "necotab.module",
}

_configured = False


def _readLevelFromConfig() -> tuple[str, dict[str, str]]:
    """Читает секцию 'logging' из core/config/config.json, если она есть.

    Возвращает (общий_уровень, {группа: уровень}). Ошибки чтения не фатальны:
    конфиг может отсутствовать (например, при запуске тестов).
    """
    level = ""
    groups: dict[str, str] = {}
    try:
        file = FileManagerPkg.ReadFile(PATH_CONFIG)
        log = file['logging']
        level = log.get("level", "")
        groups = dict(log.get("levels", {}))
    except Exception:  # noqa: BLE001 — логирование не должно ронять старт
        pass
    return level, groups


def setup_logging(level: str | None = None) -> None:
    """Настраивает корневой логгер один раз. Повторные вызовы игнорируются."""
    global _configured
    if _configured:
        return

    conf_level, group_levels = _readLevelFromConfig()
    resolved = (
        level
        or os.getenv("LOG_LEVEL")
        or conf_level
        or "INFO"
    ).upper()

    root = logging.getLogger()
    root.setLevel(resolved)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATEFMT))
    root.handlers.clear()
    root.addHandler(handler)

    # Уровни по группам: env (LOG_LEVEL_DB=DEBUG) > config.json > общий
    for name, prefix in LOGGER_GROUPS.items():
        g = (
            os.getenv(f"LOG_LEVEL_{name.upper()}")
            or group_levels.get(name)
        )
        if g:
            logging.getLogger(prefix).setLevel(g.upper())

    # uvicorn пишет свои логи — не дублируем хендлеры
    for noisy in ("uvicorn.access",):
        lg = logging.getLogger(noisy)
        lg.propagate = True

    _configured = True


def get_logger(name: str = "") -> logging.Logger:
    """Возвращает логгер с префиксом 'necotab'.

    get_logger(__name__) внутри пакета превратится в necotab.<пакет>...,
    что позволяет управлять уровнями по группам.
    """
    setup_logging()
    clean = name.replace("core.", "").replace("webapp.", "").replace("module.", "mod.")
    return logging.getLogger(f"necotab.{clean}" if clean else "necotab")
