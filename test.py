import dearpygui.dearpygui as dpg
import os

WIDTH, HEIGHT = 900, 500
TITLE_BAR_HEIGHT = 20
title_bar_drag = False

def on_close():
    dpg.destroy_context()

def minimize():
    dpg.configure_viewport(0, minimized=True)

def maximize():
    def _uploadTitleBar(width):
        dpg.configure_item(titleBarSpace, width=width - (54*3))

    cfg = dpg.get_viewport_configuration(0)
    if cfg["width"] >= 1900:
        dpg.configure_viewport(0, width=WIDTH, height=HEIGHT, x_pos=100, y_pos=100) #Надо глобальные в целом пеложении
        _uploadTitleBar(WIDTH)
    else: 
        dpg.configure_viewport(0, width=1920, height=1080, x_pos=0, y_pos=0) #Надо не стандартные 
        _uploadTitleBar(1920)

def detect_titlebar(sender, data):
    global title_bar_drag
    if dpg.is_mouse_button_down(0) and -2 <= data[1] <= TITLE_BAR_HEIGHT:
        title_bar_drag = True
    elif not dpg.is_mouse_button_down(0) and title_bar_drag:
        title_bar_drag = False

def drag_window(sender, data):
    if title_bar_drag:
        pos = dpg.get_viewport_pos()
        dpg.configure_viewport(0,
            x_pos=int(pos[0] + data[1]),
            y_pos=int(pos[1] + data[2])
        )

dpg.create_context()

font_path = os.path.join(os.environ["WINDIR"], "Fonts", "segoeui.ttf")
with dpg.font_registry():
    default_font = dpg.add_font(font_path, 16)

dpg.create_viewport(title=" ", width=WIDTH, height=HEIGHT,
                    decorated=False, resizable=True)

with dpg.window(tag="main_window", no_title_bar=True, no_resize=True,
                no_move=True, no_collapse=True, no_scrollbar=True,
                on_close=on_close):
    with dpg.group(horizontal=True):
        titleBarSpace = dpg.add_spacer(width=WIDTH - (54*3))
        dpg.add_button(label="—",  width=40, callback=minimize)
        dpg.add_button(label="☐",  width=40, callback=maximize)
        dpg.add_button(label="✕",  width=40, callback=on_close)
    dpg.add_separator()

with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=detect_titlebar)
    dpg.add_mouse_drag_handler(button=0, callback=drag_window)

dpg.setup_dearpygui()
dpg.bind_font(default_font)
dpg.set_primary_window("main_window", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()