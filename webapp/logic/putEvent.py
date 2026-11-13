import asyncio

from core.sdk import eventSignal, formEvent, SESSION_STAGE, get_logger

from webapp.logic.procEvent import PROC_EVENT

log = get_logger("webapp.putEven")

_main_loop: asyncio.AbstractEventLoop = None

def set_main_loop(loop: asyncio.AbstractEventLoop):
    global _main_loop
    _main_loop = loop

async def emit_event(event: formEvent):
    """Отправляет событие в очередь текущей сессии"""
    if queue := SESSION_STAGE.get_queue():
        
        await queue.put({
            "event": event.personType,
            "data": PROC_EVENT.get_str_by_event(event)
        })

def sync_signal_handler(sender, **kwargs):
    """Синхронный мост: безопасно отправляет задачу в асинхронный цикл"""
    event = kwargs.get('fromEvent')
    if not event or not _main_loop:
        log.warning("⚠️ Событие потеряно: нет event или не инициализирован loop")
        return

    try:
        loop = asyncio.get_running_loop()
        asyncio.create_task(emit_event(event))
    except RuntimeError:
        asyncio.run_coroutine_threadsafe(emit_event(event), _main_loop)

def registrSignal():
    eventSignal.connect(sync_signal_handler)