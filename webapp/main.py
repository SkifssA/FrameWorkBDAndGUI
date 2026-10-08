from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from core.sdk import ACTIONDISPATCHER

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")



@app.get("/api/open/{sNameTab}#{sForm}")
def read_item(sNameTab: str, request: Request):
    form = ACTIONDISPATCHER.getClassByName(f'{sNameTab}')
    if form:
        form = form.List()
        return templates.TemplateResponse(request=request, name="partials/list.html", context={
            "data": form.getData()
            , 'meta': form.getInfoMeta()
        })
    raise HTTPException(status_code=404, detail=f"Таблица {sNameTab} не найдена")

@app.get("/api/oper/{sNameTab}/{oper}")
def read_item(sNameTab: str, oper: str):
    form = ACTIONDISPATCHER.getClassByName(f'{sNameTab}')
    if form:
        idOpers = list(i['id'] for i in form.List().getInfoMeta()['operForm'])
        if oper in idOpers:
            ACTIONDISPATCHER.action(f'{sNameTab}.{oper}')
    raise HTTPException(status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}")

def runServer():
    import uvicorn
    # Запускаем uvicorn напрямую в этом же процессе
    # loop="asyncio" помогает избежать конфликта с patch_asyncio
    uvicorn.run(app, host="127.0.0.1", port=8000)