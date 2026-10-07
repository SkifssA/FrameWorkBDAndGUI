from core.decorator.setter import Setter, SETTER
from core.decorator.oper import Oper, OPER

from enum import StrEnum

class TypeDecorator(StrEnum):
    Oper = OPER
    Setter = SETTER


__all__ = [
    'Type'
    , 'Oper'
    , 'Setter'    
]