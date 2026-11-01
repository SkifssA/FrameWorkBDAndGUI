from core.package.FileManager import FileManagerPkg
from core.context import PATH_CONFIG

def validateConfig():
    conf = FileManagerPkg.ReadFile(PATH_CONFIG)
    # config.json не хранится в git (секреты) — шаблон: config.example.json
    if not isinstance(conf, dict) or "database" not in conf:
        raise FileNotFoundError(
            f"Не найден {PATH_CONFIG}. "
            f"Скопируйте core/config/config.example.json в {PATH_CONFIG} "
            "и укажите url и auth_token базы данных."
        )