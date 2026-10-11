import asyncio
import hashlib
from pathlib import Path
from typing import Optional

import aiohttp
from PIL import Image
from io import BytesIO


class ImageLoader:
    """Асинхронный загрузчик изображений без привязки к GUI-фреймворкам."""

    def __init__(self, user_agent: str = "Mozilla/5.0 (Python App)"):
        self.user_agent = user_agent
        # Сессию лучше переиспользовать для производительности
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {"User-Agent": self.user_agent}
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    async def load(self, url: str) -> Optional[Image.Image]:
        """Загружает изображение по URL и возвращает объект PIL.Image."""
        session = await self._get_session()
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    return Image.open(BytesIO(data))
                else:
                    print(f"Ошибка загрузки {url}: HTTP {response.status}")
        except Exception as e:
            print(f"Ошибка сети при загрузке {url}: {e}")
        return None

    async def close(self):
        """Корректное закрытие HTTP-сессии."""
        if self._session and not self._session.closed:
            await self._session.close()


class CachedImageLoader(ImageLoader):
    """Загрузчик с дисковым кэшированием."""

    def __init__(self, cache_dir: str = "core/assets/image_cache", **kwargs):
        super().__init__(**kwargs)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, url: str) -> Path:
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
        return self.cache_dir / filename

    async def load(self, url: str) -> Optional[Image.Image]:
        cached_path = self._get_cache_path(url)

        # 1. Проверяем кэш
        if cached_path.exists():
            try:
                # PIL лениво загружает данные, поэтому используем copy()
                # чтобы файл можно было безопасно удалить/изменить позже
                return Image.open(cached_path).copy()
            except Exception as e:
                print(f"Ошибка чтения кэша {cached_path}: {e}")
                # Если кэш битый, удаляем его и грузим заново
                cached_path.unlink(missing_ok=True)

        # 2. Загружаем из сети через родительский класс
        image = await super().load(url)

        # 3. Сохраняем в кэш при успехе
        if image is not None:
            try:
                # Конвертируем в RGB для совместимости с JPEG
                rgb_image = image.convert("RGB")
                rgb_image.save(cached_path, format="JPEG", quality=85)
            except Exception as e:
                print(f"Ошибка сохранения в кэш {cached_path}: {e}")

        return image
