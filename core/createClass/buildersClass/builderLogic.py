from .builderBase import builderBase


class builderLogic(builderBase):
    temp = """# Пользовательский файл для логики
from .{name}Dpi import {name}Dpi, {name}Obj

class {name}Logic({name}Dpi):
    pass
"""
    suffixFile = "Logic.py"
