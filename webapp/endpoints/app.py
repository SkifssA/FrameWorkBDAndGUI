from fastapi import APIRouter, HTTPException, Request, Response, Form

from core.sdk import eventSignal, typeEvent, SetterEvent, SESSION_STAGE

router = APIRouter(prefix='/app')

@router.get("/{nameMainMenu}")
async def action_oper(request: Request, nameMainMenu: str):
    "Открытие главного меню приложения"
    form = SESSION_STAGE.get_main_menu(nameMainMenu)
    eventSignal.send(fromEvent=form._get_form_event(typeEvent=typeEvent.openApp))
    return Response(content="", status_code=204)
    