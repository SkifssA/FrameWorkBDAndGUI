from core.sdk import SetOper

from module.awh.object.anime.Awh_AnimePub import Awh_AnimePub
from module.awh.object.animegenre.Awh_AnimeGenrePub import Awh_AnimeGenrePub
from module.awh.object.genre.Awh_GenrePub import Awh_GenrePub

class Awh_MainMenuPub:
    class Default: 
        @SetOper(label="Справочник", order=10)
        def mm_res(self): pass

        @SetOper(label="Аниме", order=10, headOper="mm_res")
        def mm_Awh_Anime(self): 
            Awh_AnimePub.list().openForm()

        @SetOper(label="Жанры по аниме", order=20, headOper="mm_res")
        def mm_Awh_AnimeGenre(self): 
            Awh_AnimeGenrePub.list().openForm()

        @SetOper(label="Жарны", order=30, headOper="mm_res")
        def mm_Awh_Genre(self): 
            Awh_GenrePub.list().openForm()

        def oneOpen(self):
            Awh_AnimePub.list().openForm()
        