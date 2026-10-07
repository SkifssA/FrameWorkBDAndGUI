from core.package.Rect import Rect

class EmptyAvi:
    class Default:
        def __init__(self):
            self.rect = Rect(self)

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