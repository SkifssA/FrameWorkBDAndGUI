"""
Что тут ТОЧНО должно быть:
1. Полная и человеческая работа с obj(создание, редактирование, удаление)
2. Отказываемся от асинхроности(Все методы синхроны)
3. Должно быть базой для работы
4. Минимум работы с внешним obj
"""

from abc import abstractmethod
from dacite import from_dict, Config
from dataclasses import asdict
from typing import TypeVar, Generic, Type

from core.DB.SQLLogic import SQLLogic
from core.empty.obj import EmptyObj, typeCommit

T = TypeVar('T')

class EmptyLogic(SQLLogic, Generic[T]):
    _classObj: Type[T]
    _attrForHL = []
    _attrForMC = []
    _idClass = None

    @abstractmethod
    def calcHeadLine(self, obj: T) -> str: ...
    @abstractmethod
    def calcMnemoCode(self, obj: T) -> str: ...

    def __init__(self):
        super().__init__()
        self.actionCommit = {
            typeCommit.insert: self._insert,
            typeCommit.update: self._updateObj
        }
        

    @property
    def idClass(self):
        from core.module.sc import Sc_ClsLogic
        if self.__class__._idClass is None:
            w = Sc_ClsLogic().getByMnemocode(self._getNameClass())
            if w is None:
                return 1
            self.__class__._idClass = w.id
        return self.__class__._idClass

    def insert(self)->T:
        """Создание новой записи"""
        from core.module.sc import Sc_ClsLogic
        obj:EmptyObj = self._classObj()
        obj.id = Sc_ClsLogic().getID(self._getNameClass())
        obj.gid = f'{self.idClass}/{obj.id}'
        obj.typeCommit = typeCommit.insert
        return obj

    def after_setter(self, obj:T, sNameAttr:str):
        if obj.typeCommit != typeCommit.insert:
            obj.typeCommit = typeCommit.update

        if sNameAttr in self._attrForHL:
            obj.sHeadLine = self.calcHeadLine(obj)
        if sNameAttr in self._attrForMC:
            obj.sMnemoCode = self.calcMnemoCode(obj)

    def delete(self, obj: T):
        """Удаление записи по obj"""
        obj.typeCommit = typeCommit.delete

    def load(self, id: int) -> T:
        """Получение обьекта по id"""
        from core.package.SessionStageManager import SESSION_STAGE
        w = list(i for i in SESSION_STAGE.get_all_obj() if hasattr(i, 'gid') and i.gid == f'{self.idClass}/{id}')
        if w == []:
            data = self._getById(id)
            if data['data'] != []:
                return self._createObj(data=data["data"][0])
            return self._createObj({})
        return w[0]

    def getAll(self) -> list[T]:
        res: list[T] = []
        for data in self._getAll()["data"]:
            res.append(self._createObj(data=data))
        return res

    def getAllByAttr(self, attr: str, value):
        res: list[T] = []
        for data in self._findDataBase(attr, value)["data"]:
            res.append(self._createObj(data=data))
        return res

    def findByMnemocode(self, value):
        if len(x := self._findDataBase("sMnemoCode", value)["data"]) > 0:
            return x[0].get("id", None)
        return None

    def getByMnemocode(self, value):
        if len(x := self._findDataBase("sMnemoCode", value)["data"]) > 0:
            return self._createObj(x[0])
        return None

    def commit(self, obj: T):
        value = asdict(obj)
        keys = [k for k in value.keys() if k not in ["typeCommit"] + (['id'] if obj.typeCommit == typeCommit.update else [])]
        self.actionCommit[obj.typeCommit](keys, value)

    def _createObj(self, data) -> T:
        """Получение обьекта с заполнеными полями"""
        return from_dict(
            data_class=self._classObj, data=data, config=Config(cast=[int, str, bool])
        )
