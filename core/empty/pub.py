from core.package.Rect import Rect
from core.fabric.Registry import Registry
from core.package.MetadataManager import MetadataManager

class EmptyPub:
    class Default:
        def __init__(self):
            self.rect = Rect(self)
            self.metaInfo = MetadataManager().get(self)

            self.registry = Registry(self)
            self.registry.oper()
            self.registry.setter()

        def getData(self):
            self.rect.refresh()
            return self.rect.getData()

        def onRefresh(self):...
        def onRefreshExt(self):...
        def getAttr(self):...
        def save(self):...
        def delete(self):...

    class List(Default):
        def onRefresh(self):
            return self.structuredQuery()

        def structuredQuery(self)->str:...