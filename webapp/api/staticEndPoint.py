from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse

from core.sdk import ACTIONDISPATCHER

from webapp.logic import templates, get_session_queue

router = APIRouter()

@router.get('/selectProject')
async def openMainMenu(request: Request):
    form = ACTIONDISPATCHER.getModulesConfig()
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/selectProject.html",
                    context={
                        "mata_app": form,
                    }
                )

@router.get("/events")
async def event_stream(request: Request):
    # Регистрируем сессию
    queues = get_session_queue()
    
    async def generate():
        queue = queues
        while True:
            if await request.is_disconnected():
                break
            data = await queue.get()
            yield data

    return EventSourceResponse(generate())