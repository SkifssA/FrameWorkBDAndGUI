from core.form.MainMenu import mainMenu
from core.base.oper import SetOper

from .anime.Awh_AnimeAvi import Awh_AnimeAvi
from .genre.Awh_GenreAvi import Awh_GenreAvi

class Awh_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        def firstFrame(self):
            return Awh_AnimeAvi.list()

        @SetOper(label="Справочники")
        def mm_respo(self): pass

        @SetOper(label='Аниме', order=1, headOper='mm_respo')
        async def Awh_Anime(self):
            await Awh_AnimeAvi.list().open()

        @SetOper(label='Жанры', order=2, headOper='mm_respo')
        async def Awh_Genre(self):
            await Awh_GenreAvi.list().open()
        