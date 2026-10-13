import asyncio
from threading import current_thread

from core.sdk import eventSignal, formEvent, typeEvent

from webapp.logic import get_session

dataForEvent:dict[typeEvent, str] = {
    typeEvent.openForm:'<div hx-get="/{main_menu_form}/{form}" hx-trigger="load" hx-target="body" hx-swap="outerHTML" hx-push-url="true"></div>'
    , typeEvent.refresh:'Типо обновил {form}'
}

_main_loop: asyncio.AbstractEventLoop = None

def set_main_loop(loop: asyncio.AbstractEventLoop):
    global _main_loop
    _main_loop = loop

async def emit_event(event: formEvent):
    """Отправляет событие в очередь текущей сессии"""
    session = get_session()
    if queue := session.queue:
        data = {
            'main_menu_form': session.main_menu_form._get_parent_name(),
            'form': event.form
        }
        print(f'Отправлено {event.personType} c data={data}')
        await queue.put({
            "event": event.personType,
            "data": dataForEvent[event.type].format(**data)
        })

def sync_signal_handler(sender, **kwargs):
    """Синхронный мост: безопасно отправляет задачу в асинхронный цикл"""
    event = kwargs.get('fromEvent')
    if not event or not _main_loop:
        print("⚠️ Событие потеряно: нет event или не инициализирован loop")
        return

    try:
        # 1. Проверяем, запущен ли цикл в ТЕКУЩЕМ потоке
        loop = asyncio.get_running_loop()
        
        # Если мы здесь, значит мы уже в async-потоке. 
        # Просто создаем задачу.
        asyncio.create_task(emit_event(event))
        
    except RuntimeError:
        # 2. Если RuntimeError, значит мы в другом (синхронном) потоке.
        # Используем thread-safe метод для отправки задачи в главный цикл.
        asyncio.run_coroutine_threadsafe(emit_event(event), _main_loop)

def registrSignal():
    eventSignal.connect(sync_signal_handler)

def get_session_queue():
    w = get_session().queue
    if not w:
        get_session().queue = w = asyncio.Queue()
    return w