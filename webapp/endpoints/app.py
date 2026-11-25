from fastapi import APIRouter, HTTPException, Request, Response, Body

from core.sdk import eventSignal, typeEvent, SetterEvent, SESSION_STAGE

router = APIRouter(prefix='/app')

@router.post("/close_tab")
async def close_tab(request: Request, tab_name: str = Body(..., embed=True)):
    app = SESSION_STAGE.get_app()
    app._children.pop(tab_name)
    return Response(content="", status_code=204)

@router.get("/{nameMainMenu}")
async def action_oper(request: Request, nameMainMenu: str):
    "Открытие главного меню приложения"
    form = SESSION_STAGE.get_app(nameMainMenu)
    eventSignal.send(fromEvent=form._get_form_event(typeEvent=typeEvent.openApp))
    return Response(content="", status_code=204)


@router.get("/{nameClass}/action/{nameOper}")
async def mm_action_oper(request: Request, nameClass:str, nameOper: str):
    "Операции главного меню"
    if form:=SESSION_STAGE.get_app():
        form = form._children._get_children(f'{nameClass}')
        if nameOper in form.getSetterAndOperName():
            form.get_oper_handler()[nameOper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В отображении {nameClass} не найдена операция {nameOper}"
    )