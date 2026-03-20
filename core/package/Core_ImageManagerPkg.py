import os
import io
import base64
import numpy as np
from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import ImageFormatter

class Core_ImageManagerPkg:

    async def loadFile(self, objPath):
        """
        Возвращает строку для ft.Image(src=...)
        """
        try:
            # Получаем PIL Image
            img = await self.workImage(objPath)
            # Конвертируем в Base64 для Flet
            return self.pil_to_base64(img)
        except Exception as e:
            print("Ошибка:", e)
            # Возвращаем заглушку (серый квадрат)
            return self.get_placeholder_base64()

    async def workImage(self, objPath):
        """Логика загрузки (без изменений по сути)"""
        if objPath['type'] in ('sql', 'scala', 'xml'):
            img = self.text_file_to_highlighted_image(objPath['real_path'])
        elif objPath['type'] == 'http':
            img = await self.load_image_as_url(objPath['real_path'])
        else:
            img = self.load_image_as_raw(objPath['real_path'])
        
        # Flet отлично понимает RGBA через PNG
        return img.convert("RGBA")

    def pil_to_base64(self, img: Image.Image, format: str = "PNG") -> str:
        """Конвертация PIL Image в Data URI для Flet"""
        buffered = io.BytesIO()
        img.save(buffered, format=format)
        img_bytes = buffered.getvalue()
        base64_data = base64.b64encode(img_bytes).decode('utf-8')
        return f"data:image/{format.lower()};base64,{base64_data}"

    def get_placeholder_base64(self) -> str:
        """Заглушка на случай ошибки"""
        img = Image.new("RGBA", (100, 100), (128, 128, 128, 255))
        return self.pil_to_base64(img)

    def load_image_as_raw(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Изображение не найдено: {path}")
        return Image.open(path)
    
    async def load_image_as_url(self, url):
        from ..package.Core_AiohttpPkg import Core_AiohttpPkg
        if url is None:
            raise ValueError("URL не может быть None")
        async with Core_AiohttpPkg().get(url) as response:
            content = await response.read()
        return Image.open(io.BytesIO(content))
        
    def text_file_to_highlighted_image(self, input_path):
        lexer = get_lexer_for_filename(input_path)
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        formatter = ImageFormatter(
            font_name='Consolas',
            font_size=14,
            line_numbers=True,
            style='monokai'
        )
        image_bytes = highlight(code, lexer, formatter)
        return Image.open(io.BytesIO(image_bytes))