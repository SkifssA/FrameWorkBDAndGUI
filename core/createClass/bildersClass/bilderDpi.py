from .bilderBase import BilderBase

class BilderDpi(BilderBase):
    temp = """# Системный файл для логики
from core.sdk import EmptyApi, EmptyObj

class {nameClass}Obj(EmptyObj):
    def __init__(self):
        self.id:int = None
        self.{attrObj} = None

class {nameClass}Dpi(EmptyApi):
    _classObj = {nameClass}Obj

    def _getNameClass(self):
        return "{nameClass}"

    def calcHeadLine(self, rop:{nameClass}Obj)->str:
        return f'{isHeadLine}'

    def calcMnemoCode(self, rop:{nameClass}Obj)->str:
        return f'{isMnemoCode}'

    def insert(self)->{nameClass}Obj:
        return super().insert()

    def getByMnemocode(self, value)->{nameClass}Obj|None:   
        return super().getByMnemocode(value)

    def delete(self, rop:{nameClass}Obj)->None:
        {deleteDetails}
        return super().delete(rop)
    
    def update(self, rop:{nameClass}Obj)->None:
        return super().update(rop)
    
    def load(self, id: int)->{nameClass}Obj:
        return super().load(id)

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
                res.append(f'for i in {w}Api().getAllByAttr(\'{i['attr']}\', rop.{'id' if i['attr'].startswith('id') else 'gid'}) or []:')
                res.append(f'    {w}Api().delete(i)')
                
        return '\n        '.join(res)

    def __getSetter(self):
        tempSet = 'def set{nameAttr}(self, obj:{nameClass}Obj, value): obj.{nameAttr} = value'
        listTepmSet = tuple(tempSet.format(nameAttr=i['name'], nameClass=self.data['name']) for i in self.data['attr'])
        return '\n    '.join(listTepmSet)