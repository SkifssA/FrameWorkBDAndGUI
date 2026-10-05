from typing import Unpack

from core.ui.forms.base import Base, Config
from core.ui.forms.modal import Modal
from core.ui.forms.mainmenu import MainMenu

class Locat:
    right = 'right'
    left = 'left'
    bottom = 'bottom'
    top = 'top'


class FormConstruct:
    mainMenu:MainMenu = None

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
    
    def openForm(self):
        form = self._open(self.mainMenu)
        tab = self.mainMenu.tab_widget.addTab(*form.getForOpen())
        self.mainMenu.tab_widget.setCurrentIndex(tab)

    def openModal(self):
        self.param(modal=True)
        return Modal(self.clsForm, self.returnAttr)

    def _open(self, parentForm):
        self.clsForm = self.clsForm(**self._param)
        self.clsForm.formParent = parentForm
        self.clsForm.afterOpen()
        return self.clsForm