import dearpygui.dearpygui as dpg

class ReSizeLine:
    def __init__(self, obj, tagReSize, isHorizontal:bool=False, size:int=5, par=0):
        self.obj = obj
        self.tagReSize = tagReSize
        self.isHorizontal = isHorizontal
        self.last_mouse_pos = [0.0, 0.0]
        self.dragging_resize = False
        self._regHandler()

        d = {
            'width':-1 if isHorizontal else size
            ,'height':size if isHorizontal else -1
            ,'show': False
            ,'parent': par
        }

        self.btn = dpg.add_button(**d, label='Изменение размера')

    def get(self): return self.btn

    def _regHandler(self):
        """Регистрация обработчиков и событий"""
        def on_mouse_drag(sender, app_data):
            mouse_x, mouse_y = dpg.get_mouse_pos(local=False)
            if self.dragging_resize:
                if not self.isHorizontal:
                    dx = mouse_x - self.last_mouse_pos[0]
                    self.obj.offset_x_resize += dx
                    self.last_mouse_pos[0] = mouse_x
                    dpg.configure_item(self.tagReSize, width=self.obj.offset_x_resize)
                else:
                    dy = mouse_y - self.last_mouse_pos[1]
                    self.obj.offset_y_resize += dy
                    self.last_mouse_pos[1] = mouse_y
                    dpg.configure_item(self.tagReSize, height=self.obj.offset_y_resize)

        def on_mouse_right_down(sender, app_data):
            try:
                if dpg.is_item_hovered(self.btn):
                    self.dragging_resize = 1
                self.last_mouse_pos[:] = dpg.get_mouse_pos(local=False)
            except:
                pass

        def on_mouse_right_up(sender, app_data):
            self.dragging_resize = 0

        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=on_mouse_drag)
            dpg.add_mouse_down_handler(button=dpg.mvMouseButton_Left, callback=on_mouse_right_down)
            dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left, callback=on_mouse_right_up)