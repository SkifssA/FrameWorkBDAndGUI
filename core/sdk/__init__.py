"""core.sdk — единый стабильный публичный фасад ядра для модулей.

Правило: код в `module/**` должен импортировать возможности ядра ТОЛЬКО отсюда

Внутренняя структура `core` (package/, type/, empty/, fabric/, ui/, DB/) может
свободно рефакториться — контрактом является только этот файл.

Модуль намеренно НЕ тянет тяжёлые зависимости (aiohttp, libsql) на уровне
импорта — они подключаются лениво, внутри соответствующих классов.
"""

from core.validateStart import validateConfig


from pathlib import Path

# --- Пути проекта -----------------------------------------------------------
from core import ROOT

# --- Базовые классы каркаса объектов ---------------------------------------
from core.empty.logic import EmptyLogic
from core.empty.obj import EmptyObj
from core.empty.pub import EmptyPub, eventSignal

from core.emptySubClass.base import Base as BaseSubClass

from core.decorator import Oper, Setter

from core.dataClass.baseDataClass import Base as BaseDataClass
from core.dataClass.formEvent import formEvent
from core.dataClass.setterEvent import SetterEvent
from core.dataClass.formRef import FormRef

# --- Инструменты ядра --------------------------------------------------------
from core.package.LazyVal import LazyVal
from core.package.FileManager import FileManager, FileManagerPkg

# --- Готовые экземпляры (синглтоны ядра) ------------------------------------
from core.package.MetadataManager import METADATA
from core.package.ModuleManagerPkg import ACTIONDISPATCHER
from core.package.SessionStageManager import SESSION_STAGE

# --- Системный модуль sc: реестр классов -------------------------------------
# Sc_ClsLogic — источник истины о том, какому модулю принадлежит класс/таблица
# (getPrefixModule). Импорт ставим после METADATA/ACTIONDISPATCHER: сам модуль
# sc при инициализации использует FileManagerPkg из этого пакета.

from core.module.sc.object.cls.Sc_ClsLogic import Sc_ClsLogic

# --- Переменые контекста ----------------------------------------------------
from core.context import current_session_id

# --- Логер ------------------------------------------------------------------
from core.package.loggingConfig import get_logger, setup_logging

# --- Типы -------------------------------------------------------------------
from core.dataClass.type import typeEvent

__all__ = [
    # пути
    "ROOT",
    # базовые классы
    "EmptyLogic",
    "EmptyObj",
    "EmptyPub",

    "Base",
    # декораторы
    "Oper",
    "Setter",
    # инструменты
    "LazyVal",
    "FileManager",
    "FileManagerPkg",
    "ThreadWorkerPkg",
    # Готовые экземпляры
    "METADATA",
    "ACTIONDISPATCHER",
    "SESSION_STAGE",
    # Системный модуль sc (реестр классов)
    "Sc_ClsLogic",
    # Сигналы
    "eventSignal",
    # Переменые контекста
    'current_session_id',
    #Логер
    "setup_logging",
    "get_logger",
    #Типы
    "typeEvent",
    #Разное
    "formEvent",
    "SetterEvent",
    "FormRef",
    "validateConfig"
]
