from .bilderBase import BilderBase

class BilderDvi(BilderBase):
    temp = """# Системный файл для интерфейса
from core.base import BaseAvi, Selection, Event
from .{nameClass}Api import {nameClass}Api, {nameClass}Obj

class {nameClass}Dvi(BaseAvi):
    thisApi = {nameClass}Api

    class DviDefault(BaseAvi.DefaultDefault):
        def onRefresh(self):
            return \"\"\"{sqlList}\"\"\"

        def onRefreshExt(self):
            return \"\"\"{sqlListExt}\"\"\"

        def thisRop(self)->{nameClass}Obj:
            return super().thisRop()

        def thisApi(self)->{nameClass}Api:
            return super().thisApi()
        
        {setter}

    class DviTabl(DviDefault, BaseAvi.DefaultTabl): pass

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
        tempSet = '{setHead}self.thisApi().set{nameAttr}(self.thisRop(), event.value); self.afterSetter()'
        tempSetLookUp = '{setHead}idLook = event.user_data.getId(event.value); self.thisApi().set{nameAttr}(self.thisRop(), idLook); self.afterSetter()'
        tempSetButton = '{setHead}event.user_data._getAvi()().proccessById(event, self.getAttr(\'{nameAttr}\'), lambda x: self.thisApi().set{nameAttr}(self.thisRop(), x[\'id\'])); self.afterSetter()'
        listTepmSet = []

        dictAttr = {}
        for i in self.data['attr']:
            dictAttr['nameAttr'] = i['name']
            dictAttr['setHead'] = 'def set{nameAttr}(self, event:Event.SetterEvent): '.format(**dictAttr)
            listTepmSet.append(tempSet.format(**dictAttr))
            editType = i.get('editType', None)
            dictAttr['setHead'] = 'def set{nameAttr}(self, event:Event.SetterEvent): '.format(nameAttr=i['name']+'HL')
            if editType == 'lookUp':
                listTepmSet.append(tempSetLookUp.format(**dictAttr))
            elif i['name'].startswith('id') and editType is None:
                listTepmSet.append(tempSetButton.format(**dictAttr))

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