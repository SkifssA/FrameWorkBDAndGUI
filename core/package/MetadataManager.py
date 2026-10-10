import inspect

from core.package.ModuleManagerPkg import ModuleManagerPkg
from core.package import asyncRun
from core.fabric.MetaInfo import MetaInfo
from core.dataClass.metaDataClass import metaShema

class MetadataManager:
    def get(self, obj:object|str)->metaShema:
        path = self.get_impl_path(obj)
        clsName = obj.__class__.__name__
        return self._get(f"{path}.Ameta.json", clsName)
        
    def _get(self, path:str, clsName: str)->metaShema:
        meta = MetaInfo()
        meta.readMeta(path)
        mataRepre:dict = meta.getMetaUI()
        ui:metaShema = mataRepre.get(clsName, metaShema(name=clsName))
        depMeta = None
        if (x:=meta.getDep()):
            pathDep = ModuleManagerPkg().getMetaCache(x)[x]
            depMeta = self._get(pathDep, clsName)

        if metaDef:=mataRepre.get('Default'):
            ui = metaDef.merge(ui)
        if depMeta:
            ui = depMeta.merge(ui)

        ui.attr.sort(key=lambda x: x.order)

        return ui
            
    def get_impl_path(self, obj:object|str)->str:
        """Путь к файлу, где определён класс"""
        file = inspect.getfile(obj.__class__)
        w = file.find('module')
        file = file[w:-3].replace('object', 'schemas')[:-3]
        return file