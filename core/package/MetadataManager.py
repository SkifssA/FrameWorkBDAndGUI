import inspect

from core.package.FileManager import FileManagerPkg
from core.package import asyncRun
from core.fabric.dataClass.metaDataClass import metaShema, getDataClass

class MetadataManager:
    def get(self, obj)->metaShema:
        path = f'{self.get_impl_path(obj)}'
        Ameta = getDataClass(f"{path}.Ameta.json") or {}
        Dmeta = getDataClass(f"{path}.Dmeta.json") or {'Default':{'isVisibleToolBar': False}}

        if Dmeta and Ameta:
            return Dmeta['Default'].merge(Ameta[obj.__class__.__name__])
        elif Ameta.get(obj.__class__.__name__):
            return Ameta[obj.__class__.__name__]
        elif Dmeta:
            return Dmeta['Default']
            
        
    def get_impl_path(self, obj):
        """Путь к файлу, где определён класс"""
        file = inspect.getfile(obj.__class__)
        w = file.find('module')
        file = file[w:-3].replace('object', 'schemas')[:-3]
        return file