from fastapi import APIRouter, HTTPException, Request, Response


from webapp.logic import templates, get_form, getHtmlNotMain, get_main_menu, get_session

router = APIRouter()

@router.get('/{sNameMainMenu}')
async def openMainMenu(request: Request, sNameMainMenu:str):
    form = get_main_menu(sNameMainMenu=sNameMainMenu)
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/formOpenFrom.html",
                    context={
                        "meta_main_memu": form.getInfoMeta(),
                        "main_menu": form._get_parent_name(),
                    }
                )

@router.get("/{sNameMainMenu}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameMainMenu:str, sForm: str, oper: str):
    form = get_session().main_menu_form
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameMainMenu} не найдена опрерация {oper}"
    )

@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}")
async def oper_form_endpoint(request: Request, sNameMainMenu:str, sNameTab: str, sForm: str):
    get_main_menu(sNameMainMenu=sNameMainMenu)
    return getHtmlNotMain(f'{sNameTab}/{sForm}')
        
@router.get("/{sNameMainMenu}/{sNameTab}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameTab: str, sForm: str, oper: str):
    form = get_form(f'{sNameTab}/{sForm}')
    if form:
        if oper in form.getSetterAndOperName():
            form.get_oper_handler()[oper]()
            return Response(content="", status_code=204)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}"
    )

