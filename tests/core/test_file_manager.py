"""FileManager: чтение/запись json/yaml/обычных файлов, поиск по расширению."""

import json

from core.package.FileManager import FileManagerPkg


class TestJsonRoundtrip:
    def test_create_and_read_json(self, tmp_path):
        p = str(tmp_path / "data.json")
        FileManagerPkg.CreateFile(p, {"ключ": "значение", "n": 1})
        assert FileManagerPkg.ReadFile(p) == {"ключ": "значение", "n": 1}

    def test_read_missing_json_returns_empty_dict(self, tmp_path):
        assert FileManagerPkg.ReadFile(str(tmp_path / "absent.json")) == {}


class TestTextAndYaml:
    def test_create_parent_dirs_and_read_text(self, tmp_path):
        p = str(tmp_path / "nested" / "deep" / "file.txt")
        FileManagerPkg.CreateFile(p, "привет")
        assert FileManagerPkg.ReadFile(p) == "привет"

    def test_binary_data_written_as_bytes(self, tmp_path):
        p = str(tmp_path / "raw.bin.txt")
        FileManagerPkg.CreateFile(p, b"\x01\x02")
        assert open(p, "rb").read() == b"\x01\x02"

    def test_read_yaml(self, tmp_path):
        p = tmp_path / "conf.yaml"
        p.write_text("modules:\n  - awh\n  - bc\n", encoding="utf-8")
        assert FileManagerPkg.ReadFile(str(p)) == {"modules": ["awh", "bc"]}


class TestHelpers:
    def test_exists(self, tmp_path):
        p = tmp_path / "here.txt"
        p.write_text("x")
        assert FileManagerPkg.Exists(str(p)) is True
        assert FileManagerPkg.Exists(str(tmp_path / "nope.txt")) is False

    def test_get_folders_list(self, tmp_path):
        (tmp_path / "sub1").mkdir()
        (tmp_path / "sub2").mkdir()
        (tmp_path / "file.txt").write_text("")
        assert sorted(FileManagerPkg.GetFoldersList(str(tmp_path))) == ["sub1", "sub2"]

    def test_get_folders_list_bad_path_returns_empty(self, tmp_path):
        assert FileManagerPkg.GetFoldersList(str(tmp_path / "ghost")) == []

    def test_get_files_with_extension_recursive(self, tmp_path):
        (tmp_path / "a.odb.json").write_text("{}")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "b.odb.json").write_text("{}")
        (sub / "c.json").write_text("{}")
        found = FileManagerPkg.getFilesWithExtension(str(tmp_path), ".odb.json")
        assert sorted(f.name for f in found) == ["a.odb.json", "b.odb.json"]

    def test_get_real_path_absolute_untouched(self, tmp_path):
        p = str(tmp_path / "x.txt")
        assert FileManagerPkg.getRealPath(p) == p
