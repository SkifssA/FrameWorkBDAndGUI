import json
import os
from pathlib import Path
import yaml

from core import ROOT


class FileManager:
    """Менеджер файлов"""

    def CreateFile(self, path: str, data):
        """Создаёт файлы"""
        obj = self._getObjPath(path)
        if obj["type"] in ["json", "code-workspace"]:
            self._createJsonFile(obj["real_path"], data)
        else:
            self._createDefaultFile(obj["real_path"], data)

    def ReadFile(self, path):
        """Читает файлы"""
        obj = self._getObjPath(path)

        if obj["type"] == "json":
            return self._readJsonFile(obj["real_path"])
        elif obj["type"] == "yaml":
            return self._readYamlFile(obj["real_path"])
        else:
            return self._readDefaultFile(obj["real_path"])

    def Exists(self, path):
        """Проверяет существование"""
        obj = self._getObjPath(path)
        return os.path.exists(obj["real_path"])

    def GetFoldersList(self, path):
        """Возвращает список папок"""
        try:
            obj = self._getObjPath(path)
            folders = []
            for item in os.listdir(obj["real_path"]):
                item_path = os.path.join(obj["real_path"], item)
                if os.path.isdir(item_path):
                    folders.append(item)
            return folders
        except Exception as e:
            return []

    def getFilesWithExtension(
        self, directory: str | dict, extension: str
    ) -> list[Path]:
        """Возвращает список файлов с заданным расширением."""
        if type(directory) == str:
            obj = self._getObjPath(directory)
        else:
            obj = directory

        def _sync_scan(path=None):
            if path is None:
                path = Path(obj["real_path"])
            q = extension.split(".")
            if len(q) > 2:
                w = [
                    f
                    for f in path.iterdir()
                    if f.is_file()
                    and f.suffix == f".{q[-1]}"
                    and f.stem.endswith(q[-2])
                ]
            else:
                w = [
                    f for f in path.iterdir() if f.is_file() and f.suffix == f".{q[-1]}"
                ]
            for d in path.iterdir():
                if d.is_dir():
                    w += _sync_scan(d)
            return w

        return _sync_scan()

    def getRealPath(self, path: str) -> str:
        return self._getObjPath(path=path)["real_path"]

    def _getObjPath(self, path: str):
        """Получает объект пути по строке с ."""
        # Определяем тип файла
        typeFile = path.rsplit(".", 1)[-1] if "." in path else None

        return {
            "real_path": path if path.startswith(str(ROOT)) else str(Path(ROOT) / path),
            "type": typeFile,
        }

    def _createJsonFile(self, real_path, data):
        """Создаёт json файлы"""
        with open(real_path, "w", encoding="utf-8") as f:
            content = json.dumps(data, ensure_ascii=False, indent=4)
            f.write(content)

    def _createDefaultFile(self, real_path, data):
        """Создаёт файлы"""
        os.makedirs(os.path.dirname(real_path), exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        with open(real_path, "wb") as f:
            f.write(data)

    def _readJsonFile(self, real_path):
        """Читает json файлы"""
        try:
            with open(real_path, "r", encoding="utf-8") as f:
                content = f.read()
            return json.loads(content)
        except FileNotFoundError:
            return {}
        except Exception as e:
            return f"Ошибка: {e}"

    def _readYamlFile(self, real_path):
        """Читает yaml файлы"""
        with open(real_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _readDefaultFile(self, real_path):
        """Читает файлы"""
        try:
            with open(real_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка: {e}"


FileManagerPkg = FileManager()
