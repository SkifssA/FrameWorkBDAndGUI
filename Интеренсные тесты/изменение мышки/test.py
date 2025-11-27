import dearpygui.dearpygui as dpg

dpg.create_context()

def on_hover_in(sender, app_data, user_data):
    dpg.set_viewport_mouse_cursor(dpg.mvMouseCursor_Arrow)

def on_hover_out(sender, app_data, user_data):
    # Вернём, например, стандартный курсор
    dpg.set_viewport_mouse_cursor(dpg.mvMouseCursor_Arrow)  # или Hand, если нужно

with dpg.window(label="Test", width=400, height=300):
    dpg.add_text("Наведи на кнопку ниже")
    target_widget = dpg.add_button(label="Курсор → стрелка", tag="my_button")

# Создаём реестр обработчиков
with dpg.item_handler_registry(tag="button_hover_registry"):
    dpg.add_item_hover_handler(callback=on_hover_in)
    # Dear PyGui не имеет прямого "hover out", поэтому используем workaround:
    # Например, менять курсор глобально при любом движении, но проще — использовать таймер (см. ниже)
    # Или: можно использовать фокус/активность, но это не всегда подходит

# Привязываем реестр к виджету
dpg.bind_item_handler_registry("my_button", "button_hover_registry")

# Но! Чтобы вернуть курсор обратно, когда мышь ушла с виджета,
# придётся проверять позицию мыши — так как Dear PyGui не даёт "on_mouse_exit"
def update_cursor_based_on_position():
    if not dpg.is_item_hovered("my_button"):
        dpg.set_viewport_mouse_cursor(dpg.mvMouseCursor_Hand)  # или Arrow, как "по умолчанию"
    else:
        dpg.set_viewport_mouse_cursor(dpg.mvMouseCursor_Arrow)

# Вызываем каждый кадр
dpg.set_frame_callback(dpg.mvFrameCallback_Idle, update_cursor_based_on_position)

dpg.create_viewport(title='Курсор над виджетом', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()