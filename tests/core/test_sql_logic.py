"""Антиинъекционная валидация и сборка SQL в SQLLogic."""

import pytest

from core.DB.SQLLogic import SQLLogic


class DemoLogic(SQLLogic):
    def __init__(self, name="Anime"):
        self._name = name

    def _getNameClass(self):
        return self._name


@pytest.fixture()
def logic():
    return DemoLogic()


class TestValidate:
    def test_valid_identifiers(self, logic):
        logic._validate("Anime")
        logic._validate(["id", "name_1", "sHeadLine"])

    @pytest.mark.parametrize(
        "bad",
        [
            "Anime; DROP TABLE users",
            "Anime--",
            "Anime name",
            'Anime"',
            "",
            "Anime.2",
        ],
    )
    def test_injection_raises(self, logic, bad):
        with pytest.raises(ValueError, match="SQLValidate"):
            logic._validate(bad)

    def test_getNameClassValidate_propagates_error(self):
        logic = DemoLogic(name="Bad Name")
        with pytest.raises(ValueError):
            logic._getNameClassValidate()


class TestSqlBuilding:
    def test_deleteById(self, logic, monkeypatch_sql):
        logic._deleteById(7)
        call = monkeypatch_sql[0]
        assert call["sql"] == "DELETE FROM Anime WHERE id = ?"
        assert call["parameters"] == [7]

    def test_insert(self, logic, monkeypatch_sql):
        logic._insert()
        assert monkeypatch_sql[0]["sql"] == "INSERT INTO Anime (id) VALUES (NULL)"

    def test_getAll(self, logic, monkeypatch_sql):
        logic._getAll()
        assert monkeypatch_sql[0]["sql"] == "SELECT * FROM Anime"

    def test_getById_parameterized(self, logic, monkeypatch_sql):
        logic._getById(3)
        call = monkeypatch_sql[0]
        assert call["sql"] == "SELECT * FROM Anime WHERE id = ?"
        assert call["parameters"] == [3]

    def test_findDataBase_with_value(self, logic, monkeypatch_sql):
        logic._findDataBase("name", "onepiece")
        call = monkeypatch_sql[0]
        assert call["sql"] == "SELECT * FROM Anime WHERE name = ?"
        assert call["parameters"] == ["onepiece"]

    def test_findDataBase_none_uses_is_null(self, logic, monkeypatch_sql):
        """NULL не сравнивается через '= ?' — используется IS NULL без параметров."""
        logic._findDataBase("name", None)
        call = monkeypatch_sql[0]
        assert call["sql"] == "SELECT * FROM Anime WHERE name IS NULL"
        assert call["parameters"] is None

    def test_findDataBase_injection_in_attr_blocked(self, logic, monkeypatch_sql):
        with pytest.raises(ValueError):
            logic._findDataBase("name = 1 OR 1", "x")
        assert monkeypatch_sql == []  # запрос не должен быть отправлен

    def test_updateObj(self, logic, monkeypatch_sql):
        logic._updateObj(["name", "year"], {"name": "Naruto", "year": 2002, "id": 5})
        call = monkeypatch_sql[0]
        assert call["sql"] == "UPDATE Anime SET name = ?, year = ? WHERE id = ?"
        assert list(call["parameters"]) == ["Naruto", 2002, 5]

    def test_updateObj_injection_in_keys_blocked(self, logic, monkeypatch_sql):
        with pytest.raises(ValueError):
            logic._updateObj(["name; DROP TABLE x"], {"name; DROP TABLE x": "v", "id": 1})
        assert monkeypatch_sql == []
