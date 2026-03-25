from typing import TypedDict, Unpack
import flet as ft

from core.empty.FormFlet import BaseForm
from core.package.Core_AsynRunPkg import asyncRun

class FormConfig(TypedDict, total=False):
    locat: str
    isUpdate: bool
    parent:BaseForm


class FormHandle:
    def __init__(self, clsForm:BaseForm.__class__):
        self.clsForm = clsForm()
        self.locat = 'bottom'
        self.parent:BaseForm = None

    def param(self, **kwargs:Unpack[FormConfig]):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def result(self):
        '''НЕ РЕАЛИЗОВАНО'''
        return self
    
    def open(self):
        if type(self.parent) == ft.Page:
            asyncRun(self.clsForm.open())
        else:
            if self.parent is None:
                raise AttributeError(f"Нельзя открыть форму без родителя")
            asyncRun(self.clsForm.open(parent=self.parent.locationsChildrens[self.locat]))

class ClsFormManeger:
    allForm = {}
    
    def register(self, clsForm:BaseForm):
        return self._create(clsForm=clsForm)

    def _create(self, clsForm:BaseForm):
        return FormHandle(clsForm)


FornManeger = ClsFormManeger()