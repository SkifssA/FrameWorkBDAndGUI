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
async def close_form(request: Request, form_id: str = Form(...)):
    "Закрытие формы"
    get_form(form_id).close()
    return Response(content="", status_code=204)

@router.post("/api/selected-form")
async def selected_form(request: Request, form_id: str = Form(...)):
    "Переключение вкладки"
    get_form(form_id)._open_iu()
    return Response(content="", status_code=204)

@router.post('/api/selected-app')
async def selected_app(request: Request, form_id: str = Form(...)):
    "Открытие главного меню"
    form = get_main_menu(sNameMainMenu=form_id)
    eventSignal.send(fromEvent=form._get_form_event(typeEvent.openApp))
    return Response(content="", status_code=204)

@router.post('/api/set-attr')
async def set_attr(request: Request):
    "Установка значений в obj"
    form_data = await request.form()
    for key, value in form_data.items():
        event = SetterEvent(value=value)
        get_form(get_session().active_form).get_setter()[key]['method'](event)
    return Response(content="", status_code=204)

@router.post('/api/select-row')
async def select_row(request: Request, id_row: int = Form(...), form_id: str = Form(...)):
    "Установка выбраной строки"
    form_name = get_session().active_form
    if form:=get_session().open_form.get(form_name):
        form = form._get_children(form_id)
        form.active_row = id_row
    return Response(content="", status_code=204)

@router.post('/api/selected-form-ch')
async def selected_form_ch(request: Request, form_id: str = Form(...)):
    "Установка выбраной строки"
    form_name = get_session().active_form
    if form:=get_session().open_form.get(form_name):
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
    form = get_session().main_menu_form
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameMainMenu} не найдена опрерация {oper}"
    )

@router.post("/action/{oper}")
async def action_oper(request: Request, oper: str, form_id: str = Form(...)):
    "Операции формы"
    form_name = get_session().active_form
    if form:=get_session().open_form.get(form_name):
        form = form._get_children(form_id)
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
        
