from .bilderBase import BilderBase
# {setter}
class BilderDvi(BilderBase):
    temp = """# Системный файл для интерфейса
from core.sdk import EmptyAvi, SetterEvent
from .{nameClass}Api import {nameClass}Api, {nameClass}Obj

class {nameClass}Dvi(EmptyAvi):
    thisApi = {nameClass}Api

    class DviDefault(EmptyAvi.Default):
        def structuredQuery(self):
            return \"\"\"{sqlList}\"\"\"

        def onRefresh(self):
            if (x:=self.filter._getWhere()) != '':
                return f'{{self.structuredQuery()}} where {{x}}'
            return self.structuredQuery()

        def onRefreshExt(self):
            return \"\"\"{sqlListExt}\"\"\"

        def thisRop(self)->{nameClass}Obj:
            return super().thisRop()

        def thisApi(self)->{nameClass}Api:
            return super().thisApi()

        {setter}
        
    class DviList(DviDefault, EmptyAvi.List): pass

    class DviCard(DviDefault, EmptyAvi.Card): 
        def onRefresh(self):
            return self.thisApi().load(self.idItem)

    class DviLookUp(EmptyAvi.LookUp):
        def onRefresh(self):
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
        tempSet = '{setHead}self.thisApi().set{nameAttr}(self.thisRop(), event.value); self.afterSetter(\'{nameAttr}\')'
        tempSetButton = '{setHead}\n            {import}\n            {AviClass}().proccessById(event, self.getAttr(\'{nameAttr}\'), lambda x: self.thisApi().set{nameAttr}(self.thisRop(), x[\'id\'])); self.afterSetter(\'{nameAttr}\')'
        listTepmSet = []

        dictAttr = {}
        for i in self.data['attr']:
            dictAttr['nameAttr'] = i['name']
            dictAttr['setHead'] = 'def set{nameAttr}(self, event:SetterEvent): '.format(**dictAttr)
            listTepmSet.append(tempSet.format(**dictAttr))

            editType = i.get('editType', None)
            dictAttr['setHead'] = 'def set{nameAttr}(self, event:SetterEvent): '.format(nameAttr=i['name']+'HL')
            mM = self.data['name'][:self.data['name'].find('_')].lower()
            if editType == 'lookUp':
                listTepmSet.append(tempSet.format(**dictAttr))
            elif i['name'].startswith('id') and editType is None:
                w:str = i['refTab']
                m = i['refTab'][:i['refTab'].find('_')].lower()
                mtemp = '...' if mM == m else f'{m}.'
                dictAttr['import']=f'from {mtemp}object.{x+'_' if (x:=w.split('_')[-1].lower()) == 'class' else x}.{w}Avi import {w}Avi'
                dictAttr['AviClass'] = f'{w}Avi'
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

        getSel = f',\n{self.tabSpace*3}'.join(f":{i[i.rfind('.')+1:]} as {i[i.rfind('.')+1:]}" for i in sqlstr['join'])
        getExt = f',\n{self.tabSpace*5}'.join(i for i in sqlstr['attr'] if i.endswith("HL"))
        return [f"""
                SELECT {f',\n{self.tabSpace*5}'.join(sqlstr['attr'])}
                FROM {nameTabl} AS t
                    {f'\n{self.tabSpace*5}'.join(sqlstr['join'])}
                """,
                f"""
                with t as ( select 
                    :id as id{',' if getSel != '' else ''}
                    {getSel}
                )
                select
                    t.id{',' if getExt != '' else ''}
                  {getExt}
                from t
                    {f'\n{self.tabSpace*3}'.join(sqlstr['join'])}
                """]