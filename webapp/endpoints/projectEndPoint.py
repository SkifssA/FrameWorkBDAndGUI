from fastapi import APIRouter, HTTPException, Request, Response, Form

from core.sdk import eventSignal, typeEvent, SetterEvent, SESSION_STAGE

router = APIRouter()

"""
--------------------------------------------------------
EndPoints для клиентских действий
--------------------------------------------------------
"""
@router.post("/api/close-form")
async def close_form(request: Request, form_id: str = Form(...)):
    "Закрытие формы"
    SESSION_STAGE.get_form(form_id).close()
    return Response(content="", status_code=204)

@router.post("/api/selected-form")
async def selected_form(request: Request, form_id: str = Form(...)):
    "Переключение вкладки"
    SESSION_STAGE.get_form(form_id)._open_ui()
    return Response(content="", status_code=204)

@router.post('/api/selected-app')
async def selected_app(request: Request, form_id: str = Form(...)):
    "Открытие главного меню"
    form = SESSION_STAGE.get_main_menu(sNameMainMenu=form_id)
    eventSignal.send(fromEvent=form._get_form_event(typeEvent.openApp))
    return Response(content="", status_code=204)

@router.post('/api/set-attr')
async def set_attr(request: Request):
    "Установка значений в obj"
    form_data = await request.form()
    for key, value in form_data.items():
        event = SetterEvent(value=value)
        SESSION_STAGE.get_active_form().get_setter()[key]['method'](event)
    return Response(content="", status_code=204)

@router.post('/api/select-row')
async def select_row(request: Request, id_row: int = Form(...), form_id: str = Form(...)):
    "Установка выбраной строки"
    if form:=SESSION_STAGE.get_active_form():
        form = form._get_children(form_id)
        form.active_row = id_row
    return Response(content="", status_code=204)

@router.post('/api/selected-form-ch')
async def selected_form_ch(request: Request, form_id: str = Form(...)):
    "Установка выбраной строки"
    if form:=SESSION_STAGE.get_active_form():
        form = form._get_children(form_id)
        form._open_ch()
    return Response(content="", status_code=204)


"""
--------------------------------------------------------
EndPoints для действий ядра
--------------------------------------------------------
"""
@router.get("/{sNameMainMenu}/{sForm}/action/{oper}")
async def mm_action_oper(request: Request, sNameMainMenu:str, sForm: str, oper: str):
    "Операции главного меню"
    form = SESSION_STAGE.get_main_menu()
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameMainMenu} не найдена операция {oper}"
    )

@router.post("/action/{oper}")
async def action_oper(request: Request, oper: str, form_id: str = Form(...)):
    "Операции формы"
    if form:=SESSION_STAGE.get_active_form():
        form = form._get_children(form_id)
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {SESSION_STAGE.get_active_form_name()} не найдена операция {oper}"
    )

"""
--------------------------------------------------------
EndPoints для первого открытия
--------------------------------------------------------
"""
        
