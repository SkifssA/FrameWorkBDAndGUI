# Пользовательский файл для интерфейса
from .Gmb_TaskDvi import Gmb_TaskDvi
from engine.fabric.Form import FormConstruct
from engine.base.oper import SetOper
from modules.gmb.object.Gmb_GitManagerPkg import GitFabric
from modules.gmb.object.mod.Gmb_ModApi import Gmb_ModApi
from modules.gmb.object.taskdet.Gmb_TaskDetApi import Gmb_TaskDetApi
from modules.gmb.object.Gmb_GitLabManagerPkg import Gmb_GitLabManagerPkg

class Gmb_TaskAvi(Gmb_TaskDvi):
    class List(Gmb_TaskDvi.DviList): 
        def openCh(self):
            from modules.gmb import Gmb_TaskDetAvi
            yield Gmb_TaskDetAvi.list().param(locat='right')

        @SetOper(label='Провести по процессу', img='8', order=10)
        async def openWeb(self):
            for repo in GitFabric():
                idMod = Gmb_ModApi().findByMnemocode(repo.name)
                Gmb_TaskDetApi().register(self.thisRop().id, idMod)

            if lobjTaskDet := Gmb_TaskDetApi()._getAllByAttr('idTask', self.thisRop().id):
                sBranch = "iss/{Label}/{taskIdOrText}".format(
                    Label='feat',
                    taskIdOrText = x if (x:=self.thisRop().nNumTask) else self.thisRop().sCapTask.replace(' ', '-')
                )

                sCommit = "{Label}({Modules}): {Text} #issue {idTask}".format(
                    idTask=x if (x:=self.thisRop().nNumTask) else 'notask'
                    , Label='feat'
                    , Text=self.thisRop().sCapTask
                    , Modules=', '.join(list(Gmb_ModApi().load(i.idMod).sCaption for i in lobjTaskDet or []))
                )
                print(sBranch, sCommit)

                for repo in GitFabric(list(Gmb_ModApi().load(i.idMod).sCaption for i in lobjTaskDet)):
                        repo.allProcces(sBranch, sCommit)

                        Gmb_GitLabManagerPkg().createMR(self.getAttr('id'), sCommit, sBranch)

            

    class Card(Gmb_TaskDvi.DviCard): pass

    class LookUp(Gmb_TaskDvi.DviLookUp): pass

    @classmethod
    def list(cls)->FormConstruct:
        return FormConstruct(cls.List)
    
    @classmethod
    def card(cls)->FormConstruct:
        return FormConstruct(cls.Card)
