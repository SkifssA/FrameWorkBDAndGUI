import asyncio
from threading import current_thread

from core.sdk import eventSignal, formEvent, typeEvent, ACTIONDISPATCHER

from webapp.logic import get_session, get_form, get_open_form
from webapp.logic.var import current_request, templates
from webapp.logic.dictEvent import dataForEvent, get_form_bar, get_form_bar_ch
from webapp.logic.dataClass import PutData

_main_loop: asyncio.AbstractEventLoop = None

def getFormHtlnForSSE(event:formEvent):
    data:PutData = dataForEvent[event.type]['data'](event)
    return {
       'dataHtml': w(data),
       'formCaption': data.caption_form
    }

def w(putData:PutData):
    if putData.name_template:
        return templates.TemplateResponse(
            request=current_request.get(),
            name=putData.name_template,
            context=putData.context,
        ).body.decode('utf-8')
    return ''

def set_main_loop(loop: asyncio.AbstractEventLoop):
    global _main_loop
    _main_loop = loop

async def emit_event(event: formEvent):
    """Отправляет событие в очередь текущей сессии"""
    if queue := get_session_queue():
        data = getFormHtlnForSSE(event) | {
            'form_bar': w(get_form_bar()),
            'parent': event.form[:event.form.rfind('.')]
        }

        if get_session().active_form:
            data['form_bar_ch'] = w(get_form_bar_ch(event))

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
        loop = asyncio.get_running_loop()
        asyncio.create_task(emit_event(event))
    except RuntimeError:
        asyncio.run_coroutine_threadsafe(emit_event(event), _main_loop)

def registrSignal():
    eventSignal.connect(sync_signal_handler)

def get_session_queue():
    import uuid
    w = get_session().queue
    if not w:
        get_session().queue = w = asyncio.Queue()
        w.name = f"q-{uuid.uuid4().hex[:6]}"
    return w