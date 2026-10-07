from core.sdk import SetOper

from module.bc.object.scheduledtasks.Bc_ScriptSchedulerPub import Bc_ScriptSchedulerPub
from module.bc.object.timeline.Bc_TimeLinePub import Bc_TimeLinePub

class Bc_MainMenuPub:
    class Default: 
        @SetOper(label="Справочник", order=10)
        def mm_res(self): pass

        @SetOper(label="Планировщик сценариев", order=10, headOper="mm_res")
        def mm_Bc_ScriptScheduler(self): 
            Bc_ScriptSchedulerPub.list().openForm()