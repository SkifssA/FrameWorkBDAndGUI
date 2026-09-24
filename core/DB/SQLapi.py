from abc import ABC, abstractmethod

from core.DB.Turso import ASQL, ATSQL
from core.package.AsynRun import asyncRun

class SQLApi(ABC):
    """Прослойка между sql и api"""
    @abstractmethod
    def _getNameClass(self)->str:...
    
    def _deleteById(self, id)->None:
        asyncRun(ATSQL(f"DELETE FROM {self._getNameClass()} WHERE id = ?", [id]))

    def _insert(self)->int:
        return asyncRun(ATSQL(f"INSERT INTO {self._getNameClass()} (id) VALUES (NULL)"))

    def _findDataBase(self, attr:str, value):
        if value is not None:
            w = asyncRun(ASQL(f'SELECT * FROM {self._getNameClass()} WHERE {attr} = ?', [value,]))
        else:
            w = asyncRun(ASQL(f'SELECT * FROM {self._getNameClass()} WHERE {attr} IS NULL'))
        return w

    def _getAll(self):
        return asyncRun(ASQL(f'SELECT * FROM {self._getNameClass()}'))

    def _getById(self, id):
        return asyncRun(ASQL(f"SELECT * FROM {self._getNameClass()} WHERE id = ?", [id]))

    def _updateObj(self, keys, value):
        asyncRun(ATSQL(f"UPDATE {self._getNameClass()} SET {' = ?, '.join(keys)} = ? WHERE id = ?", tuple(value[i] for i in keys) + (value['id'],)))