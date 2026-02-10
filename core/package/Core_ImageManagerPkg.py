import dearpygui.dearpygui as dpg
from PIL import Image
from pygments.formatters import ImageFormatter
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
import numpy as np
import io
import os
from io import BytesIO

class Core_ImageManagerPkg:

    async def loadFile(self, objPath):
        try:
            image_data, img_w, img_h = await self.workImage(objPath)
            with dpg.texture_registry(show=False):
                return dpg.add_static_texture(width=img_w, height=img_h, default_value=image_data)
        except Exception as e:
            print("Ошибка:", e)
            img_w, img_h = 1, 1
            pixel_data = [0.0, 0.0, 0.0, 0.0] * (img_w * img_h)
            with dpg.texture_registry(show=False):
                return dpg.add_static_texture(img_w, img_h, pixel_data)

    async def workImage(self, objPath):
        if objPath['type'] in ('sql', 'scala', 'xml'):
            img = self.text_file_to_highlighted_image(objPath['real_path'])
        elif objPath['type'] in ('http'):
            img = await self.load_image_as_url(objPath['real_path'])
        else:
            img = self.load_image_as_raw(objPath['real_path'])
        newImg = img.convert("RGBA")
        w, h = newImg.size
        data = np.array(newImg).flatten().astype(np.float32) / 255.0
        return data, w, h

    def load_image_as_raw(self, path):
        '''Работа с изображениями'''
        if not os.path.exists(path):
            raise FileNotFoundError(f"Изображение не найдено: {path}")
        return Image.open(path)
    
    async def load_image_as_url(self, url):
        from ..package.Core_AiohttpPkg import Core_AiohttpPkg
        if url is not None:
            async with Core_AiohttpPkg().get(url) as response:
                content = await response.read()
        return Image.open(BytesIO(content))
        
    def text_file_to_highlighted_image(self, input_path):
        '''Работа с текстовыми файлами'''
        lexer = get_lexer_for_filename(input_path)
        # Читаем файл
        with open(input_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Форматируем как изображение
        formatter = ImageFormatter(
            font_name='Consolas',  # или любой моноширинный шрифт
            font_size=14,
            line_numbers=True,
            line_number_start=1,
            line_number_fg='#666',
            line_number_bg='#1e1e1e',
            style='monokai'  # можно попробовать 'default', 'monokai', 'vs', и др.
        )
        
        # Подсвечиваем и получаем байты изображения
        image_bytes = highlight(code, lexer, formatter)
        
        # Конвертируем в PIL Image
        return Image.open(io.BytesIO(image_bytes))