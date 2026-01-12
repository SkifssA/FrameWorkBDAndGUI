from core.base.BaseMainMenu import mainMenu
from core.base.BaseOper import SetOper

from .anime.Awh_AnimeAvi import Awh_AnimeAvi
from .genre.Awh_GenreAvi import Awh_GenreAvi

class Awh_MainMenu(mainMenu):
    @SetOper(label="Справочники")
    def mm_respo(self): pass

    @SetOper(label='Аниме', order=1, headOper='mm_respo')
    async def Bc_Config(self):
        await Awh_AnimeAvi.list().open()

    @SetOper(label='Жанры', order=2, headOper='mm_respo')
    async def Bc_ScriptScheduler(self):
        await Awh_GenreAvi.list().open()
        