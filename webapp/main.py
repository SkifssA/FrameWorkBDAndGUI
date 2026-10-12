from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from module.bc import Bc_ScriptSchedulerPub


from core.sdk import ACTIONDISPATCHER, eventSignal

app = FastAPI()
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

templates = Jinja2Templates(directory="webapp/templates")

user_sessions: dict[str, dict[str, dict]] = {'default': {"Bc_ScriptSchedulerPub/List":Bc_ScriptSchedulerPub._getFormByName('List')()}}

def handler(sender, **kwargs):
    print(kwargs.get('fromEvent'))

eventSignal.connect(handler)

def validateOpenClass(sNameTab:str, sForm:str = 'Default'):
    class_ = ACTIONDISPATCHER.getClassByName(f"{sNameTab}")
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            return form
        raise HTTPException(
                status_code=404, detail=f"Отображение {sForm} класса {sNameTab} не найдено"
            )
    raise HTTPException(status_code=404, detail=f"Класс {sNameTab} не найден")

def get_open_form(session_id: str)->list[dict]:
    forms_data = user_sessions.get(session_id, {})
    return [{'caption': f_object.getInfoMeta()['metaForm']['caption'],
             'nameClass': f_name[:f_name.find('/')], 
             'nameForm': f_name[f_name.find('/')+1:], 
             'name': f_name} \
             for f_name, f_object in forms_data.items()]

def open_form(session_id: str, form_name:str):
    if session_id not in user_sessions:
        user_sessions[session_id] = {}

    if not any(f == form_name for f in user_sessions[session_id].keys()):
        user_sessions[session_id][form_name] = validateOpenClass(*form_name.split('/'))

    return user_sessions[session_id][form_name]

def remove_from(session_id:str, form_name:str):
    if session_id in user_sessions:
        user_sessions[session_id] = {f_name:f_data for f_name, f_data in user_sessions[session_id] if f_name != form_name}

@app.get("/{sNameMainMenu}/{sNameTab}/{sForm}")
async def oper_form_endpoint(request: Request, sNameMainMenu:str, sNameTab: str, sForm: str, session_id: str = Cookie(default="default")):
    meta_main_memu = validateOpenClass(sNameMainMenu).getInfoMeta()
    oper_form_object = open_form(session_id, f'{sNameTab}/{sForm}')
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
        
@app.get("/{sNameMainMenu}/{sNameTab}/{sForm}/action/{oper}")
async def action_oper(request: Request, sNameTab: str, sForm: str, oper: str, session_id: str = Cookie(default="default")):
    class_ = ACTIONDISPATCHER.getClassByName(f"{sNameTab}")
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            if oper in form.getSetterAndOperName():
                form.get_oper_handler()[oper]()
                return Response(content="", status_code=200)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}"
    )


@app.get('/{sNameMainMenu}')
def openMainMenu(request: Request, sNameMainMenu:str, session_id: str = Cookie(default="default")):
    form = validateOpenClass(sNameMainMenu)
    return templates.TemplateResponse(
                    request=request,
                    name=f"partials/mainmenu.html",
                    context={
                        "data": form.getData(),
                        "meta": form.getInfoMeta(),
                    }
                )

def runServer():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
