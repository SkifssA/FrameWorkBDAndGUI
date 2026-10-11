from core.package.ModuleManagerPkg import ModuleManagerPkg
from core.fabric.MetaInfo import MetaInfo
from core.dataClass.metaDataClass import metaShema

class MetadataManager:

    _memoMetaInfo:dict[str, MetaInfo] = {}
        
    def get(self, nameMetaFile:str, clsName: str, visited:list = [])->metaShema:
        path = self.get_impl_path(nameMetaFile)
        if not self._memoMetaInfo.get(nameMetaFile):
            self._memoMetaInfo[nameMetaFile] = MetaInfo().readMeta(path)
        metaInfo = self._memoMetaInfo[nameMetaFile]
        mataRepre:dict = metaInfo.getMetaUI()
        ui:metaShema = mataRepre.get(clsName, metaShema(name=clsName))

        depMeta = None
        if (x:=metaInfo.getDep()):
            if x not in visited:
                visited.append(path)
                depMeta = self.get(x, clsName, visited)

        if metaDef:=mataRepre.get('Default'):
            ui = metaDef.merge(ui)
        if depMeta:
            ui = depMeta.merge(ui)

        ui.attr.sort(key=lambda x: x.order)

        return ui
            
    def get_impl_path(self, nameMetaFile)->str:
        """Путь к файлу, где определён класс"""
        return ModuleManagerPkg().getMetaCache(nameMetaFile)[nameMetaFile]