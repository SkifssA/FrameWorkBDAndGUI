"""Тесты ядра NecoTab (без БД и без реального GUI).

Запуск:  python -m pytest tests -q     (или python tests/test_core.py)

Покрывает публичное API ядра:
- FileManagerPkg: пути от корня проекта, чтение json/yaml/txt;
- ActionDispatcherPkg: импорт модулей по строке 'Class.method', ошибки;
- Gid: разбор идентификатора;
- Base/Template Method: каркас формы, хуки, Config;
- SelectApp/AppCard: сигнал openRequested (карточка не лезет в окно);
- MetadataManager: слияние Ameta/Dmeta.
"""
import sys, os, asyncio, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from core.package.FileManager import FileManagerPkg, project_root
from core.package.ActionDispatcher import ActionDispatcherPkg
from core.type.Gid import Gid
from core.ui.forms.base import Base as Base_
from core.fabric.Form import FormConstruct as FormConstruct_


class TestPaths(unittest.TestCase):
    def test_project_root(self):
        self.assertTrue((project_root() / "project.yaml").exists())
        self.assertTrue((project_root() / "core" / "config" / "config.json").exists())

    def test_resolve_stays_inside_root(self):
        # '..' не должен выпускать за пределы проекта
        p = Path(FileManagerPkg.getRealPath("../../etc/passwd"))
        self.assertEqual(p, project_root())

    def test_read_yaml_and_json(self):
        cfg = asyncio.run(FileManagerPkg.ReadFile("core/config/config.json"))
        self.assertEqual(cfg["nameApp"], "NecoTab")
        proj = asyncio.run(FileManagerPkg.ReadFile("project.yaml"))
        self.assertIn("modules", proj)

    def test_missing_file_returns_message(self):
        r = asyncio.run(FileManagerPkg.ReadFile("no/such/file.json"))
        self.assertEqual(r, "Файл не найден")


class TestGid(unittest.TestCase):
    def test_parse(self):
        g = Gid("7/42")
        self.assertEqual(g.getIdClass(), 7)
        self.assertEqual(g.getId(), 42)
        self.assertEqual(g.get(), "7/42")

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            Gid("abc").getIdClass()


class TestActionDispatcher(unittest.TestCase):
    def test_class_method_string(self):
        # публичный контракт: строка "Class.method" резолвится в модуле-префиксе
        d = ActionDispatcherPkg()
        cls = d._getMethod(__import__("module.bc.object.Bc_ScriptSchedulerPkg",
                                      fromlist=["x"]).Bc_ScriptSchedulerPkg,
                          "run", classMethod=True)
        self.assertTrue(callable(cls))
        # и наоборот — несуществующий метод падает явно, а не молча возвращает None
        with self.assertRaises(AttributeError):
            d.action("Bc_ScriptSchedulerPkg.no_such_method", classMethod=True)

    def test_unknown_class_in_existing_module(self):
        # класс отсутствует в существующем модуле -> AttributeError (контракт API)
        with self.assertRaises(AttributeError):
            ActionDispatcherPkg().action("Bc_NoSuchClass.bar", classMethod=True)

    def test_unknown_module_raises(self):
        with self.assertRaises(ValueError):
            ActionDispatcherPkg().action("NoSuch_Class.doIt", classMethod=True)


# --- фикстуры для Template Method: классы ДОЛЖНЫ быть на уровне модуля,
# иначе inspect.getfile() не сможет найти их файл (локальные классы «встроенные»)
class _ChildForm(Base_):
    def _createMainFrameWidget(self):
        from PyQt6.QtWidgets import QLabel
        return QLabel("child")


class _ParentForm(Base_):
    def _createMainFrameWidget(self):
        from PyQt6.QtWidgets import QLabel
        return QLabel("parent")

    def getChilders(self):
        yield FormConstruct_(_ChildForm)


class TestForms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def test_base_template_method(self):
        p = _ParentForm()
        self.assertEqual(p.caption, p.metaInfo.get('caption', 'НАЗВАНИЯ НЕТ'))
        # дочерняя группа собрана и formParent проставлен.
        # ВАЖНО: тестовые классы объявлены в файле теста (не в module/...),
        # поэтому Metadata.get вернёт дефолт {'isVisibleToolBar': False} —
        # тулбар не строится и кнопок нет; проверяем сам каркас.
        children = [w for w in p.findChildren(Base_) if w is not p]
        self.assertEqual(len(children), 1)
        self.assertIs(children[0].formParent, p)
        # для классов вне module/ Metadata возвращает дефолт isVisibleToolBar=False,
        # поэтому тулбар не строится; registry всё равно инициализирован
        self.assertIsNotNone(p.registry)

    def test_appcard_emits_signal_not_navigation(self):
        from core.ui.forms.selectApp import AppCard
        card = AppCard({"name": "T", "description": "d"})
        got = []
        card.openRequested.connect(lambda d: got.append(d))
        card.findChild(__import__("PyQt6.QtWidgets", fromlist=["QPushButton"]).QPushButton).click()
        self.assertEqual(got, [{"name": "T", "description": "d"}])

    def test_metadata_for_real_module_class(self):
        # публичный контракт MetadataManager.get: слияние Ameta+Dmeta для
        # РЕАЛЬНОЙ формы модуля awh (List определён в Awh_AnimeAvi.py, схема —
        # module/awh/schemas/anime/Awh_Anime.{Ameta,Dmeta}.json)
        from core.package.MetadataManager import MetadataManager
        from module.awh.object.anime.Awh_AnimeAvi import Awh_AnimeAvi
        meta = MetadataManager().get(Awh_AnimeAvi.List())
        self.assertIsInstance(meta, dict)
        self.assertIn('caption', meta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
