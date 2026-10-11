from core.empty.pub import EmptyPub

class Form:
    def __init__(self, cls:EmptyPub.Default, clsParent:EmptyPub):
        self.object:EmptyPub.Default  = cls(clsParent)

    def getInfoMeta(self):
        return self.object.getInfoMeta()

    def getData(self):
        return self.object.getData()