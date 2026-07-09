# Пользовательский файл для логики
from .Gmb_TaskDetDpi import Gmb_TaskDetDpi, Gmb_TaskDetObj

class Gmb_TaskDetApi(Gmb_TaskDetDpi):
    def register(self, idTask, idMod):
        obj = self.getByMnemocode(f'{idTask} {idMod}')
        if not obj:
            obj = self.insert()
            self.setidTask(obj, idTask)
            self.setidMod(obj, idMod)
        self.update(obj)
        return obj
