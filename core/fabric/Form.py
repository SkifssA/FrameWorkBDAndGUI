from typing import Unpack

from core.form.Base import Base, Config
from core.package.FrameworkContext import FrameworkContext
from core.package import Core_AsynRunPkg

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
        from core.form.MainMenu import mainMenu
        from core.form.widgets.groupByCh import groupByCh

        parentForm = FrameworkContext.find_parent_form(self.clsForm, exclude_same_hierarchy=False)
        if (parentForm is not None):
            if issubclass(type(parentForm), mainMenu.Default):
                Core_AsynRunPkg.asyncRun(self.clsForm.open('tab_bar', None))
            elif issubclass(type(parentForm), groupByCh):
                Core_AsynRunPkg.asyncRun(self.clsForm.open(parentForm.group, parentForm.obj.mainForm))
            else:
                Core_AsynRunPkg.asyncRun(self.clsForm.open(parentForm.tabBar, parentForm.mainForm))
        else:
            Core_AsynRunPkg.asyncRun(self.clsForm.open('main_window', None))