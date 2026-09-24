import asyncio
import nest_asyncio

# Применяем один раз при импорте или старте приложения
nest_asyncio.apply()

def asyncRun(coroutine):
    """Выполнить корутину, поддерживая вложенные вызовы"""
    try:
        loop = asyncio.get_running_loop()
        # Loop уже запущен - используем его
        return loop.run_until_complete(coroutine)
    except RuntimeError:
        # Нет активного loop - создаём новый
        return asyncio.run(coroutine)