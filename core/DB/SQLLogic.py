from abc import ABC, abstractmethod

from core.DB.Turso import ASQL, ATSQL
from core.package.AsynRun import asyncRun
import re

class SQLLogic(ABC):
    """Прослойка между sql и Logic"""
    @abstractmethod
    def _getNameClass(self)->str:...

    def _validate(self, keys: list|str): 
        if isinstance(keys, str): keys = [keys] 
        for key in keys:
            if not re.fullmatch(r'\w+', key):
                raise ValueError(f"[SQLValidate] Не выполнен SQL запрос из-за подозрений на инъекцию")

    def _getNameClassValidate(self):
        nameClass = self._getNameClass()
        self._validate(nameClass)
        return nameClass
    
    def _deleteById(self, id)->None:
        asyncRun(ATSQL(f"DELETE FROM {self._getNameClassValidate()} WHERE id = ?", [id]))

    def _insert(self)->int:
        return asyncRun(ATSQL(f"INSERT INTO {self._getNameClassValidate()} (id) VALUES (NULL)"))

    def _findDataBase(self, attr:str, value):
        self._validate(attr)
        if value is not None:
            w = asyncRun(ASQL(f'SELECT * FROM {self._getNameClassValidate()} WHERE {attr} = ?', [value,]))
        else:
            w = asyncRun(ASQL(f'SELECT * FROM {self._getNameClassValidate()} WHERE {attr} IS NULL'))
        return w

    def _getAll(self):
        return asyncRun(ASQL(f'SELECT * FROM {self._getNameClassValidate()}'))

    def _getById(self, id):
        return asyncRun(ASQL(f"SELECT * FROM {self._getNameClassValidate()} WHERE id = ?", [id]))

    def _updateObj(self, keys:list[str], value):
        self._validate(keys)            
        asyncRun(ATSQL(f"UPDATE {self._getNameClassValidate()} SET {' = ?, '.join(keys)} = ? WHERE id = ?", tuple(value[i] for i in keys) + (value['id'],)))