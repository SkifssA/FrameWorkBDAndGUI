from core.package.FileManager import FileManagerPkg

def validateConfig():
    _pathConfig = "core/config/config.json"
    conf = FileManagerPkg.ReadFile(_pathConfig)
    # config.json не хранится в git (секреты) — шаблон: config.example.json
    if not isinstance(conf, dict) or "database" not in conf:
        raise FileNotFoundError(
            "Не найден core/config/config.json. "
            "Скопируйте core/config/config.example.json в core/config/config.json "
            "и укажите url и auth_token базы данных."
        )