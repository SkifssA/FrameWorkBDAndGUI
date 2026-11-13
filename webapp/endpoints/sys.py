from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse

from core.sdk import SESSION_STAGE

from webapp.logic.procEvent import getHtmlForm

router = APIRouter()


@router.get("/")
async def start(request: Request):
    return getHtmlForm("main.html", {}, InStr=False)

@router.get("/events")
async def event_stream(request: Request):
    # Регистрируем сессию
    queues = SESSION_STAGE.get_queue()
    
    async def generate():
        queue = queues
        while True:
            if await request.is_disconnected():
                break
            data = await queue.get()
            yield data

    return EventSourceResponse(generate(), ping=None)