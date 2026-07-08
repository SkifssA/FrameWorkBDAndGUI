# Пользовательский файл для интерфейса
from .Gmb_TaskDetDvi import Gmb_TaskDetDvi
from engine.fabric.Form import FormConstruct

class Gmb_TaskDetAvi(Gmb_TaskDetDvi):
    class List(Gmb_TaskDetDvi.DviList): pass

    class List_idTask(List): 
        def onRefresh(self):
            return f"""
                SELECT t.id,
                    t.gid,
                    t.idTask,
                    t1.sHeadLine as idTaskHL,
                    t.idMod,
                    t2.sHeadLine as idModHL
                FROM Gmb_TaskDet AS t
                    LEFT JOIN Gmb_Task t1 ON t1.id = t.idTask
                    LEFT JOIN Gmb_Mod t2 ON t2.id = t.idMod
                WHERE t.idTask = ${self.getAttr("super$id")}
                """

    class Card(Gmb_TaskDetDvi.DviCard): pass

    class LookUp(Gmb_TaskDetDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def list_idTask(cls)->FormConstruct:
        return FormConstruct(cls.List_idTask)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
