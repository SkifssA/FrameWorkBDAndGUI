from .base import Base
from .lookup import LookUp
from .checkBox import CheckBox
from .lineEdit import LineEdit

inputType:dict[str, type[Base]] = {
    'check': CheckBox,
    'lookUp': LookUp,
    'edit': LineEdit
}