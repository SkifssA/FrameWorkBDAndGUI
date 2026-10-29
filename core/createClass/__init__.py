from core.validateStart import validateConfig

validateConfig()

from .buildersClass.main import createFile
from .createTab.main import createTab
from .createModule.main import createModule

import core.validateStart

__all__ = ["createFile", "createTab", "createModule"]
