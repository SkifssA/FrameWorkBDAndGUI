from engineQT.sdk import EmptyAvi
from core.sdk import SetOper

from module.bc.object.scheduledtasks.Bc_ScriptSchedulerAvi import Bc_ScriptSchedulerAvi
from module.bc.object.timeline.Bc_TimeLineAvi import Bc_TimeLineAvi

class Bc_MainMenuAvi:
    class Default(EmptyAvi.MainMenu): 
        @SetOper(label="Справочник", order=10)
        def mm_res(self): pass

        @SetOper(label="Планировщик сценариев", order=10, headOper="mm_res")
        def mm_Bc_ScriptScheduler(self): 
            Bc_ScriptSchedulerAvi.list().openForm()