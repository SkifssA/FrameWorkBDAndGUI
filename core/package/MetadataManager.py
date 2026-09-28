import inspect

from core.package.FileManager import FileManagerPkg
from core.package import asyncRun

class MetadataManager:
    def get(self, obj)->dict:
        path = f'{self.get_impl_path(obj)}'
        a = asyncRun(FileManagerPkg.ReadFile(f"{path}.Ameta.json"))
        d = asyncRun(FileManagerPkg.ReadFile(f"{path}.Dmeta.json"))
        if obj.__class__.__name__ in a and d != 'Файл не найден':
            return self.__fillByDefault(a[obj.__class__.__name__], d['Default'])
        elif (obj.__class__.__name__ in a):
            return a[obj.__class__.__name__]
        elif 'Default' in d:
            return d['Default']
        else:
            return {'isVisibleToolBar': False}

    def __fillByDefault(self, a, d):
        self.__w(a, d, 'caption')
        self.__w(a, d, 'isVisibleToolBar')
        self.__w(a, d, 'attr')

        for i in d['attr']:
            self.__w(a['attr'], d['attr'], i)
            for j in d['attr'][i]:
                self.__w(a['attr'][i], d['attr'][i], j)
            
        return a

    def __w(self, a, d, sNAme):
        if(sNAme not in a):
            a[sNAme] = d[sNAme]

    def get_impl_path(self, obj):
        """Путь к файлу, где определён класс"""
        file = inspect.getfile(obj.__class__)
        w = file.find('module')
        file = file[w:-3].replace('object', 'schemas')[:-3]
        return file