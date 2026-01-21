from .bilderBase import BilderBase

class BilderDpi(BilderBase):
    temp = """# Системный файл для логики
import asyncio
from core.base import BaseApi, BaseObj, gid

class {nameClass}Obj(BaseObj):
    def __init__(self):
        self.id:int = None
        self.gid:gid = None
        self.{attrObj} = None

class {nameClass}Dpi(BaseApi):
    _classObj = {nameClass}Obj

    def _getNameClass(self):
        return "{nameClass}"

    def calcHeadLine(self, rop:{nameClass}Obj)->str:
        return f'{isHeadLine}'

    def calcMnemoCode(self, rop:{nameClass}Obj)->str:
        return f'{isMnemoCode}'

    async def insert(self)->{nameClass}Obj:
        return await super().insert()

    async def delete(self, rop:{nameClass}Obj)->None:
        {deleteDetails}
        return await super().delete(rop)
    
    async def update(self, rop:{nameClass}Obj)->None:
        return await super().update(rop)
    
    async def load(self, id: int)->{nameClass}Obj:
        return await super().load(id)

    {setter}
"""
    suffixFile = 'Dpi.py'

    def __init__(self, data):
        super().__init__(data)
        self.data['attrObj'] = self.__getRopAttr()
        self.data['isHeadLine'] = self.__getHeadLine()
        self.data['isMnemoCode'] = self.__getMnemoCode()
        self.data['deleteDetails'] = self.__getDelete()
        self.data['setter'] = self.__getSetter()

    def __getRopAttr(self):
        rop = []
        for i in self.data['attr']:
            if i['name'].startswith('id') or i['name'].startswith('n') or i['name'].startswith('b'):
                typeAttr = 'int'
            elif i['name'].startswith('gid'):
                typeAttr = 'gid'
            else:
                typeAttr = 'str'
            rop.append(f'{i['name']}:{typeAttr}')
        return f' = None\n{' '*8}self.'.join(rop)
    
    def __getHeadLine(self):
        rop = []
        for i in self.data['attr']:
            if 'isHeadLine' in i:
                rop.append(f'rop.{i['name']}')
        return '{' + ('} {'.join(rop) if rop != [] else 'rop.id') + '}'

    def __getMnemoCode(self):
        rop = []
        for i in self.data['attr']:
            if 'isMnemoCode' in i:
                rop.append(f'rop.{i['name']}')
        return '{' + ('} {'.join(rop) if rop != [] else 'rop.id') + '}'
    
    def __getDelete(self):
        res = []
        if 'collections' in self.data.keys():
            mM = self.data['name'][:self.data['name'].find('_')].lower()
            for i in self.data['collections']:
                w:str = i['name']
                m = i['name'][:i['name'].find('_')].lower()
                mtemp = '...' if mM == m else f'{m}.'
                res.append(f'from {mtemp}object.{w.split('_')[-1].lower()}.{w}Api import {w}Api')
                res.append(f'd = await {w}Api()._getAllByAttr(\'{i['attr']}\', rop.{'id' if i['attr'].startswith('id') else 'gid'})')
                res.append(f'if d: asyncio.gather(*({w}Api().delete(i) for i in d))')
                
        return '\n        '.join(res)

    def __getSetter(self):
        tempSet = 'def set{nameAttr}(self, obj:{nameClass}Obj, value): obj.{nameAttr} = value'
        listTepmSet = tuple(tempSet.format(nameAttr=i['name'], nameClass=self.data['name']) for i in self.data['attr'])
        return '\n    '.join(listTepmSet)