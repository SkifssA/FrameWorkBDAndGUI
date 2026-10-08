from .bilderBase import BilderBase

class BilderDpi(BilderBase):
    temp = """# Системный файл для логики
from core.sdk import EmptyLogic, EmptyObj
from dataclasses import dataclass

@dataclass
class {name}Obj(EmptyObj):
    id:int
    {attrObj} = None

class {name}Dpi(EmptyLogic):
    _classObj = {name}Obj

    def _getNameClass(self):
        return "{name}"

    def calcHeadLine(self, rop:{name}Obj)->str:
        return f'{isHeadLine}'

    def calcMnemoCode(self, rop:{name}Obj)->str:
        return f'{isMnemoCode}'

    def insert(self)->{name}Obj:
        return super().insert()

    def getByMnemocode(self, value)->{name}Obj|None:   
        return super().getByMnemocode(value)

    def delete(self, obj:{name}Obj)->None:
        {deleteDetails}
        return super().delete(obj)
    
    def update(self, rop:{name}Obj)->None:
        return super().update(rop)
    
    def load(self, id: int)->{name}Obj:
        return super().load(id)

    {setter}
"""
    suffixFile = 'Dpi.py'

    def __init__(self, data):
        super().__init__(data)
        self.dictData['attrObj'] = self.__getRopAttr()
        self.dictData['isHeadLine'] = self.__getHeadLine()
        self.dictData['isMnemoCode'] = self.__getMnemoCode()
        self.dictData['deleteDetails'] = self.__getDelete()
        self.dictData['setter'] = self.__getSetter()

    def __getRopAttr(self):
        rop = []
        for i in self.data.attr:
            if i.name.startswith('id') or i.name.startswith('n') or i.name.startswith('b'):
                typeAttr = 'int'
            elif i.name.startswith('gid'):
                typeAttr = 'gid'
            else:
                typeAttr = 'str'
            rop.append(f'{i.name}:{typeAttr}')
        return f' = None\n{' '*4}'.join(rop)
    
    def __getHeadLine(self):
        attrByHL = []
        for attr in self.data.attr:
            if attr.isHeadLine:
                attrByHL.append(f'rop.{attr.name}')
        return '{' + ('} {'.join(attrByHL) if attrByHL != [] else 'rop.id') + '}'

    def __getMnemoCode(self):
        attrByMC = []
        for attr in self.data.attr:
            if attr.isMnemoCode:
                attrByMC.append(f'rop.{attr.name}')
        return '{' + ('} {'.join(attrByMC) if attrByMC != [] else 'rop.id') + '}'
    
    def __getDelete(self):
        from core.package.ActionDispatcher import getModule
        res = []
        myModule = getModule(self.data.name)
        for collection in self.data.collections:
            module = getModule(collection.name)
            res.append(f'from module.{module} import {collection.name}Logic')
            res.append(f'for i in {collection.name}Logic().getAllByAttr(\'{collection.attr}\', obj.{'id' if collection.attr.startswith('id') else 'gid'}) or []:')
            res.append(f'    {collection.name}Logic().delete(i)')
                
        return '\n        '.join(res)

    def __getSetter(self):
        tempSet = 'def set{nameAttr}(self, obj:{nameClass}Obj, value): obj.{nameAttr} = value'
        listTepmSet = tuple(tempSet.format(nameAttr=i.name, nameClass=self.data.name) for i in self.data.attr)
        return '\n    '.join(listTepmSet)