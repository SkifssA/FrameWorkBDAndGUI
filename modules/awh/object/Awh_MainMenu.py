from core.empty.MainMenu import mainMenu
from core.base.oper import SetOper

from .anime.Awh_AnimeAvi import Awh_AnimeAvi
from .genre.Awh_GenreAvi import Awh_GenreAvi
from .animegenre.Awh_AnimeGenreAvi import Awh_AnimeGenreAvi

class Awh_MainMenu(mainMenu):
    class Default(mainMenu.Default):
        def firstFrame(self):
            return Awh_AnimeAvi.list()

        @SetOper(label="Справочники")
        def mm_respo(self): pass

        @SetOper(label='Аниме', order=1, headOper='mm_respo')
        def Awh_Anime(self):
            Awh_AnimeAvi.list().param(parent=self).open()

        @SetOper(label='Жанры', order=2, headOper='mm_respo')
        def Awh_Genre(self):
            Awh_GenreAvi.list().param(parent=self).open()
        