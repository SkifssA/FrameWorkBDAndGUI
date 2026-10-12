from core.sdk import Oper, EmptyPub

from module.bc.object.scheduledtasks.Bc_ScriptSchedulerPub import Bc_ScriptSchedulerPub
from module.bc.object.timeline.Bc_TimeLinePub import Bc_TimeLinePub
from core.sdk import Form



class Bc_MainMenuPub(EmptyPub):

    metaFile = 'Bc_MainMenu.Ameta.json'

    class Default(EmptyPub.MainMenu):
        @Oper(label="Справочник", order=10)
        def mm_res(self):
            pass

        @Oper(label="Планировщик сценариев", order=10, headOper="mm_res")
        def mm_Bc_ScriptScheduler(self):
            Bc_ScriptSchedulerPub.list().openForm()

        def onRefreshExt(self): return ""

    @classmethod
    def default(cls):
        return Form(cls.Default, cls)
