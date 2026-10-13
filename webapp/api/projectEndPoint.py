from fastapi import APIRouter, HTTPException, Request, Response, Cookie

from webapp.logic import templates, get_form, get_open_form, get_main_menu

router = APIRouter()

@router.get('/{sNameMainMenu}')
async def openMainMenu(request: Request, sNameMainMenu:str, session_id: str = Cookie(default="default")):
    form = get_main_menu(sNameMainMenu, session_id)
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/mainmenu.html",
                    context={
                        "data_main_memu": form.getData(),
                        "meta_main_memu": form.getInfoMeta(),
                    }
                )

@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}")
async def oper_form_endpoint(request: Request, sNameMainMenu:str, sNameTab: str, sForm: str, session_id: str = Cookie(default="default")):
    meta_main_memu = get_main_menu(sNameMainMenu, session_id).getInfoMeta()
    oper_form_object = get_form(session_id, f'{sNameTab}/{sForm}')
    forms = get_open_form(session_id)

    return templates.TemplateResponse(
        request=request,
        name=f"partials/{sForm.lower()}.html",
        context={
            "data": oper_form_object.getData(),
            "meta": oper_form_object.getInfoMeta(),
            "open_forms": forms,
            "active_form": f'{sNameTab}/{sForm}',
            "meta_main_memu": meta_main_memu,
            "main_menu": sNameMainMenu
        },
    )
        
@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameTab: str, sForm: str, oper: str, session_id: str = Cookie(default="default")):
    form = get_form(session_id, f'{sNameTab}/{sForm}')
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=200)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}"
    )