"""Контракт безопасности ModuleManagerPkg: парсинг sAction, поведение action(), хуки."""

import types

import pytest

from core.package.ModuleManagerPkg import ModuleManagerPkg, getModule


@pytest.fixture()
def mgr():
    return ModuleManagerPkg()


class TestGetModule:
    def test_prefix_before_underscore_lowercased(self):
        assert getModule("Awh_AnimeDpi") == "awh"

    def test_no_underscore_slices_off_last_char(self):
        """Текущее поведение find("_") == -1: срез nameClass[:-1].

        Фиксируем как регрессионный тест: имена классов без "_" обрабатываются
        некорректно (теряют последний символ). См. CONVENTION_MODULE_NAMING.md —
        все классы должны иметь префикс модуля через "_".
        """
        assert getModule("Mainmenu") == "mainmen"


class TestParseAction:
    def test_valid_action(self, mgr):
        assert mgr._parseAction("Awh_AnimeLogic.get") == ("Awh_AnimeLogic", "get")

    @pytest.mark.parametrize(
        "bad",
        [
            "Awh_AnimeLogic.",       # пустое имя метода
            ".get",                  # пустое имя класса
            "",                      # пустая строка
            "NoDotMethod",           # нет точки вообще
            "Awh_AnimeLogic.get.more",  # лишняя точка в имени метода
        ],
    )
    def test_invalid_format_raises(self, mgr, bad):
        with pytest.raises(AttributeError):
            mgr._parseAction(bad)

    @pytest.mark.parametrize(
        "private",
        ["Awh_AnimeLogic._deleteById", "Awh_AnimeLogic.__init__"],
    )
    def test_private_methods_forbidden(self, mgr, private):
        """Приватные/служебные методы недоступны через контракт sAction."""
        with pytest.raises(AttributeError):
            mgr._parseAction(private)


class TestActionDispatch:
    def _install_fake_module(self, monkeypatch, cls):
        # getModule("Fake_Pub") -> "fake"; контракт имён: Class_<...>
        fake = types.ModuleType("module.fake")
        fake.Fake_Pub = cls
        monkeypatch.setitem(__import__("sys").modules, "module.fake", fake)

    def test_instance_method_call(self, mgr, monkeypatch):
        class Fake_Pub:
            def get(self, x):
                return x * 2

        self._install_fake_module(monkeypatch, Fake_Pub)
        assert mgr.action("Fake_Pub.get", {"x": 21}) == 42

    def test_class_method_call(self, mgr, monkeypatch):
        class Fake_Pub:
            @staticmethod
            def get(y):
                return y + 1

        self._install_fake_module(monkeypatch, Fake_Pub)
        assert mgr.action("Fake_Pub.get", {"y": 1}, classMethod=True) == 2

    def test_missing_method_returns_none_and_logs(self, mgr, monkeypatch, capsys):
        class Fake_Pub:
            pass

        self._install_fake_module(monkeypatch, Fake_Pub)
        # Публичный action глотает исключения — контракт: не ронять вызывающий код
        assert mgr.action("Fake_Pub.absent") is None
        assert "не найден" in capsys.readouterr().out

    def test_missing_module_raises_valueerror_in_private_action(self, mgr):
        with pytest.raises(ValueError, match="Не удалось импортировать модуль"):
            mgr._action("NoSuch_Module.method")

    def test_public_action_swallows_import_error(self, mgr, capsys):
        assert mgr.action("NoSuch_Module.method") is None
        assert "завершился с ошибкой" in capsys.readouterr().out


class TestRunHook:
    def test_hooks_isolated_per_module(self, mgr, monkeypatch, capsys):
        """Ошибка в хуке одного модуля не блокирует другие модули."""

        class GoodPub:
            def on_start(self):
                return "ok"

        class BadPub:
            def on_start(self):
                raise RuntimeError("boom")

        calls = []

        def fake_action(sAction, kattr, classMethod):
            calls.append(sAction)
            if sAction.startswith("BadPub"):
                raise RuntimeError("boom")
            return None

        monkeypatch.setattr(mgr, "_action", fake_action)
        mgr.cacheHooks = {
            "good": {"on_startup": {"name": "GoodPub.on_start", "isClassMethod": False}},
            "bad": {"on_startup": {"name": "BadPub.on_start", "isClassMethod": False}},
            "empty": {},
        }

        mgr.runHook("on_startup")

        assert len(calls) == 2  # оба модуля попробованы
        out = capsys.readouterr().out
        assert "Хук 'on_startup' модуля 'bad'" in out

    def test_hook_without_action_skipped(self, mgr, monkeypatch):
        calls = []
        monkeypatch.setattr(
            mgr, "_action", lambda **kw: calls.append(kw["sAction"])
        )
        mgr.cacheHooks = {"m1": {"other_hook": {"name": "X.y"}}}
        mgr.runHook("on_startup")
        assert calls == []
