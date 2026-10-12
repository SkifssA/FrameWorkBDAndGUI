"""Генераторы кода (bilders): golden-тесты текста, защита ручного кода, опциональные поля."""

from dataclasses import dataclass, field

import pytest

from core.createClass.bildersClass.bilderBase import BilderBase
from core.createClass.bildersClass.bilderDpi import BilderDpi
from core.createClass.bildersClass.bilderLogic import BilderLogic
from core.dataClass.tabDataClass import tabShema, attrShema, collectionsShema


@pytest.fixture()
def tab():
    # Имя таблицы с префиксом модуля (как в реальных проектах: Awh_Anime) —
    # генератор вычисляет module.{префикс} через getModule(name).
    return tabShema(
        name="Awh_Anime",
        caption="Аниме",
        attr=[
            attrShema(name="id", caption="id", type="INT"),
            attrShema(
                name="sCaption", caption="Название", type="TEXT", isHeadLine=True
            ),
            attrShema(name="sUrl", caption="Код", type="TEXT", isMnemoCode=True),
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
        BilderDpi(tab).createFileD("out")
        code = captured_files["out/Awh_AnimeDpi.py"]
        assert "class Awh_AnimeObj(EmptyObj):" in code
        # Известное отклонение от шаблона в core.sdk: генератор всегда пишет
        # `EmptyLogic` без параметра [Obj], хотя модули в project сгенерированы
        # со старым шаблоном `EmptyLogic[Obj]`. Зафиксируем фактическое поведение.
        assert "class Awh_AnimeDpi(EmptyLogic):" in code
        assert 'return "Awh_Anime"' in code      # _getNameClass
        assert "{rop.sCaption}" in code          # headline из isHeadLine
        assert "{rop.sUrl}" in code              # mnemocode из isMnemoCode
        assert "def setsCaption(self, obj:Awh_AnimeObj, value)" in code

    def test_logic_template_minimal(self, tab, captured_files):
        BilderLogic(tab).createFileD("out")
        code = captured_files["out/Awh_AnimeLogic.py"]
        assert "from .Awh_AnimeDpi import Awh_AnimeDpi, Awh_AnimeObj" in code
        assert "class Awh_AnimeLogic(Awh_AnimeDpi):" in code

    def test_headline_fallback_to_id(self, captured_files):
        tab = tabShema(
            name="Awh_Genre",
            caption="Жанр",
            attr=[attrShema(name="id", caption="id", type="INT")],
        )
        BilderDpi(tab).createFileD("out")
        assert "return f'{rop.id}'" in captured_files["out/Awh_GenreDpi.py"]

    def test_delete_details_for_collections(self, captured_files):
        tab = tabShema(
            name="Awh_Anime",
            caption="Аниме",
            attr=[attrShema(name="id", caption="id", type="INT")],
            collections=[collectionsShema(name="Awh_Genre", attr="idAnime")],
        )
        BilderDpi(tab).createFileD("out")
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

        BilderLogic(tab).createFileA("out")
        assert created == ["out/Awh_AnimeLogic.py"]

        exists["yes"] = True  # файл пользователя уже существует
        BilderLogic(tab).createFileA("out")
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
        BilderDpi(tab).createFileD("out")
        assert created == ["out/Awh_AnimeDpi.py"]

    def test_path_and_suffix(self, tab):
        b = BilderDpi(tab)
        assert b._getPathAndFile("module/awh/object/anime") == (
            "module/awh/object/anime/Awh_AnimeDpi.py"
        )


class TestTemplateRobustness:
    def test_empty_attr_list_still_renders(self, captured_files):
        """Генератор не падает на пустом списке атрибутов.

        Известный дефект шаблона: при attr=[] строка `id:int` всё равно
        печатается из-за литерала в шаблоне, а `{attrObj}` даёт `" = None"` —
        итоговый код синтаксически некорректен. Тест фиксирует фактическое
        поведение и защищает от регрессий (например, KeyError при format).
        """
        empty = tabShema(name="T", caption="T", attr=[])
        BilderDpi(empty).createFileD("out")
        code = captured_files["out/TDpi.py"]
        assert "class TDpi(EmptyLogic):" in code
        assert "return f'{rop.id}'" in code  # fallback headline/mnemocode на id
        assert "\n     = None\n" in code  # зафиксированный дефект пустого attrObj

    def test_no_collections_gives_empty_delete_block(self, captured_files):
        tab = tabShema(
            name="Awh_X",
            caption="X",
            attr=[attrShema(name="id", caption="i", type="INT")],
        )
        BilderDpi(tab).createFileD("out")
        code = captured_files["out/Awh_XDpi.py"]
        # в delete() нет импортов других логик
        assert "Logic().delete(i)" not in code

    def test_bilderbase_merges_dictdata(self, tab, captured_files):
        class Custom(BilderBase):
            temp = "NAME={name}; EXTRA={extra}"
            suffixFile = ".txt"

            def __init__(self, data):
                super().__init__(data)
                self.dictData["extra"] = "42"

        Custom(tab).createFileD("out")
        assert captured_files["out/Awh_Anime.txt"] == "NAME=Awh_Anime; EXTRA=42"