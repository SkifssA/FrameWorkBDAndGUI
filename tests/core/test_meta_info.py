"""Парсинг JSON-метаданных в датаклассы (MetaInfo) и round-trip."""

import json

import pytest

from core.fabric.MetaInfo import MetaInfo
from core.dataClass.tabDataClass import tabShema, attrShema


ODB_JSON = {
    "name": "Anime",
    "caption": "Аниме",
    "attr": [
        {"name": "id", "caption": "id", "type": "INT", "isVisible": False},
        {"name": "name", "caption": "Название", "type": "TEXT", "isHeadLine": True},
        {"name": "year", "caption": "Год", "type": "INT", "order": 2},
    ],
    "collections": [{"name": "Awh_Genre", "attr": "idAnime"}],
    "dbData": [{"name": "seed", "version": 1}],
}

META_JSON = {
    "dep": "awh",
    "repres": [
        {
            "name": "Awh_AnimePub",
            "caption": "Аниме",
            "isVisibleToolBar": False,
            "filter": [
                {
                    "sql": "active = 1",
                    "attr": [{"name": "name", "caption": "Название", "type": "TEXT"}],
                }
            ],
            "attr": [
                {"name": "name", "caption": "Название", "isVisible": True, "order": 1},
                {"name": "hidden", "caption": "Скрытый", "isVisible": False},
            ],
        }
    ],
}


@pytest.fixture()
def write_json(tmp_path):
    def _write(data):
        p = tmp_path / "file.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return str(p)

    return _write


class TestGetMetaTab:
    def test_parses_all_sections(self, write_json):
        data = MetaInfo().getMetaTab(write_json(ODB_JSON))
        assert isinstance(data, tabShema)
        assert data.name == "Anime"
        assert [a.name for a in data.attr] == ["id", "name", "year"]
        assert data.attr[1].isHeadLine is True
        assert data.collections[0].attr == "idAnime"
        assert data.dbData[0].version == 1

    def test_optional_sections_absent(self, write_json):
        minimal = {"name": "T", "caption": "T"}
        data = MetaInfo().getMetaTab(write_json(minimal))
        assert data.attr == [] and data.collections == [] and data.dbData == []

    def test_getsql_contains_columns_and_service_fields(self, write_json):
        data = MetaInfo().getMetaTab(write_json(ODB_JSON))
        sql = data.getSQL()
        assert "CREATE TABLE Anime (" in sql
        assert "id INTEGER PRIMARY KEY AUTOINCREMENT" in sql
        assert "sMnemoCode TEXT UNIQUE" in sql
        assert "name TEXT" in sql and "year INTEGER" in sql

    def test_getsql_new_migration_suffix(self, write_json):
        data = MetaInfo().getMetaTab(write_json(ODB_JSON))
        data.isNew = True
        assert "CREATE TABLE Anime_new" in data.getSQL()

    def test_roundtrip_via_getdict(self, write_json):
        """getDict -> json -> getMetaTab должен давать эквивалентную схему."""
        original = MetaInfo().getMetaTab(write_json(ODB_JSON))
        dumped = json.loads(json.dumps(original.getDict(), ensure_ascii=False))
        restored = MetaInfo().getMetaTab(write_json(dumped))
        assert restored.getDict() == original.getDict()


class TestReadMeta:
    def test_parses_repres_and_dep(self, write_json):
        meta = MetaInfo().readMeta(write_json(META_JSON))
        assert meta.getDep() == "awh"
        ui = meta.getMetaUI()
        m = ui["Awh_AnimePub"]
        assert m.isVisibleToolBar is False
        assert m.filter[0].sql == "active = 1"
        assert isinstance(m.filter[0].attr[0], type(m.attr[0]))
        assert [a.name for a in m.attr] == ["name", "hidden"]

    def test_readmeta_resets_previous_state(self, write_json):
        info = MetaInfo()
        info.readMeta(write_json(META_JSON))
        info.readMeta(write_json({"repres": []}))
        assert info.getMetaUI() == {}

    def test_empty_file_safe(self, write_json):
        info = MetaInfo().readMeta(write_json({}))
        assert info.getMetaUI() == {}
        assert info.getDep() is None
