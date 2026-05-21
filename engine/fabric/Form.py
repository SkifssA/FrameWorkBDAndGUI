from typing import Unpack

from engine.form.Base import Base, Config
from engine.package.FrameworkContext import FrameworkContext
from engine.package import AsynRunPkg

class FormConstruct:
    def __init__(self, clsForm:Base.__class__):
        self.clsForm = clsForm()
        self.locat = 'bottom'

    def param(self, **kwargs:Unpack[Config]):
        for key, value in kwargs.items():
            setattr(self.clsForm, key, value)
        return self
    
    def result(self,callback=None, returnAttr:list=['id']):
        '''НЕ РЕАЛИЗОВАНО'''
        self.callback = callback
        self.returnAttr = returnAttr
        return self
    
    def open(self):
        AsynRunPkg.asyncRun(self.clsForm.open('tab_bar', None))

    def openModal(self):
        self.clsForm.openModal(self.callback, self.returnAttr)

    def _open(self):
        from engine.form.MainMenu import mainMenu
        from engine.form.widgets.groupByCh import groupByCh

        parentForm = FrameworkContext.find_parent_form(self.clsForm, exclude_same_hierarchy=False)
        if (parentForm is not None):
            if issubclass(type(parentForm), mainMenu.Default):
                AsynRunPkg.asyncRun(self.clsForm.open('tab_bar', None))
            elif issubclass(type(parentForm), groupByCh):
                AsynRunPkg.asyncRun(self.clsForm.open(parentForm.group, parentForm.obj.mainForm))
            else:
                AsynRunPkg.asyncRun(self.clsForm.open(parentForm.tabBar, parentForm.mainForm))
        else:
            AsynRunPkg.asyncRun(self.clsForm.open('main_window', None))