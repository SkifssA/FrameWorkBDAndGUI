import dearpygui.dearpygui as dpg
from PIL import Image
from pygments.formatters import ImageFormatter
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
import numpy as np
import io
import os
from .BaseForm import BaseForm

class CardFileView(BaseForm):
    MIN_SCALE = 0.1
    MAX_SCALE = 10.0

    def __init__(self):
        super().__init__()
        self.scale = 1
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.dragging = False
        self.last_mouse_pos = [0.0, 0.0]
        self.previous_size = None
        self.image_drawlist = None
        self.mainForm = None

    def createMainForm(self, par):
        with dpg.child_window(width=-1
                                ,height=-1
                                , no_scrollbar=True
                                , no_scroll_with_mouse= True
                                , parent=par) as image_container:
            self.image_drawlist = dpg.add_drawlist(width=-1, height=-1)
        return image_container

    async def onRefresh(self):
        return ''

    async def _refresh(self):
        self.loadFile(await self.onRefresh())
        dpg.delete_item(self.image_drawlist, children_only=True)
        self.offset_x = 0
        self.offset_y = 0
        self.container_size = dpg.get_item_rect_size(self.mainForm)
        scw = self.container_size[0] / self.img_w
        sch = self.container_size[1] / self.img_h
        self.scale = min(scw, sch)
        dpg.set_item_width(self.image_drawlist, self.container_size[0])
        dpg.set_item_height(self.image_drawlist, self.container_size[1])

        self.drawnTag = dpg.draw_image(self.textureTag, pmin=(0, 0), pmax=(1000, 1000), parent=self.image_drawlist)
        self.update_image_position()

    def loadFile(self, objPath):
        try:
            image_data, self.img_w, self.img_h = self.workImage(objPath)
            with dpg.texture_registry(show=False):
                self.textureTag = dpg.add_static_texture(width=self.img_w, height=self.img_h, default_value=image_data)
        except Exception as e:
            print("Ошибка:", e)
            self.img_w, self.img_h = 200, 150
            pixel_data = [0.0, 0.0, 0.0, 0.0] * (self.img_w * self.img_h)  # чёрный + прозрачный
            # или [1.0, 1.0, 1.0, 1.0] * N — белый непрозрачный
            with dpg.texture_registry(show=False):
                self.textureTag = dpg.add_static_texture(self.img_w, self.img_h, pixel_data)

    def regHandler(self):
        with dpg.handler_registry():
            dpg.add_mouse_wheel_handler(callback=self.on_mouse_wheel)
            dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_drag)
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_right_down)
            dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_right_up)
    
        dpg.set_viewport_resize_callback(lambda: dpg.set_frame_callback(dpg.get_frame_count() + 1, self.on_viewport_resize))

    def on_viewport_resize(self):
        # Получаем реальный размер контейнера
        container_w, container_h = dpg.get_item_rect_size(self.mainForm)
        # Обновляем размер drawlist
        dpg.set_item_width(self.image_drawlist, container_w)
        dpg.set_item_height(self.image_drawlist, container_h)
        # Сохраняем для последующих обновлений
        self.container_size = dpg.get_item_rect_size(self.image_drawlist)

        self.update_image_position()

    # === Работа с различными файлами изображения ===

    def workImage(self, objPath):
        if objPath['type'] in ('sql', 'scala', 'xml'):
            img = self.text_file_to_highlighted_image(objPath['real_path'])
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

    # === Обработчики ===
    def on_mouse_wheel(self, sender, app_data):
        global scale
        if dpg.is_item_hovered(self.mainForm):
            delta = app_data
            self.scale += delta * 0.1 * self.scale
            self.scale = max(self.MIN_SCALE, min(self.MAX_SCALE, self.scale))
            self.update_image_position()

    def on_mouse_drag(self, sender, app_data):
        if self.dragging and dpg.is_item_hovered(self.image_drawlist):
            mouse_x, mouse_y = dpg.get_mouse_pos(local=False)
            dx = mouse_x - self.last_mouse_pos[0]
            dy = mouse_y - self.last_mouse_pos[1]
            self.offset_x += dx
            self.offset_y += dy
            self.last_mouse_pos[0] = mouse_x
            self.last_mouse_pos[1] = mouse_y
            self.update_image_position()

    def on_mouse_right_down(self, sender, app_data):
        if dpg.is_item_hovered(self.mainForm):
            self.dragging = True
            self.last_mouse_pos[:] = dpg.get_mouse_pos(local=False)

    def on_mouse_right_up(self, sender, app_data):
        self.dragging = False

    def update_image_position(self):
        win_w, win_h = self.container_size
        if self.img_w * self.scale > win_w or self.img_h * self.scale > win_h:
            draw_x, draw_y = self.calcPosition(win_w, win_h)
        else:
            draw_x, draw_y = win_w / 2 - (self.img_w * self.scale) / 2, win_h / 2 - (self.img_h * self.scale) / 2
        dpg.configure_item(self.drawnTag, pmin=(draw_x, draw_y), pmax=(draw_x + self.img_w * self.scale, draw_y + self.img_h * self.scale))

    def calcPosition(self, win_w, win_h):
        if win_w < self.img_w * self.scale:
            draw_x = win_w / 2 - (self.img_w * self.scale) / 2 + self.offset_x
            if draw_x > 0 : 
                draw_x = 0
                self.offset_x = -(win_w / 2 - (self.img_w * self.scale) / 2)
            if abs(draw_x-win_w) > self.img_w * self.scale : 
                draw_x = -(self.img_w * self.scale) + win_w
                self.offset_x = win_w / 2 - (self.img_w * self.scale) / 2
        else:
            draw_x = win_w / 2 - (self.img_w * self.scale) / 2
            self.offset_x = 0

        if win_h < self.img_h * self.scale:
            draw_y = win_h / 2 - (self.img_h * self.scale) / 2 + self.offset_y
            if draw_y > 0 : 
                draw_y = 0
                self.offset_y = -(win_h / 2 - (self.img_h * self.scale) / 2)
            if abs(draw_y-win_h) > self.img_h * self.scale : 
                draw_y = -(self.img_h * self.scale) + win_h
                self.offset_y = win_h / 2 - (self.img_h * self.scale) / 2
        else:
            draw_y = win_h / 2 - (self.img_h * self.scale) / 2
            self.offset_y = 0

        return draw_x, draw_y
