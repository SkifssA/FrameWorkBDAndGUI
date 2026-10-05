from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QPixmap, QImage
from PyQt6.QtCore import Qt

from core.package.CachedImageLoader import CachedImageLoader
from core.ui.forms.base import Base
from PIL import Image as ImagePIL
from core.package.AsynRun import asyncRun

def pil_to_qpixmap(pil_image: ImagePIL.Image) -> QPixmap:
    """Конвертирует PIL.Image в QPixmap."""
    if pil_image is None:
        return QPixmap()

    # 1. Приводим к формату RGBA (4 канала: Red, Green, Blue, Alpha)
    # Это самый надежный способ для корректного отображения прозрачности
    pil_image = pil_image.convert("RGBA")
    
    # 2. Получаем размеры и сырые данные
    width, height = pil_image.size
    data = pil_image.tobytes("raw", "RGBA")
    
    # 3. Создаем QImage из байтов
    # Формат Format_RGBA8888 соответствует стандартному 32-битному цвету
    q_image = QImage(data, width, height, QImage.Format.Format_RGBA8888)
    
    # 4. Конвертируем в QPixmap
    return QPixmap.fromImage(q_image)

class ImageWidget(QWidget):
    """Виджет для отображения изображения с правильным ресайзом"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        # Убираем минимальный размер чтобы можно было уменьшать
        self.setMinimumSize(0, 0)
    
    def set_pixmap(self, pixmap: QPixmap):
        """Устанавливаем изображение"""
        self.original_pixmap = pixmap
        self.update()  # Перерисовываем
    
    def paintEvent(self, event):
        """Рисуем изображение с сохранением пропорций"""
        super().paintEvent(event)
        
        if self.original_pixmap is None or self.original_pixmap.isNull():
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Вычисляем прямоугольник для рисования с сохранением пропорций
        rect = self.rect()
        
        # Проверяем что размер валидный
        if rect.width() <= 0 or rect.height() <= 0:
            painter.end()
            return
        
        scaled_pixmap = self.original_pixmap.scaled(
            rect.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Центрируем изображение
        x = (rect.width() - scaled_pixmap.width()) // 2
        y = (rect.height() - scaled_pixmap.height()) // 2
        
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()
    
    def sizeHint(self):
        """Предпочтительный размер виджета"""
        if self.original_pixmap and not self.original_pixmap.isNull():
            return self.original_pixmap.size()
        return super().sizeHint()


class Image(Base):
    def _createMainFrameWidget(self):
        self.cachedImg = CachedImageLoader()
        self.image_widget = ImageWidget(parent=self)

        self._onRefresh()
        
        return self.image_widget

    def _onRefresh(self):

        def on_image_loaded(pixmap: QPixmap):
            if not pixmap.isNull():
                self.image_widget.set_pixmap(pixmap)
            else:
                print("Ошибка: изображение не загрузилось")

        if (x:=self.onRefresh()) is not None:
            i = asyncRun(self.cachedImg.load(x))
            if i:
                on_image_loaded(pil_to_qpixmap(i))