from fastapi import APIRouter, HTTPException, Request, Response, Form


from webapp.logic import templates, get_form, get_main_menu, get_session, remove_from
from core.sdk import eventSignal, typeEvent, SetterEvent

router = APIRouter()

"""
--------------------------------------------------------
EndPoints для клиентских действий
--------------------------------------------------------
"""
@router.post("/api/close-form")
async def action_oper(request: Request, form_id: str = Form(...)):
    "Закрытие формы"
    get_form(form_id).close()
    return Response(content="", status_code=204)

@router.post("/api/selected-form")
async def action_oper(request: Request, form_id: str = Form(...)):
    "Переключение вкладки"
    get_form(form_id).open()
    return Response(content="", status_code=204)

@router.post('/api/selected-app')
async def openMainMenu(request: Request, form_id: str = Form(...)):
    "Открытие главного меню"
    form = get_main_menu(sNameMainMenu=form_id)
    eventSignal.send(fromEvent=form.object._get_form_event(typeEvent.openApp))
    return Response(content="", status_code=204)

@router.post('/api/set-attr')
async def openMainMenu(request: Request):
    "Установка значений в obj"
    form_data = await request.form()
    for key, value in form_data.items():
        event = SetterEvent(value=value)
        get_form(get_session().active_form).get_setter()[key]['method'](event)
    return Response(content="", status_code=204)

@router.post('/api/select-row')
async def openMainMenu(request: Request, id_row: int = Form(...)):
    "Установка выбраной строки"
    get_form(get_session().active_form).object.active_row = id_row
    return Response(content="", status_code=204)

"""
--------------------------------------------------------
EndPoints для действий ядра
--------------------------------------------------------
"""
@router.get("/{sNameMainMenu}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameMainMenu:str, sForm: str, oper: str):
    "Операции главного меню"
    form = get_session().main_menu_form
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameMainMenu} не найдена опрерация {oper}"
    )

@router.get("/action/{oper}")
async def action_oper(request: Request, oper: str):
    "Операции формы"
    form_name = get_session().active_form
    if form:=get_session().open_form.get(form_name):
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {form_name} не найдена опрерация {oper}"
    )

"""
--------------------------------------------------------
EndPoints для первого открытия
--------------------------------------------------------
"""
        
