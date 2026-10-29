"""Генераторы кода (builders): golden-тесты текста, защита ручного кода, опциональные поля."""

import ast

import pytest

from core.createClass.buildersClass.builderBase import builderBase
from core.createClass.buildersClass.builderDpi import builderDpi
from core.createClass.buildersClass.builderLogic import builderLogic
from core.dataClass.tabDataClass import attrSchema, collectionsSchema, tabSchema


@pytest.fixture()
def tab():
    # Имя таблицы с префиксом модуля (как в реальных проектах: Awh_Anime) —
    # генератор вычисляет module.{префикс} через getModule(name).
    return tabSchema(
        name="Awh_Anime",
        caption="Аниме",
        attr=[
            attrSchema(name="id", caption="id", type="INT"),
            attrSchema(
                name="sCaption", caption="Название", type="TEXT", isHeadLine=True
            ),
            attrSchema(name="sUrl", caption="Код", type="TEXT", isMnemoCode=True),
        ],
        collections=[],
    )


@pytest.fixture()
def captured_files(monkeypatch):
    """Перехватывает запись файлов генераторами: FileManager.CreateFile -> dict."""
    written = {}
    monkeypatch.setattr(
        "core.package.FileManager.FileManagerPkg.CreateFile",
        lambda path, data: written.__setitem__(path, data),
    )
    return written


class TestGeneratedText:
    def test_dpi_golden_structure(self, tab, captured_files):
        builderDpi(tab).createFileD("out")
        code = captured_files["out/Awh_AnimeDpi.py"]
        assert "class Awh_AnimeObj(EmptyObj):" in code
        assert "class Awh_AnimeDpi(EmptyLogic[Awh_AnimeObj]):" in code
        assert 'return "Awh_Anime"' in code      # _getNameClass
        assert "{rop.sCaption}" in code          # headline из isHeadLine
        assert "{rop.sUrl}" in code              # mnemocode из isMnemoCode
        assert "def setsCaption(self, obj:Awh_AnimeObj, value)" in code
        # id объявлен один раз (обязательное поле), дублей нет
        assert code.count("id:int") == 1

    def test_generated_dpi_is_valid_python(self, tab, captured_files):
        """Сгенерированный код обязан быть синтаксически корректным."""
        builderDpi(tab).createFileD("out")
        ast.parse(captured_files["out/Awh_AnimeDpi.py"])

    def test_logic_template_minimal(self, tab, captured_files):
        builderLogic(tab).createFileD("out")
        code = captured_files["out/Awh_AnimeLogic.py"]
        assert "from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj" in code
        assert "class Awh_AnimeLogic(Awh_AnimeDpi):" in code

    def test_headline_fallback_to_id(self, captured_files):
        tab = tabSchema(
            name="Awh_Genre",
            caption="Жанр",
            attr=[attrSchema(name="id", caption="id", type="INT")],
        )
        builderDpi(tab).createFileD("out")
        assert "return f'{rop.id}'" in captured_files["out/Awh_GenreDpi.py"]

    def test_delete_details_for_collections(self, captured_files, monkeypatch):
        """Модуль для collection берётся из реестра классов sc (Sc_ClsLogic),
        а не из соглашения имён."""
        from core.module.sc.object.cls.Sc_ClsLogic import Sc_ClsLogic

        monkeypatch.setattr(
            Sc_ClsLogic, "getPrefixModule", lambda self, code: "awh", raising=True
        )
        tab = tabSchema(
            name="Awh_Anime",
            caption="Аниме",
            attr=[attrSchema(name="id", caption="id", type="INT")],
            collections=[collectionsSchema(name="Awh_Genre", attr="idAnime")],
        )
        builderDpi(tab).createFileD("out")
        code = captured_files["out/Awh_AnimeDpi.py"]
        assert "from module.awh import Awh_GenreLogic" in code
        assert "getAllByAttr('idAnime', obj.id)" in code


class TestCreateFileBehaviour:
    def test_createfilea_does_not_overwrite(self, tab, monkeypatch):
        """createFileA защищает пользовательский код (Logic/Pub) от перезаписи."""
        exists = {"yes": False}
        monkeypatch.setattr(
            "core.package.FileManager.FileManagerPkg.Exists",
            lambda path: exists["yes"],
        )
        created = []
        monkeypatch.setattr(
            "core.package.FileManager.FileManagerPkg.CreateFile",
            lambda path, data: created.append(path),
        )

        builderLogic(tab).createFileA("out")
        assert created == ["out/Awh_AnimeLogic.py"]

        exists["yes"] = True  # файл пользователя уже существует
        builderLogic(tab).createFileA("out")
        assert created == ["out/Awh_AnimeLogic.py"]  # повторной записи нет

    def test_createfiled_always_overwrites(self, tab, monkeypatch):
        monkeypatch.setattr(
            "core.package.FileManager.FileManagerPkg.Exists", lambda path: True
        )
        created = []
        monkeypatch.setattr(
            "core.package.FileManager.FileManagerPkg.CreateFile",
            lambda path, data: created.append(path),
        )
        builderDpi(tab).createFileD("out")
        assert created == ["out/Awh_AnimeDpi.py"]

    def test_path_and_suffix(self, tab):
        b = builderDpi(tab)
        assert b._getPathAndFile("module/awh/object/anime") == (
            "module/awh/object/anime/Awh_AnimeDpi.py"
        )


class TestTemplateRobustness:
    def test_empty_attr_list_still_renders(self, captured_files):
        """Генератор не падает на пустом списке атрибутов и выдаёт валидный код.

        Регрессия на старый дефект шаблона: при attr=[] печаталось `\" = None\"`.
        """
        empty = tabSchema(name="T", caption="T", attr=[])
        builderDpi(empty).createFileD("out")
        code = captured_files["out/TDpi.py"]
        assert "class TDpi(EmptyLogic[TObj]):" in code
        assert "return f'{rop.id}'" in code  # fallback headline/mnemocode на id
        assert "= None" not in code          # мусорных строк от пустого attrObj нет
        ast.parse(code)                      # синтаксис корректен

    def test_no_collections_gives_empty_delete_block(self, captured_files):
        tab = tabSchema(
            name="Awh_X",
            caption="X",
            attr=[attrSchema(name="id", caption="i", type="INT")],
        )
        builderDpi(tab).createFileD("out")
        code = captured_files["out/Awh_XDpi.py"]
        # в delete() нет импортов других логик
        assert "Logic().delete(i)" not in code

    def test_builderbase_merges_dictdata(self, tab, captured_files):
        class Custom(builderBase):
            temp = "NAME={name}; EXTRA={extra}"
            suffixFile = ".txt"

            def __init__(self, data):
                super().__init__(data)
                self.dictData["extra"] = "42"

        Custom(tab).createFileD("out")
        assert captured_files["out/Awh_Anime.txt"] == "NAME=Awh_Anime; EXTRA=42"
