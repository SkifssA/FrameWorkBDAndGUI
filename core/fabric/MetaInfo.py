from dacite import from_dict, Config


from core.dataClass.metaDataClass import metaShema, attrMetaShema, filterMetaShema
from core.dataClass.tabDataClass import tabShema, attrShema, collectionsShema, dbDataShema
from core.package.AsynRun import asyncRun
from core.package.FileManager import FileManagerPkg

class MetaInfo:
    def __init__(self):
        pass

    def getMetaTab(self, path)->tabShema:
        data = asyncRun(FileManagerPkg.ReadFile(path))
        attrListByData = data.get('attr', [])
    
        data['attr'] = list(from_dict(data_class=attrShema, data=i) for i in attrListByData)
        data['collections'] = list(from_dict(data_class=collectionsShema, data=i) for i in data.get('collections', []))

        data['dbData'] = list(from_dict(data_class=dbDataShema, data=i) for i in data.get('dbData', []))
    
        return from_dict(data_class=tabShema, data=data)
    
    def getMetaUI(self, path)->dict[str, metaShema]:
        res = {}
        datas = asyncRun(FileManagerPkg.ReadFile(path))
        for data in datas:
            attrGen = lambda x: list(from_dict(data_class=attrMetaShema, data=i) for i in x.get('attr', []))
            data['attr'] = attrGen(data)
            f = []
            for filter in data.get('filter', []):
                filter['attr'] = attrGen(filter)
                f.append(from_dict(data_class=filterMetaShema, data=filter))
            data['filter'] = f
    
            res[data['name']] = from_dict(data_class=metaShema, data=data)