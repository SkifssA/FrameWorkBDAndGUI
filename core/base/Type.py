class Gid:
    def getIdClass(self)->str:
        return self.value[:self.value.find('/')]
    
    def getId(self)->str:
        return self.value[self.value.find('/')+1:]