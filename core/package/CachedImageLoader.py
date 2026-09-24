import os
import hashlib
from pathlib import Path

from PyQt6.QtGui import QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtCore import QUrl, QObject, pyqtSignal


class ImageLoader(QObject):
    finished = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self._on_finished)

    def load(self, url: str):
        request = QNetworkRequest(QUrl(url))
        request.setHeader(
            QNetworkRequest.KnownHeaders.UserAgentHeader,
            b"Mozilla/5.0 (PyQt6 App)"
        )
        self.manager.get(request)

    def _on_finished(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.finished.emit(pixmap)
        else:
            print(f"Ошибка загрузки: {reply.errorString()}")
        reply.deleteLater()

class CachedImageLoader(ImageLoader):
    def __init__(self, cache_dir: str = "core/assets/image_cache", parent=None):
        super().__init__(parent)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def load(self, url: str):
        filename = hashlib.md5(url.encode()).hexdigest() + ".jpg"
        cached_path = self.cache_dir / filename

        if cached_path.exists():
            pixmap = QPixmap(str(cached_path))
            self.finished.emit(pixmap)
            return

        request = QNetworkRequest(QUrl(url))
        request.setAttribute(QNetworkRequest.Attribute.User, str(cached_path))
        self.manager.get(request)

    def _on_finished(self, reply: QNetworkReply):
        cached_path = Path(reply.request().attribute(QNetworkRequest.Attribute.User))

        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()

            with open(cached_path, 'wb') as f:
                f.write(data)

            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.finished.emit(pixmap)
        reply.deleteLater()