from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse, ServerSentEvent

from core.sdk import ACTIONDISPATCHER, SESSION_STAGE

from webapp.logic import templates

router = APIRouter()

@router.get('/selectProject')
async def openMainMenu(request: Request):
    modules = ACTIONDISPATCHER.getModulesConfig()
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/selectProject.html",
                    context={
                        "meta_app": modules,
                        "isMain": True
                    }
                )

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