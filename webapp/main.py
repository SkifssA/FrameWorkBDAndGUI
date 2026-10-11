from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from core.sdk import ACTIONDISPATCHER

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")



@app.get("/{sNameTab}#{sForm}")
def read_item(sNameTab: str, sForm:str, request: Request):
    class_ = ACTIONDISPATCHER.getClassByName(f'{sNameTab}')
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            return templates.TemplateResponse(request=request, name=f"partials/{sForm.lower()}.html", context={
                "data": form.getData()
                , 'meta': form.getInfoMeta()
                , 'name': f'{sNameTab}%23{sForm}'
            })
        raise HTTPException(status_code=404, detail=f"Отображение {sForm} таблицы {sNameTab} не найдено")
    raise HTTPException(status_code=404, detail=f"Таблица {sNameTab} не найдена")

@app.get("/{sNameTab}#{sForm}/action/{oper}")
def read_item(sNameTab: str, sForm:str, oper: str):
    class_ = ACTIONDISPATCHER.getClassByName(f'{sNameTab}')
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            if oper in form.getSetterAndOperName():
                getattr(form.List(), oper)()
                return {"success": True, "operation": oper}
    raise HTTPException(status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}")

def runServer():
    import uvicorn
    # Запускаем uvicorn напрямую в этом же процессе
    # loop="asyncio" помогает избежать конфликта с patch_asyncio
    uvicorn.run(app, host="127.0.0.1", port=8000)