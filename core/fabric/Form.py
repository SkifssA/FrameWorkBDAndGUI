from typing import Unpack

from core.ui.forms.base import Base, Config
from core.ui.forms.modal import Modal
from core.package.FrameworkContext import FrameworkContext

class Locat:
    right = 'right'
    left = 'left'
    bottom = 'bottom'
    top = 'top'


class FormConstruct:
    def __init__(self, clsForm:type[Base]):
        self.clsForm = clsForm
        self.locat = Locat.right
        self.callback = None
        self.returnAttr = None
        self._param = {}

    def param(self, **kwargs:Unpack[Config]):
        self._param = kwargs
        return self
    
    def result(self,returnAttr:list):
        self.returnAttr = returnAttr
        return self
    
    def open(self):
        return self._open()

    def openModal(self):
        self.param(modal=True)
        return Modal(self.clsForm, self.returnAttr)

    def _open(self):
        from core.ui.forms.mainmenu import MainMenu
        self.clsForm = self.clsForm(**self._param)
        parentForm = FrameworkContext.find_parent_form(self.clsForm, exclude_same_hierarchy=False)
        if (parentForm is not None):
            if isinstance(parentForm, MainMenu):
                self.clsForm.formParent = parentForm
                parentForm.tab_widget.addTab(*self.clsForm.getForOpen())
            else:
                return self.clsForm