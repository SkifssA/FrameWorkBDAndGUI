import json
import os
import asyncio
import aiofiles
import inspect
from pathlib import Path
import yaml

class Core_AsyncFileManager:
    def _getObjPath(self, path: str, index=2):
        #os.getcwd()
        caller_frame = inspect.stack()[index]
        caller_file = caller_frame.filename
        caller_dir = Path(caller_file).parent

        # Преобразуем путь, разрешая точки (.. и .)
        # Например: '../data/config.json' -> поднимаемся на уровень выше
        real_path = (caller_dir / path).resolve()

        # Создаем директории, если их нет
        real_path.parent.mkdir(parents=True, exist_ok=True)

        # Определяем тип файла
        typeFile = path.rsplit('.', 1)[-1] if '.' in path else None
        
        return {'real_path': str(real_path), 'type': typeFile}

    async def CreateFile(self, path: str, data):
        obj = self._getObjPath(path)

        if obj['type'] in ['json', 'code-workspace']:
            await self._createJsonFile(obj['real_path'], data)
        else:
            await self._createDefaultFile(obj['real_path'], data)

    async def ReadFile(self, path):
        obj = self._getObjPath(path)

        if obj['type'] == 'json':
            return await self._readJsonFile(obj['real_path'])
        elif obj['type'] == 'yaml':
            return await self._readYamlFile(obj['real_path'])
        else:
            return await self._readDefaultFile(obj['real_path'])

    async def Exists(self, path):
        obj = self._getObjPath(path)
        return await asyncio.to_thread(os.path.exists, obj['real_path'])
    
    async def GetFoldersList(self, path):
        try:
            obj = self._getObjPath(path)
            folders = []
            for item in os.listdir(obj['real_path']):
                item_path = os.path.join(obj['real_path'], item)
                if os.path.isdir(item_path):
                    folders.append(item)
            return folders
        except Exception as e:
            return []
        
    async def getFilesWithExtension(self, directory: str, extension: str) -> list[Path]:
        """Асинхронно возвращает список файлов с заданным расширением."""
        obj = self._getObjPath(directory)
        def _sync_scan():
            path = Path(obj['real_path'])
            q = extension.split('.')
            if len(q) > 2:
                return [f for f in path.iterdir() if f.is_file() and f.suffix == f'.{q[-1]}' and f.stem.endswith(q[-2])]
            else:
                return [f for f in path.iterdir() if f.is_file() and f.suffix == f'.{q[-1]}']
        
        return await asyncio.to_thread(_sync_scan)

    async def _createJsonFile(self, real_path, data):
        async with aiofiles.open(real_path, 'w', encoding='utf-8') as f:
            content = json.dumps(data, ensure_ascii=False, indent=2)
            await f.write(content)

    async def _createDefaultFile(self, real_path, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        async with aiofiles.open(real_path, 'wb') as f:
            await f.write(data)

    async def _readJsonFile(self, real_path):
        try:
            async with aiofiles.open(real_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return json.loads(content)
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка: {e}"

    async def _readYamlFile(self, real_path):
        def _read():
            with open(real_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)

        data = await asyncio.to_thread(_read)
        return data

    async def _readDefaultFile(self, real_path):
        try:
            async with aiofiles.open(real_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return content
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка: {e}"

Core_FileManagerPkg = Core_AsyncFileManager()