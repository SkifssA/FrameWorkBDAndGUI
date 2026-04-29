from .bilderBase import BilderBase

class BilderApi(BilderBase):
    temp = """# Пользовательский файл для логики
from .{nameClass}Dpi import {nameClass}Dpi, {nameClass}Obj

class {nameClass}Api({nameClass}Dpi):
    pass
"""
    suffixFile = 'Api.py'

    