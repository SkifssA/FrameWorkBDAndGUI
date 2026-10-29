from core.sdk import Oper, EmptyPub

from core.module.sc.object.cls.Sc_ClsPub import Sc_ClsPub

class Sc_MainMenuPub(EmptyPub):

    metaFile = 'Bc_MainMenu.Ameta.json'

    class Default(EmptyPub.MainMenu):
        @Oper(label="Справочник", order=10)
        def mm_res(self):
            pass

        @Oper(label="Классы", order=10, headOper="mm_res")
        def mm_Bc_ScriptScheduler(self):
            Sc_ClsPub.list().open()

        def onRefreshExt(self): return ""

    @classmethod
    def default(cls):
        return cls.Default(cls)
