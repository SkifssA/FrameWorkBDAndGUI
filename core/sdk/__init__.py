"""core.sdk — единый стабильный публичный фасад ядра для модулей.

Правило: код в `module/**` должен импортировать возможности ядра ТОЛЬКО отсюда

Внутренняя структура `core` (package/, type/, empty/, fabric/, ui/, DB/) может
свободно рефакториться — контрактом является только этот файл.

Модуль намеренно НЕ тянет тяжёлые зависимости (aiohttp, libsql) на уровне
импорта — они подключаются лениво, внутри соответствующих классов.
"""

from pathlib import Path

# --- Пути проекта -----------------------------------------------------------
from core import ROOT

# --- Базовые классы каркаса объектов ---------------------------------------
from core.empty.logic import EmptyLogic
from core.empty.obj import EmptyObj
from core.empty.pub import EmptyPub, eventSignal

from core.decorator import Oper, Setter

from core.fabric.Form import Form

from core.dataClass.formEvent import formEvent, typeEvent

# --- Инструменты ядра --------------------------------------------------------
from core.package.LazyVal import LazyVal
from core.package.FileManager import FileManager, FileManagerPkg
from core.package.ThreadWorkerPkg import ThreadWorkerPkg

# --- Готовые экземпляры (синглтоны ядра) ------------------------------------
from core.package.MetadataManager import MetadataManager
from core.package.ModuleManagerPkg import ModuleManagerPkg

# --- Переменые контекста  ---------------------------------------------------
from core.context import current_session_id, current_session_form

METADATA = MetadataManager()
ACTIONDISPATCHER = ModuleManagerPkg()

__all__ = [
    # пути
    "ROOT",
    # базовые классы
    "EmptyLogic",
    "EmptyObj",
    "EmptyPub",
    # декораторы
    "Oper",
    "Setter",
    # Фабрики
    "Form",
    # инструменты
    "LazyVal",
    "FileManager",
    "FileManagerPkg",
    "ThreadWorkerPkg",
    # Готовые экземпляры
    "METADATA",
    "ACTIONDISPATCHER",
    # Сигналы
    "eventSignal",
    # Переменые контекста
    'current_session_id',
    'current_session_form'
    #Разное
    "formEvent",
    "typeEvent"
]
