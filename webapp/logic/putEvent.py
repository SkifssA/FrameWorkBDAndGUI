import asyncio

from core.sdk import eventSignal, formEvent

from webapp.logic import get_session

async def emit_event(event: formEvent):
    """Отправляет событие в очередь текущей сессии"""
    if queue := get_session_queue(event.session_id):
        await queue.put({
            "event": event.value,
            "data": event.to_json()
        })

def sync_signal_handler(sender, **kwargs):
    """Синхронный мост: ловит сигнал и запускает асинхронную отправку"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return

    # Создаем задачу в текущем цикле
    loop.create_task(emit_event(kwargs.fromEvent))

def registrSignal():
    # Подключаем хендлер к сигналу
    eventSignal.connect(sync_signal_handler)

def get_session_queue(session_id:str):
    w = get_session(session_id).queue
    if not w:
        get_session(session_id).queue = w = asyncio.Queue()
    return w