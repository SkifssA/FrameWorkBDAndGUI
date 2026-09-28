"""core.sdk — единый стабильный публичный фасад ядра для модулей.

Правило: код в `module/**` должен импортировать возможности ядра ТОЛЬКО отсюда:

    from core.sdk import LazyVal, SetterEvent, EmptyAvi, FormConstruct, ...

Внутренняя структура `core` (package/, type/, empty/, fabric/, ui/, DB/) может
свободно рефакториться — контрактом является только этот файл.

Разделы фасада:
  * Типы и события       — Gid, SetterEvent
  * Базовые классы       — EmptyAvi / EmptyApi / EmptyObj (каркас объектов)
  * UI-контракты         — FormConstruct, Image, Text, SetOper
  * Инструменты ядра     — asyncRun, LazyVal, диспетчер действий, файловый менеджер,
                           фоновый воркер, HTTP-клиент, Metadata
  * Прочее               — ROOT, MetadataManager

Модуль намеренно НЕ тянет тяжёлые зависимости (aiohttp, libsql) на уровне
импорта — они подключаются лениво, внутри соответствующих классов.
"""

from pathlib import Path

# --- Пути проекта -----------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent

# --- Типы и события ---------------------------------------------------------
from core.type.Gid import Gid
from core.type.Event import SetterEvent

# --- Базовые классы каркаса объектов ---------------------------------------
from core.empty import EmptyAvi, EmptyApi, EmptyObj

# --- UI-контракты для Avi-слоя модулей --------------------------------------
from core.fabric.Form import FormConstruct
from core.ui.forms.image import Image
from core.ui.forms.text import Text
from core.ui.widget.menubar import SetOper

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
    'SetterEvent',
    # базовые классы
    'EmptyAvi',
    'EmptyApi',
    'EmptyObj',
    # UI-контракты
    'FormConstruct',
    'Image',
    'Text',
    'SetOper',
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