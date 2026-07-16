from windows_toasts import Toast, WindowsToaster, ToastDisplayImage
from windows_toasts.wrappers import ToastImagePosition

from engine.Run import config
from engine.package import FileManagerPkg

class ToasterPkg:
    toaster = WindowsToaster(config['nameApp'])

    def __init__(self):
        self.toast = Toast()
        self._image(config['pathIcon'])

    def _image(self, path):
        icon_path = FileManagerPkg._getObjPath(path, index=1)['real_path']
        icon = ToastDisplayImage.fromPath(
            imagePath=icon_path,
            position=ToastImagePosition.AppLogo
        )
        self.toast.AddImage(icon)
        return self

    def text(self, text):
        self.toast.text_fields = text
        return self
    
    def on_activated(self, func):
        self.toast.on_activated = lambda _: func
        return self

    def show(self):
        self.toaster.show_toast(self.toast)