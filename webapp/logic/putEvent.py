import asyncio
from threading import current_thread

from core.sdk import eventSignal, formEvent, typeEvent, ACTIONDISPATCHER

from webapp.logic import get_session, get_form, get_open_form
from webapp.logic.var import current_request, templates
from webapp.logic.dictEvent import dataForEvent
from webapp.logic.dataClass import PutData

_main_loop: asyncio.AbstractEventLoop = None

def getHtmlNotMain(event:formEvent):
    data:PutData = dataForEvent[event.type]['data'](event)
    return templates.TemplateResponse(
            request=current_request.get(),
            name=data.name_template,
            context=data.context,
        )

def set_main_loop(loop: asyncio.AbstractEventLoop):
    global _main_loop
    _main_loop = loop

async def emit_event(event: formEvent):
    """Отправляет событие в очередь текущей сессии"""
    if queue := get_session_queue():
        data = {
            'main_menu_form': get_session().main_menu_form._get_parent_name(),
            'form': event.form,
            'dataHtml': getHtmlNotMain(event).body.decode('utf-8'),
            'formCaption': get_form(event.form).getInfoMeta()['metaForm'].get('caption', '')
        }

        await queue.put({
            "event": event.personType,
            "data": dataForEvent[event.type]['templates'].format(**data)
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
    import uuid
    w = get_session().queue
    if not w:
        get_session().queue = w = asyncio.Queue()
        w.name = f"q-{uuid.uuid4().hex[:6]}"   # ← свой тег
        print(f"[NEW QUEUE] created {w.name} for session_id={id(w)}")
    return w