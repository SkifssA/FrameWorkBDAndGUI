from fastapi import APIRouter, HTTPException, Request, Response, Form


from webapp.logic import templates, get_form, getHtmlNotMain, get_main_menu, get_session, remove_from
from core.sdk import eventSignal, typeEvent

router = APIRouter()

"""
--------------------------------------------------------
EndPoints для клиентских действий
--------------------------------------------------------
"""
@router.post("/api/close-form")
async def action_oper(request: Request, form_id: str = Form(...)):
    "Закрытие формы"
    name_form = remove_from(form_id)
    if name_form == '':
        get_session().main_menu_form.open()
    else:
        get_session().open_form[name_form].open()
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

@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameTab: str, sForm: str, oper: str):
    "Операции формы"
    form = get_form(f'{sNameTab}/{sForm}')
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}"
    )

"""
--------------------------------------------------------
EndPoints для первого открытия
--------------------------------------------------------
"""

@router.get('/{sNameMainMenu}')
async def openMainMenu(request: Request, sNameMainMenu:str):
    "Открытие главного меню"
    form = get_main_menu(sNameMainMenu=sNameMainMenu)
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/formOpenFrom.html",
                    context={
                        "meta_main_memu": form.getInfoMeta(),
                        "main_menu": form._get_parent_name(),
                    }
                )

@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}")
async def oper_form_endpoint(request: Request, sNameMainMenu:str, sNameTab: str, sForm: str):
    "Открытие формы"
    get_main_menu(sNameMainMenu=sNameMainMenu)
    return getHtmlNotMain(f'{sNameTab}/{sForm}')
        
