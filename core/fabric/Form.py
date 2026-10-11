from core.empty.pub import EmptyPub

class Form:
    def __init__(self, cls:EmptyPub.Default, clsParent:EmptyPub):
        self.object:EmptyPub.Default  = cls(clsParent)

    def getInfoMeta(self):
        return self.object._getInfoMeta()

    def getSetterAndOperName(self):
        return self.object._getSetterAndOperName()

    def getData(self):
        return self.object._getData()