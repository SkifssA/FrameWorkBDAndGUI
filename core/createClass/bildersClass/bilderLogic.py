from .bilderBase import BilderBase

class BilderLogic(BilderBase):
    temp = """# Пользовательский файл для логики
from .{name}Dpi import {name}Dpi, {name}Obj

class {name}Logic({name}Dpi):
    pass
"""
    suffixFile = 'Logic.py'

    