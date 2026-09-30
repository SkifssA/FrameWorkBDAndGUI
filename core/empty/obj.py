class EmptyObj:
    def __init__(self):
        self.id:int = None
        self.gid:str = None

    def __str__(self):
        return f'{self.__class__.__name__}#{self.id}'