from core.sdk import SetOper

from module.awh.object.anime.Awh_AnimeAvi import Awh_AnimeAvi
from module.awh.object.animegenre.Awh_AnimeGenreAvi import Awh_AnimeGenreAvi
from module.awh.object.genre.Awh_GenreAvi import Awh_GenreAvi

class Awh_MainMenuAvi:
    class Default: 
        @SetOper(label="Справочник", order=10)
        def mm_res(self): pass

        @SetOper(label="Аниме", order=10, headOper="mm_res")
        def mm_Awh_Anime(self): 
            Awh_AnimeAvi.list().openForm()

        @SetOper(label="Жанры по аниме", order=20, headOper="mm_res")
        def mm_Awh_AnimeGenre(self): 
            Awh_AnimeGenreAvi.list().openForm()

        @SetOper(label="Жарны", order=30, headOper="mm_res")
        def mm_Awh_Genre(self): 
            Awh_GenreAvi.list().openForm()

        def oneOpen(self):
            Awh_AnimeAvi.list().openForm()
        