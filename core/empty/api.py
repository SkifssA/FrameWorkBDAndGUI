"""
Что тут ТОЧНО должно быть:
1. Полная и человеческая работа с obj(создание, редактирование, удаление) 
2. Отказываемся от асинхроности(Все методы синхроны)
3. Должно быть базой для работы
4. Минимум работы с внешним obj
"""

from abc import abstractmethod


from core.DB.SQLapi import SQLApi
from core.empty.obj import EmptyObj

class EmptyApi(SQLApi):
    _classObj = EmptyObj

    @abstractmethod
    def calcHeadLine(self, obj:EmptyObj)->str:...
    @abstractmethod
    def calcMnemoCode(self, obj:EmptyObj)->str:...

    def insert(self):
        """Создание новой записи"""
        obj = self._classObj()
        obj.id = self._insert()
        return obj

    def delete(self, obj:EmptyObj):
        """Удаление записи по obj"""
        return self._deleteById(obj.id)

    def load(self, id: int)->EmptyObj:
        """Получение обьекта по id"""
        data = self._getById(id)
        return self._createObj(data=data['data'][0])

    def getAll(self)->list[EmptyObj]:
        res:list[EmptyObj] = []
        for data in self._getAll()['data']:
            res.append(self._createObj(data=data))
        return res

    def getAllByAttr(self, attr:str, value):
        res:list[EmptyObj] = []
        for data in self._findDataBase(attr, value)['data']:
            res.append(self._createObj(data=data))
        return res

    def findByMnemocode(self, value):
        if len(x:=self._findDataBase('sMnemoCode', value)['data']) > 0:
            return x[0].get('id', None)
        return None 

    def getByMnemocode(self, value):
        if len(x:=self._findDataBase('sMnemoCode', value)['data']) > 0:
            return self._createObj(x[0])
        return None 

    def update(self, obj):
        value = obj.__dict__.copy()
        value['sHeadLine'] = self.calcHeadLine(obj)
        value['sMnemoCode'] = self.calcMnemoCode(obj)
        keys = [k for k in value.keys() if k != 'id']
        self._updateObj(keys, value)
        
    def _createObj(self, data)->EmptyObj:
        """Получение обьекта с заполнеными полями"""
        obj = self._classObj()
        for k, v in data.items():
            setattr(obj, k, v)
        return obj

    
        
    