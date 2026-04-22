import dearpygui.dearpygui as dpg
from core.form.Base import Base



class CardFileView(Base):
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
            self.regHandler()
        return image_container

    def onRefresh(self):
        return ''
    
    def onRefreshExt(self):
        return ''
    
    def _getAttr(self):
        return ''

    async def _refresh(self):
        self.rect.refresh()
        self.textureTag = await self.imgManager.loadFile(self.rect.getData())
        self.img_w = dpg.get_item_width(self.textureTag)
        self.img_h = dpg.get_item_height(self.textureTag)
        dpg.delete_item(self.image_drawlist, children_only=True)
        self.offset_x = 0
        self.offset_y = 0
        self.container_size = dpg.get_item_rect_size(self.mainForm)
        scw = self.container_size[0] / self.img_w
        sch = self.container_size[1] / self.img_h
        self.scale = min(scw, sch)
        dpg.set_item_width(self.image_drawlist, self.container_size[0]-17)
        dpg.set_item_height(self.image_drawlist, self.container_size[1]-17)

        self.drawnTag = dpg.draw_image(self.textureTag, pmin=(0, 0), pmax=(1000, 1000), parent=self.image_drawlist)
        self.update_image_position()

    def regHandler(self) -> None:
        with dpg.handler_registry() as handler_reg:
            self.handler_reg = handler_reg
            dpg.add_mouse_wheel_handler(callback=self.on_mouse_wheel)
            dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_drag)
            dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_right_down)
            dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Right, callback=self.on_mouse_right_up)

        with dpg.item_handler_registry() as item_handler_reg:
            self.item_handler_reg = item_handler_reg
            dpg.add_item_visible_handler(callback=self.on_viewport_resize)
        
        dpg.bind_item_handler_registry(self.image_drawlist, self.item_handler_reg)


    def deleteItem(self):
        dpg.delete_item(self.handler_reg)
        dpg.delete_item(self.item_handler_reg)
        super().deleteItem()

    def on_viewport_resize(self) -> None:
        # Получаем реальный размер контейнера
        if dpg.does_item_exist(self.mainForm):
            w = dpg.get_item_rect_size(self.mainForm)
            if (self.container_size != w):
                self.container_size = w
                scw = self.container_size[0] / self.img_w
                sch = self.container_size[1] / self.img_h
                self.scale = min(scw, sch)
                # Обновляем размер drawlist
                dpg.set_item_width(self.image_drawlist, self.container_size[0]-17)
                dpg.set_item_height(self.image_drawlist, self.container_size[1]-17)
                # Сохраняем для последующих обновлений
                self.update_image_position()

    # === Обработчики ===
    def on_mouse_wheel(self, sender, app_data):
        if dpg.does_item_exist(self.mainForm):
            if dpg.is_item_hovered(self.mainForm):
                delta = app_data
                self.scale += delta * 0.1 * self.scale
                self.scale = max(self.MIN_SCALE, min(self.MAX_SCALE, self.scale))
                self.update_image_position()

    def on_mouse_drag(self, sender, app_data):
        if dpg.does_item_exist(self.mainForm):
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
        if dpg.does_item_exist(self.mainForm):
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
