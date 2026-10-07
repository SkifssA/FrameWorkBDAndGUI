from core.package.Rect import Rect
from core.fabric.Registry import Registry

class EmptyPub:
    class Default:
        def __init__(self):
            self.rect = Rect(self)
            self.registry = Registry(self)

        def getData(self):
            self.rect.refresh()
            return self.rect.getData()

        def onRefresh(self):...
        def onRefreshExt(self):...
        def getAttr(self):...

    class List(Default):
        def onRefresh(self):
            return self.structuredQuery()

        def structuredQuery(self)->str:...