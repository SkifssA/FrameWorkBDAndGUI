from .bilderBase import BilderBase

class BilderDvi(BilderBase):
    temp = """# Системный файл для интерфейса
from core.base import BaseAvi, Selection
from .{nameClass}Api import {nameClass}Api, {nameClass}Obj

class {nameClass}Dvi(BaseAvi):
    thisApi = {nameClass}Api
    class DviDefault(BaseAvi.DefaultDefault):
        async def onRefresh(self):
            return \"\"\"{sqlList}\"\"\"

        def onRefreshExt(self):
            return \"\"\"{sqlListExt}\"\"\"

        async def thisRop(self)->{nameClass}Obj:
            return await super().thisRop()

        def thisApi(self)->{nameClass}Api:
            return super().thisApi()
        
        {setter}

    class DviList(DviDefault, BaseAvi.DefaultList): pass

    class DviCard(DviDefault, BaseAvi.DefaultCard): pass

    class DviLookUp(BaseAvi.DefaultLookUp):
        async def onRefresh(self):
            return \"\"\"
            SELECT t.id
                ,t.sHeadLine 
            FROM {nameClass} AS t
            \"\"\"
"""
    suffixFile = 'Dvi.py'

    def __init__(self, data):
        super().__init__(data)
        w = self.__getSqlList()
        self.data['setter'] = self.__getSetters()
        self.data['sqlList'] = w[0]
        self.data['sqlListExt'] = w[1]

    def __getSetters(self):
        tempSet = 'def set{nameAttr}(self, sender, app_data, user_data): self.thisApi().set{nameAttr}(self.obj, app_data); self.afterSetter()'
        tempSetLookUp = 'def set{nameAttr}HL(self, sender, app_data, user_data): idLook = user_data.getId(app_data); self.thisApi().set{nameAttr}(self.obj, idLook); self.afterSetter()'
        listTepmSet = []
        for i in self.data['attr']:
            listTepmSet.append(tempSet.format(nameAttr=i['name']))
            if  'editType' in i:
                if i['editType'] == 'lookUp':
                    listTepmSet.append(tempSetLookUp.format(nameAttr=i['name']))
        return f'\n{self.tabSpace*2}'.join(listTepmSet)
    
    def __getSqlList(self)->str:
        nameTabl = self.data['name']
        dataAttr = self.data['attr']
        sqlstr = {
            'int': 1,
            'attr': ['t.id', 't.gid'],
            'join': []
        }
        for i in dataAttr:
            sqlstr['attr'].append(f"t.{i['name']}")
            if 'refTab' in i:
                sqlstr['attr'].append(f"t{sqlstr['int']}.sHeadLine as {i['name']}HL")
                sqlstr['join'].append(f"LEFT JOIN {i['refTab']} t{sqlstr['int']} ON t{sqlstr['int']}.id = t.{i['name']}")
                sqlstr['int'] += 1
        return [f"""
                SELECT {f',\n{self.tabSpace*5}'.join(sqlstr['attr'])}
                FROM {nameTabl} AS t
                    {f'\n{self.tabSpace*5}'.join(sqlstr['join'])}
                """,
                f"""
                with t as ( select 
                    {f',\n{self.tabSpace*3}'.join(f":{i[i.rfind('.')+1:]} as {i[i.rfind('.')+1:]}" for i in sqlstr['join'])}
                )
                select {f',\n{self.tabSpace*5}'.join(i for i in sqlstr['attr'] if i.endswith("HL"))}
                from t
                    {f'\n{self.tabSpace*3}'.join(sqlstr['join'])}
                """]