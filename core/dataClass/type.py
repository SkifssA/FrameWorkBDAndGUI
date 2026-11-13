from enum import StrEnum

class typeEvent(StrEnum):
    refresh = 'refresh'
    openForm = 'openForm'
    open_form_ch = 'open_form_ch'
    closeForm = 'closeForm'
    openFormLookUp = 'openFormLookUp'
    openApp = 'openApp'
    closeApp = 'closeApp'

class typeLocat(StrEnum):
    bottom = 'bottom'
    left = 'left'
    right = 'right'