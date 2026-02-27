class Gid:
    def __init__(self, value:str):
        self.value = value

    def get(self):
        return self.value

    def getIdClass(self)->str:
        return int(self.value[:self.value.find('/')])
    
    def getId(self)->str:
        return int(self.value[self.value.find('/')+1:])