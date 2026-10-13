from fastapi import APIRouter, HTTPException, Request, Response


from webapp.logic import templates, get_form, get_open_form, get_main_menu

router = APIRouter()

@router.get('/{sNameMainMenu}')
async def openMainMenu(request: Request, sNameMainMenu:str):
    
    form = get_main_menu(sNameMainMenu=sNameMainMenu)
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/mainmenu.html",
                    context={
                        "data_main_memu": form.getData(),
                        "meta_main_memu": form.getInfoMeta(),
                    }
                )

@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}")
async def oper_form_endpoint(request: Request, sNameMainMenu:str, sNameTab: str, sForm: str):
    meta_main_memu = get_main_menu(sNameMainMenu=sNameMainMenu).getInfoMeta()
    oper_form_object = get_form(f'{sNameTab}/{sForm}')
    forms = get_open_form()

    return templates.TemplateResponse(
        request=request,
        name=f"partials/{sForm.lower()}.html",
        context={
            "data": oper_form_object.getData(),
            "meta": oper_form_object.getInfoMeta(),
            "open_forms": forms,
            "active_form": f'{sNameTab}/{sForm}',
            "meta_main_memu": meta_main_memu,
            "main_menu": sNameMainMenu,
            "partial": False
        },
    )
        
@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameTab: str, sForm: str, oper: str):
    form = get_form(f'{sNameTab}/{sForm}')
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=200)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}"
    )