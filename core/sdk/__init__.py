"""core.sdk — единый стабильный публичный фасад ядра для модулей.

Правило: код в `module/**` должен импортировать возможности ядра ТОЛЬКО отсюда

Внутренняя структура `core` (package/, type/, empty/, fabric/, ui/, DB/) может
свободно рефакториться — контрактом является только этот файл.

Модуль намеренно НЕ тянет тяжёлые зависимости (aiohttp, libsql) на уровне
импорта — они подключаются лениво, внутри соответствующих классов.
"""

from pathlib import Path

# --- Пути проекта -----------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent

# --- Типы и события ---------------------------------------------------------
from core.type.Gid import Gid

# --- Базовые классы каркаса объектов ---------------------------------------
from core.empty.logic import EmptyLogic
from core.empty.obj import EmptyObj
from core.empty.pub import EmptyPub

from core.decorator import Oper, Setter

from core.fabric.Form import Form

# --- Инструменты ядра --------------------------------------------------------
from core.package.LazyVal import LazyVal
from core.package.AsynRun import asyncRun
from core.package.FileManager import AsyncFileManager, FileManagerPkg
from core.package.ThreadWorkerPkg import ThreadWorkerPkg
from core.package.AiohttpPkg import AiohttpPkg

# --- Готовые экземпляры (синглтоны ядра) ------------------------------------
from core.package import ACTIONDISPATCHER, METADATA

__all__ = [
    # пути
    'ROOT',
    # типы и события
    'Gid',
    # базовые классы
    'EmptyLogic',
    'EmptyObj',
    'EmptyPub',
    # декораторы
    'Oper',
    'Setter',
    #Фабрики
    'Form'
    # инструменты
    'LazyVal',
    'asyncRun',
    'AsyncFileManager',
    'FileManagerPkg',
    'ThreadWorkerPkg',
    'AiohttpPkg',
    #Готовые экземпляры
    'METADATA',
    'ACTIONDISPATCHER',
]