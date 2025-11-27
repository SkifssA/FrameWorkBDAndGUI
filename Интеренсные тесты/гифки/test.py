import dearpygui.dearpygui as dpg
from PIL import Image, ImageSequence
import numpy as np
import time

class GIFPlayer:
    def __init__(self, gif_path):
        self.gif = Image.open(gif_path)
        self.frames = []
        self.delays = []

        # Извлекаем кадры и задержки
        for frame in ImageSequence.Iterator(self.gif):
            # Конвертируем в RGBA
            rgb_frame = frame.convert("RGBA")
            data = np.array(rgb_frame).ravel() / 255.0  # нормализуем в [0,1]
            self.frames.append(data)
            # Задержка в миллисекундах (из метаданных GIF)
            delay = frame.info.get("duration", 100)  # по умолчанию 100 мс
            self.delays.append(delay / 1000.0)  # в секунды

        self.current_frame = 0
        self.last_time = time.time()
        self.width, self.height = self.gif.size

    def update(self, texture_id):
        now = time.time()
        elapsed = now - self.last_time

        if elapsed >= self.delays[self.current_frame]:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_time = now

            # Обновляем текстуру
            dpg.set_value(texture_id, self.frames[self.current_frame])

# --- Инициализация DPG ---
dpg.create_context()

# Загружаем GIF
gif_player = GIFPlayer("Интеренсные тесты/гифки/test.gif")  # замените на путь к вашему GIF

# Создаём текстуру
with dpg.texture_registry():
    texture_id = dpg.add_dynamic_texture(
        width=gif_player.width,
        height=gif_player.height,
        default_value=gif_player.frames[0]
    )

# Окно с изображением
with dpg.window(label="GIF Player"):
    dpg.add_image(texture_id)

# Frame callback для обновления кадров
def render_callback():
    gif_player.update(texture_id)
    dpg.set_frame_callback(dpg.get_frame_count() + 1, render_callback)

dpg.set_frame_callback(1, render_callback)

# Запуск
dpg.create_viewport(title="GIF in Dear PyGui", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()