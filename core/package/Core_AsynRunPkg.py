import asyncio
import nest_asyncio

def asyncRun(coroutine):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Цикла нет — безопасно запускаем новый
        return asyncio.run(coroutine)
    else:
        # Цикл есть — запускаем вложенно (требует nest_asyncio)
        nest_asyncio.apply()
        return loop.run_until_complete(coroutine)