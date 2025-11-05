import dearpygui.dearpygui as dpg
from PIL import Image
import numpy as np
import os
import asyncio

class CardFileView:
    MIN_SCALE = 0.1
    MAX_SCALE = 10.0

    def __init__(self):
        self.scale = 1
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.dragging = False
        self.last_mouse_pos = [0.0, 0.0]

    async def open(self, master, w=-1, h=-1):
        self.parent = master
        with dpg.tab(label='Просмотр файла', parent=master) as tab:
            with dpg.child_window(width=-1
                                  ,height=-1
                                  , no_scrollbar=True
                                  , no_scroll_with_mouse= True) as image_container:
                self.image_drawlist = dpg.add_drawlist(width=w, height=h)
                self.regHandler()
        self.image_container = image_container
        dpg.configure_item(master, show=True)
        # Отложенно настроим размер и отрисуем изображение
        dpg.split_frame()  # ждём следующего кадра (чтобы элементы отрендерились)
        await asyncio.sleep(0)  # уступаем управление

        # Получаем реальный размер контейнера
        container_w = dpg.get_item_width(image_container)
        container_h = dpg.get_item_height(image_container)

        # Обновляем размер drawlist
        dpg.set_item_width(self.image_drawlist, container_w)
        dpg.set_item_height(self.image_drawlist, container_h)

        # Сохраняем для последующих обновлений
        self.container_size = dpg.get_item_rect_size(self.image_drawlist)
        dpg.set_item_width(self.image_drawlist, self.container_size[0])
        dpg.set_item_height(self.image_drawlist, self.container_size[1])

        # Теперь можно отрисовать
        await self.refresh()

        self.update_image_position()

    async def onRefresh(self):
        return ''

    async def refresh(self):
        self.loadFile(await self.onRefresh())
        dpg.delete_item(self.image_drawlist, children_only=True)
        self.offset_x = 0
        self.offset_y = 0

        scw = self.container_size[0] / self.img_w
        sch = self.container_size[1] / self.img_h
        self.scale = min(scw, sch)

        self.drawnTag = dpg.draw_image(self.textureTag, pmin=(0, 0), pmax=(self.img_w, self.img_h), parent=self.image_drawlist)
        self.update_image_position()

    def loadFile(self, image_path):
        try:
            image_data, self.img_w, self.img_h = self.load_image_as_raw(image_path)
            with dpg.texture_registry(show=False):
                self.textureTag = dpg.add_static_texture(width=self.img_w, height=self.img_h, default_value=image_data)
        except Exception as e:
            print(f'{image_path=}')
            print("Ошибка:", e)
            exit()

    def regHandler(self):
        with dpg.handler_registry():
            dpg.add_mouse_wheel_handler(callback=self.on_mouse_wheel)
            dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_drag)
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_right_down)
            dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_right_up)
    
        dpg.set_viewport_resize_callback(lambda: dpg.set_frame_callback(dpg.get_frame_count() + 1, self.on_viewport_resize))

    def on_viewport_resize(self):
        # Получаем реальный размер контейнера
        container_w, container_h = dpg.get_item_rect_size(self.image_container)
        # Обновляем размер drawlist
        dpg.set_item_width(self.image_drawlist, container_w)
        dpg.set_item_height(self.image_drawlist, container_h)
        # Сохраняем для последующих обновлений
        self.container_size = dpg.get_item_rect_size(self.image_drawlist)
        self.update_image_position()
        dpg.set_frame_callback(dpg.get_frame_count() + 1, self.on_viewport_resize)

    # === Загрузка изображения ===
    def load_image_as_raw(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Изображение не найдено: {path}")
        img = Image.open(path).convert("RGBA")
        w, h = img.size
        data = np.array(img).flatten().astype(np.float32) / 255.0
        return data, w, h

    # === Обработчики ===
    def on_mouse_wheel(self, sender, app_data):
        global scale
        if dpg.is_item_hovered(self.image_container):
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
        if dpg.is_item_hovered(self.image_container):
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
