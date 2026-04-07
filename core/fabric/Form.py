from typing import Unpack

from core.form.Base import Base, Config

class FormConstruct:
    def __init__(self, clsForm:Base.__class__):
        self.clsForm = clsForm()
        self.locat = 'bottom'

    def param(self, **kwargs:Unpack[Config]):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def result(self):
        '''НЕ РЕАЛИЗОВАНО'''
        return self
    
    def open(self):
        '''НЕ РЕАЛИЗОВАНО'''
        return self