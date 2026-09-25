import json
import os
import asyncio
import aiofiles
from pathlib import Path
import yaml

from core import ROOT

class AsyncFileManager:
    """Менеджер файлов"""
    async def CreateFile(self, path: str, data):
        """Асинхронно создаёт файлы файлы"""
        obj = self._getObjPath(path)
        if obj['type'] in ['json', 'code-workspace']:
            await self._createJsonFile(obj['real_path'], data)
        else:
            await self._createDefaultFile(obj['real_path'], data)

    async def ReadFile(self, path):
        """Асинхронно читает файлы"""
        obj = self._getObjPath(path)

        if obj['type'] == 'json':
            return await self._readJsonFile(obj['real_path'])
        elif obj['type'] == 'yaml':
            return await self._readYamlFile(obj['real_path'])
        else:
            return await self._readDefaultFile(obj['real_path'])

    async def Exists(self, path):
        """Асинхронно проверяет существование"""
        obj = self._getObjPath(path)
        return await asyncio.to_thread(os.path.exists, obj['real_path'])
    
    async def GetFoldersList(self, path, index=0):
        """Асинхронно возвращает список папок"""
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
        
    async def getFilesWithExtension(self, directory: str| dict, extension: str, index=0) -> list[Path]:
        """Асинхронно возвращает список файлов с заданным расширением."""
        if (type(directory) == str):
            obj = self._getObjPath(directory)
        else:
            obj = directory
            
        def _sync_scan(path=None):
            if path is None:
                path = Path(obj['real_path'])
            q = extension.split('.')
            if len(q) > 2:
                w =  [f for f in path.iterdir() if f.is_file() and f.suffix == f'.{q[-1]}' and f.stem.endswith(q[-2])]
            else:
                w =  [f for f in path.iterdir() if f.is_file() and f.suffix == f'.{q[-1]}']
            for d in path.iterdir():
                if d.is_dir():
                    w += _sync_scan(d)
            return w
        
        return await asyncio.to_thread(_sync_scan)

    def getRealPath(self, path:str)->str:
        return self._getObjPath(path=path)['real_path']

    def _getObjPath(self, path: str):
            """Получает обьект пути по строке с ."""  
            # Определяем тип файла
            typeFile = path.rsplit('.', 1)[-1] if '.' in path else None
            
            return {'real_path': f'{ROOT}/{path}' if path in ROOT else path, 'type': typeFile}

    async def _createJsonFile(self, real_path, data):
        """Создаёт json файлы"""
        async with aiofiles.open(real_path, 'w', encoding='utf-8') as f:
            content = json.dumps(data, ensure_ascii=False, indent=0)
            await f.write(content)

    async def _createDefaultFile(self, real_path, data):
        """Создаёт файлы"""
        os.makedirs(os.path.dirname(real_path), exist_ok=True)
        if isinstance(data, str):
            data = data.encode('utf-8')
        async with aiofiles.open(real_path, 'wb') as f:
            await f.write(data)

    async def _readJsonFile(self, real_path):
        """Читает json файлы"""
        try:
            async with aiofiles.open(real_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return json.loads(content)
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка: {e}"

    async def _readYamlFile(self, real_path):
        """Читает yaml файлы"""
        def _read():
            with open(real_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)

        data = await asyncio.to_thread(_read)
        return data

    async def _readDefaultFile(self, real_path):
        """Читает файлы"""
        try:
            async with aiofiles.open(real_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            return content
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка: {e}"

FileManagerPkg = AsyncFileManager()