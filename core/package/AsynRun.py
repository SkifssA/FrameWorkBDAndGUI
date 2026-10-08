import asyncio
import nest_asyncio


def asyncRun(coroutine):
    """Выполнить корутину, поддерживая вложенные вызовы"""
    try:
        loop = asyncio.get_running_loop()
        # Если цикл уже есть, создаем задачу и ждем её выполнения синхронно
        # Внимание: это может быть опасно в некоторых GUI-потоках, но для CLI/Scripts ок
        return asyncio.run_coroutine_threadsafe(coroutine, loop).result()
    except RuntimeError:
        # Если цикла нет, просто запускаем как обычно
        return asyncio.run(coroutine)