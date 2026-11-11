from abc import ABC, abstractmethod

from core.DB import ASQL, ATSQL
import re


class SQLLogic(ABC):
    """Прослойка между sql и Logic"""

    @abstractmethod
    def _getNameClass(self) -> str: ...

    def _validate(self, keys: list | str):
        if isinstance(keys, str):
            keys = [keys]
        for key in keys:
            if not re.fullmatch(r"\w+", key):
                raise ValueError(
                    f"[SQLValidate] Не выполнен SQL запрос из-за подозрений на инъекцию"
                )

    def _getNameClassValidate(self):
        nameClass = self._getNameClass()
        self._validate(nameClass)
        return nameClass

    def _deleteById(self, id) -> None:
        ATSQL(f"DELETE FROM {self._getNameClassValidate()} WHERE id = ?", [id])

    def _findDataBase(self, attr: str, value):
        self._validate(attr)
        if value is not None:
            w = ASQL(
                f"SELECT * FROM {self._getNameClassValidate()} WHERE {attr} = ?",
                [
                    value,
                ],
            )
        else:
            w = ASQL(
                f"SELECT * FROM {self._getNameClassValidate()} WHERE {attr} IS NULL"
            )
        return w

    def _getAll(self):
        return ASQL(f"SELECT * FROM {self._getNameClassValidate()}")

    def _getById(self, id):
        return ASQL(f"SELECT * FROM {self._getNameClassValidate()} WHERE id = ?", [id])

    def _insert(self, keys, value) -> int:
        self._validate(keys)
        return ATSQL(
            f"INSERT INTO {self._getNameClassValidate()} ({', '.join(keys)}) VALUES ({('?,'*len(keys))[:-1]})", tuple(value[i] for i in keys)
        )
    
    def _updateObj(self, keys: list[str], value):
        self._validate(keys)
        ATSQL(
            f"UPDATE {self._getNameClassValidate()} SET {' = ?, '.join(keys)} = ? WHERE id = ?",
            tuple(value[i] for i in keys) + (value["id"],),
        )
